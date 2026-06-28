"""Static checks for the V1 current candidate validation refresh audit."""

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
    / "v1_current_candidate_validation_refresh_audit.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_current_candidate_validation_refresh_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["audit_id"] == "v1_current_candidate_validation_refresh_audit"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["date"] == "2026-06-20"
    assert fixture["branch"] == "docs-v1-post-g60-readiness-and-next-lane-matrix"
    assert fixture["observed_workspace_branch"] == (
        "docs-v1-post-g60-readiness-and-next-lane-matrix"
    )
    assert fixture["source_lima_commit_before_audit"] == (
        "37626bf236bf96c8a57a3ca351668e90eeb0e651"
    )
    assert fixture["audit_verdict"] == (
        "LOCAL_CANDIDATE_VALIDATION_REFRESH_PASS_WITH_G61_OPERATOR_BLOCKER"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_current_candidate_validation_refresh_records_repository_state() -> None:
    state = _load_fixture()["repository_state_under_refresh"]

    assert state["lima_ai_os"]["branch"] == (
        "docs-v1-post-g60-readiness-and-next-lane-matrix"
    )
    assert state["lima_ai_os"]["commit"] == (
        "37626bf236bf96c8a57a3ca351668e90eeb0e651"
    )
    assert state["public_sparkbot_target_checkout"]["commit"] == (
        "ae5cc9c563ea2b0f08c91af03164a78b4b20e3e2"
    )
    assert "publication_resolved_by_audit" in state["public_sparkbot_target_checkout"][
        "state"
    ]
    assert state["accessible_sparkbot_checkpoint"]["state"] == (
        "clean_local_branch_tracking_origin"
    )
    assert state["arc_bot_shell_checkpoint"]["commit"] == (
        "2b95eaf11920c7c7163c5ca5a5cc4e5b3f8753c0"
    )
    assert state["arc_bot_shell_checkpoint"]["state"] == (
        "checkpoint_commit_tracks_origin_unrelated_local_worktree_drift_excluded_from_v1_proof"
    )


def test_v1_current_candidate_validation_refresh_records_consumer_validation() -> None:
    results = _load_fixture()["consumer_validation_results"]

    assert results["public_sparkbot_target_checkout"]["smoke_result"] == "8 passed"
    assert results["public_sparkbot_target_checkout"]["diff_check_result"] == (
        "passed_clean"
    )
    assert results["accessible_sparkbot_checkpoint"]["smoke_result"] == "8 passed"
    assert results["accessible_sparkbot_checkpoint"]["diff_check_result"] == (
        "passed_clean"
    )
    assert results["arc_bot_shell_checkpoint"]["smoke_result"] == "8 passed"
    assert results["arc_bot_shell_checkpoint"]["diff_check_result"] == (
        "passed_with_lf_crlf_warnings_only_not_clean_checkpoint_evidence"
    )

    assert "test_sparkbot_lima_v1_g56_fake_executor" in results[
        "public_sparkbot_target_checkout"
    ]["smoke_command"]
    assert "test_arc_bot_shell_lima_v1_g56_fake_executor" in results[
        "arc_bot_shell_checkpoint"
    ]["smoke_command"]


def test_v1_current_candidate_validation_refresh_keeps_g61_blocker() -> None:
    fixture = _load_fixture()

    assert fixture["active_blockers_remaining"] == [
        "release_candidate_acceptance_checklist_not_passed",
        "release_candidate_cutover_not_authorized",
        "final_readiness_audit_not_executed_or_passed",
        "arc_bot_shell_clean_checkpoint_proof_recorded_as_release_gate_input_only",
    ]
    assert fixture["evidence_interpretation"] == [
        "public_sparkbot_local_checkout_still_validates_fake_executor_path",
        "public_sparkbot_target_publication_resolved",
        "accessible_sparkbot_checkpoint_still_validates_fake_executor_path",
        "arc_bot_shell_checkpoint_still_validates_fake_executor_path_with_local_drift_excluded",
        "v1_candidate_harness_quickstart_execution_audit_current",
        "v1_current_gate_consistency_audit_current",
        "v1_current_gate_consistency_audit_committed_stale_claim_rejection_proof",
        "v1_g61_operator_decision_packet_status_audit_current_approve_recorded_bounded_proof_only",
        "v1_release_candidate_acceptance_checklist_blocked_not_passed",
        "v1_release_candidate_cutover_runbook_blocked_not_authority",
        "v1_final_readiness_audit_template_future_scaffolding_not_executed",
        "arc_bot_shell_clean_checkpoint_proof_recorded_as_release_gate_input_only",
        "v1_g57_through_v1_g60_candidate_only_evidence_complete",
        "later_lima_validation_supplement_current_37_147_5359_with_protected_paths_clean",
        "latest_lima_readiness_freshness_supplement_current_15_89_5361_with_protected_paths_clean",
        "latest_handoff_freshness_supplement_current_8_117_5362_and_7_64_133_5364_with_protected_paths_clean",
        "v1_g61_bounded_proof_complete_final_readiness_cutover_still_blocked",
    ]

    validation = fixture["lima_validation_results"]
    assert validation["focused_current_candidate_g61_readiness_set"] == {
        "passed": True,
        "tests_passed": 83,
    }
    assert validation["focused_current_gate_consistency_readiness_set"] == {
        "passed": True,
        "tests_passed": 153,
    }
    assert validation["compileall_lima"] == {"passed": True}
    assert validation["full_lima_suite"] == {
        "passed": True,
        "tests_passed": 5350,
    }
    assert validation["lima_diff_check"] == {
        "passed": True,
        "warnings": "LF-to-CRLF warnings only",
    }
    assert validation["lima_cached_diff_check"] == {"passed": True}

    supplement = fixture["later_lima_validation_supplement"]
    assert supplement["date"] == "2026-06-21"
    assert supplement["scope"] == (
        "lima_only_after_later_readiness_docs_fixtures_tests_changes"
    )
    assert supplement["consumer_checkpoints_rerun_by_supplement"] is False
    assert (
        supplement["release_candidate_or_g61_implementation_authority_created"]
        is False
    )
    assert supplement["focused_g61_guard_operator_freshness_set"] == {
        "passed": True,
        "tests_passed": 37,
    }
    assert supplement["focused_v1_readiness_regression_set"] == {
        "passed": True,
        "tests_passed": 147,
    }
    assert supplement["compileall_lima"] == {"passed": True}
    assert supplement["full_lima_suite"] == {
        "passed": True,
        "tests_passed": 5359,
    }
    assert supplement["lima_diff_check"] == {
        "passed": True,
        "warnings": "LF-to-CRLF warnings only",
    }
    assert supplement["lima_cached_diff_check"] == {"passed": True}
    assert supplement["protected_runtime_dependency_support_paths_status"] == "clean"

    latest = fixture["latest_lima_readiness_freshness_supplement"]
    assert latest["date"] == "2026-06-21"
    assert latest["scope"] == (
        "lima_only_after_final_blocker_register_and_branch_index_refresh"
    )
    assert latest["consumer_checkpoints_rerun_by_supplement"] is False
    assert (
        latest[
            "release_candidate_cutover_final_readiness_or_g61_implementation_authority_created"
        ]
        is False
    )
    assert latest["focused_final_blocker_index_set"] == {
        "passed": True,
        "tests_passed": 15,
    }
    assert latest["broader_affected_v1_readiness_set"] == {
        "passed": True,
        "tests_passed": 89,
    }
    assert latest["compileall_lima"] == {"passed": True}
    assert latest["full_lima_suite"] == {
        "passed": True,
        "tests_passed": 5361,
    }
    assert latest["lima_diff_check"] == {
        "passed": True,
        "warnings": "LF-to-CRLF warnings only",
    }
    assert latest["lima_cached_diff_check"] == {"passed": True}
    assert latest["protected_runtime_dependency_support_paths_status"] == "clean"

    handoff = fixture["latest_handoff_freshness_supplement"]
    assert handoff["date"] == "2026-06-21"
    assert handoff["scope"] == (
        "lima_only_after_post_g61_request_refresh_and_quickstart_artifact_refresh"
    )
    assert handoff["consumer_checkpoints_rerun_by_supplement"] is False
    assert (
        handoff[
            "release_candidate_cutover_final_readiness_arc_clean_checkpoint_consumer_production_or_g61_implementation_authority_created"
        ]
        is False
    )
    assert handoff["focused_post_g61_request_refresh_set"] == {
        "passed": True,
        "tests_passed": 8,
    }
    assert handoff["broader_g61_readiness_after_request_refresh_set"] == {
        "passed": True,
        "tests_passed": 117,
    }
    assert handoff["focused_candidate_harness_quickstart_set"] == {
        "passed": True,
        "tests_passed": 7,
    }
    assert handoff["adjacent_harness_readiness_after_quickstart_artifact_refresh_set"] == {
        "passed": True,
        "tests_passed": 64,
    }
    assert handoff["broader_g61_readiness_after_quickstart_artifact_refresh_set"] == {
        "passed": True,
        "tests_passed": 133,
    }
    assert handoff["compileall_lima"] == {"passed": True}
    assert handoff["post_g61_request_refresh_full_lima_suite"] == {
        "passed": True,
        "tests_passed": 5362,
    }
    assert handoff["quickstart_artifact_refresh_full_lima_suite"] == {
        "passed": True,
        "tests_passed": 5364,
    }
    assert handoff["lima_diff_check"] == {
        "passed": True,
        "warnings": "LF-to-CRLF warnings only",
    }
    assert handoff["lima_cached_diff_check"] == {"passed": True}
    assert handoff["protected_runtime_dependency_support_paths_status"] == "clean"


def test_v1_current_candidate_validation_refresh_preserves_boundaries() -> None:
    boundaries = _load_fixture()["boundaries_preserved"]

    for key, value in boundaries.items():
        assert value is False, key


def test_v1_current_candidate_validation_refresh_stop_conditions_are_bounded() -> None:
    assert _load_fixture()["stop_conditions"] == [
        "v1_g61_implementation_without_exact_approval",
        "treat_this_audit_as_g61_approval",
        "treat_this_audit_as_release_candidate_branch_or_tag_authority",
        "treat_this_audit_as_passed_release_candidate_checklist_cutover_or_final_readiness_audit",
        "treat_arc_candidate_smoke_as_clean_checkpoint_proof_while_local_drift_excluded",
        "consumer_repo_edit_from_audit_lane",
        "runtime_or_public_api_change_from_audit_lane",
        "runtime_vendor_sdk_import_lockfile_secret_credential_token_sdk_endpoint_network_or_fallback_required",
        "raw_sensitive_or_patch_content_persistence",
        "v1_product_production_or_completion_claim",
    ]


def test_v1_current_candidate_validation_refresh_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (
        REPO_ROOT
        / fixture["documents"]["current_candidate_validation_refresh_audit"]
    ).read_text(encoding="utf-8")

    assert "# V1 Current Candidate Validation Refresh Audit" in text
    assert fixture["source_lima_commit_before_audit"] in text
    assert "LOCAL_CANDIDATE_VALIDATION_REFRESH_PASS_WITH_G61_OPERATOR_BLOCKER" in text
    assert "Public Sparkbot target checkout" in text
    assert "8 passed" in text
    assert "Public Sparkbot target publication is resolved" in text
    assert "unrelated local worktree drift is excluded from V1 proof" in text
    assert "not clean-checkpoint evidence" in text
    assert "V1 candidate harness quickstart execution audit" in text
    assert "V1 current gate consistency audit" in text
    assert "committed proof that stale public Sparkbot publication" in text
    assert "V1-G61 operator decision packet status audit" in text
    assert "`Approve-V1-G61` is recorded for bounded local import-proof evidence only" in text
    assert "NOT_RELEASE_CANDIDATE_FINAL_READINESS_AND_CUTOVER_BLOCKERS" in text
    assert "not a passed release-candidate checklist" in text
    assert "CUTOVER_BLOCKED_AT_FINAL_READINESS_AND_OPERATOR_AUTHORIZATION" in text
    assert "not cutover authority" in text
    assert "future audit scaffolding" in text
    assert "did not execute or pass the final readiness audit" in text
    assert "Arc-Bot-shell local fake-executor smoke remains compatibility evidence only; clean-checkpoint proof is recorded separately as release-gate input evidence" in text
    assert "83 passed" in text
    assert "153 passed" in text
    assert "5350 passed" in text
    assert "## Later LIMA Validation Supplement" in text
    assert "Date: 2026-06-21" in text
    assert "does not claim that Sparkbot or Arc-Bot-shell checkpoints were rerun" in text
    assert "focused G61 guard/operator/freshness pytest set | 37 passed" in text
    assert "focused V1 readiness regression pytest set | 147 passed" in text
    assert "`python -m pytest -q tests -p no:cacheprovider` | 5359 passed" in text
    assert "protected runtime/dependency/support path status | clean" in text
    assert (
        "The later 2026-06-21 LIMA validation supplement records 37 focused "
        "G61 guard/operator/freshness tests, 147 focused V1 readiness "
        "regression tests, full LIMA suite validation with 5359 tests"
    ) in text
    assert "## Latest LIMA Readiness Freshness Supplement" in text
    assert "focused final blocker/index pytest set | 15 passed" in text
    assert "broader affected V1 readiness pytest set | 89 passed" in text
    assert "`python -m pytest -q tests -p no:cacheprovider` | 5361 passed" in text
    assert (
        "does not create release-candidate, cutover, final-readiness, or "
        "G61 implementation authority"
    ) in text
    assert (
        "The latest 2026-06-21 LIMA readiness freshness supplement records "
        "15 focused final blocker/index tests, 89 broader affected V1 readiness "
        "tests, full LIMA suite validation with 5361 tests"
    ) in text
    assert "## Latest Handoff Freshness Supplement" in text
    assert "focused post-G61 request-refresh pytest set | 8 passed" in text
    assert "broader G61/readiness pytest set after request refresh | 117 passed" in text
    assert "focused candidate harness quickstart pytest set | 7 passed" in text
    assert "adjacent harness/readiness pytest set after quickstart artifact refresh | 64 passed" in text
    assert "broader G61/readiness pytest set after quickstart artifact refresh | 133 passed" in text
    assert "latest post-G61 request refresh full LIMA suite | 5362 passed" in text
    assert "latest quickstart artifact refresh full LIMA suite | 5364 passed" in text
    assert (
        "does not create release-candidate, cutover, final-readiness, Arc "
        "clean-checkpoint, consumer production integration, or G61 implementation "
        "authority"
    ) in text
    assert (
        "The latest 2026-06-21 handoff freshness supplement records 8 focused "
        "post-G61 request-refresh tests, 117 broader G61/readiness tests, 7 "
        "focused candidate harness quickstart tests, 64 adjacent harness/readiness "
        "tests, 133 broader G61/readiness tests, full LIMA suite validation with "
        "5362 and 5364 tests"
    ) in text
    assert "`Approve-V1-G61` is recorded for bounded local import-proof evidence only" in text
    assert "V1-G61 implementation approval recorded by this audit: no." in text
    assert "Release-candidate branch or tag authority created by this audit: no." in text
    assert "Release-candidate cutover authorized by this audit: no." in text
    assert "Final readiness audit executed or passed by this audit: no." in text
    assert "Arc-Bot-shell clean-checkpoint proof claimed by this audit: no." in text
    assert "treat this audit as release-candidate branch or tag authority" in text
    assert "treat this audit as a passed release-candidate checklist" in text
    assert "treat Arc-Bot-shell local candidate smoke evidence as a substitute for the recorded clean-checkpoint proof" in text
    assert "public Sparkbot branch publication to `sparkpit-labs/Sparkbot` still requires write credentials" not in text
    assert "V1-G57 still requires exactly one valid operator decision" not in text
    assert "V1.0 completion, product readiness, or production readiness claimed: no." in text


def test_v1_current_candidate_validation_refresh_has_no_sensitive_markers() -> None:
    fixture = _load_fixture()
    output = json.dumps(fixture, sort_keys=True)
    output += (
        REPO_ROOT
        / fixture["documents"]["current_candidate_validation_refresh_audit"]
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
