"""Static checks for the V1 final blocker register."""

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
    / "v1_final_blocker_register.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_final_blocker_register_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["register_id"] == "v1_final_blocker_register"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["date"] == "2026-06-21"
    assert fixture["branch"] == (
        "docs-v1-post-g60-readiness-and-next-lane-matrix"
    )
    assert fixture["observed_workspace_branch"] == (
        "docs-v1-post-g60-readiness-and-next-lane-matrix"
    )
    assert fixture["source_lima_commit_before_register_refresh"] == (
        "37626bf236bf96c8a57a3ca351668e90eeb0e651"
    )
    assert fixture["register_verdict"] == "STOPPED_AT_V1_G61_OPERATOR_DECISION"

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_final_blocker_register_records_verified_blockers() -> None:
    blockers = _load_fixture()["verified_blockers"]
    g61 = blockers["v1_g61_implementation"]

    assert g61["implementation_approval_recorded"] is False
    assert g61["valid_operator_choices"] == [
        "Approve-V1-G61",
        "Revise-V1-G61",
        "Pause",
    ]
    assert g61["required_unblock"] == (
        "record_exactly_one_valid_v1_g61_operator_choice"
    )

    assert blockers["release_candidate_acceptance"] == {
        "checklist": "docs/readiness/V1_RELEASE_CANDIDATE_ACCEPTANCE_CHECKLIST.md",
        "current_verdict": "NOT_RELEASE_CANDIDATE_ARC_CLEAN_CHECKPOINT_AND_FINAL_READINESS_BLOCKERS",
        "passed": False,
        "required_unblock": (
            "g61_resolved_approved_work_closed_current_validation_rerun_and_checklist_passed"
        ),
    }
    assert blockers["release_candidate_cutover"] == {
        "runbook": "docs/readiness/V1_RELEASE_CANDIDATE_CUTOVER_RUNBOOK.md",
        "current_verdict": "CUTOVER_BLOCKED_AT_ARC_CLEAN_CHECKPOINT_AND_FINAL_READINESS",
        "authorized": False,
        "required_unblock": (
            "release_candidate_acceptance_checklist_and_final_readiness_audit_pass"
        ),
    }
    assert blockers["final_readiness_audit"] == {
        "template": "docs/readiness/V1_FINAL_READINESS_AUDIT_TEMPLATE.md",
        "executed_or_passed": False,
        "required_unblock": (
            "post_g61_validation_release_checklist_consumer_smoke_protected_surface_and_explicit_final_audit_pass"
        ),
    }
    assert blockers["arc_bot_shell_clean_checkpoint"] == {
        "current_evidence": (
            "local_fake_executor_compatibility_smoke_only_with_unrelated_local_drift_excluded"
        ),
        "same_day_approved_g56_smoke_proof_paths_clean": True,
        "clean_checkpoint_proof_recorded": False,
        "required_unblock": (
            "clean_checkpoint_proof_recorded_after_local_drift_absent_or_resolved_and_revalidated_before_release_final_branch_tag_cutover_or_readiness_claim"
        ),
    }


def test_v1_final_blocker_register_records_resolved_public_sparkbot() -> None:
    resolved = _load_fixture()["resolved_blockers"]["public_sparkbot_publication"]

    assert resolved["target_repository"] == "sparkpit-labs/Sparkbot"
    assert resolved["branch"] == "v1-g56-runtime-authority-chain-audit"
    assert resolved["commit"] == "ae5cc9c563ea2b0f08c91af03164a78b4b20e3e2"
    assert resolved["verified_remote_ref"] == (
        "ae5cc9c563ea2b0f08c91af03164a78b4b20e3e2 "
        "refs/heads/v1-g56-runtime-authority-chain-audit"
    )
    assert resolved["main_head"] == "ddaa019272ad11bb56d4660be7d44e81810814a7"
    assert resolved["resolved"] is True

    chain = _load_fixture()["resolved_blockers"]["provider_authority_chain_through_g60"]
    assert chain == {
        "v1_g57_complete": True,
        "v1_g58_complete": True,
        "v1_g59_complete": True,
        "v1_g60_complete": True,
        "candidate_only": True,
        "g61_implementation_approval_implied": False,
    }


def test_v1_final_blocker_register_preserves_all_boundaries() -> None:
    boundaries = _load_fixture()["boundaries_preserved"]

    for key, value in boundaries.items():
        assert value is False, key


