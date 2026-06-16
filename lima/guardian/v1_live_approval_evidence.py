"""V1 live approval evidence/capture metadata validator.

This module is the approved V1-G19 candidate runtime slice. It validates
sanitized approval evidence metadata that may be captured by a shell, harness,
or future approval provider. It never verifies raw PINs, persists raw factors,
issues approval tokens, executes actions, routes providers, wires consumers, or
invokes external systems.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import hashlib
import json
from typing import Any, Final


SCHEMA_VERSION: Final[str] = "v1-g19-candidate"
NORMALIZED_APPROVAL_OUTCOMES: Final[dict[str, str]] = {
    "approved": "approved",
    "denied": "denied",
    "revoked": "revoked",
    "stale": "stale",
    "expired": "expired",
    "superseded": "superseded",
    "blocked": "blocked",
}
ALLOWED_RISK_CLASSES: Final[frozenset[str]] = frozenset(
    {"low", "medium", "high", "critical"}
)
ALLOWED_ACTION_FAMILIES: Final[frozenset[str]] = frozenset(
    {
        "destructive_edit",
        "destructive_delete",
        "destructive_file_mutation",
        "provider_model_route",
        "connector_action",
        "browser_network_action",
        "consumer_integration",
        "scheduled_task_action",
        "physical_world_action",
    }
)
REQUIRED_TOP_LEVEL_FIELDS: Final[tuple[str, ...]] = (
    "approval_evidence_id",
    "approval_challenge_id",
    "request_or_guardian_decision_linkage",
    "tenant_scope",
    "shell_scope",
    "actor_scope",
    "session_scope",
    "approver_actor_ref",
    "approval_intent_scope",
    "action_risk_class",
    "action_family",
    "approval_outcome",
    "approval_freshness_status",
    "approval_expiration_metadata",
    "replay_prevention_metadata",
    "factor_evidence_summary",
    "capture_source_metadata",
    "audit_evidence_linkage",
    "proof_not_authority_confirmation",
    "no_raw_pin_token_secret_customer_data_confirmation",
    "no_approval_token_issuance_confirmation",
    "no_execution_authority_confirmation",
)
RAW_SENSITIVE_KEYS: Final[frozenset[str]] = frozenset(
    {
        "api_key",
        "approval_pin",
        "approval_token",
        "content",
        "credential",
        "credentials",
        "customer_data",
        "factor_value",
        "file_content",
        "file_contents",
        "message_text",
        "operator_pin",
        "password",
        "pin",
        "prompt",
        "provider_credentials",
        "raw_approval_factor",
        "raw_approval_pin",
        "raw_approval_token",
        "raw_customer_data",
        "raw_factor",
        "raw_factor_value",
        "raw_file_content",
        "raw_file_contents",
        "raw_human_input",
        "raw_pin",
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
    "raw approval",
    "raw factor",
    "raw pin",
    "raw prompt",
    "raw file contents",
    "raw file content",
    "raw customer data",
    "provider credential",
    "api key",
)
FORBIDDEN_TRUE_CLAIM_KEYS: Final[frozenset[str]] = frozenset(
    {
        "action_executed",
        "approval_token_issued",
        "browser_action_executed",
        "connector_invoked",
        "consumer_code_imported",
        "consumer_integration_added",
        "consumer_repo_mutation_added",
        "consumer_runtime_called",
        "consumer_runtime_calls_added",
        "device_command_invoked",
        "drone_control_invoked",
        "execution_allowed",
        "execution_authority_added",
        "external_send_added",
        "file_mutation_executed",
        "final_api_freeze_approved",
        "humaninput_bridge_activated",
        "iot_control_invoked",
        "model_routed",
        "network_action_executed",
        "physical_world_invoked",
        "product_ready",
        "provider_model_routed",
        "raw_pin_persisted",
        "raw_pin_verified",
        "robot_control_invoked",
        "robotics_invoked",
        "scheduled_task_executed",
        "shell_runtime_wired",
        "shell_wired",
        "side_effects_allowed",
        "tool_executed",
    }
)


class V1LiveApprovalEvidenceError(ValueError):
    """Raised when approval evidence metadata fails the V1-G19 boundary."""


def validate_v1_live_approval_evidence_capture(
    approval_metadata: Mapping[str, Any],
) -> dict[str, Any]:
    """Return a deterministic non-executing live approval evidence record."""

    if not isinstance(approval_metadata, Mapping):
        raise V1LiveApprovalEvidenceError("approval_metadata must be a mapping")

    _reject_raw_sensitive_content(approval_metadata)
    _reject_runtime_authority_claims(approval_metadata)

    for field_name in REQUIRED_TOP_LEVEL_FIELDS:
        if field_name not in approval_metadata:
            raise V1LiveApprovalEvidenceError(f"{field_name} is required")

    approval_evidence_id = _required_text(
        approval_metadata.get("approval_evidence_id"),
        "approval_evidence_id",
    )
    approval_challenge_id = _required_text(
        approval_metadata.get("approval_challenge_id"),
        "approval_challenge_id",
    )
    linkage = _validate_request_or_decision_linkage(
        approval_metadata.get("request_or_guardian_decision_linkage")
    )
    tenant_scope = _required_text(approval_metadata.get("tenant_scope"), "tenant_scope")
    shell_scope = _required_text(approval_metadata.get("shell_scope"), "shell_scope")
    actor_scope = _required_text(approval_metadata.get("actor_scope"), "actor_scope")
    session_scope = _required_text(approval_metadata.get("session_scope"), "session_scope")
    approver_actor_ref = _required_text(
        approval_metadata.get("approver_actor_ref"),
        "approver_actor_ref",
    )
    approval_intent_scope = _validate_approval_intent_scope(
        approval_metadata.get("approval_intent_scope")
    )
    action_risk_class = _risk_class(approval_metadata.get("action_risk_class"))
    action_family = _action_family(approval_metadata.get("action_family"))
    approval_outcome = _approval_outcome(approval_metadata.get("approval_outcome"))
    approval_freshness_status = _freshness_status(
        approval_metadata.get("approval_freshness_status")
    )
    expiration = _validate_expiration_metadata(
        approval_metadata.get("approval_expiration_metadata")
    )
    replay = _validate_replay_prevention(
        approval_metadata.get("replay_prevention_metadata")
    )
    factor_summary = _validate_factor_evidence_summary(
        approval_metadata.get("factor_evidence_summary")
    )
    capture_source = _validate_capture_source(
        approval_metadata.get("capture_source_metadata")
    )
    audit_linkage = _validate_audit_linkage(
        approval_metadata.get("audit_evidence_linkage")
    )
    _require_true_confirmation(
        approval_metadata.get("proof_not_authority_confirmation"),
        "proof_not_authority_confirmation",
    )
    _require_true_confirmation(
        approval_metadata.get("no_raw_pin_token_secret_customer_data_confirmation"),
        "no_raw_pin_token_secret_customer_data_confirmation",
    )
    _require_true_confirmation(
        approval_metadata.get("no_approval_token_issuance_confirmation"),
        "no_approval_token_issuance_confirmation",
    )
    _require_true_confirmation(
        approval_metadata.get("no_execution_authority_confirmation"),
        "no_execution_authority_confirmation",
    )

    evidence_is_current = (
        approval_outcome == "approved"
        and approval_freshness_status == "fresh"
        and expiration["expiration_status"] == "not_expired"
        and replay["replay_status"] == "not_replayed"
    )

    record = {
        "record_type": "v1_live_approval_evidence_capture",
        "schema_version": SCHEMA_VERSION,
        "approval_evidence_id": approval_evidence_id,
        "approval_challenge_id": approval_challenge_id,
        "request_or_guardian_decision_linkage": linkage,
        "tenant_scope": tenant_scope,
        "shell_scope": shell_scope,
        "actor_scope": actor_scope,
        "session_scope": session_scope,
        "approver_actor_ref": approver_actor_ref,
        "approval_intent_scope": approval_intent_scope,
        "action_risk_class": action_risk_class,
        "action_family": action_family,
        "approval_outcome": approval_outcome,
        "approval_freshness_status": approval_freshness_status,
        "approval_expiration_metadata": expiration,
        "replay_prevention_metadata": replay,
        "factor_evidence_summary": factor_summary,
        "capture_source_metadata": capture_source,
        "audit_evidence_linkage": audit_linkage,
        "evidence_is_current": evidence_is_current,
        "capability_open": True,
        "authority_gated": True,
        "live_approval_evidence_capture_runtime_behavior": True,
        "proof_not_authority": True,
        "non_executing": True,
        "redacted_metadata_only": True,
        "execution_allowed": False,
        "side_effects_allowed": False,
        "approval_token_issued": False,
        "raw_pin_verified": False,
        "raw_pin_persisted": False,
        "approval_token_persisted": False,
        "action_executed": False,
        "file_mutation_executed": False,
        "consumer_repo_mutation_added": False,
        "consumer_code_imported": False,
        "consumer_runtime_calls_added": False,
        "consumer_integration_added": False,
        "provider_model_routed": False,
        "tool_executed": False,
        "connector_invoked": False,
        "browser_action_executed": False,
        "network_action_executed": False,
        "scheduled_task_executed": False,
        "external_send_added": False,
        "device_command_invoked": False,
        "robot_control_invoked": False,
        "drone_control_invoked": False,
        "iot_control_invoked": False,
        "physical_world_invoked": False,
        "raw_sensitive_content_persisted": False,
        "final_api_freeze_approved": False,
        "product_ready": False,
        "metadata": {
            "v1_runtime_slice": "live_approval_evidence_capture",
            "candidate_only": True,
            "non_executing": True,
            "proof_not_authority": True,
        },
    }
    record["record_hash"] = _record_hash(record)
    return record


def _validate_request_or_decision_linkage(value: Any) -> dict[str, Any]:
    linkage = _mapping(value, "request_or_guardian_decision_linkage")
    request_id = _optional_text(linkage.get("request_id"))
    guardian_decision_id = _optional_text(linkage.get("guardian_decision_id"))
    if not request_id and not guardian_decision_id:
        raise V1LiveApprovalEvidenceError(
            "request_id or guardian_decision_id linkage is required"
        )
    if linkage.get("linkage_required") is not True:
        raise V1LiveApprovalEvidenceError("request/decision linkage is required")
    if linkage.get("proof_not_authority") is not True:
        raise V1LiveApprovalEvidenceError("linkage metadata cannot be authority")
    return {
        "request_id": request_id,
        "guardian_decision_id": guardian_decision_id,
        "linkage_required": True,
        "proof_not_authority": True,
    }


def _validate_approval_intent_scope(value: Any) -> dict[str, Any]:
    intent = _mapping(value, "approval_intent_scope")
    intent_ref = _required_text(
        intent.get("intent_ref"),
        "approval_intent_scope.intent_ref",
    )
    requested_action_ref = _required_text(
        intent.get("requested_action_ref"),
        "approval_intent_scope.requested_action_ref",
    )
    action_scope_ref = _required_text(
        intent.get("action_scope_ref"),
        "approval_intent_scope.action_scope_ref",
    )
    if intent.get("scope_bound") is not True:
        raise V1LiveApprovalEvidenceError("approval intent scope must be bound")
    if intent.get("grants_execution_authority") is not False:
        raise V1LiveApprovalEvidenceError("approval intent cannot grant execution")
    return {
        "intent_ref": intent_ref,
        "requested_action_ref": requested_action_ref,
        "action_scope_ref": action_scope_ref,
        "scope_bound": True,
        "grants_execution_authority": False,
    }


def _validate_expiration_metadata(value: Any) -> dict[str, Any]:
    expiration = _mapping(value, "approval_expiration_metadata")
    expires_at_ref = _required_text(
        expiration.get("expires_at_ref"),
        "approval_expiration_metadata.expires_at_ref",
    )
    expiration_status = _required_text(
        expiration.get("expiration_status"),
        "approval_expiration_metadata.expiration_status",
    ).lower()
    if expiration_status not in {"not_expired", "expired"}:
        raise V1LiveApprovalEvidenceError("expiration status is not allowed")
    if expiration.get("expiration_checked") is not True:
        raise V1LiveApprovalEvidenceError("expiration metadata must be checked")
    return {
        "expires_at_ref": expires_at_ref,
        "expiration_status": expiration_status,
        "expiration_checked": True,
    }


def _validate_replay_prevention(value: Any) -> dict[str, Any]:
    replay = _mapping(value, "replay_prevention_metadata")
    replay_nonce_ref = _required_text(
        replay.get("replay_nonce_ref"),
        "replay_prevention_metadata.replay_nonce_ref",
    )
    replay_status = _required_text(
        replay.get("replay_status"),
        "replay_prevention_metadata.replay_status",
    ).lower()
    if replay_status not in {"not_replayed", "replayed"}:
        raise V1LiveApprovalEvidenceError("replay status is not allowed")
    if replay.get("replay_checked") is not True:
        raise V1LiveApprovalEvidenceError("replay prevention metadata must be checked")
    return {
        "replay_nonce_ref": replay_nonce_ref,
        "replay_status": replay_status,
        "replay_checked": True,
    }


def _validate_factor_evidence_summary(value: Any) -> dict[str, Any]:
    factor = _mapping(value, "factor_evidence_summary")
    factor_family = _required_text(
        factor.get("factor_family"),
        "factor_evidence_summary.factor_family",
    )
    factor_result = _required_text(
        factor.get("factor_result"),
        "factor_evidence_summary.factor_result",
    ).lower()
    if factor_result not in {"passed", "failed", "not_required", "blocked"}:
        raise V1LiveApprovalEvidenceError("factor result is not allowed")
    if factor.get("raw_factor_value_present") is not False:
        raise V1LiveApprovalEvidenceError("raw factor values are not accepted")
    if factor.get("redacted_summary_only") is not True:
        raise V1LiveApprovalEvidenceError("factor evidence must be redacted summary only")
    return {
        "factor_family": factor_family,
        "factor_result": factor_result,
        "raw_factor_value_present": False,
        "redacted_summary_only": True,
    }


def _validate_capture_source(value: Any) -> dict[str, Any]:
    source = _mapping(value, "capture_source_metadata")
    capture_source_ref = _required_text(
        source.get("capture_source_ref"),
        "capture_source_metadata.capture_source_ref",
    )
    capture_channel = _required_text(
        source.get("capture_channel"),
        "capture_source_metadata.capture_channel",
    )
    if source.get("source_trusted_by_policy") is not True:
        raise V1LiveApprovalEvidenceError("capture source policy trust is required")
    if source.get("consumer_runtime_invoked") is not False:
        raise V1LiveApprovalEvidenceError(
            "consumer runtime calls cannot grant runtime authority"
        )
    return {
        "capture_source_ref": capture_source_ref,
        "capture_channel": capture_channel,
        "source_trusted_by_policy": True,
        "consumer_runtime_invoked": False,
    }


def _validate_audit_linkage(value: Any) -> dict[str, Any]:
    audit = _mapping(value, "audit_evidence_linkage")
    audit_record_ref = _required_text(
        audit.get("audit_record_ref"),
        "audit_evidence_linkage.audit_record_ref",
    )
    evidence_refs = _string_sequence(
        audit.get("evidence_refs"),
        "audit_evidence_linkage.evidence_refs",
    )
    if not evidence_refs:
        raise V1LiveApprovalEvidenceError("audit/evidence refs are required")
    if audit.get("required") is not True:
        raise V1LiveApprovalEvidenceError("audit/evidence linkage is required")
    if audit.get("proof_not_authority") is not True:
        raise V1LiveApprovalEvidenceError("audit/evidence metadata cannot be authority")
    return {
        "audit_record_ref": audit_record_ref,
        "evidence_refs": list(evidence_refs),
        "required": True,
        "proof_not_authority": True,
    }


def _reject_raw_sensitive_content(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            if isinstance(key, str) and key.strip().lower() in RAW_SENSITIVE_KEYS:
                raise V1LiveApprovalEvidenceError("raw sensitive content is not accepted")
            _reject_raw_sensitive_content(nested)
    elif isinstance(value, (list, tuple, set, frozenset)):
        for nested in value:
            _reject_raw_sensitive_content(nested)
    elif isinstance(value, str):
        folded = value.strip().lower()
        if any(marker in folded for marker in RAW_SENSITIVE_VALUE_MARKERS):
            raise V1LiveApprovalEvidenceError("raw sensitive content is not accepted")


def _reject_runtime_authority_claims(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            if (
                isinstance(key, str)
                and key.strip().lower() in FORBIDDEN_TRUE_CLAIM_KEYS
                and nested is not False
            ):
                raise V1LiveApprovalEvidenceError(
                    "approval evidence metadata cannot grant runtime authority"
                )
            _reject_runtime_authority_claims(nested)
    elif isinstance(value, (list, tuple, set, frozenset)):
        for nested in value:
            _reject_runtime_authority_claims(nested)


def _approval_outcome(value: Any) -> str:
    outcome = _required_text(value, "approval_outcome").lower().replace("-", "_")
    if outcome not in NORMALIZED_APPROVAL_OUTCOMES:
        raise V1LiveApprovalEvidenceError("approval outcome is not allowed")
    return NORMALIZED_APPROVAL_OUTCOMES[outcome]


def _freshness_status(value: Any) -> str:
    freshness = _required_text(value, "approval_freshness_status").lower()
    if freshness not in {"fresh", "stale"}:
        raise V1LiveApprovalEvidenceError("approval freshness status is not allowed")
    return freshness


def _risk_class(value: Any) -> str:
    risk_class = _required_text(value, "action_risk_class").lower()
    if risk_class not in ALLOWED_RISK_CLASSES:
        raise V1LiveApprovalEvidenceError("action risk class is not allowed")
    return risk_class


def _action_family(value: Any) -> str:
    action_family = _required_text(value, "action_family").lower().replace("-", "_")
    if action_family not in ALLOWED_ACTION_FAMILIES:
        raise V1LiveApprovalEvidenceError("action family is not allowed")
    return action_family


def _mapping(value: Any, field_name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping) or not value:
        raise V1LiveApprovalEvidenceError(f"{field_name} is required")
    return value


def _required_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise V1LiveApprovalEvidenceError(f"{field_name} is required")
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
        raise V1LiveApprovalEvidenceError(f"{field_name} must be a string sequence")
    return tuple(str(item).strip() for item in value if str(item).strip())


def _require_true_confirmation(value: Any, field_name: str) -> None:
    if value is True:
        return
    if isinstance(value, Mapping) and value.get("confirmed") is True:
        return
    raise V1LiveApprovalEvidenceError(f"{field_name} confirmation is required")


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
