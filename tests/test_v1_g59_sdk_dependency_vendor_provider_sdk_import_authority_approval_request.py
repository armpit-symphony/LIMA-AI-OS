"""Static checks for the V1-G59 SDK dependency/vendor import authority request."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g59_sdk_dependency_vendor_provider_sdk_import_authority_approval_request.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g59_request_docs_and_fixture_exist() -> None:
    fixture = _load_fixture()

    assert fixture["gate_id"] == (
        "v1_g59_sdk_dependency_vendor_provider_sdk_import_authority_approval_request"
    )
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == (
        "prepare-v1-g59-sdk-dependency-vendor-provider-sdk-import-authority-approval-request"
    )
    assert fixture["docs_tests_fixtures_only_request"] is True

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g59_has_no_implementation_approval_yet() -> None:
    fixture = _load_fixture()
    decision = fixture["decision_record"]

    assert fixture["implementation_approved"] is False
    assert fixture["operator_approval_recorded"] is False
    assert fixture["sdk_dependency_vendor_provider_sdk_import_authority_approved"] is False
    assert fixture["sdk_dependency_vendor_provider_sdk_import_authority_added"] is False
    assert fixture["sdk_dependency_addition_approved"] is False
    assert fixture["sdk_dependency_added"] is False
    assert fixture["dependency_manifest_edited"] is False
    assert fixture["lockfile_edited"] is False
    assert fixture["vendor_provider_sdk_import_approved"] is False
    assert fixture["vendor_provider_sdk_import_added"] is False
    assert fixture["built_in_provider_sdk_client_implementation_approved"] is False
    assert fixture["built_in_provider_sdk_client_implementation_added"] is False
    assert fixture["provider_client_construction_added"] is False
    assert decision["recorded_choice"] == "none"
    assert decision["approved_implementation_branch"] == "none"
    assert decision["implementation_approved"] is False


def test_v1_g59_exact_decision_options_are_locked() -> None:
    fixture = _load_fixture()

    assert fixture["valid_operator_choices"] == [
        "Approve-V1-G59",
        "Revise-V1-G59",
        "Pause",
    ]
    assert fixture["required_approval_wording"] == (
        "I explicitly approve V1-G59 implementation of the LIMA-side SDK "
        "dependency and vendor provider SDK import authority metadata slice, "
        "limited to the file scope, behavior scope, tests, rollback plan, and "
        "stop conditions in "
        "docs/V1_G59_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_AUTHORITY_APPROVAL_REQUEST.md."
    )
    assert fixture["proposed_implementation_branch"] == (
        "v1-g59-sdk-dependency-vendor-provider-sdk-import-authority"
    )


def test_v1_g59_target_if_approved_is_metadata_only_and_deny_by_default() -> None:
    target = _load_fixture()[
        "sdk_dependency_vendor_provider_sdk_import_authority_target_if_operator_says_yes"
    ]

    assert target["metadata_only_authority_allowed"] is True
    assert target["sdk_dependency_addition_allowed"] is False
    assert target["dependency_manifest_edit_allowed"] is False
    assert target["lockfile_edit_allowed"] is False
    assert target["vendor_provider_sdk_import_allowed"] is False
    assert target["built_in_provider_sdk_client_implementation_allowed"] is False
    assert target["provider_client_construction_allowed"] is False
    assert target["provider_execution_expansion_allowed"] is False
    assert target["guardian_gate_required"] is True
    assert target["operator_approval_linkage_required"] is True
    assert target["sdk_dependency_declaration_metadata_required"] is True
    assert target["vendor_import_declaration_metadata_required"] is True
    assert target["supply_chain_review_metadata_required"] is True
    assert target["license_security_posture_metadata_required"] is True
    assert target["sanitized_evidence_only_required"] is True
    assert target["credential_reference_metadata_only_required"] is True
    assert target["network_policy_reference_metadata_only_required"] is True
    assert target["endpoint_authority_reference_metadata_only_required"] is True
    assert target["deny_by_default_required"] is True
    assert (
        target[
            "links_v1_g48_v1_g53_v1_g54_v1_g55_v1_g56_v1_g57_v1_g58_evidence_required"
        ]
        is True
    )


def test_v1_g59_target_forbidden_authorities_are_false() -> None:
    target = _load_fixture()[
        "sdk_dependency_vendor_provider_sdk_import_authority_target_if_operator_says_yes"
    ]

    for key in (
        "lima_runtime_file_change_allowed",
        "lima_public_api_change_allowed",
        "consumer_production_runtime_code_edit_allowed",
        "direct_provider_sdk_implementation_allowed",
        "provider_endpoint_resolution_by_lima_allowed",
        "dns_lookup_by_lima_allowed",
        "http_client_by_lima_allowed",
        "socket_client_by_lima_allowed",
        "network_calls_by_lima_allowed",
        "direct_provider_egress_by_lima_allowed",
        "credential_value_access_allowed",
        "secret_lookup_allowed",
        "provider_token_or_api_key_access_allowed",
        "provider_configuration_changes_allowed",
        "fallback_execution_allowed",
        "connector_browser_network_physical_world_allowed",
        "consumer_production_runtime_integration_allowed",
        "product_readiness_claim_allowed",
        "final_public_api_freeze_claim_allowed",
    ):
        assert target[key] is False, key


def test_v1_g59_approved_file_scope_if_approved_is_exact() -> None:
    fixture = _load_fixture()

    assert fixture["approved_lima_runtime_files_if_operator_says_yes"] == []
    assert fixture["approved_lima_docs_tests_fixtures_if_operator_says_yes"] == [
        "docs/V1_G59_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_AUTHORITY.md",
        "docs/V1_G59_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_AUTHORITY_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g59_sdk_dependency_vendor_provider_sdk_import_authority.json",
        "tests/test_v1_g59_sdk_dependency_vendor_provider_sdk_import_authority.py",
    ]
    assert fixture["approved_sparkbot_files_if_operator_says_yes"] == []
    assert fixture["approved_arc_bot_shell_files_if_operator_says_yes"] == []


def test_v1_g59_prior_evidence_refs_exist() -> None:
    for relative_path in _load_fixture()["required_prior_evidence_refs"]:
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_g59_forbidden_boundaries_remain_false_in_request() -> None:
    fixture = _load_fixture()

    for key in (
        "consumer_repo_mutation_added",
        "consumer_runtime_calls_added",
        "consumer_production_runtime_integration_added",
        "live_provider_model_call_execution_added",
        "provider_sdk_network_egress_invocation_added",
        "provider_execution_expansion_added",
        "real_provider_sdk_client_added_by_lima",
        "direct_provider_sdk_added",
        "provider_endpoint_resolution_added",
        "provider_endpoint_resolution_performed",
        "direct_network_code_added",
        "dns_lookup_added",
        "http_client_added",
        "socket_client_added",
        "network_call_performed_by_lima",
        "direct_provider_egress_performed_by_lima",
        "provider_readiness_network_check_added",
        "secret_lookup_added",
        "secret_lookup_performed",
        "credential_value_access_added",
        "credential_value_accessed",
        "provider_token_or_api_key_access_added",
        "provider_token_or_api_key_accessed",
        "credential_storage_rotation_migration_or_provisioning_added",
        "provider_configuration_changes_added",
        "fallback_execution_added",
        "tool_execution_added",
        "connector_browser_network_file_device_robotics_physical_world_behavior_added",
        "raw_prompt_persisted",
        "raw_model_response_persisted",
        "raw_customer_data_persisted",
        "raw_secret_or_credential_persisted",
        "raw_provider_token_or_api_key_persisted",
        "raw_diff_or_patch_persisted",
        "raw_file_content_persisted",
        "product_ready",
        "final_public_api_freeze_approved",
    ):
        assert fixture[key] is False, key

    assert fixture["credential_reference_metadata_only"] is True
    assert fixture["network_policy_metadata_only"] is True
    assert fixture["endpoint_authority_metadata_only"] is True
    assert fixture["sdk_dependency_declaration_metadata_only"] is True
    assert fixture["vendor_import_declaration_metadata_only"] is True
    assert fixture["supply_chain_review_metadata_only"] is True
    assert fixture["license_security_posture_metadata_only"] is True


def test_v1_g59_docs_contain_request_only_boundary_language() -> None:
    fixture = _load_fixture()
    approval_text = (REPO_ROOT / fixture["documents"]["approval_request"]).read_text(
        encoding="utf-8"
    )
    decision_text = (
        REPO_ROOT / fixture["documents"]["operator_decision_packet"]
    ).read_text(encoding="utf-8")
    preflight_text = (REPO_ROOT / fixture["documents"]["preflight_audit"]).read_text(
        encoding="utf-8"
    )
    work_order_text = (REPO_ROOT / fixture["documents"]["work_order"]).read_text(
        encoding="utf-8"
    )

    assert "Approval request packet only: yes" in approval_text
    assert "Implementation approved by this request: no" in approval_text
    assert "SDK dependency added: no" in approval_text
    assert "Dependency manifest edited: no" in approval_text
    assert "Vendor provider SDK import added: no" in approval_text
    assert "Network call performed by LIMA: no" in approval_text
    assert "Direct provider egress performed by LIMA: no" in approval_text
    assert "Recorded choice: none" in decision_text
    assert "Recorded choice: Approve-V1-G59" in decision_text
    assert "Implementation must not start until `Approve-V1-G59`" in preflight_text
    assert "No `lima/` runtime files may be changed." in work_order_text


def test_v1_g59_docs_and_fixture_do_not_include_sensitive_markers() -> None:
    fixture = _load_fixture()
    output = json.dumps(fixture, sort_keys=True)
    for relative_path in fixture["documents"].values():
        output += (REPO_ROOT / relative_path).read_text(encoding="utf-8")

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
