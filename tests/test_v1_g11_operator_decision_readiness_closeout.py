"""Static checks for the V1-G11 operator decision readiness closeout."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = REPO_ROOT / "docs" / "V1_G11_OPERATOR_DECISION_READINESS_CLOSEOUT.md"
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
    / "v1_g11_operator_decision_readiness_closeout.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g11_operator_decision_readiness_closeout_exists() -> None:
    fixture = _load_fixture()
    assert DOC_PATH.exists()
    assert PACKET_PATH.exists()
    assert STATE_PATH.exists()
    assert fixture["gap_id"] == "V1-G11"
    assert fixture["closeout_id"] == "v1_g11_operator_decision_readiness_closeout"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g11-runtime-slice-approval-request"
    assert (
        fixture["source_commit_before_closeout"]
        == "12f995bce9627bc2290d37b7da4d7149bb672091"
    )
    assert fixture["document"] == "docs/V1_G11_OPERATOR_DECISION_READINESS_CLOSEOUT.md"
    assert (
        fixture["operator_decision_packet"]
        == "docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE_OPERATOR_DECISION_PACKET.md"
    )
    assert (
        fixture["closeout_verdict"]
        == "ready_for_one_valid_operator_choice_no_choice_recorded"
    )


def test_v1_g11_operator_decision_readiness_keeps_decision_record_empty() -> None:
    decision_record = _load_fixture()["decision_record"]
    assert decision_record["recorded_choice"] is None
    assert decision_record["recorded_approval_wording"] is None
    assert decision_record["recorded_revision_request"] is None
    assert decision_record["recorded_pause_reason"] is None
    assert decision_record["approved_implementation_branch"] is None
    assert decision_record["runtime_implementation_approved"] is False


def test_v1_g11_operator_decision_readiness_names_valid_choices_and_evidence() -> None:
    fixture = _load_fixture()
    assert set(fixture["valid_operator_choices"]) == {
        "Approve-V1-G11",
        "Revise-V1-G11",
        "Pause",
    }
    evidence = set(fixture["accepted_readiness_evidence"])
    assert "approval_request_records_exact_question" in evidence
    assert "preflight_audit_records_request_readiness" in evidence
    assert "work_order_records_conditional_implementation_scope" in evidence
    assert "operator_decision_packet_records_valid_choices" in evidence
    assert "decision_record_validation_rules_present" in evidence
    assert "decision_record_templates_present" in evidence
    assert "static_packet_test_verifies_no_approval_boundaries" in evidence


def test_v1_g11_operator_decision_readiness_rejects_runtime_claims() -> None:
    fixture = _load_fixture()
    rejected = set(fixture["rejected_claims"])
    assert "runtime_implementation_approved" in rejected
    assert "operator_approval_recorded" in rejected
    assert "v1_product_readiness_approved" in rejected
    assert "production_readiness_approved" in rejected
    assert "runtime_export_cleanup_approved" in rejected
    assert "final_api_freeze_approved" in rejected
    assert "implicit_approval_from_decision_packet" in rejected
    assert "implicit_approval_from_broad_v1_product_direction" in rejected


def test_v1_g11_operator_decision_readiness_adds_no_runtime_behavior() -> None:
    boundary = _load_fixture()["boundary_results"]
    for key in (
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
    ):
        assert boundary[key] is False


def test_v1_g11_operator_decision_readiness_doc_matches_fixture() -> None:
    fixture = _load_fixture()
    text = DOC_PATH.read_text(encoding="utf-8")
    state = STATE_PATH.read_text(encoding="utf-8")
    assert "V1-G11 is ready for exactly one valid operator choice" in text
    assert "Recorded choice: `none`" in text
    assert "Runtime implementation approved: no" in text
    assert "Any missing, mixed, misspelled, or extra choice value" in text
    assert "Runtime implementation is not approved." in text
    assert "Runtime behavior added: no." in text
    assert "Record exactly one valid operator choice" in text
    assert fixture["recommended_next_step"] == (
        "record_exactly_one_valid_operator_choice_in_decision_record"
    )
    assert "V1-G11 operator decision readiness closeout document" in state
