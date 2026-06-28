"""Static checks for the V1 release-candidate cutover authorization packet."""

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
    / "v1_release_candidate_cutover_authorization_packet.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_release_candidate_cutover_authorization_packet_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["packet_id"] == "v1_release_candidate_cutover_authorization_packet"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["date"] == "2026-06-28"
    assert fixture["branch"] == "docs-v1-post-g60-readiness-and-next-lane-matrix"
    assert fixture["source_lima_commit_before_packet"] == "ecd7ca3"
    assert fixture["packet_status"] == "AWAITING_EXPLICIT_CUTOVER_OPERATOR_DECISION"

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_release_candidate_cutover_authorization_packet_records_exact_choices() -> None:
    fixture = _load_fixture()

    assert fixture["valid_operator_choices"] == [
        "Approve-V1-RC-Cutover",
        "Revise-V1-RC-Cutover",
        "Pause",
    ]
    assert fixture["current_recorded_choice"] is None
    assert fixture["next_required_action"] == "record_exactly_one_valid_cutover_operator_choice"


def test_v1_release_candidate_cutover_authorization_packet_records_ready_evidence() -> None:
    evidence = _load_fixture()["evidence_ready_for_decision"]

    assert evidence["g61_operator_decision"] == "Approve-V1-G61"
    assert evidence["bounded_g61_proof_closeout_complete"] is True
    assert evidence["release_candidate_acceptance_checklist_verdict"] == (
        "CHECKLIST_SATISFIED_FOR_FIRST_CONSUMER_HARNESS_TESTING_CUTOVER_AUTHORIZATION_REQUIRED"
    )
    assert evidence["final_readiness_reconciliation_audit_verdict"] == (
        "PASS_CANDIDATE_READY_FOR_FIRST_CONSUMER_HARNESS_TESTING_CUTOVER_AUTHORIZATION_REQUIRED"
    )
    assert evidence["cutover_runbook_verdict"] == "CUTOVER_BLOCKED_AT_OPERATOR_AUTHORIZATION"
    assert evidence["final_blocker_register_verdict"] == "STOPPED_AT_CUTOVER_AUTHORITY"
    assert evidence["arc_bot_shell_clean_checkpoint_commit"] == (
        "99a4ba4955f13626c2176a2c44592000029a16c3"
    )
    assert evidence["focused_v1_readiness_status_tests_passed_before_packet"] == 96
    assert evidence["compileall_lima_passed_before_packet"] is True
    assert evidence["full_lima_suite_tests_passed_before_packet"] == 5405


def test_v1_release_candidate_cutover_authorization_packet_records_post_packet_validation() -> None:
    validation = _load_fixture()["post_packet_validation"]

    assert validation["focused_cutover_packet_current_gate_tests_passed"] == 37
    assert validation["broader_v1_readiness_status_tests_passed"] == 102
    assert validation["compileall_lima_passed"] is True
    assert validation["full_lima_suite_tests_passed"] == 5412
    assert validation["diff_check_passed"] is True
    assert validation["release_or_cutover_authority_created_by_validation"] is False


def test_v1_release_candidate_cutover_authorization_packet_preserves_boundaries() -> None:
    fixture = _load_fixture()
    boundaries = fixture["boundaries_preserved"]

    for key, value in boundaries.items():
        assert value is False, key

    approval_effect = fixture["approval_effect_if_recorded_later"]
    assert approval_effect["authorizes_runbook_to_create_release_candidate_branch_after_validation"] is True
    assert approval_effect["authorizes_runbook_to_create_release_candidate_tag_after_validation"] is True
    assert approval_effect["requires_separate_cutover_audit"] is True
    assert approval_effect["authorizes_product_readiness"] is False
    assert approval_effect["authorizes_production_readiness"] is False


def test_v1_release_candidate_cutover_authorization_packet_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["packet"]).read_text(encoding="utf-8")

    assert "# V1 Release Candidate Cutover Authorization Packet" in text
    assert fixture["source_lima_commit_before_packet"] in text
    assert fixture["packet_status"] in text
    assert "No valid cutover operator decision is recorded yet." in text
    assert "Approve-V1-RC-Cutover" in text
    assert "Revise-V1-RC-Cutover" in text
    assert "Pause" in text
    assert "Current recorded choice: none." in text
    assert "CHECKLIST_SATISFIED_FOR_FIRST_CONSUMER_HARNESS_TESTING_CUTOVER_AUTHORIZATION_REQUIRED" in text
    assert "PASS_CANDIDATE_READY_FOR_FIRST_CONSUMER_HARNESS_TESTING_CUTOVER_AUTHORIZATION_REQUIRED" in text
    assert "CUTOVER_BLOCKED_AT_OPERATOR_AUTHORIZATION" in text
    assert "STOPPED_AT_CUTOVER_AUTHORITY" in text
    assert "99a4ba4955f13626c2176a2c44592000029a16c3" in text
    assert "Post-Packet Validation Executed" in text
    assert "passed, 37 tests" in text
    assert "passed, 102 tests" in text
    assert "passed, 5412 tests" in text
    assert "Cutover operator decision recorded by this packet: no." in text
    assert "Release-candidate branch authorized by this packet without a later recorded valid choice: no." in text
    assert "Product readiness claimed by this packet: no." in text
    assert "Production readiness claimed by this packet: no." in text


def test_v1_release_candidate_cutover_authorization_packet_has_no_sensitive_markers() -> None:
    fixture = _load_fixture()
    output = json.dumps(fixture, sort_keys=True)
    output += (REPO_ROOT / fixture["documents"]["packet"]).read_text(encoding="utf-8")

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
