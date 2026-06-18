"""V1 live provider/model call authority metadata validator.

This module is the approved V1-G44 candidate runtime slice. It validates
sanitized authority/preflight metadata for a future Guardian-gated provider
call. It never calls providers/models, dispatches requests, performs network
I/O, reads secrets, accesses credential values, executes fallback, or invokes
external systems.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import hashlib
import json
from typing import Any, Final


SCHEMA_VERSION: Final[str] = "v1-g44-candidate"
ALLOWED_MODEL_ROLES: Final[frozenset[str]] = frozenset(
    {
        "primary",
        "backup",
        "heavy_hitter",
        "agent_override",
        "workstation",
        "local",
        "codex_subscription",
        "provider_readiness",
        "fallback",
    }
)
ALLOWED_DATA_SENSITIVITY: Final[frozenset[str]] = frozenset(
    {"public", "internal", "confidential", "restricted", "regulated"}
)
ALLOWED_BUDGET_CLASSES: Final[frozenset[str]] = frozenset(
    {"free", "low", "medium", "high", "critical"}
)
ALLOWED_COST_CLASSES: Final[frozenset[str]] = frozenset(
    {"free", "low", "medium", "high", "critical"}
)
ALLOWED_LATENCY_TIERS: Final[frozenset[str]] = frozenset(
    {"interactive", "standard", "batch", "background"}
)
REQUIRED_TOP_LEVEL_FIELDS: Final[tuple[str, ...]] = (
    "authority_id",
    "request_or_guardian_decision_linkage",
    "tenant_scope",
    "shell_scope",
    "actor_scope",
    "session_scope",
    "source_provider_model_route_authority_ref",
    "source_provider_model_dispatch_evidence_ref",
    "provider_id",
    "model_id",
    "model_role",
    "provider_boundary_metadata",
    "credential_reference_metadata",
    "network_policy_reference_metadata",
    "prompt_reference_metadata",
    "output_handling_policy",
    "data_sensitivity",
    "budget_class",
    "estimated_cost_class",
    "latency_tier",
    "approval_evidence_linkage",
    "audit_evidence_linkage",
    "proof_not_execution_confirmation",
    "no_raw_prompt_model_response_customer_data_confirmation",
    "no_secret_lookup_confirmation",
    "no_credential_value_access_confirmation",
    "no_network_call_confirmation",
    "no_live_provider_call_execution_confirmation",
    "no_fallback_execution_confirmation",
)
RAW_SENSITIVE_KEYS: Final[frozenset[str]] = frozenset(
    {
        "api_key",
        "bearer_token",
        "content",
        "credential",
        "credentials",
        "customer_data",
        "message_text",
        "model_response",
        "oauth_token",
        "output_text",
        "password",
        "prompt",
        "prompt_text",
        "provider_api_key",
        "provider_credentials",
        "provider_token",
        "raw_customer_context",
        "raw_customer_data",
        "raw_model_response",
        "raw_output",
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
    "api key",
    "bearer token",
    "model response text",
    "provider credential",
    "provider token",
    "raw customer context",
    "raw customer data",
    "raw model response",
    "raw prompt",
    "raw secret",
    "raw-secret-",
    "secret value",
)
FORBIDDEN_TRUE_CLAIM_KEYS: Final[frozenset[str]] = frozenset(
    {
        "action_executed",
        "actual_model_request_dispatch_execution_added",
        "browser_action_executed",
        "connector_invoked",
        "consumer_code_imported",
        "consumer_integration_added",
        "consumer_repo_mutation_added",
        "consumer_runtime_called",
        "consumer_runtime_calls_added",
        "credential_access_added",
        "credential_accessed",
        "credential_value_access_added",
        "credential_value_accessed",
        "device_command_invoked",
        "drone_control_invoked",
        "execution_allowed",
        "execution_authority_added",
        "external_send_added",
        "fallback_executed",
        "fallback_execution_added",
        "fallback_execution_allowed",
        "file_mutation_executed",
        "humaninput_bridge_activated",
        "iot_control_invoked",
        "live_provider_call_executed",
        "live_provider_call_execution_added",
        "live_provider_call_performed",
        "live_provider_model_call_execution_added",
        "model_request_dispatched",
        "network_action_executed",
        "network_call_added",
        "network_call_performed",
        "physical_world_invoked",
        "product_ready",
        "provider_called",
        "provider_model_call_allowed",
        "provider_model_calls_added",
        "provider_readiness_check_performed",
        "provider_readiness_network_check_added",
        "provider_readiness_network_check_allowed",
        "robot_control_invoked",
        "robotics_invoked",
        "scheduled_task_executed",
        "secret_lookup_added",
        "secret_lookup_performed",
        "shell_runtime_wired",
        "side_effects_allowed",
        "token_guardian_live_routing_added",
        "tool_executed",
    }
)


class V1LiveProviderModelCallAuthorityError(ValueError):
    """Raised when live provider/model call authority metadata fails V1-G44."""


def validate_v1_live_provider_model_call_authority(
    authority_metadata: Mapping[str, Any],
) -> dict[str, Any]:
    """Return a deterministic non-executing live provider call authority record."""

    if not isinstance(authority_metadata, Mapping):
        raise V1LiveProviderModelCallAuthorityError(
            "authority_metadata must be a mapping"
        )

    _reject_raw_sensitive_content(authority_metadata)

    for field_name in REQUIRED_TOP_LEVEL_FIELDS:
        if field_name not in authority_metadata:
            raise V1LiveProviderModelCallAuthorityError(f"{field_name} is required")

    authority_id = _required_text(authority_metadata.get("authority_id"), "authority_id")
    linkage = _validate_request_or_decision_linkage(
        authority_metadata.get("request_or_guardian_decision_linkage")
    )
    tenant_scope = _required_text(authority_metadata.get("tenant_scope"), "tenant_scope")
    shell_scope = _required_text(authority_metadata.get("shell_scope"), "shell_scope")
    actor_scope = _required_text(authority_metadata.get("actor_scope"), "actor_scope")
    session_scope = _required_text(authority_metadata.get("session_scope"), "session_scope")
    route_ref = _required_text(
        authority_metadata.get("source_provider_model_route_authority_ref"),
        "source_provider_model_route_authority_ref",
    )
    dispatch_ref = _required_text(
        authority_metadata.get("source_provider_model_dispatch_evidence_ref"),
        "source_provider_model_dispatch_evidence_ref",
    )
    provider_id = _required_text(authority_metadata.get("provider_id"), "provider_id")
    model_id = _required_text(authority_metadata.get("model_id"), "model_id")
    model_role = _model_role(authority_metadata.get("model_role"))
    provider_boundary = _validate_provider_boundary(
        authority_metadata.get("provider_boundary_metadata")
    )
    credential_reference = _validate_credential_reference(
        authority_metadata.get("credential_reference_metadata")
    )
    network_policy = _validate_network_policy_reference(
        authority_metadata.get("network_policy_reference_metadata")
    )
    prompt_reference = _validate_prompt_reference(
        authority_metadata.get("prompt_reference_metadata")
    )
    output_policy = _validate_output_policy(
        authority_metadata.get("output_handling_policy")
    )
    data_sensitivity = _data_sensitivity(authority_metadata.get("data_sensitivity"))
    budget_class = _budget_class(authority_metadata.get("budget_class"))
    estimated_cost_class = _cost_class(authority_metadata.get("estimated_cost_class"))
    latency_tier = _latency_tier(authority_metadata.get("latency_tier"))
    approval_linkage = _validate_approval_evidence_linkage(
        authority_metadata.get("approval_evidence_linkage")
    )
    audit_linkage = _validate_audit_linkage(
        authority_metadata.get("audit_evidence_linkage")
    )
    _require_true_confirmation(
        authority_metadata.get("proof_not_execution_confirmation"),
        "proof_not_execution_confirmation",
    )
    _require_true_confirmation(
        authority_metadata.get("no_raw_prompt_model_response_customer_data_confirmation"),
        "no_raw_prompt_model_response_customer_data_confirmation",
    )
    _require_true_confirmation(
        authority_metadata.get("no_secret_lookup_confirmation"),
        "no_secret_lookup_confirmation",
    )
    _require_true_confirmation(
        authority_metadata.get("no_credential_value_access_confirmation"),
        "no_credential_value_access_confirmation",
    )
    _require_true_confirmation(
        authority_metadata.get("no_network_call_confirmation"),
        "no_network_call_confirmation",
    )
    _require_true_confirmation(
        authority_metadata.get("no_live_provider_call_execution_confirmation"),
        "no_live_provider_call_execution_confirmation",
    )
    _require_true_confirmation(
        authority_metadata.get("no_fallback_execution_confirmation"),
        "no_fallback_execution_confirmation",
    )
    _reject_runtime_authority_claims(authority_metadata)

    record = {
        "record_type": "v1_live_provider_model_call_authority",
        "schema_version": SCHEMA_VERSION,
        "authority_id": authority_id,
        "request_or_guardian_decision_linkage": linkage,
        "tenant_scope": tenant_scope,
        "shell_scope": shell_scope,
        "actor_scope": actor_scope,
        "session_scope": session_scope,
        "source_provider_model_route_authority_ref": route_ref,
        "source_provider_model_dispatch_evidence_ref": dispatch_ref,
        "provider_id": provider_id,
        "model_id": model_id,
        "model_role": model_role,
        "provider_boundary_metadata": provider_boundary,
        "credential_reference_metadata": credential_reference,
        "network_policy_reference_metadata": network_policy,
        "prompt_reference_metadata": prompt_reference,
        "output_handling_policy": output_policy,
        "data_sensitivity": data_sensitivity,
        "budget_class": budget_class,
        "estimated_cost_class": estimated_cost_class,
        "latency_tier": latency_tier,
        "approval_evidence_linkage": approval_linkage,
        "audit_evidence_linkage": audit_linkage,
        "capability_open": True,
        "authority_gated": True,
        "live_provider_model_call_authority_runtime_behavior": True,
        "proof_not_execution": True,
        "non_executing": True,
        "authority_preflight_metadata_only": True,
        "redacted_metadata_only": True,
        "live_provider_model_call_execution_added": False,
        "actual_model_request_dispatch_execution_added": False,
        "model_request_dispatched": False,
        "network_call_added": False,
        "network_call_performed": False,
        "provider_readiness_network_check_added": False,
        "token_guardian_live_routing_added": False,
        "secret_lookup_added": False,
        "credential_value_access_added": False,
        "credential_access_added": False,
        "fallback_execution_added": False,
        "fallback_executed": False,
        "tool_executed": False,
        "execution_allowed": False,
        "side_effects_allowed": False,
        "action_executed": False,
        "file_mutation_executed": False,
        "consumer_repo_mutation_added": False,
        "consumer_code_imported": False,
        "consumer_runtime_calls_added": False,
        "consumer_integration_added": False,
        "shell_runtime_wired": False,
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
        "product_ready": False,
        "metadata": {
            "v1_runtime_slice": "live_provider_model_call_authority",
            "candidate_only": True,
            "non_executing": True,
            "proof_not_execution": True,
        },
    }
    record["record_hash"] = _record_hash(record)
    return record


def _validate_request_or_decision_linkage(value: Any) -> dict[str, Any]:
    linkage = _mapping(value, "request_or_guardian_decision_linkage")
    request_id = _optional_text(linkage.get("request_id"))
    guardian_decision_id = _optional_text(linkage.get("guardian_decision_id"))
    if not request_id and not guardian_decision_id:
        raise V1LiveProviderModelCallAuthorityError(
            "request_id or guardian_decision_id linkage is required"
        )
    if linkage.get("linkage_required") is not True:
        raise V1LiveProviderModelCallAuthorityError(
            "request/decision linkage is required"
        )
    if linkage.get("proof_not_execution") is not True:
        raise V1LiveProviderModelCallAuthorityError(
            "linkage metadata cannot be execution authority"
        )
    if linkage.get("grants_execution_authority") is not False:
        raise V1LiveProviderModelCallAuthorityError(
            "linkage metadata cannot grant execution"
        )
    return {
        "request_id": request_id,
        "guardian_decision_id": guardian_decision_id,
        "linkage_required": True,
        "proof_not_execution": True,
        "grants_execution_authority": False,
    }


def _validate_provider_boundary(value: Any) -> dict[str, Any]:
    boundary = _mapping(value, "provider_boundary_metadata")
    provider_boundary_ref = _required_text(
        boundary.get("provider_boundary_ref"),
        "provider_boundary_metadata.provider_boundary_ref",
    )
    provider_class = _required_text(
        boundary.get("provider_class"),
        "provider_boundary_metadata.provider_class",
    )
    if boundary.get("provider_configured_for_scope") is not True:
        raise V1LiveProviderModelCallAuthorityError(
            "provider boundary configuration is required"
        )
    if boundary.get("live_provider_call_authority_policy_bound") is not True:
        raise V1LiveProviderModelCallAuthorityError(
            "live provider call authority policy binding is required"
        )
    if boundary.get("live_provider_call_execution_allowed") is not False:
        raise V1LiveProviderModelCallAuthorityError(
            "live provider call execution is not allowed"
        )
    if boundary.get("provider_readiness_network_check_allowed") is not False:
        raise V1LiveProviderModelCallAuthorityError(
            "provider readiness network checks are not allowed"
        )
    if boundary.get("token_guardian_live_routing_allowed") is not False:
        raise V1LiveProviderModelCallAuthorityError(
            "Token Guardian live routing is not allowed"
        )
    if boundary.get("proof_not_execution") is not True:
        raise V1LiveProviderModelCallAuthorityError(
            "provider boundary metadata cannot be execution authority"
        )
    return {
        "provider_boundary_ref": provider_boundary_ref,
        "provider_class": provider_class,
        "provider_configured_for_scope": True,
        "live_provider_call_authority_policy_bound": True,
        "live_provider_call_execution_allowed": False,
        "provider_readiness_network_check_allowed": False,
        "token_guardian_live_routing_allowed": False,
        "proof_not_execution": True,
    }


def _validate_credential_reference(value: Any) -> dict[str, Any]:
    credential = _mapping(value, "credential_reference_metadata")
    credential_ref = _optional_text(credential.get("credential_ref"))
    provider_is_no_key_local = credential.get("provider_is_no_key_local") is True
    if not credential_ref and not provider_is_no_key_local:
        raise V1LiveProviderModelCallAuthorityError("credential reference is required")
    if credential.get("reference_only") is not True:
        raise V1LiveProviderModelCallAuthorityError(
            "credential metadata must be reference only"
        )
    if credential.get("secret_lookup_performed") is not False:
        raise V1LiveProviderModelCallAuthorityError("secret lookup is not allowed")
    if credential.get("credential_value_accessed") is not False:
        raise V1LiveProviderModelCallAuthorityError(
            "credential value access is not allowed"
        )
    if credential.get("raw_secret_present") is not False:
        raise V1LiveProviderModelCallAuthorityError(
            "raw credential values are not accepted"
        )
    if credential.get("credential_value_present") is not False:
        raise V1LiveProviderModelCallAuthorityError(
            "raw credential values are not accepted"
        )
    if credential.get("provider_token_present") is not False:
        raise V1LiveProviderModelCallAuthorityError(
            "provider tokens are not accepted"
        )
    return {
        "credential_ref": credential_ref,
        "provider_is_no_key_local": provider_is_no_key_local,
        "reference_only": True,
        "secret_lookup_performed": False,
        "credential_value_accessed": False,
        "raw_secret_present": False,
        "credential_value_present": False,
        "provider_token_present": False,
    }


def _validate_network_policy_reference(value: Any) -> dict[str, Any]:
    network = _mapping(value, "network_policy_reference_metadata")
    network_policy_ref = _required_text(
        network.get("network_policy_ref"),
        "network_policy_reference_metadata.network_policy_ref",
    )
    if network.get("reference_only") is not True:
        raise V1LiveProviderModelCallAuthorityError(
            "network policy metadata must be reference only"
        )
    if network.get("network_scope_bound") is not True:
        raise V1LiveProviderModelCallAuthorityError("network policy scope is required")
    if network.get("network_call_performed") is not False:
        raise V1LiveProviderModelCallAuthorityError("network calls are not allowed")
    if network.get("provider_endpoint_resolution_performed") is not False:
        raise V1LiveProviderModelCallAuthorityError(
            "provider endpoint resolution is not allowed"
        )
    if network.get("proof_not_execution") is not True:
        raise V1LiveProviderModelCallAuthorityError(
            "network policy metadata cannot be execution authority"
        )
    return {
        "network_policy_ref": network_policy_ref,
        "reference_only": True,
        "network_scope_bound": True,
        "network_call_performed": False,
        "provider_endpoint_resolution_performed": False,
        "proof_not_execution": True,
    }


def _validate_prompt_reference(value: Any) -> dict[str, Any]:
    prompt = _mapping(value, "prompt_reference_metadata")
    prompt_ref = _required_text(
        prompt.get("prompt_ref"),
        "prompt_reference_metadata.prompt_ref",
    )
    prompt_context_class = _required_text(
        prompt.get("prompt_context_class"),
        "prompt_reference_metadata.prompt_context_class",
    )
    if prompt.get("reference_only") is not True:
        raise V1LiveProviderModelCallAuthorityError(
            "prompt metadata must be reference only"
        )
    if prompt.get("redacted") is not True:
        raise V1LiveProviderModelCallAuthorityError("prompt reference must be redacted")
    if prompt.get("raw_prompt_present") is not False:
        raise V1LiveProviderModelCallAuthorityError("raw prompts are not accepted")
    if prompt.get("raw_customer_data_present") is not False:
        raise V1LiveProviderModelCallAuthorityError(
            "raw customer data is not accepted"
        )
    return {
        "prompt_ref": prompt_ref,
        "prompt_context_class": prompt_context_class,
        "reference_only": True,
        "redacted": True,
        "raw_prompt_present": False,
        "raw_customer_data_present": False,
    }


def _validate_output_policy(value: Any) -> dict[str, Any]:
    output = _mapping(value, "output_handling_policy")
    output_policy_ref = _required_text(
        output.get("output_policy_ref"),
        "output_handling_policy.output_policy_ref",
    )
    audit_output_ref = _required_text(
        output.get("audit_output_ref"),
        "output_handling_policy.audit_output_ref",
    )
    if output.get("redacted_output_required") is not True:
        raise V1LiveProviderModelCallAuthorityError(
            "redacted output handling is required"
        )
    if output.get("raw_model_response_present") is not False:
        raise V1LiveProviderModelCallAuthorityError(
            "raw model responses are not accepted"
        )
    if output.get("persist_raw_model_response") is not False:
        raise V1LiveProviderModelCallAuthorityError(
            "raw model responses must not be persisted"
        )
    if output.get("proof_not_execution") is not True:
        raise V1LiveProviderModelCallAuthorityError(
            "output policy metadata cannot be execution authority"
        )
    return {
        "output_policy_ref": output_policy_ref,
        "audit_output_ref": audit_output_ref,
        "redacted_output_required": True,
        "raw_model_response_present": False,
        "persist_raw_model_response": False,
        "proof_not_execution": True,
    }


def _validate_approval_evidence_linkage(value: Any) -> dict[str, Any]:
    approval = _mapping(value, "approval_evidence_linkage")
    approval_evidence_ref = _required_text(
        approval.get("approval_evidence_ref"),
        "approval_evidence_linkage.approval_evidence_ref",
    )
    if approval.get("approval_required_by_policy") is not True:
        raise V1LiveProviderModelCallAuthorityError(
            "approval evidence is required by policy"
        )
    if approval.get("approval_evidence_current") is not True:
        raise V1LiveProviderModelCallAuthorityError("approval evidence must be current")
    if approval.get("proof_not_execution") is not True:
        raise V1LiveProviderModelCallAuthorityError(
            "approval evidence metadata cannot be execution authority"
        )
    if approval.get("grants_execution_authority") is not False:
        raise V1LiveProviderModelCallAuthorityError(
            "approval evidence cannot grant execution"
        )
    return {
        "approval_required_by_policy": True,
        "approval_evidence_ref": approval_evidence_ref,
        "approval_evidence_current": True,
        "proof_not_execution": True,
        "grants_execution_authority": False,
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
        allow_empty=False,
    )
    if audit.get("required") is not True:
        raise V1LiveProviderModelCallAuthorityError("audit/evidence linkage is required")
    if audit.get("proof_not_execution") is not True:
        raise V1LiveProviderModelCallAuthorityError(
            "audit/evidence metadata cannot be execution authority"
        )
    return {
        "audit_record_ref": audit_record_ref,
        "evidence_refs": list(evidence_refs),
        "required": True,
        "proof_not_execution": True,
    }


def _reject_raw_sensitive_content(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            if isinstance(key, str) and key.strip().lower() in RAW_SENSITIVE_KEYS:
                raise V1LiveProviderModelCallAuthorityError(
                    "raw sensitive content is not accepted"
                )
            _reject_raw_sensitive_content(nested)
    elif isinstance(value, (list, tuple, set, frozenset)):
        for nested in value:
            _reject_raw_sensitive_content(nested)
    elif isinstance(value, str):
        folded = value.strip().lower()
        if any(marker in folded for marker in RAW_SENSITIVE_VALUE_MARKERS):
            raise V1LiveProviderModelCallAuthorityError(
                "raw sensitive content is not accepted"
            )


def _reject_runtime_authority_claims(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            if (
                isinstance(key, str)
                and key.strip().lower() in FORBIDDEN_TRUE_CLAIM_KEYS
                and nested is not False
            ):
                raise V1LiveProviderModelCallAuthorityError(
                    "authority metadata cannot grant runtime execution"
                )
            _reject_runtime_authority_claims(nested)
    elif isinstance(value, (list, tuple, set, frozenset)):
        for nested in value:
            _reject_runtime_authority_claims(nested)


def _model_role(value: Any) -> str:
    model_role = _normalize_token(_required_text(value, "model_role"))
    if model_role not in ALLOWED_MODEL_ROLES:
        raise V1LiveProviderModelCallAuthorityError("model role is not allowed")
    return model_role


def _data_sensitivity(value: Any) -> str:
    sensitivity = _normalize_token(_required_text(value, "data_sensitivity"))
    if sensitivity not in ALLOWED_DATA_SENSITIVITY:
        raise V1LiveProviderModelCallAuthorityError("data sensitivity is not allowed")
    return sensitivity


def _budget_class(value: Any) -> str:
    budget_class = _normalize_token(_required_text(value, "budget_class"))
    if budget_class not in ALLOWED_BUDGET_CLASSES:
        raise V1LiveProviderModelCallAuthorityError("budget class is not allowed")
    return budget_class


def _cost_class(value: Any) -> str:
    cost_class = _normalize_token(_required_text(value, "estimated_cost_class"))
    if cost_class not in ALLOWED_COST_CLASSES:
        raise V1LiveProviderModelCallAuthorityError(
            "estimated cost class is not allowed"
        )
    return cost_class


def _latency_tier(value: Any) -> str:
    latency_tier = _normalize_token(_required_text(value, "latency_tier"))
    if latency_tier not in ALLOWED_LATENCY_TIERS:
        raise V1LiveProviderModelCallAuthorityError("latency tier is not allowed")
    return latency_tier


def _mapping(value: Any, field_name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping) or not value:
        raise V1LiveProviderModelCallAuthorityError(f"{field_name} is required")
    return value


def _required_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise V1LiveProviderModelCallAuthorityError(f"{field_name} is required")
    return value.strip()


def _optional_text(value: Any) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        return None
    return value.strip()


def _string_sequence(
    value: Any,
    field_name: str,
    *,
    allow_empty: bool,
) -> tuple[str, ...]:
    if isinstance(value, str):
        value = (value,)
    if not isinstance(value, Sequence) or isinstance(value, (bytes, bytearray)):
        raise V1LiveProviderModelCallAuthorityError(
            f"{field_name} must be a string sequence"
        )
    normalized = tuple(str(item).strip() for item in value if str(item).strip())
    if not normalized and not allow_empty:
        raise V1LiveProviderModelCallAuthorityError(f"{field_name} is required")
    return normalized


def _require_true_confirmation(value: Any, field_name: str) -> None:
    if value is True:
        return
    if isinstance(value, Mapping) and value.get("confirmed") is True:
        return
    raise V1LiveProviderModelCallAuthorityError(
        f"{field_name} confirmation is required"
    )


def _normalize_token(value: str) -> str:
    return value.strip().lower().replace("-", "_").replace(" ", "_")


def _record_hash(record: Mapping[str, Any]) -> str:
    sanitized = _json_ready(
        {key: value for key, value in record.items() if key != "record_hash"}
    )
    encoded = json.dumps(sanitized, sort_keys=True, separators=(",", ":")).encode(
        "utf-8"
    )
    return hashlib.sha256(encoded).hexdigest()


def _json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _json_ready(nested) for key, nested in value.items()}
    if isinstance(value, (list, tuple, set, frozenset)):
        return [_json_ready(nested) for nested in value]
    return value
