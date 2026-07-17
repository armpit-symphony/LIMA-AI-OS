"""Static checks for the V1-G11 broad-goal non-approval audit."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = REPO_ROOT / "docs" / "V1_G11_BROAD_GOAL_NON_APPROVAL_AUDIT.md"
STATE_PATH = REPO_ROOT / "docs" / "CURRENT_PROJECT_STATE.md"
PACKET_PATH = (
    REPO_ROOT
    / "docs"
    / "V1_G11_RUNTIME_REQUEST_DECISION_GATE_OPERATOR_DECISION_PACKET.md"
)
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g11_broad_goal_non_approval_audit.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g11_broad_goal_non_approval_audit_exists() -> None:
    fixture = _load_fixture()
    assert DOC_PATH.exists()
    assert PACKET_PATH.exists()
    assert fixture["gap_id"] == "V1-G11"
    assert fixture["audit_id"] == "v1_g11_broad_goal_non_approval_audit"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g11-runtime-slice-approval-request"
    assert (
        fixture["source_commit_before_audit"]
        == "27291969071307f837c44bfa375f4e36add58aa3"
    )
    assert fixture["document"] == "docs/V1_G11_BROAD_GOAL_NON_APPROVAL_AUDIT.md"
    assert (
        fixture["operator_decision_packet"]
        == "docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE_OPERATOR_DECISION_PACKET.md"
    )


def test_v1_g11_broad_goal_is_direction_not_runtime_approval() -> None:
    fixture = _load_fixture()
    assert fixture["audited_input_class"] == "broad_v1_product_objective_continuation"
    assert fixture["accepted_as_product_direction"] is True
    assert fixture["accepted_as_v1_g11_runtime_approval"] is False
    assert fixture["decision_record_required_for_approval"] is True
    required = fixture["required_approve_record"]
    assert required["recorded_choice"] == "Approve-V1-G11"
    assert required["recorded_approval_wording_must_match_packet"] is True
    assert required["recorded_revision_request"] == "none"
    assert required["recorded_pause_reason"] == "none"
    assert required["approved_implementation_branch"] == "v1-g11-runtime-request-decision-gate"
    assert required["runtime_implementation_approved"] == "yes"


def test_v1_g11_broad_goal_keeps_current_decision_record_empty() -> None:
    decision_record = _load_fixture()["current_decision_record"]
    assert decision_record["recorded_choice"] is None
    assert decision_record["recorded_approval_wording"] is None
    assert decision_record["recorded_revision_request"] is None
    assert decision_record["recorded_pause_reason"] is None
    assert decision_record["approved_implementation_branch"] is None
    assert decision_record["runtime_implementation_approved"] is False


def test_v1_g11_broad_goal_records_approval_evidence_failures() -> None:
    failures = set(_load_fixture()["approval_evidence_failures"])
    assert "not_recorded_in_decision_record" in failures
    assert "recorded_choice_not_approve_v1_g11" in failures
    assert "exact_required_approval_wording_not_recorded" in failures
    assert "approved_implementation_branch_not_recorded" in failures
    assert "runtime_implementation_approved_not_yes" in failures
    assert "decision_record_remains_empty" in failures


def test_v1_g11_broad_goal_accepts_product_direction_only() -> None:
    direction = set(_load_fixture()["accepted_direction"])
    assert "first_consumers_sparkbot_shell_sparkbot_arc_bot_shell" in direction
    assert "shell_haptics_acceptable_future_shell_experience" in direction
    assert "live_approval_and_real_guardian_decision_acceptable_future_v1_runtime_requirement" in (
        direction
    )
    assert "provider_model_routing_acceptable_future_v1_runtime_requirement" in direction
    assert "destructive_edit_delete_requires_operator_approval_in_lima_and_shells" in direction
    assert "sparkbot_remains_r_and_d_behavior_reference" in direction


def test_v1_g11_broad_goal_rejects_runtime_and_release_claims() -> None:
    rejected = set(_load_fixture()["rejected_claims"])
    assert "v1_g11_runtime_implementation_approved" in rejected
    assert "runtime_export_cleanup_approved" in rejected
    assert "final_api_freeze_approved" in rejected
    assert "provider_model_runtime_routing_approved" in rejected
    assert "shell_wiring_approved" in rejected
    assert "haptic_device_behavior_in_lima_approved" in rejected
    assert "production_readiness_approved" in rejected


def test_v1_g11_broad_goal_adds_no_runtime_behavior() -> None:
    boundary = _load_fixture()["boundary_results"]
    for key in (
        "runtime_implementation_approved",
        "operator_approval_recorded",
        "runtime_behavior_added",
        "lima_runtime_files_changed",
        "tests_support_changed",
        "shell_repos_changed",
        "sparkbot_code_copied",
        "sparkbot_import_added",
        "provider_model_routing_added",
        "shell_wiring_added",
        "persistence_added",
        "haptic_device_behavior_added",
        "browser_file_network_device_robotics_physical_world_added",
        "runtime_export_cleanup_approved",
        "final_freeze_approved",
        "v1_product_ready",
        "production_ready",
    ):
        assert boundary[key] is False


def test_v1_g11_broad_goal_non_approval_doc_matches_fixture() -> None:
    fixture = _load_fixture()
    text = DOC_PATH.read_text(encoding="utf-8")
    state = STATE_PATH.read_text(encoding="utf-8")
    packet = PACKET_PATH.read_text(encoding="utf-8")
    assert "This audit records that the active broad V1 product objective is product direction only." in text
    assert "It is not a valid V1-G11 operator decision" in text
    assert "The broad V1 product objective fails the V1-G11 approval evidence test" in text
    assert "Result: no approval recorded." in text
    assert "Runtime implementation approved: no." in text
    assert "The broad objective remains accepted as product direction" in text
    assert "The broad objective does not approve V1-G11 runtime implementation." in text
    assert "Record exactly one valid operator choice" in text
    assert fixture["recommended_next_step"] == (
        "record_exactly_one_valid_operator_choice_in_decision_record"
    )
    assert "V1-G11 broad goal non-approval audit document" in state
    assert "General V1 product direction" in packet
