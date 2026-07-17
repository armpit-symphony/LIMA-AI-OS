"""Tests for the approved V1-G55 real provider SDK/network egress wrapper."""

from __future__ import annotations

import copy
import importlib
import json
from pathlib import Path
from typing import Any

import pytest

from lima.harness import (
    V1RealProviderSdkNetworkEgressError,
    execute_v1_real_provider_sdk_network_egress,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g55_real_provider_sdk_network_egress.json"
)
G22_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g22_final_public_api_freeze.json"
)
G50_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g50_real_provider_executor_invocation.json"
)
G51_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g51_executable_real_provider_executor_invocation.json"
)
G53_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g53_provider_sdk_network_credential_authority.json"
)
G54_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g54_fake_sdk_egress_harness.json"
)
RUNTIME_MODULE_PATH = (
    REPO_ROOT / "lima" / "harness" / "v1_real_provider_sdk_network_egress.py"
)


def _load_json(path: Path) -> dict[str, Any]:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _load_fixture() -> dict[str, Any]:
    return _load_json(FIXTURE_PATH)


def _egress_request(**overrides: Any) -> dict[str, Any]:
    fixture = _load_fixture()
    g50 = _load_json(G50_FIXTURE_PATH)
    g51 = _load_json(G51_FIXTURE_PATH)
    g53 = _load_json(G53_FIXTURE_PATH)
    g54 = _load_json(G54_FIXTURE_PATH)
    refs = fixture["egress_request_policy_refs"]
    request = {
        "egress_request_id": "egress-request:v1-g55:001",
        "invocation_request_envelope": copy.deepcopy(
            g50["invocation_request_envelope"]
        ),
        "invocation_response_envelope": copy.deepcopy(
            g50["invocation_response_envelope"]
        ),
        "provider_model_scope": copy.deepcopy(g50["provider_model_scope"]),
        "credential_network_hardening_linkage": copy.deepcopy(
            g50["credential_network_hardening_linkage"]
        ),
        "g50_execution_boundary_metadata": copy.deepcopy(
            g50["execution_boundary_metadata"]
        ),
        "g51_execution_boundary": copy.deepcopy(g51["execution_boundary"]),
        "g53_provider_sdk_authority_metadata": copy.deepcopy(
            g53["provider_sdk_authority_metadata"]
        ),
        "g53_endpoint_resolution_authority_metadata": copy.deepcopy(
            g53["endpoint_resolution_authority_metadata"]
        ),
        "g53_provider_network_egress_authority_metadata": copy.deepcopy(
            g53["provider_network_egress_authority_metadata"]
        ),
        "g53_credential_reference_authority_metadata": copy.deepcopy(
            g53["credential_reference_authority_metadata"]
        ),
        "g53_authority_chain_linkage": copy.deepcopy(g53["authority_chain_linkage"]),
        "g54_fake_sdk_harness_evidence": copy.deepcopy(
            g54["fake_sdk_harness_evidence"]
        ),
        "g54_fake_egress_harness_evidence": copy.deepcopy(
            g54["fake_egress_harness_evidence"]
        ),
        "g54_authority_chain_linkage": copy.deepcopy(g54["authority_chain_linkage"]),
        "provider_sdk_network_executor_ref": refs[
            "provider_sdk_network_executor_ref"
        ],
        "provider_sdk_request_ref": refs["provider_sdk_request_ref"],
        "sanitized_input_ref": refs["sanitized_input_ref"],
        "sanitized_output_ref": refs["sanitized_output_ref"],
        "endpoint_policy_ref": refs["endpoint_policy_ref"],
        "timeout_policy_ref": refs["timeout_policy_ref"],
        "cost_policy_ref": refs["cost_policy_ref"],
        "denial_policy_ref": refs["denial_policy_ref"],
        "g55_execution_approval_linkage": copy.deepcopy(
            fixture["g55_execution_approval_linkage"]
        ),
        "g55_execution_boundary": copy.deepcopy(fixture["g55_execution_boundary"]),
        "audit_evidence_linkage": copy.deepcopy(fixture["audit_evidence_linkage"]),
        "redaction_policy": copy.deepcopy(fixture["redaction_policy"]),
        "caller_injected_provider_sdk_network_executor_confirmation": True,
        "local_tests_use_fake_injected_executors_only_confirmation": True,
        "no_built_in_provider_sdk_client_confirmation": True,
        "no_sdk_dependency_confirmation": True,
        "no_direct_provider_sdk_implementation_confirmation": True,
        "no_lima_owned_endpoint_resolution_confirmation": True,
        "no_lima_owned_dns_http_socket_network_call_confirmation": True,
        "no_secret_lookup_confirmation": True,
        "no_credential_value_access_confirmation": True,
        "no_provider_token_or_api_key_access_confirmation": True,
        "no_provider_configuration_change_confirmation": True,
        "no_fallback_execution_confirmation": True,
        "no_consumer_production_runtime_integration_confirmation": True,
        "no_connector_browser_network_device_physical_world_confirmation": True,
        "no_raw_content_secret_credential_customer_data_diff_patch_confirmation": True,
        "no_product_readiness_confirmation": True,
    }
    request.update(overrides)
    return request


