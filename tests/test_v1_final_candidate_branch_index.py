"""Static checks for the 11 final candidate branch index."""

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
    / "v1_final_candidate_branch_index.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_final_candidate_branch_index_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["index_id"] == "v1_final_candidate_branch_index"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["date"] == "2026-06-21"
    assert fixture["branch"] == "docs-v1-post-g60-readiness-and-next-lane-matrix"
    assert fixture["observed_workspace_branch"] == (
        "docs-v1-post-g60-readiness-and-next-lane-matrix"
    )
    assert fixture["source_lima_commit_before_index"] == (
        "37626bf236bf96c8a57a3ca351668e90eeb0e651"
    )
    assert fixture["index_verdict"] == (
        "CANDIDATE_INDEX_READY_WITH_G61_OPERATOR_BLOCKER"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_final_candidate_branch_index_records_lima_checkpoints() -> None:
    checkpoints = _load_fixture()["lima_branch_checkpoints"]

    assert [checkpoint["branch"] for checkpoint in checkpoints] == [
        "docs-v1-post-g60-readiness-and-next-lane-matrix",
        "prepare-v1-g61-runtime-vendor-sdk-import-execution-proof-approval-request",
        "audit-v1-g61-runtime-vendor-sdk-import-execution-proof-approval-request",
        "audit-v1-g61-preapproval-runtime-tree-guard",
        "docs-v1-post-g61-request-readiness-refresh",
        "audit-v1-g61-operator-decision-packet-status",
        "docs-v1-candidate-harness-quickstart-execution-audit",
        "audit-v1-current-gate-consistency",
        "audit-v1-post-validation-readiness-change-freshness",
        "audit-v1-arc-bot-shell-local-drift-exclusion",
        "docs-v1-release-candidate-acceptance-checklist",
        "docs-v1-release-candidate-cutover-runbook",
        "docs-v1-final-blocker-index-freshness",
        "docs-v1-post-g61-request-readiness-freshness",
        "docs-v1-quickstart-artifact-freshness",
        "docs-v1-handoff-freshness",
        "v1-g61-runtime-vendor-sdk-import-execution-proof",
    ]
    assert [checkpoint["commit_or_label"] for checkpoint in checkpoints] == [
        "37626bf236bf96c8a57a3ca351668e90eeb0e651",
        "request-stage lane label",
        "audit lane label",
        "guard audit label",
        "readiness lane label",
        "status audit lane label",
        "quickstart audit lane label",
        "consistency audit lane label",
        "freshness audit lane label",
        "Arc drift audit lane label",
        "checklist lane label",
        "runbook lane label",
        "freshness supplement label",
        "latest request freshness supplement label",
        "latest quickstart artifact freshness supplement label",
        "latest handoff freshness supplement label",
        "proposed future implementation branch",
    ]


def test_v1_final_candidate_branch_index_records_consumer_checkpoints() -> None:
    consumers = _load_fixture()["consumer_checkpoints"]

    public_sparkbot = consumers["public_sparkbot_target_checkout"]
    assert public_sparkbot["local_path"] == "C:\\Users\\limap\\Sparkbot-public"
    assert public_sparkbot["branch"] == "v1-g56-runtime-authority-chain-audit"
    assert public_sparkbot["commit"] == (
        "ae5cc9c563ea2b0f08c91af03164a78b4b20e3e2"
    )
    assert "publication_resolved_by_audit" in public_sparkbot["status"]

    accessible_sparkbot = consumers["accessible_sparkbot_checkpoint"]
    assert accessible_sparkbot["local_path"] == "C:\\Users\\limap\\Sparkbot"
    assert accessible_sparkbot["commit"] == (
        "ddaa4ccaacd328ddcc1f00a040c2c140abee428e"
    )
    assert accessible_sparkbot["status"] == "clean_local_branch_tracking_origin"

    arc_bot_shell = consumers["arc_bot_shell_checkpoint"]
    assert arc_bot_shell["local_path"] == "C:\\Users\\limap\\Arc-Bot-shell"
    assert arc_bot_shell["commit"] == "2b95eaf11920c7c7163c5ca5a5cc4e5b3f8753c0"
    assert arc_bot_shell["status"] == (
        "checkpoint_commit_tracks_origin_unrelated_local_worktree_drift_excluded_from_v1_proof_same_day_approved_g56_smoke_proof_paths_clean"
    )

    assert _load_fixture()["current_validation_evidence"] == {
        "consumer_quickstart_smoke_refresh_public_accessible_arc_tests": [8, 8, 8],
        "arc_bot_shell_same_day_approved_g56_smoke_proof_paths_clean": True,
        "lima_post_validation_readiness_freshness_full_suite_tests": 5359,
        "lima_quickstart_post_refresh_focused_tests": 17,
        "lima_quickstart_post_refresh_broader_v1_tests": 108,
        "lima_quickstart_post_refresh_full_suite_tests": 5360,
        "lima_latest_final_blocker_index_refresh_focused_tests": 15,
        "lima_latest_final_blocker_index_refresh_broader_v1_tests": 89,
        "lima_latest_final_blocker_index_refresh_full_suite_tests": 5361,
        "lima_latest_post_g61_request_readiness_refresh_focused_tests": 8,
        "lima_latest_post_g61_request_readiness_refresh_broader_v1_tests": 117,
        "lima_latest_post_g61_request_readiness_refresh_full_suite_tests": 5362,
        "lima_latest_quickstart_artifact_refresh_focused_tests": 7,
        "lima_latest_quickstart_artifact_refresh_adjacent_tests": 64,
        "lima_latest_quickstart_artifact_refresh_broader_v1_tests": 133,
        "lima_latest_quickstart_artifact_refresh_full_suite_tests": 5364,
        "lima_latest_handoff_freshness_post_g61_request_focused_tests": 8,
        "lima_latest_handoff_freshness_post_g61_request_broader_v1_tests": 117,
        "lima_latest_handoff_freshness_post_g61_request_full_suite_tests": 5362,
        "lima_latest_handoff_freshness_quickstart_focused_tests": 7,
        "lima_latest_handoff_freshness_quickstart_adjacent_tests": 64,
        "lima_latest_handoff_freshness_quickstart_broader_v1_tests": 133,
        "lima_latest_handoff_freshness_quickstart_full_suite_tests": 5364,
    }

    drift = _load_fixture()["arc_bot_shell_local_drift_exclusion"]
    assert drift == {
        "audit_document": "docs/audits/V1_ARC_BOT_SHELL_LOCAL_DRIFT_EXCLUSION_AUDIT.md",
        "tracked_modified_file_count": 7,
        "untracked_file_count": 64,
        "release_candidate_final_readiness_proof": False,
        "same_day_approved_g56_smoke_proof_paths_clean": True,
        "clean_checkpoint_proof_recorded": True,
    }


def test_v1_final_candidate_branch_index_requires_external_unblocks() -> None:
    fixture = _load_fixture()

    assert fixture["required_current_unblocks"] == [
        "g61_operator_decision_packet_status_audit_current_and_consistent_with_recorded_decision_state",
        "g61_preapproval_runtime_tree_guard_audit_current_and_passing",
        "if_approve_v1_g61_then_runtime_vendor_sdk_import_execution_proof_scope_complete",
        "release_candidate_acceptance_checklist_passed",
        "release_candidate_cutover_authorized_after_final_readiness_pass",
        "final_readiness_audit_executed_and_passed",
    ]
    assert fixture["valid_v1_g61_choices"] == [
        "Approve-V1-G61",
        "Revise-V1-G61",
        "Pause",
    ]
    assert fixture["post_unblock_sequence"] == [
        "rerun_public_sparkbot_g56_smoke_and_diff_check",
        "rerun_accessible_sparkbot_g56_smoke_and_diff_check",
        "rerun_arc_bot_shell_g56_smoke_and_diff_check",
        "refresh_candidate_harness_quickstart_execution_audit",
        "refresh_current_gate_consistency_audit",
        "refresh_post_validation_readiness_change_freshness_audit_if_readiness_docs_fixtures_or_static_tests_change_after_validation_refresh",
        "refresh_g61_operator_decision_packet_status_audit",
        "refresh_g61_preapproval_runtime_tree_guard_audit",
        "rerun_lima_compileall_full_suite_and_diff_checks",
        "refresh_current_candidate_validation_refresh_audit",
        "refresh_final_blocker_register_and_branch_index_freshness_after_later_readiness_edits",
        "preserve_focused_g61_implementation_test_and_closeout_as_bounded_local_proof",
        "refresh_arc_bot_shell_local_drift_exclusion_audit_if_arc_drift_changes_before_final_readiness",
        "confirm_arc_bot_shell_clean_checkpoint_proof_remains_current_before_release_final_branch_tag_cutover_or_readiness_claim",
        "run_final_readiness_audit_on_separate_branch",
        "if_checklist_final_audit_and_cutover_authorization_pass_use_cutover_runbook_before_branch_tag_cutover_or_readiness",
    ]


def test_v1_final_candidate_branch_index_preserves_boundaries() -> None:
    boundaries = _load_fixture()["boundaries_preserved"]

    for key, value in boundaries.items():
        assert value is False, key


def test_v1_final_candidate_branch_index_stop_conditions_are_bounded() -> None:
    assert _load_fixture()["stop_conditions"] == [
        "v1_g61_implementation_without_exact_approval",
        "treat_this_index_as_g61_approval",
        "treat_this_index_as_release_candidate_branch_or_tag_authority",
        "treat_this_index_as_passed_release_candidate_checklist_cutover_or_final_readiness_audit",
        "treat_arc_candidate_smoke_as_clean_checkpoint_proof_while_local_drift_excluded",
        "consumer_repo_edit_from_index_lane",
        "runtime_or_public_api_change_from_index_lane",
        "runtime_vendor_sdk_import_lockfile_secret_credential_token_sdk_endpoint_network_or_fallback_required",
        "raw_sensitive_or_patch_content_persistence",
        "v1_product_production_or_completion_claim",
    ]


def test_v1_final_candidate_branch_index_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (
        REPO_ROOT / fixture["documents"]["final_candidate_branch_index"]
    ).read_text(encoding="utf-8")

    assert "# V1 Final Candidate Branch Index" in text
    assert fixture["source_lima_commit_before_index"] in text
    assert "CANDIDATE_INDEX_READY_WITH_G61_OPERATOR_BLOCKER" in text
    assert "docs-v1-post-g60-readiness-and-next-lane-matrix" in text
    assert "audit-v1-g61-preapproval-runtime-tree-guard" in text
    assert "audit-v1-g61-operator-decision-packet-status" in text
    assert "docs-v1-release-candidate-cutover-runbook" in text
    assert "docs-v1-release-candidate-acceptance-checklist" in text
    assert "docs-v1-final-blocker-index-freshness" in text
    assert "docs-v1-post-g61-request-readiness-freshness" in text
    assert "docs-v1-quickstart-artifact-freshness" in text
    assert "docs-v1-handoff-freshness" in text
    assert "docs-v1-candidate-harness-quickstart-execution-audit" in text
    assert "audit-v1-current-gate-consistency" in text
    assert "audit-v1-post-validation-readiness-change-freshness" in text
    assert "audit-v1-arc-bot-shell-local-drift-exclusion" in text
    assert "V1_CANDIDATE_HARNESS_QUICKSTART_EXECUTION_AUDIT.md" in text
    assert "V1_CURRENT_GATE_CONSISTENCY_AUDIT.md" in text
    assert "V1_CURRENT_CANDIDATE_VALIDATION_REFRESH_AUDIT.md" in text
    assert "V1_POST_VALIDATION_READINESS_CHANGE_FRESHNESS_AUDIT.md" in text
    assert "V1_ARC_BOT_SHELL_CLEAN_CHECKPOINT_PROOF.md" in text
    assert "V1_RELEASE_CANDIDATE_ACCEPTANCE_CHECKLIST.md" in text
    assert "V1_G61_OPERATOR_DECISION_PACKET_STATUS_AUDIT.md" in text
    assert "V1_G61_PREAPPROVAL_RUNTIME_TREE_GUARD_AUDIT.md" in text
    assert "V1_RELEASE_CANDIDATE_CUTOVER_RUNBOOK.md" in text
    assert "This index is not release-candidate branch or tag authority" in text
    assert "NOT_RELEASE_CANDIDATE_FINAL_READINESS_AND_CUTOVER_BLOCKERS" in text
    assert "CUTOVER_BLOCKED_AT_FINAL_READINESS_AND_OPERATOR_AUTHORIZATION" in text
    assert "future audit scaffolding only" in text
    assert "Arc-Bot-shell clean checkpoint: recorded at clean pushed commit `99a4ba4955f13626c2176a2c44592000029a16c3`" in text
    assert "LIMA quickstart post-refresh validation: passed, 17 focused quickstart/handoff tests, 108 broader V1 harness/readiness tests, and 5360 full-suite tests." in text
    assert "LIMA latest final blocker/index readiness refresh: passed, 15 focused final blocker/index tests, 89 broader affected V1 readiness tests, and 5361 full-suite tests." in text
    assert "LIMA latest post-G61 request readiness-refresh: passed, 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, and 5362 full-suite tests." in text
    assert "LIMA latest quickstart artifact refresh: passed, 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5364 full-suite tests." in text
    assert "LIMA latest handoff freshness supplement: passed, 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5362/5364 full-suite tests." in text
    assert "Arc-Bot-shell clean-checkpoint proof: recorded at clean pushed commit `99a4ba4955f13626c2176a2c44592000029a16c3`; release-candidate/final-readiness authority remains blocked." in text
    assert "clean pushed commit `99a4ba4955f13626c2176a2c44592000029a16c3`" in text
    assert "historical Arc-Bot-shell local drift as compatibility-only context" in text
    assert "Run the final readiness audit after release checklist refresh, then require explicit cutover authorization before any branch, tag, cutover, or readiness claim" in text
    assert "must remain current and consistent with the recorded decision state" in text
    assert "must remain current and passing before any final readiness audit, release-candidate branch, tag, cutover, or readiness claim" in text
    assert "Re-run or refresh `docs/audits/V1_G61_PREAPPROVAL_RUNTIME_TREE_GUARD_AUDIT.md`" in text
    assert "Re-run or refresh `docs/audits/V1_POST_VALIDATION_READINESS_CHANGE_FRESHNESS_AUDIT.md`" in text
    assert "Refresh final blocker/register and branch-index freshness evidence after any later readiness edits" in text
    assert "Confirm `docs/audits/V1_ARC_BOT_SHELL_CLEAN_CHECKPOINT_PROOF.md` remains current before final-readiness evaluation." in text
    assert "sparkpit-labs/Sparkbot" in text
    assert "clean checkpoint proof recorded" in text
    assert "Approve-V1-G61" in text
    assert "Public Sparkbot G56 branch pushed to `sparkpit-labs/Sparkbot`: yes." in text
    assert "Release-candidate branch or tag authority created by this index: no." in text
    assert "Release-candidate cutover authorized by this index: no." in text
    assert "Final readiness audit executed or passed by this index: no." in text
    assert "Arc-Bot-shell clean-checkpoint proof claimed by this index: no." in text
    assert "treat this index as release-candidate branch or tag authority" in text
    assert "treat this index as a passed release-candidate checklist" in text
    assert "treat Arc-Bot-shell local candidate smoke evidence as a substitute for the recorded clean-checkpoint proof" in text
    assert "If the release-candidate acceptance checklist and final readiness audit pass" in text
    assert "Additional V1-G61 implementation approval recorded by this index: no." in text
    assert "V1.0 completion, product readiness, or production readiness claimed: no." in text


def test_v1_final_candidate_branch_index_has_no_sensitive_markers() -> None:
    fixture = _load_fixture()
    output = json.dumps(fixture, sort_keys=True)
    output += (
        REPO_ROOT / fixture["documents"]["final_candidate_branch_index"]
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
