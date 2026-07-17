"""Tests for the approved V1-G48 provider credential/network hardening slice."""

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
    / "v1_g48_provider_credential_network_hardening.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _candidate_metadata() -> dict[str, Any]:
    fixture = _load_fixture()
    return {
        "credential_reference_policy": copy.deepcopy(
            fixture["credential_reference_policy"]
        ),
        "provider_network_policy": copy.deepcopy(fixture["provider_network_policy"]),
        "redaction_and_audit_policy": copy.deepcopy(
            fixture["redaction_and_audit_policy"]
        ),
    }


def _assert_hardening_metadata_is_allowed(metadata: dict[str, Any]) -> None:
    credential = metadata["credential_reference_policy"]
    network = metadata["provider_network_policy"]
    audit = metadata["redaction_and_audit_policy"]

    assert credential["reference_only"] is True
    assert credential["metadata_only"] is True
    for key in (
        "secret_lookup_allowed",
        "secret_lookup_performed",
        "ambient_environment_secret_lookup_allowed",
        "credential_value_access_allowed",
        "credential_value_accessed",
        "credential_storage_or_rotation_allowed",
        "provider_token_or_api_key_access_allowed",
        "raw_secret_present",
        "credential_value_present",
        "provider_token_present",
        "api_key_present",
    ):
        assert credential[key] is False, key

    assert network["reference_only"] is True
    assert network["metadata_only"] is True
    assert network["deny_by_default"] is True
    assert network["network_scope_bound"] is True
    for key in (
        "provider_endpoint_resolution_allowed",
        "provider_endpoint_resolution_performed",
        "dns_lookup_allowed",
        "http_client_allowed",
        "socket_client_allowed",
        "network_calls_allowed",
        "network_call_performed",
        "provider_readiness_network_check_allowed",
        "direct_provider_egress_allowed",
    ):
        assert network[key] is False, key

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


def test_v1_g48_fixture_records_approved_scope_and_status() -> None:
    fixture = _load_fixture()

    assert fixture["packet_set_id"] == "v1_g48_provider_credential_network_hardening"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g48-provider-credential-network-hardening"
    assert fixture["operator_decision"] == "Approve-V1-G48"
    assert fixture["approved_scope"] == (
        "provider_credential_network_hardening_metadata_slice"
    )
    assert fixture["provider_credential_network_hardening_approved"] is True
    assert fixture["provider_credential_network_hardening_added"] is True
    assert fixture["product_ready"] is False


def test_v1_g48_file_scope_is_exact_and_runtime_unchanged() -> None:
    fixture = _load_fixture()

    assert fixture["approved_lima_runtime_files_changed"] == []
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["approved_lima_docs_tests_fixtures_changed"] == [
        "docs/V1_G48_PROVIDER_CREDENTIAL_NETWORK_HARDENING.md",
        "docs/V1_G48_PROVIDER_CREDENTIAL_NETWORK_HARDENING_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g48_provider_credential_network_hardening.json",
        "tests/test_v1_g48_provider_credential_network_hardening.py",
    ]
    for relative_path in fixture["approved_lima_docs_tests_fixtures_changed"]:
        assert (REPO_ROOT / relative_path).exists()
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["arc_bot_shell_files_changed"] is False


def test_v1_g48_credential_policy_is_reference_only() -> None:
    credential = _load_fixture()["credential_reference_policy"]

    assert credential["policy_id"] == "credential-policy:v1-g48:provider-reference-only"
    assert credential["credential_ref"] == "credential-ref:v1-g48:provider:metadata-only"
    assert credential["vault_policy_ref"] == "vault-policy:v1-g48:reference-only"
    assert credential["rotation_policy_ref"] == "rotation-policy:v1-g48:not-executed"
    assert credential["reference_only"] is True
    assert credential["metadata_only"] is True
    assert credential["secret_lookup_allowed"] is False
    assert credential["credential_value_access_allowed"] is False
    assert credential["provider_token_or_api_key_access_allowed"] is False
    assert credential["raw_secret_present"] is False
    assert credential["credential_value_present"] is False
    assert credential["provider_token_present"] is False
    assert credential["api_key_present"] is False


def test_v1_g48_network_policy_is_reference_only_and_deny_by_default() -> None:
    network = _load_fixture()["provider_network_policy"]

    assert network["policy_id"] == (
        "network-policy:v1-g48:provider-egress-reference-only"
    )
    assert network["provider_network_policy_ref"] == (
        "provider-network-policy:v1-g48:deny-by-default"
    )
    assert network["allowed_provider_boundary_ref"] == (
        "provider-boundary:v1-g48:metadata-only"
    )
    assert network["reference_only"] is True
    assert network["metadata_only"] is True
    assert network["deny_by_default"] is True
    assert network["provider_endpoint_resolution_allowed"] is False
    assert network["dns_lookup_allowed"] is False
    assert network["http_client_allowed"] is False
    assert network["socket_client_allowed"] is False
    assert network["network_calls_allowed"] is False
    assert network["direct_provider_egress_allowed"] is False


