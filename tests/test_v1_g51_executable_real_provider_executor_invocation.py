"""Tests for the approved V1-G51 executable provider invocation wrapper."""

from __future__ import annotations

import copy
import importlib
import json
from pathlib import Path
from typing import Any

import pytest

from lima.harness import (
    V1ExecutableRealProviderExecutorInvocationError,
    execute_v1_executable_real_provider_executor_invocation,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g51_executable_real_provider_executor_invocation.json"
)
G50_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g50_real_provider_executor_invocation.json"
)
G22_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g22_final_public_api_freeze.json"
)
RUNTIME_MODULE_PATH = (
    REPO_ROOT / "lima" / "harness" / "v1_executable_real_provider_executor_invocation.py"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _load_g50_fixture() -> dict[str, Any]:
    fixture = json.loads(G50_FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _load_g22_fixture() -> dict[str, Any]:
    fixture = json.loads(G22_FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _execution_request(**overrides: Any) -> dict[str, Any]:
    g50 = _load_g50_fixture()
    request = {
        "invocation_id": "invocation:v1-g51:001",
        "invocation_request_envelope": copy.deepcopy(
            g50["invocation_request_envelope"]
        ),
        "invocation_response_envelope": copy.deepcopy(
            g50["invocation_response_envelope"]
        ),
        "provider_model_scope": copy.deepcopy(g50["provider_model_scope"]),
        "executor_authority_linkage": copy.deepcopy(
            g50["executor_authority_linkage"]
        ),
        "credential_network_hardening_linkage": copy.deepcopy(
            g50["credential_network_hardening_linkage"]
        ),
        "g50_execution_boundary_metadata": copy.deepcopy(
            g50["execution_boundary_metadata"]
        ),
        "provider_executor_ref": "provider-executor:v1-g51:fake-real-provider",
        "provider_request_ref": "provider-request:v1-g51:redacted:001",
        "g51_execution_approval_linkage": {
            "approval_evidence_ref": "approval-evidence:v1-g51:001",
            "approval_evidence_current": True,
            "approval_scope": "v1-g51-executable-real-provider-executor-invocation",
            "grants_executable_real_provider_executor_invocation_authority": True,
            "proof_of_operator_approval": True,
        },
        "g51_execution_boundary": copy.deepcopy(_load_fixture()["execution_boundary"]),
        "audit_evidence_linkage": {
            "audit_record_ref": "audit:v1-g51:executable-real-provider-executor",
            "evidence_refs": [
                "evidence:v1-g50:invocation-request-envelope-metadata",
                "evidence:v1-g49:real-provider-executor-authority-design",
                "evidence:v1-g48:credential-reference-only",
            ],
            "required": True,
            "sanitized_evidence_only": True,
        },
        "redaction_policy": {
            "redaction_policy_ref": "redaction-policy:v1-g51:sanitized",
            "redacted_input_required": True,
            "redacted_output_required": True,
            "raw_prompt_persistence_allowed": False,
            "raw_model_response_persistence_allowed": False,
            "raw_customer_data_persistence_allowed": False,
            "raw_secret_credential_persistence_allowed": False,
            "raw_diff_patch_file_content_persistence_allowed": False,
        },
        "caller_injected_provider_executor_confirmation": True,
        "no_built_in_provider_sdk_confirmation": True,
        "no_direct_network_code_confirmation": True,
        "no_provider_endpoint_resolution_confirmation": True,
        "no_secret_lookup_confirmation": True,
        "no_credential_value_access_confirmation": True,
        "no_provider_token_or_api_key_access_confirmation": True,
        "no_fallback_execution_confirmation": True,
        "no_connector_browser_network_physical_world_confirmation": True,
        "no_raw_prompt_model_response_customer_data_persistence_confirmation": True,
    }
    request.update(overrides)
    return request


def _provider_result(**overrides: Any) -> dict[str, Any]:
    result = {
        "provider_call_ref": "provider-call-ref:v1-g51:fake:001",
        "redacted_output_ref": "redacted-output-ref:v1-g51:001",
        "redacted_output_summary_ref": "output-summary-ref:v1-g51:redacted",
        "finish_status": "completed",
        "usage_metadata": {
            "input_tokens": 13,
            "output_tokens": 8,
            "total_tokens": 21,
        },
    }
    result.update(overrides)
    return result


def test_v1_g51_fixture_records_approved_scope_and_boundaries() -> None:
    fixture = _load_fixture()

    assert fixture["packet_set_id"] == (
        "v1_g51_executable_real_provider_executor_invocation"
    )
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g51-executable-real-provider-executor-invocation"
    assert fixture["operator_decision"] == "Approve-V1-G51"
    assert fixture["scope_amendment_decision"] == "Approve-V1-G51-Scope-Amendment"
    assert fixture["approved_scope"] == (
        "executable_real_provider_executor_invocation_wrapper_slice"
    )
    assert fixture["executable_real_provider_executor_invocation_wrapper_approved"] is True
    assert fixture["executable_real_provider_executor_invocation_wrapper_added"] is True
    assert fixture["provider_executor_invocation_added"] is True
    assert fixture["real_provider_executor_invocation_added"] is True
    assert fixture["product_ready"] is False


def test_v1_g51_file_scope_is_exact() -> None:
    fixture = _load_fixture()

    assert fixture["approved_runtime_files_changed"] == [
        "lima/harness/v1_executable_real_provider_executor_invocation.py",
        "lima/harness/__init__.py",
    ]
    assert fixture["approved_scope_amendment_files_changed"] == [
        "tests/test_v1_g46_live_provider_model_call_execution.py"
    ]
    assert set(fixture["approved_docs_tests_fixtures_changed"]) == {
        "docs/V1_G51_EXECUTABLE_REAL_PROVIDER_EXECUTOR_INVOCATION.md",
        "docs/V1_G51_EXECUTABLE_REAL_PROVIDER_EXECUTOR_INVOCATION_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g51_executable_real_provider_executor_invocation.json",
        "tests/fixtures/runtime_extraction/v1_g22_final_public_api_freeze.json",
        "tests/test_v1_g51_executable_real_provider_executor_invocation.py",
    }
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["arc_bot_shell_files_changed"] is False


def test_v1_g51_harness_all_exports_match_fixture() -> None:
    fixture = _load_fixture()
    harness = importlib.import_module("lima.harness")
    expected_exports = fixture["post_refresh_harness_all_exports"]
    actual_exports = list(getattr(harness, "__all__"))

    assert actual_exports[: len(expected_exports)] == expected_exports


def test_v1_g51_existing_harness_exports_are_preserved() -> None:
    fixture = _load_fixture()
    harness = importlib.import_module("lima.harness")
    exports = set(getattr(harness, "__all__"))

    for symbol_name in fixture["previous_harness_exports"]:
        assert symbol_name in exports
        assert hasattr(harness, symbol_name), symbol_name

    assert fixture["existing_frozen_harness_exports_preserved"] is True
    assert fixture["existing_frozen_harness_exports_removed"] is False
    assert fixture["existing_frozen_harness_exports_renamed"] is False


def test_v1_g51_execution_symbols_are_public_harness_exports() -> None:
    fixture = _load_fixture()
    harness = importlib.import_module("lima.harness")
    exports = set(getattr(harness, "__all__"))

    assert fixture["added_harness_exports"] == [
        "V1ExecutableRealProviderExecutorInvocationError",
        "execute_v1_executable_real_provider_executor_invocation",
    ]
    for symbol_name in fixture["added_harness_exports"]:
        assert symbol_name in exports
        assert hasattr(harness, symbol_name), symbol_name


def test_v1_g51_g22_freeze_fixture_reflects_execution_exports() -> None:
    fixture = _load_fixture()
    g22 = _load_g22_fixture()
    expected_exports = fixture["post_refresh_harness_all_exports"]
    actual_exports = g22["public_subpackage_export_surfaces"]["lima.harness"]

    assert actual_exports[: len(expected_exports)] == expected_exports
    assert fixture["g22_final_public_api_freeze_fixture_refreshed"] is True


def test_v1_g51_executes_only_through_injected_provider_executor() -> None:
    calls: list[dict[str, Any]] = []

    def fake_executor(payload: Any) -> dict[str, Any]:
        assert isinstance(payload, dict)
        calls.append(dict(payload))
        return _provider_result()

    record = execute_v1_executable_real_provider_executor_invocation(
        _execution_request(),
        fake_executor,
    )

    assert len(calls) == 1
    assert calls[0] == {
        "invocation_id": "invocation:v1-g51:001",
        "invocation_request_id": (
            "real-provider-executor-invocation-request:v1-g50:metadata-only"
        ),
        "invocation_response_id": (
            "real-provider-executor-invocation-response:v1-g50:metadata-only"
        ),
        "provider_scope_ref": "provider-scope:v1-g49:single-provider-reference",
        "model_scope_ref": "model-scope:v1-g49:single-model-class-reference",
        "executor_authority_ref": (
            "real-provider-executor-authority:v1-g49:metadata-only"
        ),
        "credential_policy_ref": "credential-policy:v1-g48:provider-reference-only",
        "network_policy_ref": "network-policy:v1-g48:provider-egress-reference-only",
        "provider_executor_ref": "provider-executor:v1-g51:fake-real-provider",
        "provider_request_ref": "provider-request:v1-g51:redacted:001",
        "redacted_input_ref": "redacted-input-ref:v1-g50:metadata-only",
        "redacted_output_ref": "redacted-output-ref:v1-g50:metadata-only",
        "redaction_policy_ref": "redaction-policy:v1-g51:sanitized",
        "audit_record_ref": "audit:v1-g51:executable-real-provider-executor",
        "timeout_policy_ref": "timeout-policy:v1-g50:metadata-only",
        "retry_policy_ref": "retry-policy:v1-g50:no-execution",
        "cost_policy_ref": "cost-policy:v1-g50:metadata-only",
        "failure_policy_ref": "failure-policy:v1-g50:fail-closed",
        "max_attempts": 1,
    }
    assert record["record_type"] == "v1_executable_real_provider_executor_invocation"
    assert record["schema_version"] == "v1-g51-candidate"
    assert record["executable_real_provider_executor_invocation_wrapper_added"] is True
    assert record["provider_executor_invocation_added"] is True
    assert record["provider_executor_invoked"] is True
    assert record["real_provider_executor_invocation_added"] is True
    assert record["real_provider_executor_invoked"] is True
    assert record["actual_model_request_dispatch_execution_added"] is True
    assert record["model_request_dispatched"] is True
    assert record["caller_injected_provider_executor_only"] is True
    assert record["provider_call_ref"] == "provider-call-ref:v1-g51:fake:001"
    assert record["usage_metadata"] == {
        "input_tokens": 13,
        "output_tokens": 8,
        "total_tokens": 21,
    }


def test_v1_g51_execution_record_keeps_forbidden_boundaries_false() -> None:
    record = execute_v1_executable_real_provider_executor_invocation(
        _execution_request(),
        lambda payload: _provider_result(),
    )

    for key in (
        "built_in_provider_sdk_added",
        "built_in_provider_sdk_used",
        "direct_provider_sdk_added",
        "direct_provider_sdk_used",
        "direct_network_code_added",
        "direct_network_code_used",
        "network_call_performed_by_lima_harness",
        "provider_endpoint_resolution_added",
        "provider_endpoint_resolution_performed",
        "provider_readiness_network_check_added",
        "token_guardian_live_routing_added",
        "ambient_environment_secret_lookup_added",
        "secret_lookup_added",
        "secret_lookup_performed",
        "credential_value_access_added",
        "credential_value_accessed",
        "provider_token_or_api_key_access_added",
        "provider_token_or_api_key_accessed",
        "credential_storage_or_rotation_added",
        "provider_configuration_changes_added",
        "fallback_execution_added",
        "fallback_executed",
        "tool_execution_added",
        "tool_executed",
        "action_executed",
        "file_mutation_executed",
        "consumer_repo_mutation_added",
        "consumer_code_imported",
        "consumer_runtime_calls_added",
        "consumer_integration_added",
        "shell_runtime_wired",
        "connector_invoked",
        "browser_action_executed",
        "network_action_executed",
        "scheduled_task_executed",
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
    ):
        assert record[key] is False


def test_v1_g51_records_are_deterministic_for_sanitized_fake_executor() -> None:
    first = execute_v1_executable_real_provider_executor_invocation(
        _execution_request(),
        lambda payload: _provider_result(),
    )
    second = execute_v1_executable_real_provider_executor_invocation(
        _execution_request(),
        lambda payload: _provider_result(),
    )

    assert first == second
    assert first["record_hash"] == second["record_hash"]


def test_v1_g51_output_does_not_emit_sensitive_values() -> None:
    record = execute_v1_executable_real_provider_executor_invocation(
        _execution_request(),
        lambda payload: _provider_result(),
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


def test_v1_g51_missing_v1_g50_request_envelope_fails_closed() -> None:
    request = _execution_request()
    del request["invocation_request_envelope"]

    with pytest.raises(
        V1ExecutableRealProviderExecutorInvocationError,
        match="invocation_request_envelope",
    ):
        execute_v1_executable_real_provider_executor_invocation(
            request,
            lambda payload: _provider_result(),
        )


def test_v1_g51_tampered_v1_g50_request_envelope_fails_closed() -> None:
    envelope = copy.deepcopy(_execution_request()["invocation_request_envelope"])
    envelope["provider_sdk_client_allowed"] = True

    with pytest.raises(
        V1ExecutableRealProviderExecutorInvocationError,
        match="provider_sdk_client_allowed",
    ):
        execute_v1_executable_real_provider_executor_invocation(
            _execution_request(invocation_request_envelope=envelope),
            lambda payload: _provider_result(),
        )


def test_v1_g51_tampered_v1_g50_response_envelope_fails_closed() -> None:
    envelope = copy.deepcopy(_execution_request()["invocation_response_envelope"])
    envelope["provider_executor_invoked"] = True

    with pytest.raises(
        V1ExecutableRealProviderExecutorInvocationError,
        match="provider_executor_invoked",
    ):
        execute_v1_executable_real_provider_executor_invocation(
            _execution_request(invocation_response_envelope=envelope),
            lambda payload: _provider_result(),
        )


def test_v1_g51_tampered_executor_authority_linkage_fails_closed() -> None:
    authority = copy.deepcopy(_execution_request()["executor_authority_linkage"])
    authority["executable_provider_invocation_allowed"] = True

    with pytest.raises(
        V1ExecutableRealProviderExecutorInvocationError,
        match="executable_provider_invocation_allowed",
    ):
        execute_v1_executable_real_provider_executor_invocation(
            _execution_request(executor_authority_linkage=authority),
            lambda payload: _provider_result(),
        )


def test_v1_g51_tampered_hardening_linkage_fails_closed() -> None:
    hardening = copy.deepcopy(_execution_request()["credential_network_hardening_linkage"])
    hardening["secret_lookup_allowed"] = True

    with pytest.raises(
        V1ExecutableRealProviderExecutorInvocationError,
        match="secret_lookup_allowed",
    ):
        execute_v1_executable_real_provider_executor_invocation(
            _execution_request(credential_network_hardening_linkage=hardening),
            lambda payload: _provider_result(),
        )


def test_v1_g51_missing_provider_executor_fails_closed() -> None:
    with pytest.raises(
        V1ExecutableRealProviderExecutorInvocationError,
        match="provider_executor",
    ):
        execute_v1_executable_real_provider_executor_invocation(
            _execution_request(),
            None,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    "field",
    [
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
    ],
)
def test_v1_g51_execution_boundary_forbidden_flags_fail_closed(field: str) -> None:
    boundary = copy.deepcopy(_execution_request()["g51_execution_boundary"])
    boundary[field] = True

    with pytest.raises(
        V1ExecutableRealProviderExecutorInvocationError,
        match="forbidden behavior",
    ):
        execute_v1_executable_real_provider_executor_invocation(
            _execution_request(g51_execution_boundary=boundary),
            lambda payload: _provider_result(),
        )


@pytest.mark.parametrize(
    "field",
    [
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
    ],
)
def test_v1_g51_required_confirmations_fail_closed(field: str) -> None:
    with pytest.raises(V1ExecutableRealProviderExecutorInvocationError, match=field):
        execute_v1_executable_real_provider_executor_invocation(
            _execution_request(**{field: False}),
            lambda payload: _provider_result(),
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
def test_v1_g51_raw_sensitive_request_content_fails_closed(
    field: str,
    value: str,
) -> None:
    with pytest.raises(
        V1ExecutableRealProviderExecutorInvocationError,
        match="raw sensitive",
    ):
        execute_v1_executable_real_provider_executor_invocation(
            _execution_request(**{field: value}),
            lambda payload: _provider_result(),
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
def test_v1_g51_raw_sensitive_provider_result_fails_closed(
    field: str,
    value: str,
) -> None:
    with pytest.raises(
        V1ExecutableRealProviderExecutorInvocationError,
        match="raw sensitive",
    ):
        execute_v1_executable_real_provider_executor_invocation(
            _execution_request(),
            lambda payload: _provider_result(**{field: value}),
        )


@pytest.mark.parametrize(
    "claim",
    [
        "built_in_provider_sdk_added",
        "direct_network_code_added",
        "provider_endpoint_resolution_added",
        "network_call_performed",
        "secret_lookup_added",
        "credential_value_access_added",
        "fallback_execution_added",
        "product_ready",
    ],
)
def test_v1_g51_forbidden_true_claims_fail_closed(claim: str) -> None:
    with pytest.raises(
        V1ExecutableRealProviderExecutorInvocationError,
        match="forbidden behavior",
    ):
        execute_v1_executable_real_provider_executor_invocation(
            _execution_request(**{claim: True}),
            lambda payload: _provider_result(),
        )


def test_v1_g51_invalid_finish_status_fails_closed() -> None:
    with pytest.raises(
        V1ExecutableRealProviderExecutorInvocationError,
        match="finish_status",
    ):
        execute_v1_executable_real_provider_executor_invocation(
            _execution_request(),
            lambda payload: _provider_result(finish_status="streaming"),
        )


def test_v1_g51_inconsistent_usage_metadata_fails_closed() -> None:
    with pytest.raises(
        V1ExecutableRealProviderExecutorInvocationError,
        match="total_tokens",
    ):
        execute_v1_executable_real_provider_executor_invocation(
            _execution_request(),
            lambda payload: _provider_result(
                usage_metadata={
                    "input_tokens": 13,
                    "output_tokens": 8,
                    "total_tokens": 14,
                }
            ),
        )


def test_v1_g51_provider_executor_errors_are_wrapped() -> None:
    def failing_executor(payload: Any) -> dict[str, Any]:
        raise RuntimeError("provider failure")

    with pytest.raises(
        V1ExecutableRealProviderExecutorInvocationError,
        match="executor failed",
    ):
        execute_v1_executable_real_provider_executor_invocation(
            _execution_request(),
            failing_executor,
        )


def test_v1_g51_runtime_source_has_no_direct_provider_or_network_clients() -> None:
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


def test_v1_g51_fixture_records_no_unapproved_consumer_or_external_changes() -> None:
    fixture = _load_fixture()

    for key in (
        "built_in_provider_sdk_added",
        "built_in_provider_sdk_used",
        "direct_provider_sdk_added",
        "direct_provider_sdk_used",
        "direct_network_code_added",
        "direct_network_code_used",
        "network_call_performed_by_lima_harness",
        "provider_endpoint_resolution_added",
        "provider_endpoint_resolution_performed",
        "network_call_performed",
        "ambient_environment_secret_lookup_added",
        "secret_lookup_added",
        "secret_lookup_performed",
        "credential_value_access_added",
        "credential_value_accessed",
        "provider_token_or_api_key_access_added",
        "provider_token_or_api_key_accessed",
        "fallback_execution_added",
        "fallback_executed",
        "provider_readiness_network_check_added",
        "token_guardian_live_routing_added",
        "tool_execution_added",
        "connector_browser_network_file_device_robotics_physical_world_behavior_added",
        "consumer_repo_mutation_added",
        "sparkbot_files_changed",
        "arc_bot_shell_files_changed",
        "consumer_runtime_calls_added",
        "consumer_integration_added",
        "raw_prompt_persisted",
        "raw_model_response_persisted",
        "raw_customer_data_persisted",
        "raw_secret_or_credential_persisted",
        "provider_token_or_api_key_persisted",
        "raw_diff_or_patch_persisted",
        "raw_file_content_persisted",
        "raw_sensitive_content_persisted",
        "product_ready",
    ):
        assert fixture[key] is False


def test_v1_g51_evidence_refs_exist() -> None:
    fixture = _load_fixture()

    for relative_path in fixture["accepted_evidence_refs"]:
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g51_rollback_metadata_is_local_and_reversible() -> None:
    rollback = _load_fixture()["rollback_metadata"]

    assert rollback["rollback_ref"] == (
        "rollback:v1-g51:executable-real-provider-executor-invocation"
    )
    assert rollback["rollback_runtime_file_refs"] == [
        "lima/harness/v1_executable_real_provider_executor_invocation.py",
        "lima/harness/__init__.py",
    ]
    assert rollback["rollback_scope_amendment_refs"] == [
        "tests/test_v1_g46_live_provider_model_call_execution.py"
    ]
    assert rollback["consumer_repo_changes_required"] is False
    assert rollback["external_service_changes_required"] is False
    assert rollback["provider_configuration_changes_required"] is False
    assert rollback["credential_rotation_required"] is False


def test_v1_g51_required_confirmations_are_true() -> None:
    confirmations = _load_fixture()["required_confirmations"]

    assert all(confirmations.values())
    assert confirmations["caller_injected_provider_executor_only_confirmation"] is True
    assert confirmations["local_tests_use_fake_injected_executors_only_confirmation"] is True
    assert confirmations["no_built_in_provider_sdk_confirmation"] is True
    assert confirmations["no_direct_network_code_confirmation"] is True
    assert confirmations["no_provider_endpoint_resolution_confirmation"] is True
    assert confirmations["no_secret_lookup_confirmation"] is True
    assert confirmations["no_credential_value_access_confirmation"] is True
    assert confirmations["no_fallback_execution_confirmation"] is True
    assert confirmations["no_product_readiness_confirmation"] is True


def test_v1_g51_lima_validation_results_are_recorded() -> None:
    validation = _load_fixture()["lima_validation_results"]

    assert validation["focused_v1_g51_validation"]["passed"] is True
    assert validation["focused_v1_g51_validation"]["tests_passed"] == 71
    assert validation["focused_v1_g51_g50_g49_g48_g47_g46_g22_validation"]["passed"] is True
    assert (
        validation["focused_v1_g51_g50_g49_g48_g47_g46_g22_validation"][
            "tests_passed"
        ]
        == 286
    )
    assert validation["compileall_lima"] == {
        "command": "python -m compileall lima",
        "passed": True,
    }
    assert validation["full_lima_suite"]["passed"] is True
    assert validation["full_lima_suite"]["tests_passed"] == 4516


def test_v1_g51_docs_contain_boundary_language() -> None:
    implementation_text = (
        REPO_ROOT / "docs" / "V1_G51_EXECUTABLE_REAL_PROVIDER_EXECUTOR_INVOCATION.md"
    ).read_text(encoding="utf-8")
    closeout_text = (
        REPO_ROOT
        / "docs"
        / "V1_G51_EXECUTABLE_REAL_PROVIDER_EXECUTOR_INVOCATION_CLOSEOUT.md"
    ).read_text(encoding="utf-8")

    assert "caller-injected provider executor" in implementation_text
    assert "No built-in provider SDK" in implementation_text
    assert "No Sparkbot file was changed" in implementation_text
    assert "Fallback execution added: no" in implementation_text
    assert "V1-G51 is complete" in closeout_text
    assert "No product-readiness or production-readiness claim" in closeout_text