def test_v1_final_blocker_register_records_evidence_and_next_actions() -> None:
    fixture = _load_fixture()

    assert fixture["current_verified_evidence"] == [
        "v1_candidate_handoff_manifest_exists",
        "v1_candidate_handoff_execution_audit_exists",
        "v1_candidate_harness_quickstart_exists",
        "v1_candidate_harness_quickstart_execution_audit_exists",
        "v1_public_sparkbot_g56_publication_resolution_audit_exists",
        "v1_g60_implementation_evidence_exists",
        "v1_g60_independent_audit_exists",
        "v1_runtime_readiness_rollup_through_g60_exists",
        "v1_g61_approval_request_exists",
        "v1_g61_request_gate_audit_exists",
        "v1_g61_preapproval_runtime_tree_guard_audit_exists",
        "v1_g61_preapproval_runtime_tree_guard_audit_current_2026_06_21_no_openai_import_no_provider_client_no_future_files",
        "v1_g61_operator_decision_packet_status_audit_exists",
        "v1_g61_operator_decision_packet_status_audit_current_awaiting_choice",
        "v1_post_g61_request_readiness_refresh_exists",
        "v1_current_candidate_validation_refresh_audit_exists",
        "v1_current_gate_consistency_audit_exists",
        "v1_post_validation_readiness_change_freshness_audit_exists",
        "v1_post_validation_readiness_change_freshness_full_suite_passed_same_turn_5359",
        "v1_release_candidate_acceptance_checklist_exists",
        "v1_release_candidate_acceptance_checklist_current_not_release_candidate_g61_operator_blocker",
        "v1_release_candidate_cutover_runbook_exists",
        "v1_release_candidate_cutover_runbook_current_cutover_blocked_at_g61_operator_decision",
        "v1_final_readiness_audit_template_exists_future_scaffolding_only",
        "public_sparkbot_local_g56_fake_executor_smoke_passed",
        "accessible_sparkbot_g56_fake_executor_smoke_passed",
        "arc_bot_shell_g56_fake_executor_smoke_passed",
        "same_turn_consumer_smoke_refresh_public_accessible_arc_8_each_with_arc_compatibility_only",
        "arc_bot_shell_same_day_recheck_approved_g56_smoke_proof_paths_clean",
        "arc_bot_shell_local_drift_exclusion_audit_current_7_modified_49_untracked_excluded_from_release_proof",
        "arc_bot_shell_local_drift_excluded_from_v1_proof",
        "consumer_repo_diff_hygiene_passed_with_arc_local_drift_caveat",
        "lima_focused_g61_handoff_status_tests_passed_prior_current_gate_set_153",
        "lima_full_suite_passed_prior_current_evidence_5350",
        "lima_post_validation_readiness_freshness_full_suite_passed_same_turn_5359",
        "lima_quickstart_post_refresh_validation_17_108_5360_passed",
        "lima_latest_final_blocker_index_refresh_15_89_5361_passed",
        "lima_latest_post_g61_request_readiness_refresh_8_117_5362_passed",
        "lima_latest_quickstart_artifact_refresh_7_64_133_5364_passed",
        "lima_latest_handoff_freshness_8_117_5362_plus_7_64_133_5364_passed",
        "lima_diff_hygiene_passed",
    ]
    assert fixture["next_unblock_actions"] == [
        "record_exactly_one_v1_g61_operator_choice",
        "if_approve_v1_g61_is_recorded_implement_only_runtime_vendor_sdk_import_execution_proof_scope",
        "rerun_current_candidate_validation_after_any_approved_g61_work",
        "pass_release_candidate_acceptance_checklist_final_readiness_audit_and_clean_arc_checkpoint_proof_before_branch_tag_cutover_or_readiness",
    ]


