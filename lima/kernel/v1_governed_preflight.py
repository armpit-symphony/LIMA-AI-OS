"""V1 governed preflight runner.

This module composes the existing candidate, Guardian, and audit slices into
one caller-facing runtime entry point. It does not execute tools, call model
providers, mutate files, invoke connectors, or create approval tokens.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
from typing import Any, Protocol

from lima.contracts.guardian import ConsequentialActionRequest, GuardianDecision
from lima.guardian import review_v1_runtime_request
from lima.spine import build_v1_audit_event_record, build_v1_audit_lineage_record

from .v1_runtime_request import build_v1_runtime_request


class V1GovernedPreflightError(ValueError):
    """Raised when the governed preflight runner cannot proceed safely."""


class V1AuditAppendStore(Protocol):
    """Minimal append-only audit store surface required by this runner."""

    def append_record(self, record: Mapping[str, Any]) -> Mapping[str, Any]:
        """Append one sanitized audit record and return a non-authorizing ack."""


@dataclass(frozen=True)
class V1GovernedPreflightResult:
    """Composed non-executing result for one candidate preflight."""

    request: ConsequentialActionRequest
    decision: GuardianDecision
    audit_event_record: Mapping[str, Any]
    audit_lineage_record: Mapping[str, Any]
    audit_store_acks: tuple[Mapping[str, Any], ...] = ()
    execution_allowed: bool = False
    side_effects_allowed: bool = False
    provider_model_routed: bool = False
    shell_wired: bool = False


def run_v1_governed_preflight(
    candidate: Mapping[str, Any],
    *,
    tenant_ref: str,
    actor_ref: str | None = None,
    occurred_at: str | None = None,
    event_id: str | None = None,
    privacy_class: str = "internal",
    redaction_class: str = "summary_only",
    retention_class: str = "standard",
    visibility_class: str = "security_view",
    content_refs: Sequence[str] = (),
    audit_store: V1AuditAppendStore | None = None,
) -> V1GovernedPreflightResult:
    """Run one normalized candidate through request, Guardian, and audit slices.

    The returned result is proof/evidence for a governed preflight only. It is
    intentionally not execution authority for model calls, tool calls, file
    mutations, connector access, network activity, or shell wiring.
    """

    normalized_tenant_ref = _required_text(tenant_ref, "tenant_ref")
    request = build_v1_runtime_request(candidate)
    decision = review_v1_runtime_request(request)
    normalized_occurred_at = occurred_at or _utc_now()
    normalized_actor_ref = actor_ref or f"actor:{request.actor_id}"

    audit_metadata = {
        "event_id": event_id
        or _stable_id(
            "event:v1-governed-preflight",
            f"{request.request_id}:{decision.decision_id}:{normalized_occurred_at}",
        ),
        "tenant_ref": normalized_tenant_ref,
        "actor_ref": _required_text(normalized_actor_ref, "actor_ref"),
        "occurred_at": _required_text(normalized_occurred_at, "occurred_at"),
        "privacy_class": privacy_class,
        "redaction_class": redaction_class,
        "retention_class": retention_class,
        "visibility_class": visibility_class,
        "evidence_refs": tuple(request.evidence_refs),
        "redacted_summary": _redacted_summary(request, decision),
        "content_refs": _string_sequence(content_refs, "content_refs"),
    }

    event_record = build_v1_audit_event_record(request, decision, audit_metadata)
    lineage_record = build_v1_audit_lineage_record(event_record)
    audit_store_acks: tuple[Mapping[str, Any], ...] = ()

    if audit_store is not None:
        event_ack = dict(audit_store.append_record(event_record))
        lineage_ack = dict(audit_store.append_record(lineage_record))
        audit_store_acks = (event_ack, lineage_ack)

    return V1GovernedPreflightResult(
        request=request,
        decision=decision,
        audit_event_record=event_record,
        audit_lineage_record=lineage_record,
        audit_store_acks=audit_store_acks,
    )


def _redacted_summary(
    request: ConsequentialActionRequest,
    decision: GuardianDecision,
) -> str:
    linkage = decision.metadata.get("audit_evidence_linkage")
    if isinstance(linkage, Mapping):
        summary = linkage.get("redacted_summary")
        if isinstance(summary, str) and summary.strip():
            return summary.strip()
    target_ref = request.target_ref or "no-target"
    return f"{request.action_type.value}:{target_ref}"


def _required_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise V1GovernedPreflightError(f"{field_name} is required")
    return value.strip()


def _string_sequence(value: Sequence[str], field_name: str) -> tuple[str, ...]:
    if isinstance(value, (str, bytes, bytearray)) or not isinstance(value, Sequence):
        raise V1GovernedPreflightError(f"{field_name} must be a sequence")
    return tuple(str(item).strip() for item in value if str(item).strip())


def _stable_id(prefix: str, value: str) -> str:
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]
    return f"{prefix}:{digest}"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
