"""V1 shell/harness guiderail input contract.

This module is the approved V1-G15 candidate contract slice. It validates
structured guiderail input from shells and harnesses so later authority
lanes can classify requests without relying on raw prompts or implicit
capability claims. It does not wire shells, execute capabilities, route
providers, mutate files, activate HumanInput, or invoke external systems.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import hashlib
import json
from typing import Any, Final


SCHEMA_VERSION: Final[str] = "v1-g15-candidate"
ALLOWED_GUARDRAIL_MODES: Final[frozenset[str]] = frozenset(
    {"dry_run", "preview_only", "approval_required", "execution_authorized"}
)
ALLOWED_POSTURES: Final[frozenset[str]] = frozenset(
    {"dry_run", "preview_only", "approval_required", "execution_authorized"}
)
ALLOWED_CAPABILITY_LANES: Final[frozenset[str]] = frozenset(
    {
        "automation",
        "browser_network",
        "connector",
        "drafting",
        "file_mutation",
        "informational",
        "office_action",
        "physical_world",
        "planning",
        "provider_model",
        "shell",
        "tool",
    }
)
REQUIRED_TOP_LEVEL_FIELDS: Final[tuple[str, ...]] = (
    "capability_profile",
    "guardrail_mode",
    "approval_policy",
    "actor_scope",
    "session_scope",
    "tenant_scope",
    "shell_scope",
    "allowed_capability_lanes",
    "destructive_edit_delete_policy",
    "file_mutation_policy",
    "provider_model_policy",
    "connector_policy",
    "browser_network_policy",
    "physical_world_policy",
    "emergency_stop_expectations",
    "rollback_expectations",
    "dry_run_vs_execution_authorized_posture",
    "operator_approval_evidence_expectations",
    "audit_evidence_linkage_expectations",
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
FORBIDDEN_TRUE_CLAIM_KEYS: Final[frozenset[str]] = frozenset(
    {
        "approval_token_issued",
        "browser_action_executed",
        "connector_invoked",
        "consumer_integration_added",
        "device_command_invoked",
        "execution_allowed",
        "file_mutation_executed",
        "final_api_freeze_approved",
        "humaninput_bridge_activated",
        "model_routed",
        "network_action_executed",
        "physical_world_invoked",
        "product_ready",
        "provider_model_routed",
        "robotics_invoked",
        "shell_wired",
        "side_effects_allowed",
        "tool_executed",
    }
)


class V1GuiderailInputError(ValueError):
    """Raised when shell/harness guiderail input fails closed."""


def validate_v1_shell_harness_guiderail_input(
    guiderail_input: Mapping[str, Any],
) -> dict[str, Any]:
    """Return normalized V1 shell/harness guiderail input metadata."""

    if not isinstance(guiderail_input, Mapping):
        raise V1GuiderailInputError("guiderail_input must be a mapping")

    _reject_raw_sensitive_content(guiderail_input)
    _reject_runtime_authority_claims(guiderail_input)

    for field_name in REQUIRED_TOP_LEVEL_FIELDS:
        if field_name not in guiderail_input:
            raise V1GuiderailInputError(f"{field_name} is required")

    capability_profile = _mapping(
        guiderail_input.get("capability_profile"),
        "capability_profile",
    )
    guardrail_mode = _required_enum(
        guiderail_input.get("guardrail_mode"),
        ALLOWED_GUARDRAIL_MODES,
        "guardrail_mode",
    )
    approval_policy = _mapping(guiderail_input.get("approval_policy"), "approval_policy")
    actor_scope = _required_text(guiderail_input.get("actor_scope"), "actor_scope")
    session_scope = _required_text(guiderail_input.get("session_scope"), "session_scope")
    tenant_scope = _required_text(guiderail_input.get("tenant_scope"), "tenant_scope")
    shell_scope = _required_text(guiderail_input.get("shell_scope"), "shell_scope")
    allowed_capability_lanes = _capability_lanes(
        guiderail_input.get("allowed_capability_lanes")
    )
    destructive_policy = _mapping(
        guiderail_input.get("destructive_edit_delete_policy"),
        "destructive_edit_delete_policy",
    )
    file_mutation_policy = _mapping(
        guiderail_input.get("file_mutation_policy"),
        "file_mutation_policy",
    )
    provider_model_policy = _mapping(
        guiderail_input.get("provider_model_policy"),
        "provider_model_policy",
    )
    connector_policy = _mapping(guiderail_input.get("connector_policy"), "connector_policy")
    browser_network_policy = _mapping(
        guiderail_input.get("browser_network_policy"),
        "browser_network_policy",
    )
    physical_world_policy = _mapping(
        guiderail_input.get("physical_world_policy"),
        "physical_world_policy",
    )
    emergency_stop = _mapping(
        guiderail_input.get("emergency_stop_expectations"),
        "emergency_stop_expectations",
    )
    rollback = _mapping(
        guiderail_input.get("rollback_expectations"),
        "rollback_expectations",
    )
    posture = _required_enum(
        guiderail_input.get("dry_run_vs_execution_authorized_posture"),
        ALLOWED_POSTURES,
        "dry_run_vs_execution_authorized_posture",
    )
    approval_evidence = _mapping(
        guiderail_input.get("operator_approval_evidence_expectations"),
        "operator_approval_evidence_expectations",
    )
    audit_linkage = _mapping(
        guiderail_input.get("audit_evidence_linkage_expectations"),
        "audit_evidence_linkage_expectations",
    )
    evidence_refs = _string_sequence(guiderail_input.get("evidence_refs", ()), "evidence_refs")

    _validate_profile(capability_profile, allowed_capability_lanes)
    _validate_destructive_policy(destructive_policy)
    _validate_file_mutation_policy(file_mutation_policy)
    _validate_policy_metadata_only(provider_model_policy, "provider_model_policy")
    _validate_policy_metadata_only(connector_policy, "connector_policy")
    _validate_policy_metadata_only(browser_network_policy, "browser_network_policy")
    _validate_physical_world_policy(physical_world_policy)
    _validate_consequential_expectations(
        allowed_capability_lanes,
        emergency_stop,
        rollback,
        approval_evidence,
        audit_linkage,
    )

    record = {
        "record_type": "v1_shell_harness_guiderail_input",
        "schema_version": SCHEMA_VERSION,
        "capability_profile": _json_ready(capability_profile),
        "guardrail_mode": guardrail_mode,
        "approval_policy": _json_ready(approval_policy),
        "actor_scope": actor_scope,
        "session_scope": session_scope,
        "tenant_scope": tenant_scope,
        "shell_scope": shell_scope,
        "allowed_capability_lanes": list(allowed_capability_lanes),
        "destructive_edit_delete_policy": _json_ready(destructive_policy),
        "file_mutation_policy": _json_ready(file_mutation_policy),
        "provider_model_policy": _json_ready(provider_model_policy),
        "connector_policy": _json_ready(connector_policy),
        "browser_network_policy": _json_ready(browser_network_policy),
        "physical_world_policy": _json_ready(physical_world_policy),
        "emergency_stop_expectations": _json_ready(emergency_stop),
        "rollback_expectations": _json_ready(rollback),
        "dry_run_vs_execution_authorized_posture": posture,
        "operator_approval_evidence_expectations": _json_ready(approval_evidence),
        "audit_evidence_linkage_expectations": _json_ready(audit_linkage),
        "evidence_refs": list(evidence_refs),
        "capability_open": True,
        "authority_gated": True,
        "proof_not_authority": True,
        "execution_allowed": False,
        "side_effects_allowed": False,
        "approval_token_issued": False,
        "provider_model_routed": False,
        "shell_wired": False,
        "connector_invoked": False,
        "browser_action_executed": False,
        "network_action_executed": False,
        "file_mutation_executed": False,
        "physical_world_invoked": False,
        "consumer_integration_added": False,
        "final_api_freeze_approved": False,
        "product_ready": False,
        "metadata": {
            "v1_runtime_slice": "shell_harness_guiderail_contract",
            "candidate_only": True,
            "non_executing": True,
        },
    }
    record["record_hash"] = _record_hash(record)
    return record


def _validate_profile(
    capability_profile: Mapping[str, Any],
    allowed_capability_lanes: tuple[str, ...],
) -> None:
    _required_text(capability_profile.get("profile_id"), "capability_profile.profile_id")
    profile_lanes = _capability_lanes(capability_profile.get("capability_lanes"))
    if not set(profile_lanes).issubset(set(allowed_capability_lanes)):
        raise V1GuiderailInputError("capability_profile lanes must be allowed")


def _validate_destructive_policy(policy: Mapping[str, Any]) -> None:
    if policy.get("requires_explicit_approval") is not True:
        raise V1GuiderailInputError(
            "destructive_edit_delete_policy requires explicit approval"
        )
    if policy.get("mutation_without_approval_allowed") is not False:
        raise V1GuiderailInputError("destructive mutation without approval is not allowed")


def _validate_file_mutation_policy(policy: Mapping[str, Any]) -> None:
    if policy.get("requires_explicit_approval") is not True:
        raise V1GuiderailInputError("file_mutation_policy requires explicit approval")
    if policy.get("execution_allowed_without_future_policy") is not False:
        raise V1GuiderailInputError("file mutation execution requires a future policy lane")


def _validate_policy_metadata_only(policy: Mapping[str, Any], field_name: str) -> None:
    if policy.get("policy_metadata_only") is not True:
        raise V1GuiderailInputError(f"{field_name} must be policy metadata only")
    if policy.get("execution_allowed") is not False:
        raise V1GuiderailInputError(f"{field_name} cannot allow execution")


def _validate_physical_world_policy(policy: Mapping[str, Any]) -> None:
    mode = _required_text(policy.get("mode"), "physical_world_policy.mode")
    if mode != "blocked_until_dedicated_authority_lane":
        raise V1GuiderailInputError(
            "physical_world_policy requires a dedicated authority lane"
        )
    if policy.get("execution_allowed") is not False:
        raise V1GuiderailInputError("physical-world execution is not allowed")


def _validate_consequential_expectations(
    lanes: tuple[str, ...],
    emergency_stop: Mapping[str, Any],
    rollback: Mapping[str, Any],
    approval_evidence: Mapping[str, Any],
    audit_linkage: Mapping[str, Any],
) -> None:
    consequential = {
        "automation",
        "browser_network",
        "connector",
        "file_mutation",
        "office_action",
        "physical_world",
        "provider_model",
        "shell",
        "tool",
    }
    if set(lanes) & consequential:
        if emergency_stop.get("represented") is not True:
            raise V1GuiderailInputError("emergency stop expectations are required")
        if rollback.get("represented") is not True:
            raise V1GuiderailInputError("rollback expectations are required")
    if approval_evidence.get("represented") is not True:
        raise V1GuiderailInputError("operator approval evidence expectations are required")
    if audit_linkage.get("represented") is not True:
        raise V1GuiderailInputError("audit/evidence linkage expectations are required")


def _reject_raw_sensitive_content(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            if isinstance(key, str) and key.strip().lower() in RAW_SENSITIVE_KEYS:
                raise V1GuiderailInputError("raw sensitive content is not accepted")
            _reject_raw_sensitive_content(nested)
    elif isinstance(value, (list, tuple, set, frozenset)):
        for nested in value:
            _reject_raw_sensitive_content(nested)
    elif isinstance(value, str):
        folded = value.strip().lower()
        if any(marker in folded for marker in RAW_SENSITIVE_VALUE_MARKERS):
            raise V1GuiderailInputError("raw sensitive content is not accepted")


def _reject_runtime_authority_claims(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            if (
                isinstance(key, str)
                and key.strip().lower() in FORBIDDEN_TRUE_CLAIM_KEYS
                and nested is not False
            ):
                raise V1GuiderailInputError("guiderail input cannot grant runtime authority")
            _reject_runtime_authority_claims(nested)
    elif isinstance(value, (list, tuple, set, frozenset)):
        for nested in value:
            _reject_runtime_authority_claims(nested)


def _mapping(value: Any, field_name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping) or not value:
        raise V1GuiderailInputError(f"{field_name} is required")
    return value


def _capability_lanes(value: Any) -> tuple[str, ...]:
    lanes = _string_sequence(value, "allowed_capability_lanes")
    if not lanes:
        raise V1GuiderailInputError("allowed_capability_lanes are required")
    unknown = [lane for lane in lanes if lane not in ALLOWED_CAPABILITY_LANES]
    if unknown:
        raise V1GuiderailInputError("unknown capability lane")
    return lanes


def _required_enum(value: Any, allowed: frozenset[str], field_name: str) -> str:
    normalized = _required_text(value, field_name).lower()
    if normalized not in allowed:
        raise V1GuiderailInputError(f"{field_name} is not allowed")
    return normalized


def _required_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise V1GuiderailInputError(f"{field_name} is required")
    return value.strip()


def _string_sequence(value: Any, field_name: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        value = (value,)
    if not isinstance(value, Sequence) or isinstance(value, (bytes, bytearray)):
        raise V1GuiderailInputError(f"{field_name} must be a string sequence")
    return tuple(str(item).strip().lower() for item in value if str(item).strip())


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
