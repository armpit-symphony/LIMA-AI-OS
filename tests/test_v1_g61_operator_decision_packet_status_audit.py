"""Static checks for the V1-G61 operator decision packet status audit."""

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
    / "v1_g61_operator_decision_packet_status_audit.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g61_operator_decision_status_audit_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["audit_id"] == "v1_g61_operator_decision_packet_status_audit"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["date"] == "2026-06-22"
    assert fixture["observed_workspace_branch"] == (
        "docs-v1-post-g60-readiness-and-next-lane-matrix"
    )
    assert fixture["audit_verdict"] == "PASS_G61_OPERATOR_DECISION_PACKET_APPROVED"

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_g61_operator_decision_state_records_exact_approval() -> None:
    state = _load_fixture()["decision_state"]

    assert state == {
        "decision_packet_status": "approved",
        "operator_decision_packet_date": "2026-06-22",
        "current_recorded_choice": "Approve-V1-G61",
        "recorded_approval_wording": (
            "I explicitly approve V1-G61 implementation of the runtime vendor "
            "SDK import execution proof slice, limited to the file scope, "
            "behavior scope, tests, rollback plan, and stop conditions in "
            "docs/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_APPROVAL_REQUEST.md."
        ),
        "recorded_revision_request": "none",
        "recorded_pause_reason": "none",
        "approved_implementation_branch": (
            "v1-g61-runtime-vendor-sdk-import-execution-proof"
        ),
        "implementation_approved": True,
        "current_gate_consistency_audit_date": "2026-06-21",
        "post_validation_readiness_change_freshness_full_suite_tests_passed": 5359,
        "latest_final_blocker_index_refresh_focused_tests_passed": 15,
        "latest_final_blocker_index_refresh_broader_tests_passed": 89,
        "latest_final_blocker_index_refresh_full_lima_suite_tests_passed": 5361,
        "latest_quickstart_post_refresh_public_sparkbot_tests_passed": 8,
        "latest_quickstart_post_refresh_accessible_sparkbot_tests_passed": 8,
        "latest_quickstart_post_refresh_arc_bot_shell_tests_passed": 8,
        "latest_quickstart_post_refresh_focused_tests_passed": 17,
        "latest_quickstart_post_refresh_broader_v1_tests_passed": 108,
        "latest_quickstart_post_refresh_full_lima_suite_tests_passed": 5360,
        "latest_post_g61_request_readiness_refresh_focused_tests_passed": 8,
        "latest_post_g61_request_readiness_refresh_broader_tests_passed": 117,
        "latest_post_g61_request_readiness_refresh_full_lima_suite_tests_passed": 5362,
        "latest_quickstart_artifact_refresh_focused_tests_passed": 7,
        "latest_quickstart_artifact_refresh_adjacent_tests_passed": 64,
        "latest_quickstart_artifact_refresh_broader_tests_passed": 133,
        "latest_quickstart_artifact_refresh_full_lima_suite_tests_passed": 5364,
        "arc_bot_shell_local_drift_compatibility_only_tracked_modified_file_count": 7,
        "arc_bot_shell_local_drift_compatibility_only_untracked_file_count": 64,
        "arc_bot_shell_clean_checkpoint_evidence": False,
        "latest_arc_same_day_recheck_approved_g56_smoke_proof_paths_clean": True,
        "latest_arc_same_day_recheck_dirty_worktree_compatibility_only": True,
    }


def test_v1_g61_operator_decision_valid_choices_and_exact_approval_are_locked() -> None:
    fixture = _load_fixture()

    assert fixture["valid_operator_choices"] == [
        "Approve-V1-G61",
        "Revise-V1-G61",
        "Pause",
    ]
    assert fixture["required_exact_approval_text"] == (
        "Approve-V1-G61\n\n"
        "I explicitly approve V1-G61 implementation of the runtime vendor SDK "
        "import execution proof slice, limited to the file scope, behavior "
        "scope, tests, rollback plan, and stop conditions in "
        "docs/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_APPROVAL_REQUEST.md."
    )
    assert fixture["implementation_unlock_requires"] == [
        "approve_v1_g61_recorded_as_operator_choice",
        "exact_approval_wording_recorded",
        "approved_branch_v1_g61_runtime_vendor_sdk_import_execution_proof",
        "implementation_file_scope_limited_to_approval_request",
        "preapproval_runtime_tree_guard_clean_before_implementation",
        "post_validation_freshness_latest_final_blocker_index_15_89_5361_current_before_implementation",
        "post_validation_freshness_latest_post_g61_request_8_117_5362_current_before_implementation",
        "post_validation_freshness_latest_quickstart_artifact_7_64_133_5364_current_before_implementation",
        "current_gate_freshness_quickstart_and_arc_drift_audits_current_before_implementation",
    ]


