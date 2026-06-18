"""Tests for the approved V1-G49 real provider executor authority design slice."""

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


def _load_g48_fixture() -> dict[str, Any]:
    fixture = json.loads(G48_FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _candidate_metadata() -> dict[str, Any]:
    fixture = _load_fixture()
    return {
        "executor_authority_metadata": copy.deepcopy(
            fixture["executor_authority_metadata"]
        ),
        "provider_model_scope": copy.deepcopy(fixture["provider_model_scope"]),
        "credential_network_hardening_linkage": copy.deepcopy(
            fixture["credential_network_hardening_linkage"]
        ),
        "redaction_and_audit_policy": copy.deepcopy(
            fixture["redaction_and_audit_policy"]
        ),
    }


def _assert_executor_metadata_is_allowed(metadata: dict[str, Any]) -> None:
    executor = metadata["executor_authority_metadata"]
    scope = metadata["provider_model_scope"]
    linkage = metadata["credential_network_hardening_linkage"]
    audit = metadata["redaction_and_audit_policy"]

    assert executor["metadata_only"] is True
    assert executor["non_executing"] is True
    assert executor["proof_not_execution"] is True
    for key in (
        "executor_invocation_allowed",
        "real_provider_executor_invocation_allowed",
        "fake_provider_executor_invocation_allowed",
        "provider_sdk_client_allowed",
        "provider_endpoint_resolution_allowed",
        "network_calls_allowed",
        "secret_lookup_allowed",
        "credential_value_access_allowed",
        "fallback_execution_allowed",
        "product_readiness_claim_allowed",
    ):
        assert executor[key] is False, key

    assert scope["reference_only"] is True
    assert scope["metadata_only"] is True
    for key in (
        "provider_configuration_changed",
        "provider_endpoint_selected",
        "model_invocation_selected",
    ):
        assert scope[key] is False, key

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


def test_v1_g49_fixture_records_approved_scope_and_status() -> None:
    fixture = _load_fixture()

    assert fixture["packet_set_id"] == "v1_g49_real_provider_executor"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g49-real-provider-executor"
    assert fixture["operator_decision"] == "Approve-V1-G49"
    assert fixture["approved_scope"] == (
        "real_provider_executor_authority_design_metadata_slice"
    )
    assert fixture["real_provider_executor_authority_design_approved"] is True
    assert fixture["real_provider_executor_authority_design_added"] is True
    assert fixture["product_ready"] is False


def test_v1_g49_file_scope_is_exact_and_runtime_unchanged() -> None:
    fixture = _load_fixture()

    assert fixture["approved_lima_runtime_files_changed"] == []
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["approved_lima_docs_tests_fixtures_changed"] == [
        "docs/V1_G49_REAL_PROVIDER_EXECUTOR.md",
        "docs/V1_G49_REAL_PROVIDER_EXECUTOR_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g49_real_provider_executor.json",
        "tests/test_v1_g49_real_provider_executor.py",
    ]
    for relative_path in fixture["approved_lima_docs_tests_fixtures_changed"]:
        assert (REPO_ROOT / relative_path).exists()
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["arc_bot_shell_files_changed"] is False


def test_v1_g49_executor_authority_metadata_is_non_executing() -> None:
    executor = _load_fixture()["executor_authority_metadata"]

    assert executor["executor_authority_id"] == (
        "real-provider-executor-authority:v1-g49:metadata-only"
    )
    assert executor["executor_authority_type"] == (
        "real_provider_executor_design_metadata"
    )
    assert executor["metadata_only"] is True
    assert executor["non_executing"] is True
    assert executor["proof_not_execution"] is True
    assert executor["executor_invocation_allowed"] is False
    assert executor["real_provider_executor_invocation_allowed"] is False
    assert executor["fake_provider_executor_invocation_allowed"] is False
    assert executor["provider_sdk_client_allowed"] is False
    assert executor["provider_endpoint_resolution_allowed"] is False
    assert executor["network_calls_allowed"] is False
    assert executor["secret_lookup_allowed"] is False
    assert executor["credential_value_access_allowed"] is False
    assert executor["fallback_execution_allowed"] is False


def test_v1_g49_provider_model_scope_is_reference_only() -> None:
    scope = _load_fixture()["provider_model_scope"]

    assert scope["provider_scope_ref"] == (
        "provider-scope:v1-g49:single-provider-reference"
    )
    assert scope["model_scope_ref"] == (
        "model-scope:v1-g49:single-model-class-reference"
    )
    assert scope["route_authority_ref"] == "route:v1-g20:metadata-only"
    assert scope["dispatch_evidence_ref"] == (
        "provider-model-dispatch:v1-g43:fake-provider:001"
    )
    assert scope["reference_only"] is True
    assert scope["metadata_only"] is True
    assert scope["provider_configuration_changed"] is False
    assert scope["provider_endpoint_selected"] is False
    assert scope["model_invocation_selected"] is False


def test_v1_g49_links_to_v1_g48_hardening_by_reference() -> None:
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


def test_v1_g49_redaction_and_audit_policy_is_sanitized() -> None:
    audit = _load_fixture()["redaction_and_audit_policy"]

    assert audit["executor_authority_evidence_ref"] == (
        "evidence:v1-g49:real-provider-executor-authority-design"
    )
    assert audit["audit_record_ref"] == (
        "audit:v1-g49:real-provider-executor-authority-design"
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


def test_v1_g49_allowed_metadata_passes_local_fail_closed_checks() -> None:
    _assert_executor_metadata_is_allowed(_candidate_metadata())


@pytest.mark.parametrize(
    ("section", "field"),
    [
        ("executor_authority_metadata", "executor_invocation_allowed"),
        ("executor_authority_metadata", "real_provider_executor_invocation_allowed"),
        ("executor_authority_metadata", "fake_provider_executor_invocation_allowed"),
        ("executor_authority_metadata", "provider_sdk_client_allowed"),
        ("executor_authority_metadata", "provider_endpoint_resolution_allowed"),
        ("executor_authority_metadata", "network_calls_allowed"),
        ("executor_authority_metadata", "secret_lookup_allowed"),
        ("executor_authority_metadata", "credential_value_access_allowed"),
        ("executor_authority_metadata", "fallback_execution_allowed"),
        ("executor_authority_metadata", "product_readiness_claim_allowed"),
        ("provider_model_scope", "provider_configuration_changed"),
        ("provider_model_scope", "provider_endpoint_selected"),
        ("provider_model_scope", "model_invocation_selected"),
        ("credential_network_hardening_linkage", "secret_lookup_allowed"),
        ("credential_network_hardening_linkage", "credential_value_access_allowed"),
        (
            "credential_network_hardening_linkage",
            "provider_token_or_api_key_access_allowed",
        ),
        (
            "credential_network_hardening_linkage",
            "provider_endpoint_resolution_allowed",
        ),
        ("credential_network_hardening_linkage", "network_calls_allowed"),
        ("credential_network_hardening_linkage", "direct_provider_egress_allowed"),
        ("redaction_and_audit_policy", "raw_prompt_persistence_allowed"),
        ("redaction_and_audit_policy", "raw_model_response_persistence_allowed"),
        ("redaction_and_audit_policy", "raw_customer_data_persistence_allowed"),
        ("redaction_and_audit_policy", "raw_secret_credential_persistence_allowed"),
        ("redaction_and_audit_policy", "raw_diff_patch_file_content_persistence_allowed"),
    ],
)
def test_v1_g49_forbidden_metadata_claims_fail_closed(
    section: str,
    field: str,
) -> None:
    metadata = _candidate_metadata()
    metadata[section][field] = True

    with pytest.raises(AssertionError, match=field):
        _assert_executor_metadata_is_allowed(metadata)


def test_v1_g49_top_level_forbidden_boundaries_remain_false() -> None:
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


def test_v1_g49_prior_evidence_refs_exist() -> None:
    fixture = _load_fixture()

    for relative_path in fixture["required_prior_evidence_refs"]:
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g49_future_gates_remain_blocked() -> None:
    fixture = _load_fixture()

    assert fixture["future_required_gates"] == [
        "real_provider_executor_invocation_approval_request",
        "built_in_provider_sdk_approval_request",
        "provider_network_egress_approval_request",
        "fallback_execution_approval_request",
        "connector_browser_network_authority_approval_request",
        "physical_world_authority_approval_request",
        "product_readiness_approval_request",
    ]
    assert fixture["blocked_future_authorities"] == {
        "real_provider_executor_invocation_approved": False,
        "provider_secret_lookup_approved": False,
        "provider_credential_value_access_approved": False,
        "provider_network_egress_approved": False,
        "built_in_provider_sdk_approved": False,
        "fallback_execution_approved": False,
        "connector_browser_network_authority_approved": False,
        "physical_world_authority_approved": False,
        "product_readiness_approved": False,
    }


def test_v1_g49_required_confirmations_are_true() -> None:
    confirmations = _load_fixture()["required_confirmations"]

    assert all(confirmations.values())
    assert confirmations["executor_authority_metadata_only_confirmation"] is True
    assert confirmations["non_executing_authority_design_confirmation"] is True
    assert confirmations["v1_g48_credential_network_hardening_linkage_confirmation"] is True
    assert confirmations["no_provider_executor_invocation_confirmation"] is True
    assert confirmations["no_provider_endpoint_resolution_confirmation"] is True
    assert confirmations["proof_not_real_provider_invocation_authority_confirmation"] is True
    assert confirmations["proof_not_product_readiness_confirmation"] is True


def test_v1_g49_lima_validation_results_are_recorded() -> None:
    validation = _load_fixture()["lima_validation_results"]

    assert validation["focused_v1_g49_validation"]["passed"] is True
    assert validation["focused_v1_g49_validation"]["tests_passed"] == 37
    assert validation["focused_v1_g49_g48_g47_g46_g22_validation"]["passed"] is True
    assert (
        validation["focused_v1_g49_g48_g47_g46_g22_validation"]["tests_passed"] == 151
    )
    assert validation["compileall_lima"] == {
        "command": "python -m compileall lima",
        "passed": True,
    }
    assert validation["full_lima_suite"]["passed"] is True
    assert validation["full_lima_suite"]["tests_passed"] == 4381


def test_v1_g49_fixture_and_docs_do_not_include_sensitive_markers() -> None:
    output = json.dumps(_load_fixture(), sort_keys=True)
    output += (REPO_ROOT / "docs" / "V1_G49_REAL_PROVIDER_EXECUTOR.md").read_text(
        encoding="utf-8"
    )
    output += (
        REPO_ROOT / "docs" / "V1_G49_REAL_PROVIDER_EXECUTOR_CLOSEOUT.md"
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
