"""Tests for the approved V1-G59 SDK dependency/vendor import authority slice."""

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
    / "v1_g59_sdk_dependency_vendor_provider_sdk_import_authority.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g59_fixture_records_approved_scope_and_status() -> None:
    fixture = _load_fixture()

    assert fixture["packet_set_id"] == (
        "v1_g59_sdk_dependency_vendor_provider_sdk_import_authority"
    )
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g59-sdk-dependency-vendor-provider-sdk-import-authority"
    assert fixture["operator_decision"] == "Approve-V1-G59"
    assert fixture["approved_scope"] == (
        "sdk_dependency_vendor_provider_sdk_import_authority_metadata_slice"
    )
    assert fixture["required_approval_wording"] == (
        "I explicitly approve V1-G59 implementation of the LIMA-side SDK "
        "dependency and vendor provider SDK import authority metadata slice, "
        "limited to the file scope, behavior scope, tests, rollback plan, and "
        "stop conditions in "
        "docs/V1_G59_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_AUTHORITY_APPROVAL_REQUEST.md."
    )
    assert fixture["sdk_dependency_vendor_provider_sdk_import_authority_approved"] is True
    assert fixture["sdk_dependency_vendor_provider_sdk_import_authority_added"] is True
    assert fixture["sdk_dependency_vendor_provider_sdk_import_authority_result"] == (
        "sdk_dependency_vendor_provider_sdk_import_authority_metadata_recorded"
    )
    assert fixture["metadata_only"] is True
    assert fixture["docs_tests_fixtures_only"] is True


def test_v1_g59_lima_file_scope_is_exact_and_runtime_unchanged() -> None:
    fixture = _load_fixture()

    assert fixture["approved_lima_runtime_files_changed"] == []
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["lima_public_api_changed"] is False
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["arc_bot_shell_files_changed"] is False
    assert fixture["approved_lima_docs_tests_fixtures_changed"] == [
        "docs/V1_G59_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_AUTHORITY.md",
        "docs/V1_G59_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_AUTHORITY_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g59_sdk_dependency_vendor_provider_sdk_import_authority.json",
        "tests/test_v1_g59_sdk_dependency_vendor_provider_sdk_import_authority.py",
    ]
    assert fixture["decision_packet_updated"] == (
        "docs/V1_G59_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_AUTHORITY_OPERATOR_DECISION_PACKET.md"
    )

    for relative_path in fixture["approved_lima_docs_tests_fixtures_changed"]:
        assert (REPO_ROOT / relative_path).exists()
    assert (REPO_ROOT / fixture["decision_packet_updated"]).exists()


def test_v1_g59_authority_requirements_are_locked() -> None:
    requirements = _load_fixture()["sdk_dependency_vendor_import_authority_requirements"]

    assert requirements == {
        "guardian_gate_required": True,
        "operator_approval_linkage_required": True,
        "sdk_dependency_declaration_metadata_required": True,
        "vendor_import_declaration_metadata_required": True,
        "supply_chain_review_metadata_required": True,
        "license_security_posture_metadata_required": True,
        "sanitized_evidence_only_required": True,
        "credential_reference_metadata_only_required": True,
        "network_policy_reference_metadata_only_required": True,
        "endpoint_authority_reference_metadata_only_required": True,
        "deny_by_default_required": True,
        "links_v1_g48_v1_g53_v1_g54_v1_g55_v1_g56_v1_g57_v1_g58_evidence_required": True,
        "audit_evidence_metadata_is_not_execution_authority": True,
        "approval_metadata_is_not_broad_execution_authority": True,
    }


def test_v1_g59_dependency_import_and_consumer_runtime_remain_blocked() -> None:
    fixture = _load_fixture()

    assert fixture["sdk_dependency_addition_approved"] is False
    assert fixture["sdk_dependency_added"] is False
    assert fixture["dependency_manifest_edited"] is False
    assert fixture["lockfile_edited"] is False
    assert fixture["vendor_provider_sdk_import_approved"] is False
    assert fixture["vendor_provider_sdk_import_added"] is False
    assert fixture["built_in_provider_sdk_client_implementation_approved"] is False
    assert fixture["built_in_provider_sdk_client_implementation_added"] is False
    assert fixture["provider_client_construction_added"] is False
    assert fixture["provider_execution_expansion_added"] is False
    assert fixture["provider_execution_expansion_approved"] is False
    assert fixture["consumer_repo_mutation_added"] is False
    assert fixture["consumer_runtime_calls_added"] is False
    assert fixture["consumer_production_runtime_integration_added"] is False
    assert fixture["consumer_production_runtime_source_files_changed"] is False
    assert fixture["live_provider_model_call_execution_added"] is False
    assert fixture["provider_sdk_network_egress_invocation_added"] is False

    assert fixture["blocked_future_authorities"] == {
        "sdk_dependency_addition_approved": False,
        "dependency_manifest_edit_approved": False,
        "lockfile_edit_approved": False,
        "vendor_provider_sdk_import_approved": False,
        "built_in_provider_sdk_client_implementation_approved": False,
        "provider_client_construction_approved": False,
        "direct_provider_sdk_implementation_approved": False,
        "provider_secret_lookup_approved": False,
        "provider_credential_value_access_approved": False,
        "lima_owned_provider_endpoint_resolution_approved": False,
        "lima_owned_provider_network_egress_approved": False,
        "fallback_execution_approved": False,
        "connector_browser_network_authority_approved": False,
        "consumer_production_runtime_integration_approved": False,
        "physical_world_authority_approved": False,
        "product_readiness_approved": False,
        "final_public_api_freeze_approved": False,
    }


