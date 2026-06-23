"""Static checks for the V1 operator unblock action packet."""

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
    / "v1_operator_unblock_action_packet.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_operator_unblock_packet_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["packet_id"] == "v1_operator_unblock_action_packet"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["date"] == "2026-06-21"
    assert fixture["branch"] == "docs-v1-g61-operator-unblock-action-packet-refresh"
    assert fixture["source_lima_commit_before_packet_refresh"] == (
        "37626bf236bf96c8a57a3ca351668e90eeb0e651"
    )
    assert fixture["packet_verdict"] == "AWAITING_OPERATOR_G61_DECISION"

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_operator_unblock_packet_records_resolved_prior_actions() -> None:
    resolved = _load_fixture()["resolved_prior_actions"]

    publication = resolved["public_sparkbot_publication"]
    assert publication["target_repository"] == "sparkpit-labs/Sparkbot"
    assert publication["branch"] == "v1-g56-runtime-authority-chain-audit"
    assert publication["commit"] == "ae5cc9c563ea2b0f08c91af03164a78b4b20e3e2"
    assert publication["verified_remote_ref"] == (
        "ae5cc9c563ea2b0f08c91af03164a78b4b20e3e2 "
        "refs/heads/v1-g56-runtime-authority-chain-audit"
    )
    assert publication["resolution_audit"] == (
        "docs/audits/V1_PUBLIC_SPARKBOT_G56_PUBLICATION_RESOLUTION_AUDIT.md"
    )
    assert publication["resolved"] is True

    g57 = resolved["v1_g57_decision_and_implementation"]
    assert g57["decision_packet"] == (
        "docs/V1_G57_PROVIDER_EXECUTION_HARDENING_AUTHORIZATION_OPERATOR_DECISION_PACKET.md"
    )
    assert g57["implementation_evidence"] == (
        "docs/V1_G57_PROVIDER_EXECUTION_HARDENING_AUTHORIZATION.md"
    )
    assert g57["independent_audit"] == (
        "docs/audits/V1_G57_PROVIDER_EXECUTION_HARDENING_AUTHORIZATION_AUDIT.md"
    )
    assert g57["completed_and_audited_as_candidate_only"] is True


def test_v1_operator_unblock_packet_records_exact_g61_decision_action() -> None:
    action = _load_fixture()["required_operator_actions"]["v1_g61_operator_decision"]

    assert action["required_action"] == (
        "record_exactly_one_valid_v1_g61_operator_choice"
    )
    assert action["valid_choices"] == ["Approve-V1-G61", "Revise-V1-G61", "Pause"]
    assert action["operator_choice_recorded_by_packet"] is False
    assert action["exact_approve_text"] == (
        "Approve-V1-G61\n\n"
        "I explicitly approve V1-G61 implementation of the runtime vendor SDK "
        "import execution proof slice, limited to the file "
        "scope, behavior scope, tests, rollback plan, and stop conditions in "
        "docs/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_APPROVAL_REQUEST.md."
    )
    assert action["decision_packet"] == (
        "docs/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_OPERATOR_DECISION_PACKET.md"
    )
    assert action["decision_packet_status_audit"] == (
        "docs/audits/V1_G61_OPERATOR_DECISION_PACKET_STATUS_AUDIT.md"
    )
    assert action["approval_request"] == (
        "docs/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_APPROVAL_REQUEST.md"
    )
    assert action["approved_future_file_scope_if_approved"] == [
        "docs/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF.md",
        "docs/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g61_runtime_vendor_sdk_import_execution_proof.json",
        "tests/test_v1_g61_runtime_vendor_sdk_import_execution_proof.py",
    ]
    assert action["close_evidence_required"] == [
        "g61_operator_decision_packet_status_audit_current_and_consistent_with_recorded_decision_state",
        "candidate_harness_quickstart_execution_audit_current_consumers_8_8_8_lima_17_108_5360",
        "post_validation_readiness_change_freshness_current_5359_latest_quickstart_5360_final_blocker_index_15_89_5361_post_g61_request_8_117_5362_and_quickstart_artifact_7_64_133_5364_full_suite_evidence",
        "arc_bot_shell_local_drift_exclusion_audit_current_same_day_recheck_proof_paths_clean_dirty_arc_compatibility_only",
        "exactly_one_valid_operator_choice_recorded",
        "if_approve_v1_g61_then_implementation_stays_in_approved_test_scoped_import_proof_scope",
        "if_revise_or_pause_then_implementation_does_not_begin",
        "post_validation_readiness_change_freshness_evidence_remains_current_before_release_final_branch_tag_cutover_or_readiness_claim",
        "g61_decision_does_not_pass_release_checklist_authorize_cutover_execute_final_readiness_or_prove_arc_clean_checkpoint",
    ]


