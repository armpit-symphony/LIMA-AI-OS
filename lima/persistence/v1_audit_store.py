"""Explicit local audit store for V1-G12 redacted records.

This module writes only sanitized V1-G12 audit/evidence records to a caller
provided local directory. It does not use external databases, migrations,
queues, workers, subprocesses, threads, or any live connector.
"""

from __future__ import annotations

from collections.abc import Mapping
import json
from pathlib import Path
from typing import Any, Final

from lima.spine.v1_audit_evidence import V1AuditEvidenceError, validate_v1_audit_record


STORE_FILENAME: Final[str] = "v1_audit_records.jsonl"


class V1AuditStoreError(ValueError):
    """Raised when the V1 local audit store fails closed."""


class V1LocalAuditStore:
    """Append-only local store for redacted V1 audit/evidence records."""

    def __init__(self, store_dir: str | Path) -> None:
        if not isinstance(store_dir, (str, Path)) or not str(store_dir).strip():
            raise V1AuditStoreError("store_dir must be an explicit local path")
        self._store_dir = Path(store_dir)
        self._records_path = self._store_dir / STORE_FILENAME

    @property
    def store_dir(self) -> Path:
        """Return the explicit local audit-store directory."""

        return self._store_dir

    @property
    def records_path(self) -> Path:
        """Return the append-only JSONL record path."""

        return self._records_path

    def append_record(self, record: Mapping[str, Any]) -> dict[str, Any]:
        """Append a sanitized record and return a non-authorizing ack."""

        sanitized = self._validate_record(record)
        record_key = _record_key(sanitized)
        if any(_record_key(existing) == record_key for existing in self._read_all_records()):
            raise V1AuditStoreError("audit records are append-only; duplicate record rejected")

        self._store_dir.mkdir(parents=True, exist_ok=True)
        self._ensure_records_path_is_inside_store()
        with self._records_path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(sanitized, sort_keys=True, separators=(",", ":")))
            handle.write("\n")

        return {
            "stored": True,
            "record_key": record_key,
            "record_hash": sanitized["record_hash"],
            "store_path_ref": f"local-audit-store:{STORE_FILENAME}",
            "audit_record_is_authority": False,
            "execution_allowed": False,
            "approval_token_issued": False,
        }

    def get_by_event_id(
        self,
        event_id: str,
        *,
        tenant_ref: str,
        shell_id: str,
    ) -> dict[str, Any] | None:
        """Return one redacted event record within tenant/shell scope."""

        return self._lookup_one(
            "event_id",
            event_id,
            tenant_ref=tenant_ref,
            shell_id=shell_id,
            record_type="v1_audit_event",
        )

    def get_by_lineage_id(
        self,
        lineage_id: str,
        *,
        tenant_ref: str,
        shell_id: str,
    ) -> tuple[dict[str, Any], ...]:
        """Return redacted records for one lineage within tenant/shell scope."""

        return self._lookup_many("lineage_id", lineage_id, tenant_ref=tenant_ref, shell_id=shell_id)

    def get_by_decision_id(
        self,
        decision_id: str,
        *,
        tenant_ref: str,
        shell_id: str,
    ) -> tuple[dict[str, Any], ...]:
        """Return redacted records for one decision within tenant/shell scope."""

        return self._lookup_many("decision_id", decision_id, tenant_ref=tenant_ref, shell_id=shell_id)

    def _lookup_one(
        self,
        field_name: str,
        value: str,
        *,
        tenant_ref: str,
        shell_id: str,
        record_type: str | None = None,
    ) -> dict[str, Any] | None:
        matches = self._lookup_many(
            field_name,
            value,
            tenant_ref=tenant_ref,
            shell_id=shell_id,
            record_type=record_type,
        )
        if not matches:
            return None
        if len(matches) > 1:
            raise V1AuditStoreError("scoped lookup returned multiple records")
        return matches[0]

    def _lookup_many(
        self,
        field_name: str,
        value: str,
        *,
        tenant_ref: str,
        shell_id: str,
        record_type: str | None = None,
    ) -> tuple[dict[str, Any], ...]:
        normalized_value = _required_text(value, field_name)
        normalized_tenant = _required_text(tenant_ref, "tenant_ref")
        normalized_shell = _required_text(shell_id, "shell_id")

        scoped_matches: list[dict[str, Any]] = []
        scope_mismatch = False
        for record in self._read_all_records():
            if record_type is not None and record.get("record_type") != record_type:
                continue
            if record.get(field_name) != normalized_value:
                continue
            if record.get("tenant_ref") == normalized_tenant and record.get("shell_id") == normalized_shell:
                scoped_matches.append(record)
            else:
                scope_mismatch = True

        if scope_mismatch and not scoped_matches:
            raise V1AuditStoreError("cross-tenant or cross-shell lookup denied")
        return tuple(scoped_matches)

    def _read_all_records(self) -> tuple[dict[str, Any], ...]:
        if not self._records_path.exists():
            return ()
        self._ensure_records_path_is_inside_store()

        records: list[dict[str, Any]] = []
        with self._records_path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if not line.strip():
                    continue
                try:
                    raw_record = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise V1AuditStoreError("audit store contains invalid JSON") from exc
                records.append(self._validate_record(raw_record))
        return tuple(records)

    def _validate_record(self, record: Mapping[str, Any]) -> dict[str, Any]:
        try:
            return validate_v1_audit_record(record)
        except V1AuditEvidenceError as exc:
            raise V1AuditStoreError(str(exc)) from exc

    def _ensure_records_path_is_inside_store(self) -> None:
        store_dir = self._store_dir.resolve()
        records_path = self._records_path.resolve()
        if records_path.parent != store_dir:
            raise V1AuditStoreError("audit store writes must stay inside store_dir")


def _record_key(record: Mapping[str, Any]) -> str:
    record_type = _required_text(record.get("record_type"), "record_type")
    if record_type == "v1_audit_event":
        return f"event:{_required_text(record.get('event_id'), 'event_id')}"
    if record_type == "v1_audit_lineage":
        return f"lineage:{_required_text(record.get('lineage_id'), 'lineage_id')}"
    raise V1AuditStoreError("unsupported record type")


def _required_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise V1AuditStoreError(f"{field_name} is required")
    return value.strip()