def test_v1_g61_operator_decision_packet_text_matches_fixture() -> None:
    fixture = _load_fixture()
    decision_text = (
        REPO_ROOT / fixture["documents"]["operator_decision_packet"]
    ).read_text(encoding="utf-8")
    audit_text = (REPO_ROOT / fixture["documents"]["status_audit"]).read_text(
        encoding="utf-8"
    )

    assert "Decision packet status: `approved`" in decision_text
    assert "Date: 2026-06-22" in decision_text
    assert "Current recorded choice: Approve-V1-G61" in decision_text
    assert "Recorded choice: Approve-V1-G61" in decision_text
    assert (
        "Recorded approval wording: I explicitly approve V1-G61 implementation "
        "of the runtime vendor SDK import execution proof slice, limited to the "
        "file scope, behavior scope, tests, rollback plan, and stop conditions "
        "in docs/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_APPROVAL_REQUEST.md."
        in decision_text
    )
    assert (
        "Approved implementation branch: "
        "`v1-g61-runtime-vendor-sdk-import-execution-proof`"
        in decision_text
    )
    assert "Implementation approved: yes." in decision_text
    assert "Valid choice: Approve-V1-G61" in decision_text
    assert "Valid choice: Revise-V1-G61" in decision_text
    assert "Valid choice: Pause" in decision_text
    assert fixture["required_exact_approval_text"] in decision_text
    assert "V1_POST_VALIDATION_READINESS_CHANGE_FRESHNESS_AUDIT.md" in decision_text
    assert "V1_CANDIDATE_HARNESS_QUICKSTART_EXECUTION_AUDIT.md" in decision_text
    assert "V1_ARC_BOT_SHELL_LOCAL_DRIFT_EXCLUSION_AUDIT.md" in decision_text
    assert "V1_G61_PREAPPROVAL_RUNTIME_TREE_GUARD_AUDIT.md" in decision_text
    assert "latest quickstart post-refresh full-suite evidence passing 5360 tests" in decision_text
    assert "latest final blocker/index refresh evidence passing 15 focused tests, 89 broader affected readiness tests, and 5361 full-suite tests" in decision_text
    assert "latest post-G61 request readiness-refresh evidence passing 8 focused tests, 117 broader G61/readiness tests, and 5362 full-suite tests" in decision_text
    assert "latest quickstart artifact refresh evidence passing 7 focused tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5364 full-suite tests" in decision_text
    assert "public Sparkbot, accessible Sparkbot, and Arc-Bot-shell each passing 8 consumer smoke tests" in decision_text
    assert "LIMA post-refresh validation passing 17 focused quickstart/handoff tests, 108 broader V1 harness/readiness tests, and 5360 full-suite tests" in decision_text
    assert "latest quickstart artifact refresh validation passing 7 focused tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5364 full-suite tests" in decision_text
    assert "7 tracked modified files and 64 untracked files as compatibility-only evidence, not clean-checkpoint proof" in decision_text
    assert "same-day Arc recheck keeps approved G56 smoke proof paths clean" in decision_text
    assert "Preapproval runtime-tree guard reviewed before implementation: clean." in decision_text
    assert "Local approved import execution proof reviewed: `openai` imported successfully with sanitized version evidence `2.43.0`." in decision_text
    assert "Latest final blocker/index freshness reviewed: LIMA 15/89/5361." in decision_text
    assert "Latest post-G61 request readiness-refresh reviewed: LIMA 8/117/5362." in decision_text
    assert "Latest quickstart artifact refresh reviewed: LIMA 7/64/133/5364." in decision_text
    assert "Recorded choice: Revise-V1-G61" not in decision_text
    assert "Recorded choice: Pause" not in decision_text

    assert "# V1-G61 Operator Decision Packet Status Audit" in audit_text
    assert fixture["audit_verdict"] in audit_text
    assert "Current recorded choice: Approve-V1-G61" in audit_text
    assert "Current gate consistency audit date: 2026-06-21" in audit_text
    assert "current same-turn full-suite freshness evidence passing 5359 tests" in audit_text
    assert "Latest quickstart post-refresh evidence: public Sparkbot 8 tests, accessible Sparkbot 8 tests, Arc-Bot-shell 8 tests, LIMA focused quickstart/handoff 17 tests, broader V1 harness/readiness 108 tests, and full LIMA suite 5360 tests" in audit_text
    assert "Latest final blocker/index freshness evidence: 15 focused final blocker/index tests, 89 broader affected readiness tests, and full LIMA suite 5361 tests" in audit_text
    assert "Latest post-G61 request readiness-refresh evidence: 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, and full LIMA suite 5362 tests" in audit_text
    assert "Latest quickstart artifact refresh evidence: 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and full LIMA suite 5364 tests" in audit_text
    assert "7 tracked modified files and 64 untracked files remain excluded from V1 release-candidate/final-readiness proof" in audit_text
    assert "Latest Arc same-day recheck: approved G56 smoke proof paths clean; dirty worktree remains compatibility-only evidence" in audit_text
    assert "Implementation may proceed only if all of the following are true" in audit_text
    assert "candidate harness quickstart execution audit" in audit_text
    assert "post-validation readiness-change freshness audit including latest final blocker/index 15/89/5361 evidence, latest post-G61 request readiness-refresh 8/117/5362 evidence, and latest quickstart artifact refresh 7/64/133/5364 evidence" in audit_text
    assert "Use the approved decision packet as authority only for the bounded V1-G61 import execution proof" in audit_text