def test_v1_g48_redaction_and_audit_policy_is_sanitized() -> None:
    audit = _load_fixture()["redaction_and_audit_policy"]

    assert audit["redaction_policy_ref"] == (
        "redaction-policy:v1-g48:provider-hardening"
    )
    assert audit["audit_record_ref"] == (
        "audit:v1-g48:provider-credential-network-hardening"
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


def test_v1_g48_allowed_metadata_passes_local_fail_closed_checks() -> None:
    _assert_hardening_metadata_is_allowed(_candidate_metadata())


@pytest.mark.parametrize(
    ("section", "field"),
    [
        ("credential_reference_policy", "secret_lookup_allowed"),
        ("credential_reference_policy", "secret_lookup_performed"),
        ("credential_reference_policy", "ambient_environment_secret_lookup_allowed"),
        ("credential_reference_policy", "credential_value_access_allowed"),
        ("credential_reference_policy", "credential_value_accessed"),
        ("credential_reference_policy", "credential_storage_or_rotation_allowed"),
        ("credential_reference_policy", "provider_token_or_api_key_access_allowed"),
        ("credential_reference_policy", "raw_secret_present"),
        ("credential_reference_policy", "credential_value_present"),
        ("credential_reference_policy", "provider_token_present"),
        ("credential_reference_policy", "api_key_present"),
        ("provider_network_policy", "provider_endpoint_resolution_allowed"),
        ("provider_network_policy", "provider_endpoint_resolution_performed"),
        ("provider_network_policy", "dns_lookup_allowed"),
        ("provider_network_policy", "http_client_allowed"),
        ("provider_network_policy", "socket_client_allowed"),
        ("provider_network_policy", "network_calls_allowed"),
        ("provider_network_policy", "network_call_performed"),
        ("provider_network_policy", "provider_readiness_network_check_allowed"),
        ("provider_network_policy", "direct_provider_egress_allowed"),
        ("redaction_and_audit_policy", "raw_prompt_persistence_allowed"),
        ("redaction_and_audit_policy", "raw_model_response_persistence_allowed"),
        ("redaction_and_audit_policy", "raw_customer_data_persistence_allowed"),
        ("redaction_and_audit_policy", "raw_secret_credential_persistence_allowed"),
        ("redaction_and_audit_policy", "raw_diff_patch_file_content_persistence_allowed"),
    ],
)
def test_v1_g48_forbidden_metadata_claims_fail_closed(
    section: str,
    field: str,
) -> None:
    metadata = _candidate_metadata()
    metadata[section][field] = True

    with pytest.raises(AssertionError, match=field):
        _assert_hardening_metadata_is_allowed(metadata)


def test_v1_g48_top_level_forbidden_boundaries_remain_false() -> None:
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


def test_v1_g48_prior_evidence_refs_exist() -> None:
    fixture = _load_fixture()

    for relative_path in fixture["required_prior_evidence_refs"]:
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g48_future_gates_remain_blocked() -> None:
    fixture = _load_fixture()

    assert fixture["future_required_gates"] == [
        "real_provider_executor_approval_request",
        "built_in_provider_sdk_approval_request",
        "provider_network_egress_approval_request",
        "fallback_execution_approval_request",
        "connector_browser_network_authority_approval_request",
        "physical_world_authority_approval_request",
        "product_readiness_approval_request",
    ]
    assert fixture["blocked_future_authorities"] == {
        "real_provider_executor_approved": False,
        "provider_secret_lookup_approved": False,
        "provider_credential_value_access_approved": False,
        "provider_network_egress_approved": False,
        "built_in_provider_sdk_approved": False,
        "fallback_execution_approved": False,
        "connector_browser_network_authority_approved": False,
        "physical_world_authority_approved": False,
        "product_readiness_approved": False,
    }


def test_v1_g48_required_confirmations_are_true() -> None:
    confirmations = _load_fixture()["required_confirmations"]

    assert all(confirmations.values())
    assert confirmations["credential_reference_only_confirmation"] is True
    assert confirmations["network_policy_reference_only_confirmation"] is True
    assert confirmations["deny_by_default_network_confirmation"] is True
    assert confirmations["no_provider_endpoint_resolution_confirmation"] is True
    assert confirmations["no_provider_token_or_api_key_access_confirmation"] is True
    assert confirmations["proof_not_real_provider_authority_confirmation"] is True
    assert confirmations["proof_not_product_readiness_confirmation"] is True


def test_v1_g48_lima_validation_results_are_recorded() -> None:
    validation = _load_fixture()["lima_validation_results"]

    assert validation["focused_v1_g48_validation"]["passed"] is True
    assert validation["focused_v1_g48_validation"]["tests_passed"] == 37
    assert validation["focused_v1_g48_g47_g46_g22_validation"]["passed"] is True
    assert validation["focused_v1_g48_g47_g46_g22_validation"]["tests_passed"] == 114
    assert validation["compileall_lima"] == {
        "command": "python -m compileall lima",
        "passed": True,
    }
    assert validation["full_lima_suite"]["passed"] is True
    assert validation["full_lima_suite"]["tests_passed"] == 4336


def test_v1_g48_fixture_and_docs_do_not_include_sensitive_markers() -> None:
    output = json.dumps(_load_fixture(), sort_keys=True)
    output += (
        REPO_ROOT / "docs" / "V1_G48_PROVIDER_CREDENTIAL_NETWORK_HARDENING.md"
    ).read_text(encoding="utf-8")
    output += (
        REPO_ROOT / "docs" / "V1_G48_PROVIDER_CREDENTIAL_NETWORK_HARDENING_CLOSEOUT.md"
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
