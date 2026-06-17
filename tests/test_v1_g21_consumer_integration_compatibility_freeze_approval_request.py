"""Static checks for the V1-G21 consumer compatibility/freeze request."""

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
    / "v1_g21_consumer_integration_compatibility_freeze_approval_request.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g21_request_docs_and_fixture_exist() -> None:
    fixture = _load_fixture()

    assert fixture["gate_id"] == (
        "v1_g21_consumer_integration_compatibility_freeze_approval_request"
    )
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == (
        "prepare-v1-g21-consumer-integration-compatibility-freeze-approval-request"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g21_has_no_implementation_approval_yet() -> None:
    fixture = _load_fixture()
    decision = fixture["decision_record"]

    assert fixture["implementation_approved"] is False
    assert fixture["operator_approval_recorded"] is False
    assert fixture["consumer_integration_compatibility_freeze_behavior_added"] is False
    assert fixture["consumer_repo_mutation_added"] is False
    assert fixture["consumer_integration_added"] is False
    assert fixture["consumer_runtime_calls_added"] is False
    assert fixture["consumer_code_imports_added"] is False
    assert fixture["final_api_freeze_approved"] is False
    assert fixture["runtime_export_cleanup_approved"] is False
    assert decision["recorded_choice"] == "none"
    assert decision["approved_implementation_branch"] == "none"
    assert decision["implementation_approved"] is False


def test_v1_g21_exact_decision_options_are_locked() -> None:
    fixture = _load_fixture()

    assert fixture["valid_operator_choices"] == [
        "Approve-V1-G21",
        "Revise-V1-G21",
        "Pause",
    ]
    assert fixture["required_approval_wording"].startswith(
        "I explicitly approve V1-G21 implementation"
    )
    assert fixture["proposed_implementation_branch"] == (
        "v1-g21-consumer-integration-compatibility-freeze"
    )


def test_v1_g21_compatibility_families_are_represented() -> None:
    families = set(_load_fixture()["compatibility_families"])

    assert "candidate_export_surface_compatibility" in families
    assert "runtime_symbol_compatibility" in families
    assert "import_surface_expectation_compatibility" in families
    assert "fixture_compatibility_matrix" in families
    assert "version_commit_metadata_compatibility" in families
    assert "guardian_approval_provider_route_boundary_compatibility" in families
    assert "no_live_consumer_runtime_call_confirmation" in families
    assert "no_consumer_repo_mutation_confirmation" in families
    assert "final_public_api_freeze_not_claimed_confirmation" in families


def test_v1_g21_required_artifact_fields_are_present() -> None:
    fields = set(_load_fixture()["required_artifact_fields"])

    assert "compatibility_packet_id" in fields
    assert "consumer_packet_family" in fields
    assert "consumer_name" in fields
    assert "consumer_repository" in fields
    assert "consumer_branch_ref" in fields
    assert "consumer_commit_sha" in fields
    assert "candidate_export_surface_refs" in fields
    assert "runtime_symbol_refs" in fields
    assert "import_surface_expectations" in fields
    assert "fixture_compatibility_matrix" in fields
    assert "version_compatibility_metadata" in fields
    assert "guardian_boundary_compatibility" in fields
    assert "approval_boundary_compatibility" in fields
    assert "provider_model_route_boundary_compatibility" in fields
    assert "consumer_runtime_call_prohibition" in fields
    assert "no_consumer_repo_mutation_confirmation" in fields
    assert "no_live_import_call_confirmation" in fields
    assert "final_public_api_freeze_not_claimed_confirmation" in fields
    assert "audit_evidence_linkage" in fields
    assert "proof_not_authority_confirmation" in fields
    assert "no_raw_content_secret_credential_customer_data_confirmation" in fields
    assert "no_execution_authority_confirmation" in fields


def test_v1_g21_supported_consumer_families_are_locked() -> None:
    assert _load_fixture()["supported_consumer_packet_families"] == [
        "sparkbot",
        "arc_bot",
        "lima_robo_os",
        "lima_office",
        "future_shell",
    ]


def test_v1_g21_forbidden_boundaries_remain_false() -> None:
    fixture = _load_fixture()

    assert fixture["consumer_repo_mutation_added"] is False
    assert fixture["consumer_integration_added"] is False
    assert fixture["consumer_runtime_calls_added"] is False
    assert fixture["consumer_code_imports_added"] is False
    assert fixture["shell_runtime_wiring_added"] is False
    assert fixture["final_api_freeze_approved"] is False
    assert fixture["runtime_export_cleanup_approved"] is False
    assert fixture["provider_model_calls_added"] is False
    assert fixture["secret_lookup_added"] is False
    assert fixture["credential_access_added"] is False
    assert fixture["tool_execution_added"] is False
    assert fixture[
        "connector_browser_network_file_device_robotics_physical_world_behavior_added"
    ] is False
    assert fixture["product_ready"] is False


def test_v1_g21_docs_contain_consumer_boundary_language() -> None:
    fixture = _load_fixture()
    approval_text = (REPO_ROOT / fixture["documents"]["approval_request"]).read_text(
        encoding="utf-8"
    )
    decision_text = (REPO_ROOT / fixture["documents"]["operator_decision_packet"]).read_text(
        encoding="utf-8"
    )

    assert "consumer repo edits" in approval_text
    assert "live consumer imports/calls" in approval_text
    assert "final public API freeze" in approval_text
    assert "Do not edit consumer repos" in decision_text
    assert "Recorded choice: none" in decision_text
    assert "Recorded choice: Approve-V1-G21" in decision_text
