"""V1 local document harness.

This module is a candidate-only, Guardian-gated read-only document inspection
helper for local PC testing. It reads a single operator-supplied local document
after a non-executing GuardianDecision preflight and returns bounded metadata
plus a short preview. It does not write files, delete files, call providers,
invoke connectors, persist audit records, or claim production readiness.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile
from typing import Any, Final
from xml.etree import ElementTree

from lima.contracts.guardian import (
    ConsequentialActionRequest,
    ConsequentialActionType,
    GuardianDecision,
    GuardianDecisionStatus,
)
from lima.guardian.v1_decision_gate import review_v1_runtime_request


SCHEMA_VERSION: Final[str] = "v1-local-document-harness-candidate"
DEFAULT_MAX_BYTES: Final[int] = 2_000_000
DEFAULT_MAX_PREVIEW_CHARS: Final[int] = 1200
TEXT_EXTENSIONS: Final[frozenset[str]] = frozenset(
    {".txt", ".md", ".csv", ".json", ".log", ".xml", ".html", ".htm"}
)
SUPPORTED_EXTENSIONS: Final[frozenset[str]] = TEXT_EXTENSIONS | frozenset(
    {".docx", ".pdf"}
)


class V1LocalDocumentHarnessError(ValueError):
    """Raised when local document inspection cannot proceed safely."""


def build_v1_local_document_request(
    document_path: str | Path,
    *,
    actor_id: str = "local-operator",
    shell_id: str = "local-pc-document-harness",
    request_id: str | None = None,
) -> ConsequentialActionRequest:
    """Build the non-executing Guardian preflight request used by the CLI."""

    target_ref = _target_ref(document_path)
    normalized_request_id = request_id or _stable_id("v1-local-doc-request", target_ref)
    return ConsequentialActionRequest(
        request_id=normalized_request_id,
        intent_id="intent:v1-local-document-harness",
        input_id="input:v1-local-document-harness",
        actor_id=actor_id,
        shell_id=shell_id,
        action_type=ConsequentialActionType.FILE_OPERATION,
        target_ref=target_ref,
        requested_tool_pack="files",
        risk_class="read_only",
        typed_args={
            "operation": "read_only_document_inspection",
            "destructive": False,
            "approved": False,
        },
        evidence_refs=("evidence:v1-local-document-harness:operator-supplied-path",),
        metadata={
            "v1_runtime_slice": "typed_request_guardian_decision_preflight",
            "v1_action_category": "informational",
            "execution_allowed": False,
            "side_effects_allowed": False,
            "approval_token_issued": False,
            "audit_evidence_linkage": {
                "lineage_id": "lineage:v1-local-document-harness",
                "redacted_summary": "local read-only document inspection preflight",
            },
        },
    )


def inspect_v1_local_document(
    document_path: str | Path,
    *,
    guardian_decision: GuardianDecision,
    tenant_ref: str = "tenant:local-test",
    allowed_root: str | Path | None = None,
    max_bytes: int = DEFAULT_MAX_BYTES,
    max_preview_chars: int = DEFAULT_MAX_PREVIEW_CHARS,
) -> dict[str, Any]:
    """Return a deterministic read-only local document inspection record."""

    _validate_guardian_decision(guardian_decision)
    if not isinstance(max_bytes, int) or max_bytes <= 0:
        raise V1LocalDocumentHarnessError("max_bytes must be a positive integer")
    if not isinstance(max_preview_chars, int) or max_preview_chars < 0:
        raise V1LocalDocumentHarnessError(
            "max_preview_chars must be a non-negative integer"
        )

    path = _resolve_document_path(document_path, allowed_root)
    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise V1LocalDocumentHarnessError("unsupported document extension")

    stat = path.stat()
    if stat.st_size > max_bytes:
        raise V1LocalDocumentHarnessError("document exceeds max_bytes")

    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    preview, parser = _preview_for_document(path, data, max_preview_chars)

    record = {
        "record_type": "v1_local_document_harness_result",
        "schema_version": SCHEMA_VERSION,
        "candidate_only": True,
        "local_only": True,
        "guardian_gated": True,
        "read_only": True,
        "dry_run": True,
        "tenant_ref": tenant_ref,
        "actor_id": guardian_decision.actor_id,
        "shell_id": guardian_decision.shell_id,
        "decision_id": guardian_decision.decision_id,
        "decision_status": guardian_decision.status.value,
        "target_ref": _target_ref(path),
        "file_name": path.name,
        "extension": suffix,
        "size_bytes": stat.st_size,
        "sha256": digest,
        "parser": parser,
        "preview_char_count": len(preview),
        "preview_text": preview,
        "execution_allowed": False,
        "side_effects_allowed": False,
        "file_read": True,
        "file_written": False,
        "file_deleted": False,
        "file_mutated": False,
        "provider_model_routed": False,
        "provider_called": False,
        "network_action_executed": False,
        "connector_invoked": False,
        "audit_persisted": False,
        "product_ready": False,
        "metadata": {
            "v1_runtime_slice": "local_document_harness",
            "preview_bounded": True,
            "max_preview_chars": max_preview_chars,
            "max_bytes": max_bytes,
            "proof_not_authority": True,
        },
    }
    record["record_hash"] = _record_hash(record)
    return record


def _validate_guardian_decision(decision: GuardianDecision) -> None:
    if not isinstance(decision, GuardianDecision):
        raise V1LocalDocumentHarnessError("guardian_decision is required")
    if decision.status is not GuardianDecisionStatus.APPROVED:
        raise V1LocalDocumentHarnessError("guardian decision must be approved")
    if decision.action_type is not ConsequentialActionType.FILE_OPERATION:
        raise V1LocalDocumentHarnessError("guardian decision must cover a file operation")
    if decision.constraints.get("v1_preflight_only") is not True:
        raise V1LocalDocumentHarnessError("guardian decision must be V1 preflight")
    if decision.constraints.get("execution_allowed") is not False:
        raise V1LocalDocumentHarnessError("guardian decision cannot allow execution")
    if decision.constraints.get("side_effects_allowed") is not False:
        raise V1LocalDocumentHarnessError("guardian decision cannot allow side effects")
    if decision.constraints.get("approval_token_issued") is not False:
        raise V1LocalDocumentHarnessError("approval tokens are not accepted")
    if decision.allowed_tool_packs:
        raise V1LocalDocumentHarnessError("tool packs cannot be enabled")


def _resolve_document_path(
    document_path: str | Path,
    allowed_root: str | Path | None,
) -> Path:
    if not isinstance(document_path, (str, Path)) or not str(document_path).strip():
        raise V1LocalDocumentHarnessError("document_path is required")
    path = Path(document_path).expanduser().resolve(strict=True)
    if not path.is_file():
        raise V1LocalDocumentHarnessError("document_path must be a file")
    if allowed_root is not None:
        root = Path(allowed_root).expanduser().resolve(strict=True)
        try:
            path.relative_to(root)
        except ValueError as exc:
            raise V1LocalDocumentHarnessError(
                "document_path must be inside allowed_root"
            ) from exc
    return path


def _preview_for_document(
    path: Path,
    data: bytes,
    max_preview_chars: int,
) -> tuple[str, str]:
    suffix = path.suffix.lower()
    if max_preview_chars == 0:
        return "", "metadata_only"
    if suffix in TEXT_EXTENSIONS:
        return _truncate(data.decode("utf-8", errors="replace"), max_preview_chars), "text"
    if suffix == ".docx":
        return _truncate(_extract_docx_text(path), max_preview_chars), "docx_xml_text"
    if suffix == ".pdf":
        page_count = len(re.findall(rb"/Type\s*/Page\b", data))
        preview = f"PDF metadata: {len(data)} bytes; page markers detected: {page_count}."
        return _truncate(preview, max_preview_chars), "pdf_metadata"
    raise V1LocalDocumentHarnessError("unsupported document extension")


def _extract_docx_text(path: Path) -> str:
    try:
        with zipfile.ZipFile(path) as archive:
            document_xml = archive.read("word/document.xml")
    except (KeyError, zipfile.BadZipFile) as exc:
        raise V1LocalDocumentHarnessError("invalid docx document") from exc

    try:
        root = ElementTree.fromstring(document_xml)
    except ElementTree.ParseError as exc:
        raise V1LocalDocumentHarnessError("invalid docx XML") from exc

    parts = [node.text.strip() for node in root.iter() if node.text and node.text.strip()]
    return " ".join(parts)


def _truncate(value: str, max_chars: int) -> str:
    value = " ".join(value.replace("\r", "\n").split())
    if len(value) <= max_chars:
        return value
    return value[: max_chars - 3].rstrip() + "..."


def _target_ref(document_path: str | Path) -> str:
    return f"local-document:{Path(document_path).name}"


def _stable_id(prefix: str, value: str) -> str:
    return f"{prefix}:{hashlib.sha256(value.encode('utf-8')).hexdigest()[:16]}"


def _record_hash(record: dict[str, Any]) -> str:
    sanitized = {key: value for key, value in record.items() if key != "record_hash"}
    encoded = json.dumps(sanitized, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the V1 local document harness.")
    parser.add_argument("--path", required=True, help="Local document path to inspect.")
    parser.add_argument("--allowed-root", help="Optional root that must contain the file.")
    parser.add_argument("--actor-id", default="local-operator")
    parser.add_argument("--shell-id", default="local-pc-document-harness")
    parser.add_argument("--tenant-ref", default="tenant:local-test")
    parser.add_argument("--max-bytes", type=int, default=DEFAULT_MAX_BYTES)
    parser.add_argument("--max-preview-chars", type=int, default=DEFAULT_MAX_PREVIEW_CHARS)
    args = parser.parse_args(argv)

    request = build_v1_local_document_request(
        args.path,
        actor_id=args.actor_id,
        shell_id=args.shell_id,
    )
    decision = review_v1_runtime_request(request)
    record = inspect_v1_local_document(
        args.path,
        guardian_decision=decision,
        tenant_ref=args.tenant_ref,
        allowed_root=args.allowed_root,
        max_bytes=args.max_bytes,
        max_preview_chars=args.max_preview_chars,
    )
    json.dump(record, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
