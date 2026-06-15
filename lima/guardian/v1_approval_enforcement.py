"""V1 destructive approval-enforcement gate.

This module is the approved V1-G14 runtime slice boundary. It validates
sanitized approval evidence for destructive edit/delete file-mutation
requests that have already passed the V1-G11 GuardianDecision preflight.
It does not execute, mutate files, issue approval tokens, persist records,
route providers, wire shells, or invoke any external system.
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


SCHEMA_VERSION: Final[str] = "v1-g14-candidate"
REQUIRED_APPROVAL_SCOPE: Final[str] = "destructive_edit_delete_file_mutation"
ALLOWED_APPROVAL_STATES: Final[frozenset[str]] = frozenset({"granted"})
BLOCKED_APPROVAL_STATES: Final[frozenset[str]] = frozenset(
    {"denied", "expired", "revoked", "stale", "superseded"}
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
    "provider credential",
)
FORBIDDEN_AUTHORITY_KEYS: Final[frozenset[str]] = frozenset(
    {
        "approval_granted",
        "approved",
        "approved_for_execution",
        "authorized",
        "decision",
        "guardian_decision",
        "guardian_decision_ref",
        "operator_pin_verified",
    }
)
FORBIDDEN_TRUE_CLAIM_KEYS: Final[frozenset[str]] = frozenset(
    {
        "approval_enforcement_record_is_authority",
        "approval_token_issued",
        "audit_record_is_authority",
        "browser_action_executed",
        "connector_invoked",
        "device_command_invoked",
        "execution_allowed",
        "file_deleted",
        "file_mutated",
        "file_mutation_executed",
        "file_overwritten",
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


class V1ApprovalEnforcementError(ValueError):
    """Raised when approval evidence cannot satisfy the V1-G14 gate."""


def enforce_v1_destructive_approval(
    request: ConsequentialActionRequest,
    decision: GuardianDecision,
    approval_metadata: Mapping[str, Any],
) -> dict[str, Any]:
    """Return a redacted non-executing approval-enforcement record."""

    if not isinstance(approval_metadata, Mapping):
        raise V1ApprovalEnforcementError("approval_metadata must be a mapping")

    _validate_reviewed_destructive_request_decision(request, decision)
    _reject_raw_sensitive_content(approval_metadata)
    _reject_authority_claims(approval_metadata)

    approval_id = _required_text(approval_metadata.get("approval_id"), "approval_id")
    approval_evidence_ref = _required_text(
        approval_metadata.get("approval_evidence_ref"),
        "approval_evidence_ref",
    )
    approving_actor_ref = _required_text(
        approval_metadata.get("approving_actor_ref"),
        "approving_actor_ref",
    )
    approval_recorded_at = _required_text(
        approval_metadata.get("approval_recorded_at"),
        "approval_recorded_at",
    )
    approval_scope = _required_text(
        approval_metadata.get("approval_scope"),
        "approval_scope",
    )
    if approval_scope != REQUIRED_APPROVAL_SCOPE:
        raise V1ApprovalEnforcementError("approval_scope does not match request scope")

    _validate_approval_state(approval_metadata)
    _validate_approval_linkage(
        request,
        decision,
        approval_metadata,
        approval_evidence_ref,
    )
    evidence_refs = _evidence_refs(request, decision, approval_metadata, approval_evidence_ref)
    linkage = _decision_linkage(decision)
    tenant_ref = _required_text(approval_metadata.get("tenant_ref"), "tenant_ref")

    record = {
        "record_type": "v1_approval_enforcement",
        "schema_version": SCHEMA_VERSION,
        "approval_enforcement_status": "satisfied",
        "request_id": _required_text(request.request_id, "request_id"),
        "decision_id": _required_text(decision.decision_id, "decision_id"),
        "input_id": _optional_text(request.input_id),
        "intent_id": _optional_text(request.intent_id),
        "actor_id": _required_text(request.actor_id, "actor_id"),
        "shell_id": _required_text(request.shell_id, "shell_id"),
        "tenant_ref": tenant_ref,
        "target_ref": _optional_text(request.target_ref),
        "action_type": request.action_type.value,
        "risk_class": _required_text(decision.risk_class, "risk_class"),
        "decision_status": decision.status.value,
        "approval_id": approval_id,
        "approval_evidence_ref": approval_evidence_ref,
        "approving_actor_ref": approving_actor_ref,
        "approval_recorded_at": approval_recorded_at,
        "approval_scope": approval_scope,
        "approval_state": "granted",
        "lineage_id": _required_text(linkage.get("lineage_id"), "lineage_id"),
        "evidence_refs": list(evidence_refs),
        "approval_enforcement_record_is_authority": False,
        "execution_allowed": False,
        "side_effects_allowed": False,
        "approval_token_issued": False,
        "provider_model_routed": False,
        "shell_wired": False,
        "file_mutation_executed": False,
        "metadata": {
            "v1_runtime_slice": "destructive_approval_enforcement",
            "source_runtime_slice": request.metadata.get("v1_runtime_slice"),
            "redacted": True,
            "proof_not_authority": True,
            "non_executing": True,
        },
    }
    record["record_hash"] = _record_hash(record)
    return record


def _validate_reviewed_destructive_request_decision(
    request: ConsequentialActionRequest,
    decision: GuardianDecision,
) -> None:
    if not isinstance(request, ConsequentialActionRequest):
        raise V1ApprovalEnforcementError("request must be a ConsequentialActionRequest")
    if not isinstance(decision, GuardianDecision):
        raise V1ApprovalEnforcementError("decision must be a GuardianDecision")

    if decision.request_id != request.request_id:
        raise V1ApprovalEnforcementError("decision request_id must match request")
    if decision.input_id != request.input_id:
        raise V1ApprovalEnforcementError("decision input_id must match request")
    if decision.intent_id != request.intent_id:
        raise V1ApprovalEnforcementError("decision intent_id must match request")
    if decision.actor_id != request.actor_id:
        raise V1ApprovalEnforcementError("decision actor_id must match request")
    if decision.shell_id != request.shell_id:
        raise V1ApprovalEnforcementError("decision shell_id must match request")
    if decision.action_type is not request.action_type:
        raise V1ApprovalEnforcementError("decision action_type must match request")
    if decision.target_ref != request.target_ref:
        raise V1ApprovalEnforcementError("decision target_ref must match request")
    if decision.risk_class != request.risk_class:
        raise V1ApprovalEnforcementError("decision risk_class must match request")

    if request.metadata.get("v1_runtime_slice") != "typed_request_guardian_decision_preflight":
        raise V1ApprovalEnforcementError("request must come from the V1-G11 runtime slice")
    if decision.metadata.get("v1_runtime_slice") != "typed_request_guardian_decision_preflight":
        raise V1ApprovalEnforcementError("decision must come from the V1-G11 runtime slice")
    if decision.constraints.get("v1_preflight_only") is not True:
        raise V1ApprovalEnforcementError("decision must be a V1 preflight decision")
    if decision.constraints.get("non_executing") is not True:
        raise V1ApprovalEnforcementError("decision must be non-executing")
    if decision.constraints.get("execution_allowed") is not False:
        raise V1ApprovalEnforcementError("decision cannot allow execution")
    if decision.constraints.get("side_effects_allowed") is not False:
        raise V1ApprovalEnforcementError("decision cannot allow side effects")
    if decision.constraints.get("approval_token_issued") is not False:
        raise V1ApprovalEnforcementError("approval tokens cannot enter V1-G14")
    if decision.constraints.get("provider_model_routed") is not False:
        raise V1ApprovalEnforcementError("provider/model routing is not allowed")
    if decision.constraints.get("shell_wired") is not False:
        raise V1ApprovalEnforcementError("shell wiring is not allowed")
    if decision.allowed_tool_packs:
        raise V1ApprovalEnforcementError("tool packs cannot enter V1-G14")

    if decision.status is not GuardianDecisionStatus.NEEDS_OPERATOR_PIN:
        raise V1ApprovalEnforcementError("decision must require operator approval")
    if request.action_type is not ConsequentialActionType.FILE_OPERATION:
        raise V1ApprovalEnforcementError("request must be a file operation")
    if request.metadata.get("v1_action_category") != "file_mutation":
        raise V1ApprovalEnforcementError("request must be file_mutation shaped")
    if request.typed_args.get("destructive") is not True:
        raise V1ApprovalEnforcementError("request must be destructive")


def _validate_approval_state(approval_metadata: Mapping[str, Any]) -> None:
    state = _required_text(approval_metadata.get("approval_state"), "approval_state").lower()
    if state in BLOCKED_APPROVAL_STATES:
        raise V1ApprovalEnforcementError("approval_state is not grantable")
    if state not in ALLOWED_APPROVAL_STATES:
        raise V1ApprovalEnforcementError("approval_state must be granted")

    freshness = _required_text(
        approval_metadata.get("approval_freshness"),
        "approval_freshness",
    ).lower()
    if freshness != "fresh":
        raise V1ApprovalEnforcementError("approval evidence is stale")

    replay_status = _required_text(
        approval_metadata.get("approval_replay_status"),
        "approval_replay_status",
    ).lower()
    if replay_status != "not_replayed":
        raise V1ApprovalEnforcementError("approval evidence is replayed")


def _validate_approval_linkage(
    request: ConsequentialActionRequest,
    decision: GuardianDecision,
    approval_metadata: Mapping[str, Any],
    approval_evidence_ref: str,
) -> None:
    linkage = _decision_linkage(decision)
    expected = {
        "request_id": request.request_id,
        "decision_id": decision.decision_id,
        "actor_id": request.actor_id,
        "shell_id": request.shell_id,
        "target_ref": request.target_ref,
    }
    for field_name, expected_value in expected.items():
        actual = _required_text(approval_metadata.get(field_name), field_name)
        if actual != expected_value:
            raise V1ApprovalEnforcementError(f"{field_name} does not match approval scope")

    tenant_ref = _required_text(approval_metadata.get("tenant_ref"), "tenant_ref")
    expected_tenant_ref = linkage.get("tenant_ref")
    if expected_tenant_ref is not None and tenant_ref != expected_tenant_ref:
        raise V1ApprovalEnforcementError("tenant_ref does not match approval scope")
    evidence_refs = _string_sequence(approval_metadata.get("evidence_refs", ()), "evidence_refs")
    if approval_evidence_ref not in evidence_refs:
        raise V1ApprovalEnforcementError("approval_evidence_ref must be in evidence_refs")


def _decision_linkage(decision: GuardianDecision) -> Mapping[str, Any]:
    linkage = decision.metadata.get("audit_evidence_linkage")
    if not isinstance(linkage, Mapping):
        raise V1ApprovalEnforcementError("decision audit linkage is required")
    return linkage


def _evidence_refs(
    request: ConsequentialActionRequest,
    decision: GuardianDecision,
    approval_metadata: Mapping[str, Any],
    approval_evidence_ref: str,
) -> tuple[str, ...]:
    refs: list[str] = []
    for source in (
        approval_metadata.get("evidence_refs", ()),
        request.evidence_refs,
        decision.evidence_refs,
    ):
        refs.extend(_string_sequence(source, "evidence_refs"))

    normalized = tuple(dict.fromkeys(refs))
    if approval_evidence_ref not in normalized:
        raise V1ApprovalEnforcementError("approval_evidence_ref must be in evidence_refs")
    return normalized


def _reject_raw_sensitive_content(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            if isinstance(key, str) and key.strip().lower() in RAW_SENSITIVE_KEYS:
                raise V1ApprovalEnforcementError("raw sensitive content is not accepted")
            _reject_raw_sensitive_content(nested)
    elif isinstance(value, (list, tuple, set, frozenset)):
        for nested in value:
            _reject_raw_sensitive_content(nested)
    elif isinstance(value, str):
        folded = value.strip().lower()
        if any(marker in folded for marker in RAW_SENSITIVE_VALUE_MARKERS):
            raise V1ApprovalEnforcementError("raw sensitive content is not accepted")


def _reject_authority_claims(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            folded_key = key.strip().lower() if isinstance(key, str) else ""
            if folded_key in FORBIDDEN_AUTHORITY_KEYS:
                raise V1ApprovalEnforcementError("forged authority metadata is not accepted")
            if folded_key in FORBIDDEN_TRUE_CLAIM_KEYS and nested is not False:
                raise V1ApprovalEnforcementError("approval metadata cannot grant authority or execute")
            _reject_authority_claims(nested)
    elif isinstance(value, (list, tuple, set, frozenset)):
        for nested in value:
            _reject_authority_claims(nested)


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


def _required_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise V1ApprovalEnforcementError(f"{field_name} is required")
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
        raise V1ApprovalEnforcementError(f"{field_name} must be a string sequence")

    return tuple(str(item).strip() for item in value if str(item).strip())