def _provider_sdk_network_result(**overrides: Any) -> dict[str, Any]:
    result = {
        "provider_sdk_call_ref": "provider-sdk-call:v1-g55:fake:001",
        "provider_sdk_response_ref": "provider-sdk-response:v1-g55:sanitized:001",
        "provider_network_egress_record_ref": (
            "provider-network-egress:v1-g55:caller-injected:001"
        ),
        "redacted_output_ref": "redacted-output-ref:v1-g55:sanitized:001",
        "redacted_output_summary_ref": (
            "output-summary-ref:v1-g55:sanitized:001"
        ),
        "finish_status": "completed",
        "usage_metadata": {
            "input_tokens": 17,
            "output_tokens": 11,
            "total_tokens": 28,
        },
        "network_call_performed_by_lima_harness": False,
        "direct_provider_egress_performed_by_lima": False,
        "secret_lookup_performed": False,
        "credential_value_accessed": False,
        "provider_token_or_api_key_accessed": False,
    }
    result.update(overrides)
    return result


def test_v1_g55_fixture_records_approved_scope_and_boundaries() -> None:
    fixture = _load_fixture()

    assert fixture["packet_set_id"] == "v1_g55_real_provider_sdk_network_egress"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g55-real-provider-sdk-network-egress"
    assert fixture["operator_decision"] == "Approve-V1-G55"
    assert fixture["approved_scope"] == (
        "bounded_real_provider_sdk_network_egress_authority_slice"
    )
    assert fixture["real_provider_sdk_network_egress_authority_approved"] is True
    assert fixture["real_provider_sdk_network_egress_authority_wrapper_added"] is True
    assert fixture["provider_sdk_network_egress_invocation_added"] is True
    assert fixture["caller_injected_provider_sdk_network_executor_only"] is True
    assert fixture["local_tests_use_fake_injected_executors_only"] is True
    assert fixture["product_ready"] is False


def test_v1_g55_file_scope_is_exact() -> None:
    fixture = _load_fixture()

    assert fixture["approved_lima_runtime_files_changed"] == [
        "lima/harness/v1_real_provider_sdk_network_egress.py",
        "lima/harness/__init__.py",
    ]
    assert fixture["approved_lima_docs_tests_fixtures_changed"] == [
        "docs/V1_G55_REAL_PROVIDER_SDK_NETWORK_EGRESS.md",
        "docs/V1_G55_REAL_PROVIDER_SDK_NETWORK_EGRESS_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g55_real_provider_sdk_network_egress.json",
        "tests/fixtures/runtime_extraction/v1_g22_final_public_api_freeze.json",
        "tests/test_v1_g55_real_provider_sdk_network_egress.py",
    ]
    assert fixture["approved_scope_amendment_files_changed"] == [
        "tests/test_v1_g51_executable_real_provider_executor_invocation.py",
        "tests/test_v1_g55_decision_log_status.py",
    ]
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["arc_bot_shell_files_changed"] is False
    assert fixture["consumer_production_runtime_integration_added"] is False


def test_v1_g55_harness_all_exports_match_fixture() -> None:
    fixture = _load_fixture()
    harness = importlib.import_module("lima.harness")

    assert list(getattr(harness, "__all__")) == fixture[
        "post_refresh_harness_all_exports"
    ]


def test_v1_g55_existing_harness_exports_are_preserved() -> None:
    fixture = _load_fixture()
    harness = importlib.import_module("lima.harness")
    exports = set(getattr(harness, "__all__"))

    for symbol_name in fixture["previous_harness_exports"]:
        assert symbol_name in exports
        assert hasattr(harness, symbol_name), symbol_name

    assert fixture["existing_frozen_harness_exports_preserved"] is True
    assert fixture["existing_frozen_harness_exports_removed"] is False
    assert fixture["existing_frozen_harness_exports_renamed"] is False


