"""Static checks for the V1-G12 operator-decision readiness guard."""

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
    / "v1_g12_operator_decision_readiness_guard.json"
)
STATE_PATH = REPO_ROOT / "docs" / "CURRENT_PROJECT_STATE.md"


def _load_json(path: Path) -> dict[str, Any]:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g12_operator_decision_readiness_docs_exist() -> None:
    fixture = _load_json(FIXTURE_PATH)
    assert fixture["gap_id"] == "V1-G12"
    assert fixture["guard_id"] == "v1_g12_operator_decision_readiness_guard"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g12-durable-audit-evidence-persistence-approval-request"
    assert fixture["source_commit_before_guard"] == "d47414ef55be46c66112b658467737ab59d35250"
    assert fixture["docs_tests_fixtures_only"] is True
    assert (
        fixture["closeout_verdict"]
        == "ready_for_one_valid_operator_choice_no_choice_recorded"
    )
    assert fixture["guard_status"] == "active_until_approve_v1_g12_recorded"

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g12_operator_decision_record_is_empty_and_fail_closed() -> None:
    decision_record = _load_json(FIXTURE_PATH)["decision_record"]
    assert decision_record["recorded_choice"] is None
    assert decision_record["recorded_approval_wording"] is None
    assert decision_record["recorded_revision_request"] is None
    assert decision_record["recorded_pause_reason"] is None
    assert decision_record["approved_implementation_branch"] is None
    assert decision_record["runtime_implementation_approved"] is False


def test_v1_g12_valid_choices_are_exact() -> None:
    fixture = _load_json(FIXTURE_PATH)
    assert set(fixture["valid_operator_choices"]) == {
        "Approve-V1-G12",
        "Revise-V1-G12",
        "Pause",
    }


def test_v1_g12_no_implicit_approval_inputs_are_rejected() -> None:
    fixture = _load_json(FIXTURE_PATH)
    non_approval_inputs = set(fixture["non_approval_inputs"])
    assert "persistent_broad_goal_to_finish_lima" in non_approval_inputs
    assert "v1_g11_audit_pass" in non_approval_inputs
    assert "v1_g12_approval_request" in non_approval_inputs
    assert "v1_g12_work_order" in non_approval_inputs
    assert "v1_g12_operator_decision_packet_with_none_record" in non_approval_inputs
    assert "v1_g8_v1_g8a_static_persistence_contract_evidence" in non_approval_inputs
    assert "successful_validation_on_request_branch" in non_approval_inputs

    rejected = set(fixture["rejected_claims"])
    assert "runtime_implementation_approved" in rejected
    assert "operator_approval_recorded" in rejected
    assert "durable_persistence_implemented" in rejected
    assert "implicit_approval_from_v1_g11_audit" in rejected
    assert "implicit_approval_from_broad_goal" in rejected
    assert "final_api_freeze_approved" in rejected


def test_v1_g12_authoritative_record_does_not_approve_runtime() -> None:
    fixture = _load_json(FIXTURE_PATH)
    record_ref = fixture["authoritative_approval_record"]
    guarded = _load_json(REPO_ROOT / record_ref["file"])
    decision_record = guarded[record_ref["path"]]

    assert decision_record["recorded_choice"] is None
    assert decision_record["approved_implementation_branch"] is None
    assert decision_record["runtime_implementation_approved"] is False
    assert decision_record["recorded_choice"] != record_ref["required_recorded_choice"]
    assert (
        decision_record["approved_implementation_branch"]
        != record_ref["required_approved_implementation_branch"]
    )


def test_v1_g12_readiness_guard_adds_no_runtime_behavior() -> None:
    boundary = _load_json(FIXTURE_PATH)["boundary_results"]
    for key in (
        "runtime_behavior_added",
        "durable_persistence_added",
        "storage_adapter_added",
        "query_api_added",
        "external_database_writes_added",
        "lima_runtime_files_changed",
        "tests_support_changed",
        "shell_repos_changed",
        "sparkbot_code_copied",
        "sparkbot_import_added",
        "provider_model_routing_added",
        "shell_wiring_added",
        "haptic_device_behavior_added",
        "browser_file_network_device_robotics_physical_world_added",
        "runtime_export_cleanup_approved",
        "final_freeze_approved",
        "v1_product_ready",
        "production_ready",
    ):
        assert boundary[key] is False


def test_v1_g12_readiness_guard_docs_match_fixture() -> None:
    fixture = _load_json(FIXTURE_PATH)
    readiness_text = (REPO_ROOT / fixture["documents"]["readiness_closeout"]).read_text(
        encoding="utf-8"
    )
    guard_text = (REPO_ROOT / fixture["documents"]["no_implicit_approval_guard"]).read_text(
        encoding="utf-8"
    )
    state_text = STATE_PATH.read_text(encoding="utf-8")

    combined = readiness_text + "\n" + guard_text
    for phrase in fixture["doc_required_phrases"]:
        assert phrase in combined

    assert "V1-G12 operator decision readiness closeout document" in state_text
    assert "V1-G12 no implicit runtime approval guard document" in state_text
    assert (
        fixture["recommended_next_step"]
        == "record_exactly_one_valid_operator_choice_in_v1_g12_decision_record"
    )
