"""Static checks for the V1-G60 SDK dependency/vendor import audit."""

from __future__ import annotations

import ast
import json
import tomllib
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
AUDIT_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g60_sdk_dependency_vendor_provider_sdk_import_audit.json"
)
G60_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g60_sdk_dependency_vendor_provider_sdk_import.json"
)
PYPROJECT_PATH = REPO_ROOT / "pyproject.toml"
LIMA_ROOT = REPO_ROOT / "lima"


def _load_json(path: Path) -> dict[str, Any]:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _load_audit_fixture() -> dict[str, Any]:
    return _load_json(AUDIT_FIXTURE_PATH)


def _load_g60_fixture() -> dict[str, Any]:
    return _load_json(G60_FIXTURE_PATH)


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


def test_v1_g60_audit_fixture_and_docs_exist() -> None:
    fixture = _load_audit_fixture()

    assert fixture["audit_id"] == "v1_g60_sdk_dependency_vendor_provider_sdk_import_audit"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "audit-v1-g60-sdk-dependency-vendor-provider-sdk-import"
    assert fixture["source_branch"] == "v1-g60-sdk-dependency-vendor-provider-sdk-import"
    assert fixture["source_commit_before_audit"] == (
        "1c11061ae1af1cbc850171d7488f6f40c85caee7"
    )
    assert fixture["audit_verdict"] == "PASS"
    assert fixture["operator_decision"] == "Approve-V1-G60"

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path
    for relative_path in fixture["lima_files_reviewed"]:
        assert (REPO_ROOT / relative_path).exists(), relative_path
    for relative_path in fixture["evidence_fixtures_reviewed"]:
        assert (REPO_ROOT / relative_path).exists(), relative_path
    for relative_path in fixture["tests_reviewed"]:
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_g60_audit_matches_implementation_fixture_and_pyproject() -> None:
    audit = _load_audit_fixture()
    g60 = _load_g60_fixture()
    project = tomllib.loads(PYPROJECT_PATH.read_text(encoding="utf-8"))["project"]

    assert g60["operator_decision"] == audit["operator_decision"]
    assert g60["api_status"] == audit["api_status"]
    assert g60["branch"] == audit["source_branch"]
    assert g60["approved_scope"] == audit["approved_scope"]
    assert g60["sdk_dependency_added"] is True
    assert g60["dependency_manifest_edited"] is True
    assert g60["approved_dependency_declaration"] == "openai>=1.0.0,<3.0.0"
    assert g60["approved_dependency_declaration"] not in project["dependencies"]
    assert project["dependencies"] == []
    assert g60["approved_lima_runtime_files_changed"] == audit[
        "lima_runtime_files_reviewed"
    ]
    assert g60["lima_runtime_files_changed"] is False
    assert g60["lima_public_api_changed"] is False
    assert g60["metadata_and_manifest_only"] is True


def test_v1_g60_audit_operator_decision_is_exact() -> None:
    audit = _load_audit_fixture()
    decision_text = (REPO_ROOT / audit["decision_packet_reviewed"]).read_text(
        encoding="utf-8"
    )

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


def test_v1_g60_audit_import_boundary_has_no_lima_runtime_import() -> None:
    audit_results = _load_audit_fixture()["audit_results"]
    imported_modules = _lima_imported_modules()

    assert audit_results["approved_vendor_provider_sdk_module"] == "openai"
    assert audit_results["vendor_provider_sdk_import_boundary_recorded"] is True
    assert audit_results["vendor_provider_sdk_runtime_import_added_to_lima"] is False
    assert audit_results["runtime_import_execution_claimed"] is False
    assert "openai" not in imported_modules


def test_v1_g60_audit_authority_requirements_match_implementation() -> None:
    audit_results = _load_audit_fixture()["audit_results"]
    requirements = _load_g60_fixture()["dependency_and_import_requirements"]

    assert audit_results["guardian_gate_required"] is True
    assert audit_results["operator_approval_linkage_required"] is True
    assert audit_results["supply_chain_review_metadata_required"] is True
    assert audit_results["license_security_posture_metadata_required"] is True
    assert audit_results["deny_by_default_required"] is True
    assert audit_results["credential_reference_metadata_only"] is True
    assert audit_results["network_policy_reference_metadata_only"] is True
    assert audit_results["endpoint_authority_reference_metadata_only"] is True
    assert audit_results["sanitized_evidence_only"] is True
    assert audit_results["audit_evidence_metadata_is_not_execution_authority"] is True
    assert audit_results["approval_metadata_is_not_broad_execution_authority"] is True
    assert requirements["guardian_gate_required"] is True
    assert requirements["operator_approval_linkage_required"] is True
    assert requirements["deny_by_default_required"] is True
    assert requirements[
        "links_v1_g48_v1_g53_v1_g54_v1_g55_v1_g56_v1_g57_v1_g58_v1_g59_evidence_required"
    ]