def test_v1_g55_execution_symbols_are_public_harness_exports() -> None:
    fixture = _load_fixture()
    harness = importlib.import_module("lima.harness")
    exports = set(getattr(harness, "__all__"))

    assert fixture["added_harness_exports"] == [
        "V1RealProviderSdkNetworkEgressError",
        "execute_v1_real_provider_sdk_network_egress",
    ]
    for symbol_name in fixture["added_harness_exports"]:
        assert symbol_name in exports
        assert hasattr(harness, symbol_name), symbol_name


def test_v1_g55_g22_freeze_fixture_reflects_execution_exports() -> None:
    fixture = _load_fixture()
    g22 = _load_json(G22_FIXTURE_PATH)

    assert (
        g22["public_subpackage_export_surfaces"]["lima.harness"]
        == fixture["post_refresh_harness_all_exports"]
    )
    assert fixture["g22_final_public_api_freeze_fixture_refreshed"] is True


def test_v1_g55_executes_only_through_injected_provider_sdk_network_executor() -> None:
    calls: list[dict[str, Any]] = []

    def fake_executor(payload: Any) -> dict[str, Any]:
        assert isinstance(payload, dict)
        calls.append(dict(payload))
        return _provider_sdk_network_result()

    record = execute_v1_real_provider_sdk_network_egress(
        _egress_request(),
        fake_executor,
    )

    assert len(calls) == 1
    assert calls[0] == {
        "egress_request_id": "egress-request:v1-g55:001",
        "invocation_request_id": (
            "real-provider-executor-invocation-request:v1-g50:metadata-only"
        ),
        "invocation_response_id": (
            "real-provider-executor-invocation-response:v1-g50:metadata-only"
        ),
        "provider_scope_ref": "provider-scope:v1-g49:single-provider-reference",
        "model_scope_ref": "model-scope:v1-g49:single-model-class-reference",
        "credential_policy_ref": "credential-policy:v1-g48:provider-reference-only",
        "network_policy_ref": "network-policy:v1-g48:provider-egress-reference-only",
        "provider_sdk_authority_ref": "provider-sdk-authority:v1-g53:metadata-only",
        "endpoint_resolution_authority_ref": (
            "endpoint-resolution-authority:v1-g53:metadata-only"
        ),
        "provider_network_egress_authority_ref": (
            "provider-network-egress-authority:v1-g53:metadata-only"
        ),
        "credential_reference_authority_ref": (
            "credential-reference-authority:v1-g53:metadata-only"
        ),
        "fake_sdk_harness_ref": "fake-sdk-harness:v1-g54:in-process-only",
        "fake_egress_harness_ref": "fake-egress-harness:v1-g54:in-process-only",
        "g51_execution_boundary_ref": "boundary:v1-g51:caller-injected-executor",
        "g55_execution_boundary_ref": (
            "boundary:v1-g55:caller-injected-sdk-network-executor"
        ),
        "provider_sdk_network_executor_ref": (
            "provider-sdk-network-executor:v1-g55:caller-injected"
        ),
        "provider_sdk_request_ref": "provider-sdk-request:v1-g55:sanitized",
        "sanitized_input_ref": "sanitized-input:v1-g55:metadata-only",
        "sanitized_output_ref": "sanitized-output:v1-g55:metadata-only",
        "redacted_input_ref": "redacted-input-ref:v1-g50:metadata-only",
        "redacted_output_ref": "redacted-output-ref:v1-g50:metadata-only",
        "redaction_policy_ref": (
            "redaction-policy:v1-g55:sanitized-sdk-network-egress"
        ),
        "audit_record_ref": "audit:v1-g55:real-provider-sdk-network-egress",
        "endpoint_policy_ref": "endpoint-policy:v1-g55:caller-owned-reference-only",
        "timeout_policy_ref": "timeout-policy:v1-g55:bounded",
        "g50_timeout_policy_ref": "timeout-policy:v1-g50:metadata-only",
        "cost_policy_ref": "cost-policy:v1-g55:bounded",
        "g50_cost_policy_ref": "cost-policy:v1-g50:metadata-only",
        "denial_policy_ref": "denial-policy:v1-g55:fail-closed",
        "failure_policy_ref": "failure-policy:v1-g50:fail-closed",
        "max_attempts": 1,
    }
    assert record["record_type"] == "v1_real_provider_sdk_network_egress"
    assert record["schema_version"] == "v1-g55-candidate"
    assert record["provider_sdk_network_executor_invoked"] is True
    assert record["provider_sdk_network_egress_invocation_added"] is True
    assert record["provider_sdk_call_ref"] == "provider-sdk-call:v1-g55:fake:001"
    assert record["usage_metadata"] == {
        "input_tokens": 17,
        "output_tokens": 11,
        "total_tokens": 28,
    }


