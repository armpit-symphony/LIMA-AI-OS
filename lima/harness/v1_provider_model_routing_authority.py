"""V1 provider/model routing authority metadata validator.

This module is the approved V1-G20 candidate runtime slice. It validates
sanitized provider/model routing authority metadata for a future Guardian-gated
Harness decision. It never calls providers/models, dispatches model requests,
executes fallback, reads secrets, executes tools, wires consumers, or invokes
external systems.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import hashlib
import json
from typing import Any, Final


SCHEMA_VERSION: Final[str] = "v1-g20-candidate"
ALLOWED_ROUTE_FAMILIES: Final[frozenset[str]] = frozenset(
    {
        "primary_model_route",
        "backup_fallback_route",
        "heavy_hitter_route",
        "agent_override_route",
        "workstation_model_seat_route",
        "local_endpoint_route",
        "codex_subscription_route",
        "provider_readiness_self_inspection_route",
    }
)
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
ALLOWED_PROMPT_CONTEXT_CLASSES: Final[frozenset[str]] = frozenset(
    {
        "none",
        "planning_metadata",
        "redacted_summary",
        "synthetic_fixture",
        "user_prompt_redacted",
        "code_context_redacted",
        "customer_context_redacted",
        "private_data_redacted",
    }
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
    "route_id",
    "route_family",
    "route_intent_scope",
    "request_or_guardian_decision_linkage",
    "tenant_scope",
    "shell_scope",
    "actor_scope",
    "session_scope",
    "provider_id",
    "model_id",
    "model_role",
    "provider_boundary_metadata",
    "data_sensitivity",
    "prompt_context_class",
    "requested_tool_packs",
    "allowed_tool_packs",
    "credential_reference_metadata",
    "budget_class",
    "estimated_cost_class",
    "latency_tier",
    "fallback_chain_metadata",
    "approval_evidence_linkage_when_required",
    "provider_configuration_ref",
    "audit_evidence_linkage",
    "proof_not_authority_confirmation",
    "no_raw_prompt_secret_credential_customer_data_confirmation",
    "no_secret_lookup_confirmation",
    "no_live_provider_call_confirmation",
    "no_execution_authority_confirmation",
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
        "password",
        "prompt",
        "provider_api_key",
        "provider_credentials",
        "provider_token",
        "raw_customer_context",
        "raw_customer_data",
        "raw_model_response",
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
    "raw prompt",
    "raw customer data",
    "raw customer context",
    "provider credential",
    "provider token",
    "api key",
    "bearer token",
    "secret value",
)
FORBIDDEN_TRUE_CLAIM_KEYS: Final[frozenset[str]] = frozenset(
    {
        "action_executed",
        "browser_action_executed",
        "connector_invoked",
        "consumer_code_imported",
        "consumer_integration_added",
        "consumer_repo_mutation_added",
        "consumer_runtime_called",
        "consumer_runtime_calls_added",
        "credential_access_added",
        "credential_accessed",
        "device_command_invoked",
        "drone_control_invoked",
        "execution_allowed",
        "execution_authority_added",
        "external_send_added",
        "fallback_executed",
        "fallback_execution_allowed",
        "file_mutation_executed",
        "final_api_freeze_approved",
        "humaninput_bridge_activated",
        "iot_control_invoked",
        "live_provider_call_allowed",
        "live_provider_call_performed",
        "model_request_dispatched",
        "model_routed",
        "network_action_executed",
        "physical_world_invoked",
        "product_ready",
        "provider_called",
        "provider_model_call_allowed",
        "provider_model_calls_added",
        "provider_model_routed",
        "provider_model_routing_added",
        "provider_readiness_check_performed",
        "provider_readiness_checks_added",
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


class V1ProviderModelRoutingAuthorityError(ValueError):
    """Raised when provider/model route metadata fails the V1-G20 boundary."""


def validate_v1_provider_model_routing_authority(
    route_metadata: Mapping[str, Any],
) -> dict[str, Any]:
    """Return a deterministic non-executing provider/model route authority record."""

    if not isinstance(route_metadata, Mapping):
        raise V1ProviderModelRoutingAuthorityError("route_metadata must be a mapping")

    _reject_raw_sensitive_content(route_metadata)
    _reject_runtime_authority_claims(route_metadata)

    for field_name in REQUIRED_TOP_LEVEL_FIELDS:
        if field_name not in route_metadata:
            raise V1ProviderModelRoutingAuthorityError(f"{field_name} is required")

    route_id = _required_text(route_metadata.get("route_id"), "route_id")
    route_family = _route_family(route_metadata.get("route_family"))
    route_intent_scope = _validate_route_intent_scope(
        route_metadata.get("route_intent_scope")
    )
    linkage = _validate_request_or_decision_linkage(
        route_metadata.get("request_or_guardian_decision_linkage")
    )
    tenant_scope = _required_text(route_metadata.get("tenant_scope"), "tenant_scope")
    shell_scope = _required_text(route_metadata.get("shell_scope"), "shell_scope")
    actor_scope = _required_text(route_metadata.get("actor_scope"), "actor_scope")
    session_scope = _required_text(route_metadata.get("session_scope"), "session_scope")
    provider_id = _required_text(route_metadata.get("provider_id"), "provider_id")
    model_id = _required_text(route_metadata.get("model_id"), "model_id")
    model_role = _model_role(route_metadata.get("model_role"))
    provider_boundary = _validate_provider_boundary(
        route_metadata.get("provider_boundary_metadata")
    )
    data_sensitivity = _data_sensitivity(route_metadata.get("data_sensitivity"))
    prompt_context_class = _prompt_context_class(
        route_metadata.get("prompt_context_class")
    )
    requested_tool_packs = _string_sequence(
        route_metadata.get("requested_tool_packs"),
        "requested_tool_packs",
        allow_empty=True,
    )
    allowed_tool_packs = _string_sequence(
        route_metadata.get("allowed_tool_packs"),
        "allowed_tool_packs",
        allow_empty=False,
    )
    _validate_tool_pack_scope(requested_tool_packs, allowed_tool_packs)
    credential_reference = _validate_credential_reference(
        route_metadata.get("credential_reference_metadata")
    )
    budget_class = _budget_class(route_metadata.get("budget_class"))
    estimated_cost_class = _cost_class(route_metadata.get("estimated_cost_class"))
    latency_tier = _latency_tier(route_metadata.get("latency_tier"))
    fallback_chain = _validate_fallback_chain(
        route_metadata.get("fallback_chain_metadata")
    )
    approval_linkage = _validate_approval_evidence_linkage(
        route_metadata.get("approval_evidence_linkage_when_required")
    )
    provider_configuration_ref = _required_text(
        route_metadata.get("provider_configuration_ref"),
        "provider_configuration_ref",
    )
    audit_linkage = _validate_audit_linkage(route_metadata.get("audit_evidence_linkage"))
    _require_true_confirmation(
        route_metadata.get("proof_not_authority_confirmation"),
        "proof_not_authority_confirmation",
    )
    _require_true_confirmation(
        route_metadata.get("no_raw_prompt_secret_credential_customer_data_confirmation"),
        "no_raw_prompt_secret_credential_customer_data_confirmation",
    )
    _require_true_confirmation(
        route_metadata.get("no_secret_lookup_confirmation"),
        "no_secret_lookup_confirmation",
    )
    _require_true_confirmation(
        route_metadata.get("no_live_provider_call_confirmation"),
        "no_live_provider_call_confirmation",
    )
    _require_true_confirmation(
        route_metadata.get("no_execution_authority_confirmation"),
        "no_execution_authority_confirmation",
    )

    record = {
        "record_type": "v1_provider_model_routing_authority",
        "schema_version": SCHEMA_VERSION,
        "route_id": route_id,
        "route_family": route_family,
        "route_intent_scope": route_intent_scope,
        "request_or_guardian_decision_linkage": linkage,
        "tenant_scope": tenant_scope,
        "shell_scope": shell_scope,
        "actor_scope": actor_scope,
        "session_scope": session_scope,
        "provider_id": provider_id,
        "model_id": model_id,
        "model_role": model_role,
        "provider_boundary_metadata": provider_boundary,
        "data_sensitivity": data_sensitivity,
        "prompt_context_class": prompt_context_class,
        "requested_tool_packs": list(requested_tool_packs),
        "allowed_tool_packs": list(allowed_tool_packs),
        "credential_reference_metadata": credential_reference,
        "budget_class": budget_class,
        "estimated_cost_class": estimated_cost_class,
        "latency_tier": latency_tier,
        "fallback_chain_metadata": fallback_chain,
        "approval_evidence_linkage_when_required": approval_linkage,
        "provider_configuration_ref": provider_configuration_ref,
        "audit_evidence_linkage": audit_linkage,
        "capability_open": True,
        "authority_gated": True,
        "provider_model_routing_authority_runtime_behavior": True,
        "proof_not_authority": True,
        "non_executing": True,
        "redacted_metadata_only": True,
        "route_metadata_only": True,
        "provider_model_routing_added": False,
        "provider_model_calls_added": False,
        "live_provider_call_performed": False,
        "model_request_dispatched": False,
        "fallback_executed": False,
        "provider_readiness_checks_added": False,
        "token_guardian_live_routing_added": False,
        "secret_lookup_added": False,
        "credential_access_added": False,
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
        "final_api_freeze_approved": False,
        "product_ready": False,
        "metadata": {
            "v1_runtime_slice": "provider_model_routing_authority",
            "candidate_only": True,
            "non_executing": True,
            "proof_not_authority": True,
        },
    }
    record["record_hash"] = _record_hash(record)
    return record


def _validate_route_intent_scope(value: Any) -> dict[str, Any]:
    intent = _mapping(value, "route_intent_scope")
    route_intent_ref = _required_text(
        intent.get("route_intent_ref"),
        "route_intent_scope.route_intent_ref",
    )
    requested_model_route_ref = _required_text(
        intent.get("requested_model_route_ref"),
        "route_intent_scope.requested_model_route_ref",
    )
    capability_scope_ref = _required_text(
        intent.get("capability_scope_ref"),
        "route_intent_scope.capability_scope_ref",
    )
    if intent.get("scope_bound") is not True:
        raise V1ProviderModelRoutingAuthorityError("route intent scope must be bound")
    if intent.get("grants_execution_authority") is not False:
        raise V1ProviderModelRoutingAuthorityError("route intent cannot grant execution")
    return {
        "route_intent_ref": route_intent_ref,
        "requested_model_route_ref": requested_model_route_ref,
        "capability_scope_ref": capability_scope_ref,
        "scope_bound": True,
        "grants_execution_authority": False,
    }


def _validate_request_or_decision_linkage(value: Any) -> dict[str, Any]:
    linkage = _mapping(value, "request_or_guardian_decision_linkage")
    request_id = _optional_text(linkage.get("request_id"))
    guardian_decision_id = _optional_text(linkage.get("guardian_decision_id"))
    if not request_id and not guardian_decision_id:
        raise V1ProviderModelRoutingAuthorityError(
            "request_id or guardian_decision_id linkage is required"
        )
    if linkage.get("linkage_required") is not True:
        raise V1ProviderModelRoutingAuthorityError("request/decision linkage is required")
    if linkage.get("proof_not_authority") is not True:
        raise V1ProviderModelRoutingAuthorityError("linkage metadata cannot be authority")
    return {
        "request_id": request_id,
        "guardian_decision_id": guardian_decision_id,
        "linkage_required": True,
        "proof_not_authority": True,
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
        raise V1ProviderModelRoutingAuthorityError(
            "provider boundary configuration is required"
        )
    if boundary.get("live_provider_call_allowed") is not False:
        raise V1ProviderModelRoutingAuthorityError("live provider calls are not allowed")
    if boundary.get("provider_readiness_network_check_allowed") is not False:
        raise V1ProviderModelRoutingAuthorityError(
            "provider readiness checks are not allowed"
        )
    if boundary.get("credential_lookup_allowed") is not False:
        raise V1ProviderModelRoutingAuthorityError("secret lookup is not allowed")
    if boundary.get("proof_not_authority") is not True:
        raise V1ProviderModelRoutingAuthorityError(
            "provider boundary metadata cannot be authority"
        )
    return {
        "provider_boundary_ref": provider_boundary_ref,
        "provider_class": provider_class,
        "provider_configured_for_scope": True,
        "live_provider_call_allowed": False,
        "provider_readiness_network_check_allowed": False,
        "credential_lookup_allowed": False,
        "proof_not_authority": True,
    }


def _validate_credential_reference(value: Any) -> dict[str, Any]:
    credential = _mapping(value, "credential_reference_metadata")
    credential_ref = _optional_text(credential.get("credential_ref"))
    provider_is_no_key_local = credential.get("provider_is_no_key_local") is True
    if not credential_ref and not provider_is_no_key_local:
        raise V1ProviderModelRoutingAuthorityError("credential reference is required")
    if credential.get("reference_only") is not True:
        raise V1ProviderModelRoutingAuthorityError(
            "credential metadata must be reference only"
        )
    if credential.get("secret_lookup_performed") is not False:
        raise V1ProviderModelRoutingAuthorityError("secret lookup is not allowed")
    if credential.get("raw_secret_present") is not False:
        raise V1ProviderModelRoutingAuthorityError(
            "raw credential values are not accepted"
        )
    if credential.get("credential_value_present") is not False:
        raise V1ProviderModelRoutingAuthorityError(
            "raw credential values are not accepted"
        )
    return {
        "credential_ref": credential_ref,
        "provider_is_no_key_local": provider_is_no_key_local,
        "reference_only": True,
        "secret_lookup_performed": False,
        "raw_secret_present": False,
        "credential_value_present": False,
    }


def _validate_fallback_chain(value: Any) -> dict[str, Any]:
    fallback = _mapping(value, "fallback_chain_metadata")
    fallback_chain_ref = _required_text(
        fallback.get("fallback_chain_ref"),
        "fallback_chain_metadata.fallback_chain_ref",
    )
    if fallback.get("fallback_inherits_same_gates") is not True:
        raise V1ProviderModelRoutingAuthorityError(
            "fallback candidates must inherit the same gates"
        )
    candidates = _mapping_sequence(
        fallback.get("fallback_candidates"),
        "fallback_chain_metadata.fallback_candidates",
    )
    normalized_candidates: list[dict[str, Any]] = []
    for index, candidate in enumerate(candidates):
        prefix = f"fallback_chain_metadata.fallback_candidates[{index}]"
        candidate_ref = _required_text(candidate.get("candidate_ref"), f"{prefix}.candidate_ref")
        candidate_provider_id = _required_text(
            candidate.get("provider_id"),
            f"{prefix}.provider_id",
        )
        candidate_model_id = _required_text(candidate.get("model_id"), f"{prefix}.model_id")
        candidate_route_family = _route_family(candidate.get("route_family"))
        if candidate.get("inherits_same_gates") is not True:
            raise V1ProviderModelRoutingAuthorityError(
                "fallback candidates must inherit the same gates"
            )
        if candidate.get("secret_lookup_performed") is not False:
            raise V1ProviderModelRoutingAuthorityError("secret lookup is not allowed")
        if candidate.get("live_provider_call_allowed") is not False:
            raise V1ProviderModelRoutingAuthorityError(
                "live provider calls are not allowed"
            )
        if candidate.get("fallback_execution_allowed") is not False:
            raise V1ProviderModelRoutingAuthorityError(
                "fallback execution is not allowed"
            )
        normalized_candidates.append(
            {
                "candidate_ref": candidate_ref,
                "provider_id": candidate_provider_id,
                "model_id": candidate_model_id,
                "route_family": candidate_route_family,
                "inherits_same_gates": True,
                "secret_lookup_performed": False,
                "live_provider_call_allowed": False,
                "fallback_execution_allowed": False,
            }
        )
    return {
        "fallback_chain_ref": fallback_chain_ref,
        "fallback_inherits_same_gates": True,
        "fallback_candidates": normalized_candidates,
    }


def _validate_approval_evidence_linkage(value: Any) -> dict[str, Any]:
    approval = _mapping(value, "approval_evidence_linkage_when_required")
    approval_required = approval.get("approval_required_by_policy") is True
    approval_evidence_ref = _optional_text(approval.get("approval_evidence_ref"))
    if approval_required and not approval_evidence_ref:
        raise V1ProviderModelRoutingAuthorityError("approval evidence is required")
    if approval_required and approval.get("approval_evidence_current") is not True:
        raise V1ProviderModelRoutingAuthorityError("approval evidence must be current")
    if approval.get("proof_not_authority") is not True:
        raise V1ProviderModelRoutingAuthorityError(
            "approval evidence metadata cannot be authority"
        )
    if approval.get("grants_execution_authority") is not False:
        raise V1ProviderModelRoutingAuthorityError(
            "approval evidence cannot grant execution"
        )
    return {
        "approval_required_by_policy": approval_required,
        "approval_evidence_ref": approval_evidence_ref,
        "approval_evidence_current": (
            True if approval_required else approval.get("approval_evidence_current") is True
        ),
        "proof_not_authority": True,
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
        raise V1ProviderModelRoutingAuthorityError("audit/evidence linkage is required")
    if audit.get("proof_not_authority") is not True:
        raise V1ProviderModelRoutingAuthorityError(
            "audit/evidence metadata cannot be authority"
        )
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
                raise V1ProviderModelRoutingAuthorityError(
                    "raw sensitive content is not accepted"
                )
            _reject_raw_sensitive_content(nested)
    elif isinstance(value, (list, tuple, set, frozenset)):
        for nested in value:
            _reject_raw_sensitive_content(nested)
    elif isinstance(value, str):
        folded = value.strip().lower()
        if any(marker in folded for marker in RAW_SENSITIVE_VALUE_MARKERS):
            raise V1ProviderModelRoutingAuthorityError(
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
                raise V1ProviderModelRoutingAuthorityError(
                    "route metadata cannot grant runtime authority"
                )
            _reject_runtime_authority_claims(nested)
    elif isinstance(value, (list, tuple, set, frozenset)):
        for nested in value:
            _reject_runtime_authority_claims(nested)


def _validate_tool_pack_scope(
    requested_tool_packs: tuple[str, ...],
    allowed_tool_packs: tuple[str, ...],
) -> None:
    allowed = set(allowed_tool_packs)
    extra = [tool_pack for tool_pack in requested_tool_packs if tool_pack not in allowed]
    if extra:
        raise V1ProviderModelRoutingAuthorityError(
            "requested tool packs cannot exceed allowed tool packs"
        )


def _route_family(value: Any) -> str:
    route_family = _normalize_token(_required_text(value, "route_family"))
    if route_family not in ALLOWED_ROUTE_FAMILIES:
        raise V1ProviderModelRoutingAuthorityError("route family is not allowed")
    return route_family


def _model_role(value: Any) -> str:
    model_role = _normalize_token(_required_text(value, "model_role"))
    if model_role not in ALLOWED_MODEL_ROLES:
        raise V1ProviderModelRoutingAuthorityError("model role is not allowed")
    return model_role


def _data_sensitivity(value: Any) -> str:
    sensitivity = _normalize_token(_required_text(value, "data_sensitivity"))
    if sensitivity not in ALLOWED_DATA_SENSITIVITY:
        raise V1ProviderModelRoutingAuthorityError("data sensitivity is not allowed")
    return sensitivity


def _prompt_context_class(value: Any) -> str:
    prompt_class = _normalize_token(_required_text(value, "prompt_context_class"))
    if prompt_class not in ALLOWED_PROMPT_CONTEXT_CLASSES:
        raise V1ProviderModelRoutingAuthorityError(
            "prompt context class is not allowed"
        )
    return prompt_class


def _budget_class(value: Any) -> str:
    budget_class = _normalize_token(_required_text(value, "budget_class"))
    if budget_class not in ALLOWED_BUDGET_CLASSES:
        raise V1ProviderModelRoutingAuthorityError("budget class is not allowed")
    return budget_class


def _cost_class(value: Any) -> str:
    cost_class = _normalize_token(_required_text(value, "estimated_cost_class"))
    if cost_class not in ALLOWED_COST_CLASSES:
        raise V1ProviderModelRoutingAuthorityError("estimated cost class is not allowed")
    return cost_class


def _latency_tier(value: Any) -> str:
    latency_tier = _normalize_token(_required_text(value, "latency_tier"))
    if latency_tier not in ALLOWED_LATENCY_TIERS:
        raise V1ProviderModelRoutingAuthorityError("latency tier is not allowed")
    return latency_tier


def _mapping(value: Any, field_name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping) or not value:
        raise V1ProviderModelRoutingAuthorityError(f"{field_name} is required")
    return value


def _mapping_sequence(value: Any, field_name: str) -> tuple[Mapping[str, Any], ...]:
    if (
        not isinstance(value, Sequence)
        or isinstance(value, (str, bytes, bytearray))
        or not value
    ):
        raise V1ProviderModelRoutingAuthorityError(f"{field_name} is required")
    if not all(isinstance(item, Mapping) and item for item in value):
        raise V1ProviderModelRoutingAuthorityError(f"{field_name} must contain mappings")
    return tuple(value)


def _required_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise V1ProviderModelRoutingAuthorityError(f"{field_name} is required")
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
        raise V1ProviderModelRoutingAuthorityError(f"{field_name} must be a string sequence")
    normalized = tuple(str(item).strip() for item in value if str(item).strip())
    if not normalized and not allow_empty:
        raise V1ProviderModelRoutingAuthorityError(f"{field_name} is required")
    return normalized


def _require_true_confirmation(value: Any, field_name: str) -> None:
    if value is True:
        return
    if isinstance(value, Mapping) and value.get("confirmed") is True:
        return
    raise V1ProviderModelRoutingAuthorityError(f"{field_name} confirmation is required")


def _normalize_token(value: str) -> str:
    return value.strip().lower().replace("-", "_").replace(" ", "_")


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
