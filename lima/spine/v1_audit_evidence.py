"""V1 durable audit/evidence record builders.

This module is the approved V1-G12 runtime slice boundary. It turns
already-reviewed V1 request and GuardianDecision metadata into redacted
audit/evidence records. It does not approve, execute, route providers,
wire shells, read raw content, or perform persistence by itself.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import hashlib
import json
from typing import Any, Final

from lima.contracts.guardian import (
    ConsequentialActionRequest,
    ConsequentialActionType,
    GuardianDecision,
    GuardianDecisionStatus,
)


SCHEMA_VERSION: Final[str] = "v1-g12-candidate"
ALLOWED_PRIVACY_CLASSES: Final[frozenset[str]] = frozenset(
    {"public", "internal", "private", "confidential"}
)
ALLOWED_REDACTION_CLASSES: Final[frozenset[str]] = frozenset(
    {"summary_only", "reference_only", "hash_only", "masked"}
)
ALLOWED_RETENTION_CLASSES: Final[frozenset[str]] = frozenset(
    {"ephemeral", "short", "standard", "extended"}
)
ALLOWED_VISIBILITY_CLASSES: Final[frozenset[str]] = frozenset(
    {"operator_view", "admin_view", "security_view", "system_only"}
)
RAW_SENSITIVE_KEYS: Final[frozenset[str]] = frozenset(
    {
        "api_key",
        "approval_pin",
        "approval_token",
        "customer_data",
        "file_contents",
        "message_text",
        "operator_pin",
        "password",
        "pin",
        "prompt",
        "provider_credentials",
        "raw_approval_pin",
        "raw_approval_token",
        "raw_customer_data",
        "raw_file_contents",
        "raw_human_input",
        "raw_prompt",
        "raw_secret",
        "raw_text",
        "secret",
        "secret_value",
        "token",
        "transcript",
    }
)
RAW_SENSITIVE_VALUE_MARKERS: Final[tuple[str, ...]] = (
    "raw-secret-",
    "raw secret",
    "approval-pin",
    "approval token",
    "raw prompt",
    "raw file contents",
    "raw customer data",
)
FORBIDDEN_TRUE_CLAIM_KEYS: Final[frozenset[str]] = frozenset(
    {
        "approved_for_execution",
        "audit_record_is_authority",
        "browser_action_executed",
        "connector_invoked",
        "device_command_invoked",
        "execution_allowed",
        "file_mutation_executed",
        "humaninput_bridge_activated",
        "model_routed",
        "network_action_executed",
        "physical_world_invoked",
        "provider_model_routed",
        "robotics_invoked",
        "shell_wired",
        "side_effects_allowed",
        "tool_executed",
    }
)


class V1AuditEvidenceError(ValueError):
    """Raised when metadata cannot enter the V1-G12 audit/evidence slice."""


def build_v1_audit_event_record(
    request: ConsequentialActionRequest,
    decision: GuardianDecision,
    metadata: Mapping[str, Any],
) -> dict[str, Any]:
    """Build a redacted audit event record from reviewed V1 request metadata."""

    if not isinstance(metadata, Mapping):
        raise V1AuditEvidenceError("metadata must be a mapping")

    _validate_reviewed_request_decision(request, decision)
    _reject_raw_sensitive_content(metadata)
    _reject_external_or_authority_claims(metadata)

    linkage = _decision_linkage(decision)
    lineage_id = _required_text(metadata.get("lineage_id") or linkage.get("lineage_id"), "lineage_id")
    event_id = _required_text(metadata.get("event_id"), "event_id")
    tenant_ref = _required_text(metadata.get("tenant_ref"), "tenant_ref")
    actor_ref = _required_text(metadata.get("actor_ref"), "actor_ref")
    occurred_at = _required_text(metadata.get("occurred_at"), "occurred_at")
    redacted_summary = _required_text(
        metadata.get("redacted_summary") or linkage.get("redacted_summary"),
        "redacted_summary",
    )
    privacy_class = _required_enum(
        metadata.get("privacy_class"),
        ALLOWED_PRIVACY_CLASSES,
        "privacy_class",
    )
    redaction_class = _required_enum(
        metadata.get("redaction_class"),
        ALLOWED_REDACTION_CLASSES,
        "redaction_class",
    )
    retention_class = _required_enum(
        metadata.get("retention_class"),
        ALLOWED_RETENTION_CLASSES,
        "retention_class",
    )
    visibility_class = _required_enum(
        metadata.get("visibility_class"),
        ALLOWED_VISIBILITY_CLASSES,
        "visibility_class",
    )
    evidence_refs = _evidence_refs(request, decision, metadata)
    approval_id, approval_evidence_ref = _approval_evidence_if_required(
        request,
        metadata,
        evidence_refs,
    )

    record = {
        "record_type": "v1_audit_event",
        "schema_version": SCHEMA_VERSION,
        "event_id": event_id,
        "lineage_id": lineage_id,
        "tenant_ref": tenant_ref,
        "actor_ref": actor_ref,
        "actor_id": _required_text(decision.actor_id, "actor_id"),
        "shell_id": _required_text(decision.shell_id, "shell_id"),
        "request_id": _required_text(request.request_id, "request_id"),
        "input_id": _optional_text(request.input_id),
        "intent_id": _optional_text(request.intent_id),
        "decision_id": _required_text(decision.decision_id, "decision_id"),
        "approval_id": approval_id,
        "approval_evidence_ref": approval_evidence_ref,
        "event_type": "guardian_decision",
        "event_status": _audit_status(decision.status),
        "decision_status": decision.status.value,
        "approval_level": _optional_text(decision.approval_level),
        "action_type": request.action_type.value,
        "target_ref": _optional_text(request.target_ref),
        "risk_class": _required_text(decision.risk_class, "risk_class"),
        "privacy_class": privacy_class,
        "redaction_class": redaction_class,
        "retention_class": retention_class,
        "visibility_class": visibility_class,
        "content_refs": list(_string_sequence(metadata.get("content_refs", ()), "content_refs")),
        "secret_refs": [],
        "evidence_refs": list(evidence_refs),
        "redacted_summary": redacted_summary,
        "occurred_at": occurred_at,
        "contains_secret": False,
        "contains_biometric": False,
        "contains_safety_critical": False,
        "audit_record_is_authority": False,
        "execution_allowed": False,
        "side_effects_allowed": False,
        "approval_token_issued": False,
        "provider_model_routed": False,
        "shell_wired": False,
        "metadata": {
            "v1_runtime_slice": "durable_audit_evidence_persistence",
            "source_runtime_slice": request.metadata.get("v1_runtime_slice"),
            "redacted": True,
            "append_only_required": True,
            "proof_not_authority": True,
        },
    }
    record["record_hash"] = _record_hash(record)
    return validate_v1_audit_record(record)


def build_v1_audit_lineage_record(event_record: Mapping[str, Any]) -> dict[str, Any]:
    """Build a redacted lineage record from a validated V1 audit event."""

    event = validate_v1_audit_record(event_record)
    if event["record_type"] != "v1_audit_event":
        raise V1AuditEvidenceError("lineage records require a v1 audit event")

    record = {
        "record_type": "v1_audit_lineage",
        "schema_version": SCHEMA_VERSION,
        "lineage_id": event["lineage_id"],
        "tenant_ref": event["tenant_ref"],
        "actor_ref": event["actor_ref"],
        "actor_id": event["actor_id"],
        "shell_id": event["shell_id"],
        "root_event_id": event["event_id"],
        "latest_event_id": event["event_id"],
        "event_ids": [event["event_id"]],
        "input_id": event["input_id"],
        "intent_id": event["intent_id"],
        "decision_id": event["decision_id"],
        "approval_id": event["approval_id"],
        "risk_class": event["risk_class"],
        "status": event["event_status"],
        "privacy_class": event["privacy_class"],
        "redaction_class": event["redaction_class"],
        "retention_class": event["retention_class"],
        "visibility_class": event["visibility_class"],
        "evidence_refs": list(event["evidence_refs"]),
        "redacted_summary": event["redacted_summary"],
        "created_at": event["occurred_at"],
        "updated_at": event["occurred_at"],
        "audit_record_is_authority": False,
        "execution_allowed": False,
        "approval_token_issued": False,
        "metadata": {
            "v1_runtime_slice": "durable_audit_evidence_persistence",
            "redacted": True,
            "proof_not_authority": True,
        },
    }
    record["record_hash"] = _record_hash(record)
    return validate_v1_audit_record(record)


def validate_v1_audit_record(record: Mapping[str, Any]) -> dict[str, Any]:
    """Return a redacted audit record copy or fail closed."""

    if not isinstance(record, Mapping):
        raise V1AuditEvidenceError("audit record must be a mapping")

    _reject_raw_sensitive_content(record)
    _reject_external_or_authority_claims(record)
    normalized = dict(record)
    record_type = _required_text(normalized.get("record_type"), "record_type")

    required_fields = (
        "schema_version",
        "lineage_id",
        "tenant_ref",
        "actor_ref",
        "actor_id",
        "shell_id",
        "decision_id",
        "risk_class",
        "privacy_class",
        "redaction_class",
        "retention_class",
        "visibility_class",
        "evidence_refs",
        "redacted_summary",
        "record_hash",
    )
    for field_name in required_fields:
        _required_text_or_sequence(normalized.get(field_name), field_name)

    if normalized["schema_version"] != SCHEMA_VERSION:
        raise V1AuditEvidenceError("unsupported schema_version")
    if normalized.get("audit_record_is_authority") is not False:
        raise V1AuditEvidenceError("audit records are proof, not authority")
    if normalized.get("execution_allowed") is not False:
        raise V1AuditEvidenceError("audit records cannot allow execution")
    if normalized.get("approval_token_issued") is not False:
        raise V1AuditEvidenceError("audit records cannot issue approval tokens")
    if normalized.get("contains_secret") is True:
        raise V1AuditEvidenceError("raw secret persistence is not allowed")

    if record_type == "v1_audit_event":
        _required_text(normalized.get("event_id"), "event_id")
        _required_text(normalized.get("request_id"), "request_id")
        _required_text(normalized.get("event_status"), "event_status")
        _required_text(normalized.get("action_type"), "action_type")
        _required_text(normalized.get("occurred_at"), "occurred_at")
    elif record_type == "v1_audit_lineage":
        _required_text(normalized.get("root_event_id"), "root_event_id")
        _required_text(normalized.get("latest_event_id"), "latest_event_id")
        _required_text_or_sequence(normalized.get("event_ids"), "event_ids")
        _required_text(normalized.get("created_at"), "created_at")
        _required_text(normalized.get("updated_at"), "updated_at")
    else:
        raise V1AuditEvidenceError("unsupported audit record type")

    expected_hash = _record_hash({key: value for key, value in normalized.items() if key != "record_hash"})
    if normalized["record_hash"] != expected_hash:
        raise V1AuditEvidenceError("record_hash does not match sanitized record")

    return normalized


def _validate_reviewed_request_decision(
    request: ConsequentialActionRequest,
    decision: GuardianDecision,
) -> None:
    if not isinstance(request, ConsequentialActionRequest):
        raise V1AuditEvidenceError("request must be a ConsequentialActionRequest")
    if not isinstance(decision, GuardianDecision):
        raise V1AuditEvidenceError("decision must be a GuardianDecision")
    if decision.request_id != request.request_id:
        raise V1AuditEvidenceError("decision request_id must match request")
    if decision.input_id != request.input_id:
        raise V1AuditEvidenceError("decision input_id must match request")
    if decision.intent_id != request.intent_id:
        raise V1AuditEvidenceError("decision intent_id must match request")
    if decision.actor_id != request.actor_id:
        raise V1AuditEvidenceError("decision actor_id must match request")
    if decision.shell_id != request.shell_id:
        raise V1AuditEvidenceError("decision shell_id must match request")
    if decision.action_type is not request.action_type:
        raise V1AuditEvidenceError("decision action_type must match request")

    if request.metadata.get("v1_runtime_slice") != "typed_request_guardian_decision_preflight":
        raise V1AuditEvidenceError("request must come from the V1-G11 runtime slice")
    if decision.metadata.get("v1_runtime_slice") != "typed_request_guardian_decision_preflight":
        raise V1AuditEvidenceError("decision must come from the V1-G11 runtime slice")
    if decision.constraints.get("v1_preflight_only") is not True:
        raise V1AuditEvidenceError("decision must be a V1 preflight decision")
    if decision.constraints.get("non_executing") is not True:
        raise V1AuditEvidenceError("decision must be non-executing")
    if decision.constraints.get("execution_allowed") is not False:
        raise V1AuditEvidenceError("decision cannot allow execution")
    if decision.constraints.get("side_effects_allowed") is not False:
        raise V1AuditEvidenceError("decision cannot allow side effects")
    if decision.constraints.get("approval_token_issued") is not False:
        raise V1AuditEvidenceError("approval tokens cannot enter audit persistence")
    if decision.allowed_tool_packs:
        raise V1AuditEvidenceError("tool packs cannot enter V1-G12 persistence")


def _decision_linkage(decision: GuardianDecision) -> Mapping[str, Any]:
    linkage = decision.metadata.get("audit_evidence_linkage")
    if not isinstance(linkage, Mapping):
        raise V1AuditEvidenceError("decision audit linkage is required")
    return linkage


def _approval_evidence_if_required(
    request: ConsequentialActionRequest,
    metadata: Mapping[str, Any],
    evidence_refs: tuple[str, ...],
) -> tuple[str | None, str | None]:
    destructive = bool(request.typed_args.get("destructive"))
    if request.action_type is ConsequentialActionType.FILE_OPERATION and destructive:
        approval_id = _required_text(metadata.get("approval_id"), "approval_id")
        approval_evidence_ref = _required_text(
            metadata.get("approval_evidence_ref"),
            "approval_evidence_ref",
        )
        if approval_evidence_ref not in evidence_refs:
            raise V1AuditEvidenceError("approval_evidence_ref must be in evidence_refs")
        return approval_id, approval_evidence_ref

    return _optional_text(metadata.get("approval_id")), _optional_text(
        metadata.get("approval_evidence_ref")
    )


def _evidence_refs(
    request: ConsequentialActionRequest,
    decision: GuardianDecision,
    metadata: Mapping[str, Any],
) -> tuple[str, ...]:
    refs: list[str] = []
    for source in (
        metadata.get("evidence_refs", ()),
        request.evidence_refs,
        decision.evidence_refs,
    ):
        refs.extend(_string_sequence(source, "evidence_refs"))

    normalized = tuple(dict.fromkeys(refs))
    if not normalized:
        raise V1AuditEvidenceError("evidence_refs are required")
    return normalized


def _audit_status(status: GuardianDecisionStatus) -> str:
    if status is GuardianDecisionStatus.APPROVED:
        return "approved"
    if status in {
        GuardianDecisionStatus.NEEDS_OPERATOR_PIN,
        GuardianDecisionStatus.NEEDS_HUMAN_CONFIRMATION,
        GuardianDecisionStatus.NEEDS_BREAKGLASS,
    }:
        return "needs_approval"
    if status is GuardianDecisionStatus.DENIED:
        return "denied"
    return "blocked"


def _reject_raw_sensitive_content(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            if isinstance(key, str) and key.strip().lower() in RAW_SENSITIVE_KEYS:
                raise V1AuditEvidenceError("raw sensitive content is not accepted")
            _reject_raw_sensitive_content(nested)
    elif isinstance(value, (list, tuple, set, frozenset)):
        for nested in value:
            _reject_raw_sensitive_content(nested)
    elif isinstance(value, str):
        folded = value.strip().lower()
        if any(marker in folded for marker in RAW_SENSITIVE_VALUE_MARKERS):
            raise V1AuditEvidenceError("raw sensitive content is not accepted")


def _reject_external_or_authority_claims(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            if (
                isinstance(key, str)
                and key.strip().lower() in FORBIDDEN_TRUE_CLAIM_KEYS
                and nested is not False
            ):
                raise V1AuditEvidenceError("audit metadata cannot grant authority or execute")
            _reject_external_or_authority_claims(nested)
    elif isinstance(value, (list, tuple, set, frozenset)):
        for nested in value:
            _reject_external_or_authority_claims(nested)


def _record_hash(record: Mapping[str, Any]) -> str:
    sanitized = _json_ready({key: value for key, value in record.items() if key != "record_hash"})
    encoded = json.dumps(sanitized, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _json_ready(nested) for key, nested in value.items()}
    if isinstance(value, (list, tuple, set, frozenset)):
        return [_json_ready(nested) for nested in value]
    return value


def _required_enum(value: Any, allowed: frozenset[str], field_name: str) -> str:
    normalized = _required_text(value, field_name).lower()
    if normalized not in allowed:
        raise V1AuditEvidenceError(f"{field_name} is not allowed")
    return normalized


def _required_text_or_sequence(value: Any, field_name: str) -> None:
    if isinstance(value, str):
        _required_text(value, field_name)
        return
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray, str)):
        if not _string_sequence(value, field_name):
            raise V1AuditEvidenceError(f"{field_name} is required")
        return
    raise V1AuditEvidenceError(f"{field_name} is required")


def _required_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise V1AuditEvidenceError(f"{field_name} is required")
    return value.strip()


def _optional_text(value: Any) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        return None
    return value.strip()


def _string_sequence(value: Any, field_name: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        value = (value,)
    if not isinstance(value, Sequence) or isinstance(value, (bytes, bytearray)):
        raise V1AuditEvidenceError(f"{field_name} must be a string sequence")

    normalized = tuple(str(item).strip() for item in value if str(item).strip())
    return normalized