def test_v1_g55_execution_record_keeps_forbidden_boundaries_false() -> None:
    record = execute_v1_real_provider_sdk_network_egress(
        _egress_request(),
        lambda payload: _provider_sdk_network_result(),
    )

    for key in (
        "built_in_provider_sdk_client_added",
        "built_in_provider_sdk_client_used",
        "real_provider_sdk_client_added_by_lima",
        "sdk_dependency_added",
        "direct_provider_sdk_implementation_added",
        "direct_provider_sdk_implementation_used",
        "provider_endpoint_resolution_added_by_lima",
        "provider_endpoint_resolution_performed_by_lima",
        "direct_network_code_added_by_lima",
        "dns_lookup_performed_by_lima",
        "http_client_used_by_lima",
        "socket_client_used_by_lima",
        "network_call_performed_by_lima_harness",
        "direct_provider_egress_performed_by_lima",
        "provider_readiness_network_check_added",
        "ambient_environment_secret_lookup_added",
        "secret_lookup_added",
        "secret_lookup_performed",
        "credential_value_access_added",
        "credential_value_accessed",
        "provider_token_or_api_key_access_added",
        "provider_token_or_api_key_accessed",
        "credential_storage_rotation_migration_or_provisioning_added",
        "provider_configuration_changes_added",
        "fallback_execution_added",
        "fallback_executed",
        "consumer_repo_mutation_added",
        "consumer_runtime_calls_added",
        "consumer_production_runtime_integration_added",
        "connector_browser_network_file_device_robotics_physical_world_behavior_added",
        "scheduled_task_execution_added",
        "external_send_added",
        "device_command_invoked",
        "robot_control_invoked",
        "drone_control_invoked",
        "iot_control_invoked",
        "physical_world_invoked",
        "raw_prompt_persisted",
        "raw_model_response_persisted",
        "raw_customer_data_persisted",
        "raw_secret_or_credential_persisted",
        "provider_token_or_api_key_persisted",
        "raw_diff_or_patch_persisted",
        "raw_file_content_persisted",
        "raw_sensitive_content_persisted",
        "product_ready",
        "production_ready",
    ):
        assert record[key] is False


def test_v1_g55_records_are_deterministic_for_sanitized_fake_executor() -> None:
    first = execute_v1_real_provider_sdk_network_egress(
        _egress_request(),
        lambda payload: _provider_sdk_network_result(),
    )
    second = execute_v1_real_provider_sdk_network_egress(
        _egress_request(),
        lambda payload: _provider_sdk_network_result(),
    )

    assert first == second
    assert first["record_hash"] == second["record_hash"]


def test_v1_g55_output_does_not_emit_sensitive_values() -> None:
    record = execute_v1_real_provider_sdk_network_egress(
        _egress_request(),
        lambda payload: _provider_sdk_network_result(),
    )
    output = json.dumps(record, sort_keys=True, default=str)

    for forbidden in (
        "raw prompt value",
        "raw model response value",
        "raw customer data value",
        "provider credential value",
        "provider token value",
        "api key value",
        "raw-secret-123",
    ):
        assert forbidden not in output


def test_v1_g55_missing_v1_g48_hardening_linkage_fails_closed() -> None:
    request = _egress_request()
    del request["credential_network_hardening_linkage"]

    with pytest.raises(
        V1RealProviderSdkNetworkEgressError,
        match="credential_network_hardening_linkage",
    ):
        execute_v1_real_provider_sdk_network_egress(
            request,
            lambda payload: _provider_sdk_network_result(),
        )


def test_v1_g55_missing_provider_sdk_network_executor_fails_closed() -> None:
    with pytest.raises(
        V1RealProviderSdkNetworkEgressError,
        match="provider_sdk_network_executor",
    ):
        execute_v1_real_provider_sdk_network_egress(
            _egress_request(),
            None,  # type: ignore[arg-type]
        )