def test_v1_g59_forbidden_boundaries_remain_false() -> None:
    fixture = _load_fixture()

    for group_name in ("forbidden_boundaries", "sensitive_content_boundaries"):
        for key, value in fixture[group_name].items():
            assert value is False, f"{group_name}.{key}"


def test_v1_g59_future_gates_are_required_before_expansion() -> None:
    fixture = _load_fixture()

    assert fixture["future_required_gates"] == [
        "sdk_dependency_addition_approval_request",
        "dependency_manifest_edit_approval_request",
        "lockfile_edit_approval_request",
        "vendor_provider_sdk_import_approval_request",
        "built_in_provider_sdk_client_implementation_approval_request",
        "provider_client_construction_approval_request",
        "provider_credential_value_access_approval_request",
        "lima_owned_provider_endpoint_resolution_approval_request",
        "lima_owned_provider_network_egress_approval_request",
        "fallback_execution_approval_request",
        "connector_browser_network_authority_approval_request",
        "consumer_production_runtime_integration_approval_request",
        "physical_world_authority_approval_request",
        "product_readiness_approval_request",
        "final_public_api_freeze_approval_request",
    ]
    assert all(fixture["required_confirmations"].values())


def test_v1_g59_accepted_evidence_refs_exist() -> None:
    for relative_path in _load_fixture()["accepted_evidence_refs"]:
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_g59_decision_packet_records_exact_approval() -> None:
    decision_text = (
        REPO_ROOT
        / "docs"
        / "V1_G59_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_AUTHORITY_OPERATOR_DECISION_PACKET.md"
    ).read_text(encoding="utf-8")

    assert "Decision packet status: `approved`" in decision_text
    assert "Recorded choice: Approve-V1-G59" in decision_text
    assert (
        "Recorded approval wording: I explicitly approve V1-G59 implementation "
        "of the LIMA-side SDK dependency and vendor provider SDK import "
        "authority metadata slice, limited to the file scope, behavior scope, "
        "tests, rollback plan, and stop conditions in "
        "docs/V1_G59_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_AUTHORITY_APPROVAL_REQUEST.md."
        in decision_text
    )
    assert (
        "Approved implementation branch: "
        "`v1-g59-sdk-dependency-vendor-provider-sdk-import-authority`"
        in decision_text
    )
    assert "Implementation approved: yes." in decision_text


def test_v1_g59_docs_contain_boundary_language() -> None:
    implementation_text = (
        REPO_ROOT
        / "docs"
        / "V1_G59_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_AUTHORITY.md"
    ).read_text(encoding="utf-8")
    closeout_text = (
        REPO_ROOT
        / "docs"
        / "V1_G59_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_AUTHORITY_CLOSEOUT.md"
    ).read_text(encoding="utf-8")

    assert "metadata-only SDK dependency and vendor provider SDK import authority" in implementation_text
    assert "No `lima/` runtime file" in implementation_text
    assert "SDK dependency added: no" in implementation_text
    assert "Dependency manifest edited: no" in implementation_text
    assert "Lockfile edited: no" in implementation_text
    assert "Vendor provider SDK import added: no" in implementation_text
    assert "Provider client construction added: no" in implementation_text
    assert "Direct provider egress performed by LIMA: no" in implementation_text
    assert "Endpoint-authority metadata only: yes" in implementation_text
    assert "V1-G59 is complete" in closeout_text
    assert "Product readiness claimed: no" in closeout_text
    assert "Final public API freeze claimed: no" in closeout_text


def test_v1_g59_fixture_and_docs_do_not_include_sensitive_markers() -> None:
    fixture = _load_fixture()
    output = json.dumps(fixture, sort_keys=True)
    output += (
        REPO_ROOT
        / "docs"
        / "V1_G59_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_AUTHORITY.md"
    ).read_text(encoding="utf-8")
    output += (
        REPO_ROOT
        / "docs"
        / "V1_G59_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_AUTHORITY_CLOSEOUT.md"
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
