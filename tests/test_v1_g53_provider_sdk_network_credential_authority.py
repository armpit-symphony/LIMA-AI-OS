"""Tests for the approved V1-G53 provider SDK/network/credential authority slice."""

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
    / "v1_g53_provider_sdk_network_credential_authority.json"
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


def _load_json(path: Path) -> dict[str, Any]:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _load_fixture() -> dict[str, Any]:
    return _load_json(FIXTURE_PATH)


def _candidate_metadata() -> dict[str, Any]:
    fixture = _load_fixture()
    return {
        "provider_sdk_authority_metadata": copy.deepcopy(
            fixture["provider_sdk_authority_metadata"]
        ),
        "endpoint_resolution_authority_metadata": copy.deepcopy(
            fixture["endpoint_resolution_authority_metadata"]
        ),
        "provider_network_egress_authority_metadata": copy.deepcopy(
            fixture["provider_network_egress_authority_metadata"]
        ),
        "credential_reference_authority_metadata": copy.deepcopy(
            fixture["credential_reference_authority_metadata"]
        ),
        "authority_chain_linkage": copy.deepcopy(fixture["authority_chain_linkage"]),
        "redaction_and_audit_policy": copy.deepcopy(
            fixture["redaction_and_audit_policy"]
        ),
    }


def _assert_authority_metadata_is_allowed(metadata: dict[str, Any]) -> None:
    sdk = metadata["provider_sdk_authority_metadata"]
    endpoint = metadata["endpoint_resolution_authority_metadata"]
    network = metadata["provider_network_egress_authority_metadata"]
    credential = metadata["credential_reference_authority_metadata"]
    chain = metadata["authority_chain_linkage"]
    audit = metadata["redaction_and_audit_policy"]

    assert sdk["metadata_only"] is True
    assert sdk["non_executing"] is True
    assert sdk["proof_not_execution"] is True
    for key in (
        "provider_sdk_client_allowed",
        "built_in_provider_sdk_client_allowed",
        "direct_provider_sdk_implementation_allowed",
        "sdk_dependency_addition_allowed",
        "sdk_client_construction_allowed",
        "sdk_call_allowed",
        "sdk_call_performed",
        "network_calls_allowed",
        "credential_value_access_allowed",
        "provider_token_or_api_key_access_allowed",
        "fallback_execution_allowed",
        "product_readiness_claim_allowed",
    ):
        assert sdk[key] is False, key

    assert endpoint["metadata_only"] is True
    assert endpoint["reference_only"] is True
    assert endpoint["non_executing"] is True
    for key in (
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
        assert endpoint[key] is False, key

    assert network["metadata_only"] is True
    assert network["reference_only"] is True
    assert network["non_executing"] is True
    assert network["network_scope_bound"] is True
    assert network["deny_by_default"] is True
    for key in (
        "network_egress_execution_allowed",
        "network_calls_allowed",
        "network_call_performed",
        "direct_provider_egress_allowed",
        "provider_endpoint_resolution_allowed",
        "dns_lookup_allowed",
        "http_client_allowed",
        "socket_client_allowed",
        "provider_readiness_network_check_allowed",
    ):
        assert network[key] is False, key

    assert credential["metadata_only"] is True
    assert credential["reference_only"] is True
    assert credential["credential_reference_only"] is True
    for key in (
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
        assert credential[key] is False, key

    assert chain["authority_records_metadata_only"] is True
    assert chain["guardian_gate_required"] is True
    assert chain["no_runtime_enforcement_added"] is True
    assert chain["no_public_api_change_required"] is True
    assert chain["credential_reference_only"] is True
    assert chain["network_policy_reference_only"] is True
    assert chain["deny_by_default_network_required"] is True
    for key in (
        "provider_sdk_client_allowed",
        "endpoint_resolution_execution_allowed",
        "network_egress_execution_allowed",
        "secret_lookup_allowed",
        "credential_value_access_allowed",
        "provider_token_or_api_key_access_allowed",
        "fallback_execution_allowed",
        "consumer_production_runtime_integration_allowed",
    ):
        assert chain[key] is False, key

    assert audit["audit_required"] is True
    assert audit["sanitized_evidence_only"] is True
    assert audit["redacted_input_required"] is True
    assert audit["redacted_output_required"] is True
    for key in (
        "raw_prompt_persistence_allowed",
        "raw_model_response_persistence_allowed",
        "raw_customer_data_persistence_allowed",
        "raw_secret_credential_persistence_allowed",
        "raw_provider_token_api_key_persistence_allowed",
        "raw_diff_patch_file_content_persistence_allowed",
    ):
        assert audit[key] is False, key


def test_v1_g53_fixture_records_approved_scope_and_status() -> None:
    fixture = _load_fixture()

    assert fixture["packet_set_id"] == (
        "v1_g53_provider_sdk_network_credential_authority"
    )
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g53-provider-sdk-network-credential-authority"
    assert fixture["operator_decision"] == "Approve-V1-G53"
    assert fixture["approved_scope"] == (
        "provider_sdk_network_credential_authority_metadata_slice"
    )
    assert fixture["provider_sdk_network_credential_authority_approved"] is True
    assert fixture["provider_sdk_network_credential_authority_added"] is True
    assert fixture["metadata_only_authority_design_added"] is True
    assert fixture["product_ready"] is False


def test_v1_g53_file_scope_is_exact_and_runtime_unchanged() -> None:
    fixture = _load_fixture()

    assert fixture["approved_lima_runtime_files_changed"] == []
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["lima_public_api_changed"] is False
    assert fixture["approved_lima_docs_tests_fixtures_changed"] == [
        "docs/V1_G53_PROVIDER_SDK_NETWORK_CREDENTIAL_AUTHORITY.md",
        "docs/V1_G53_PROVIDER_SDK_NETWORK_CREDENTIAL_AUTHORITY_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g53_provider_sdk_network_credential_authority.json",
        "tests/test_v1_g53_provider_sdk_network_credential_authority.py",
    ]
    for relative_path in fixture["approved_lima_docs_tests_fixtures_changed"]:
        assert (REPO_ROOT / relative_path).exists()
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["arc_bot_shell_files_changed"] is False


def test_v1_g53_provider_sdk_authority_metadata_is_non_executing() -> None:
    sdk = _load_fixture()["provider_sdk_authority_metadata"]

    assert sdk["provider_sdk_authority_id"] == (
        "provider-sdk-authority:v1-g53:metadata-only"
    )
    assert sdk["authority_type"] == "provider_sdk_authority_metadata"
    assert sdk["metadata_only"] is True
    assert sdk["built_in_provider_sdk_authority_metadata_allowed"] is True
    assert sdk["provider_sdk_client_allowed"] is False
    assert sdk["built_in_provider_sdk_client_allowed"] is False
    assert sdk["direct_provider_sdk_implementation_allowed"] is False
    assert sdk["sdk_dependency_addition_allowed"] is False
    assert sdk["sdk_client_construction_allowed"] is False
    assert sdk["sdk_call_allowed"] is False
    assert sdk["sdk_call_performed"] is False


def test_v1_g53_endpoint_resolution_authority_metadata_is_reference_only() -> None:
    endpoint = _load_fixture()["endpoint_resolution_authority_metadata"]

    assert endpoint["endpoint_resolution_authority_id"] == (
        "endpoint-resolution-authority:v1-g53:metadata-only"
    )
    assert endpoint["authority_type"] == (
        "provider_endpoint_resolution_authority_metadata"
    )
    assert endpoint["metadata_only"] is True
    assert endpoint["reference_only"] is True
    assert endpoint["provider_endpoint_resolution_authority_metadata_allowed"] is True
    assert endpoint["provider_endpoint_resolution_allowed"] is False
    assert endpoint["provider_endpoint_resolution_performed"] is False
    assert endpoint["endpoint_resolution_execution_allowed"] is False
    assert endpoint["provider_endpoint_selected"] is False
    assert endpoint["provider_configuration_changed"] is False


def test_v1_g53_network_egress_authority_metadata_is_deny_by_default() -> None:
    network = _load_fixture()["provider_network_egress_authority_metadata"]

    assert network["network_egress_authority_id"] == (
        "provider-network-egress-authority:v1-g53:metadata-only"
    )
    assert network["authority_type"] == "provider_network_egress_authority_metadata"
    assert network["metadata_only"] is True
    assert network["reference_only"] is True
    assert network["network_policy_ref"] == (
        "network-policy:v1-g48:provider-egress-reference-only"
    )
    assert network["network_scope_bound"] is True
    assert network["deny_by_default"] is True
    assert network["network_egress_execution_allowed"] is False
    assert network["network_calls_allowed"] is False
    assert network["network_call_performed"] is False
    assert network["direct_provider_egress_allowed"] is False


def test_v1_g53_credential_reference_authority_links_to_v1_g48() -> None:
    credential = _load_fixture()["credential_reference_authority_metadata"]
    g48 = _load_json(G48_FIXTURE_PATH)

    assert credential["credential_authority_id"] == (
        "credential-reference-authority:v1-g53:metadata-only"
    )
    assert credential["authority_type"] == "credential_reference_authority_metadata"
    assert credential["credential_policy_ref"] == g48["credential_reference_policy"][
        "policy_id"
    ]
    assert credential["credential_ref"] == g48["credential_reference_policy"][
        "credential_ref"
    ]
    assert credential["vault_policy_ref"] == g48["credential_reference_policy"][
        "vault_policy_ref"
    ]
    assert credential["credential_reference_only"] is True
    assert credential["secret_lookup_allowed"] is False
    assert credential["credential_value_access_allowed"] is False
    assert credential["provider_token_or_api_key_access_allowed"] is False


def test_v1_g53_authority_chain_links_prior_evidence_by_reference() -> None:
    chain = _load_fixture()["authority_chain_linkage"]
    g48 = _load_json(G48_FIXTURE_PATH)
    g50 = _load_json(G50_FIXTURE_PATH)
    g51 = _load_json(G51_FIXTURE_PATH)
    g52 = _load_json(G52_FIXTURE_PATH)

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
    assert g52["consumer_fake_executor_provider_invocation_smoke_added"] is True
    assert chain["authority_records_metadata_only"] is True
    assert chain["no_runtime_enforcement_added"] is True
    assert chain["no_public_api_change_required"] is True


def test_v1_g53_redaction_and_audit_policy_is_sanitized() -> None:
    audit = _load_fixture()["redaction_and_audit_policy"]

    assert audit["authority_evidence_ref"] == (
        "evidence:v1-g53:provider-sdk-network-credential-authority"
    )
    assert audit["audit_record_ref"] == (
        "audit:v1-g53:provider-sdk-network-credential-authority"
    )
    assert audit["audit_required"] is True
    assert audit["sanitized_evidence_only"] is True
    assert audit["redacted_input_required"] is True
    assert audit["redacted_output_required"] is True
    assert audit["raw_prompt_persistence_allowed"] is False
    assert audit["raw_model_response_persistence_allowed"] is False
    assert audit["raw_customer_data_persistence_allowed"] is False
    assert audit["raw_secret_credential_persistence_allowed"] is False
    assert audit["raw_provider_token_api_key_persistence_allowed"] is False
    assert audit["raw_diff_patch_file_content_persistence_allowed"] is False


def test_v1_g53_allowed_metadata_passes_local_fail_closed_checks() -> None:
    _assert_authority_metadata_is_allowed(_candidate_metadata())


@pytest.mark.parametrize(
    ("section", "field"),
    [
        ("provider_sdk_authority_metadata", "provider_sdk_client_allowed"),
        ("provider_sdk_authority_metadata", "built_in_provider_sdk_client_allowed"),
        (
            "provider_sdk_authority_metadata",
            "direct_provider_sdk_implementation_allowed",
        ),
        ("provider_sdk_authority_metadata", "sdk_dependency_addition_allowed"),
        ("provider_sdk_authority_metadata", "sdk_client_construction_allowed"),
        ("provider_sdk_authority_metadata", "sdk_call_allowed"),
        ("provider_sdk_authority_metadata", "sdk_call_performed"),
        ("provider_sdk_authority_metadata", "network_calls_allowed"),
        ("provider_sdk_authority_metadata", "credential_value_access_allowed"),
        (
            "provider_sdk_authority_metadata",
            "provider_token_or_api_key_access_allowed",
        ),
        (
            "endpoint_resolution_authority_metadata",
            "provider_endpoint_resolution_allowed",
        ),
        (
            "endpoint_resolution_authority_metadata",
            "provider_endpoint_resolution_performed",
        ),
        (
            "endpoint_resolution_authority_metadata",
            "endpoint_resolution_execution_allowed",
        ),
        ("endpoint_resolution_authority_metadata", "provider_endpoint_selected"),
        ("endpoint_resolution_authority_metadata", "provider_configuration_changed"),
        ("endpoint_resolution_authority_metadata", "dns_lookup_allowed"),
        ("endpoint_resolution_authority_metadata", "http_client_allowed"),
        ("endpoint_resolution_authority_metadata", "socket_client_allowed"),
        (
            "provider_network_egress_authority_metadata",
            "network_egress_execution_allowed",
        ),
        ("provider_network_egress_authority_metadata", "network_calls_allowed"),
        ("provider_network_egress_authority_metadata", "network_call_performed"),
        ("provider_network_egress_authority_metadata", "direct_provider_egress_allowed"),
        (
            "provider_network_egress_authority_metadata",
            "provider_endpoint_resolution_allowed",
        ),
        ("credential_reference_authority_metadata", "secret_lookup_allowed"),
        ("credential_reference_authority_metadata", "secret_lookup_performed"),
        (
            "credential_reference_authority_metadata",
            "ambient_environment_secret_lookup_allowed",
        ),
        ("credential_reference_authority_metadata", "credential_value_access_allowed"),
        ("credential_reference_authority_metadata", "credential_value_accessed"),
        (
            "credential_reference_authority_metadata",
            "provider_token_or_api_key_access_allowed",
        ),
        (
            "credential_reference_authority_metadata",
            "provider_token_or_api_key_accessed",
        ),
        ("authority_chain_linkage", "fallback_execution_allowed"),
        ("authority_chain_linkage", "consumer_production_runtime_integration_allowed"),
    ],
)
def test_v1_g53_forbidden_metadata_claims_fail_closed(
    section: str,
    field: str,
) -> None:
    metadata = _candidate_metadata()
    metadata[section][field] = True

    with pytest.raises(AssertionError, match=field):
        _assert_authority_metadata_is_allowed(metadata)


def test_v1_g53_top_level_forbidden_boundaries_remain_false() -> None:
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
        "direct_provider_sdk_added",
        "direct_provider_sdk_used",
        "sdk_dependency_added",
        "provider_endpoint_resolution_added",
        "provider_endpoint_resolution_performed",
        "direct_network_code_added",
        "direct_network_code_used",
        "network_call_performed",
        "network_call_performed_by_lima_harness",
        "direct_provider_egress_added",
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
        "provider_readiness_network_check_performed",
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

    assert fixture["credential_reference_metadata_only"] is True


def test_v1_g53_prior_evidence_refs_exist() -> None:
    fixture = _load_fixture()

    for relative_path in fixture["required_prior_evidence_refs"]:
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g53_future_gates_remain_blocked() -> None:
    fixture = _load_fixture()

    assert fixture["future_required_gates"] == [
        "fake_sdk_or_fake_egress_harness_approval_request",
        "real_provider_sdk_network_egress_implementation_approval_request",
        "credential_value_access_approval_request",
        "fallback_execution_approval_request",
        "connector_browser_network_authority_approval_request",
        "consumer_production_runtime_integration_approval_request",
        "physical_world_authority_approval_request",
        "product_readiness_approval_request",
    ]
    assert fixture["blocked_future_authorities"] == {
        "built_in_provider_sdk_client_approved": False,
        "direct_provider_sdk_implementation_approved": False,
        "provider_endpoint_resolution_execution_approved": False,
        "provider_network_egress_execution_approved": False,
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


def test_v1_g53_required_confirmations_are_true() -> None:
    confirmations = _load_fixture()["required_confirmations"]

    assert all(confirmations.values())
    assert confirmations["provider_sdk_network_credential_authority_metadata_only_confirmation"] is True
    assert confirmations["non_executing_authority_design_confirmation"] is True
    assert confirmations["v1_g48_credential_network_hardening_linkage_confirmation"] is True
    assert confirmations["v1_g51_executable_wrapper_boundary_linkage_confirmation"] is True
    assert confirmations["v1_g52_consumer_fake_executor_smoke_linkage_confirmation"] is True
    assert confirmations["no_built_in_provider_sdk_client_confirmation"] is True
    assert confirmations["no_provider_endpoint_resolution_execution_confirmation"] is True
    assert confirmations["no_provider_egress_confirmation"] is True
    assert confirmations["proof_not_product_readiness_confirmation"] is True


def test_v1_g53_lima_validation_results_are_recorded() -> None:
    validation = _load_fixture()["lima_validation_results"]

    assert validation["focused_v1_g53_validation"]["passed"] is True
    assert validation["focused_v1_g53_validation"]["tests_passed"] == 47
    assert (
        validation["focused_v1_g53_g52_g51_g50_g48_g22_validation"]["passed"] is True
    )
    assert (
        validation["focused_v1_g53_g52_g51_g50_g48_g22_validation"]["tests_passed"]
        == 236
    )
    assert validation["compileall_lima"] == {
        "command": "python -m compileall lima",
        "passed": True,
    }
    assert validation["full_lima_suite"]["passed"] is True
    assert validation["full_lima_suite"]["tests_passed"] == 4591


def test_v1_g53_fixture_and_docs_do_not_include_sensitive_markers() -> None:
    output = json.dumps(_load_fixture(), sort_keys=True)
    output += (
        REPO_ROOT
        / "docs"
        / "V1_G53_PROVIDER_SDK_NETWORK_CREDENTIAL_AUTHORITY.md"
    ).read_text(encoding="utf-8")
    output += (
        REPO_ROOT
        / "docs"
        / "V1_G53_PROVIDER_SDK_NETWORK_CREDENTIAL_AUTHORITY_CLOSEOUT.md"
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