def test_v1_g55_tampered_v1_g50_request_envelope_fails_closed() -> None:
    envelope = copy.deepcopy(_egress_request()["invocation_request_envelope"])
    envelope["provider_sdk_client_allowed"] = True

    with pytest.raises(
        V1RealProviderSdkNetworkEgressError,
        match="forbidden behavior",
    ):
        execute_v1_real_provider_sdk_network_egress(
            _egress_request(invocation_request_envelope=envelope),
            lambda payload: _provider_sdk_network_result(),
        )


def test_v1_g55_tampered_v1_g51_boundary_fails_closed() -> None:
    boundary = copy.deepcopy(_egress_request()["g51_execution_boundary"])
    boundary["network_call_performed_by_lima_harness"] = True

    with pytest.raises(
        V1RealProviderSdkNetworkEgressError,
        match="forbidden behavior",
    ):
        execute_v1_real_provider_sdk_network_egress(
            _egress_request(g51_execution_boundary=boundary),
            lambda payload: _provider_sdk_network_result(),
        )


def test_v1_g55_tampered_v1_g53_authority_fails_closed() -> None:
    authority = copy.deepcopy(_egress_request()["g53_provider_sdk_authority_metadata"])
    authority["sdk_dependency_addition_allowed"] = True

    with pytest.raises(
        V1RealProviderSdkNetworkEgressError,
        match="forbidden behavior",
    ):
        execute_v1_real_provider_sdk_network_egress(
            _egress_request(g53_provider_sdk_authority_metadata=authority),
            lambda payload: _provider_sdk_network_result(),
        )


def test_v1_g55_tampered_v1_g54_fake_egress_evidence_fails_closed() -> None:
    evidence = copy.deepcopy(_egress_request()["g54_fake_egress_harness_evidence"])
    evidence["http_client_used"] = True

    with pytest.raises(
        V1RealProviderSdkNetworkEgressError,
        match="forbidden behavior",
    ):
        execute_v1_real_provider_sdk_network_egress(
            _egress_request(g54_fake_egress_harness_evidence=evidence),
            lambda payload: _provider_sdk_network_result(),
        )


@pytest.mark.parametrize(
    "field",
    [
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
    ],
)
def test_v1_g55_execution_boundary_forbidden_flags_fail_closed(field: str) -> None:
    boundary = copy.deepcopy(_egress_request()["g55_execution_boundary"])
    boundary[field] = True

    with pytest.raises(
        V1RealProviderSdkNetworkEgressError,
        match="forbidden behavior",
    ):
        execute_v1_real_provider_sdk_network_egress(
            _egress_request(g55_execution_boundary=boundary),
            lambda payload: _provider_sdk_network_result(),
        )


@pytest.mark.parametrize(
    "field",
    [
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
    ],
)
def test_v1_g55_required_confirmations_fail_closed(field: str) -> None:
    with pytest.raises(V1RealProviderSdkNetworkEgressError, match=field):
        execute_v1_real_provider_sdk_network_egress(
            _egress_request(**{field: False}),
            lambda payload: _provider_sdk_network_result(),
        )


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("raw_prompt", "raw prompt value"),
        ("raw_model_response", "raw model response value"),
        ("raw_customer_data", "raw customer data value"),
        ("credentials", "provider credential value"),
        ("provider_token", "provider token value"),
        ("provider_api_key", "api key value"),
        ("raw_secret", "raw-secret-123"),
    ],
)
def test_v1_g55_raw_sensitive_request_content_fails_closed(
    field: str,
    value: str,
) -> None:
    with pytest.raises(
        V1RealProviderSdkNetworkEgressError,
        match="raw sensitive",
    ):
        execute_v1_real_provider_sdk_network_egress(
            _egress_request(**{field: value}),
            lambda payload: _provider_sdk_network_result(),
        )


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("raw_model_response", "raw model response value"),
        ("raw_customer_data", "raw customer data value"),
        ("credentials", "provider credential value"),
        ("provider_token", "provider token value"),
        ("provider_api_key", "api key value"),
        ("raw_secret", "raw-secret-123"),
        ("raw_response_payload", "raw response payload value"),
    ],
)
def test_v1_g55_raw_sensitive_provider_result_fails_closed(
    field: str,
    value: str,
) -> None:
    with pytest.raises(
        V1RealProviderSdkNetworkEgressError,
        match="raw sensitive",
    ):
        execute_v1_real_provider_sdk_network_egress(
            _egress_request(),
            lambda payload: _provider_sdk_network_result(**{field: value}),
        )


