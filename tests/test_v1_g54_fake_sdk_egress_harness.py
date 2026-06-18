"""Tests for the approved V1-G54 fake SDK/fake-egress harness slice."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g54_fake_sdk_egress_harness.json"
)
G48_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g48_provider_credential_network_hardening.json"
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
G52_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g52_consumer_fake_executor_provider_invocation_smoke.json"
)
G53_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g53_provider_sdk_network_credential_authority.json"
)


class _TestLocalFakeSdkHarness:
    def call(self, request: dict[str, Any]) -> dict[str, Any]:
        assert request["provider_ref"] == "provider-ref:v1-g54:fake-only"
        return {
            "record_id": "test-record:v1-g54:fake-sdk",
            "executor": "test-module-local-fake-sdk",
            "execution_scope": "local_pytest_process_only",
            "request_record_ref": "fake-sdk-request:v1-g54:sanitized",
            "response_record_ref": "fake-sdk-response:v1-g54:sanitized",
            "result": "simulated_success_no_network",
            "raw_prompt_present": False,
            "raw_model_response_present": False,
            "raw_customer_data_present": False,
            "secret_present": False,
            "credential_value_present": False,
            "provider_token_present": False,
            "api_key_present": False,
            "network_call_performed": False,
            "provider_egress_performed": False,
        }


class _TestLocalFakeEgressHarness:
    def evaluate(self, request: dict[str, Any]) -> dict[str, Any]:
        assert request["network_scope"] == "fake-egress-only"
        return {
            "record_id": "test-record:v1-g54:fake-egress",
            "executor": "test-module-local-fake-egress",
            "execution_scope": "local_pytest_process_only",
            "allow_record_ref": "fake-egress-allow:v1-g54:sanitized",
            "deny_record_ref": "fake-egress-deny:v1-g54:sanitized",
            "result": "simulated_denied_no_network",
            "deny_reason": "network_egress_execution_unapproved",
            "endpoint_resolution_performed": False,
            "dns_lookup_performed": False,
            "http_client_used": False,
            "socket_client_used": False,
            "network_call_performed": False,
            "provider_egress_performed": False,
            "provider_configuration_changed": False,
        }


def _load_json(path: Path) -> dict[str, Any]:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _load_fixture() -> dict[str, Any]:
    return _load_json(FIXTURE_PATH)


def _candidate_metadata() -> dict[str, Any]:
    fixture = _load_fixture()
    return {
        "fake_sdk_harness_evidence": copy.deepcopy(
            fixture["fake_sdk_harness_evidence"]
        ),
        "fake_egress_harness_evidence": copy.deepcopy(
            fixture["fake_egress_harness_evidence"]
        ),
        "harness_execution_records": copy.deepcopy(
            fixture["harness_execution_records"]
        ),
        "authority_chain_linkage": copy.deepcopy(fixture["authority_chain_linkage"]),
        "redaction_and_audit_policy": copy.deepcopy(
            fixture["redaction_and_audit_policy"]
        ),
    }


def _assert_harness_metadata_is_allowed(metadata: dict[str, Any]) -> None:
    sdk = metadata["fake_sdk_harness_evidence"]
    egress = metadata["fake_egress_harness_evidence"]
    records = metadata["harness_execution_records"]
    chain = metadata["authority_chain_linkage"]
    audit = metadata["redaction_and_audit_policy"]

    assert sdk["test_only"] is True
    assert sdk["docs_tests_fixtures_only"] is True
    assert sdk["test_module_local_only"] is True
    assert sdk["in_process_only"] is True
    assert sdk["deterministic"] is True
    assert sdk["sanitized_evidence_only"] is True
    for key in (
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
        assert sdk[key] is False, key

    assert egress["test_only"] is True
    assert egress["docs_tests_fixtures_only"] is True
    assert egress["test_module_local_only"] is True
    assert egress["in_process_only"] is True
    assert egress["deterministic"] is True
    assert egress["sanitized_evidence_only"] is True
    assert egress["deny_by_default"] is True
    assert egress["network_simulation_only"] is True
    for key in (
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
        assert egress[key] is False, key

    fake_sdk_record = records["fake_sdk_test_record"]
    assert fake_sdk_record["execution_scope"] == "local_pytest_process_only"
    for key in (
        "raw_prompt_present",
        "raw_model_response_present",
        "raw_customer_data_present",
        "secret_present",
        "credential_value_present",
        "provider_token_present",
        "api_key_present",
        "network_call_performed",
        "provider_egress_performed",
    ):
        assert fake_sdk_record[key] is False, key

    fake_egress_record = records["fake_egress_test_record"]
    assert fake_egress_record["execution_scope"] == "local_pytest_process_only"
    assert fake_egress_record["deny_reason"] == "network_egress_execution_unapproved"
    for key in (
        "endpoint_resolution_performed",
        "dns_lookup_performed",
        "http_client_used",
        "socket_client_used",
        "network_call_performed",
        "provider_egress_performed",
        "provider_configuration_changed",
    ):
        assert fake_egress_record[key] is False, key

    assert chain["authority_records_metadata_only"] is True
    assert chain["guardian_gate_required"] is True
    assert chain["no_runtime_enforcement_added"] is True
    assert chain["no_public_api_change_required"] is True
    assert chain["credential_reference_only"] is True
    assert chain["network_policy_reference_only"] is True
    assert chain["deny_by_default_network_required"] is True
    assert chain["test_module_local_fake_harness_only"] is True
    for key in (
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
        assert chain[key] is False, key

    assert audit["audit_required"] is True
    assert audit["sanitized_evidence_only"] is True
    assert audit["redacted_input_required"] is True
    assert audit["redacted_output_required"] is True
    assert audit["fake_records_must_be_metadata_only"] is True
    for key in (
        "raw_prompt_persistence_allowed",
        "raw_model_response_persistence_allowed",
        "raw_customer_data_persistence_allowed",
        "raw_secret_credential_persistence_allowed",
        "raw_provider_token_api_key_persistence_allowed",
        "raw_diff_patch_file_content_persistence_allowed",
    ):
        assert audit[key] is False, key


def test_v1_g54_fixture_records_approved_scope_and_status() -> None:
    fixture = _load_fixture()

    assert fixture["packet_set_id"] == "v1_g54_fake_sdk_egress_harness"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g54-fake-sdk-egress-harness"
    assert fixture["operator_decision"] == "Approve-V1-G54"
    assert fixture["approved_scope"] == "fake_sdk_egress_harness_evidence_slice"
    assert fixture["fake_sdk_egress_harness_approved"] is True
    assert fixture["fake_sdk_egress_harness_added"] is True
    assert fixture["fake_sdk_harness_evidence_added"] is True
    assert fixture["fake_egress_harness_evidence_added"] is True
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["product_ready"] is False
    assert fixture["production_ready"] is False


def test_v1_g54_file_scope_is_exact_and_runtime_unchanged() -> None:
    fixture = _load_fixture()

    assert fixture["approved_lima_runtime_files_changed"] == []
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["lima_public_api_changed"] is False
    assert fixture["approved_lima_docs_tests_fixtures_changed"] == [
        "docs/V1_G54_FAKE_SDK_EGRESS_HARNESS.md",
        "docs/V1_G54_FAKE_SDK_EGRESS_HARNESS_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g54_fake_sdk_egress_harness.json",
        "tests/test_v1_g54_fake_sdk_egress_harness.py",
    ]
    for relative_path in fixture["approved_lima_docs_tests_fixtures_changed"]:
        assert (REPO_ROOT / relative_path).exists()
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["arc_bot_shell_files_changed"] is False


def test_v1_g54_fake_sdk_harness_evidence_is_test_local() -> None:
    sdk = _load_fixture()["fake_sdk_harness_evidence"]

    assert sdk["harness_id"] == "fake-sdk-harness:v1-g54:in-process-only"
    assert sdk["authority_type"] == "fake_sdk_harness_evidence"
    assert sdk["test_only"] is True
    assert sdk["docs_tests_fixtures_only"] is True
    assert sdk["test_module_local_only"] is True
    assert sdk["in_process_only"] is True
    assert sdk["fake_request_record_ref"] == "fake-sdk-request:v1-g54:sanitized"
    assert sdk["fake_response_record_ref"] == "fake-sdk-response:v1-g54:sanitized"
    assert sdk["real_sdk_client_used"] is False
    assert sdk["sdk_dependency_added"] is False
    assert sdk["sdk_call_performed"] is False
    assert sdk["network_call_performed"] is False


def test_v1_g54_fake_egress_harness_evidence_is_deny_by_default() -> None:
    egress = _load_fixture()["fake_egress_harness_evidence"]

    assert egress["harness_id"] == "fake-egress-harness:v1-g54:in-process-only"
    assert egress["authority_type"] == "fake_egress_harness_evidence"
    assert egress["test_only"] is True
    assert egress["docs_tests_fixtures_only"] is True
    assert egress["test_module_local_only"] is True
    assert egress["in_process_only"] is True
    assert egress["deny_by_default"] is True
    assert egress["network_simulation_only"] is True
    assert egress["fake_allow_record_ref"] == "fake-egress-allow:v1-g54:sanitized"
    assert egress["fake_deny_record_ref"] == "fake-egress-deny:v1-g54:sanitized"
    assert egress["provider_endpoint_resolution_performed"] is False
    assert egress["dns_lookup_performed"] is False
    assert egress["http_client_used"] is False
    assert egress["socket_client_used"] is False
    assert egress["network_call_performed"] is False
    assert egress["direct_provider_egress_performed"] is False


def test_v1_g54_test_local_fake_sdk_component_returns_sanitized_record() -> None:
    result = _TestLocalFakeSdkHarness().call(
        {
            "provider_ref": "provider-ref:v1-g54:fake-only",
            "request_record_ref": "fake-sdk-request:v1-g54:sanitized",
            "redacted_input_ref": "redacted-input:v1-g54:fake-sdk",
        }
    )

    assert result == _load_fixture()["harness_execution_records"][
        "fake_sdk_test_record"
    ]


def test_v1_g54_test_local_fake_egress_component_denies_without_network() -> None:
    result = _TestLocalFakeEgressHarness().evaluate(
        {
            "network_scope": "fake-egress-only",
            "allow_record_ref": "fake-egress-allow:v1-g54:sanitized",
            "deny_record_ref": "fake-egress-deny:v1-g54:sanitized",
        }
    )

    assert result == _load_fixture()["harness_execution_records"][
        "fake_egress_test_record"
    ]


def test_v1_g54_authority_chain_links_prior_evidence_by_reference() -> None:
    chain = _load_fixture()["authority_chain_linkage"]
    g48 = _load_json(G48_FIXTURE_PATH)
    g50 = _load_json(G50_FIXTURE_PATH)
    g51 = _load_json(G51_FIXTURE_PATH)
    g52 = _load_json(G52_FIXTURE_PATH)
    g53 = _load_json(G53_FIXTURE_PATH)

    assert chain["credential_policy_ref"] == g48["credential_reference_policy"][
        "policy_id"
    ]
    assert chain["network_policy_ref"] == g48["provider_network_policy"][
        "policy_id"
    ]
    assert chain["invocation_request_ref"] == g50["invocation_request_envelope"][
        "invocation_request_id"
    ]
    assert chain["execution_wrapper_boundary_ref"] == g51["execution_boundary"][
        "provider_executor_boundary_ref"
    ]
    assert chain["consumer_fake_executor_smoke_ref"].startswith(
        "consumer-fake-executor-smoke:v1-g52"
    )
    assert chain["provider_sdk_authority_ref"] == g53[
        "provider_sdk_authority_metadata"
    ]["provider_sdk_authority_id"]
    assert chain["endpoint_resolution_authority_ref"] == g53[
        "endpoint_resolution_authority_metadata"
    ]["endpoint_resolution_authority_id"]
    assert chain["provider_network_egress_authority_ref"] == g53[
        "provider_network_egress_authority_metadata"
    ]["network_egress_authority_id"]
    assert chain["credential_reference_authority_ref"] == g53[
        "credential_reference_authority_metadata"
    ]["credential_authority_id"]
    assert chain["fake_sdk_harness_ref"] == "fake-sdk-harness:v1-g54:in-process-only"
    assert chain["fake_egress_harness_ref"] == (
        "fake-egress-harness:v1-g54:in-process-only"
    )


def test_v1_g54_redaction_and_audit_policy_is_sanitized() -> None:
    audit = _load_fixture()["redaction_and_audit_policy"]

    assert audit["harness_evidence_ref"] == (
        "evidence:v1-g54:fake-sdk-egress-harness"
    )
    assert audit["fake_sdk_harness_evidence_ref"] == (
        "evidence:v1-g54:fake-sdk-harness"
    )
    assert audit["fake_egress_harness_evidence_ref"] == (
        "evidence:v1-g54:fake-egress-harness"
    )
    assert audit["audit_record_ref"] == "audit:v1-g54:fake-sdk-egress-harness"
    assert audit["audit_required"] is True
    assert audit["sanitized_evidence_only"] is True
    assert audit["redacted_input_required"] is True
    assert audit["redacted_output_required"] is True
    assert audit["fake_records_must_be_metadata_only"] is True
    assert audit["raw_prompt_persistence_allowed"] is False
    assert audit["raw_model_response_persistence_allowed"] is False
    assert audit["raw_customer_data_persistence_allowed"] is False
    assert audit["raw_secret_credential_persistence_allowed"] is False
    assert audit["raw_provider_token_api_key_persistence_allowed"] is False
    assert audit["raw_diff_patch_file_content_persistence_allowed"] is False


def test_v1_g54_allowed_metadata_passes_local_fail_closed_checks() -> None:
    _assert_harness_metadata_is_allowed(_candidate_metadata())


@pytest.mark.parametrize(
    ("section", "field"),
    [
        ("fake_sdk_harness_evidence", "real_sdk_client_used"),
        ("fake_sdk_harness_evidence", "built_in_provider_sdk_client_used"),
        ("fake_sdk_harness_evidence", "direct_provider_sdk_implementation_used"),
        ("fake_sdk_harness_evidence", "sdk_dependency_added"),
        ("fake_sdk_harness_evidence", "sdk_client_constructed"),
        ("fake_sdk_harness_evidence", "sdk_call_performed"),
        ("fake_sdk_harness_evidence", "provider_endpoint_resolution_performed"),
        ("fake_sdk_harness_evidence", "network_calls_allowed"),
        ("fake_sdk_harness_evidence", "network_call_performed"),
        ("fake_sdk_harness_evidence", "credential_value_access_allowed"),
        ("fake_sdk_harness_evidence", "provider_token_or_api_key_access_allowed"),
        ("fake_sdk_harness_evidence", "fallback_execution_allowed"),
        (
            "fake_sdk_harness_evidence",
            "consumer_production_runtime_integration_allowed",
        ),
        ("fake_sdk_harness_evidence", "product_readiness_claim_allowed"),
        ("fake_egress_harness_evidence", "endpoint_resolution_execution_allowed"),
        ("fake_egress_harness_evidence", "provider_endpoint_resolution_performed"),
        ("fake_egress_harness_evidence", "dns_lookup_allowed"),
        ("fake_egress_harness_evidence", "dns_lookup_performed"),
        ("fake_egress_harness_evidence", "http_client_allowed"),
        ("fake_egress_harness_evidence", "http_client_used"),
        ("fake_egress_harness_evidence", "socket_client_allowed"),
        ("fake_egress_harness_evidence", "socket_client_used"),
        ("fake_egress_harness_evidence", "network_calls_allowed"),
        ("fake_egress_harness_evidence", "network_call_performed"),
        ("fake_egress_harness_evidence", "direct_provider_egress_allowed"),
        ("fake_egress_harness_evidence", "direct_provider_egress_performed"),
        (
            "fake_egress_harness_evidence",
            "provider_readiness_network_check_allowed",
        ),
        ("fake_egress_harness_evidence", "provider_configuration_change_allowed"),
        ("fake_egress_harness_evidence", "fallback_execution_allowed"),
        (
            "fake_egress_harness_evidence",
            "consumer_production_runtime_integration_allowed",
        ),
        ("fake_egress_harness_evidence", "product_readiness_claim_allowed"),
        ("authority_chain_linkage", "provider_sdk_client_allowed"),
        ("authority_chain_linkage", "sdk_dependency_allowed"),
        ("authority_chain_linkage", "direct_provider_sdk_implementation_allowed"),
        ("authority_chain_linkage", "endpoint_resolution_execution_allowed"),
        ("authority_chain_linkage", "network_egress_execution_allowed"),
        ("authority_chain_linkage", "secret_lookup_allowed"),
        ("authority_chain_linkage", "credential_value_access_allowed"),
        ("authority_chain_linkage", "provider_token_or_api_key_access_allowed"),
        ("authority_chain_linkage", "provider_configuration_change_allowed"),
        ("authority_chain_linkage", "fallback_execution_allowed"),
        ("authority_chain_linkage", "consumer_production_runtime_integration_allowed"),
        ("authority_chain_linkage", "connector_browser_network_physical_world_allowed"),
        ("authority_chain_linkage", "product_readiness_claim_allowed"),
    ],
)
def test_v1_g54_forbidden_metadata_claims_fail_closed(
    section: str,
    field: str,
) -> None:
    metadata = _candidate_metadata()
    metadata[section][field] = True

    with pytest.raises(AssertionError, match=field):
        _assert_harness_metadata_is_allowed(metadata)


def test_v1_g54_top_level_forbidden_boundaries_remain_false() -> None:
    fixture = _load_fixture()

    for key in (
        "consumer_repo_mutation_added",
        "consumer_runtime_calls_added",
        "consumer_production_runtime_integration_added",
        "live_provider_model_call_execution_added",
        "provider_executor_invocation_added",
        "provider_executor_invoked",
        "real_provider_executor_invocation_added",
        "real_provider_executor_invoked",
        "fake_provider_executor_invocation_added",
        "fake_provider_executor_invoked",
        "actual_model_request_dispatch_execution_added",
        "model_request_dispatched",
        "built_in_provider_sdk_client_added",
        "built_in_provider_sdk_used",
        "real_provider_sdk_client_added",
        "real_provider_sdk_client_used",
        "direct_provider_sdk_added",
        "direct_provider_sdk_used",
        "sdk_dependency_added",
        "sdk_dependency_used",
        "provider_endpoint_resolution_added",
        "provider_endpoint_resolution_performed",
        "direct_network_code_added",
        "direct_network_code_used",
        "dns_lookup_added",
        "dns_lookup_performed",
        "http_client_added",
        "http_client_used",
        "socket_client_added",
        "socket_client_used",
        "network_call_performed",
        "network_call_performed_by_lima_harness",
        "direct_provider_egress_added",
        "direct_provider_egress_performed",
        "provider_readiness_network_check_added",
        "provider_readiness_network_check_performed",
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
        "token_guardian_live_routing_added",
        "tool_execution_added",
        "tool_execution_outside_local_tests_added",
        "action_execution_added",
        "action_execution_outside_local_fake_harness_tests_added",
        "connector_browser_network_file_device_robotics_physical_world_behavior_added",
        "scheduled_task_execution_added",
        "external_send_added",
        "external_database_write_added",
        "migration_added",
        "queue_worker_daemon_background_service_subprocess_thread_added",
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
    assert fixture["test_module_local_fake_components_only"] is True
    assert fixture["in_process_fake_components_only"] is True


def test_v1_g54_prior_evidence_refs_exist() -> None:
    fixture = _load_fixture()

    for relative_path in fixture["required_prior_evidence_refs"]:
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g54_future_gates_remain_blocked() -> None:
    fixture = _load_fixture()

    assert fixture["future_required_gates"] == [
        "v1_g54_fake_sdk_egress_harness_audit",
        "v1_runtime_authority_chain_audit_through_g54",
        "readiness_next_lane_metadata_refresh_through_g54",
        "real_provider_sdk_network_egress_implementation_approval_request",
        "credential_value_access_approval_request",
        "fallback_execution_approval_request",
        "connector_browser_network_authority_approval_request",
        "consumer_production_runtime_integration_approval_request",
        "physical_world_authority_approval_request",
        "product_readiness_approval_request",
    ]
    assert fixture["blocked_future_authorities"] == {
        "real_provider_sdk_client_approved": False,
        "built_in_provider_sdk_client_approved": False,
        "sdk_dependency_approved": False,
        "direct_provider_sdk_implementation_approved": False,
        "provider_endpoint_resolution_execution_approved": False,
        "provider_network_egress_execution_approved": False,
        "dns_http_socket_network_call_approved": False,
        "direct_provider_egress_approved": False,
        "provider_secret_lookup_approved": False,
        "provider_credential_value_access_approved": False,
        "provider_token_or_api_key_access_approved": False,
        "provider_configuration_change_approved": False,
        "fallback_execution_approved": False,
        "connector_browser_network_authority_approved": False,
        "consumer_production_runtime_integration_approved": False,
        "physical_world_authority_approved": False,
        "product_readiness_approved": False,
    }


def test_v1_g54_required_confirmations_are_true() -> None:
    confirmations = _load_fixture()["required_confirmations"]

    assert all(confirmations.values())
    assert confirmations["fake_sdk_egress_harness_evidence_confirmation"] is True
    assert confirmations["test_module_local_fake_components_only_confirmation"] is True
    assert confirmations["in_process_fake_components_only_confirmation"] is True
    assert confirmations["v1_g53_provider_sdk_network_credential_authority_linkage_confirmation"] is True
    assert confirmations["no_real_provider_sdk_client_confirmation"] is True
    assert confirmations["no_sdk_dependency_confirmation"] is True
    assert confirmations["no_provider_endpoint_resolution_execution_confirmation"] is True
    assert confirmations["no_dns_http_socket_network_call_confirmation"] is True
    assert confirmations["no_provider_egress_confirmation"] is True
    assert confirmations["proof_not_product_readiness_confirmation"] is True


def test_v1_g54_lima_validation_results_are_recorded() -> None:
    validation = _load_fixture()["lima_validation_results"]

    assert validation["focused_v1_g54_validation"]["passed"] is True
    assert validation["focused_v1_g54_validation"]["tests_passed"] == 59
    assert (
        validation["focused_v1_g54_g53_g52_g51_g50_g48_g22_validation"]["passed"]
        is True
    )
    assert (
        validation["focused_v1_g54_g53_g52_g51_g50_g48_g22_validation"][
            "tests_passed"
        ]
        == 295
    )
    assert validation["compileall_lima"] == {
        "command": "python -m compileall lima",
        "passed": True,
    }
    assert validation["full_lima_suite"]["passed"] is True
    assert validation["full_lima_suite"]["tests_passed"] == 4658


def test_v1_g54_fixture_and_docs_do_not_include_sensitive_markers() -> None:
    output = json.dumps(_load_fixture(), sort_keys=True)
    output += (
        REPO_ROOT / "docs" / "V1_G54_FAKE_SDK_EGRESS_HARNESS.md"
    ).read_text(encoding="utf-8")
    output += (
        REPO_ROOT / "docs" / "V1_G54_FAKE_SDK_EGRESS_HARNESS_CLOSEOUT.md"
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
