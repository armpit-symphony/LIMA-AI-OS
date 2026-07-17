"""Tests for the approved V1-G60 SDK dependency/vendor import slice."""

from __future__ import annotations

import ast
import json
import tomllib
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PYPROJECT_PATH = REPO_ROOT / "pyproject.toml"
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g60_sdk_dependency_vendor_provider_sdk_import.json"
)
LIMA_ROOT = REPO_ROOT / "lima"


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _load_pyproject() -> dict[str, Any]:
    return tomllib.loads(PYPROJECT_PATH.read_text(encoding="utf-8"))


def _lima_imported_modules() -> set[str]:
    modules: set[str] = set()
    for path in sorted(LIMA_ROOT.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                modules.add(node.module)
    return modules


def test_v1_g60_fixture_records_approved_scope_and_status() -> None:
    fixture = _load_fixture()

    assert fixture["packet_set_id"] == "v1_g60_sdk_dependency_vendor_provider_sdk_import"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g60-sdk-dependency-vendor-provider-sdk-import"
    assert fixture["operator_decision"] == "Approve-V1-G60"
    assert fixture["approved_scope"] == (
        "sdk_dependency_addition_vendor_provider_sdk_import_approval_slice"
    )
    assert fixture["required_approval_wording"] == (
        "I explicitly approve V1-G60 implementation of the LIMA-side SDK "
        "dependency addition and vendor provider SDK import approval slice, "
        "limited to the file scope, behavior scope, tests, rollback plan, and "
        "stop conditions in "
        "docs/V1_G60_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_APPROVAL_REQUEST.md."
    )
    assert fixture["sdk_dependency_addition_vendor_provider_sdk_import_approved"] is True
    assert fixture["sdk_dependency_added"] is True
    assert fixture["dependency_manifest_edited"] is True
    assert fixture["implementation_result"] == (
        "sdk_dependency_declaration_and_vendor_import_boundary_recorded"
    )
    assert fixture["metadata_and_manifest_only"] is True


def test_v1_g60_pyproject_declares_only_the_approved_dependency() -> None:
    fixture = _load_fixture()
    project = _load_pyproject()["project"]

    assert fixture["approved_dependency_manifest"] == "pyproject.toml"
    assert fixture["approved_dependency_declaration"] == "openai>=1.0.0,<3.0.0"
    assert fixture["approved_vendor_provider_sdk_module"] == "openai"
    assert project["dependencies"] == []


def test_v1_g60_file_scope_is_exact_and_runtime_unchanged() -> None:
    fixture = _load_fixture()

    assert fixture["approved_lima_runtime_files_changed"] == []
    assert fixture["approved_dependency_manifest_files_changed"] == ["pyproject.toml"]
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["lima_public_api_changed"] is False
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["arc_bot_shell_files_changed"] is False
    assert fixture["approved_lima_docs_tests_fixtures_changed"] == [
        "docs/V1_G60_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT.md",
        "docs/V1_G60_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g60_sdk_dependency_vendor_provider_sdk_import.json",
        "tests/test_v1_g60_sdk_dependency_vendor_provider_sdk_import.py",
    ]
    assert fixture["decision_packet_updated"] == (
        "docs/V1_G60_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_OPERATOR_DECISION_PACKET.md"
    )

    for relative_path in fixture["approved_dependency_manifest_files_changed"]:
        assert (REPO_ROOT / relative_path).exists()
    for relative_path in fixture["approved_lima_docs_tests_fixtures_changed"]:
        assert (REPO_ROOT / relative_path).exists()
    assert (REPO_ROOT / fixture["decision_packet_updated"]).exists()


def test_v1_g60_vendor_import_boundary_does_not_touch_lima_runtime() -> None:
    fixture = _load_fixture()
    imported_modules = _lima_imported_modules()

    assert fixture["vendor_provider_sdk_import_boundary_approved"] is True
    assert fixture["vendor_provider_sdk_import_boundary_recorded"] is True
    assert fixture["vendor_provider_sdk_runtime_import_added_to_lima"] is False
    assert fixture["runtime_import_execution_claimed"] is False
    assert "openai" not in imported_modules


def test_v1_g60_authority_requirements_are_locked() -> None:
    requirements = _load_fixture()["dependency_and_import_requirements"]

    assert requirements == {
        "guardian_gate_required": True,
        "operator_approval_linkage_required": True,
        "supply_chain_review_metadata_required": True,
        "license_security_posture_metadata_required": True,
        "dependency_name_version_constraint_metadata_required": True,
        "vendor_import_declaration_metadata_required": True,
        "sanitized_evidence_only_required": True,
        "credential_reference_metadata_only_required": True,
        "network_policy_reference_metadata_only_required": True,
        "endpoint_authority_reference_metadata_only_required": True,
        "deny_by_default_required": True,
        "links_v1_g48_v1_g53_v1_g54_v1_g55_v1_g56_v1_g57_v1_g58_v1_g59_evidence_required": True,
        "audit_evidence_metadata_is_not_execution_authority": True,
        "approval_metadata_is_not_broad_execution_authority": True,
    }


def test_v1_g60_future_authorities_remain_blocked() -> None:
    fixture = _load_fixture()

    assert fixture["lockfile_edited"] is False
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

    for key, value in fixture["blocked_future_authorities"].items():
        assert value is False, key


def test_v1_g60_forbidden_boundaries_remain_false() -> None:
    fixture = _load_fixture()

    for group_name in ("forbidden_boundaries", "sensitive_content_boundaries"):
        for key, value in fixture[group_name].items():
            assert value is False, f"{group_name}.{key}"


def test_v1_g60_future_gates_are_required_before_expansion() -> None:
    fixture = _load_fixture()

    assert fixture["future_required_gates"] == [
        "runtime_vendor_sdk_import_execution_approval_request",
        "built_in_provider_sdk_client_implementation_approval_request",
        "provider_client_construction_approval_request",
        "provider_credential_value_access_approval_request",
        "provider_token_or_api_key_access_approval_request",
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


def test_v1_g60_accepted_evidence_refs_exist() -> None:
    for relative_path in _load_fixture()["accepted_evidence_refs"]:
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_g60_decision_packet_records_exact_approval() -> None:
    decision_text = (
        REPO_ROOT
        / "docs"
        / "V1_G60_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_OPERATOR_DECISION_PACKET.md"
    ).read_text(encoding="utf-8")

    assert "Decision packet status: `approved`" in decision_text
    assert "Recorded choice: Approve-V1-G60" in decision_text
    assert (
        "Recorded approval wording: I explicitly approve V1-G60 implementation "
        "of the LIMA-side SDK dependency addition and vendor provider SDK import "
        "approval slice, limited to the file scope, behavior scope, tests, "
        "rollback plan, and stop conditions in "
        "docs/V1_G60_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_APPROVAL_REQUEST.md."
        in decision_text
    )
    assert (
        "Approved implementation branch: "
        "`v1-g60-sdk-dependency-vendor-provider-sdk-import`"
        in decision_text
    )
    assert "Implementation approved: yes." in decision_text


def test_v1_g60_docs_contain_boundary_language() -> None:
    implementation_text = (
        REPO_ROOT / "docs" / "V1_G60_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT.md"
    ).read_text(encoding="utf-8")
    closeout_text = (
        REPO_ROOT
        / "docs"
        / "V1_G60_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_CLOSEOUT.md"
    ).read_text(encoding="utf-8")

    assert "Approved dependency declaration: `openai>=1.0.0,<3.0.0`" in closeout_text
    assert "No `lima/` runtime file" in implementation_text
    assert "SDK dependency added to `pyproject.toml`: yes" in implementation_text
    assert "Lockfile edited: no" in implementation_text
    assert "Runtime vendor SDK import added to `lima/`: no" in implementation_text
    assert "Provider client construction added: no" in implementation_text
    assert "Network call performed by LIMA: no" in implementation_text
    assert "Direct provider egress performed by LIMA: no" in implementation_text
    assert "V1-G60 is complete" in closeout_text
    assert "Product readiness claimed: no" in closeout_text
    assert "Final public API freeze claimed: no" in closeout_text


def test_v1_g60_fixture_and_docs_do_not_include_sensitive_markers() -> None:
    fixture = _load_fixture()
    output = json.dumps(fixture, sort_keys=True)
    output += (
        REPO_ROOT / "docs" / "V1_G60_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT.md"
    ).read_text(encoding="utf-8")
    output += (
        REPO_ROOT
        / "docs"
        / "V1_G60_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_CLOSEOUT.md"
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