@pytest.mark.parametrize(
    "claim",
    [
        "built_in_provider_sdk_client_added",
        "sdk_dependency_added",
        "direct_provider_sdk_implementation_added",
        "provider_endpoint_resolution_added",
        "network_call_performed_by_lima",
        "direct_provider_egress_performed_by_lima",
        "secret_lookup_added",
        "credential_value_access_added",
        "fallback_execution_added",
        "product_ready",
    ],
)
def test_v1_g55_forbidden_true_claims_fail_closed(claim: str) -> None:
    with pytest.raises(
        V1RealProviderSdkNetworkEgressError,
        match="forbidden behavior",
    ):
        execute_v1_real_provider_sdk_network_egress(
            _egress_request(**{claim: True}),
            lambda payload: _provider_sdk_network_result(),
        )


def test_v1_g55_invalid_finish_status_fails_closed() -> None:
    with pytest.raises(
        V1RealProviderSdkNetworkEgressError,
        match="finish_status",
    ):
        execute_v1_real_provider_sdk_network_egress(
            _egress_request(),
            lambda payload: _provider_sdk_network_result(finish_status="streaming"),
        )


def test_v1_g55_inconsistent_usage_metadata_fails_closed() -> None:
    with pytest.raises(
        V1RealProviderSdkNetworkEgressError,
        match="total_tokens",
    ):
        execute_v1_real_provider_sdk_network_egress(
            _egress_request(),
            lambda payload: _provider_sdk_network_result(
                usage_metadata={
                    "input_tokens": 17,
                    "output_tokens": 11,
                    "total_tokens": 20,
                }
            ),
        )


def test_v1_g55_provider_executor_errors_are_wrapped() -> None:
    def failing_executor(payload: Any) -> dict[str, Any]:
        raise RuntimeError("provider failure")

    with pytest.raises(
        V1RealProviderSdkNetworkEgressError,
        match="executor failed",
    ):
        execute_v1_real_provider_sdk_network_egress(
            _egress_request(),
            failing_executor,
        )


def test_v1_g55_runtime_source_has_no_direct_provider_or_network_clients() -> None:
    source = RUNTIME_MODULE_PATH.read_text(encoding="utf-8")

    for forbidden in (
        "import requests",
        "import httpx",
        "import urllib",
        "import socket",
        "import subprocess",
        "import openai",
        "import anthropic",
        "import litellm",
        "os.environ",
    ):
        assert forbidden not in source


def test_v1_g55_fixture_records_no_unapproved_consumer_or_external_changes() -> None:
    fixture = _load_fixture()

    for key in (
        "consumer_repo_mutation_added",
        "consumer_runtime_calls_added",
        "consumer_production_runtime_integration_added",
        "built_in_provider_sdk_client_added",
        "built_in_provider_sdk_client_used",
        "real_provider_sdk_client_added_by_lima",
        "real_provider_sdk_client_used_by_lima",
        "sdk_dependency_added",
        "sdk_dependency_used",
        "direct_provider_sdk_implementation_added",
        "direct_provider_sdk_implementation_used",
        "vendor_provider_sdk_import_added",
        "provider_endpoint_resolution_added_by_lima",
        "provider_endpoint_resolution_performed_by_lima",
        "direct_network_code_added_by_lima",
        "dns_lookup_added_by_lima",
        "dns_lookup_performed_by_lima",
        "http_client_added_by_lima",
        "http_client_used_by_lima",
        "socket_client_added_by_lima",
        "socket_client_used_by_lima",
        "network_call_performed_by_lima",
        "network_call_performed_by_lima_harness",
        "direct_provider_egress_performed_by_lima",
        "provider_readiness_network_check_added",
        "provider_readiness_network_check_performed",
        "ambient_environment_secret_lookup_added",
        "secret_lookup_added",
        "secret_lookup_performed",
        "credential_value_access_added",
        "credential_value_accessed",
        "provider_token_or_api_key_access_added",
        "provider_token_or_api_key_accessed",
        "provider_configuration_changes_added",
        "fallback_execution_added",
        "fallback_executed",
        "connector_browser_network_file_device_robotics_physical_world_behavior_added",
        "external_send_added",
        "raw_prompt_persisted",
        "raw_model_response_persisted",
        "raw_customer_data_persisted",
        "raw_secret_or_credential_persisted",
        "provider_token_or_api_key_persisted",
        "raw_diff_or_patch_persisted",
        "raw_file_content_persisted",
        "raw_sensitive_content_persisted",
        "product_ready",
        "production_ready",
    ):
        assert fixture[key] is False

    assert fixture["credential_reference_metadata_only"] is True


