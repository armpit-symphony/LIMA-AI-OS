"""Tests for the approved V1-G46 live provider/model call execution slice."""

from __future__ import annotations

import importlib
import json
from pathlib import Path
from typing import Any

import pytest

from lima.harness import (
    V1LiveProviderModelCallExecutionError,
    execute_v1_live_provider_model_call,
    validate_v1_live_provider_model_call_authority,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g46_live_provider_model_call_execution.json"
)
G22_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g22_final_public_api_freeze.json"
)
RUNTIME_MODULE_PATH = (
    REPO_ROOT / "lima" / "harness" / "v1_live_provider_model_call_execution.py"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _load_g22_fixture() -> dict[str, Any]:
    fixture = json.loads(G22_FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _authority_metadata(**overrides: Any) -> dict[str, Any]:
    record = {
        "authority_id": "authority:v1-g44:001",
        "request_or_guardian_decision_linkage": {
            "request_id": "request:v1-g44:001",
            "guardian_decision_id": "decision:v1-g44:001",
            "linkage_required": True,
            "proof_not_execution": True,
            "grants_execution_authority": False,
        },
        "tenant_scope": "tenant:alpha",
        "shell_scope": "shell:sparkbot-shell",
        "actor_scope": "actor:user-123",
        "session_scope": "session:local",
        "source_provider_model_route_authority_ref": "route:v1-g20:001",
        "source_provider_model_dispatch_evidence_ref": (
            "provider-model-dispatch:v1-g43:fake-provider:001"
        ),
        "provider_id": "provider:openai:metadata-ref",
        "model_id": "model:gpt-class",
        "model_role": "primary",
        "provider_boundary_metadata": {
            "provider_boundary_ref": "provider-boundary:v1-g44:openai",
            "provider_class": "hosted_api_metadata",
            "provider_configured_for_scope": True,
            "live_provider_call_authority_policy_bound": True,
            "live_provider_call_execution_allowed": False,
            "provider_readiness_network_check_allowed": False,
            "token_guardian_live_routing_allowed": False,
            "proof_not_execution": True,
        },
        "credential_reference_metadata": {
            "credential_ref": "vault-ref:metadata/openai-live-call",
            "provider_is_no_key_local": False,
            "reference_only": True,
            "secret_lookup_performed": False,
            "credential_value_accessed": False,
            "raw_secret_present": False,
            "credential_value_present": False,
            "provider_token_present": False,
        },
        "network_policy_reference_metadata": {
            "network_policy_ref": "network-policy:v1-g44:provider-egress",
            "reference_only": True,
            "network_scope_bound": True,
            "network_call_performed": False,
            "provider_endpoint_resolution_performed": False,
            "proof_not_execution": True,
        },
        "prompt_reference_metadata": {
            "prompt_ref": "prompt-ref:v1-g44:redacted-summary",
            "prompt_context_class": "redacted_summary",
            "reference_only": True,
            "redacted": True,
            "raw_prompt_present": False,
            "raw_customer_data_present": False,
        },
        "output_handling_policy": {
            "output_policy_ref": "output-policy:v1-g44:redacted",
            "audit_output_ref": "audit-output:v1-g44:redacted-summary",
            "redacted_output_required": True,
            "raw_model_response_present": False,
            "persist_raw_model_response": False,
            "proof_not_execution": True,
        },
        "data_sensitivity": "internal",
        "budget_class": "medium",
        "estimated_cost_class": "low",
        "latency_tier": "interactive",
        "approval_evidence_linkage": {
            "approval_required_by_policy": True,
            "approval_evidence_ref": "approval-evidence:v1-g44:001",
            "approval_evidence_current": True,
            "proof_not_execution": True,
            "grants_execution_authority": False,
        },
        "audit_evidence_linkage": {
            "audit_record_ref": "audit:v1-g44:live-provider-call-authority",
            "evidence_refs": [
                "route:v1-g20:001",
                "provider-model-dispatch:v1-g43:fake-provider:001",
            ],
            "required": True,
            "proof_not_execution": True,
        },
        "proof_not_execution_confirmation": True,
        "no_raw_prompt_model_response_customer_data_confirmation": True,
        "no_secret_lookup_confirmation": True,
        "no_credential_value_access_confirmation": True,
        "no_network_call_confirmation": True,
        "no_live_provider_call_execution_confirmation": True,
        "no_fallback_execution_confirmation": True,
    }
    record.update(overrides)
    return record


def _authority_record() -> dict[str, Any]:
    return validate_v1_live_provider_model_call_authority(_authority_metadata())


def _execution_request(**overrides: Any) -> dict[str, Any]:
    request = {
        'guardian_decision': {
            'decision_id': 'decision:v1-g44:001',
            'status': 'allow',
            'allowed': True,
            'requires_approval': False,
        },
        "execution_id": "execution:v1-g46:001",
        "authority_record": _authority_record(),
        "provider_executor_ref": "provider-executor:v1-g46:fake-openai",
        "provider_request_ref": "provider-request:v1-g46:redacted:001",
        "redacted_prompt_ref": "prompt-ref:v1-g46:redacted-summary",
        "redacted_input_summary_ref": "input-summary:v1-g46:redacted",
        "execution_approval_linkage": {
            "approval_evidence_ref": "approval-evidence:v1-g46:001",
            "approval_evidence_current": True,
            "approval_scope": "v1-g46-live-provider-model-call-execution",
            "grants_live_provider_execution_authority": True,
            "proof_of_operator_approval": True,
        },
        "audit_evidence_linkage": {
            "audit_record_ref": "audit:v1-g46:live-provider-model-call-execution",
            "evidence_refs": [
                "authority:v1-g44:001",
                "provider-model-dispatch:v1-g43:fake-provider:001",
            ],
            "required": True,
            "sanitized_evidence_only": True,
        },
        "redaction_policy": {
            "redaction_policy_ref": "redaction-policy:v1-g46:sanitized",
            "redacted_input_required": True,
            "redacted_output_required": True,
            "raw_prompt_persistence_allowed": False,
            "raw_model_response_persistence_allowed": False,
            "raw_customer_data_persistence_allowed": False,
            "raw_secret_credential_persistence_allowed": False,
        },
        "execution_boundary": {
            "provider_executor_boundary_ref": "boundary:v1-g46:injected-executor",
            "provider_executor_injected": True,
            "direct_provider_sdk_used": False,
            "direct_network_code_used": False,
            "ambient_secret_lookup_performed": False,
            "credential_value_accessed": False,
            "fallback_allowed": False,
            "tool_execution_allowed": False,
            "consumer_repo_mutation_allowed": False,
            "connector_browser_network_file_device_robotics_physical_world_behavior_allowed": False,
        },
        "provider_executor_injected_confirmation": True,
        "no_direct_provider_sdk_confirmation": True,
        "no_direct_network_code_confirmation": True,
        "no_ambient_secret_lookup_confirmation": True,
        "no_credential_value_access_confirmation": True,
        "no_fallback_execution_confirmation": True,
        "no_raw_prompt_model_response_customer_data_persistence_confirmation": True,
    }
    request.update(overrides)
    return request


def _provider_result(**overrides: Any) -> dict[str, Any]:
    result = {
        "provider_call_id": "provider-call:v1-g46:fake:001",
        "output_ref": "audit-output:v1-g46:redacted-summary",
        "redacted_output_summary_ref": "output-summary:v1-g46:redacted",
        "finish_status": "completed",
        "usage_metadata": {
            "input_tokens": 11,
            "output_tokens": 7,
            "total_tokens": 18,
        },
    }
    result.update(overrides)
    return result


def test_v1_g46_fixture_records_approved_scope_and_boundaries() -> None:
    fixture = _load_fixture()

    assert fixture["packet_set_id"] == "v1_g46_live_provider_model_call_execution"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g46-live-provider-model-call-execution"
    assert fixture["operator_decision"] == "Approve-V1-G46"
    assert fixture["approved_scope"] == "live_provider_model_call_execution_slice"
    assert fixture["live_provider_model_call_execution_approved"] is True
    assert fixture["live_provider_model_call_execution_added"] is True
    assert fixture["provider_executor_invocation_added"] is True
    assert fixture["actual_model_request_dispatch_execution_added"] is True
    assert fixture["product_ready"] is False


def test_v1_g46_file_scope_is_exact() -> None:
    fixture = _load_fixture()

    assert fixture["approved_runtime_files_changed"] == [
        "lima/harness/v1_live_provider_model_call_execution.py",
        "lima/harness/__init__.py",
    ]
    assert set(fixture["approved_docs_tests_fixtures_changed"]) == {
        "docs/V1_G46_LIVE_PROVIDER_MODEL_CALL_EXECUTION.md",
        "docs/V1_G46_LIVE_PROVIDER_MODEL_CALL_EXECUTION_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g46_live_provider_model_call_execution.json",
        "tests/test_v1_g46_live_provider_model_call_execution.py",
        "tests/fixtures/runtime_extraction/v1_g22_final_public_api_freeze.json",
    }


def test_v1_g46_harness_all_exports_match_execution_fixture() -> None:
    fixture = _load_fixture()
    harness = importlib.import_module("lima.harness")
    expected_exports = fixture["post_refresh_harness_all_exports"]
    actual_exports = list(getattr(harness, "__all__"))

    assert actual_exports[: len(expected_exports)] == expected_exports


def test_v1_g46_existing_harness_exports_are_preserved() -> None:
    fixture = _load_fixture()
    harness = importlib.import_module("lima.harness")
    exports = set(getattr(harness, "__all__"))

    for symbol_name in fixture["previous_frozen_harness_exports"]:
        assert symbol_name in exports
        assert hasattr(harness, symbol_name), symbol_name

    assert fixture["existing_frozen_harness_exports_preserved"] is True
    assert fixture["existing_frozen_harness_exports_removed"] is False
    assert fixture["existing_frozen_harness_exports_renamed"] is False


def test_v1_g46_execution_symbols_are_public_harness_exports() -> None:
    fixture = _load_fixture()
    harness = importlib.import_module("lima.harness")
    exports = set(getattr(harness, "__all__"))

    assert fixture["added_harness_exports"] == [
        "V1LiveProviderModelCallExecutionError",
        "execute_v1_live_provider_model_call",
    ]
    for symbol_name in fixture["added_harness_exports"]:
        assert symbol_name in exports
        assert hasattr(harness, symbol_name), symbol_name


def test_v1_g46_g22_freeze_fixture_reflects_execution_exports() -> None:
    fixture = _load_fixture()
    g22 = _load_g22_fixture()
    expected_exports = fixture["post_refresh_harness_all_exports"]
    actual_exports = g22["public_subpackage_export_surfaces"]["lima.harness"]

    assert actual_exports[: len(expected_exports)] == expected_exports
    assert fixture["g22_final_public_api_freeze_fixture_refreshed"] is True


def test_v1_g46_g22_runtime_symbol_inventory_is_not_expanded() -> None:
    g22 = _load_g22_fixture()

    gates = {entry["gate"] for entry in g22["v1_runtime_symbol_surfaces"]}
    assert "V1-G46" not in gates


def test_v1_g46_executes_only_through_injected_provider_executor() -> None:
    calls: list[dict[str, Any]] = []

    def fake_executor(payload: Any) -> dict[str, Any]:
        assert isinstance(payload, dict)
        calls.append(dict(payload))
        return _provider_result()

    record = execute_v1_live_provider_model_call(_execution_request(), fake_executor)

    assert len(calls) == 1
    assert calls[0] == {
        'guardian_decision': {
            'decision_id': 'decision:v1-g44:001',
            'status': 'allow',
            'allowed': True,
            'requires_approval': False,
        },
        'guardian_decision_id': 'decision:v1-g44:001',
        "execution_id": "execution:v1-g46:001",
        "authority_id": "authority:v1-g44:001",
        "authority_record_hash": _authority_record()["record_hash"],
        "provider_id": "provider:openai:metadata-ref",
        "model_id": "model:gpt-class",
        "model_role": "primary",
        "provider_executor_ref": "provider-executor:v1-g46:fake-openai",
        "provider_request_ref": "provider-request:v1-g46:redacted:001",
        "redacted_prompt_ref": "prompt-ref:v1-g46:redacted-summary",
        "redacted_input_summary_ref": "input-summary:v1-g46:redacted",
        "redaction_policy_ref": "redaction-policy:v1-g46:sanitized",
        "audit_record_ref": "audit:v1-g46:live-provider-model-call-execution",
        "data_sensitivity": "internal",
        "budget_class": "medium",
        "estimated_cost_class": "low",
        "latency_tier": "interactive",
    }
    assert record["record_type"] == "v1_live_provider_model_call_execution"
    assert record["schema_version"] == "v1-g46-candidate"
    assert record["live_provider_model_call_execution_added"] is True
    assert record["provider_executor_invocation_added"] is True
    assert record["provider_executor_invoked"] is True
    assert record["actual_model_request_dispatch_execution_added"] is True
    assert record["model_request_dispatched"] is True
    assert record["provider_call_id"] == "provider-call:v1-g46:fake:001"
    assert record["provider_output_ref"] == "audit-output:v1-g46:redacted-summary"
    assert record["usage_metadata"] == {
        "input_tokens": 11,
        "output_tokens": 7,
        "total_tokens": 18,
    }


def test_v1_g46_execution_record_keeps_forbidden_boundaries_false() -> None:
    record = execute_v1_live_provider_model_call(
        _execution_request(),
        lambda payload: _provider_result(),
    )

    for key in (
        "direct_provider_sdk_added",
        "direct_provider_sdk_used",
        "direct_network_code_added",
        "direct_network_code_used",
        "network_call_performed_by_lima_harness",
        "provider_readiness_network_check_added",
        "token_guardian_live_routing_added",
        "secret_lookup_added",
        "credential_value_access_added",
        "credential_access_added",
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
        "raw_sensitive_content_persisted",
        "product_ready",
    ):
        assert record[key] is False


def test_v1_g46_records_are_deterministic_for_sanitized_fake_executor() -> None:
    first = execute_v1_live_provider_model_call(
        _execution_request(),
        lambda payload: _provider_result(),
    )
    second = execute_v1_live_provider_model_call(
        _execution_request(),
        lambda payload: _provider_result(),
    )

    assert first == second
    assert first["record_hash"] == second["record_hash"]


def test_v1_g46_output_does_not_emit_sensitive_values() -> None:
    record = execute_v1_live_provider_model_call(
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


def test_v1_g46_missing_authority_fails_closed() -> None:
    request = _execution_request()
    del request["authority_record"]

    with pytest.raises(V1LiveProviderModelCallExecutionError, match="authority_record"):
        execute_v1_live_provider_model_call(request, lambda payload: _provider_result())


def test_v1_g46_tampered_authority_hash_fails_closed() -> None:
    authority = _authority_record()
    authority["model_id"] = "model:tampered"

    with pytest.raises(V1LiveProviderModelCallExecutionError, match="record_hash"):
        execute_v1_live_provider_model_call(
            _execution_request(authority_record=authority),
            lambda payload: _provider_result(),
        )


def test_v1_g46_missing_provider_executor_fails_closed() -> None:
    with pytest.raises(V1LiveProviderModelCallExecutionError, match="provider_executor"):
        execute_v1_live_provider_model_call(_execution_request(), None)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("direct_provider_sdk_used", True, "forbidden behavior"),
        ("direct_network_code_used", True, "forbidden behavior"),
        ("ambient_secret_lookup_performed", True, "forbidden behavior"),
        ("credential_value_accessed", True, "forbidden behavior"),
        ("fallback_allowed", True, "forbidden behavior"),
        ("tool_execution_allowed", True, "forbidden behavior"),
        ("consumer_repo_mutation_allowed", True, "forbidden behavior"),
        (
            "connector_browser_network_file_device_robotics_physical_world_behavior_allowed",
            True,
            "forbidden behavior",
        ),
    ],
)
def test_v1_g46_execution_boundary_forbidden_flags_fail_closed(
    field: str,
    value: Any,
    match: str,
) -> None:
    boundary = dict(_execution_request()["execution_boundary"])
    boundary[field] = value

    with pytest.raises(V1LiveProviderModelCallExecutionError, match=match):
        execute_v1_live_provider_model_call(
            _execution_request(execution_boundary=boundary),
            lambda payload: _provider_result(),
        )


@pytest.mark.parametrize(
    "field",
    [
        "provider_executor_injected_confirmation",
        "no_direct_provider_sdk_confirmation",
        "no_direct_network_code_confirmation",
        "no_ambient_secret_lookup_confirmation",
        "no_credential_value_access_confirmation",
        "no_fallback_execution_confirmation",
        "no_raw_prompt_model_response_customer_data_persistence_confirmation",
    ],
)
def test_v1_g46_required_confirmations_fail_closed(field: str) -> None:
    with pytest.raises(V1LiveProviderModelCallExecutionError, match=field):
        execute_v1_live_provider_model_call(
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
def test_v1_g46_raw_sensitive_request_content_fails_closed(
    field: str,
    value: str,
) -> None:
    with pytest.raises(V1LiveProviderModelCallExecutionError, match="raw sensitive"):
        execute_v1_live_provider_model_call(
            _execution_request(**{field: value}),
            lambda payload: _provider_result(),
        )


def test_v1_g46_raw_sensitive_provider_result_fails_closed() -> None:
    with pytest.raises(V1LiveProviderModelCallExecutionError, match="raw sensitive"):
        execute_v1_live_provider_model_call(
            _execution_request(),
            lambda payload: _provider_result(raw_model_response="raw model response value"),
        )


def test_v1_g46_inconsistent_usage_metadata_fails_closed() -> None:
    with pytest.raises(V1LiveProviderModelCallExecutionError, match="total_tokens"):
        execute_v1_live_provider_model_call(
            _execution_request(),
            lambda payload: _provider_result(
                usage_metadata={
                    "input_tokens": 11,
                    "output_tokens": 7,
                    "total_tokens": 12,
                }
            ),
        )


def test_v1_g46_provider_executor_errors_are_wrapped() -> None:
    def failing_executor(payload: Any) -> dict[str, Any]:
        raise RuntimeError("provider failure")

    with pytest.raises(V1LiveProviderModelCallExecutionError, match="executor failed"):
        execute_v1_live_provider_model_call(_execution_request(), failing_executor)


@pytest.mark.parametrize(
    'guardian_decision',
    [
        None,
        {},
        {
            'decision_id': '',
            'status': 'allow',
            'allowed': True,
            'requires_approval': False,
        },
        {
            'decision_id': 'decision:v1-g44:001',
            'status': 'deny',
            'allowed': False,
            'requires_approval': False,
        },
        {
            'decision_id': 'decision:v1-g44:001',
            'status': 'approval_required',
            'allowed': False,
            'requires_approval': True,
        },
    ],
)
def test_v1_g46_invalid_guardian_decisions_fail_closed(
    guardian_decision: Any,
) -> None:
    calls = 0

    def fake_executor(payload: Any) -> dict[str, Any]:
        nonlocal calls
        calls += 1
        return _provider_result()

    with pytest.raises(V1LiveProviderModelCallExecutionError, match='Guardian|guardian'):
        execute_v1_live_provider_model_call(
            _execution_request(guardian_decision=guardian_decision),
            fake_executor,
        )

    assert calls == 0


def test_v1_g46_guardian_decision_id_is_preserved_end_to_end() -> None:
    observed_payload: dict[str, Any] = {}

    def fake_executor(payload: Any) -> dict[str, Any]:
        observed_payload.update(payload)
        return _provider_result()

    record = execute_v1_live_provider_model_call(_execution_request(), fake_executor)

    expected = 'decision:v1-g44:001'
    assert observed_payload['guardian_decision_id'] == expected
    assert observed_payload['guardian_decision']['decision_id'] == expected
    assert record['guardian_decision_id'] == expected
    assert record['guardian_decision']['decision_id'] == expected


def test_v1_g46_mismatched_guardian_lineage_fails_closed() -> None:
    with pytest.raises(V1LiveProviderModelCallExecutionError, match='does not match'):
        execute_v1_live_provider_model_call(
            _execution_request(
                guardian_decision={
                    'decision_id': 'guardian-decision:wrong',
                    'status': 'allow',
                    'allowed': True,
                    'requires_approval': False,
                }
            ),
            lambda payload: _provider_result(),
        )


def test_v1_g46_unsupported_executor_fails_closed() -> None:
    calls = 0

    def executor(payload: Any) -> dict[str, Any]:
        nonlocal calls
        calls += 1
        return _provider_result()

    with pytest.raises(V1LiveProviderModelCallExecutionError, match='unsupported executor'):
        execute_v1_live_provider_model_call(
            _execution_request(provider_executor_ref='provider-executor:network'),
            executor,
        )

    assert calls == 0


def test_v1_g46_runtime_source_has_no_direct_provider_or_network_clients() -> None:
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


def test_v1_g46_fixture_records_no_unapproved_consumer_or_external_changes() -> None:
    fixture = _load_fixture()

    for key in (
        "g44_authority_validator_weakened",
        "direct_provider_sdk_added",
        "direct_network_code_added",
        "ambient_environment_secret_lookup_added",
        "secret_lookup_added",
        "credential_value_access_added",
        "fallback_execution_added",
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
        "raw_diff_or_patch_persisted",
        "raw_file_content_persisted",
        "credential_or_secret_persisted",
    ):
        assert fixture[key] is False


def test_v1_g46_evidence_refs_exist() -> None:
    fixture = _load_fixture()

    for relative_path in fixture["accepted_evidence_refs"]:
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g46_rollback_metadata_is_local_and_reversible() -> None:
    rollback = _load_fixture()["rollback_metadata"]

    assert rollback["rollback_ref"] == "rollback:v1-g46:live-provider-model-call-execution"
    assert rollback["rollback_runtime_file_refs"] == [
        "lima/harness/v1_live_provider_model_call_execution.py",
        "lima/harness/__init__.py",
    ]
    assert rollback["consumer_repo_changes_required"] is False
    assert rollback["external_service_changes_required"] is False
    assert rollback["provider_configuration_changes_required"] is False
    assert rollback["credential_rotation_required"] is False


def test_v1_g46_required_fixture_confirmations_are_true() -> None:
    confirmations = _load_fixture()["required_confirmations"]

    assert confirmations["provider_executor_injected_confirmation"] is True
    assert confirmations["no_direct_provider_sdk_confirmation"] is True
    assert confirmations["no_direct_network_code_confirmation"] is True
    assert confirmations["no_ambient_secret_lookup_confirmation"] is True
    assert confirmations["no_credential_value_access_confirmation"] is True
    assert confirmations["no_fallback_execution_confirmation"] is True
    assert (
        confirmations[
            "no_raw_prompt_model_response_customer_data_persistence_confirmation"
        ]
        is True
    )
    assert confirmations["no_consumer_repo_mutation_confirmation"] is True
    assert confirmations["no_connector_browser_network_physical_world_confirmation"] is True
    assert confirmations["no_product_readiness_confirmation"] is True


def test_v1_g46_docs_contain_boundary_language() -> None:
    implementation_text = (
        REPO_ROOT / "docs" / "V1_G46_LIVE_PROVIDER_MODEL_CALL_EXECUTION.md"
    ).read_text(encoding="utf-8")
    closeout_text = (
        REPO_ROOT / "docs" / "V1_G46_LIVE_PROVIDER_MODEL_CALL_EXECUTION_CLOSEOUT.md"
    ).read_text(encoding="utf-8")

    assert "caller-injected provider executor" in implementation_text
    assert "No built-in provider SDK" in implementation_text
    assert "No Sparkbot or Arc-Bot-shell file" in implementation_text
    assert "Fallback execution added: no" in implementation_text
    assert "V1-G46 is complete" in closeout_text
    assert "No product-readiness or production-readiness claim" in closeout_text
