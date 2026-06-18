"""V1 executable real provider executor invocation wrapper.

This module is the approved V1-G51 candidate runtime slice. It validates the
V1-G50 invocation envelope metadata, V1-G49 executor authority linkage,
V1-G48 credential/network hardening linkage, redaction policy, approval
linkage, and execution boundaries before calling a caller-injected provider
executor. It contains no provider SDK clients, direct network client code,
ambient secret lookup, credential value access, fallback execution, tools,
connectors, or consumer repository integration.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
import hashlib
import json
from typing import Any, Final


SCHEMA_VERSION: Final[str] = "v1-g51-candidate"
G50_REQUEST_ENVELOPE_TYPE: Final[str] = (
    "real_provider_executor_invocation_request_metadata"
)
G50_RESPONSE_ENVELOPE_TYPE: Final[str] = (
    "real_provider_executor_invocation_response_metadata"
)
G51_APPROVAL_SCOPE: Final[str] = (
    "v1-g51-executable-real-provider-executor-invocation"
)
ALLOWED_FINISH_STATUSES: Final[frozenset[str]] = frozenset(
    {"completed", "blocked", "failed", "cancelled"}
)
REQUIRED_EXECUTION_FIELDS: Final[tuple[str, ...]] = (
    "invocation_id",
    "invocation_request_envelope",
    "invocation_response_envelope",
    "provider_model_scope",
    "executor_authority_linkage",
    "credential_network_hardening_linkage",
    "g50_execution_boundary_metadata",
    "provider_executor_ref",
    "provider_request_ref",
    "g51_execution_approval_linkage",
    "g51_execution_boundary",
    "audit_evidence_linkage",
    "redaction_policy",
    "caller_injected_provider_executor_confirmation",
    "no_built_in_provider_sdk_confirmation",
    "no_direct_network_code_confirmation",
    "no_provider_endpoint_resolution_confirmation",
    "no_secret_lookup_confirmation",
    "no_credential_value_access_confirmation",
    "no_provider_token_or_api_key_access_confirmation",
    "no_fallback_execution_confirmation",
    "no_connector_browser_network_physical_world_confirmation",
    "no_raw_prompt_model_response_customer_data_persistence_confirmation",
)
RAW_SENSITIVE_KEYS: Final[frozenset[str]] = frozenset(
    {
        "api_key",
        "bearer_token",
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
        "raw_request_payload",
        "raw_response_payload",
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
    "raw request payload",
    "raw response payload",
    "raw secret",
    "raw-secret-",
    "secret value",
)
FORBIDDEN_TRUE_CLAIM_KEYS: Final[frozenset[str]] = frozenset(
    {
        "ambient_environment_secret_lookup_added",
        "ambient_secret_lookup_performed",
        "browser_action_executed",
        "built_in_provider_sdk_added",
        "built_in_provider_sdk_used",
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
        "direct_network_client_added",
        "direct_network_code_added",
        "direct_network_code_used",
        "direct_provider_sdk_added",
        "direct_provider_sdk_used",
        "drone_control_invoked",
        "external_send_added",
        "fallback_executed",
        "fallback_execution_added",
        "fallback_execution_allowed",
        "file_mutation_executed",
        "humaninput_bridge_activated",
        "iot_control_invoked",
        "network_call_performed",
        "physical_world_invoked",
        "product_ready",
        "provider_configuration_changes_added",
        "provider_endpoint_resolution_added",
        "provider_endpoint_resolution_performed",
        "provider_readiness_check_performed",
        "provider_readiness_network_check_added",
        "provider_readiness_network_check_allowed",
        "provider_token_or_api_key_access_added",
        "provider_token_or_api_key_accessed",
        "raw_customer_data_persisted",
        "raw_diff_or_patch_persisted",
        "raw_file_content_persisted",
        "raw_model_response_persisted",
        "raw_prompt_persisted",
        "raw_sensitive_content_persisted",
        "robot_control_invoked",
        "robotics_invoked",
        "scheduled_task_executed",
        "secret_lookup_added",
        "secret_lookup_performed",
        "shell_runtime_wired",
        "token_guardian_live_routing_added",
        "tool_executed",
        "tool_execution_added",
    }
)


class V1ExecutableRealProviderExecutorInvocationError(ValueError):
    """Raised when V1-G51 executable provider invocation is not authorized."""


def execute_v1_executable_real_provider_executor_invocation(
    invocation_request: Mapping[str, Any],
    provider_executor: Callable[[Mapping[str, Any]], Mapping[str, Any]],
) -> dict[str, Any]:
    """Execute one bounded provider invocation through an injected executor.

    The wrapper performs local validation and returns sanitized evidence. It
    does not include provider SDK clients, network clients, endpoint resolution,
    secret lookup, credential value access, or fallback behavior.
    """

    if not isinstance(invocation_request, Mapping):
        raise V1ExecutableRealProviderExecutorInvocationError(
            "invocation_request must be a mapping"
        )
    if not callable(provider_executor):
        raise V1ExecutableRealProviderExecutorInvocationError(
            "provider_executor must be injected and callable"
        )

    _reject_raw_sensitive_content(invocation_request)
    _reject_forbidden_claims(invocation_request)

    for field_name in REQUIRED_EXECUTION_FIELDS:
        if field_name not in invocation_request:
            raise V1ExecutableRealProviderExecutorInvocationError(
                f"{field_name} is required"
            )

    invocation_id = _required_text(invocation_request.get("invocation_id"), "invocation_id")
    request_envelope = _validate_g50_request_envelope(
        invocation_request.get("invocation_request_envelope")
    )
    response_envelope = _validate_g50_response_envelope(
        invocation_request.get("invocation_response_envelope")
    )
    scope = _validate_provider_model_scope(invocation_request.get("provider_model_scope"))
    authority = _validate_executor_authority_linkage(
        invocation_request.get("executor_authority_linkage")
    )
    hardening = _validate_credential_network_hardening_linkage(
        invocation_request.get("credential_network_hardening_linkage")
    )
    g50_boundary = _validate_g50_execution_boundary_metadata(
        invocation_request.get("g50_execution_boundary_metadata")
    )
    provider_executor_ref = _required_text(
        invocation_request.get("provider_executor_ref"),
        "provider_executor_ref",
    )
    provider_request_ref = _required_text(
        invocation_request.get("provider_request_ref"),
        "provider_request_ref",
    )
    approval = _validate_g51_execution_approval_linkage(
        invocation_request.get("g51_execution_approval_linkage")
    )
    boundary = _validate_g51_execution_boundary(
        invocation_request.get("g51_execution_boundary")
    )
    audit = _validate_audit_linkage(invocation_request.get("audit_evidence_linkage"))
    redaction = _validate_redaction_policy(invocation_request.get("redaction_policy"))

    for field_name in (
        "caller_injected_provider_executor_confirmation",
        "no_built_in_provider_sdk_confirmation",
        "no_direct_network_code_confirmation",
        "no_provider_endpoint_resolution_confirmation",
        "no_secret_lookup_confirmation",
        "no_credential_value_access_confirmation",
        "no_provider_token_or_api_key_access_confirmation",
        "no_fallback_execution_confirmation",
        "no_connector_browser_network_physical_world_confirmation",
        "no_raw_prompt_model_response_customer_data_persistence_confirmation",
    ):
        _require_true_confirmation(invocation_request.get(field_name), field_name)

    executor_payload = {
        "invocation_id": invocation_id,
        "invocation_request_id": request_envelope["invocation_request_id"],
        "invocation_response_id": response_envelope["invocation_response_id"],
        "provider_scope_ref": scope["provider_scope_ref"],
        "model_scope_ref": scope["model_scope_ref"],
        "executor_authority_ref": authority["executor_authority_ref"],
        "credential_policy_ref": hardening["credential_policy_ref"],
        "network_policy_ref": hardening["network_policy_ref"],
        "provider_executor_ref": provider_executor_ref,
        "provider_request_ref": provider_request_ref,
        "redacted_input_ref": request_envelope["redacted_input_ref"],
        "redacted_output_ref": response_envelope["redacted_output_ref"],
        "redaction_policy_ref": redaction["redaction_policy_ref"],
        "audit_record_ref": audit["audit_record_ref"],
        "timeout_policy_ref": g50_boundary["timeout_policy_ref"],
        "retry_policy_ref": g50_boundary["retry_policy_ref"],
        "cost_policy_ref": g50_boundary["cost_policy_ref"],
        "failure_policy_ref": g50_boundary["failure_policy_ref"],
        "max_attempts": boundary["max_attempts"],
    }

    try:
        provider_result = provider_executor(executor_payload)
    except Exception as exc:  # pragma: no cover - exact exception type is caller-owned.
        raise V1ExecutableRealProviderExecutorInvocationError(
            "provider executor failed"
        ) from exc

    result = _validate_provider_result(provider_result)

    record = {
        "record_type": "v1_executable_real_provider_executor_invocation",
        "schema_version": SCHEMA_VERSION,
        "invocation_id": invocation_id,
        "invocation_request_id": request_envelope["invocation_request_id"],
        "invocation_response_id": response_envelope["invocation_response_id"],
        "provider_scope_ref": scope["provider_scope_ref"],
        "model_scope_ref": scope["model_scope_ref"],
        "executor_authority_ref": authority["executor_authority_ref"],
        "credential_policy_ref": hardening["credential_policy_ref"],
        "network_policy_ref": hardening["network_policy_ref"],
        "provider_executor_ref": provider_executor_ref,
        "provider_request_ref": provider_request_ref,
        "provider_call_ref": result["provider_call_ref"],
        "provider_output_ref": result["redacted_output_ref"],
        "redacted_output_summary_ref": result["redacted_output_summary_ref"],
        "finish_status": result["finish_status"],
        "usage_metadata": result["usage_metadata"],
        "g51_execution_approval_linkage": approval,
        "g51_execution_boundary": boundary,
        "audit_evidence_linkage": audit,
        "redaction_policy": redaction,
        "capability_open": True,
        "authority_gated": True,
        "candidate_only": True,
        "executable_real_provider_executor_invocation_wrapper_added": True,
        "provider_executor_invocation_added": True,
        "provider_executor_invoked": True,
        "real_provider_executor_invocation_added": True,
        "real_provider_executor_invoked": True,
        "actual_model_request_dispatch_execution_added": True,
        "model_request_dispatched": True,
        "caller_injected_provider_executor_only": True,
        "local_tests_use_fake_injected_executors_only": True,
        "built_in_provider_sdk_added": False,
        "built_in_provider_sdk_used": False,
        "direct_provider_sdk_added": False,
        "direct_provider_sdk_used": False,
        "direct_network_code_added": False,
        "direct_network_code_used": False,
        "network_call_performed_by_lima_harness": False,
        "provider_endpoint_resolution_added": False,
        "provider_endpoint_resolution_performed": False,
        "provider_readiness_network_check_added": False,
        "token_guardian_live_routing_added": False,
        "ambient_environment_secret_lookup_added": False,
        "secret_lookup_added": False,
        "secret_lookup_performed": False,
        "credential_value_access_added": False,
        "credential_value_accessed": False,
        "provider_token_or_api_key_access_added": False,
        "provider_token_or_api_key_accessed": False,
        "credential_storage_or_rotation_added": False,
        "provider_configuration_changes_added": False,
        "fallback_execution_added": False,
        "fallback_executed": False,
        "tool_execution_added": False,
        "tool_executed": False,
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
        "raw_prompt_persisted": False,
        "raw_model_response_persisted": False,
        "raw_customer_data_persisted": False,
        "raw_secret_or_credential_persisted": False,
        "provider_token_or_api_key_persisted": False,
        "raw_diff_or_patch_persisted": False,
        "raw_file_content_persisted": False,
        "raw_sensitive_content_persisted": False,
        "product_ready": False,
        "metadata": {
            "v1_runtime_slice": "executable_real_provider_executor_invocation",
            "sanitized_evidence_only": True,
            "provider_executor_injected": True,
            "no_built_in_provider_sdk": True,
            "no_direct_network_code": True,
        },
    }
    _reject_raw_sensitive_content(record)
    record["record_hash"] = _record_hash(record)
    return record


def _validate_g50_request_envelope(value: Any) -> dict[str, str]:
    envelope = _mapping(value, "invocation_request_envelope")
    if envelope.get("envelope_type") != G50_REQUEST_ENVELOPE_TYPE:
        raise V1ExecutableRealProviderExecutorInvocationError(
            "V1-G50 invocation request envelope is required"
        )
    if envelope.get("metadata_only") is not True:
        raise V1ExecutableRealProviderExecutorInvocationError(
            "V1-G50 request envelope must be metadata-only"
        )
    if envelope.get("non_executing") is not True:
        raise V1ExecutableRealProviderExecutorInvocationError(
            "V1-G50 request envelope must be non-executing metadata"
        )
    if envelope.get("proof_not_execution") is not True:
        raise V1ExecutableRealProviderExecutorInvocationError(
            "V1-G50 request envelope proof metadata is required"
        )
    if envelope.get("guardian_gate_required") is not True:
        raise V1ExecutableRealProviderExecutorInvocationError(
            "Guardian gate metadata is required"
        )
    for field_name in (
        "provider_executor_invocation_allowed",
        "real_provider_executor_invocation_allowed",
        "fake_provider_executor_invocation_allowed",
        "executable_provider_invocation_allowed",
        "model_request_dispatch_allowed",
        "provider_sdk_client_allowed",
        "provider_endpoint_resolution_allowed",
        "network_calls_allowed",
        "secret_lookup_allowed",
        "credential_value_access_allowed",
        "provider_token_or_api_key_access_allowed",
        "fallback_execution_allowed",
        "raw_prompt_present",
        "raw_request_payload_present",
        "product_readiness_claim_allowed",
    ):
        if envelope.get(field_name) is not False:
            raise V1ExecutableRealProviderExecutorInvocationError(
                f"{field_name} must remain blocked in V1-G50 metadata"
            )
    return {
        "invocation_request_id": _required_text(
            envelope.get("invocation_request_id"),
            "invocation_request_id",
        ),
        "redacted_input_ref": _required_text(
            envelope.get("redacted_input_ref"),
            "redacted_input_ref",
        ),
    }


def _validate_g50_response_envelope(value: Any) -> dict[str, str]:
    envelope = _mapping(value, "invocation_response_envelope")
    if envelope.get("envelope_type") != G50_RESPONSE_ENVELOPE_TYPE:
        raise V1ExecutableRealProviderExecutorInvocationError(
            "V1-G50 invocation response envelope is required"
        )
    if envelope.get("metadata_only") is not True:
        raise V1ExecutableRealProviderExecutorInvocationError(
            "V1-G50 response envelope must be metadata-only"
        )
    if envelope.get("non_executing") is not True:
        raise V1ExecutableRealProviderExecutorInvocationError(
            "V1-G50 response envelope must be non-executing metadata"
        )
    if envelope.get("proof_not_execution") is not True:
        raise V1ExecutableRealProviderExecutorInvocationError(
            "V1-G50 response envelope proof metadata is required"
        )
    if envelope.get("invocation_status") != "not_invoked":
        raise V1ExecutableRealProviderExecutorInvocationError(
            "V1-G50 response envelope must remain not_invoked"
        )
    if envelope.get("sanitized_evidence_only") is not True:
        raise V1ExecutableRealProviderExecutorInvocationError(
            "V1-G50 response envelope must be sanitized evidence only"
        )
    for field_name in (
        "provider_executor_invoked",
        "real_provider_executor_invoked",
        "fake_provider_executor_invoked",
        "model_response_received",
        "network_call_performed",
        "provider_sdk_client_used",
        "provider_endpoint_resolved",
        "secret_lookup_performed",
        "credential_value_accessed",
        "fallback_execution_performed",
        "raw_model_response_present",
        "raw_response_payload_present",
        "raw_error_payload_present",
        "product_readiness_claim_allowed",
    ):
        if envelope.get(field_name) is not False:
            raise V1ExecutableRealProviderExecutorInvocationError(
                f"{field_name} must remain blocked in V1-G50 metadata"
            )
    return {
        "invocation_response_id": _required_text(
            envelope.get("invocation_response_id"),
            "invocation_response_id",
        ),
        "redacted_output_ref": _required_text(
            envelope.get("redacted_output_ref"),
            "redacted_output_ref",
        ),
    }


def _validate_provider_model_scope(value: Any) -> dict[str, str]:
    scope = _mapping(value, "provider_model_scope")
    if scope.get("reference_only") is not True:
        raise V1ExecutableRealProviderExecutorInvocationError(
            "provider/model scope must be reference-only"
        )
    if scope.get("metadata_only") is not True:
        raise V1ExecutableRealProviderExecutorInvocationError(
            "provider/model scope must be metadata-only"
        )
    for field_name in (
        "provider_configuration_changed",
        "provider_endpoint_selected",
        "model_invocation_selected",
        "executable_invocation_selected",
    ):
        if scope.get(field_name) is not False:
            raise V1ExecutableRealProviderExecutorInvocationError(
                f"{field_name} is not allowed"
            )
    return {
        "provider_scope_ref": _required_text(
            scope.get("provider_scope_ref"),
            "provider_scope_ref",
        ),
        "model_scope_ref": _required_text(
            scope.get("model_scope_ref"),
            "model_scope_ref",
        ),
    }


def _validate_executor_authority_linkage(value: Any) -> dict[str, str]:
    authority = _mapping(value, "executor_authority_linkage")
    if authority.get("reference_only") is not True:
        raise V1ExecutableRealProviderExecutorInvocationError(
            "executor authority linkage must be reference-only"
        )
    if authority.get("metadata_only") is not True:
        raise V1ExecutableRealProviderExecutorInvocationError(
            "executor authority linkage must be metadata-only"
        )
    if authority.get("executor_authority_design_required") is not True:
        raise V1ExecutableRealProviderExecutorInvocationError(
            "V1-G49 executor authority design is required"
        )
    for field_name in (
        "executor_invocation_allowed",
        "real_provider_executor_invocation_allowed",
        "fake_provider_executor_invocation_allowed",
        "executable_provider_invocation_allowed",
    ):
        if authority.get(field_name) is not False:
            raise V1ExecutableRealProviderExecutorInvocationError(
                f"{field_name} must remain blocked in V1-G49 metadata"
            )
    return {
        "executor_authority_ref": _required_text(
            authority.get("executor_authority_ref"),
            "executor_authority_ref",
        )
    }


def _validate_credential_network_hardening_linkage(value: Any) -> dict[str, str]:
    hardening = _mapping(value, "credential_network_hardening_linkage")
    if hardening.get("credential_reference_only") is not True:
        raise V1ExecutableRealProviderExecutorInvocationError(
            "credential policy must be reference-only"
        )
    if hardening.get("network_policy_reference_only") is not True:
        raise V1ExecutableRealProviderExecutorInvocationError(
            "network policy must be reference-only"
        )
    if hardening.get("deny_by_default_network_required") is not True:
        raise V1ExecutableRealProviderExecutorInvocationError(
            "deny-by-default network policy is required"
        )
    for field_name in (
        "secret_lookup_allowed",
        "credential_value_access_allowed",
        "provider_token_or_api_key_access_allowed",
        "provider_endpoint_resolution_allowed",
        "network_calls_allowed",
        "direct_provider_egress_allowed",
    ):
        if hardening.get(field_name) is not False:
            raise V1ExecutableRealProviderExecutorInvocationError(
                f"{field_name} is not allowed"
            )
    return {
        "credential_policy_ref": _required_text(
            hardening.get("credential_policy_ref"),
            "credential_policy_ref",
        ),
        "network_policy_ref": _required_text(
            hardening.get("network_policy_ref"),
            "network_policy_ref",
        ),
    }


def _validate_g50_execution_boundary_metadata(value: Any) -> dict[str, str]:
    boundary = _mapping(value, "g50_execution_boundary_metadata")
    if boundary.get("estimated_cost_only") is not True:
        raise V1ExecutableRealProviderExecutorInvocationError(
            "V1-G50 cost policy must remain estimate-only"
        )
    if boundary.get("metadata_only") is not True:
        raise V1ExecutableRealProviderExecutorInvocationError(
            "V1-G50 execution boundary must be metadata-only"
        )
    if boundary.get("non_executing") is not True:
        raise V1ExecutableRealProviderExecutorInvocationError(
            "V1-G50 execution boundary must be non-executing"
        )
    if boundary.get("max_attempts_metadata") != 1:
        raise V1ExecutableRealProviderExecutorInvocationError(
            "V1-G50 max attempts metadata must be one"
        )
    for field_name in (
        "provider_executor_call_allowed",
        "retry_execution_allowed",
        "timeout_enforcement_runtime_added",
        "billing_call_allowed",
        "cost_meter_network_call_allowed",
        "provider_readiness_network_check_allowed",
        "fallback_execution_allowed",
        "error_payload_raw_persistence_allowed",
    ):
        if boundary.get(field_name) is not False:
            raise V1ExecutableRealProviderExecutorInvocationError(
                f"{field_name} must remain blocked in V1-G50 metadata"
            )
    return {
        "timeout_policy_ref": _required_text(
            boundary.get("timeout_policy_ref"),
            "timeout_policy_ref",
        ),
        "retry_policy_ref": _required_text(
            boundary.get("retry_policy_ref"),
            "retry_policy_ref",
        ),
        "cost_policy_ref": _required_text(
            boundary.get("cost_policy_ref"),
            "cost_policy_ref",
        ),
        "failure_policy_ref": _required_text(
            boundary.get("failure_policy_ref"),
            "failure_policy_ref",
        ),
    }


def _validate_g51_execution_approval_linkage(value: Any) -> dict[str, Any]:
    approval = _mapping(value, "g51_execution_approval_linkage")
    approval_evidence_ref = _required_text(
        approval.get("approval_evidence_ref"),
        "g51_execution_approval_linkage.approval_evidence_ref",
    )
    if approval.get("approval_evidence_current") is not True:
        raise V1ExecutableRealProviderExecutorInvocationError(
            "execution approval evidence must be current"
        )
    if approval.get("approval_scope") != G51_APPROVAL_SCOPE:
        raise V1ExecutableRealProviderExecutorInvocationError(
            "V1-G51 execution approval scope is required"
        )
    if (
        approval.get(
            "grants_executable_real_provider_executor_invocation_authority"
        )
        is not True
    ):
        raise V1ExecutableRealProviderExecutorInvocationError(
            "executable provider invocation authority is required"
        )
    if approval.get("proof_of_operator_approval") is not True:
        raise V1ExecutableRealProviderExecutorInvocationError(
            "operator approval proof is required"
        )
    return {
        "approval_evidence_ref": approval_evidence_ref,
        "approval_evidence_current": True,
        "approval_scope": G51_APPROVAL_SCOPE,
        "grants_executable_real_provider_executor_invocation_authority": True,
        "proof_of_operator_approval": True,
    }


def _validate_g51_execution_boundary(value: Any) -> dict[str, Any]:
    boundary = _mapping(value, "g51_execution_boundary")
    boundary_ref = _required_text(
        boundary.get("provider_executor_boundary_ref"),
        "g51_execution_boundary.provider_executor_boundary_ref",
    )
    if boundary.get("caller_injected_provider_executor") is not True:
        raise V1ExecutableRealProviderExecutorInvocationError(
            "caller-injected provider executor is required"
        )
    if boundary.get("provider_executor_call_allowed") is not True:
        raise V1ExecutableRealProviderExecutorInvocationError(
            "G51 provider executor call authority is required"
        )
    if boundary.get("max_attempts") != 1:
        raise V1ExecutableRealProviderExecutorInvocationError(
            "max_attempts must be one"
        )
    for field_name in (
        "built_in_provider_sdk_used",
        "direct_provider_sdk_used",
        "direct_network_code_used",
        "provider_endpoint_resolution_performed",
        "network_call_performed_by_lima_harness",
        "ambient_secret_lookup_performed",
        "secret_lookup_performed",
        "credential_value_accessed",
        "provider_token_or_api_key_accessed",
        "fallback_allowed",
        "tool_execution_allowed",
        "consumer_repo_mutation_allowed",
        "connector_browser_network_file_device_robotics_physical_world_behavior_allowed",
    ):
        if boundary.get(field_name) is not False:
            raise V1ExecutableRealProviderExecutorInvocationError(
                "execution boundary allows forbidden behavior"
            )
    return {
        "provider_executor_boundary_ref": boundary_ref,
        "caller_injected_provider_executor": True,
        "provider_executor_call_allowed": True,
        "max_attempts": 1,
        "built_in_provider_sdk_used": False,
        "direct_provider_sdk_used": False,
        "direct_network_code_used": False,
        "provider_endpoint_resolution_performed": False,
        "network_call_performed_by_lima_harness": False,
        "ambient_secret_lookup_performed": False,
        "secret_lookup_performed": False,
        "credential_value_accessed": False,
        "provider_token_or_api_key_accessed": False,
        "fallback_allowed": False,
        "tool_execution_allowed": False,
        "consumer_repo_mutation_allowed": False,
        "connector_browser_network_file_device_robotics_physical_world_behavior_allowed": False,
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
        raise V1ExecutableRealProviderExecutorInvocationError(
            "audit linkage is required"
        )
    if audit.get("sanitized_evidence_only") is not True:
        raise V1ExecutableRealProviderExecutorInvocationError(
            "audit linkage must be sanitized evidence only"
        )
    return {
        "audit_record_ref": audit_record_ref,
        "evidence_refs": list(evidence_refs),
        "required": True,
        "sanitized_evidence_only": True,
    }


def _validate_redaction_policy(value: Any) -> dict[str, Any]:
    policy = _mapping(value, "redaction_policy")
    redaction_policy_ref = _required_text(
        policy.get("redaction_policy_ref"),
        "redaction_policy.redaction_policy_ref",
    )
    if policy.get("redacted_input_required") is not True:
        raise V1ExecutableRealProviderExecutorInvocationError(
            "redacted input is required"
        )
    if policy.get("redacted_output_required") is not True:
        raise V1ExecutableRealProviderExecutorInvocationError(
            "redacted output is required"
        )
    for field_name in (
        "raw_prompt_persistence_allowed",
        "raw_model_response_persistence_allowed",
        "raw_customer_data_persistence_allowed",
        "raw_secret_credential_persistence_allowed",
        "raw_diff_patch_file_content_persistence_allowed",
    ):
        if policy.get(field_name) is not False:
            raise V1ExecutableRealProviderExecutorInvocationError(
                "raw prompt/model response/customer data persistence is not allowed"
            )
    return {
        "redaction_policy_ref": redaction_policy_ref,
        "redacted_input_required": True,
        "redacted_output_required": True,
        "raw_prompt_persistence_allowed": False,
        "raw_model_response_persistence_allowed": False,
        "raw_customer_data_persistence_allowed": False,
        "raw_secret_credential_persistence_allowed": False,
        "raw_diff_patch_file_content_persistence_allowed": False,
    }


def _validate_provider_result(value: Any) -> dict[str, Any]:
    result = _mapping(value, "provider_result")
    _reject_raw_sensitive_content(result)
    _reject_forbidden_claims(result)

    finish_status = _normalize_token(
        _required_text(result.get("finish_status"), "finish_status")
    )
    if finish_status not in ALLOWED_FINISH_STATUSES:
        raise V1ExecutableRealProviderExecutorInvocationError(
            "finish_status is not allowed"
        )

    usage = _mapping(result.get("usage_metadata"), "usage_metadata")
    input_tokens = _nonnegative_int(usage.get("input_tokens"), "input_tokens")
    output_tokens = _nonnegative_int(usage.get("output_tokens"), "output_tokens")
    total_tokens = _nonnegative_int(usage.get("total_tokens"), "total_tokens")
    if total_tokens < input_tokens + output_tokens:
        raise V1ExecutableRealProviderExecutorInvocationError(
            "total_tokens is inconsistent"
        )

    return {
        "provider_call_ref": _required_text(
            result.get("provider_call_ref"),
            "provider_call_ref",
        ),
        "redacted_output_ref": _required_text(
            result.get("redacted_output_ref"),
            "redacted_output_ref",
        ),
        "redacted_output_summary_ref": _required_text(
            result.get("redacted_output_summary_ref"),
            "redacted_output_summary_ref",
        ),
        "finish_status": finish_status,
        "usage_metadata": {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
        },
    }


def _reject_raw_sensitive_content(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            if isinstance(key, str) and key.strip().lower() in RAW_SENSITIVE_KEYS:
                raise V1ExecutableRealProviderExecutorInvocationError(
                    "raw sensitive content is not accepted"
                )
            _reject_raw_sensitive_content(nested)
    elif isinstance(value, (list, tuple, set, frozenset)):
        for nested in value:
            _reject_raw_sensitive_content(nested)
    elif isinstance(value, str):
        folded = value.strip().lower()
        if any(marker in folded for marker in RAW_SENSITIVE_VALUE_MARKERS):
            raise V1ExecutableRealProviderExecutorInvocationError(
                "raw sensitive content is not accepted"
            )


def _reject_forbidden_claims(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            if (
                isinstance(key, str)
                and key.strip().lower() in FORBIDDEN_TRUE_CLAIM_KEYS
                and nested is not False
            ):
                raise V1ExecutableRealProviderExecutorInvocationError(
                    "execution request cannot claim forbidden behavior"
                )
            _reject_forbidden_claims(nested)
    elif isinstance(value, (list, tuple, set, frozenset)):
        for nested in value:
            _reject_forbidden_claims(nested)


def _mapping(value: Any, field_name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping) or not value:
        raise V1ExecutableRealProviderExecutorInvocationError(
            f"{field_name} is required"
        )
    return value


def _required_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise V1ExecutableRealProviderExecutorInvocationError(
            f"{field_name} is required"
        )
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
        raise V1ExecutableRealProviderExecutorInvocationError(
            f"{field_name} must be a string sequence"
        )
    normalized = tuple(str(item).strip() for item in value if str(item).strip())
    if not normalized and not allow_empty:
        raise V1ExecutableRealProviderExecutorInvocationError(
            f"{field_name} is required"
        )
    return normalized


def _require_true_confirmation(value: Any, field_name: str) -> None:
    if value is True:
        return
    if isinstance(value, Mapping) and value.get("confirmed") is True:
        return
    raise V1ExecutableRealProviderExecutorInvocationError(
        f"{field_name} confirmation is required"
    )


def _nonnegative_int(value: Any, field_name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise V1ExecutableRealProviderExecutorInvocationError(
            f"{field_name} must be a non-negative integer"
        )
    return value


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
