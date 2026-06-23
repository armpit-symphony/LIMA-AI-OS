"""Static checks for the root README V1 status alignment."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
README_PATH = REPO_ROOT / "README.md"
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_readme_status_alignment.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_readme_status_fixture_preserves_candidate_only_boundary() -> None:
    fixture = _load_fixture()

    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == (
        "docs-v1-post-g60-readiness-and-next-lane-matrix"
    )
    assert fixture["request_stage_lane_label"] == (
        "prepare-v1-g61-runtime-vendor-sdk-import-execution-proof-approval-request"
    )
    assert fixture["source_commit_before_alignment"] == (
        "37626bf236bf96c8a57a3ca351668e90eeb0e651"
    )
    assert fixture["documents"]["readme"] == "README.md"
    assert fixture["documents"]["current_project_state"] == "docs/CURRENT_PROJECT_STATE.md"
    assert fixture["readme_section"] == "Current V1 Status"
    assert fixture["current_project_state_section"] == "Current V1 Gate Snapshot"
    assert fixture["current_project_state_snapshot_authoritative_for_branch"] is True
    assert fixture["later_appended_historical_lane_notes_override_current_snapshot"] is False
    assert fixture["latest_completed_gate"] == "V1-G60"
    assert fixture["latest_authority_chain_audit"] == "V1-G56"
    assert fixture["latest_readiness_rollup"] == "V1-G60"
    assert (
        fixture["latest_request_stage_readiness_refresh"]
        == "V1_POST_G61_REQUEST_READINESS_REFRESH"
    )
    assert fixture["current_gate"] == "V1-G61"
    assert fixture["next_lane_request_only"] is True
    assert fixture["g56_request_packet_prepared"] is True
    assert fixture["g56_operator_approval_recorded"] is True
    assert fixture["g56_runtime_implementation_approved"] is True
    assert fixture["g56_independent_audit_complete"] is True
    assert fixture["g57_request_packet_prepared"] is True
    assert fixture["g57_operator_approval_recorded"] is True
    assert fixture["g57_runtime_implementation_approved"] is True
    assert fixture["g60_request_packet_prepared"] is True
    assert fixture["g60_operator_approval_recorded"] is True
    assert fixture["g60_runtime_implementation_approved"] is True
    assert fixture["g60_independent_audit_complete"] is True
    assert fixture["public_sparkbot_g56_publication_blocker_resolved"] is True
    assert fixture["public_sparkbot_g56_publication_resolution_commit"] == (
        "ae5cc9c563ea2b0f08c91af03164a78b4b20e3e2"
    )
    assert fixture["g61_request_packet_prepared"] is True
    assert fixture["g61_request_gate_audit_complete"] is True
    assert fixture["g61_preapproval_runtime_tree_guard_audit_complete"] is True
    assert fixture["g61_operator_decision_packet_status_audit_complete"] is True
    assert fixture["post_g61_request_readiness_refresh_complete"] is True
    assert fixture["current_gate_consistency_audit_complete"] is True
    assert fixture["candidate_test_handoff_manifest_current"] is True
    assert fixture["arc_bot_shell_local_drift_exclusion_audit_current"] is True
    assert (
        fixture["arc_bot_shell_local_drift_exclusion_audit_tracked_modified_file_count"]
        == 7
    )
    assert (
        fixture["arc_bot_shell_local_drift_exclusion_audit_untracked_file_count"]
        == 64
    )
    assert (
        fixture["arc_bot_shell_same_day_recheck_approved_g56_smoke_proof_paths_clean"]
        is True
    )
    assert fixture["arc_bot_shell_local_drift_excluded_from_v1_proof"] is True
    assert fixture["arc_bot_shell_clean_checkpoint_evidence"] is False
    assert (
        fixture[
            "arc_bot_shell_clean_checkpoint_required_before_release_candidate_final_readiness_branch_tag_cutover_or_readiness_claim"
        ]
        is True
    )
    assert fixture["candidate_harness_quickstart_current"] is True
    assert fixture["candidate_harness_quickstart_verdict"] == (
        "QUICKSTART_READY_FOR_LOCAL_CANDIDATE_SMOKE_WITH_G61_OPERATOR_BLOCKER"
    )
    assert fixture["candidate_harness_quickstart_execution_audit_complete"] is True
    assert fixture["candidate_harness_quickstart_execution_audit_verdict"] == (
        "PASS_LOCAL_CANDIDATE_HARNESS_QUICKSTART_WITH_G61_OPERATOR_BLOCKER"
    )
    assert (
        fixture[
            "candidate_harness_quickstart_execution_same_turn_consumer_refresh_complete"
        ]
        is True
    )
    assert (
        fixture[
            "candidate_harness_quickstart_execution_same_turn_consumer_refresh_public_sparkbot_tests_passed"
        ]
        == 8
    )
    assert (
        fixture[
            "candidate_harness_quickstart_execution_same_turn_consumer_refresh_accessible_sparkbot_tests_passed"
        ]
        == 8
    )
    assert (
        fixture[
            "candidate_harness_quickstart_execution_same_turn_consumer_refresh_arc_bot_shell_tests_passed"
        ]
        == 8
    )
    assert (
        fixture[
            "candidate_harness_quickstart_execution_post_refresh_focused_tests_passed"
        ]
        == 17
    )
    assert (
        fixture[
            "candidate_harness_quickstart_execution_post_refresh_broader_v1_tests_passed"
        ]
        == 108
    )
    assert (
        fixture[
            "candidate_harness_quickstart_execution_post_refresh_full_lima_suite_tests_passed"
        ]
        == 5360
    )
    assert (
        fixture[
            "candidate_harness_quickstart_execution_post_refresh_release_authority_created"
        ]
        is False
    )
    assert fixture["consumer_harness_usability_matrix_current"] is True
    assert fixture["consumer_checkpoint_manifest_current"] is True
    assert fixture["current_candidate_validation_refresh_audit_complete"] is True
    assert fixture[
        "current_candidate_validation_refresh_focused_current_gate_tests_passed"
    ] == 153
    assert fixture[
        "current_candidate_validation_refresh_full_lima_suite_tests_passed"
    ] == 5350
    assert (
        fixture["current_candidate_validation_refresh_lima_only_supplement_date"]
        == "2026-06-21"
    )
    assert (
        fixture[
            "current_candidate_validation_refresh_lima_only_supplement_focused_g61_guard_tests_passed"
        ]
        == 37
    )
    assert (
        fixture[
            "current_candidate_validation_refresh_lima_only_supplement_focused_v1_readiness_tests_passed"
        ]
        == 147
    )
    assert (
        fixture[
            "current_candidate_validation_refresh_lima_only_supplement_full_lima_suite_tests_passed"
        ]
        == 5359
    )
    assert (
        fixture[
            "current_candidate_validation_refresh_lima_only_supplement_consumer_checkpoints_rerun"
        ]
        is False
    )
    assert (
        fixture[
            "current_candidate_validation_refresh_lima_only_supplement_protected_paths_clean"
        ]
        is True
    )
    assert (
        fixture[
            "current_candidate_validation_refresh_lima_only_supplement_release_authority_created"
        ]
        is False
    )
    assert (
        fixture["current_candidate_validation_refresh_latest_supplement_date"]
        == "2026-06-21"
    )
    assert (
        fixture[
            "current_candidate_validation_refresh_latest_supplement_focused_final_blocker_index_tests_passed"
        ]
        == 15
    )
    assert (
        fixture[
            "current_candidate_validation_refresh_latest_supplement_broader_v1_readiness_tests_passed"
        ]
        == 89
    )
    assert (
        fixture[
            "current_candidate_validation_refresh_latest_supplement_full_lima_suite_tests_passed"
        ]
        == 5361
    )
    assert (
        fixture[
            "current_candidate_validation_refresh_latest_supplement_consumer_checkpoints_rerun"
        ]
        is False
    )
    assert (
        fixture[
            "current_candidate_validation_refresh_latest_supplement_protected_paths_clean"
        ]
        is True
    )
    assert (
        fixture[
            "current_candidate_validation_refresh_latest_supplement_release_cutover_final_readiness_or_g61_authority_created"
        ]
        is False
    )
    assert (
        fixture["current_candidate_validation_refresh_latest_handoff_supplement_date"]
        == "2026-06-21"
    )
    assert (
        fixture[
            "current_candidate_validation_refresh_latest_handoff_supplement_post_g61_request_focused_tests_passed"
        ]
        == 8
    )
    assert (
        fixture[
            "current_candidate_validation_refresh_latest_handoff_supplement_post_g61_request_broader_tests_passed"
        ]
        == 117
    )
    assert (
        fixture[
            "current_candidate_validation_refresh_latest_handoff_supplement_post_g61_request_full_lima_suite_tests_passed"
        ]
        == 5362
    )
    assert (
        fixture[
            "current_candidate_validation_refresh_latest_handoff_supplement_quickstart_focused_tests_passed"
        ]
        == 7
    )
    assert (
        fixture[
            "current_candidate_validation_refresh_latest_handoff_supplement_quickstart_adjacent_tests_passed"
        ]
        == 64
    )
    assert (
        fixture[
            "current_candidate_validation_refresh_latest_handoff_supplement_quickstart_broader_tests_passed"
        ]
        == 133
    )
    assert (
        fixture[
            "current_candidate_validation_refresh_latest_handoff_supplement_quickstart_full_lima_suite_tests_passed"
        ]
        == 5364
    )
    assert (
        fixture[
            "current_candidate_validation_refresh_latest_handoff_supplement_consumer_checkpoints_rerun"
        ]
        is False
    )
    assert (
        fixture[
            "current_candidate_validation_refresh_latest_handoff_supplement_protected_paths_clean"
        ]
        is True
    )
    assert (
        fixture[
            "current_candidate_validation_refresh_latest_handoff_supplement_release_cutover_final_readiness_arc_clean_checkpoint_consumer_production_or_g61_authority_created"
        ]
        is False
    )
    assert fixture["post_validation_readiness_change_freshness_audit_complete"] is True
    assert (
        fixture[
            "post_validation_readiness_change_freshness_requires_same_turn_validation"
        ]
        is True
    )
    assert (
        fixture[
            "post_validation_readiness_change_freshness_full_lima_suite_tests_passed"
        ]
        == 5359
    )
    assert (
        fixture[
            "post_validation_readiness_change_latest_quickstart_post_refresh_full_lima_suite_tests_passed"
        ]
        == 5360
    )
    assert (
        fixture[
            "post_validation_readiness_change_latest_final_blocker_index_focused_tests_passed"
        ]
        == 15
    )
    assert (
        fixture[
            "post_validation_readiness_change_latest_final_blocker_index_broader_tests_passed"
        ]
        == 89
    )
    assert (
        fixture[
            "post_validation_readiness_change_latest_final_blocker_index_full_lima_suite_tests_passed"
        ]
        == 5361
    )
    assert (
        fixture[
            "post_validation_readiness_change_latest_post_g61_request_refresh_focused_tests_passed"
        ]
        == 8
    )
    assert (
        fixture[
            "post_validation_readiness_change_latest_post_g61_request_refresh_broader_tests_passed"
        ]
        == 117
    )
    assert (
        fixture[
            "post_validation_readiness_change_latest_post_g61_request_refresh_full_lima_suite_tests_passed"
        ]
        == 5362
    )
    assert (
        fixture[
            "post_validation_readiness_change_latest_quickstart_artifact_refresh_focused_tests_passed"
        ]
        == 7
    )
    assert (
        fixture[
            "post_validation_readiness_change_latest_quickstart_artifact_refresh_adjacent_tests_passed"
        ]
        == 64
    )
    assert (
        fixture[
            "post_validation_readiness_change_latest_quickstart_artifact_refresh_broader_tests_passed"
        ]
        == 133
    )
    assert (
        fixture[
            "post_validation_readiness_change_latest_quickstart_artifact_refresh_full_lima_suite_tests_passed"
        ]
        == 5364
    )
    assert (
        fixture[
            "post_validation_readiness_change_latest_quickstart_artifact_refresh_release_cutover_final_readiness_production_arc_clean_checkpoint_or_g61_authority_created"
        ]
        is False
    )
    assert (
        fixture[
            "post_validation_readiness_change_freshness_release_authority_created"
        ]
        is False
    )
    assert fixture["release_candidate_acceptance_checklist_current"] is True
    assert fixture["release_candidate_acceptance_checklist_verdict"] == (
        "NOT_RELEASE_CANDIDATE_ARC_CLEAN_CHECKPOINT_AND_FINAL_READINESS_BLOCKERS"
    )
    assert fixture["release_candidate_cutover_runbook_current"] is True
    assert fixture["release_candidate_cutover_runbook_verdict"] == (
        "CUTOVER_BLOCKED_AT_ARC_CLEAN_CHECKPOINT_AND_FINAL_READINESS"
    )
    assert fixture["final_readiness_audit_template_current"] is True
    assert fixture["final_blocker_register_current"] is True
    assert fixture["g61_operator_approval_recorded"] is False
    assert fixture["g61_runtime_implementation_approved"] is False
    assert fixture["g61_valid_operator_choices"] == [
        "Approve-V1-G61",
        "Revise-V1-G61",
        "Pause",
    ]
    assert fixture["v1_g55_operator_approval_recorded"] is True
    assert fixture["v1_g55_runtime_implementation_approved"] is True
    assert fixture["v1_g55_independent_audit_complete"] is True
    assert fixture["g55_wrapper_added"] is True
    assert fixture["g55_public_api_exports_changed"] is True
    assert fixture["g55_public_api_change_limited_to_approved_harness_exports"] is True
    assert fixture["g55_caller_injected_provider_sdk_network_executor_only"] is True
    assert fixture["v1_product_ready"] is False
    assert fixture["production_ready"] is False

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_v1_readme_status_fixture_names_first_shells() -> None:
    assert set(_load_fixture()["v1_target_shells"]) == {
        "Sparkbot_shell",
        "Sparkbot",
        "Arc-Bot-shell",
    }


def test_v1_readme_status_fixture_adds_no_new_runtime_or_integration_behavior() -> None:
    fixture = _load_fixture()

    for key in (
        "runtime_behavior_added_by_status_refresh",
        "tests_support_changed",
        "shell_repos_changed",
        "sparkbot_import_added",
        "sparkbot_code_copied",
        "sparkbot_or_arc_bot_shell_changed_for_g61",
        "g61_runtime_vendor_sdk_import_execution_proof_added",
        "dependency_manifest_changed_by_status_refresh",
        "lockfile_edited_by_status_refresh",
        "built_in_provider_sdk_client_added",
        "vendor_sdk_import_added_to_lima",
        "provider_endpoint_resolution_by_lima_added",
        "network_call_performed_by_lima",
        "secret_lookup_added",
        "credential_value_access_added",
        "provider_token_or_api_key_access_added",
        "provider_configuration_changes_added",
        "fallback_execution_added",
        "consumer_production_runtime_integration_added",
        "connector_browser_network_file_device_robotics_physical_world_behavior_added",
    ):
        assert fixture[key] is False, key
    assert fixture["g61_preapproval_runtime_tree_guard_added"] is True


def test_v1_readme_status_fixture_points_to_exact_next_step() -> None:
    fixture = _load_fixture()

    assert fixture["next_recommended_lane"] == (
        "operator_decision_v1_g61_runtime_vendor_sdk_import_execution_proof"
    )
    assert fixture["next_step"] == "record_v1_g61_operator_decision"


def test_readme_contains_current_v1_status_and_boundaries() -> None:
    text = README_PATH.read_text(encoding="utf-8")

    assert "## Current V1 Status" in text
    assert "LIMA remains `CANDIDATE_ONLY`." in text
    assert "`Sparkbot_shell`, public `Sparkbot`, and `Arc-Bot-shell`" in text
    assert "completed implementation evidence is refreshed through `V1-G60`" in text
    assert (
        "request-stage readiness is refreshed through the post-G61 request readiness refresh"
        in text
    )
    assert "The V1 readiness chain is refreshed through `V1-G60`" not in text
    assert "V1-G61 runtime vendor SDK import execution proof approval request is prepared" in text
    assert "V1-G61 request gate is independently audited" in text
    assert "V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_APPROVAL_REQUEST_AUDIT.md" in text
    assert "V1_G61_PREAPPROVAL_RUNTIME_TREE_GUARD_AUDIT.md" in text
    assert "no runtime vendor SDK import or provider client construction appears in `lima/`" in text
    assert "V1_G61_OPERATOR_DECISION_PACKET_STATUS_AUDIT.md" in text
    assert "only the exact `Approve-V1-G61` wording can unlock the future approved implementation branch" in text
    assert "V1_POST_G61_REQUEST_READINESS_REFRESH.md" in text
    assert "V1_CURRENT_GATE_CONSISTENCY_AUDIT.md" in text
    assert "rejects stale public Sparkbot publication or V1-G57 active-blocker language" in text
    assert "V1_CANDIDATE_TEST_HANDOFF_MANIFEST.md" in text
    assert "V1_CANDIDATE_HARNESS_QUICKSTART.md" in text
    assert "V1_CANDIDATE_HARNESS_QUICKSTART_EXECUTION_AUDIT.md" in text
    assert "V1_CONSUMER_HARNESS_USABILITY_MATRIX.md" in text
    assert "V1_CONSUMER_CHECKPOINT_MANIFEST.md" in text
    assert "V1_CURRENT_CANDIDATE_VALIDATION_REFRESH_AUDIT.md" in text
    assert "V1_POST_VALIDATION_READINESS_CHANGE_FRESHNESS_AUDIT.md" in text
    assert "V1_ARC_BOT_SHELL_LOCAL_DRIFT_EXCLUSION_AUDIT.md" in text
    assert "V1_RELEASE_CANDIDATE_ACCEPTANCE_CHECKLIST.md" in text
    assert "V1_RELEASE_CANDIDATE_CUTOVER_RUNBOOK.md" in text
    assert "V1_FINAL_READINESS_AUDIT_TEMPLATE.md" in text
    assert "V1_FINAL_BLOCKER_REGISTER.md" in text
    assert "V1_OPERATOR_UNBLOCK_ACTION_PACKET.md" in text
    assert "V1_FINAL_CANDIDATE_BRANCH_INDEX.md" in text
    assert "operator handoff action" in text
    assert "saved candidate branch map" in text
    assert "Arc-Bot-shell smoke evidence is current compatibility evidence only" in text
    assert "unrelated local Arc worktree drift is excluded from V1 proof" in text
    assert "not clean-checkpoint evidence" in text
    assert "7 tracked modified files and 64 untracked files as excluded from V1 release-candidate/final-readiness proof" in text
    assert "same-day recheck evidence that approved G56 smoke proof paths remain clean" in text
    assert "A clean Arc-Bot-shell checkpoint proof is required before any release-candidate pass, final-readiness pass, branch, tag, cutover, or readiness claim." in text
    assert "focused current-gate/release-readiness validation as passing with 153 tests" in text
    assert "full LIMA suite passing with 5350 tests" in text
    assert "A later 2026-06-21 LIMA-only validation supplement" in text
    assert "37 focused G61 guard/operator/freshness tests" in text
    assert "147 focused V1 readiness regression tests" in text
    assert "full LIMA suite validation with 5359 tests" in text
    assert "protected runtime/dependency/support path status as clean" in text
    assert "does not claim Sparkbot or Arc-Bot-shell checkpoints were rerun" in text
    assert "latest 2026-06-21 LIMA readiness freshness supplement" in text
    assert "15 focused final blocker/index tests" in text
    assert "89 broader affected V1 readiness tests" in text
    assert "full LIMA suite validation with 5361 tests" in text
    assert "does not claim Sparkbot or Arc-Bot-shell checkpoints were rerun or create release, cutover, final-readiness, or G61 implementation authority" in text
    assert "latest 2026-06-21 handoff freshness supplement" in text
    assert "8 focused post-G61 request-refresh tests" in text
    assert "117 broader G61/readiness tests" in text
    assert "7 focused candidate harness quickstart tests" in text
    assert "64 adjacent harness/readiness tests" in text
    assert "133 broader G61/readiness tests" in text
    assert "full LIMA suite validation with 5362 and 5364 tests" in text
    assert "does not claim Sparkbot or Arc-Bot-shell checkpoints were rerun or create release, cutover, final-readiness, Arc clean-checkpoint, consumer production integration, or G61 implementation authority" in text
    assert "candidate harness quickstart execution audit now records same-turn consumer smoke refresh evidence" in text
    assert "public Sparkbot, accessible Sparkbot, and Arc-Bot-shell each passing 8 tests" in text
    assert "17 focused quickstart/handoff tests" in text
    assert "108 broader V1 harness/readiness tests" in text
    assert "5360 full-suite tests" in text
    assert "post-validation readiness-change freshness audit records that later readiness docs, fixtures, or tests require same-turn focused, full-suite, and diff-check evidence" in text
    assert "current same-turn full-suite freshness evidence passing 5359 tests after release/cutover freshness checks" in text
    assert "latest quickstart post-refresh full-suite evidence passing 5360 tests" in text
    assert "latest final blocker/index refresh evidence passing" in text
    assert "15 focused final blocker/index tests" in text
    assert "89 broader affected V1 readiness tests" in text
    assert "5361 full-suite tests" in text
    assert "latest post-G61 request readiness-refresh supplement evidence passing 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, and 5362 full-suite tests" in text
    assert "latest quickstart artifact refresh evidence passing 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5364 full-suite tests" in text
    assert "current validation refresh evidence, post-validation freshness evidence, and clean Arc-Bot-shell checkpoint proof before any future V1.0.0 release-candidate branch, tag, cutover, or readiness claim" in text
    assert "consumer smoke path testable with fake in-process executors and sanitized fixtures" in text
    assert "The V1.0.0 release-candidate acceptance checklist and cutover runbook still require post-G61 refresh." in text
    assert "Do not create a V1.0.0 release-candidate branch, release tag, cutover claim, or readiness claim until clean Arc-Bot-shell checkpoint proof is recorded, the release checklist and cutover runbook are updated after G61 closeout, and the future final readiness audit passes." in text
    assert "former public Sparkbot G56 GitHub 403 publication blocker is resolved" in text
    assert "V1_PUBLIC_SPARKBOT_G56_PUBLICATION_RESOLUTION_AUDIT.md" in text
    assert "public Sparkbot remote publication remains blocked by GitHub 403" not in text
    assert "`V1-G60` is complete as approved dependency declaration" in text
    assert "`openai>=1.0.0,<3.0.0`" in text
    assert "The active next V1 lane is post-G61 release-candidate readiness refresh." in text
    assert "the bounded V1-G61 runtime vendor SDK import execution proof is complete as local test-scoped evidence" in text
    assert "Do not edit lockfiles, add runtime vendor SDK imports in `lima/`, add built-in provider SDK clients" in text
    assert "edit lockfiles" in text
    assert "add runtime vendor SDK imports in `lima/`" in text
    assert "add built-in provider SDK clients" in text
    assert "make LIMA-owned network calls" in text
    assert "read secrets" in text
    assert "access credential values" in text
    assert "change provider configuration" in text
    assert "execute fallback" in text
    assert "wire consumer production runtime behavior" in text
    assert "Existing V1 candidate slices remain non-production evidence only" in text
    assert "does not authorize runtime import execution, built-in SDK clients" in text
    assert "LIMA-owned network, credential" in text
    assert "physical-world behavior" in text


def test_current_project_state_contains_current_g61_gate_snapshot() -> None:
    fixture = _load_fixture()
    state_text = (
        REPO_ROOT / fixture["documents"]["current_project_state"]
    ).read_text(encoding="utf-8")

    assert "### Current V1 Gate Snapshot" in state_text
    assert "LIMA remains `CANDIDATE_ONLY`." in state_text
    assert "V1 runtime authority chain audit through G56: complete." in state_text
    assert "V1 readiness rollup through G60: complete." in state_text
    assert "V1 post-G60 next-lane decision matrix: complete." in state_text
    assert "V1-G55 real provider SDK/network egress wrapper: implemented and independently audited" in state_text
    assert "Public Sparkbot G56 publication blocker: resolved" in state_text
    assert "V1_PUBLIC_SPARKBOT_G56_PUBLICATION_RESOLUTION_AUDIT.md" in state_text
    assert "Public Sparkbot remote publication remains blocked by GitHub 403" not in state_text
    assert "V1-G56 consumer fake-executor provider SDK/network egress smoke: implemented and audited" in state_text
    assert "V1-G60 SDK dependency declaration and vendor provider SDK import-boundary evidence: implemented and audited" in state_text
    assert "V1-G61 runtime vendor SDK import execution proof approval packet: approved and completed as bounded local import proof." in state_text
    assert "V1-G61 request-gate audit: complete as request-only evidence" in state_text
    assert "V1-G61 preapproval runtime-tree guard audit: complete as request-only evidence" in state_text
    assert "V1_G61_PREAPPROVAL_RUNTIME_TREE_GUARD_AUDIT.md" in state_text
    assert "V1-G61 operator decision packet status audit: complete as request-only evidence" in state_text
    assert "V1_G61_OPERATOR_DECISION_PACKET_STATUS_AUDIT.md" in state_text
    assert "V1 post-G61 request readiness refresh: complete as request-only evidence" in state_text
    assert "V1 current gate consistency audit: complete as docs/tests/fixtures-only evidence" in state_text
    assert "V1_CURRENT_GATE_CONSISTENCY_AUDIT.md" in state_text
    assert "V1 candidate test handoff manifest: refreshed" in state_text
    assert "V1_CANDIDATE_TEST_HANDOFF_MANIFEST.md" in state_text
    assert "Arc-Bot-shell local checkpoint caveat" in state_text
    assert "unrelated local Arc worktree drift is excluded from V1 proof" in state_text
    assert "not clean-checkpoint evidence" in state_text
    assert "current drift exclusion audit records 7 tracked modified files and 64 untracked files as excluded from V1 release-candidate/final-readiness proof" in state_text
    assert "same-day recheck evidence that approved G56 smoke proof paths remain clean" in state_text
    assert "V1_ARC_BOT_SHELL_LOCAL_DRIFT_EXCLUSION_AUDIT.md" in state_text
    assert "A clean Arc-Bot-shell checkpoint proof is required before any release-candidate pass, final-readiness pass, branch, tag, cutover, or readiness claim." in state_text
    assert "V1 candidate harness quickstart: added" in state_text
    assert "QUICKSTART_READY_FOR_LOCAL_CANDIDATE_SMOKE_WITH_G61_OPERATOR_BLOCKER" in state_text
    assert "V1_CANDIDATE_HARNESS_QUICKSTART.md" in state_text
    assert "V1 candidate harness quickstart execution audit: complete" in state_text
    assert "PASS_LOCAL_CANDIDATE_HARNESS_QUICKSTART_WITH_G61_OPERATOR_BLOCKER" in state_text
    assert "V1_CANDIDATE_HARNESS_QUICKSTART_EXECUTION_AUDIT.md" in state_text
    assert "V1 candidate harness quickstart same-turn consumer smoke refresh" in state_text
    assert "public Sparkbot, accessible Sparkbot, and Arc-Bot-shell each passing 8 smoke tests" in state_text
    assert "post-refresh LIMA validation passing 17 focused quickstart/handoff tests, 108 broader V1 harness/readiness tests, and 5360 full-suite tests" in state_text
    assert "Arc-Bot-shell remains compatibility evidence only while unrelated local drift is excluded from V1 proof" in state_text
    assert "V1 consumer harness usability matrix: refreshed" in state_text
    assert "V1_CONSUMER_HARNESS_USABILITY_MATRIX.md" in state_text
    assert "V1_CONSUMER_CHECKPOINT_MANIFEST.md" in state_text
    assert "V1 current candidate validation refresh audit: complete" in state_text
    assert "focused current-gate/release-readiness validation passing 153 tests" in state_text
    assert "full LIMA suite passing 5350 tests" in state_text
    assert "V1_CURRENT_CANDIDATE_VALIDATION_REFRESH_AUDIT.md" in state_text
    assert "V1 current candidate validation refresh LIMA-only supplement" in state_text
    assert "recorded on 2026-06-21" in state_text
    assert "37 focused G61 guard/operator/freshness tests" in state_text
    assert "147 focused V1 readiness regression tests" in state_text
    assert "full LIMA suite validation with 5359 tests" in state_text
    assert "protected runtime/dependency/support path status clean" in state_text
    assert "does not claim Sparkbot or Arc-Bot-shell checkpoints were rerun" in state_text
    assert "does not create release-candidate or G61 implementation authority" in state_text
    assert "V1 current candidate validation refresh latest LIMA readiness freshness supplement" in state_text
    assert "15 focused final blocker/index tests" in state_text
    assert "89 broader affected V1 readiness tests" in state_text
    assert "full LIMA suite validation with 5361 tests" in state_text
    assert "does not create release-candidate, cutover, final-readiness, or G61 implementation authority" in state_text
    assert "V1 current candidate validation refresh latest handoff freshness supplement" in state_text
    assert "8 focused post-G61 request-refresh tests" in state_text
    assert "117 broader G61/readiness tests" in state_text
    assert "7 focused candidate harness quickstart tests" in state_text
    assert "64 adjacent harness/readiness tests" in state_text
    assert "133 broader G61/readiness tests" in state_text
    assert "full LIMA suite validation with 5362 and 5364 tests" in state_text
    assert "does not create release-candidate, cutover, final-readiness, Arc-Bot-shell clean-checkpoint, consumer production integration, or G61 implementation authority" in state_text
    assert "V1 post-validation readiness-change freshness audit: added" in state_text
    assert "same-turn focused, full-suite, and diff-check evidence requirements" in state_text
    assert "current same-turn full-suite freshness evidence passing 5359 tests after release/cutover freshness checks" in state_text
    assert "latest quickstart post-refresh full-suite evidence passing 5360 tests" in state_text
    assert "latest final blocker/index refresh evidence passing 15 focused final blocker/index tests, 89 broader affected readiness tests, and 5361 full-suite tests" in state_text
    assert "V1 post-validation readiness-change latest post-G61 request supplement: recorded on 2026-06-21 with 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, full LIMA suite validation with 5362 tests" in state_text
    assert "V1 post-validation readiness-change latest quickstart artifact refresh supplement: recorded on 2026-06-21 with 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, full LIMA suite validation with 5364 tests" in state_text
    assert "does not claim Sparkbot or Arc-Bot-shell checkpoints were rerun and does not create release-candidate, cutover, final-readiness, production, Arc-Bot-shell clean-checkpoint, or G61 implementation authority" in state_text
    assert "V1_POST_VALIDATION_READINESS_CHANGE_FRESHNESS_AUDIT.md" in state_text
    assert "V1 release-candidate acceptance checklist: added" in state_text
    assert "V1_RELEASE_CANDIDATE_ACCEPTANCE_CHECKLIST.md" in state_text
    assert "NOT_RELEASE_CANDIDATE_ARC_CLEAN_CHECKPOINT_AND_FINAL_READINESS_BLOCKERS" in state_text
    assert "V1 release-candidate cutover runbook: added" in state_text
    assert "V1_RELEASE_CANDIDATE_CUTOVER_RUNBOOK.md" in state_text
    assert "CUTOVER_BLOCKED_AT_ARC_CLEAN_CHECKPOINT_AND_FINAL_READINESS" in state_text
    assert "V1 final readiness audit template: refreshed" in state_text
    assert "refreshed to require current validation refresh evidence through latest LIMA readiness freshness 15/89/5361 validation and latest handoff freshness 8/117/5362 plus 7/64/133/5364 validation, post-validation readiness-change freshness evidence, and clean Arc-Bot-shell checkpoint proof before any future pass" in state_text
    assert "V1_FINAL_READINESS_AUDIT_TEMPLATE.md" in state_text
    assert "V1 final blocker register: refreshed with active G61 operator-decision blocker" in state_text
    assert "V1_FINAL_BLOCKER_REGISTER.md" in state_text
    assert "V1 operator unblock action packet: added as the current operator handoff packet" in state_text
    assert "V1_OPERATOR_UNBLOCK_ACTION_PACKET.md" in state_text
    assert "V1 final candidate branch index: refreshed as the saved branch/checkpoint map" in state_text
    assert "V1_FINAL_CANDIDATE_BRANCH_INDEX.md" in state_text
    assert "V1-G61 valid operator choices: `Approve-V1-G61`, `Revise-V1-G61`, or `Pause`." in state_text
    assert "V1-G61 implementation approval recorded: yes, limited to bounded local import proof." in state_text
    assert "Current snapshot authority note" in state_text
    assert "the `Current V1 Gate Snapshot` above is the controlling V1 state" in state_text
    assert "do not override the post-G61 release-readiness gate" in state_text
    assert "The next smallest safe V1 step is post-G61 release-candidate readiness refresh." in state_text
    assert "Do not create a V1.0.0 release-candidate branch, release tag, cutover claim, or readiness claim until" in state_text
    assert "clean Arc-Bot-shell checkpoint proof, and the future final readiness audit are refreshed and pass after G61 closeout" in state_text
    assert "V1_RELEASE_CANDIDATE_CUTOVER_RUNBOOK.md" in state_text
    assert "After the bounded V1-G61 import proof, do not edit Sparkbot or Arc-Bot-shell for G61" in state_text
    assert "make LIMA-owned DNS/HTTP/socket/network calls" in state_text
    assert "read secrets" in state_text
    assert "edit Sparkbot or Arc-Bot-shell for G61" in state_text
    assert "claim V1/product/production readiness" in state_text


def test_current_status_docs_reject_stale_active_blocker_language() -> None:
    fixture = _load_fixture()
    current_status_docs = [
        fixture["documents"]["readme"],
        fixture["documents"]["current_project_state"],
        "docs/V1_PRODUCT_READINESS_TARGET.md",
        "docs/V1_READINESS_GAP_MATRIX.md",
        "docs/readiness/V1_FINAL_BLOCKER_REGISTER.md",
        "docs/readiness/V1_OPERATOR_UNBLOCK_ACTION_PACKET.md",
    ]
    combined_text = "\n".join(
        (REPO_ROOT / relative_path).read_text(encoding="utf-8")
        for relative_path in current_status_docs
    )

    for stale_phrase in (
        "public Sparkbot remote publication remains blocked by GitHub 403",
        "public Sparkbot publication blocker is unresolved",
        "public Sparkbot publication blocker is still unresolved",
        "public Sparkbot write-credential gate",
        "missing_write_credentials",
        "target_push_still_blocked",
        "The remaining V1 blocker is the V1-G57 operator decision",
        "remaining V1 blocker is the V1-G57 operator decision",
        "V1-G57 still requires exactly one valid operator decision",
        "record exactly one V1-G57 operator choice",
        "Do not implement V1-G57 unless",
    ):
        assert stale_phrase not in combined_text