def test_v1_final_blocker_register_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["final_blocker_register"]).read_text(
        encoding="utf-8"
    )

    assert "# V1 Final Blocker Register" in text
    assert "STOPPED_AT_V1_G61_OPERATOR_DECISION" in text
    assert "V1_PUBLIC_SPARKBOT_G56_PUBLICATION_RESOLUTION_AUDIT.md" in text
    assert "V1_CANDIDATE_HARNESS_QUICKSTART_EXECUTION_AUDIT.md" in text
    assert "V1_CURRENT_CANDIDATE_VALIDATION_REFRESH_AUDIT.md" in text
    assert "V1_CURRENT_GATE_CONSISTENCY_AUDIT.md" in text
    assert "V1_POST_VALIDATION_READINESS_CHANGE_FRESHNESS_AUDIT.md" in text
    assert "V1_G61_PREAPPROVAL_RUNTIME_TREE_GUARD_AUDIT.md" in text
    assert "V1-G61 preapproval runtime-tree guard audit current: satisfied, refreshed on 2026-06-21" in text
    assert "no `openai` import, no provider SDK client construction, and no future G61 implementation files present before approval" in text
    assert "V1_G61_OPERATOR_DECISION_PACKET_STATUS_AUDIT.md" in text
    assert "V1_ARC_BOT_SHELL_LOCAL_DRIFT_EXCLUSION_AUDIT.md" in text
    assert "V1_RELEASE_CANDIDATE_ACCEPTANCE_CHECKLIST.md" in text
    assert "V1_RELEASE_CANDIDATE_CUTOVER_RUNBOOK.md" in text
    assert "V1_FINAL_READINESS_AUDIT_TEMPLATE.md" in text
    assert "NOT_RELEASE_CANDIDATE_ARC_CLEAN_CHECKPOINT_AND_FINAL_READINESS_BLOCKERS" in text
    assert "CUTOVER_BLOCKED_AT_ARC_CLEAN_CHECKPOINT_AND_FINAL_READINESS" in text
    assert "future audit scaffolding only" in text
    assert "This register is not release-candidate authority" in text
    assert "does not authorize a V1.0.0 branch, tag, release cutover" in text
    assert "V1-G61 operator decision packet status audit current: satisfied, awaiting exactly one valid operator choice." in text
    assert "earlier current-gate/release-readiness set 153 tests before later readiness freshness supplements" in text
    assert "earlier current evidence 5350 tests before later readiness freshness supplements" in text
    assert "same-turn evidence 5359 tests after release/cutover freshness checks" in text
    assert "Same-turn consumer smoke refresh: passed, public Sparkbot 8 tests, accessible Sparkbot 8 tests, and Arc-Bot-shell 8 tests; Arc-Bot-shell remains compatibility evidence only while unrelated local drift is excluded." in text
    assert "Arc-Bot-shell same-day approved G56 smoke proof-path recheck: passed; approved proof paths remain clean while unrelated local drift remains excluded from V1 release-candidate/final-readiness proof." in text
    assert "LIMA quickstart post-refresh validation: passed, 17 focused quickstart/handoff tests, 108 broader V1 harness/readiness tests, and 5360 full-suite tests." in text
    assert "LIMA latest final blocker/index readiness refresh: passed, 15 focused final blocker/index tests, 89 broader affected V1 readiness tests, and 5361 full-suite tests." in text
    assert "LIMA latest post-G61 request readiness-refresh: passed, 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, and 5362 full-suite tests." in text
    assert "LIMA latest quickstart artifact refresh: passed, 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5364 full-suite tests." in text
    assert "LIMA latest handoff freshness supplement: passed, 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5362/5364 full-suite tests." in text
    assert "7 tracked modified files and 64 untracked files excluded from V1 release-candidate/final-readiness proof" in text
    assert "Arc-Bot-shell local worktree drift is excluded from V1 proof" in text
    assert "not clean-checkpoint evidence" in text
    assert "clean checkpoint proof recorded after local drift is absent or resolved and revalidated before any release-candidate pass, final-readiness pass, branch, tag, cutover, or readiness claim" in text
    assert "Public Sparkbot G56 branch pushed to `sparkpit-labs/Sparkbot`: yes." in text
    assert "Release-candidate branch or tag authority created by this register: no." in text
    assert "Release-candidate cutover authorized by this register: no." in text
    assert "Final readiness audit executed or passed by this register: no." in text
    assert "Arc-Bot-shell clean-checkpoint proof claimed by this register: no." in text
    assert "Pass the release-candidate acceptance checklist, final readiness audit, and clean Arc-Bot-shell checkpoint proof" in text
    assert "Approve-V1-G61" in text
    assert "V1-G61 implementation approval recorded: no." in text
    assert "V1-G61 runtime vendor SDK import execution proof implemented: no." in text
    assert "Provider SDK clients added: no." in text
    assert "V1.0 completion, product readiness, or production readiness claimed: no." in text


def test_v1_final_blocker_register_has_no_sensitive_markers() -> None:
    fixture = _load_fixture()
    output = json.dumps(fixture, sort_keys=True)
    output += (REPO_ROOT / fixture["documents"]["final_blocker_register"]).read_text(
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
