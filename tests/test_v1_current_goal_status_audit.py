"""Static checks for the V1 current goal status audit."""

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
    / "v1_current_goal_status_audit.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_current_goal_status_audit_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["audit_id"] == "v1_current_goal_status_audit"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["date"] == "2026-06-28"
    assert fixture["branch"] == "docs-v1-post-g60-readiness-and-next-lane-matrix"
    assert fixture["source_lima_commit_before_audit"] == (
        "a290d9cee297f93d1dad8229d615e10348542057"
    )
    assert fixture["audit_verdict"] == (
        "GOAL_NOT_COMPLETE_CUTOVER_OPERATOR_DECISION_REQUIRED"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_current_goal_status_audit_records_goal_incomplete() -> None:
    goal = _load_fixture()["goal_completion"]

    assert goal == {
        "goal_complete": False,
        "completion_claim_allowed": False,
        "primary_remaining_blocker": "record_exactly_one_valid_cutover_operator_choice",
        "current_recorded_valid_cutover_operator_choice_count": 0,
        "required_approval_choice_for_cutover": "Approve-V1-RC-Cutover",
    }


def test_v1_current_goal_status_audit_records_achieved_evidence() -> None:
    evidence = _load_fixture()["achieved_evidence"]

    assert evidence["candidate_only_api_status_current"] is True
    assert evidence["target_shells"] == [
        "Sparkbot_shell",
        "Sparkbot",
        "Arc-Bot-shell",
    ]
    assert evidence["public_sparkbot_publication_blocker_resolved"] is True
    assert evidence["provider_authority_chain_g57_through_g60_complete_candidate_only"] is True
    assert evidence["g61_operator_decision"] == "Approve-V1-G61"
    assert evidence["g61_bounded_local_import_proof_complete"] is True
    assert evidence["arc_bot_shell_clean_checkpoint_commit"] == (
        "99a4ba4955f13626c2176a2c44592000029a16c3"
    )
    assert evidence["release_candidate_acceptance_checklist_verdict"] == (
        "CHECKLIST_SATISFIED_FOR_FIRST_CONSUMER_HARNESS_TESTING_CUTOVER_AUTHORIZATION_REQUIRED"
    )
    assert evidence["final_readiness_reconciliation_verdict"] == (
        "PASS_CANDIDATE_READY_FOR_FIRST_CONSUMER_HARNESS_TESTING_CUTOVER_AUTHORIZATION_REQUIRED"
    )
    assert evidence["cutover_authorization_packet_status"] == (
        "AWAITING_EXPLICIT_CUTOVER_OPERATOR_DECISION"
    )
    assert evidence["cutover_authorization_packet_status_audit_verdict"] == (
        "PASS_CUTOVER_AUTHORIZATION_PACKET_AWAITING_EXPLICIT_OPERATOR_DECISION"
    )
    assert evidence["cutover_authorization_packet_valid_choice_count"] == 0
    assert evidence["latest_status_audit_focused_tests_passed"] == 21
    assert evidence["latest_status_audit_broader_tests_passed"] == 130
    assert evidence["latest_status_audit_compileall_passed"] is True
    assert evidence["latest_status_audit_full_lima_suite_tests_passed"] == 5433
    assert evidence["latest_status_audit_diff_hygiene_passed"] is True


def test_v1_current_goal_status_audit_records_unproven_requirements() -> None:
    requirements = _load_fixture()["requirements_not_yet_proven"]

    for key, value in requirements.items():
        assert value is False, key

    assert set(requirements) == {
        "exactly_one_valid_cutover_operator_choice_recorded",
        "approve_v1_rc_cutover_recorded",
        "cutover_runbook_executed_after_approval",
        "release_candidate_branch_created_under_runbook_controls",
        "v1_0_0_release_candidate_tag_created_under_runbook_controls",
        "separate_release_candidate_cutover_audit_exists",
        "final_v1_0_0_readiness_claim",
        "product_readiness",
        "production_readiness",
        "consumer_production_integration",
    }


def test_v1_current_goal_status_audit_preserves_boundaries() -> None:
    fixture = _load_fixture()

    for key, value in fixture["boundaries_preserved"].items():
        assert value is False, key

    assert fixture["next_required_action"] == "record_exactly_one_valid_cutover_operator_choice"


def test_v1_current_goal_status_audit_records_validation_refresh() -> None:
    validation = _load_fixture()["post_audit_validation_refresh"]

    assert validation["focused_current_goal_status_tests_passed"] == 21
    assert validation["broader_v1_readiness_status_tests_passed"] == 130
    assert validation["compileall_lima_passed"] is True
    assert validation["full_lima_suite_tests_passed"] == 5433
    assert validation["cutover_operator_choice_created_by_validation"] is False
    assert (
        validation[
            "release_branch_tag_cutover_or_readiness_authority_created_by_validation"
        ]
        is False
    )
    assert (
        validation[
            "runtime_provider_network_credential_connector_or_physical_world_behavior_added_by_validation"
        ]
        is False
    )


def test_v1_current_goal_status_audit_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["audit"]).read_text(encoding="utf-8")

    assert "# V1 Current Goal Status Audit" in text
    assert fixture["source_lima_commit_before_audit"] in text
    assert fixture["audit_verdict"] in text
    assert "The goal is not complete." in text
    assert "current recorded valid cutover operator choice count is `0`" in text
    assert "CANDIDATE_ONLY" in text
    assert "Sparkbot_shell" in text
    assert "Sparkbot" in text
    assert "Arc-Bot-shell" in text
    assert "99a4ba4955f13626c2176a2c44592000029a16c3" in text
    assert "CHECKLIST_SATISFIED_FOR_FIRST_CONSUMER_HARNESS_TESTING_CUTOVER_AUTHORIZATION_REQUIRED" in text
    assert "PASS_CANDIDATE_READY_FOR_FIRST_CONSUMER_HARNESS_TESTING_CUTOVER_AUTHORIZATION_REQUIRED" in text
    assert "AWAITING_EXPLICIT_CUTOVER_OPERATOR_DECISION" in text
    assert "PASS_CUTOVER_AUTHORIZATION_PACKET_AWAITING_EXPLICIT_OPERATOR_DECISION" in text
    assert "focused tests 21 passed" in text
    assert "broader V1 readiness/status tests 130 passed" in text
    assert "full LIMA suite 5433 passed" in text
    assert "Exactly one valid cutover operator choice recorded | not proven" in text
    assert "Release-candidate branch created under runbook controls | not proven and not authorized" in text
    assert "V1.0.0 completion claimed by this audit: no." in text
    assert "Post-Audit Validation Refresh" in text
    assert "passed, 21 tests" in text
    assert "passed, 130 tests" in text
    assert "passed, 5433 tests" in text
    assert "This validation refresh creates no cutover operator choice" in text
    assert "Machine action: `record_exactly_one_valid_cutover_operator_choice`" in text


def test_v1_current_goal_status_audit_has_no_sensitive_markers() -> None:
    fixture = _load_fixture()
    output = json.dumps(fixture, sort_keys=True)
    output += (REPO_ROOT / fixture["documents"]["audit"]).read_text(encoding="utf-8")

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
