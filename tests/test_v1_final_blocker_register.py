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
    assert fixture["date"] == "2026-06-28"
    assert fixture["branch"] == (
        "docs-v1-post-g60-readiness-and-next-lane-matrix"
    )
    assert fixture["observed_workspace_branch"] == (
        "docs-v1-post-g60-readiness-and-next-lane-matrix"
    )
    assert fixture["source_lima_commit_before_register_refresh"] == (
        "bfa27f37212a24f0ca3e7d21c37e4ff80192db14"
    )
    assert fixture["register_verdict"] == "STOPPED_AT_CUTOVER_AUTHORITY"

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_final_blocker_register_records_verified_blockers() -> None:
    fixture = _load_fixture()
    blockers = fixture["verified_blockers"]
    resolved = fixture["resolved_blockers"]

    assert resolved["v1_g61_implementation"] == {
        "operator_decision": "Approve-V1-G61",
        "proof": "docs/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF.md",
        "closeout": "docs/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_CLOSEOUT.md",
        "bounded_local_import_proof_only": True,
        "resolved": True,
    }
    assert resolved["arc_bot_shell_clean_checkpoint"] == {
        "proof": "docs/audits/V1_ARC_BOT_SHELL_CLEAN_CHECKPOINT_PROOF.md",
        "clean_pushed_commit": "99a4ba4955f13626c2176a2c44592000029a16c3",
        "resolved": True,
        "release_authority_created": False,
    }
    assert "v1_g61_implementation" not in blockers
    assert "arc_bot_shell_clean_checkpoint" not in blockers

    assert resolved["release_candidate_acceptance"] == {
        "checklist": "docs/readiness/V1_RELEASE_CANDIDATE_ACCEPTANCE_CHECKLIST.md",
        "current_verdict": "CHECKLIST_SATISFIED_FOR_FIRST_CONSUMER_HARNESS_TESTING_CUTOVER_AUTHORIZATION_REQUIRED",
        "passed_for_first_consumer_harness_testing": True,
        "release_authority_created": False,
    }
    assert resolved["final_readiness_reconciliation"] == {
        "audit": "docs/audits/V1_FINAL_READINESS_RECONCILIATION_AUDIT.md",
        "verdict": "PASS_CANDIDATE_READY_FOR_FIRST_CONSUMER_HARNESS_TESTING_CUTOVER_AUTHORIZATION_REQUIRED",
        "resolved_for_first_consumer_harness_testing": True,
        "release_authority_created": False,
    }
    assert "release_candidate_acceptance" not in blockers
    assert "final_readiness_audit" not in blockers
    assert blockers["release_candidate_cutover"] == {
        "runbook": "docs/readiness/V1_RELEASE_CANDIDATE_CUTOVER_RUNBOOK.md",
        "current_verdict": "CUTOVER_BLOCKED_AT_OPERATOR_AUTHORIZATION",
        "authorized": False,
        "required_unblock": "approve_v1_rc_cutover_recorded_in_cutover_authorization_packet",
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

    assert boundaries["release_candidate_acceptance_checklist_passed_by_register"] is True
    assert boundaries["final_readiness_audit_passed_by_register"] is True

    for key, value in boundaries.items():
        if key in {
            "release_candidate_acceptance_checklist_passed_by_register",
            "final_readiness_audit_passed_by_register",
        }:
            continue
        assert value is False, key


def test_v1_final_blocker_register_records_evidence_and_next_actions() -> None:
    fixture = _load_fixture()
    evidence = set(fixture["current_verified_evidence"])

    required = {
        "v1_candidate_handoff_manifest_exists",
        "v1_g61_operator_decision_packet_status_audit_current_approve_v1_g61_recorded",
        "v1_g61_runtime_vendor_sdk_import_execution_proof_and_closeout_complete_bounded_local_only",
        "v1_release_candidate_acceptance_checklist_current_satisfied_for_first_consumer_harness_testing_cutover_authorization_required",
        "v1_release_candidate_cutover_runbook_current_cutover_blocked_at_operator_authorization",
        "arc_bot_shell_clean_checkpoint_proof_recorded_at_clean_pushed_commit_99a4ba4955f13626c2176a2c44592000029a16c3",
        "arc_bot_shell_historical_local_drift_exclusion_superseded_by_clean_checkpoint_proof",
        "consumer_repo_diff_hygiene_passed_at_recorded_checkpoints",
        "lima_diff_hygiene_passed",
        "v1_final_readiness_reconciliation_audit_passed_for_first_consumer_harness_testing",
        "v1_final_readiness_audit_current_consumer_smoke_8_8_8_lima_5391_passed",
    }
    assert required <= evidence
    assert "v1_g61_operator_decision_packet_status_audit_current_awaiting_choice" not in evidence
    assert "arc_bot_shell_local_drift_excluded_from_v1_proof" not in evidence
    assert fixture["next_unblock_actions"] == [
        "record_exactly_one_valid_cutover_operator_choice_before_branch_tag_cutover_or_readiness_claim",
        "refresh_validation_if_release_readiness_artifacts_change_before_cutover",
        "confirm_checklist_reconciliation_and_arc_clean_checkpoint_remain_current_before_branch_tag_cutover_or_readiness",
    ]
def test_v1_final_blocker_register_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["final_blocker_register"]).read_text(
        encoding="utf-8"
    )

    assert "# V1 Final Blocker Register" in text
    assert "STOPPED_AT_CUTOVER_AUTHORITY" in text
    assert "V1_PUBLIC_SPARKBOT_G56_PUBLICATION_RESOLUTION_AUDIT.md" in text
    assert "V1_CANDIDATE_HARNESS_QUICKSTART_EXECUTION_AUDIT.md" in text
    assert "V1_CURRENT_CANDIDATE_VALIDATION_REFRESH_AUDIT.md" in text
    assert "V1_CURRENT_GATE_CONSISTENCY_AUDIT.md" in text
    assert "V1_POST_VALIDATION_READINESS_CHANGE_FRESHNESS_AUDIT.md" in text
    assert "V1_G61_PREAPPROVAL_RUNTIME_TREE_GUARD_AUDIT.md" in text
    assert "V1-G61 preapproval runtime-tree guard audit current: satisfied before approval" in text
    assert "no `openai` import, no provider SDK client construction, and no unapproved future G61 implementation files present" in text
    assert "V1_G61_OPERATOR_DECISION_PACKET_STATUS_AUDIT.md" in text
    assert "V1_ARC_BOT_SHELL_LOCAL_DRIFT_EXCLUSION_AUDIT.md" in text
    assert "V1_RELEASE_CANDIDATE_ACCEPTANCE_CHECKLIST.md" in text
    assert "V1_RELEASE_CANDIDATE_CUTOVER_RUNBOOK.md" in text
    assert "V1_RELEASE_CANDIDATE_CUTOVER_AUTHORIZATION_PACKET.md" in text
    assert "V1_FINAL_READINESS_AUDIT_TEMPLATE.md" in text
    assert "CHECKLIST_SATISFIED_FOR_FIRST_CONSUMER_HARNESS_TESTING_CUTOVER_AUTHORIZATION_REQUIRED" in text
    assert "CUTOVER_BLOCKED_AT_OPERATOR_AUTHORIZATION" in text
    assert "AWAITING_EXPLICIT_CUTOVER_OPERATOR_DECISION" in text
    assert "V1 final readiness reconciliation audit current state: passed for first-consumer harness testing" in text
    assert "PASS_CANDIDATE_READY_FOR_FIRST_CONSUMER_HARNESS_TESTING_CUTOVER_AUTHORIZATION_REQUIRED" in text
    assert "This register is not cutover authority" in text
    assert "does not authorize a V1.0.0 branch, tag, release cutover" in text
    assert "V1-G61 operator decision packet status audit current: satisfied, `Approve-V1-G61` recorded." in text
    assert "earlier current-gate/release-readiness set 153 tests before later readiness freshness supplements" in text
    assert "earlier current evidence 5350 tests before later readiness freshness supplements" in text
    assert "same-turn evidence 5359 tests after release/cutover freshness checks" in text
    assert "Same-turn consumer smoke refresh: passed, public Sparkbot 8 tests, accessible Sparkbot 8 tests, and Arc-Bot-shell 8 tests." in text
    assert "Arc-Bot-shell clean-checkpoint proof: recorded at clean pushed commit `99a4ba4955f13626c2176a2c44592000029a16c3`" in text
    assert "LIMA quickstart post-refresh validation: passed, 17 focused quickstart/handoff tests, 108 broader V1 harness/readiness tests, and 5360 full-suite tests." in text
    assert "LIMA latest final blocker/index readiness refresh: passed, 15 focused final blocker/index tests, 89 broader affected V1 readiness tests, and 5361 full-suite tests." in text
    assert "LIMA latest post-G61 request readiness-refresh: passed, 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, and 5362 full-suite tests." in text
    assert "LIMA latest quickstart artifact refresh: passed, 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5364 full-suite tests." in text
    assert "LIMA latest handoff freshness supplement: passed, 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5362/5364 full-suite tests." in text
    assert "Arc-Bot-shell local drift exclusion audit: historical compatibility evidence only; superseded by clean-checkpoint proof for release-gate evaluation" in text
    assert "Arc-Bot-shell clean-checkpoint proof is now the release-gate input" in text
    assert "clean pushed commit `99a4ba4955f13626c2176a2c44592000029a16c3`" in text
    assert "Public Sparkbot G56 branch pushed to `sparkpit-labs/Sparkbot`: yes." in text
    assert "Release-candidate branch or tag authority created by this register: no." in text
    assert "Release-candidate cutover authorized by this register: no." in text
    assert "Final readiness audit executed by this register: no." in text
    assert "Final readiness reconciliation consumed by this register: yes." in text
    assert "Arc-Bot-shell clean-checkpoint proof created by this register: no." in text
    assert "Record exactly one valid cutover operator choice" in text
    assert "Approve-V1-G61" in text
    assert "Additional V1-G61 implementation approval recorded by this register: no." in text
    assert "Additional V1-G61 runtime vendor SDK import execution proof implemented by this register: no." in text
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