def test_v1_operator_unblock_packet_preserves_current_evidence_and_boundaries() -> None:
    fixture = _load_fixture()

    assert fixture["current_evidence_to_preserve"] == [
        "v1_public_sparkbot_g56_publication_resolution_audit",
        "v1_g57_provider_execution_hardening_authorization_audit",
        "v1_g60_sdk_dependency_vendor_provider_sdk_import_audit",
        "v1_g61_request_gate_audit",
        "v1_g61_preapproval_runtime_tree_guard_audit",
        "v1_g61_preapproval_runtime_tree_guard_audit_current_2026_06_21_no_openai_import_no_provider_client_no_future_files",
        "v1_g61_operator_decision_packet_status_audit",
        "v1_post_g61_request_readiness_refresh",
        "v1_candidate_harness_quickstart",
        "v1_candidate_harness_quickstart_execution_audit",
        "v1_candidate_harness_quickstart_post_refresh_consumers_8_8_8_lima_17_108_5360",
        "v1_consumer_harness_usability_matrix",
        "v1_current_gate_consistency_audit",
        "v1_current_candidate_validation_refresh_audit",
        "v1_post_validation_readiness_change_freshness_audit",
        "v1_post_validation_readiness_change_freshness_full_suite_passed_same_turn_5359",
        "v1_latest_quickstart_post_refresh_full_suite_passed_5360",
        "v1_latest_final_blocker_index_refresh_15_89_5361_passed",
        "v1_latest_post_g61_request_readiness_refresh_8_117_5362_passed",
        "v1_latest_quickstart_artifact_refresh_7_64_133_5364_passed",
        "v1_latest_handoff_freshness_8_117_5362_plus_7_64_133_5364_passed",
        "v1_arc_bot_shell_local_drift_exclusion_audit_current_7_modified_49_untracked_excluded_from_release_proof",
        "v1_arc_bot_shell_same_day_drift_recheck_g56_proof_paths_clean_dirty_arc_compatibility_only",
        "v1_release_candidate_acceptance_checklist_not_release_candidate_g61_operator_blocker",
        "v1_release_candidate_cutover_runbook_cutover_blocked_at_g61_operator_decision",
        "v1_final_readiness_audit_template_future_scaffolding_only",
        "arc_bot_shell_local_drift_caveat_preserved_as_compatibility_only_until_clean_checkpoint_proof_recorded",
    ]

    for key, value in fixture["boundaries_preserved"].items():
        assert value is False, key