def test_v1_g61_operator_decision_boundaries_remain_bounded() -> None:
    boundaries = _load_fixture()["boundaries_preserved"]

    assert boundaries["operator_decision_recorded_by_audit"] is True
    assert boundaries["v1_g61_implementation_approval_recorded_by_audit"] is True
    assert boundaries["runtime_vendor_sdk_import_execution_proof_implemented"] is True

    for key, value in boundaries.items():
        if key in {
            "operator_decision_recorded_by_audit",
            "v1_g61_implementation_approval_recorded_by_audit",
            "runtime_vendor_sdk_import_execution_proof_implemented",
        }:
            continue
        assert value is False, key


def test_v1_g61_operator_decision_stop_conditions_are_bounded() -> None:
    fixture = _load_fixture()

    assert fixture["implementation_remains_blocked_if"] == [
        "revise_v1_g61_recorded",
        "pause_recorded",
        "missing_choice",
        "partial_approval",
        "paraphrased_approval",
        "extra_file_scope",
        "runtime_import_added",
        "dependency_or_lockfile_edit",
        "provider_client_construction",
        "endpoint_resolution",
        "network_call",
        "credential_access",
        "fallback_execution",
        "consumer_production_integration",
        "product_readiness_claim",
    ]
    assert fixture["stop_conditions"] == [
        "g61_implementation_without_exact_approval",
        "more_than_one_operator_choice_recorded",
        "paraphrased_approval_wording_accepted",
        "lima_dependency_lockfile_sparkbot_or_arc_bot_shell_edit_from_audit_lane",
        "runtime_import_provider_client_endpoint_network_credential_fallback_connector_or_physical_world_behavior_added",
        "v1_product_production_or_completion_claim",
    ]
    assert fixture["next_step"] == (
        "complete_v1_g61_import_execution_proof_closeout_then_refresh_release_candidate_readiness"
    )


def test_v1_g61_operator_decision_status_audit_has_no_sensitive_markers() -> None:
    fixture = _load_fixture()
    output = json.dumps(fixture, sort_keys=True)
    for relative_path in fixture["documents"].values():
        output += (REPO_ROOT / relative_path).read_text(encoding="utf-8")

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
