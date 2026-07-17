"""Static checks for the V1-G23 consumer import dry-run request."""

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
    / "v1_g23_consumer_integration_proof_to_import_dry_run_approval_request.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g23_request_docs_and_fixture_exist() -> None:
    fixture = _load_fixture()

    assert fixture["gate_id"] == (
        "v1_g23_consumer_integration_proof_to_import_dry_run_approval_request"
    )
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == (
        "prepare-v1-g23-consumer-integration-proof-to-import-dry-run-approval-request"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g23_has_no_implementation_approval_yet() -> None:
    fixture = _load_fixture()
    decision = fixture["decision_record"]

    assert fixture["implementation_approved"] is False
    assert fixture["operator_approval_recorded"] is False
    assert fixture["consumer_import_dry_run_behavior_added"] is False
    assert fixture["consumer_repo_mutation_added"] is False
    assert fixture["consumer_integration_added"] is False
    assert fixture["consumer_runtime_calls_added"] is False
    assert fixture["consumer_code_imports_added"] is False
    assert fixture["runtime_export_cleanup_approved"] is False
    assert decision["recorded_choice"] == "none"
    assert decision["approved_implementation_branch"] == "none"
    assert decision["implementation_approved"] is False


def test_v1_g23_exact_decision_options_are_locked() -> None:
    fixture = _load_fixture()

    assert fixture["valid_operator_choices"] == [
        "Approve-V1-G23",
        "Revise-V1-G23",
        "Pause",
    ]
    assert fixture["required_approval_wording"].startswith(
        "I explicitly approve V1-G23 implementation"
    )
    assert fixture["proposed_implementation_branch"] == (
        "v1-g23-consumer-integration-proof-to-import-dry-run"
    )


def test_v1_g23_import_plan_families_are_represented() -> None:
    families = set(_load_fixture()["import_plan_families"])

    assert "consumer_proof_packet_linkage" in families
    assert "consumer_compatibility_packet_linkage" in families
    assert "frozen_public_api_surface_linkage" in families
    assert "proposed_import_statements_metadata_only" in families
    assert "proposed_call_sites_metadata_only" in families
    assert "adapter_boundary_mapping" in families
    assert "guardian_boundary_mapping" in families
    assert "approval_boundary_mapping" in families
    assert "provider_model_route_boundary_mapping" in families
    assert "no_live_import_call_confirmation" in families
    assert "no_consumer_repo_mutation_confirmation" in families
    assert "no_runtime_export_cleanup_confirmation" in families
    assert "proof_not_authority_confirmation" in families


def test_v1_g23_required_artifact_fields_are_present() -> None:
    fields = set(_load_fixture()["required_artifact_fields"])

    assert "import_plan_id" in fields
    assert "consumer_packet_family" in fields
    assert "consumer_name" in fields
    assert "consumer_repository" in fields
    assert "consumer_branch_ref" in fields
    assert "consumer_commit_sha" in fields
    assert "proof_packet_ref" in fields
    assert "compatibility_packet_ref" in fields
    assert "frozen_api_packet_ref" in fields
    assert "proposed_import_metadata" in fields
    assert "proposed_call_site_metadata" in fields
    assert "adapter_boundary_mapping" in fields
    assert "guardian_boundary_mapping" in fields
    assert "approval_boundary_mapping" in fields
    assert "provider_model_route_boundary_mapping" in fields
    assert "expected_test_command_metadata" in fields
    assert "rollback_metadata" in fields
    assert "no_consumer_repo_mutation_confirmation" in fields
    assert "no_live_import_call_confirmation" in fields
    assert "no_runtime_export_cleanup_confirmation" in fields
    assert "no_raw_content_secret_credential_customer_data_confirmation" in fields
    assert "proof_not_authority_confirmation" in fields
    assert "audit_evidence_linkage" in fields


def test_v1_g23_supported_consumer_families_are_locked() -> None:
    assert _load_fixture()["supported_consumer_packet_families"] == [
        "sparkbot",
        "arc_bot",
        "lima_robo_os",
        "lima_office",
        "future_shell",
    ]


def test_v1_g23_forbidden_boundaries_remain_false() -> None:
    fixture = _load_fixture()

    assert fixture["consumer_repo_mutation_added"] is False
    assert fixture["consumer_integration_added"] is False
    assert fixture["consumer_runtime_calls_added"] is False
    assert fixture["consumer_code_imports_added"] is False
    assert fixture["shell_runtime_wiring_added"] is False
    assert fixture["runtime_export_cleanup_approved"] is False
    assert fixture["provider_model_calls_added"] is False
    assert fixture["secret_lookup_added"] is False
    assert fixture["credential_access_added"] is False
    assert fixture["tool_execution_added"] is False
    assert fixture[
        "connector_browser_network_file_device_robotics_physical_world_behavior_added"
    ] is False
    assert fixture["product_ready"] is False


def test_v1_g23_docs_contain_import_boundary_language() -> None:
    fixture = _load_fixture()
    approval_text = (REPO_ROOT / fixture["documents"]["approval_request"]).read_text(
        encoding="utf-8"
    )
    decision_text = (REPO_ROOT / fixture["documents"]["operator_decision_packet"]).read_text(
        encoding="utf-8"
    )

    assert "consumer repo edits" in approval_text
    assert "live consumer imports/calls" in approval_text
    assert "runtime export cleanup" in approval_text
    assert "Do not edit consumer repos" in decision_text
    assert "Recorded choice: none" in decision_text
    assert "Recorded choice: Approve-V1-G23" in decision_text