def test_v1_operator_unblock_packet_stop_conditions_and_next_step_are_bounded() -> None:
    fixture = _load_fixture()

    assert fixture["stop_conditions"] == [
        "v1_g61_implementation_without_exact_approval",
        "treat_this_packet_as_g61_approval",
        "treat_this_packet_as_release_candidate_branch_or_tag_authority",
        "treat_this_packet_as_passed_release_candidate_checklist_cutover_or_final_readiness_audit",
        "consumer_repo_edit_from_packet_lane",
        "arc_bot_shell_smoke_used_as_clean_checkpoint_while_local_drift_unresolved_or_only_excluded",
        "dependency_manifest_or_lockfile_edit_from_packet_lane",
        "runtime_or_public_api_change_from_packet_lane",
        "runtime_vendor_sdk_import_provider_client_secret_credential_token_endpoint_network_or_fallback_required",
        "raw_sensitive_or_patch_content_persistence",
        "v1_product_production_or_completion_claim",
    ]
    assert fixture["next_step_after_action"] == (
        "resolve_v1_g61_operator_decision_then_implement_only_approved_g61_scope_or_preserve_pause_revision_outcome_then_refresh_validation_preserve_post_validation_freshness_release_checklist_final_readiness_cutover_and_recorded_arc_clean_checkpoint_proof"
    )


