"""Static checks for the V1-G18 consumer proof packet audit intake request."""

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
    / "v1_g18_consumer_proof_packet_audit_intake_approval_request.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g18_request_docs_and_fixture_exist() -> None:
    fixture = _load_fixture()

    assert fixture["gate_id"] == "v1_g18_consumer_proof_packet_audit_intake_approval_request"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "prepare-v1-consumer-proof-packet-audit-intake-approval-request"

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g18_has_no_implementation_approval_yet() -> None:
    fixture = _load_fixture()
    decision = fixture["decision_record"]

    assert fixture["implementation_approved"] is False
    assert fixture["operator_approval_recorded"] is False
    assert fixture["runtime_behavior_added"] is False
    assert fixture["consumer_repo_mutation_added"] is False
    assert fixture["consumer_integration_added"] is False
    assert fixture["consumer_runtime_calls_added"] is False
    assert decision["recorded_choice"] == "none"
    assert decision["approved_implementation_branch"] == "none"
    assert decision["implementation_approved"] is False


def test_v1_g18_exact_decision_options_are_locked() -> None:
    fixture = _load_fixture()

    assert fixture["valid_operator_choices"] == [
        "Approve-V1-G18",
        "Revise-V1-G18",
        "Pause",
    ]
    assert fixture["required_approval_wording"].startswith(
        "I explicitly approve V1-G18 implementation"
    )
    assert fixture["proposed_implementation_branch"] == (
        "v1-g18-consumer-proof-packet-audit-intake"
    )


def test_v1_g18_consumer_packet_families_are_represented() -> None:
    families = set(_load_fixture()["consumer_packet_families"])

    assert "sparkbot" in families
    assert "arc_bot" in families
    assert "lima_robo_os" in families
    assert "lima_office" in families
    assert "future_shell" in families


def test_v1_g18_required_artifact_fields_are_present() -> None:
    fields = set(_load_fixture()["required_artifact_fields"])

    assert "consumer_name" in fields
    assert "consumer_repository" in fields
    assert "consumer_branch_ref" in fields
    assert "consumer_commit_sha" in fields
    assert "proof_packet_path" in fields
    assert "audit_packet_path" in fields
    assert "machine_readable_summary_path" in fields
    assert "validation_commands" in fields
    assert "proposed_import_call_shape_evidence" in fields
    assert "normalized_metadata_examples" in fields
    assert "capability_profile_expectations" in fields
    assert "guardian_approval_boundary_expectations" in fields
    assert "dry_run_non_execution_confirmation" in fields
    assert "no_live_consumer_runtime_path_calls_lima" in fields
    assert "no_bypass_claims" in fields
    assert "independent_audit_required" in fields
    assert "packet_status" in fields


def test_v1_g18_packet_status_ledger_values_are_locked() -> None:
    statuses = _load_fixture()["normalized_packet_statuses"]

    assert statuses == [
        "received",
        "missing",
        "blocked",
        "rejected",
        "accepted_static_evidence",
    ]


def test_v1_g18_forbidden_boundaries_remain_false() -> None:
    fixture = _load_fixture()

    assert fixture["consumer_repo_mutation_added"] is False
    assert fixture["consumer_integration_added"] is False
    assert fixture["consumer_runtime_calls_added"] is False
    assert fixture["provider_model_routing_added"] is False
    assert fixture["connector_browser_network_file_device_robotics_physical_world_behavior_added"] is False
    assert fixture["final_api_freeze_approved"] is False
    assert fixture["product_ready"] is False


def test_v1_g18_docs_contain_consumer_boundary_language() -> None:
    fixture = _load_fixture()
    approval_text = (REPO_ROOT / fixture["documents"]["approval_request"]).read_text(
        encoding="utf-8"
    )
    decision_text = (REPO_ROOT / fixture["documents"]["operator_decision_packet"]).read_text(
        encoding="utf-8"
    )

    assert "Sparkbot proof packet intake" in approval_text
    assert "Arc Bot proof packet intake" in approval_text
    assert "LIMA Robo OS proof packet intake" in approval_text
    assert "LIMA Office proof packet intake" in approval_text
    assert "no live consumer runtime path calls LIMA yet" in approval_text
    assert "Do not touch consumer repos" in decision_text
    assert "Recorded choice: none" in decision_text
    assert "Recorded choice: Approve-V1-G18" in decision_text
