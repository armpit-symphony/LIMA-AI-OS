"""Static checks for the V1 release-candidate cutover runbook."""

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
    / "v1_release_candidate_cutover_runbook.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_release_candidate_cutover_runbook_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["runbook_id"] == "v1_release_candidate_cutover_runbook"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["date"] == "2026-06-28"
    assert fixture["branch"] == "docs-v1-post-g60-readiness-and-next-lane-matrix"
    assert fixture["source_lima_commit_before_runbook_refresh"] == (
        "bfa27f37212a24f0ca3e7d21c37e4ff80192db14"
    )
    assert fixture["runbook_verdict"] == (
        "CUTOVER_BLOCKED_AT_OPERATOR_AUTHORIZATION"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_release_candidate_cutover_runbook_preconditions_are_complete() -> None:
    preconditions = set(_load_fixture()["cutover_preconditions"])

    assert "exactly_one_valid_v1_g61_operator_decision_recorded" in preconditions
    assert "if_g61_approved_then_approved_implementation_and_closeout_complete" in preconditions
    assert "if_g61_revised_or_paused_then_cutover_remains_stopped" in preconditions
    assert "release_candidate_acceptance_checklist_satisfied" in preconditions
    assert (
        "current_candidate_validation_refresh_audit_current_and_records_latest_153_5350_validation_plus_15_89_5361_supplement_and_8_117_5362_plus_7_64_133_5364_handoff_supplement"
        in preconditions
    )
    assert (
        "post_validation_readiness_change_freshness_audit_current_and_records_same_turn_5359_latest_quickstart_5360_final_blocker_index_15_89_5361_post_g61_request_8_117_5362_and_quickstart_artifact_7_64_133_5364_evidence_requirement"
        in preconditions
    )
    assert (
        "latest_quickstart_post_refresh_validation_current_consumers_8_8_8_lima_17_108_5360"
        in preconditions
    )
    assert "current_gate_consistency_audit_current_and_passes" in preconditions
    assert (
        "g61_operator_decision_packet_status_audit_current_and_approve_v1_g61_recorded"
        in preconditions
    )
    assert "final_readiness_audit_passes" in preconditions
    assert "public_sparkbot_accessible_sparkbot_and_arc_bot_shell_smoke_validation_passes" in preconditions
    assert (
        "arc_bot_shell_clean_checkpoint_proof_recorded_at_clean_pushed_commit_99a4ba4955f13626c2176a2c44592000029a16c3_before_release_final_branch_tag_cutover_or_readiness_claim"
        in preconditions
    )
    assert (
        "arc_bot_shell_historical_local_drift_exclusion_superseded_by_clean_checkpoint_proof"
        in preconditions
    )
    assert (
        "arc_bot_shell_clean_checkpoint_proof_recorded_at_clean_pushed_commit_99a4ba4955f13626c2176a2c44592000029a16c3_before_release_final_branch_tag_cutover_or_readiness_claim"
        in preconditions
    )
    assert "lima_compileall_full_suite_and_diff_hygiene_pass" in preconditions
    assert "evidence_sanitized" in preconditions
    assert (
        "no_unapproved_runtime_provider_network_credential_connector_browser_file_device_robotics_physical_world_consumer_production_or_product_readiness_behavior"
        in preconditions
    )


def test_v1_release_candidate_cutover_runbook_current_state_is_blocked() -> None:
    state = _load_fixture()["current_state"]

    assert state["v1_g61_operator_decision_recorded"] is True
    assert state["v1_g61_operator_decision"] == "Approve-V1-G61"
    assert state["g61_implementation_and_closeout_complete_if_approved"] is True
    assert state["g61_runtime_vendor_sdk_import_execution_proof_current"] is True
    assert state["release_candidate_acceptance_checklist_satisfied"] is True
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
    assert state["latest_quickstart_post_refresh_public_sparkbot_tests_passed"] == 8
    assert state["latest_quickstart_post_refresh_accessible_sparkbot_tests_passed"] == 8
    assert state["latest_quickstart_post_refresh_arc_bot_shell_tests_passed"] == 8
    assert state["latest_quickstart_post_refresh_focused_tests_passed"] == 17
    assert state["latest_quickstart_post_refresh_broader_v1_tests_passed"] == 108
    assert state["latest_quickstart_post_refresh_full_lima_suite_tests_passed"] == 5360
    assert state["latest_quickstart_post_refresh_release_authority_created"] is False
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
            "current_candidate_validation_refresh_latest_supplement_cutover_authority_created"
        ]
        is False
    )
    assert state["current_gate_consistency_audit_current"] is True
    assert state["g61_operator_decision_packet_status_audit_current"] is True
    assert state["final_readiness_audit_exists"] is True
    assert state["final_readiness_audit_verdict"] == (
        "BLOCKED_RELEASE_CANDIDATE_CHECKLIST_AND_CUTOVER_AUTHORITY_NOT_SATISFIED"
    )
    assert state["final_readiness_audit_exists_and_passes"] is False
    assert state["final_readiness_reconciliation_audit_exists_and_passes"] is True
    assert state["final_readiness_reconciliation_audit_verdict"] == (
        "PASS_CANDIDATE_READY_FOR_FIRST_CONSUMER_HARNESS_TESTING_CUTOVER_AUTHORIZATION_REQUIRED"
    )
    assert state["final_readiness_audit_lima_full_suite_tests_passed"] == 5391
    assert state["public_sparkbot_candidate_smoke"] is True
    assert state["accessible_sparkbot_candidate_smoke"] is True
    assert state["arc_bot_shell_candidate_smoke"] is True
    assert state["arc_bot_shell_local_drift_exclusion_audit_current"] is True
    assert state["arc_bot_shell_local_drift_exclusion_audit_tracked_modified_file_count"] == 7
    assert state["arc_bot_shell_local_drift_exclusion_audit_untracked_file_count"] == 64
    assert state["arc_bot_shell_local_drift_excluded_from_v1_proof"] is True
    assert state["arc_bot_shell_clean_checkpoint_evidence"] is True
    assert state["arc_bot_shell_clean_checkpoint_commit"] == "99a4ba4955f13626c2176a2c44592000029a16c3"
    assert state["arc_bot_shell_historical_local_drift_exclusion_superseded_by_clean_checkpoint_proof"] is True
    assert state["lima_full_suite"] is True
    assert state["cutover_authorized_by_runbook"] is False
    assert state["release_candidate_branch_creation_allowed"] is False
    assert state["release_candidate_tag_creation_allowed"] is False