def test_v1_operator_unblock_packet_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["operator_unblock_packet"]).read_text(
        encoding="utf-8"
    )

    assert "# V1 Operator Unblock Action Packet" in text
    assert fixture["source_lima_commit_before_packet_refresh"] in text
    assert "AWAITING_OPERATOR_G61_DECISION" in text
    assert "Approve-V1-G61" in text
    assert "I explicitly approve V1-G61 implementation" in text
    assert "Public Sparkbot V1-G56 publication is recorded as resolved" in text
    assert "V1_CANDIDATE_HARNESS_QUICKSTART_EXECUTION_AUDIT.md" in text
    assert "V1_CONSUMER_HARNESS_USABILITY_MATRIX.md" in text
    assert "V1_CURRENT_GATE_CONSISTENCY_AUDIT.md" in text
    assert "V1_CURRENT_CANDIDATE_VALIDATION_REFRESH_AUDIT.md" in text
    assert "V1_POST_VALIDATION_READINESS_CHANGE_FRESHNESS_AUDIT.md" in text
    assert "V1_ARC_BOT_SHELL_LOCAL_DRIFT_EXCLUSION_AUDIT.md" in text
    assert "V1_RELEASE_CANDIDATE_ACCEPTANCE_CHECKLIST.md" in text
    assert "V1_RELEASE_CANDIDATE_CUTOVER_RUNBOOK.md" in text
    assert "V1_FINAL_READINESS_AUDIT_TEMPLATE.md" in text
    assert "V1_G61_OPERATOR_DECISION_PACKET_STATUS_AUDIT.md" in text
    assert "V1_G61_PREAPPROVAL_RUNTIME_TREE_GUARD_AUDIT.md" in text
    assert "V1-G61 preapproval runtime-tree guard evidence: refreshed on 2026-06-21" in text
    assert "no `openai` import, no provider SDK client construction, and no future G61 implementation files present before approval" in text
    assert "This packet is not release-candidate branch, tag, cutover, or final readiness authority" in text
    assert "post-validation readiness-change freshness evidence to remain current" in text
    assert "Arc-Bot-shell clean-checkpoint proof to be recorded after local drift is absent or resolved and revalidated before any branch, tag, cutover, or readiness claim" in text
    assert "NOT_RELEASE_CANDIDATE_ARC_CLEAN_CHECKPOINT_AND_FINAL_READINESS_BLOCKERS" in text
    assert "CUTOVER_BLOCKED_AT_ARC_CLEAN_CHECKPOINT_AND_FINAL_READINESS" in text
    assert "Final readiness audit, not executed or passed by this packet" in text
    assert "Arc-Bot-shell clean checkpoint, not recorded" in text
    assert "7 tracked modified files and 64 untracked files as compatibility-only evidence excluded from release-candidate/final-readiness proof" in text
    assert "Post-validation readiness-change freshness evidence, currently same-turn full-suite freshness evidence of 5359 tests after release/cutover freshness checks, latest quickstart post-refresh full-suite evidence of 5360 tests, latest final blocker/index refresh evidence of 15 focused tests, 89 broader affected readiness tests, and 5361 full-suite tests, latest post-G61 request readiness-refresh evidence of 8 focused tests, 117 broader G61/readiness tests, and 5362 full-suite tests, and latest quickstart artifact refresh evidence of 7 focused tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5364 full-suite tests." in text
    assert "latest same-day recheck confirming approved G56 smoke proof paths remain clean" in text
    assert "candidate harness quickstart execution audit remains current and records public Sparkbot, accessible Sparkbot, and Arc-Bot-shell each passing 8 consumer smoke tests plus LIMA post-refresh validation passing 17 focused quickstart/handoff tests, 108 broader V1 harness/readiness tests, and 5360 full-suite tests" in text
    assert "post-validation readiness-change freshness evidence remains current, including same-turn 5359 full-suite evidence after release/cutover freshness checks, latest quickstart post-refresh 5360 full-suite evidence, latest final blocker/index 15/89/5361 evidence, latest post-G61 request readiness-refresh 8/117/5362 evidence, and latest quickstart artifact refresh 7/64/133/5364 evidence" in text
    assert "Arc-Bot-shell local drift exclusion audit remains current, including the same-day recheck that approved G56 smoke proof paths are clean and dirty Arc local work remains compatibility-only evidence" in text
    assert "V1 candidate harness quickstart post-refresh validation: public Sparkbot 8 tests, accessible Sparkbot 8 tests, Arc-Bot-shell 8 tests, LIMA focused quickstart/handoff 17 tests, broader V1 harness/readiness 108 tests, and full LIMA suite 5360 tests" in text
    assert "V1 post-validation readiness-change freshness evidence: same-turn full-suite freshness evidence passing 5359 tests after release/cutover freshness checks" in text
    assert "V1 latest quickstart post-refresh full-suite freshness evidence: 5360 tests" in text
    assert "V1 latest final blocker/index freshness evidence: 15 focused final blocker/index tests, 89 broader affected readiness tests, and 5361 full-suite tests" in text
    assert "V1 latest post-G61 request readiness-refresh evidence: 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, and 5362 full-suite tests" in text
    assert "V1 latest quickstart artifact refresh evidence: 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5364 full-suite tests" in text
    assert "V1 latest handoff freshness supplement: 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5362/5364 full-suite tests" in text
    assert "V1 Arc-Bot-shell same-day drift recheck: approved G56 smoke proof paths clean; 7 tracked modified files and 64 untracked files remain compatibility-only evidence" in text
    assert "Arc-Bot-shell local drift caveat" in text
    assert "current drift exclusion records 7 tracked modified files and 64 untracked files as excluded from V1 release-candidate/final-readiness proof" in text
    assert "it is not release-candidate, final-readiness, branch, tag, cutover, or readiness evidence unless clean checkpoint proof is recorded" in text
    assert "use Arc-Bot-shell smoke evidence as clean-checkpoint evidence while unrelated local drift remains unresolved or only excluded from V1 proof" in text
    assert "treat this packet as release-candidate branch or tag authority" in text
    assert "treat this packet as a passed release-candidate checklist" in text
    assert "V1-G61 preapproval runtime-tree guard audit" in text
    assert "G61 operator decision packet status audit remains current and consistent with the recorded decision state" in text
    assert "V1-G61 operator decision recorded by this packet: no." in text
    assert "Release-candidate branch or tag authority created by this packet: no." in text
    assert "Release-candidate cutover authorized by this packet: no." in text
    assert "Final readiness audit executed or passed by this packet: no." in text
    assert "Arc-Bot-shell clean-checkpoint proof claimed by this packet: no." in text
    assert "V1.0 completion, product readiness, or production readiness claimed: no." in text
    assert "preserve post-validation readiness-change freshness evidence" in text


def test_v1_operator_unblock_packet_has_no_sensitive_markers() -> None:
    fixture = _load_fixture()
    output = json.dumps(fixture, sort_keys=True)
    output += (REPO_ROOT / fixture["documents"]["operator_unblock_packet"]).read_text(
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
