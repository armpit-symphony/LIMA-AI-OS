"""Static checks for the V1-G22 final public API freeze request."""

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
    / "v1_g22_final_public_api_freeze_approval_request.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g22_request_docs_and_fixture_exist() -> None:
    fixture = _load_fixture()

    assert fixture["gate_id"] == "v1_g22_final_public_api_freeze_approval_request"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "prepare-v1-g22-final-public-api-freeze-approval-request"

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g22_has_no_implementation_approval_yet() -> None:
    fixture = _load_fixture()
    decision = fixture["decision_record"]

    assert fixture["implementation_approved"] is False
    assert fixture["operator_approval_recorded"] is False
    assert fixture["final_public_api_freeze_implemented"] is False
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["runtime_export_cleanup_approved"] is False
    assert fixture["runtime_export_cleanup_added"] is False
    assert fixture["runtime_behavior_changed"] is False
    assert decision["recorded_choice"] == "none"
    assert decision["approved_implementation_branch"] == "none"
    assert decision["implementation_approved"] is False


def test_v1_g22_exact_decision_options_are_locked() -> None:
    fixture = _load_fixture()

    assert fixture["valid_operator_choices"] == [
        "Approve-V1-G22",
        "Revise-V1-G22",
        "Pause",
    ]
    assert fixture["required_approval_wording"].startswith(
        "I explicitly approve V1-G22 implementation"
    )
    assert fixture["proposed_implementation_branch"] == "v1-g22-final-public-api-freeze"


def test_v1_g22_freeze_families_are_represented() -> None:
    families = set(_load_fixture()["freeze_families"])

    assert "package_public_import_surface_inventory" in families
    assert "subpackage_all_export_inventory" in families
    assert "v1_candidate_runtime_symbol_inventory" in families
    assert "consumer_compatibility_reference_linkage" in families
    assert "import_surface_expectation_linkage" in families
    assert "future_public_api_change_gate" in families
    assert "runtime_export_cleanup_not_approved_confirmation" in families
    assert "no_live_consumer_import_call_confirmation" in families
    assert "no_consumer_repo_mutation_confirmation" in families
    assert "no_runtime_behavior_change_confirmation" in families
    assert "proof_not_authority_confirmation" in families


def test_v1_g22_required_artifact_fields_are_present() -> None:
    fields = set(_load_fixture()["required_artifact_fields"])

    assert "final_api_freeze_packet_id" in fields
    assert "api_status" in fields
    assert "freeze_scope" in fields
    assert "public_package_surfaces" in fields
    assert "public_subpackage_export_surfaces" in fields
    assert "v1_runtime_symbol_surfaces" in fields
    assert "candidate_export_inventory_refs" in fields
    assert "consumer_compatibility_refs" in fields
    assert "import_surface_expectation_refs" in fields
    assert "backward_compatibility_policy" in fields
    assert "future_change_gate_policy" in fields
    assert "runtime_export_cleanup_policy" in fields
    assert "guardian_boundary_confirmation" in fields
    assert "approval_boundary_confirmation" in fields
    assert "provider_model_route_boundary_confirmation" in fields
    assert "no_consumer_repo_mutation_confirmation" in fields
    assert "no_live_import_call_confirmation" in fields
    assert "no_runtime_behavior_change_confirmation" in fields
    assert "no_secret_credential_customer_data_confirmation" in fields
    assert "proof_not_authority_confirmation" in fields
    assert "audit_evidence_linkage" in fields


def test_v1_g22_public_surface_modules_are_locked() -> None:
    assert _load_fixture()["public_surface_modules_to_freeze"] == [
        "lima",
        "lima.contracts",
        "lima.kernel",
        "lima.guardian",
        "lima.spine",
        "lima.persistence",
        "lima.shells.contracts",
        "lima.harness",
        "lima.adapters",
    ]


def test_v1_g22_approved_file_scope_is_docs_tests_fixtures_only() -> None:
    approved_files = set(_load_fixture()["approved_files_if_operator_says_yes"])

    assert approved_files == {
        "docs/V1_G22_FINAL_PUBLIC_API_FREEZE.md",
        "docs/V1_G22_FINAL_PUBLIC_API_FREEZE_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g22_final_public_api_freeze.json",
        "tests/test_v1_g22_final_public_api_freeze.py",
    }
    assert all(not path.startswith("lima/") for path in approved_files)


def test_v1_g22_forbidden_boundaries_remain_false() -> None:
    fixture = _load_fixture()

    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["runtime_export_cleanup_approved"] is False
    assert fixture["runtime_export_cleanup_added"] is False
    assert fixture["consumer_repo_mutation_added"] is False
    assert fixture["consumer_integration_added"] is False
    assert fixture["consumer_runtime_calls_added"] is False
    assert fixture["consumer_code_imports_added"] is False
    assert fixture["shell_runtime_wiring_added"] is False
    assert fixture["provider_model_calls_added"] is False
    assert fixture["secret_lookup_added"] is False
    assert fixture["credential_access_added"] is False
    assert fixture["tool_execution_added"] is False
    assert fixture["runtime_behavior_changed"] is False
    assert fixture[
        "connector_browser_network_file_device_robotics_physical_world_behavior_added"
    ] is False
    assert fixture["product_ready"] is False


def test_v1_g22_docs_contain_final_api_boundary_language() -> None:
    fixture = _load_fixture()
    approval_text = (REPO_ROOT / fixture["documents"]["approval_request"]).read_text(
        encoding="utf-8"
    )
    decision_text = (REPO_ROOT / fixture["documents"]["operator_decision_packet"]).read_text(
        encoding="utf-8"
    )

    assert "final public API freeze" in approval_text
    assert "runtime export cleanup" in approval_text
    assert "No `lima/` runtime files may be created or edited" in approval_text
    assert "Do not edit `lima/` runtime files" in decision_text
    assert "Recorded choice: none" in decision_text
    assert "Recorded choice: Approve-V1-G22" in decision_text
