"""Static checks for the V1 final readiness audit template."""

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
    / "v1_final_readiness_audit_template.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_final_readiness_template_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["template_id"] == "v1_final_readiness_audit_template"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["date"] == "2026-06-22"
    assert fixture["branch"] == "docs-v1-post-g60-readiness-and-next-lane-matrix"
    assert fixture["observed_workspace_branch"] == (
        "docs-v1-post-g60-readiness-and-next-lane-matrix"
    )
    assert fixture["source_lima_commit_before_template"] == (
        "37626bf236bf96c8a57a3ca351668e90eeb0e651"
    )
    assert fixture["template_verdict"] == (
        "READY_TO_RUN_FINAL_AUDIT_AFTER_RELEASE_CHECKLIST_REFRESH"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_final_readiness_template_requires_unblocks_before_pass() -> None:
    fixture = _load_fixture()

    assert fixture["required_unblocks_before_pass"] == {
        "exactly_one_v1_g61_operator_decision_recorded": True,
        "g61_implementation_complete_if_approved": True,
        "current_validation_refresh_rerun_after_g61_outcome": True,
        "post_validation_readiness_doc_fixture_test_changes_have_same_turn_validation_or_are_absent": True,
        "release_candidate_acceptance_checklist_blockers_closed": False,
        "release_candidate_cutover_preconditions_satisfied_not_executed_by_template": False,
        "arc_bot_shell_clean_checkpoint_proof_recorded_before_pass_branch_tag_cutover_or_readiness_claim": True,
    }
    assert fixture["required_repository_evidence"] == [
        "lima_ai_os_branch_and_commit_under_audit",
        "public_sparkbot_branch_and_target_publication_proof",
        "accessible_sparkbot_branch_and_pushed_commit",
        "arc_bot_shell_branch_and_pushed_commit",
        "arc_bot_shell_clean_checkpoint_proof_recorded_at_clean_pushed_commit_99a4ba4955f13626c2176a2c44592000029a16c3_before_release_candidate_final_readiness_branch_tag_cutover_or_readiness_claim",
        "candidate_harness_quickstart_execution_audit_state",
        "candidate_harness_quickstart_execution_audit_post_refresh_consumers_8_8_8_lima_17_108_5360_current",
        "release_candidate_acceptance_checklist_state",
        "release_candidate_cutover_runbook_state",
        "current_candidate_validation_refresh_audit_state_including_latest_15_89_5361_supplement_and_8_117_5362_plus_7_64_133_5364_handoff_supplement",
        "post_validation_readiness_change_freshness_audit_state",
        "post_validation_readiness_docs_fixtures_tests_change_disposition_no_later_changes_or_same_turn_validation_evidence_including_5359_full_suite_freshness_latest_quickstart_5360_final_blocker_index_15_89_5361_post_g61_request_8_117_5362_and_quickstart_artifact_7_64_133_5364_freshness",
        "current_gate_consistency_audit_state",
        "g61_decision_state_approve_v1_g61_recorded",
        "g61_operator_decision_packet_status_audit_state",
        "g61_implementation_proof_and_closeout_state",
        "g61_preapproval_runtime_tree_guard_state",
        "post_g61_authorities_remain_blocked_unless_separately_approved",
    ]
def test_v1_final_readiness_template_validation_commands_cover_all_repos() -> None:
    commands = _load_fixture()["required_validation_commands"]

    assert set(commands) == {
        "public_sparkbot",
        "accessible_sparkbot",
        "arc_bot_shell",
        "lima_ai_os",
    }
    assert "test_sparkbot_lima_v1_g56_fake_executor" in commands["public_sparkbot"][0]
    assert commands["public_sparkbot"][1] == "git diff --check"
    assert "test_sparkbot_lima_v1_g56_fake_executor" in commands[
        "accessible_sparkbot"
    ][0]
    assert "test_arc_bot_shell_lima_v1_g56_fake_executor" in commands[
        "arc_bot_shell"
    ][0]
    assert commands["lima_ai_os"] == [
        "python -m compileall lima",
        "python -m pytest -q tests -p no:cacheprovider",
        "git diff --check",
        "git diff --cached --check",
    ]


def test_v1_final_readiness_template_pass_and_fail_criteria_are_explicit() -> None:
    fixture = _load_fixture()

    assert fixture["pass_criteria"] == [
        "exactly_one_valid_g61_decision_recorded_as_approve_v1_g61",
        "release_candidate_acceptance_checklist_satisfied",
        "release_candidate_cutover_runbook_preconditions_satisfied_before_branch_tag_cutover_or_readiness_action",
        "g61_implementation_and_closeout_pass",
        "public_sparkbot_branch_publication_remains_proven",
        "candidate_harness_quickstart_execution_audit_current",
        "candidate_harness_quickstart_execution_audit_post_refresh_consumers_8_8_8_lima_17_108_5360_current",
        "current_candidate_validation_refresh_audit_current_latest_153_5350_15_89_5361_and_8_117_5362_plus_7_64_133_5364_handoff_supplement",
        "post_validation_readiness_change_freshness_audit_current_for_later_readiness_changes",
        "post_validation_readiness_doc_fixture_test_changes_have_same_turn_focused_full_and_diff_check_evidence_including_5359_full_suite_freshness_latest_quickstart_5360_final_blocker_index_15_89_5361_post_g61_request_8_117_5362_and_quickstart_artifact_7_64_133_5364_freshness",
        "current_gate_consistency_audit_current",
        "g61_operator_decision_packet_status_audit_current",
        "public_sparkbot_g56_smoke_passes",
        "accessible_sparkbot_g56_smoke_passes",
        "arc_bot_shell_g56_smoke_passes",
        "arc_bot_shell_clean_checkpoint_proof_current_at_clean_pushed_commit_99a4ba4955f13626c2176a2c44592000029a16c3",
        "arc_bot_shell_clean_checkpoint_proof_recorded_before_release_candidate_final_readiness_branch_tag_cutover_or_readiness_claim",
        "lima_compileall_passes",
        "lima_full_suite_passes",
        "g61_preapproval_runtime_tree_guard_still_passes",
        "all_diff_checks_pass",
        "all_evidence_sanitized",
        "no_forbidden_behavior_or_readiness_claim_added_outside_final_audit_scope",
    ]
    assert fixture["fail_criteria"] == [
        "no_valid_g61_operator_decision_recorded_as_approve_v1_g61",
        "release_candidate_acceptance_checklist_still_reports_blocker",
        "release_candidate_cutover_runbook_still_reports_blocker_before_branch_tag_cutover_or_readiness_action",
        "g61_implementation_missing_despite_approve_v1_g61",
        "g61_implementation_exceeds_approved_file_scope",
        "g61_preapproval_runtime_tree_guard_fails",
        "current_candidate_validation_refresh_audit_missing_stale_or_not_latest_153_5350_15_89_5361_and_8_117_5362_plus_7_64_133_5364_handoff_supplement",
        "post_validation_readiness_change_freshness_audit_missing_stale_or_incomplete_for_later_readiness_changes",
        "post_validation_readiness_doc_fixture_test_changes_lack_same_turn_focused_full_and_diff_check_evidence_including_5359_full_suite_freshness_latest_quickstart_5360_final_blocker_index_15_89_5361_post_g61_request_8_117_5362_and_quickstart_artifact_7_64_133_5364_freshness",
        "current_gate_consistency_audit_fails_or_records_stale_current_state_language",
        "g61_operator_decision_packet_status_audit_missing_stale_or_contradicts_recorded_decision_state",
        "consumer_or_lima_validation_fails",
        "candidate_harness_quickstart_execution_audit_missing_stale_failed_or_lacks_post_refresh_consumers_8_8_8_lima_17_108_5360",
        "arc_bot_shell_clean_checkpoint_proof_missing_stale_or_commit_mismatch_before_v1_release_candidate_final_readiness_branch_tag_cutover_or_readiness_claim",
        "arc_bot_shell_evidence_reverts_to_compatibility_only_without_clean_checkpoint_before_v1_release_candidate_final_readiness_branch_tag_cutover_or_readiness_claim",
        "arc_bot_shell_historical_drift_exclusion_treated_as_release_proof_before_release_candidate_final_readiness_branch_tag_cutover_or_readiness_claim",
        "arc_bot_shell_clean_checkpoint_proof_missing_before_release_candidate_final_readiness_branch_tag_cutover_or_readiness_claim",
        "raw_sensitive_or_patch_content_persisted",
        "forbidden_provider_network_secret_fallback_connector_physical_or_production_behavior_appears",
    ]


def test_v1_final_readiness_template_preserves_boundaries() -> None:
    boundaries = _load_fixture()["boundaries_preserved"]

    for key, value in boundaries.items():
        assert value is False, key


def test_v1_final_readiness_template_future_output_shape_is_bounded() -> None:
    fixture = _load_fixture()

    assert fixture["future_final_audit_output_files"] == [
        "docs/audits/V1_FINAL_READINESS_AUDIT.md",
        "tests/fixtures/runtime_extraction/v1_final_readiness_audit.json",
        "tests/test_v1_final_readiness_audit.py",
    ]
    assert fixture["allowed_future_pass_verdict"] == (
        "PASS_CANDIDATE_READY_FOR_FIRST_CONSUMER_TESTING"
    )
    assert fixture["production_readiness_claim_allowed"] is False


def test_v1_final_readiness_template_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (
        REPO_ROOT / fixture["documents"]["final_readiness_audit_template"]
    ).read_text(encoding="utf-8")

    assert "# V1 Final Readiness Audit Template" in text
    assert fixture["source_lima_commit_before_template"] in text
    assert "READY_TO_RUN_FINAL_AUDIT_AFTER_RELEASE_CHECKLIST_REFRESH" in text
    assert "exactly one V1-G61 operator decision is recorded; current state is `Approve-V1-G61`" in text
    assert "the bounded G61 implementation proof and closeout are complete" in text
    assert "V1_CANDIDATE_HARNESS_QUICKSTART.md" in text
    assert "V1_CANDIDATE_HARNESS_QUICKSTART_EXECUTION_AUDIT.md" in text
    assert "V1_CONSUMER_HARNESS_USABILITY_MATRIX.md" in text
    assert "V1_CONSUMER_CHECKPOINT_MANIFEST.md" in text
    assert "V1_RELEASE_CANDIDATE_ACCEPTANCE_CHECKLIST.md" in text
    assert "V1_RELEASE_CANDIDATE_CUTOVER_RUNBOOK.md" in text
    assert "V1_CURRENT_CANDIDATE_VALIDATION_REFRESH_AUDIT.md" in text
    assert "V1_POST_VALIDATION_READINESS_CHANGE_FRESHNESS_AUDIT.md" in text
    assert "V1_CURRENT_GATE_CONSISTENCY_AUDIT.md" in text
    assert "V1_ARC_BOT_SHELL_LOCAL_DRIFT_EXCLUSION_AUDIT.md" in text
    assert "V1_G61_OPERATOR_DECISION_PACKET_STATUS_AUDIT.md" in text
    assert "V1 release-candidate acceptance checklist state" in text
    assert "V1 release-candidate cutover runbook state" in text
    assert "V1 current candidate validation refresh audit state" in text
    assert "including latest LIMA readiness freshness supplement evidence of 15 focused final blocker/index tests, 89 broader affected V1 readiness tests, and 5361 full-suite tests, plus latest handoff freshness supplement evidence of 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5362/5364 full-suite tests" in text
    assert "V1 post-validation readiness-change freshness audit state" in text
    assert "post-validation readiness docs/fixtures/tests change disposition" in text
    assert "same-turn focused, full-suite, and diff-check validation evidence recorded" in text
    assert "current same-turn full-suite freshness evidence passing 5359 tests after release/cutover freshness checks" in text
    assert "latest final blocker/index refresh evidence passing 15 focused tests, 89 broader affected readiness tests, and 5361 full-suite tests" in text
    assert "latest post-G61 request refresh evidence passing 8 focused tests, 117 broader G61/readiness tests, and 5362 full-suite tests" in text
    assert "latest quickstart artifact refresh evidence passing 7 focused tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5364 full-suite tests" in text
    assert "V1 current gate consistency audit state" in text
    assert "V1 candidate harness quickstart execution audit state" in text
    assert "V1 candidate harness quickstart execution audit post-refresh validation state, including consumers 8/8/8 and LIMA 17/108/5360 tests" in text
    assert "Arc-Bot-shell clean-checkpoint proof state" in text
    assert "Arc-Bot-shell historical local drift exclusion audit state" in text
    assert "clean pushed commit `99a4ba4955f13626c2176a2c44592000029a16c3`" in text
    assert "Arc-Bot-shell clean-checkpoint proof" in text
    assert "V1 release-candidate acceptance checklist is satisfied" in text
    assert "V1 candidate harness quickstart execution audit remains current" in text
    assert "V1 candidate harness quickstart execution audit post-refresh validation remains current and records consumers 8/8/8 plus LIMA 17/108/5360 tests" in text
    assert "V1 current candidate validation refresh audit remains current" in text
    assert "latest focused current-gate validation, full LIMA suite evidence, latest LIMA readiness freshness supplement evidence of 15 focused final blocker/index tests, 89 broader affected V1 readiness tests, and 5361 full-suite tests, and latest handoff freshness supplement evidence of 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5362/5364 full-suite tests" in text
    assert "V1 post-validation readiness-change freshness audit remains current" in text
    assert "same-turn focused validation, full LIMA suite, and diff-check evidence" in text
    assert "same-turn focused validation, full LIMA suite, and diff-check evidence recorded before the audit passes, including current same-turn full-suite freshness evidence passing 5359 tests after release/cutover freshness checks, latest quickstart post-refresh full-suite evidence passing 5360 tests, latest final blocker/index refresh evidence passing 15 focused tests, 89 broader affected readiness tests, and 5361 full-suite tests, latest post-G61 request refresh evidence passing 8 focused tests, 117 broader G61/readiness tests, and 5362 full-suite tests, and latest quickstart artifact refresh evidence passing 7 focused tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5364 full-suite tests" in text
    assert "V1 current gate consistency audit remains current and rejects stale public Sparkbot publication or V1-G57 active-blocker language" in text
    assert "V1 release-candidate cutover runbook preconditions are satisfied before any branch, tag, cutover, or readiness action" in text
    assert "Arc-Bot-shell clean-checkpoint proof remains current at clean pushed commit `99a4ba4955f13626c2176a2c44592000029a16c3`" in text
    assert "Arc-Bot-shell clean-checkpoint proof is recorded before any release-candidate pass, final-readiness pass, branch, tag, cutover, or readiness claim" in text
    assert "V1 release-candidate acceptance checklist still reports a blocker" in text
    assert "V1 current candidate validation refresh audit is missing, stale, or does not record the latest focused current-gate, full-suite, and latest LIMA readiness freshness supplement evidence" in text
    assert "V1 post-validation readiness-change freshness audit is missing, stale, or does not cover readiness docs, fixtures, or tests changed after the current validation refresh" in text
    assert "readiness docs, fixtures, or tests changed after the current validation refresh without same-turn focused validation, full LIMA suite, and diff-check evidence" in text
    assert "V1 candidate harness quickstart execution audit is missing, stale, does not record current post-refresh consumers 8/8/8 plus LIMA 17/108/5360 tests, or records a failed consumer smoke or diff check" in text
    assert "Arc-Bot-shell clean-checkpoint proof is missing, stale, or no longer matches the documented clean pushed commit" in text
    assert "Arc-Bot-shell evidence reverts to compatibility-only smoke without current clean-checkpoint proof before a V1 release-candidate, final-readiness, branch, tag, cutover, or readiness claim" in text
    assert "Arc-Bot-shell historical drift exclusion is treated as release proof instead of superseded compatibility context before a release-candidate pass, final-readiness pass, branch, tag, cutover, or readiness claim" in text
    assert "Arc-Bot-shell clean-checkpoint proof is missing before a release-candidate pass, final-readiness pass, branch, tag, cutover, or readiness claim" in text
    assert "V1 release-candidate cutover runbook still reports a blocker before branch, tag, cutover, or readiness action" in text
    assert "V1_G61_PREAPPROVAL_RUNTIME_TREE_GUARD_AUDIT.md" in text
    assert "V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF.md" in text
    assert "V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_CLOSEOUT.md" in text
    assert "G61 preapproval runtime-tree guard state" in text
    assert "G61 operator decision packet status audit state" in text
    assert "G61 implementation proof and closeout state" in text
    assert "G61 preapproval runtime-tree guard fails" in text
    assert "V1 current gate consistency audit fails or records stale current-state language" in text
    assert "V1-G61 operator decision packet status audit is missing, stale, or contradicts the recorded G61 decision state" in text
    assert "Final audit executed by this template: no." in text
    assert "Release-candidate checklist passed by this template: no." in text
    assert "Release-candidate cutover authorized by this template: no." in text
    assert "Branch or tag action authorized by this template: no." in text
    assert "cutover or readiness-claim authority" in text
    assert "Arc-Bot-shell clean-checkpoint proof created by this template: no." in text
    assert "Stop the final audit and record a blocked verdict" in text
    assert "PASS_CANDIDATE_READY_FOR_FIRST_CONSUMER_TESTING" in text
    assert "must not claim production readiness" in text


def test_v1_final_readiness_template_has_no_sensitive_markers() -> None:
    fixture = _load_fixture()
    output = json.dumps(fixture, sort_keys=True)
    output += (
        REPO_ROOT / fixture["documents"]["final_readiness_audit_template"]
    ).read_text(encoding="utf-8")

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