def test_v1_g55_evidence_refs_exist() -> None:
    fixture = _load_fixture()

    for relative_path in fixture["required_prior_evidence_refs"]:
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g55_rollback_metadata_is_local_and_reversible() -> None:
    rollback = _load_fixture()["rollback_metadata"]

    assert rollback["rollback_ref"] == "rollback:v1-g55:real-provider-sdk-network-egress"
    assert rollback["rollback_runtime_file_refs"] == [
        "lima/harness/v1_real_provider_sdk_network_egress.py",
        "lima/harness/__init__.py",
    ]
    assert rollback["rollback_scope_amendment_refs"] == [
        "tests/test_v1_g51_executable_real_provider_executor_invocation.py",
        "tests/test_v1_g55_decision_log_status.py",
    ]
    assert rollback["consumer_repo_changes_required"] is False
    assert rollback["external_service_changes_required"] is False
    assert rollback["provider_configuration_changes_required"] is False
    assert rollback["credential_rotation_required"] is False


def test_v1_g55_required_confirmations_are_true() -> None:
    confirmations = _load_fixture()["required_confirmations"]

    assert all(confirmations.values())
    assert confirmations["operator_approval_recorded_confirmation"] is True
    assert confirmations["caller_injected_provider_sdk_network_executor_only_confirmation"] is True
    assert confirmations["local_tests_use_fake_injected_executors_only_confirmation"] is True
    assert confirmations["no_built_in_provider_sdk_client_confirmation"] is True
    assert confirmations["no_lima_owned_dns_http_socket_network_call_confirmation"] is True
    assert confirmations["no_secret_lookup_confirmation"] is True
    assert confirmations["proof_not_product_readiness_confirmation"] is True


def test_v1_g55_lima_validation_results_are_recorded() -> None:
    validation = _load_fixture()["lima_validation_results"]

    assert validation["focused_v1_g55_validation"]["passed"] is True
    assert validation["focused_v1_g55_g54_g53_g52_g51_g50_g48_g22_validation"][
        "passed"
    ] is True
    assert validation["compileall_lima"] == {
        "command": "python -m compileall lima",
        "passed": True,
    }
    assert validation["full_lima_suite"]["passed"] is True


def test_v1_g55_fixture_and_docs_do_not_include_sensitive_markers() -> None:
    output = json.dumps(_load_fixture(), sort_keys=True)
    output += (
        REPO_ROOT / "docs" / "V1_G55_REAL_PROVIDER_SDK_NETWORK_EGRESS.md"
    ).read_text(encoding="utf-8")
    output += (
        REPO_ROOT / "docs" / "V1_G55_REAL_PROVIDER_SDK_NETWORK_EGRESS_CLOSEOUT.md"
    ).read_text(encoding="utf-8")

    for forbidden in (
        "diff --git",
        "@@",
        "BEGIN PATCH",
        "raw patch body",
        "raw prompt value",
        "raw model response value",
        "raw customer data value",
        "provider credential value",
        "provider token value",
        "api key value",
        "raw-secret-123",
    ):
        assert forbidden not in output


def test_v1_g55_docs_contain_boundary_language() -> None:
    implementation_text = (
        REPO_ROOT / "docs" / "V1_G55_REAL_PROVIDER_SDK_NETWORK_EGRESS.md"
    ).read_text(encoding="utf-8")
    closeout_text = (
        REPO_ROOT / "docs" / "V1_G55_REAL_PROVIDER_SDK_NETWORK_EGRESS_CLOSEOUT.md"
    ).read_text(encoding="utf-8")

    assert "caller-injected provider SDK/network executor" in implementation_text
    assert "No built-in provider SDK client" in implementation_text
    assert "No Sparkbot file was changed" in implementation_text
    assert "Fallback execution added: no" in implementation_text
    assert "V1-G55 is complete" in closeout_text
    assert "No product-readiness or production-readiness claim" in closeout_text