def test_v1_release_candidate_cutover_runbook_future_procedure_is_gated() -> None:
    fixture = _load_fixture()

    assert fixture["future_cutover_procedure"] == [
        "confirm_final_readiness_audit_pass_candidate_ready_for_first_consumer_testing",
        "confirm_release_candidate_acceptance_checklist_satisfied",
        "confirm_current_gate_consistency_audit_passes",
        "confirm_g61_operator_decision_packet_status_audit_current_and_consistent_with_decision_state",
        "confirm_consumer_smoke_tests_pass",
        "confirm_arc_bot_shell_clean_checkpoint_proof_recorded_at_clean_pushed_commit_99a4ba4955f13626c2176a2c44592000029a16c3",
        "confirm_historical_arc_drift_exclusion_is_superseded_compatibility_context_only",
        "confirm_current_candidate_validation_refresh_latest_153_5350_15_89_5361_and_8_117_5362_plus_7_64_133_5364_handoff_supplement_evidence",
        "confirm_post_validation_readiness_change_freshness_same_turn_5359_latest_quickstart_5360_final_blocker_index_15_89_5361_post_g61_request_8_117_5362_and_quickstart_artifact_7_64_133_5364_evidence",
        "confirm_lima_compileall_full_suite_and_diff_checks_pass",
        "confirm_git_status_clean_except_intentional_release_candidate_metadata",
        "create_release_candidate_branch_only_after_operator_approval",
        "create_v1_0_0_release_candidate_tag_only_after_operator_approval",
        "record_branch_tag_identifiers_in_future_cutover_audit",
    ]
    assert fixture["future_cutover_audit_files"] == [
        "docs/audits/V1_RELEASE_CANDIDATE_CUTOVER_AUDIT.md",
        "tests/fixtures/runtime_extraction/v1_release_candidate_cutover_audit.json",
        "tests/test_v1_release_candidate_cutover_audit.py",
    ]