def test_v1_g60_audit_forbidden_boundaries_remain_false() -> None:
    results = _load_audit_fixture()["audit_results"]

    for key in (
        "vendor_provider_sdk_runtime_import_added_to_lima",
        "lima_runtime_files_changed",
        "lima_public_api_changed",
        "lima_runtime_behavior_added_by_v1_g60",
        "sparkbot_files_changed",
        "arc_bot_shell_files_changed",
        "consumer_production_runtime_source_files_changed",
        "consumer_runtime_calls_added",
        "consumer_integration_added",
        "lockfile_edited",
        "lockfile_edit_approved",
        "built_in_provider_sdk_client_implementation_added",
        "built_in_provider_sdk_client_implementation_approved",
        "provider_client_construction_added",
        "provider_client_construction_approved",
        "provider_execution_expansion_added",
        "provider_execution_expansion_approved",
        "live_provider_model_call_execution_added",
        "direct_provider_sdk_call_implementation_added",
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
        "credential_value_access_added",
        "provider_token_or_api_key_access_added",
        "provider_configuration_changes_added",
        "fallback_execution_added",
        "token_guardian_live_routing_added",
        "human_input_bridge_activated",
        "tool_execution_added",
        "connector_browser_network_file_device_robotics_physical_world_behavior_added",
        "scheduled_task_execution_added",
        "external_send_added",
        "raw_sensitive_content_persisted",
        "product_ready",
        "production_ready",
        "final_public_api_freeze_approved",
    ):
        assert results[key] is False, key


def test_v1_g60_audit_blocked_future_authorities_remain_false() -> None:
    blocked = _load_audit_fixture()["still_blocked_authorities"]

    for key, value in blocked.items():
        assert value is False, key


def test_v1_g60_audit_validation_evidence_is_recorded() -> None:
    fixture = _load_audit_fixture()
    validation = fixture["validation_evidence"]
    audit_validation = fixture["audit_branch_validation_evidence"]

    assert validation["focused_v1_g60_implementation_validation"] == {
        "passed": True,
        "tests_passed": 12,
    }
    assert validation[
        "focused_v1_g60_g59_g58_g57_g56_g55_g54_g53_g48_authority_readiness_validation"
    ] == {
        "passed": True,
        "tests_passed": 351,
    }
    assert validation["compileall_lima"] == {"passed": True}
    assert validation["full_lima_suite"] == {"passed": True, "tests_passed": 5228}
    assert audit_validation["focused_v1_g60_audit_validation"] == {
        "passed": True,
        "tests_passed": 11,
    }
    assert audit_validation["focused_v1_g60_audit_chain_validation"] == {
        "passed": True,
        "tests_passed": 362,
    }
    assert audit_validation["compileall_lima"] == {"passed": True}
    assert audit_validation["full_lima_suite"] == {
        "passed": True,
        "tests_passed": 5239,
    }


def test_v1_g60_audit_docs_contain_required_boundary_language() -> None:
    audit = _load_audit_fixture()
    text = (REPO_ROOT / audit["documents"]["audit"]).read_text(encoding="utf-8")

    assert "Audit verdict: `PASS`" in text
    assert "SDK dependency declaration and vendor provider SDK import-boundary slice" in text
    assert "Approved dependency declaration is `openai>=1.0.0,<3.0.0`: pass." in text
    assert "LIMA `lima/` runtime files changed by V1-G60: none, pass." in text
    assert "Vendor provider SDK runtime import in `lima/` was not added: pass." in text
    assert "Provider client construction remains unapproved and absent: pass." in text
    assert "Direct provider egress by LIMA remains absent: pass." in text
    assert "Final public API freeze remains unapproved: pass." in text
    assert "does not prove installed runtime import execution" in text
    assert "V1-G60 passes independent audit" in text


def test_v1_g60_audit_fixture_and_doc_do_not_include_sensitive_markers() -> None:
    audit = _load_audit_fixture()
    output = json.dumps(audit, sort_keys=True)
    output += (REPO_ROOT / audit["documents"]["audit"]).read_text(encoding="utf-8")

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


def test_v1_g60_audit_next_steps_remain_bounded() -> None:
    fixture = _load_audit_fixture()

    assert fixture["next_recommended_steps"] == [
        "post_g60_readiness_refresh",
        "post_g60_next_lane_decision_matrix",
        "prepare_next_explicit_operator_gate",
    ]
    assert fixture["audit_results"]["product_ready"] is False
    assert fixture["audit_results"]["production_ready"] is False
