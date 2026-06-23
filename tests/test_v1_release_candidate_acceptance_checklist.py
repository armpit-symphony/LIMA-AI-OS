"""Static checks for the V1 release-candidate acceptance checklist."""

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
    / "v1_release_candidate_acceptance_checklist.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_release_candidate_acceptance_checklist_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["checklist_id"] == "v1_release_candidate_acceptance_checklist"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["date"] == "2026-06-22"
    assert fixture["branch"] == "docs-v1-post-g60-readiness-and-next-lane-matrix"
    assert fixture["source_lima_commit_before_checklist"] == (
        "37626bf236bf96c8a57a3ca351668e90eeb0e651"
    )
    assert fixture["checklist_verdict"] == (
        "NOT_RELEASE_CANDIDATE_ARC_CLEAN_CHECKPOINT_AND_FINAL_READINESS_BLOCKERS"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_release_candidate_acceptance_checklist_targets_first_consumers() -> None:
    assert set(_load_fixture()["release_candidate_targets"]) == {
        "Sparkbot_shell",
        "Sparkbot",
        "Arc-Bot-shell",
    }


def test_v1_release_candidate_acceptance_checklist_entry_criteria_cover_release_bar() -> None:
    criteria = set(_load_fixture()["entry_criteria"])

    assert "exactly_one_valid_v1_g61_operator_decision_recorded" in criteria
    assert "if_approve_v1_g61_then_g61_implementation_closeout_and_focused_tests_pass" in criteria
    assert "if_revise_or_pause_then_release_candidate_work_remains_stopped" in criteria
    assert "final_blocker_register_has_no_release_candidate_blocker" in criteria
    assert "final_readiness_audit_executed_and_passed" in criteria
    assert (
        "release_candidate_cutover_authorized_after_checklist_and_final_readiness_pass"
        in criteria
    )
    assert "candidate_harness_quickstart_current" in criteria
    assert "candidate_harness_quickstart_execution_audit_current" in criteria
    assert (
        "candidate_harness_quickstart_execution_audit_same_turn_consumer_refresh_public_accessible_arc_8_each_and_lima_17_108_5360"
        in criteria
    )
    assert "current_candidate_validation_refresh_audit_current" in criteria
    assert "current_candidate_validation_refresh_latest_supplement_15_89_5361_current" in criteria
    assert (
        "current_candidate_validation_refresh_latest_handoff_supplement_8_117_5362_and_7_64_133_5364_current"
        in criteria
    )
    assert "post_validation_readiness_change_freshness_audit_current" in criteria
    assert (
        "post_validation_readiness_change_freshness_latest_final_blocker_index_15_89_5361_current"
        in criteria
    )
    assert (
        "post_validation_readiness_change_freshness_latest_post_g61_request_refresh_8_117_5362_current"
        in criteria
    )
    assert (
        "post_validation_readiness_change_freshness_latest_quickstart_artifact_refresh_7_64_133_5364_current"
        in criteria
    )
    assert "current_gate_consistency_audit_current" in criteria
    assert (
        "g61_operator_decision_packet_status_audit_current_and_approve_v1_g61_recorded"
        in criteria
    )
    assert "consumer_harness_usability_matrix_current" in criteria
    assert "public_sparkbot_target_publication_proven" in criteria
    assert "public_sparkbot_g56_fake_executor_smoke_passes" in criteria
    assert "accessible_sparkbot_g56_fake_executor_smoke_passes" in criteria
    assert "arc_bot_shell_g56_fake_executor_smoke_passes" in criteria
    assert (
        "arc_bot_shell_local_drift_exclusion_audit_current_7_tracked_modified_files_49_untracked_entries_excluded_from_release_proof"
        in criteria
    )
    assert (
        "arc_bot_shell_clean_checkpoint_proof_recorded_after_local_drift_absent_or_resolved_and_revalidated_before_release_final_branch_tag_cutover_or_readiness_claim"
        in criteria
    )
    assert "compileall_lima_passes" in criteria
    assert "focused_current_gate_validation_passes" in criteria
    assert "full_lima_suite_passes" in criteria
    assert "lima_diff_checks_pass" in criteria
    assert "consumer_diff_hygiene_passes" in criteria
    assert "evidence_sanitized" in criteria
    assert (
        "no_forbidden_runtime_provider_network_credential_connector_browser_file_device_robotics_physical_world_or_consumer_production_behavior"
        in criteria
    )


def test_v1_release_candidate_acceptance_checklist_current_state_is_not_release_candidate() -> None:
    state = _load_fixture()["current_criteria_state"]

    assert state["v1_g61_operator_decision_recorded"] is True
    assert state["v1_g61_operator_decision"] == "Approve-V1-G61"
    assert state["v1_g61_implementation_and_closeout_complete_if_approved"] is True
    assert state["v1_g61_runtime_vendor_sdk_import_execution_proof_current"] is True
    assert state["final_blocker_register_clear"] is False
    assert state["final_readiness_audit_executed_and_passed"] is False
    assert state["release_candidate_cutover_authorized"] is False
    assert state["candidate_harness_quickstart_current"] is True
    assert state["candidate_harness_quickstart_execution_audit_current"] is True
    assert (
        state[
            "candidate_harness_quickstart_execution_same_turn_consumer_refresh_public_sparkbot_tests_passed"
        ]
        == 8
    )
    assert (
        state[
            "candidate_harness_quickstart_execution_same_turn_consumer_refresh_accessible_sparkbot_tests_passed"
        ]
        == 8
    )
    assert (
        state[
            "candidate_harness_quickstart_execution_same_turn_consumer_refresh_arc_bot_shell_tests_passed"
        ]
        == 8
    )
    assert (
        state["candidate_harness_quickstart_execution_post_refresh_focused_tests_passed"]
        == 17
    )
    assert (
        state[
            "candidate_harness_quickstart_execution_post_refresh_broader_v1_tests_passed"
        ]
        == 108
    )
    assert (
        state[
            "candidate_harness_quickstart_execution_post_refresh_full_lima_suite_tests_passed"
        ]
        == 5360
    )
    assert (
        state[
            "candidate_harness_quickstart_execution_post_refresh_release_authority_created"
        ]
        is False
    )
    assert state["current_candidate_validation_refresh_audit_current"] is True
    assert state["post_validation_readiness_change_freshness_audit_current"] is True
    assert state["post_validation_readiness_change_freshness_full_lima_suite_tests_passed"] == 5359
    assert (
        state[
            "post_validation_readiness_change_freshness_latest_final_blocker_index_focused_tests_passed"
        ]
        == 15
    )
    assert (
        state[
            "post_validation_readiness_change_freshness_latest_final_blocker_index_broader_tests_passed"
        ]
        == 89
    )
    assert (
        state[
            "post_validation_readiness_change_freshness_latest_final_blocker_index_full_lima_suite_tests_passed"
        ]
        == 5361
    )
    assert (
        state[
            "post_validation_readiness_change_freshness_latest_post_g61_request_refresh_focused_tests_passed"
        ]
        == 8
    )
    assert (
        state[
            "post_validation_readiness_change_freshness_latest_post_g61_request_refresh_broader_tests_passed"
        ]
        == 117
    )
    assert (
        state[
            "post_validation_readiness_change_freshness_latest_post_g61_request_refresh_full_lima_suite_tests_passed"
        ]
        == 5362
    )
    assert (
        state[
            "post_validation_readiness_change_freshness_latest_quickstart_artifact_refresh_focused_tests_passed"
        ]
        == 7
    )
    assert (
        state[
            "post_validation_readiness_change_freshness_latest_quickstart_artifact_refresh_adjacent_tests_passed"
        ]
        == 64
    )
    assert (
        state[
            "post_validation_readiness_change_freshness_latest_quickstart_artifact_refresh_broader_tests_passed"
        ]
        == 133
    )
    assert (
        state[
            "post_validation_readiness_change_freshness_latest_quickstart_artifact_refresh_full_lima_suite_tests_passed"
        ]
        == 5364
    )
    assert state["post_validation_readiness_change_freshness_release_authority_created"] is False
    assert state["current_gate_consistency_audit_current"] is True
    assert state["g61_operator_decision_packet_status_audit_current"] is True
    assert state["consumer_harness_usability_matrix_current"] is True
    assert state["public_sparkbot_publication_proven"] is True
    assert state["public_sparkbot_g56_fake_executor_smoke"] is True
    assert state["accessible_sparkbot_g56_fake_executor_smoke"] is True
    assert state["arc_bot_shell_g56_fake_executor_smoke"] is True
    assert state["arc_bot_shell_local_drift_exclusion_audit_current"] is True
    assert state["arc_bot_shell_local_drift_exclusion_audit_tracked_modified_file_count"] == 7
    assert state["arc_bot_shell_local_drift_exclusion_audit_untracked_file_count"] == 64
    assert state["arc_bot_shell_local_drift_excluded_from_v1_proof"] is True
    assert state["arc_bot_shell_clean_checkpoint_evidence"] is False
    assert state["compileall_lima"] is True
    assert state["focused_current_gate_validation_tests_passed"] == 153
    assert state["full_lima_suite_tests_passed"] == 5350
    assert (
        state[
            "current_candidate_validation_refresh_latest_supplement_focused_final_blocker_index_tests_passed"
        ]
        == 15
    )
    assert (
        state[
            "current_candidate_validation_refresh_latest_supplement_broader_v1_readiness_tests_passed"
        ]
        == 89
    )
    assert (
        state[
            "current_candidate_validation_refresh_latest_supplement_full_lima_suite_tests_passed"
        ]
        == 5361
    )
    assert (
        state[
            "current_candidate_validation_refresh_latest_handoff_supplement_post_g61_request_focused_tests_passed"
        ]
        == 8
    )
    assert (
        state[
            "current_candidate_validation_refresh_latest_handoff_supplement_post_g61_request_broader_tests_passed"
        ]
        == 117
    )
    assert (
        state[
            "current_candidate_validation_refresh_latest_handoff_supplement_post_g61_request_full_lima_suite_tests_passed"
        ]
        == 5362
    )
    assert (
        state[
            "current_candidate_validation_refresh_latest_handoff_supplement_quickstart_focused_tests_passed"
        ]
        == 7
    )
    assert (
        state[
            "current_candidate_validation_refresh_latest_handoff_supplement_quickstart_adjacent_tests_passed"
        ]
        == 64
    )
    assert (
        state[
            "current_candidate_validation_refresh_latest_handoff_supplement_quickstart_broader_tests_passed"
        ]
        == 133
    )
    assert (
        state[
            "current_candidate_validation_refresh_latest_handoff_supplement_quickstart_full_lima_suite_tests_passed"
        ]
        == 5364
    )
    assert (
        state[
            "current_candidate_validation_refresh_latest_supplement_release_authority_created"
        ]
        is False
    )
    assert state["full_lima_suite"] is True
    assert state["lima_diff_hygiene"] is True
    assert state["consumer_diff_hygiene"] is True
    assert state["evidence_sanitized"] is True
    assert state["product_or_production_readiness_approved"] is False

    assert _load_fixture()["release_candidate_claim_allowed"] is False


def test_v1_release_candidate_acceptance_checklist_validation_commands_are_complete() -> None:
    commands = _load_fixture()["validation_commands"]

    assert "test_sparkbot_lima_v1_g56_fake_executor" in commands["public_sparkbot"][0]
    assert commands["public_sparkbot"][1] == "git diff --check"
    assert "test_sparkbot_lima_v1_g56_fake_executor" in commands["accessible_sparkbot"][0]
    assert commands["accessible_sparkbot"][1] == "git diff --check"
    assert "test_arc_bot_shell_lima_v1_g56_fake_executor" in commands["arc_bot_shell"][0]
    assert commands["arc_bot_shell"][1] == "git diff --check"
    assert commands["lima_ai_os"] == [
        "python -m compileall lima",
        "python -m pytest -q tests -p no:cacheprovider",
        "git diff --check",
        "git diff --cached --check",
    ]


def test_v1_release_candidate_acceptance_checklist_preserves_false_boundaries() -> None:
    for key, value in _load_fixture()["required_false_boundaries"].items():
        assert value is False, key


def test_v1_release_candidate_acceptance_checklist_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["checklist"]).read_text(
        encoding="utf-8"
    )

    assert "# V1 Release Candidate Acceptance Checklist" in text
    assert "Date: 2026-06-22" in text
    assert fixture["source_lima_commit_before_checklist"] in text
    assert "NOT_RELEASE_CANDIDATE_ARC_CLEAN_CHECKPOINT_AND_FINAL_READINESS_BLOCKERS" in text
    assert "minimum evidence required before LIMA-AI-OS can be called a V1.0.0 release candidate" in text
    assert "locally testable by Sparkbot and Arc-Bot-shell harnesses only as fake-executor" in text
    assert "V1_CANDIDATE_HARNESS_QUICKSTART.md" in text
    assert "V1_CANDIDATE_HARNESS_QUICKSTART_EXECUTION_AUDIT.md" in text
    assert "V1_CURRENT_CANDIDATE_VALIDATION_REFRESH_AUDIT.md" in text
    assert "V1_POST_VALIDATION_READINESS_CHANGE_FRESHNESS_AUDIT.md" in text
    assert "V1_CURRENT_GATE_CONSISTENCY_AUDIT.md" in text
    assert "V1_G61_OPERATOR_DECISION_PACKET_STATUS_AUDIT.md" in text
    assert "V1_ARC_BOT_SHELL_LOCAL_DRIFT_EXCLUSION_AUDIT.md" in text
    assert "V1_OPERATOR_UNBLOCK_ACTION_PACKET.md" in text
    assert "V1_FINAL_CANDIDATE_BRANCH_INDEX.md" in text
    assert "This checklist is not branch, tag, cutover, final readiness" in text
    assert "Arc-Bot-shell clean-checkpoint proof is recorded after local drift is absent or resolved and revalidated" in text
    assert "V1 candidate harness quickstart remains current as the shortest safe local smoke command path." in text
    assert "V1 candidate harness quickstart execution audit remains current and records public Sparkbot, accessible Sparkbot, and Arc-Bot-shell local smoke passes." in text
    assert "V1 candidate harness quickstart execution audit records the latest same-turn consumer smoke refresh with public Sparkbot, accessible Sparkbot, and Arc-Bot-shell each passing 8 tests" in text
    assert "post-refresh LIMA validation passing 17 focused quickstart/handoff tests, 108 broader V1 harness/readiness tests, and 5360 full-suite tests" in text
    assert "V1 current candidate validation refresh audit remains current" in text
    assert "latest LIMA readiness freshness supplement evidence of 15 focused final blocker/index tests, 89 broader affected V1 readiness tests, and 5361 full-suite tests, and latest handoff freshness supplement evidence of 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5362/5364 full-suite tests" in text
    assert "V1 post-validation readiness-change freshness audit remains current" in text
    assert "same-turn focused, full-suite, and diff-check evidence requirements" in text
    assert "current same-turn full-suite freshness evidence passing 5359 tests after release/cutover freshness checks" in text
    assert "latest final blocker/index refresh evidence passing 15 focused tests, 89 broader affected readiness tests, and 5361 full-suite tests" in text
    assert "latest post-G61 request refresh evidence passing 8 focused tests, 117 broader G61/readiness tests, and 5362 full-suite tests" in text
    assert "latest quickstart artifact refresh evidence passing 7 focused tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5364 full-suite tests" in text
    assert "V1 current gate consistency audit remains current and rejects stale public Sparkbot publication or V1-G57 active-blocker language." in text
    assert "V1-G61 operator decision packet status audit remains current and records `Approve-V1-G61`." in text
    assert "Exactly one valid V1-G61 operator decision is recorded." in text
    assert "V1 final readiness audit is executed and passed." in text
    assert "V1 release-candidate cutover runbook remains blocked" in text
    assert "Arc-Bot-shell clean-checkpoint proof is recorded" in text
    assert "before any release-candidate pass, final-readiness pass, branch, tag, cutover, or readiness claim" in text
    assert "Arc-Bot-shell local drift exclusion audit | satisfied as compatibility evidence only; current audit records 7 tracked modified files and 64 untracked files excluded from release proof; not clean-checkpoint evidence" in text
    assert "the current audit records 7 tracked modified files and 64 untracked files as excluded from release proof" in text
    assert "Final readiness audit executed and passed | not satisfied" in text
    assert "Release-candidate cutover authorized | not satisfied" in text
    assert "Arc-Bot-shell clean-checkpoint proof | not satisfied" in text
    assert "V1-G61 operator decision recorded | satisfied, `Approve-V1-G61` recorded by operator" in text
    assert "V1-G61 implementation and closeout complete if approved | satisfied, bounded local import proof and closeout recorded with focused G61 test and full-suite evidence" in text
    assert "Candidate harness quickstart execution audit current | satisfied" in text
    assert "Candidate harness quickstart post-refresh proof | satisfied, consumers 8/8/8 and LIMA 17/108/5360 tests" in text
    assert "Current candidate validation refresh audit current | satisfied, latest current-gate/release-readiness set 153 tests, full suite 5350 tests, latest LIMA readiness freshness supplement 15/89/5361 tests, and latest handoff freshness supplement 8/117/5362 plus 7/64/133/5364 tests" in text
    assert "Post-validation readiness-change freshness audit current | satisfied, same-turn full-suite freshness evidence 5359 tests" in text
    assert "latest final blocker/index refresh evidence 15/89/5361 tests" in text
    assert "latest post-G61 request refresh evidence 8/117/5362 tests" in text
    assert "latest quickstart artifact refresh evidence 7/64/133/5364 tests" in text
    assert "Current gate consistency audit current | satisfied" in text
    assert "V1-G61 operator decision packet status audit current | satisfied, `Approve-V1-G61` recorded" in text
    assert "LIMA focused current-gate/release-readiness validation | satisfied, 153 tests" in text
    assert "LIMA full suite | satisfied, 5350 tests" in text
    assert "LIMA current validation latest readiness freshness supplement | satisfied, 15 focused final blocker/index tests, 89 broader affected V1 readiness tests, and 5361 full-suite tests" in text
    assert "LIMA current validation latest handoff freshness supplement | satisfied, 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5362/5364 full-suite tests" in text
    assert "LIMA quickstart post-refresh full suite | satisfied, 5360 tests" in text
    assert "LIMA latest final blocker/index refresh full suite | satisfied, 5361 tests" in text
    assert "LIMA latest post-G61 request refresh full suite | satisfied, 5362 tests" in text
    assert "LIMA latest quickstart artifact refresh full suite | satisfied, 5364 tests" in text
    assert "Consumer harness usability matrix current | satisfied" in text
    assert "V1.0.0 release-candidate branch or tag created by this checklist: false." in text
    assert "V1 release-candidate cutover authorized by this checklist: false." in text
    assert "V1 final readiness audit executed or passed by this checklist: false." in text
    assert "Arc-Bot-shell clean-checkpoint proof claimed by this checklist: false." in text
    assert "The next state-changing step is clean Arc-Bot-shell checkpoint proof followed by a future final readiness audit." in text
    assert "Do not create a V1.0.0 release-candidate branch" in text
    assert "until this checklist, the future final readiness audit, and clean Arc-Bot-shell checkpoint proof all pass" in text
    assert "V1_RELEASE_CANDIDATE_CUTOVER_RUNBOOK.md" in text
    assert "That runbook is currently blocked and does not approve cutover." in text


def test_v1_release_candidate_acceptance_checklist_has_no_sensitive_markers() -> None:
    fixture = _load_fixture()
    output = json.dumps(fixture, sort_keys=True)
    output += (REPO_ROOT / fixture["documents"]["checklist"]).read_text(
        encoding="utf-8"
    )

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