def test_v1_release_candidate_cutover_runbook_preserves_false_boundaries() -> None:
    for key, value in _load_fixture()["required_false_boundaries"].items():
        assert value is False, key


def test_v1_release_candidate_cutover_runbook_records_stop_conditions() -> None:
    assert _load_fixture()["stop_conditions"] == [
        "v1_g61_implementation_without_exact_approval",
        "treat_runbook_as_g61_approval",
        "treat_runbook_as_passed_release_candidate_checklist_cutover_or_final_readiness_audit",
        "treat_arc_candidate_smoke_as_substitute_for_recorded_clean_checkpoint_proof",
        "release_candidate_branch_or_tag_before_checklist_final_audit_and_explicit_operator_authorization",
        "consumer_repo_edit_from_runbook_lane",
        "runtime_or_public_api_change_from_runbook_lane",
        "runtime_vendor_sdk_import_lockfile_secret_credential_token_sdk_endpoint_network_or_fallback_required",
        "raw_sensitive_or_patch_content_persistence",
        "v1_product_production_or_completion_claim",
    ]


def test_v1_release_candidate_cutover_runbook_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["runbook"]).read_text(
        encoding="utf-8"
    )

    assert "# V1 Release Candidate Cutover Runbook" in text
    assert fixture["source_lima_commit_before_runbook_refresh"] in text
    assert "CUTOVER_BLOCKED_AT_OPERATOR_AUTHORIZATION" in text
    assert "PASS_CANDIDATE_READY_FOR_FIRST_CONSUMER_HARNESS_TESTING_CUTOVER_AUTHORIZATION_REQUIRED" in text
    assert "controlled path from the current V1 candidate evidence set" in text
    assert "V1_CURRENT_CANDIDATE_VALIDATION_REFRESH_AUDIT.md" in text
    assert "V1_CURRENT_GATE_CONSISTENCY_AUDIT.md" in text
    assert "V1_G61_OPERATOR_DECISION_PACKET_STATUS_AUDIT.md" in text
    assert "V1_ARC_BOT_SHELL_LOCAL_DRIFT_EXCLUSION_AUDIT.md" in text
    assert "V1_OPERATOR_UNBLOCK_ACTION_PACKET.md" in text
    assert "V1_FINAL_CANDIDATE_BRANCH_INDEX.md" in text
    assert "This runbook is not itself cutover authority" in text
    assert "post-validation readiness-change freshness audit" in text
    assert "V1-G61 operator decision recorded | satisfied, `Approve-V1-G61` recorded by operator" in text
    assert "G61 implementation and closeout complete if approved | satisfied, bounded local import proof and closeout recorded" in text
    assert "Current candidate validation refresh audit current | satisfied, latest current-gate/release-readiness set 153 tests, full suite 5350 tests, latest LIMA readiness freshness supplement 15/89/5361 tests, and latest handoff freshness supplement 8/117/5362 plus 7/64/133/5364 tests" in text
    assert "Post-validation readiness-change freshness audit current | satisfied, same-turn full-suite freshness evidence 5359 tests" in text
    assert "latest final blocker/index refresh evidence 15/89/5361 tests" in text
    assert "latest post-G61 request refresh evidence 8/117/5362 tests" in text
    assert "latest quickstart artifact refresh evidence 7/64/133/5364 tests" in text
    assert "latest quickstart post-refresh full-suite evidence passing 5360 tests" in text
    assert "latest final blocker/index refresh evidence passing 15 focused tests, 89 broader affected readiness tests, and 5361 full-suite tests" in text
    assert "latest post-G61 request refresh evidence passing 8 focused tests, 117 broader G61/readiness tests, and 5362 full-suite tests" in text
    assert "latest quickstart artifact refresh evidence passing 7 focused tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5364 full-suite tests" in text
    assert "Latest quickstart post-refresh validation | satisfied, consumers 8/8/8 and LIMA 17/108/5360 tests" in text
    assert "LIMA full suite | satisfied at current validation checkpoint; latest validation-refresh supplement full-suite evidence 5361 tests; latest handoff freshness supplement full-suite evidence 5362/5364 tests; latest quickstart post-refresh full-suite evidence 5360 tests; latest final blocker/index refresh full-suite evidence 5361 tests; latest post-G61 request refresh full-suite evidence 5362 tests; latest quickstart artifact refresh full-suite evidence 5364 tests" in text
    assert "Current gate consistency audit current | satisfied" in text
    assert "V1-G61 operator decision packet status audit current | satisfied, `Approve-V1-G61` recorded" in text
    assert "Final readiness audit exists | satisfied" in text
    assert "Final readiness reconciliation audit passes | satisfied" in text
    assert "Arc-Bot-shell local drift exclusion audit | historical compatibility evidence only; superseded by clean-checkpoint proof for release-gate evaluation" in text
    assert "Arc-Bot-shell clean-checkpoint proof | satisfied, clean pushed commit `99a4ba4955f13626c2176a2c44592000029a16c3` recorded in `docs/audits/V1_ARC_BOT_SHELL_CLEAN_CHECKPOINT_PROOF.md`" in text
    assert "Cutover authorized by this runbook | blocked pending explicit operator authorization" in text
    assert "Confirm Arc-Bot-shell clean-checkpoint proof remains recorded" in text
    assert "historical Arc-Bot-shell local drift exclusion evidence is treated only as superseded compatibility context" in text
    assert "Confirm Arc-Bot-shell evidence is not treated as release-candidate, final-readiness, branch, tag, cutover, or readiness evidence unless the clean checkpoint proof remains current" in text
    assert "not current release-candidate evidence" in text
    assert "Release-candidate branch creation | blocked" in text
    assert "Release-candidate tag creation | blocked" in text
    assert "Create a release-candidate branch only after operator approval" in text
    assert "Confirm the current gate consistency audit still passes" in text
    assert "Confirm the G61 operator decision packet status audit is current and consistent with the recorded decision state." in text
    assert "Confirm the current candidate validation refresh audit records the latest focused current-gate validation, full-suite evidence, latest LIMA readiness freshness supplement evidence of 15 focused final blocker/index tests, 89 broader affected V1 readiness tests, and 5361 full-suite tests, and latest handoff freshness supplement evidence of 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5362/5364 full-suite tests." in text
    assert "Confirm the post-validation readiness-change freshness audit covers later readiness docs, fixtures, or tests with same-turn focused, full-suite, and diff-check evidence, including current same-turn full-suite freshness evidence of 5359 tests after release/cutover freshness checks, latest quickstart post-refresh full-suite evidence of 5360 tests, latest final blocker/index refresh evidence of 15 focused tests, 89 broader affected readiness tests, and 5361 full-suite tests, latest post-G61 request refresh evidence of 8 focused tests, 117 broader G61/readiness tests, and 5362 full-suite tests, and latest quickstart artifact refresh evidence of 7 focused tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5364 full-suite tests." in text
    assert "Create a V1.0.0 release-candidate tag only after operator approval" in text
    assert "V1_RELEASE_CANDIDATE_CUTOVER_AUDIT.md" in text
    assert "V1.0.0 release-candidate branch created by this runbook: false." in text
    assert "V1.0.0 release-candidate tag created by this runbook: false." in text
    assert "V1 release-candidate cutover authorized by this runbook: false." in text
    assert "V1 final readiness audit executed by this runbook: false." in text
    assert "V1 final readiness audit passed by this runbook: false." in text
    assert "Arc-Bot-shell clean-checkpoint proof created by this runbook: false." in text
    assert "treat this runbook as release cutover authorization" in text
    assert "treat Arc-Bot-shell local candidate smoke evidence as a substitute for the recorded clean-checkpoint proof" in text
    assert "before the checklist and final audit pass and explicit branch/tag authorization is recorded" not in text
    assert "Keep cutover blocked." in text
    assert "The checklist/final-readiness loop is reconciled for first-consumer harness testing" in text


def test_v1_release_candidate_cutover_runbook_has_no_sensitive_markers() -> None:
    fixture = _load_fixture()
    output = json.dumps(fixture, sort_keys=True)
    output += (REPO_ROOT / fixture["documents"]["runbook"]).read_text(
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
