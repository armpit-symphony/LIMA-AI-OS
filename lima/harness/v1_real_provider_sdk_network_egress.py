"""V1 bounded real provider SDK/network egress authority wrapper.

This module is the approved V1-G55 candidate runtime slice. It validates
V1-G48 credential/network hardening, V1-G50 invocation-envelope metadata,
V1-G51 caller-injected executor boundary metadata, V1-G53 SDK/network/
credential authority metadata, and V1-G54 fake SDK/fake-egress evidence before
calling a caller-injected provider SDK/network executor.

The wrapper contains no provider SDK clients, SDK dependencies, direct provider
SDK implementation, endpoint resolution, DNS/HTTP/socket/network clients,
ambient secret lookup, credential value access, fallback execution, connectors,
browser/device/robotics behavior, or consumer production integration.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
import hashlib
import json
from typing import Any, Final


SCHEMA_VERSION: Final[str] = "v1-g55-candidate"
G50_REQUEST_ENVELOPE_TYPE: Final[str] = (
    "real_provider_executor_invocation_request_metadata"
)
G50_RESPONSE_ENVELOPE_TYPE: Final[str] = (
    "real_provider_executor_invocation_response_metadata"
)
G55_APPROVAL_SCOPE: Final[str] = "v1-g55-real-provider-sdk-network-egress"
ALLOWED_FINISH_STATUSES: Final[frozenset[str]] = frozenset(
    {"completed", "blocked", "failed", "cancelled"}
)
REQUIRED_EXECUTION_FIELDS: Final[tuple[str, ...]] = (
    "egress_request_id",
    "invocation_request_envelope",
    "invocation_response_envelope",
    "provider_model_scope",
    "credential_network_hardening_linkage",
    "g50_execution_boundary_metadata",
    "g51_execution_boundary",
    "g53_provider_sdk_authority_metadata",
    "g53_endpoint_resolution_authority_metadata",
    "g53_provider_network_egress_authority_metadata",
    "g53_credential_reference_authority_metadata",
    "g53_authority_chain_linkage",
    "g54_fake_sdk_harness_evidence",
    "g54_fake_egress_harness_evidence",
    "g54_authority_chain_linkage",
    "provider_sdk_network_executor_ref",
    "provider_sdk_request_ref",
    "sanitized_input_ref",
    "sanitized_output_ref",
    "endpoint_policy_ref",
    "timeout_policy_ref",
    "cost_policy_ref",
    "denial_policy_ref",
    "g55_execution_approval_linkage",
    "g55_execution_boundary",
    "audit_evidence_linkage",
    "redaction_policy",
    "caller_injected_provider_sdk_network_executor_confirmation",
    "local_tests_use_fake_injected_executors_only_confirmation",
    "no_built_in_provider_sdk_client_confirmation",
    "no_sdk_dependency_confirmation",
    "no_direct_provider_sdk_implementation_confirmation",
    "no_lima_owned_endpoint_resolution_confirmation",
    "no_lima_owned_dns_http_socket_network_call_confirmation",
    "no_secret_lookup_confirmation",
    "no_credential_value_access_confirmation",
    "no_provider_token_or_api_key_access_confirmation",
    "no_provider_configuration_change_confirmation",
    "no_fallback_execution_confirmation",
    "no_consumer_production_runtime_integration_confirmation",
    "no_connector_browser_network_device_physical_world_confirmation",
    "no_raw_content_secret_credential_customer_data_diff_patch_confirmation",
    "no_product_readiness_confirmation",
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
        "ambient_environment_secret_lookup_allowed",
        "ambient_secret_lookup_performed",
        "browser_action_executed",
        "built_in_provider_sdk_added",
        "built_in_provider_sdk_client_added",
        "built_in_provider_sdk_client_allowed",
        "built_in_provider_sdk_client_used",
        "built_in_provider_sdk_used",
        "connector_browser_network_file_device_robotics_physical_world_behavior_added",
        "connector_invoked",
        "consumer_code_imported",
        "consumer_integration_added",
        "consumer_production_runtime_integration_added",
        "consumer_production_runtime_integration_allowed",
        "consumer_repo_mutation_added",
        "consumer_repo_mutation_allowed",
        "consumer_runtime_called",
        "consumer_runtime_calls_added",
        "credential_access_added",
        "credential_accessed",
        "credential_storage_rotation_migration_or_provisioning_added",
        "credential_storage_rotation_migration_or_provisioning_allowed",
        "credential_value_access_added",
        "credential_value_access_allowed",
        "credential_value_accessed",
        "device_command_invoked",
        "direct_network_client_added",
        "direct_network_code_added",
        "direct_network_code_used",
        "direct_provider_egress_added",
        "direct_provider_egress_allowed",
        "direct_provider_egress_performed",
        "direct_provider_egress_performed_by_lima",
        "direct_provider_sdk_added",
        "direct_provider_sdk_implementation_added",
        "direct_provider_sdk_implementation_allowed",
        "direct_provider_sdk_implementation_used",
        "direct_provider_sdk_used",
        "dns_lookup_added",
        "dns_lookup_allowed",
        "dns_lookup_performed",
        "drone_control_invoked",
        "endpoint_resolution_execution_allowed",
        "external_send_added",
        "fallback_allowed",
        "fallback_executed",
        "fallback_execution_added",
        "fallback_execution_allowed",
        "file_mutation_executed",
        "http_client_added",
        "http_client_allowed",
        "http_client_used",
        "humaninput_bridge_activated",
        "iot_control_invoked",
        "lima_owned_endpoint_resolution_performed",
        "model_request_dispatched",
        "network_action_executed",
        "network_call_performed",
        "network_call_performed_by_lima",
        "network_call_performed_by_lima_harness",
        "network_calls_allowed",
        "network_egress_execution_allowed",
        "physical_world_invoked",
        "product_readiness_claim_allowed",
        "product_ready",
        "production_ready",
        "provider_configuration_change_allowed",
        "provider_configuration_changed",
        "provider_configuration_changes_added",
        "provider_endpoint_resolution_added",
        "provider_endpoint_resolution_allowed",
        "provider_endpoint_resolution_performed",
        "provider_endpoint_selected",
        "provider_readiness_check_performed",
        "provider_readiness_network_check_added",
        "provider_readiness_network_check_allowed",
        "provider_sdk_client_allowed",
        "provider_sdk_client_constructed",
        "provider_sdk_client_used",
        "provider_token_or_api_key_access_added",
        "provider_token_or_api_key_access_allowed",
        "provider_token_or_api_key_accessed",
        "raw_customer_data_persisted",
        "raw_diff_or_patch_persisted",
        "raw_file_content_persisted",
        "raw_model_response_persisted",
        "raw_prompt_persisted",
        "raw_sensitive_content_persisted",
        "real_provider_sdk_client_added",
        "real_provider_sdk_client_used",
        "robot_control_invoked",
        "robotics_invoked",
        "scheduled_task_executed",
        "sdk_call_allowed",
        "sdk_call_performed",
        "sdk_client_construction_allowed",
        "sdk_dependency_added",
        "sdk_dependency_addition_allowed",
        "secret_lookup_added",
        "secret_lookup_allowed",
        "secret_lookup_performed",
        "shell_runtime_wired",
        "socket_client_added",
        "socket_client_allowed",
        "socket_client_used",
        "token_guardian_live_routing_added",
        "tool_executed",
        "tool_execution_added",
        "tool_execution_allowed",
    }
)


class V1RealProviderSdkNetworkEgressError(ValueError):
    """Raised when V1-G55 SDK/network egress authority is not satisfied."""


def execute_v1_real_provider_sdk_network_egress(
    egress_request: Mapping[str, Any],
    provider_sdk_network_executor: Callable[[Mapping[str, Any]], Mapping[str, Any]],
) -> dict[str, Any]:
    """Execute bounded SDK/network egress through a caller-injected executor.

    The wrapper validates authority-chain metadata and returns sanitized
    evidence. It does not construct SDK clients, resolve endpoints, open
    network connections, read secrets, access credential values, or perform
    fallback. The only execution hook is the caller-supplied callable.
    """

    if not isinstance(egress_request, Mapping):
        raise V1RealProviderSdkNetworkEgressError(
            "egress_request must be a mapping"
        )
    if not callable(provider_sdk_network_executor):
        raise V1RealProviderSdkNetworkEgressError(
            "provider_sdk_network_executor must be injected and callable"
        )

    _reject_raw_sensitive_content(egress_request)
    _reject_forbidden_claims(egress_request)

    for field_name in REQUIRED_EXECUTION_FIELDS:
        if field_name not in egress_request:
            raise V1RealProviderSdkNetworkEgressError(f"{field_name} is required")

    egress_request_id = _required_text(
        egress_request.get("egress_request_id"),
        "egress_request_id",
    )
    request_envelope = _validate_g50_request_envelope(
        egress_request.get("invocation_request_envelope")
    )
    response_envelope = _validate_g50_response_envelope(
        egress_request.get("invocation_response_envelope")
    )
    scope = _validate_provider_model_scope(egress_request.get("provider_model_scope"))
    hardening = _validate_credential_network_hardening_linkage(
        egress_request.get("credential_network_hardening_linkage")
    )
    g50_boundary = _validate_g50_execution_boundary_metadata(
        egress_request.get("g50_execution_boundary_metadata")
    )
    g51_boundary = _validate_g51_execution_boundary(
        egress_request.get("g51_execution_boundary")
    )
    sdk_authority = _validate_g53_provider_sdk_authority_metadata(
        egress_request.get("g53_provider_sdk_authority_metadata")
    )
    endpoint_authority = _validate_g53_endpoint_resolution_authority_metadata(
        egress_request.get("g53_endpoint_resolution_authority_metadata")
    )
    network_authority = _validate_g53_provider_network_egress_authority_metadata(
        egress_request.get("g53_provider_network_egress_authority_metadata")
    )
    credential_authority = _validate_g53_credential_reference_authority_metadata(
        egress_request.get("g53_credential_reference_authority_metadata")
    )
    g53_chain = _validate_g53_authority_chain_linkage(
        egress_request.get("g53_authority_chain_linkage")
    )
    fake_sdk = _validate_g54_fake_sdk_harness_evidence(
        egress_request.get("g54_fake_sdk_harness_evidence")
    )
    fake_egress = _validate_g54_fake_egress_harness_evidence(
        egress_request.get("g54_fake_egress_harness_evidence")
    )
    g54_chain = _validate_g54_authority_chain_linkage(
        egress_request.get("g54_authority_chain_linkage")
    )
    provider_sdk_network_executor_ref = _required_text(
        egress_request.get("provider_sdk_network_executor_ref"),
        "provider_sdk_network_executor_ref",
    )
    provider_sdk_request_ref = _required_text(
        egress_request.get("provider_sdk_request_ref"),
        "provider_sdk_request_ref",
    )
    sanitized_input_ref = _required_text(
        egress_request.get("sanitized_input_ref"),
        "sanitized_input_ref",
    )
    sanitized_output_ref = _required_text(
        egress_request.get("sanitized_output_ref"),
        "sanitized_output_ref",
    )
    endpoint_policy_ref = _required_text(
        egress_request.get("endpoint_policy_ref"),
        "endpoint_policy_ref",
    )
    timeout_policy_ref = _required_text(
        egress_request.get("timeout_policy_ref"),
        "timeout_policy_ref",
    )
    cost_policy_ref = _required_text(
        egress_request.get("cost_policy_ref"),
        "cost_policy_ref",
    )
    denial_policy_ref = _required_text(
        egress_request.get("denial_policy_ref"),
        "denial_policy_ref",
    )
    approval = _validate_g55_execution_approval_linkage(
        egress_request.get("g55_execution_approval_linkage")
    )
    boundary = _validate_g55_execution_boundary(
        egress_request.get("g55_execution_boundary")
    )
    audit = _validate_audit_linkage(egress_request.get("audit_evidence_linkage"))
    redaction = _validate_redaction_policy(egress_request.get("redaction_policy"))

    for field_name in (
        "caller_injected_provider_sdk_network_executor_confirmation",
        "local_tests_use_fake_injected_executors_only_confirmation",
        "no_built_in_provider_sdk_client_confirmation",
        "no_sdk_dependency_confirmation",
        "no_direct_provider_sdk_implementation_confirmation",
        "no_lima_owned_endpoint_resolution_confirmation",
        "no_lima_owned_dns_http_socket_network_call_confirmation",
        "no_secret_lookup_confirmation",
        "no_credential_value_access_confirmation",
        "no_provider_token_or_api_key_access_confirmation",
        "no_provider_configuration_change_confirmation",
        "no_fallback_execution_confirmation",
        "no_consumer_production_runtime_integration_confirmation",
        "no_connector_browser_network_device_physical_world_confirmation",
        "no_raw_content_secret_credential_customer_data_diff_patch_confirmation",
        "no_product_readiness_confirmation",
    ):
        _require_true_confirmation(egress_request.get(field_name), field_name)

    if hardening["credential_policy_ref"] != credential_authority["credential_policy_ref"]:
        raise V1RealProviderSdkNetworkEgressError(
            "credential policy refs must match G48/G53 authority metadata"
        )
    if hardening["network_policy_ref"] != network_authority["network_policy_ref"]:
        raise V1RealProviderSdkNetworkEgressError(
            "network policy refs must match G48/G53 authority metadata"
        )
    if g53_chain["credential_policy_ref"] != hardening["credential_policy_ref"]:
        raise V1RealProviderSdkNetworkEgressError(
            "G53 authority chain must link the G48 credential policy"
        )
    if g54_chain["provider_sdk_authority_ref"] != sdk_authority["provider_sdk_authority_id"]:
        raise V1RealProviderSdkNetworkEgressError(
            "G54 chain must link the G53 provider SDK authority"
        )

    executor_payload = {
        "egress_request_id": egress_request_id,
        "invocation_request_id": request_envelope["invocation_request_id"],
        "invocation_response_id": response_envelope["invocation_response_id"],
        "provider_scope_ref": scope["provider_scope_ref"],
        "model_scope_ref": scope["model_scope_ref"],
        "credential_policy_ref": hardening["credential_policy_ref"],
        "network_policy_ref": hardening["network_policy_ref"],
        "provider_sdk_authority_ref": sdk_authority["provider_sdk_authority_id"],
        "endpoint_resolution_authority_ref": endpoint_authority[
            "endpoint_resolution_authority_id"
        ],
        "provider_network_egress_authority_ref": network_authority[
            "network_egress_authority_id"
        ],
        "credential_reference_authority_ref": credential_authority[
            "credential_authority_id"
        ],
        "fake_sdk_harness_ref": fake_sdk["harness_id"],
        "fake_egress_harness_ref": fake_egress["harness_id"],
        "g51_execution_boundary_ref": g51_boundary["provider_executor_boundary_ref"],
        "g55_execution_boundary_ref": boundary["provider_sdk_network_egress_boundary_ref"],
        "provider_sdk_network_executor_ref": provider_sdk_network_executor_ref,
        "provider_sdk_request_ref": provider_sdk_request_ref,
        "sanitized_input_ref": sanitized_input_ref,
        "sanitized_output_ref": sanitized_output_ref,
        "redacted_input_ref": request_envelope["redacted_input_ref"],
        "redacted_output_ref": response_envelope["redacted_output_ref"],
        "redaction_policy_ref": redaction["redaction_policy_ref"],
        "audit_record_ref": audit["audit_record_ref"],
        "endpoint_policy_ref": endpoint_policy_ref,
        "timeout_policy_ref": timeout_policy_ref,
        "g50_timeout_policy_ref": g50_boundary["timeout_policy_ref"],
        "cost_policy_ref": cost_policy_ref,
        "g50_cost_policy_ref": g50_boundary["cost_policy_ref"],
        "denial_policy_ref": denial_policy_ref,
        "failure_policy_ref": g50_boundary["failure_policy_ref"],
        "max_attempts": boundary["max_attempts"],
    }

    try:
        provider_result = provider_sdk_network_executor(executor_payload)
    except Exception as exc:  # pragma: no cover - caller-owned exception details.
        raise V1RealProviderSdkNetworkEgressError(
            "provider SDK/network executor failed"
        ) from exc

    result = _validate_provider_sdk_network_result(provider_result)

    record = {
        "record_type": "v1_real_provider_sdk_network_egress",
        "schema_version": SCHEMA_VERSION,
        "egress_request_id": egress_request_id,
        "invocation_request_id": request_envelope["invocation_request_id"],
        "invocation_response_id": response_envelope["invocation_response_id"],
        "provider_scope_ref": scope["provider_scope_ref"],
        "model_scope_ref": scope["model_scope_ref"],
        "credential_policy_ref": hardening["credential_policy_ref"],
        "network_policy_ref": hardening["network_policy_ref"],
        "provider_sdk_authority_ref": sdk_authority["provider_sdk_authority_id"],
        "endpoint_resolution_authority_ref": endpoint_authority[
            "endpoint_resolution_authority_id"
        ],
        "provider_network_egress_authority_ref": network_authority[
            "network_egress_authority_id"
        ],
        "credential_reference_authority_ref": credential_authority[
            "credential_authority_id"
        ],
        "fake_sdk_harness_ref": fake_sdk["harness_id"],
        "fake_egress_harness_ref": fake_egress["harness_id"],
        "provider_sdk_network_executor_ref": provider_sdk_network_executor_ref,
        "provider_sdk_request_ref": provider_sdk_request_ref,
        "provider_sdk_call_ref": result["provider_sdk_call_ref"],
        "provider_sdk_response_ref": result["provider_sdk_response_ref"],
        "provider_network_egress_record_ref": result[
            "provider_network_egress_record_ref"
        ],
        "redacted_output_ref": result["redacted_output_ref"],
        "redacted_output_summary_ref": result["redacted_output_summary_ref"],
        "finish_status": result["finish_status"],
        "usage_metadata": result["usage_metadata"],
        "g55_execution_approval_linkage": approval,
        "g55_execution_boundary": boundary,
        "g51_execution_boundary": g51_boundary,
        "g53_authority_chain_linkage": g53_chain,
        "g54_authority_chain_linkage": g54_chain,
        "audit_evidence_linkage": audit,
        "redaction_policy": redaction,
        "capability_open": True,
        "authority_gated": True,
        "candidate_only": True,
        "real_provider_sdk_network_egress_authority_wrapper_added": True,
        "provider_sdk_network_egress_invocation_added": True,
        "provider_sdk_network_executor_invoked": True,
        "caller_injected_provider_sdk_network_executor_only": True,
        "local_tests_use_fake_injected_executors_only": True,
        "provider_sdk_network_egress_invoked_through_injected_executor": True,
        "built_in_provider_sdk_client_added": False,
        "built_in_provider_sdk_client_used": False,
        "real_provider_sdk_client_added_by_lima": False,
        "sdk_dependency_added": False,
        "direct_provider_sdk_implementation_added": False,
        "direct_provider_sdk_implementation_used": False,
        "provider_endpoint_resolution_added_by_lima": False,
        "provider_endpoint_resolution_performed_by_lima": False,
        "direct_network_code_added_by_lima": False,
        "dns_lookup_performed_by_lima": False,
        "http_client_used_by_lima": False,
        "socket_client_used_by_lima": False,
        "network_call_performed_by_lima_harness": False,
        "direct_provider_egress_performed_by_lima": False,
        "provider_readiness_network_check_added": False,
        "ambient_environment_secret_lookup_added": False,
        "secret_lookup_added": False,
        "secret_lookup_performed": False,
        "credential_reference_metadata_only": True,
        "credential_value_access_added": False,
        "credential_value_accessed": False,
        "provider_token_or_api_key_access_added": False,
        "provider_token_or_api_key_accessed": False,
        "credential_storage_rotation_migration_or_provisioning_added": False,
        "provider_configuration_changes_added": False,
        "fallback_execution_added": False,
        "fallback_executed": False,
        "consumer_repo_mutation_added": False,
        "consumer_runtime_calls_added": False,
        "consumer_production_runtime_integration_added": False,
        "connector_browser_network_file_device_robotics_physical_world_behavior_added": False,
        "scheduled_task_execution_added": False,
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
        "production_ready": False,
        "metadata": {
            "v1_runtime_slice": "real_provider_sdk_network_egress",
            "sanitized_evidence_only": True,
            "provider_sdk_network_executor_injected": True,
            "no_built_in_provider_sdk_client": True,
            "no_lima_owned_network_code": True,
            "no_lima_owned_secret_lookup": True,
        },
    }
    _reject_raw_sensitive_content(record)
    record["record_hash"] = _record_hash(record)
    return record


def _validate_g50_request_envelope(value: Any) -> dict[str, str]:
    envelope = _mapping(value, "invocation_request_envelope")
    if envelope.get("envelope_type") != G50_REQUEST_ENVELOPE_TYPE:
        raise V1RealProviderSdkNetworkEgressError(
            "V1-G50 invocation request envelope is required"
        )
    if envelope.get("metadata_only") is not True:
        raise V1RealProviderSdkNetworkEgressError(
            "V1-G50 request envelope must be metadata-only"
        )
    if envelope.get("non_executing") is not True:
        raise V1RealProviderSdkNetworkEgressError(
            "V1-G50 request envelope must be non-executing metadata"
        )
    if envelope.get("proof_not_execution") is not True:
        raise V1RealProviderSdkNetworkEgressError(
            "V1-G50 request envelope proof metadata is required"
        )
    if envelope.get("guardian_gate_required") is not True:
        raise V1RealProviderSdkNetworkEgressError(
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
            raise V1RealProviderSdkNetworkEgressError(
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
        raise V1RealProviderSdkNetworkEgressError(
            "V1-G50 invocation response envelope is required"
        )
    if envelope.get("metadata_only") is not True:
        raise V1RealProviderSdkNetworkEgressError(
            "V1-G50 response envelope must be metadata-only"
        )
    if envelope.get("non_executing") is not True:
        raise V1RealProviderSdkNetworkEgressError(
            "V1-G50 response envelope must be non-executing metadata"
        )
    if envelope.get("proof_not_execution") is not True:
        raise V1RealProviderSdkNetworkEgressError(
            "V1-G50 response envelope proof metadata is required"
        )
    if envelope.get("invocation_status") != "not_invoked":
        raise V1RealProviderSdkNetworkEgressError(
            "V1-G50 response envelope must remain not_invoked"
        )
    if envelope.get("sanitized_evidence_only") is not True:
        raise V1RealProviderSdkNetworkEgressError(
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
            raise V1RealProviderSdkNetworkEgressError(
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
        raise V1RealProviderSdkNetworkEgressError(
            "provider/model scope must be reference-only"
        )
    if scope.get("metadata_only") is not True:
        raise V1RealProviderSdkNetworkEgressError(
            "provider/model scope must be metadata-only"
        )
    for field_name in (
        "provider_configuration_changed",
        "provider_endpoint_selected",
        "model_invocation_selected",
        "executable_invocation_selected",
    ):
        if scope.get(field_name) is not False:
            raise V1RealProviderSdkNetworkEgressError(f"{field_name} is not allowed")
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


def _validate_credential_network_hardening_linkage(value: Any) -> dict[str, str]:
    hardening = _mapping(value, "credential_network_hardening_linkage")
    if hardening.get("credential_reference_only") is not True:
        raise V1RealProviderSdkNetworkEgressError(
            "credential policy must be reference-only"
        )
    if hardening.get("network_policy_reference_only") is not True:
        raise V1RealProviderSdkNetworkEgressError(
            "network policy must be reference-only"
        )
    if hardening.get("deny_by_default_network_required") is not True:
        raise V1RealProviderSdkNetworkEgressError(
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
            raise V1RealProviderSdkNetworkEgressError(f"{field_name} is not allowed")
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
        raise V1RealProviderSdkNetworkEgressError(
            "V1-G50 cost policy must remain estimate-only"
        )
    if boundary.get("metadata_only") is not True:
        raise V1RealProviderSdkNetworkEgressError(
            "V1-G50 execution boundary must be metadata-only"
        )
    if boundary.get("non_executing") is not True:
        raise V1RealProviderSdkNetworkEgressError(
            "V1-G50 execution boundary must be non-executing"
        )
    if boundary.get("max_attempts_metadata") != 1:
        raise V1RealProviderSdkNetworkEgressError(
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
            raise V1RealProviderSdkNetworkEgressError(
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


def _validate_g51_execution_boundary(value: Any) -> dict[str, Any]:
    boundary = _mapping(value, "g51_execution_boundary")
    boundary_ref = _required_text(
        boundary.get("provider_executor_boundary_ref"),
        "g51_execution_boundary.provider_executor_boundary_ref",
    )
    if boundary.get("caller_injected_provider_executor") is not True:
        raise V1RealProviderSdkNetworkEgressError(
            "caller-injected provider executor boundary is required"
        )
    if boundary.get("provider_executor_call_allowed") is not True:
        raise V1RealProviderSdkNetworkEgressError(
            "G51 provider executor call authority is required"
        )
    if boundary.get("max_attempts") != 1:
        raise V1RealProviderSdkNetworkEgressError("G51 max_attempts must be one")
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
            raise V1RealProviderSdkNetworkEgressError(
                "G51 execution boundary allows forbidden behavior"
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


def _validate_g53_provider_sdk_authority_metadata(value: Any) -> dict[str, str]:
    metadata = _mapping(value, "g53_provider_sdk_authority_metadata")
    if metadata.get("metadata_only") is not True:
        raise V1RealProviderSdkNetworkEgressError(
            "G53 provider SDK authority must be metadata-only"
        )
    if metadata.get("proof_not_execution") is not True:
        raise V1RealProviderSdkNetworkEgressError(
            "G53 provider SDK authority proof metadata is required"
        )
    for field_name in (
        "built_in_provider_sdk_client_allowed",
        "direct_provider_sdk_implementation_allowed",
        "sdk_dependency_addition_allowed",
        "sdk_client_construction_allowed",
        "credential_value_access_allowed",
        "provider_token_or_api_key_access_allowed",
        "fallback_execution_allowed",
        "product_readiness_claim_allowed",
    ):
        if metadata.get(field_name) is not False:
            raise V1RealProviderSdkNetworkEgressError(
                f"{field_name} must remain blocked in G53 metadata"
            )
    return {
        "provider_sdk_authority_id": _required_text(
            metadata.get("provider_sdk_authority_id"),
            "provider_sdk_authority_id",
        )
    }


def _validate_g53_endpoint_resolution_authority_metadata(value: Any) -> dict[str, str]:
    metadata = _mapping(value, "g53_endpoint_resolution_authority_metadata")
    if metadata.get("metadata_only") is not True or metadata.get("reference_only") is not True:
        raise V1RealProviderSdkNetworkEgressError(
            "G53 endpoint authority must be metadata-only and reference-only"
        )
    for field_name in (
        "provider_endpoint_resolution_allowed",
        "provider_endpoint_resolution_performed",
        "endpoint_resolution_execution_allowed",
        "provider_endpoint_selected",
        "provider_configuration_changed",
        "dns_lookup_allowed",
        "http_client_allowed",
        "socket_client_allowed",
        "network_calls_allowed",
        "direct_provider_egress_allowed",
        "provider_readiness_network_check_allowed",
    ):
        if metadata.get(field_name) is not False:
            raise V1RealProviderSdkNetworkEgressError(
                f"{field_name} must remain blocked in G53 metadata"
            )
    return {
        "endpoint_resolution_authority_id": _required_text(
            metadata.get("endpoint_resolution_authority_id"),
            "endpoint_resolution_authority_id",
        )
    }


def _validate_g53_provider_network_egress_authority_metadata(
    value: Any,
) -> dict[str, str]:
    metadata = _mapping(value, "g53_provider_network_egress_authority_metadata")
    if metadata.get("metadata_only") is not True or metadata.get("reference_only") is not True:
        raise V1RealProviderSdkNetworkEgressError(
            "G53 network authority must be metadata-only and reference-only"
        )
    if metadata.get("network_scope_bound") is not True:
        raise V1RealProviderSdkNetworkEgressError("G53 network scope must be bound")
    if metadata.get("deny_by_default") is not True:
        raise V1RealProviderSdkNetworkEgressError(
            "G53 network authority must be deny-by-default"
        )
    for field_name in (
        "network_calls_allowed",
        "network_call_performed",
        "direct_provider_egress_allowed",
        "provider_endpoint_resolution_allowed",
        "dns_lookup_allowed",
        "http_client_allowed",
        "socket_client_allowed",
        "provider_readiness_network_check_allowed",
    ):
        if metadata.get(field_name) is not False:
            raise V1RealProviderSdkNetworkEgressError(
                f"{field_name} must remain blocked in G53 metadata"
            )
    return {
        "network_egress_authority_id": _required_text(
            metadata.get("network_egress_authority_id"),
            "network_egress_authority_id",
        ),
        "network_policy_ref": _required_text(
            metadata.get("network_policy_ref"),
            "network_policy_ref",
        ),
    }


def _validate_g53_credential_reference_authority_metadata(
    value: Any,
) -> dict[str, str]:
    metadata = _mapping(value, "g53_credential_reference_authority_metadata")
    if metadata.get("metadata_only") is not True or metadata.get("reference_only") is not True:
        raise V1RealProviderSdkNetworkEgressError(
            "G53 credential authority must be metadata-only and reference-only"
        )
    if metadata.get("credential_reference_only") is not True:
        raise V1RealProviderSdkNetworkEgressError(
            "G53 credential authority must remain reference-only"
        )
    for field_name in (
        "secret_lookup_allowed",
        "secret_lookup_performed",
        "ambient_environment_secret_lookup_allowed",
        "credential_value_access_allowed",
        "credential_value_accessed",
        "provider_token_or_api_key_access_allowed",
        "provider_token_or_api_key_accessed",
        "credential_storage_rotation_migration_or_provisioning_allowed",
        "raw_secret_present",
        "credential_value_present",
        "provider_token_present",
        "api_key_present",
    ):
        if metadata.get(field_name) is not False:
            raise V1RealProviderSdkNetworkEgressError(
                f"{field_name} must remain blocked in G53 metadata"
            )
    return {
        "credential_authority_id": _required_text(
            metadata.get("credential_authority_id"),
            "credential_authority_id",
        ),
        "credential_policy_ref": _required_text(
            metadata.get("credential_policy_ref"),
            "credential_policy_ref",
        ),
    }


def _validate_g53_authority_chain_linkage(value: Any) -> dict[str, str]:
    chain = _mapping(value, "g53_authority_chain_linkage")
    if chain.get("authority_records_metadata_only") is not True:
        raise V1RealProviderSdkNetworkEgressError(
            "G53 authority chain must be metadata-only"
        )
    if chain.get("guardian_gate_required") is not True:
        raise V1RealProviderSdkNetworkEgressError("Guardian gate is required")
    if chain.get("credential_reference_only") is not True:
        raise V1RealProviderSdkNetworkEgressError(
            "G53 credential linkage must be reference-only"
        )
    if chain.get("network_policy_reference_only") is not True:
        raise V1RealProviderSdkNetworkEgressError(
            "G53 network linkage must be reference-only"
        )
    if chain.get("deny_by_default_network_required") is not True:
        raise V1RealProviderSdkNetworkEgressError(
            "G53 chain must require deny-by-default network policy"
        )
    for field_name in (
        "provider_sdk_client_allowed",
        "endpoint_resolution_execution_allowed",
        "network_egress_execution_allowed",
        "secret_lookup_allowed",
        "credential_value_access_allowed",
        "provider_token_or_api_key_access_allowed",
        "fallback_execution_allowed",
        "consumer_production_runtime_integration_allowed",
    ):
        if chain.get(field_name) is not False:
            raise V1RealProviderSdkNetworkEgressError(
                f"{field_name} must remain blocked in G53 chain"
            )
    return {
        "credential_policy_ref": _required_text(
            chain.get("credential_policy_ref"),
            "credential_policy_ref",
        ),
        "network_policy_ref": _required_text(
            chain.get("network_policy_ref"),
            "network_policy_ref",
        ),
        "invocation_request_ref": _required_text(
            chain.get("invocation_request_ref"),
            "invocation_request_ref",
        ),
        "execution_wrapper_boundary_ref": _required_text(
            chain.get("execution_wrapper_boundary_ref"),
            "execution_wrapper_boundary_ref",
        ),
    }


def _validate_g54_fake_sdk_harness_evidence(value: Any) -> dict[str, str]:
    evidence = _mapping(value, "g54_fake_sdk_harness_evidence")
    for field_name in (
        "test_only",
        "test_module_local_only",
        "in_process_only",
        "deterministic",
        "sanitized_evidence_only",
    ):
        if evidence.get(field_name) is not True:
            raise V1RealProviderSdkNetworkEgressError(
                f"G54 fake SDK evidence requires {field_name}"
            )
    for field_name in (
        "real_sdk_client_used",
        "built_in_provider_sdk_client_used",
        "direct_provider_sdk_implementation_used",
        "sdk_dependency_added",
        "sdk_client_constructed",
        "sdk_call_performed",
        "provider_endpoint_resolution_performed",
        "network_calls_allowed",
        "network_call_performed",
        "credential_value_access_allowed",
        "provider_token_or_api_key_access_allowed",
        "fallback_execution_allowed",
        "consumer_production_runtime_integration_allowed",
        "product_readiness_claim_allowed",
    ):
        if evidence.get(field_name) is not False:
            raise V1RealProviderSdkNetworkEgressError(
                f"{field_name} must remain blocked in G54 fake SDK evidence"
            )
    return {
        "harness_id": _required_text(evidence.get("harness_id"), "harness_id")
    }


def _validate_g54_fake_egress_harness_evidence(value: Any) -> dict[str, str]:
    evidence = _mapping(value, "g54_fake_egress_harness_evidence")
    for field_name in (
        "test_only",
        "test_module_local_only",
        "in_process_only",
        "deterministic",
        "sanitized_evidence_only",
        "deny_by_default",
        "network_simulation_only",
    ):
        if evidence.get(field_name) is not True:
            raise V1RealProviderSdkNetworkEgressError(
                f"G54 fake egress evidence requires {field_name}"
            )
    for field_name in (
        "endpoint_resolution_execution_allowed",
        "provider_endpoint_resolution_performed",
        "dns_lookup_allowed",
        "dns_lookup_performed",
        "http_client_allowed",
        "http_client_used",
        "socket_client_allowed",
        "socket_client_used",
        "network_calls_allowed",
        "network_call_performed",
        "direct_provider_egress_allowed",
        "direct_provider_egress_performed",
        "provider_readiness_network_check_allowed",
        "provider_configuration_change_allowed",
        "fallback_execution_allowed",
        "consumer_production_runtime_integration_allowed",
        "product_readiness_claim_allowed",
    ):
        if evidence.get(field_name) is not False:
            raise V1RealProviderSdkNetworkEgressError(
                f"{field_name} must remain blocked in G54 fake egress evidence"
            )
    return {
        "harness_id": _required_text(evidence.get("harness_id"), "harness_id")
    }


def _validate_g54_authority_chain_linkage(value: Any) -> dict[str, str]:
    chain = _mapping(value, "g54_authority_chain_linkage")
    if chain.get("authority_records_metadata_only") is not True:
        raise V1RealProviderSdkNetworkEgressError(
            "G54 authority chain must be metadata-only"
        )
    if chain.get("guardian_gate_required") is not True:
        raise V1RealProviderSdkNetworkEgressError("G54 Guardian gate is required")
    if chain.get("test_module_local_fake_harness_only") is not True:
        raise V1RealProviderSdkNetworkEgressError(
            "G54 fake harness linkage must remain test-module-local"
        )
    for field_name in (
        "provider_sdk_client_allowed",
        "sdk_dependency_allowed",
        "direct_provider_sdk_implementation_allowed",
        "endpoint_resolution_execution_allowed",
        "network_egress_execution_allowed",
        "secret_lookup_allowed",
        "credential_value_access_allowed",
        "provider_token_or_api_key_access_allowed",
        "provider_configuration_change_allowed",
        "fallback_execution_allowed",
        "consumer_production_runtime_integration_allowed",
        "connector_browser_network_physical_world_allowed",
        "product_readiness_claim_allowed",
    ):
        if chain.get(field_name) is not False:
            raise V1RealProviderSdkNetworkEgressError(
                f"{field_name} must remain blocked in G54 chain"
            )
    return {
        "provider_sdk_authority_ref": _required_text(
            chain.get("provider_sdk_authority_ref"),
            "provider_sdk_authority_ref",
        ),
        "endpoint_resolution_authority_ref": _required_text(
            chain.get("endpoint_resolution_authority_ref"),
            "endpoint_resolution_authority_ref",
        ),
        "provider_network_egress_authority_ref": _required_text(
            chain.get("provider_network_egress_authority_ref"),
            "provider_network_egress_authority_ref",
        ),
        "credential_reference_authority_ref": _required_text(
            chain.get("credential_reference_authority_ref"),
            "credential_reference_authority_ref",
        ),
        "fake_sdk_harness_ref": _required_text(
            chain.get("fake_sdk_harness_ref"),
            "fake_sdk_harness_ref",
        ),
        "fake_egress_harness_ref": _required_text(
            chain.get("fake_egress_harness_ref"),
            "fake_egress_harness_ref",
        ),
    }


def _validate_g55_execution_approval_linkage(value: Any) -> dict[str, Any]:
    approval = _mapping(value, "g55_execution_approval_linkage")
    approval_evidence_ref = _required_text(
        approval.get("approval_evidence_ref"),
        "g55_execution_approval_linkage.approval_evidence_ref",
    )
    if approval.get("approval_evidence_current") is not True:
        raise V1RealProviderSdkNetworkEgressError(
            "G55 approval evidence must be current"
        )
    if approval.get("approval_scope") != G55_APPROVAL_SCOPE:
        raise V1RealProviderSdkNetworkEgressError(
            "V1-G55 execution approval scope is required"
        )
    if (
        approval.get("grants_bounded_real_provider_sdk_network_egress_authority")
        is not True
    ):
        raise V1RealProviderSdkNetworkEgressError(
            "bounded real provider SDK/network egress authority is required"
        )
    if approval.get("proof_of_operator_approval") is not True:
        raise V1RealProviderSdkNetworkEgressError(
            "operator approval proof is required"
        )
    return {
        "approval_evidence_ref": approval_evidence_ref,
        "approval_evidence_current": True,
        "approval_scope": G55_APPROVAL_SCOPE,
        "grants_bounded_real_provider_sdk_network_egress_authority": True,
        "proof_of_operator_approval": True,
    }


def _validate_g55_execution_boundary(value: Any) -> dict[str, Any]:
    boundary = _mapping(value, "g55_execution_boundary")
    boundary_ref = _required_text(
        boundary.get("provider_sdk_network_egress_boundary_ref"),
        "g55_execution_boundary.provider_sdk_network_egress_boundary_ref",
    )
    if boundary.get("caller_injected_provider_sdk_network_executor") is not True:
        raise V1RealProviderSdkNetworkEgressError(
            "caller-injected provider SDK/network executor is required"
        )
    if boundary.get("provider_sdk_network_executor_call_allowed") is not True:
        raise V1RealProviderSdkNetworkEgressError(
            "G55 injected executor call authority is required"
        )
    if boundary.get("max_attempts") != 1:
        raise V1RealProviderSdkNetworkEgressError("G55 max_attempts must be one")
    for field_name in (
        "built_in_provider_sdk_client_used",
        "lima_owned_provider_sdk_client_used",
        "direct_provider_sdk_implementation_used",
        "sdk_dependency_used",
        "lima_owned_endpoint_resolution_performed",
        "dns_lookup_performed_by_lima",
        "http_client_used_by_lima",
        "socket_client_used_by_lima",
        "network_call_performed_by_lima_harness",
        "direct_provider_egress_performed_by_lima",
        "secret_lookup_performed",
        "credential_value_accessed",
        "provider_token_or_api_key_accessed",
        "provider_configuration_changed",
        "fallback_allowed",
        "consumer_production_runtime_integration_allowed",
        "connector_browser_network_file_device_robotics_physical_world_behavior_allowed",
    ):
        if boundary.get(field_name) is not False:
            raise V1RealProviderSdkNetworkEgressError(
                "G55 execution boundary allows forbidden behavior"
            )
    return {
        "provider_sdk_network_egress_boundary_ref": boundary_ref,
        "caller_injected_provider_sdk_network_executor": True,
        "provider_sdk_network_executor_call_allowed": True,
        "max_attempts": 1,
        "built_in_provider_sdk_client_used": False,
        "lima_owned_provider_sdk_client_used": False,
        "direct_provider_sdk_implementation_used": False,
        "sdk_dependency_used": False,
        "lima_owned_endpoint_resolution_performed": False,
        "dns_lookup_performed_by_lima": False,
        "http_client_used_by_lima": False,
        "socket_client_used_by_lima": False,
        "network_call_performed_by_lima_harness": False,
        "direct_provider_egress_performed_by_lima": False,
        "secret_lookup_performed": False,
        "credential_value_accessed": False,
        "provider_token_or_api_key_accessed": False,
        "provider_configuration_changed": False,
        "fallback_allowed": False,
        "consumer_production_runtime_integration_allowed": False,
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
        raise V1RealProviderSdkNetworkEgressError("audit linkage is required")
    if audit.get("sanitized_evidence_only") is not True:
        raise V1RealProviderSdkNetworkEgressError(
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
        raise V1RealProviderSdkNetworkEgressError("redacted input is required")
    if policy.get("redacted_output_required") is not True:
        raise V1RealProviderSdkNetworkEgressError("redacted output is required")
    for field_name in (
        "raw_prompt_persistence_allowed",
        "raw_model_response_persistence_allowed",
        "raw_customer_data_persistence_allowed",
        "raw_secret_credential_persistence_allowed",
        "raw_provider_token_api_key_persistence_allowed",
        "raw_diff_patch_file_content_persistence_allowed",
    ):
        if policy.get(field_name) is not False:
            raise V1RealProviderSdkNetworkEgressError(
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
        "raw_provider_token_api_key_persistence_allowed": False,
        "raw_diff_patch_file_content_persistence_allowed": False,
    }


def _validate_provider_sdk_network_result(value: Any) -> dict[str, Any]:
    result = _mapping(value, "provider_sdk_network_result")
    _reject_raw_sensitive_content(result)
    _reject_forbidden_claims(result)

    finish_status = _normalize_token(
        _required_text(result.get("finish_status"), "finish_status")
    )
    if finish_status not in ALLOWED_FINISH_STATUSES:
        raise V1RealProviderSdkNetworkEgressError("finish_status is not allowed")

    usage = _mapping(result.get("usage_metadata"), "usage_metadata")
    input_tokens = _nonnegative_int(usage.get("input_tokens"), "input_tokens")
    output_tokens = _nonnegative_int(usage.get("output_tokens"), "output_tokens")
    total_tokens = _nonnegative_int(usage.get("total_tokens"), "total_tokens")
    if total_tokens < input_tokens + output_tokens:
        raise V1RealProviderSdkNetworkEgressError("total_tokens is inconsistent")

    for field_name in (
        "network_call_performed_by_lima_harness",
        "direct_provider_egress_performed_by_lima",
        "secret_lookup_performed",
        "credential_value_accessed",
        "provider_token_or_api_key_accessed",
    ):
        if result.get(field_name, False) is not False:
            raise V1RealProviderSdkNetworkEgressError(
                "provider SDK/network result claims forbidden LIMA behavior"
            )

    return {
        "provider_sdk_call_ref": _required_text(
            result.get("provider_sdk_call_ref"),
            "provider_sdk_call_ref",
        ),
        "provider_sdk_response_ref": _required_text(
            result.get("provider_sdk_response_ref"),
            "provider_sdk_response_ref",
        ),
        "provider_network_egress_record_ref": _required_text(
            result.get("provider_network_egress_record_ref"),
            "provider_network_egress_record_ref",
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
                raise V1RealProviderSdkNetworkEgressError(
                    "raw sensitive content is not accepted"
                )
            _reject_raw_sensitive_content(nested)
    elif isinstance(value, (list, tuple, set, frozenset)):
        for nested in value:
            _reject_raw_sensitive_content(nested)
    elif isinstance(value, str):
        folded = value.strip().lower()
        if any(marker in folded for marker in RAW_SENSITIVE_VALUE_MARKERS):
            raise V1RealProviderSdkNetworkEgressError(
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
                raise V1RealProviderSdkNetworkEgressError(
                    "execution request cannot claim forbidden behavior"
                )
            _reject_forbidden_claims(nested)
    elif isinstance(value, (list, tuple, set, frozenset)):
        for nested in value:
            _reject_forbidden_claims(nested)


def _mapping(value: Any, field_name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping) or not value:
        raise V1RealProviderSdkNetworkEgressError(f"{field_name} is required")
    return value


def _required_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise V1RealProviderSdkNetworkEgressError(f"{field_name} is required")
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
        raise V1RealProviderSdkNetworkEgressError(
            f"{field_name} must be a string sequence"
        )
    normalized = tuple(str(item).strip() for item in value if str(item).strip())
    if not normalized and not allow_empty:
        raise V1RealProviderSdkNetworkEgressError(f"{field_name} is required")
    return normalized


def _require_true_confirmation(value: Any, field_name: str) -> None:
    if value is True:
        return
    if isinstance(value, Mapping) and value.get("confirmed") is True:
        return
    raise V1RealProviderSdkNetworkEgressError(
        f"{field_name} confirmation is required"
    )


def _nonnegative_int(value: Any, field_name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise V1RealProviderSdkNetworkEgressError(
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
