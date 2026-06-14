"""Static checks for the V1-G14 implementation blocker audit."""

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
    / "v1_g14_implementation_blocker_audit.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g14_blocker_audit_docs_and_fixture_exist() -> None:
    fixture = _load_fixture()

    assert fixture["audit_id"] == "v1_g14_implementation_blocker_audit"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g14-destructive-approval-enforcement-approval-request"
    assert fixture["source_commit_before_audit"] == (
        "c3f55365b0b37af52b73b4fdb7b25c5a5de22005"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g14_blocker_is_missing_operator_decision() -> None:
    fixture = _load_fixture()
    decision = fixture["decision_record"]

    assert fixture["audit_verdict"] == "BLOCKED_PENDING_OPERATOR_DECISION"
    assert fixture["blocker"] == "missing_valid_approve_v1_g14_decision_record"
    assert fixture["required_unblock_choice"] == "Approve-V1-G14"
    assert fixture["required_approved_branch"] == "v1-g14-destructive-approval-enforcement"
    assert fixture["valid_operator_choices"] == [
        "Approve-V1-G14",
        "Revise-V1-G14",
        "Pause",
    ]
    assert decision["recorded_choice"] == "none"
    assert decision["recorded_approval_wording"] == "none"
    assert decision["approved_implementation_branch"] == "none"
    assert decision["runtime_implementation_approved"] is False


def test_v1_g14_broad_goal_and_request_are_not_approval() -> None:
    not_approval = set(_load_fixture()["inputs_that_are_not_approval"])

    assert "persistent_broad_goal" in not_approval
    assert "v1_g13_recommendation" in not_approval
    assert "v1_g14_approval_request" in not_approval
    assert "v1_g14_preflight_audit" in not_approval
    assert "v1_g14_work_order" in not_approval
    assert "operator_decision_packet_with_recorded_choice_none" in not_approval
    assert "v1_g3_static_destructive_approval_contract" in not_approval
    assert "v1_g11_runtime_request_decision_gate_evidence" in not_approval
    assert "v1_g12_durable_audit_evidence_persistence_evidence" in not_approval
    assert "successful_validation_on_request_branch" in not_approval


def test_v1_g14_only_docs_work_can_continue_without_approval() -> None:
    can_continue = set(_load_fixture()["can_continue_without_approval"])
    cannot_continue = set(_load_fixture()["cannot_continue_without_approval"])

    assert can_continue == {
        "docs_tests_fixtures_review",
        "guard_docs",
        "audit_docs",
        "decision_recording_work",
    }
    assert "v1_g14_runtime_implementation" in cannot_continue
    assert "lima_runtime_file_changes_for_v1_g14" in cannot_continue
    assert "destructive_approval_enforcement_behavior" in cannot_continue
    assert "file_mutation_delete_overwrite_external_file_action_behavior" in cannot_continue
    assert "approval_token_issuance" in cannot_continue
    assert "raw_pin_verification_or_persistence" in cannot_continue
    assert "approval_metadata_as_execution_authority" in cannot_continue
    assert "provider_model_routing" in cannot_continue
    assert "shell_wiring_or_consumer_integration" in cannot_continue
    assert "humaninput_bridge_activation" in cannot_continue
    assert "runtime_export_cleanup" in cannot_continue
    assert "final_api_freeze" in cannot_continue


def test_v1_g14_blocker_audit_preserves_boundaries() -> None:
    boundaries = _load_fixture()["boundaries"]

    assert boundaries["runtime_behavior_added"] is False
    assert boundaries["approval_enforcement_added"] is False
    assert boundaries["file_mutation_behavior_added"] is False
    assert boundaries["approval_tokens_issued"] is False
    assert boundaries["raw_pin_verification_or_persistence_added"] is False
    assert boundaries["external_database_writes_added"] is False
    assert boundaries["lima_runtime_files_changed"] is False
    assert boundaries["provider_model_routing_added"] is False
    assert boundaries["shell_runtime_wiring_added"] is False
    assert boundaries["humaninput_bridge_activated"] is False
    assert boundaries["connector_behavior_added"] is False
    assert boundaries["browser_file_network_device_robotics_physical_world_behavior_added"] is False
    assert boundaries["consumer_repos_touched"] is False
    assert boundaries["sparkbot_touched"] is False
    assert boundaries["sparkbot_shell_touched"] is False
    assert boundaries["arc_bot_shell_touched"] is False
    assert boundaries["lima_robo_os_touched"] is False
    assert boundaries["lima_office_touched"] is False
    assert boundaries["product_ready"] is False
    assert boundaries["production_ready"] is False
    assert boundaries["runtime_export_cleanup_approved"] is False
    assert boundaries["final_api_freeze_approved"] is False


def test_v1_g14_blocker_docs_match_fixture() -> None:
    fixture = _load_fixture()
    guard_text = (
        REPO_ROOT / fixture["documents"]["no_implicit_approval_guard"]
    ).read_text(encoding="utf-8")
    audit_text = (
        REPO_ROOT / fixture["documents"]["implementation_blocker_audit"]
    ).read_text(encoding="utf-8")
    state_text = (REPO_ROOT / fixture["documents"]["current_state"]).read_text(
        encoding="utf-8"
    )

    assert "V1-G14 runtime implementation is blocked pending an explicit operator decision" in audit_text
    assert "The current V1-G14 Decision Record fails the approval evidence test" in guard_text
    assert "Recorded choice: `none`" in audit_text
    assert "Approve-V1-G14" in guard_text
    assert "V1-G14 no implicit runtime approval guard document" in state_text
    assert "V1-G14 implementation blocker status: active until `Approve-V1-G14` is recorded" in state_text
