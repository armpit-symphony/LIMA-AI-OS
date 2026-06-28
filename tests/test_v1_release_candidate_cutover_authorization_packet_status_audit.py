"""Static checks for the V1 cutover authorization packet status audit."""

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
    / "v1_release_candidate_cutover_authorization_packet_status_audit.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_cutover_authorization_packet_status_audit_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert (
        fixture["audit_id"]
        == "v1_release_candidate_cutover_authorization_packet_status_audit"
    )
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["date"] == "2026-06-28"
    assert fixture["branch"] == "docs-v1-post-g60-readiness-and-next-lane-matrix"
    assert fixture["source_lima_commit_before_audit"] == (
        "5fef77d748a68de46e003a7e464564b4450d352d"
    )
    assert fixture["audit_verdict"] == (
        "PASS_CUTOVER_AUTHORIZATION_PACKET_AWAITING_EXPLICIT_OPERATOR_DECISION"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_cutover_authorization_packet_status_audit_records_zero_decisions() -> None:
    status = _load_fixture()["packet_status_verified"]

    assert status["packet_status"] == "AWAITING_EXPLICIT_CUTOVER_OPERATOR_DECISION"
    assert status["valid_operator_choices"] == [
        "Approve-V1-RC-Cutover",
        "Revise-V1-RC-Cutover",
        "Pause",
    ]
    assert status["current_recorded_choice"] is None
    assert status["recorded_valid_cutover_operator_choice_count"] == 0
    assert status["next_required_machine_action"] == (
        "record_exactly_one_valid_cutover_operator_choice"
    )


def test_v1_cutover_authorization_packet_status_audit_records_ready_evidence() -> None:
    evidence = _load_fixture()["evidence_ready_but_not_sufficient_for_cutover"]

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
    assert evidence["focused_packet_current_gate_tests_passed"] == 37
    assert evidence["broader_v1_readiness_status_tests_passed"] == 102
    assert evidence["compileall_lima_passed"] is True
    assert evidence["full_lima_suite_tests_passed"] == 5412
    assert evidence["diff_hygiene_passed"] is True


def test_v1_cutover_authorization_packet_status_audit_creates_no_authority() -> None:
    fixture = _load_fixture()

    for key, value in fixture["authorization_result"].items():
        if key == "valid_cutover_operator_choice_count_after_audit":
            assert value == 0
            continue
        assert value is False, key

    for key, value in fixture["boundaries_preserved"].items():
        assert value is False, key

    assert fixture["next_required_action"] == "record_exactly_one_valid_cutover_operator_choice"


def test_v1_cutover_authorization_packet_status_audit_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["audit"]).read_text(encoding="utf-8")

    assert "# V1 Release Candidate Cutover Authorization Packet Status Audit" in text
    assert fixture["source_lima_commit_before_audit"] in text
    assert fixture["audit_verdict"] in text
    assert "AWAITING_EXPLICIT_CUTOVER_OPERATOR_DECISION" in text
    assert "Current recorded choice | none" in text
    assert "Recorded valid cutover operator choice count | `0`" in text
    assert "Approve-V1-RC-Cutover" in text
    assert "Revise-V1-RC-Cutover" in text
    assert "Pause" in text
    assert "CHECKLIST_SATISFIED_FOR_FIRST_CONSUMER_HARNESS_TESTING_CUTOVER_AUTHORIZATION_REQUIRED" in text
    assert "PASS_CANDIDATE_READY_FOR_FIRST_CONSUMER_HARNESS_TESTING_CUTOVER_AUTHORIZATION_REQUIRED" in text
    assert "CUTOVER_BLOCKED_AT_OPERATOR_AUTHORIZATION" in text
    assert "STOPPED_AT_CUTOVER_AUTHORITY" in text
    assert "99a4ba4955f13626c2176a2c44592000029a16c3" in text
    assert "focused packet/current-gate tests 37 passed" in text
    assert "full LIMA suite 5412 passed" in text
    assert "Release-candidate branch creation allowed now: no." in text
    assert "Release-candidate tag creation allowed now: no." in text
    assert "Release cutover allowed now: no." in text
    assert "Product readiness claimed by this audit: no." in text
    assert "Production readiness claimed by this audit: no." in text
    assert fixture["next_required_action"] in text


def test_v1_cutover_authorization_packet_status_audit_has_no_sensitive_markers() -> None:
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
