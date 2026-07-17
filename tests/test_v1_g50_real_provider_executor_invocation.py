"""Tests for the approved V1-G50 real provider executor invocation metadata slice."""

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
    / "v1_g50_real_provider_executor_invocation.json"
)
G49_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g49_real_provider_executor.json"
)
G48_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g48_provider_credential_network_hardening.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _load_g49_fixture() -> dict[str, Any]:
    fixture = json.loads(G49_FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _load_g48_fixture() -> dict[str, Any]:
    fixture = json.loads(G48_FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _candidate_metadata() -> dict[str, Any]:
    fixture = _load_fixture()
    return {
        "invocation_request_envelope": copy.deepcopy(
            fixture["invocation_request_envelope"]
        ),
        "invocation_response_envelope": copy.deepcopy(
            fixture["invocation_response_envelope"]
        ),
        "provider_model_scope": copy.deepcopy(fixture["provider_model_scope"]),
        "executor_authority_linkage": copy.deepcopy(
            fixture["executor_authority_linkage"]
        ),
        "credential_network_hardening_linkage": copy.deepcopy(
            fixture["credential_network_hardening_linkage"]
        ),
        "execution_boundary_metadata": copy.deepcopy(
            fixture["execution_boundary_metadata"]
        ),
        "redaction_and_audit_policy": copy.deepcopy(
            fixture["redaction_and_audit_policy"]
        ),
    }


def _assert_invocation_metadata_is_allowed(metadata: dict[str, Any]) -> None:
    request = metadata["invocation_request_envelope"]
    response = metadata["invocation_response_envelope"]
    scope = metadata["provider_model_scope"]
    authority = metadata["executor_authority_linkage"]
    linkage = metadata["credential_network_hardening_linkage"]
    boundary = metadata["execution_boundary_metadata"]
    audit = metadata["redaction_and_audit_policy"]

    assert request["metadata_only"] is True
    assert request["non_executing"] is True
    assert request["proof_not_execution"] is True
    assert request["guardian_gate_required"] is True
    for key in (
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
        assert request[key] is False, key

    assert response["metadata_only"] is True
    assert response["non_executing"] is True
    assert response["proof_not_execution"] is True
    assert response["sanitized_evidence_only"] is True
    assert response["invocation_status"] == "not_invoked"
    for key in (
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
        assert response[key] is False, key

    assert scope["reference_only"] is True
    assert scope["metadata_only"] is True
    for key in (
        "provider_configuration_changed",
        "provider_endpoint_selected",
        "model_invocation_selected",
        "executable_invocation_selected",
    ):
        assert scope[key] is False, key

    assert authority["reference_only"] is True
    assert authority["metadata_only"] is True
    assert authority["executor_authority_design_required"] is True
    for key in (
        "executor_invocation_allowed",
        "real_provider_executor_invocation_allowed",
        "fake_provider_executor_invocation_allowed",
        "executable_provider_invocation_allowed",
    ):
        assert authority[key] is False, key

    assert linkage["credential_reference_only"] is True
    assert linkage["network_policy_reference_only"] is True
    assert linkage["deny_by_default_network_required"] is True
    for key in (
        "secret_lookup_allowed",
        "credential_value_access_allowed",
        "provider_token_or_api_key_access_allowed",
        "provider_endpoint_resolution_allowed",
        "network_calls_allowed",
        "direct_provider_egress_allowed",
    ):
        assert linkage[key] is False, key

    assert boundary["estimated_cost_only"] is True
    assert boundary["metadata_only"] is True
    assert boundary["non_executing"] is True
    assert boundary["max_attempts_metadata"] == 1
    for key in (
        "provider_executor_call_allowed",
        "retry_execution_allowed",
        "timeout_enforcement_runtime_added",
        "billing_call_allowed",
        "cost_meter_network_call_allowed",
        "provider_readiness_network_check_allowed",
        "fallback_execution_allowed",
        "error_payload_raw_persistence_allowed",
    ):
        assert boundary[key] is False, key

    assert audit["audit_required"] is True
    assert audit["sanitized_evidence_only"] is True
    assert audit["redacted_input_required"] is True
    assert audit["redacted_output_required"] is True
    for key in (
        "raw_prompt_persistence_allowed",
        "raw_model_response_persistence_allowed",
        "raw_customer_data_persistence_allowed",
        "raw_secret_credential_persistence_allowed",
        "raw_diff_patch_file_content_persistence_allowed",
    ):
        assert audit[key] is False, key


def test_v1_g50_fixture_records_approved_scope_and_status() -> None:
    fixture = _load_fixture()

    assert fixture["packet_set_id"] == "v1_g50_real_provider_executor_invocation"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g50-real-provider-executor-invocation"
    assert fixture["operator_decision"] == "Approve-V1-G50"
    assert fixture["approved_scope"] == (
        "real_provider_executor_invocation_metadata_slice"
    )
    assert fixture["real_provider_executor_invocation_metadata_approved"] is True
    assert fixture["real_provider_executor_invocation_metadata_added"] is True
    assert fixture["executable_provider_invocation_approved"] is False
    assert fixture["executable_provider_invocation_added"] is False
    assert fixture["product_ready"] is False


def test_v1_g50_file_scope_is_exact_and_runtime_unchanged() -> None:
    fixture = _load_fixture()

    assert fixture["approved_lima_runtime_files_changed"] == []
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["lima_public_api_changed"] is False
    assert fixture["approved_lima_docs_tests_fixtures_changed"] == [
        "docs/V1_G50_REAL_PROVIDER_EXECUTOR_INVOCATION.md",
        "docs/V1_G50_REAL_PROVIDER_EXECUTOR_INVOCATION_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g50_real_provider_executor_invocation.json",
        "tests/test_v1_g50_real_provider_executor_invocation.py",
    ]
    for relative_path in fixture["approved_lima_docs_tests_fixtures_changed"]:
        assert (REPO_ROOT / relative_path).exists()
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["arc_bot_shell_files_changed"] is False


def test_v1_g50_invocation_request_envelope_is_non_executing() -> None:
    request = _load_fixture()["invocation_request_envelope"]

    assert request["invocation_request_id"] == (
        "real-provider-executor-invocation-request:v1-g50:metadata-only"
    )
    assert request["envelope_type"] == (
        "real_provider_executor_invocation_request_metadata"
    )
    assert request["metadata_only"] is True
    assert request["non_executing"] is True
    assert request["proof_not_execution"] is True
    assert request["guardian_gate_required"] is True
    assert request["provider_executor_invocation_allowed"] is False
    assert request["real_provider_executor_invocation_allowed"] is False
    assert request["fake_provider_executor_invocation_allowed"] is False
    assert request["executable_provider_invocation_allowed"] is False
    assert request["model_request_dispatch_allowed"] is False
    assert request["provider_sdk_client_allowed"] is False
    assert request["provider_endpoint_resolution_allowed"] is False
    assert request["network_calls_allowed"] is False
    assert request["secret_lookup_allowed"] is False
    assert request["credential_value_access_allowed"] is False
    assert request["fallback_execution_allowed"] is False


def test_v1_g50_invocation_response_envelope_is_non_executing() -> None:
    response = _load_fixture()["invocation_response_envelope"]

    assert response["invocation_response_id"] == (
        "real-provider-executor-invocation-response:v1-g50:metadata-only"
    )
    assert response["envelope_type"] == (
        "real_provider_executor_invocation_response_metadata"
    )
    assert response["metadata_only"] is True
    assert response["non_executing"] is True
    assert response["proof_not_execution"] is True
    assert response["invocation_status"] == "not_invoked"
    assert response["sanitized_evidence_only"] is True
    assert response["provider_executor_invoked"] is False
    assert response["real_provider_executor_invoked"] is False
    assert response["fake_provider_executor_invoked"] is False
    assert response["model_response_received"] is False
    assert response["network_call_performed"] is False
    assert response["provider_sdk_client_used"] is False
    assert response["provider_endpoint_resolved"] is False
    assert response["secret_lookup_performed"] is False
    assert response["credential_value_accessed"] is False
    assert response["fallback_execution_performed"] is False


def test_v1_g50_provider_model_scope_is_reference_only_from_g49() -> None:
    scope = _load_fixture()["provider_model_scope"]
    g49_scope = _load_g49_fixture()["provider_model_scope"]

    assert scope["provider_scope_ref"] == g49_scope["provider_scope_ref"]
    assert scope["model_scope_ref"] == g49_scope["model_scope_ref"]
    assert scope["route_authority_ref"] == g49_scope["route_authority_ref"]
    assert scope["dispatch_evidence_ref"] == g49_scope["dispatch_evidence_ref"]
    assert scope["executor_authority_ref"] == (
        _load_g49_fixture()["executor_authority_metadata"]["executor_authority_id"]
    )
    assert scope["reference_only"] is True
    assert scope["metadata_only"] is True
    assert scope["provider_configuration_changed"] is False
    assert scope["provider_endpoint_selected"] is False
    assert scope["model_invocation_selected"] is False
    assert scope["executable_invocation_selected"] is False


def test_v1_g50_links_to_v1_g49_authority_by_reference() -> None:
    authority = _load_fixture()["executor_authority_linkage"]
    g49 = _load_g49_fixture()

    assert authority["v1_g49_fixture_ref"] == (
        "tests/fixtures/runtime_extraction/v1_g49_real_provider_executor.json"
    )
    assert authority["executor_authority_ref"] == (
        g49["executor_authority_metadata"]["executor_authority_id"]
    )
    assert authority["executor_authority_evidence_ref"] == (
        g49["redaction_and_audit_policy"]["executor_authority_evidence_ref"]
    )
    assert authority["reference_only"] is True
    assert authority["metadata_only"] is True
    assert authority["executor_invocation_allowed"] is False
    assert authority["executable_provider_invocation_allowed"] is False


def test_v1_g50_links_to_v1_g48_hardening_by_reference() -> None:
    linkage = _load_fixture()["credential_network_hardening_linkage"]
    g48 = _load_g48_fixture()

    assert linkage["v1_g48_fixture_ref"] == (
        "tests/fixtures/runtime_extraction/"
        "v1_g48_provider_credential_network_hardening.json"
    )
    assert linkage["credential_policy_ref"] == g48["credential_reference_policy"][
        "policy_id"
    ]
    assert linkage["network_policy_ref"] == g48["provider_network_policy"]["policy_id"]
    assert linkage["credential_reference_only"] is True
    assert linkage["network_policy_reference_only"] is True
    assert linkage["deny_by_default_network_required"] is True
    assert linkage["secret_lookup_allowed"] is False
    assert linkage["credential_value_access_allowed"] is False
    assert linkage["provider_endpoint_resolution_allowed"] is False
    assert linkage["network_calls_allowed"] is False
    assert linkage["direct_provider_egress_allowed"] is False


def test_v1_g50_execution_boundary_metadata_is_non_executing() -> None:
    boundary = _load_fixture()["execution_boundary_metadata"]

    assert boundary["timeout_policy_ref"] == "timeout-policy:v1-g50:metadata-only"
    assert boundary["retry_policy_ref"] == "retry-policy:v1-g50:no-execution"
    assert boundary["cost_policy_ref"] == "cost-policy:v1-g50:metadata-only"
    assert boundary["failure_policy_ref"] == "failure-policy:v1-g50:fail-closed"
    assert boundary["estimated_cost_only"] is True
    assert boundary["metadata_only"] is True
    assert boundary["non_executing"] is True
    assert boundary["max_attempts_metadata"] == 1
    assert boundary["provider_executor_call_allowed"] is False
    assert boundary["retry_execution_allowed"] is False
    assert boundary["timeout_enforcement_runtime_added"] is False
    assert boundary["billing_call_allowed"] is False
    assert boundary["cost_meter_network_call_allowed"] is False
    assert boundary["provider_readiness_network_check_allowed"] is False
    assert boundary["fallback_execution_allowed"] is False
    assert boundary["error_payload_raw_persistence_allowed"] is False


def test_v1_g50_redaction_and_audit_policy_is_sanitized() -> None:
    audit = _load_fixture()["redaction_and_audit_policy"]

    assert audit["invocation_request_evidence_ref"] == (
        "evidence:v1-g50:invocation-request-envelope-metadata"
    )
    assert audit["invocation_response_evidence_ref"] == (
        "evidence:v1-g50:invocation-response-envelope-metadata"
    )
    assert audit["executor_authority_evidence_ref"] == (
        "evidence:v1-g49:real-provider-executor-authority-design"
    )
    assert audit["audit_record_ref"] == (
        "audit:v1-g50:real-provider-executor-invocation-metadata"
    )
    assert audit["audit_required"] is True
    assert audit["sanitized_evidence_only"] is True
    assert audit["redacted_input_required"] is True
    assert audit["redacted_output_required"] is True
    assert audit["raw_prompt_persistence_allowed"] is False
    assert audit["raw_model_response_persistence_allowed"] is False
    assert audit["raw_customer_data_persistence_allowed"] is False
    assert audit["raw_secret_credential_persistence_allowed"] is False
    assert audit["raw_diff_patch_file_content_persistence_allowed"] is False


def test_v1_g50_allowed_metadata_passes_local_fail_closed_checks() -> None:
    _assert_invocation_metadata_is_allowed(_candidate_metadata())


@pytest.mark.parametrize(
    ("section", "field"),
    [
        ("invocation_request_envelope", "provider_executor_invocation_allowed"),
        ("invocation_request_envelope", "real_provider_executor_invocation_allowed"),
        ("invocation_request_envelope", "fake_provider_executor_invocation_allowed"),
        ("invocation_request_envelope", "executable_provider_invocation_allowed"),
        ("invocation_request_envelope", "model_request_dispatch_allowed"),
        ("invocation_request_envelope", "provider_sdk_client_allowed"),
        ("invocation_request_envelope", "provider_endpoint_resolution_allowed"),
        ("invocation_request_envelope", "network_calls_allowed"),
        ("invocation_request_envelope", "secret_lookup_allowed"),
        ("invocation_request_envelope", "credential_value_access_allowed"),
        ("invocation_request_envelope", "provider_token_or_api_key_access_allowed"),
        ("invocation_request_envelope", "fallback_execution_allowed"),
        ("invocation_request_envelope", "raw_prompt_present"),
        ("invocation_request_envelope", "raw_request_payload_present"),
        ("invocation_response_envelope", "provider_executor_invoked"),
        ("invocation_response_envelope", "real_provider_executor_invoked"),
        ("invocation_response_envelope", "fake_provider_executor_invoked"),
        ("invocation_response_envelope", "model_response_received"),
        ("invocation_response_envelope", "network_call_performed"),
        ("invocation_response_envelope", "provider_sdk_client_used"),
        ("invocation_response_envelope", "provider_endpoint_resolved"),
        ("invocation_response_envelope", "secret_lookup_performed"),
        ("invocation_response_envelope", "credential_value_accessed"),
        ("invocation_response_envelope", "fallback_execution_performed"),
        ("provider_model_scope", "provider_configuration_changed"),
        ("provider_model_scope", "provider_endpoint_selected"),
        ("provider_model_scope", "model_invocation_selected"),
        ("provider_model_scope", "executable_invocation_selected"),
        ("executor_authority_linkage", "executor_invocation_allowed"),
        ("executor_authority_linkage", "executable_provider_invocation_allowed"),
        ("credential_network_hardening_linkage", "network_calls_allowed"),
        ("execution_boundary_metadata", "provider_executor_call_allowed"),
    ],
)
def test_v1_g50_forbidden_metadata_claims_fail_closed(
    section: str,
    field: str,
) -> None:
    metadata = _candidate_metadata()
    metadata[section][field] = True

    with pytest.raises(AssertionError, match=field):
        _assert_invocation_metadata_is_allowed(metadata)


def test_v1_g50_top_level_forbidden_boundaries_remain_false() -> None:
    fixture = _load_fixture()

    for key in (
        "consumer_repo_mutation_added",
        "consumer_runtime_calls_added",
        "live_provider_model_call_execution_added",
        "provider_executor_invocation_added",
        "fake_provider_executor_invocation_added",
        "real_provider_executor_invocation_added",
        "direct_provider_sdk_added",
        "direct_provider_sdk_used",
        "direct_network_code_added",
        "direct_network_code_used",
        "provider_endpoint_resolution_added",
        "provider_endpoint_resolution_performed",
        "network_call_performed",
        "ambient_environment_secret_lookup_added",
        "secret_lookup_added",
        "secret_lookup_performed",
        "credential_value_access_added",
        "credential_value_accessed",
        "provider_token_or_api_key_access_added",
        "credential_storage_or_rotation_added",
        "provider_configuration_changes_added",
        "fallback_execution_added",
        "provider_readiness_network_check_added",
        "token_guardian_live_routing_added",
        "tool_execution_added",
        "action_execution_added",
        "connector_browser_network_file_device_robotics_physical_world_behavior_added",
        "scheduled_task_execution_added",
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
    ):
        assert fixture[key] is False


def test_v1_g50_prior_evidence_refs_exist() -> None:
    fixture = _load_fixture()

    for relative_path in fixture["required_prior_evidence_refs"]:
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g50_future_gates_remain_blocked() -> None:
    fixture = _load_fixture()

    assert fixture["future_required_gates"] == [
        "executable_real_provider_executor_invocation_approval_request",
        "built_in_provider_sdk_approval_request",
        "provider_network_egress_approval_request",
        "fallback_execution_approval_request",
        "connector_browser_network_authority_approval_request",
        "physical_world_authority_approval_request",
        "product_readiness_approval_request",
    ]
    assert fixture["blocked_future_authorities"] == {
        "executable_real_provider_executor_invocation_approved": False,
        "provider_secret_lookup_approved": False,
        "provider_credential_value_access_approved": False,
        "provider_network_egress_approved": False,
        "built_in_provider_sdk_approved": False,
        "fallback_execution_approved": False,
        "connector_browser_network_authority_approved": False,
        "physical_world_authority_approved": False,
        "product_readiness_approved": False,
    }


def test_v1_g50_required_confirmations_are_true() -> None:
    confirmations = _load_fixture()["required_confirmations"]

    assert all(confirmations.values())
    assert confirmations["invocation_metadata_only_confirmation"] is True
    assert confirmations["non_executing_invocation_envelope_confirmation"] is True
    assert confirmations["v1_g49_executor_authority_linkage_confirmation"] is True
    assert confirmations["v1_g48_credential_network_hardening_linkage_confirmation"] is True
    assert confirmations["no_provider_executor_invocation_confirmation"] is True
    assert confirmations["no_provider_endpoint_resolution_confirmation"] is True
    assert confirmations["proof_not_executable_provider_invocation_authority_confirmation"] is True
    assert confirmations["proof_not_product_readiness_confirmation"] is True


def test_v1_g50_lima_validation_results_are_recorded() -> None:
    validation = _load_fixture()["lima_validation_results"]

    assert validation["focused_v1_g50_validation"]["passed"] is True
    assert validation["focused_v1_g50_validation"]["tests_passed"] == 48
    assert validation["focused_v1_g50_g49_g48_g47_g46_g22_validation"]["passed"] is True
    assert (
        validation["focused_v1_g50_g49_g48_g47_g46_g22_validation"]["tests_passed"]
        == 207
    )
    assert validation["compileall_lima"] == {
        "command": "python -m compileall lima",
        "passed": True,
    }
    assert validation["full_lima_suite"]["passed"] is True
    assert validation["full_lima_suite"]["tests_passed"] == 4437


def test_v1_g50_fixture_and_docs_do_not_include_sensitive_markers() -> None:
    output = json.dumps(_load_fixture(), sort_keys=True)
    output += (
        REPO_ROOT / "docs" / "V1_G50_REAL_PROVIDER_EXECUTOR_INVOCATION.md"
    ).read_text(encoding="utf-8")
    output += (
        REPO_ROOT / "docs" / "V1_G50_REAL_PROVIDER_EXECUTOR_INVOCATION_CLOSEOUT.md"
    ).read_text(encoding="utf-8")

    for forbidden in (
        "diff --git",
        "@@",
        "BEGIN PATCH",
        "raw prompt value",
        "raw model response value",
        "raw customer data value",
        "provider credential value",
        "provider token value",
        "api key value",
        "raw-secret-123",
    ):
        assert forbidden not in output
