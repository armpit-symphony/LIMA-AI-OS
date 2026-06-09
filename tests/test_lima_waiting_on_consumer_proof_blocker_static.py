from __future__ import annotations

import json
import pathlib
from typing import Any, Mapping


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "waiting_on_consumer_proof_blockers"
    / "waiting_on_consumer_proof_blockers.json"
)


def _load_fixture() -> Mapping[str, Any]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _text(path_key: str) -> str:
    fixture = _load_fixture()
    return (REPO_ROOT / fixture[path_key]).read_text(encoding="utf-8")


def _blocker_audit_text() -> str:
    return _text("blocker_audit_path")


def _static_tests_audit_text() -> str:
    return _text("static_tests_audit_path")


def test_waiting_blocker_fixture_is_static_metadata_only() -> None:
    fixture = _load_fixture()

    assert fixture["schema_version"] == "0.1"
    assert fixture["fixture_scope"] == "static_waiting_on_consumer_proof_blocker_only"
    assert fixture["audit_status"] == "PASS"
    assert fixture["base_commit"] == "71ae071a7ab51395b3d6aa139a25a1a581ab39ce"


def test_waiting_blocker_source_paths_exist() -> None:
    fixture = _load_fixture()

    for path_key in (
        "blocker_audit_path",
        "current_state_audit_path",
        "current_state_static_tests_audit_path",
        "operator_delivery_request_path",
        "dry_run_delivery_brief_path",
        "static_tests_audit_path",
    ):
        assert (REPO_ROOT / fixture[path_key]).exists(), path_key


def test_blocker_audit_records_waiting_state_without_readiness_claim() -> None:
    audit = _blocker_audit_text()

    assert "PASS for LIMA-local blocker audit." in audit
    assert "The current blocker is missing operator/consumer evidence" in audit
    assert "This is not the same as Sparkbot or Arc Bot product readiness." in audit
    assert "Ready to wait for operator confirmation or consumer proof packets." in audit


def test_current_evidence_state_remains_missing() -> None:
    fixture = _load_fixture()
    audit = _blocker_audit_text()

    for expected_phrase in fixture["current_evidence_state"].values():
        assert expected_phrase in audit


def test_missing_external_inputs_are_operator_or_consumer_owned() -> None:
    fixture = _load_fixture()
    audit = _blocker_audit_text()

    for missing_input in fixture["missing_external_inputs"]:
        assert missing_input in audit

    assert "must come from the operator or consumer repo teams" in audit


def test_no_confirmation_or_proof_audit_branch_can_run_without_input() -> None:
    fixture = _load_fixture()
    audit = _blocker_audit_text()

    confirmation_branch = fixture["must_not_run_branches"]["delivery_confirmation_status"]
    proof_results_branch = fixture["must_not_run_branches"]["consumer_owned_proof_results"]

    assert confirmation_branch in audit
    assert "unless the operator explicitly confirms manual" in audit
    assert proof_results_branch in audit
    assert "unless a Sparkbot or Arc Bot proof packet is supplied" in audit


def test_allowed_next_actions_remain_input_dependent() -> None:
    fixture = _load_fixture()
    audit = _blocker_audit_text()

    for action in fixture["allowed_next_actions"]:
        assert action in audit

    assert "Allowed next actions are input-dependent:" in audit


def test_not_ready_claims_remain_negative_boundaries() -> None:
    fixture = _load_fixture()
    audit = _blocker_audit_text()

    for claim in fixture["not_ready_claims"]:
        assert claim in audit

    assert "Without those inputs, LIMA must not claim:" in audit


def test_forbidden_surfaces_remain_documented_as_blocked() -> None:
    fixture = _load_fixture()
    audit = _blocker_audit_text()

    for surface in fixture["forbidden_surfaces"]:
        assert surface in audit

    assert "This audit does not authorize:" in audit


def test_handoff_artifacts_already_exist_and_are_not_recreated() -> None:
    delivery_brief = _text("dry_run_delivery_brief_path")
    operator_request = _text("operator_delivery_request_path")

    assert "This is the current operator-facing delivery brief for Sparkbot and Arc Bot repo teams." in delivery_brief
    assert "Manually send this request to the Sparkbot repo team:" in operator_request
    assert "Manually send this request to the Arc Bot / LIMA Office repo team:" in operator_request


def test_static_tests_allowed_files_are_exact() -> None:
    fixture = _load_fixture()
    static_audit = _static_tests_audit_text()

    for path in fixture["allowed_files"]:
        assert f"`{path}`" in static_audit

    assert "No `lima/`, package metadata, public export, consumer repo, or runtime behavior changes are made." in static_audit


def test_static_tests_recommend_independent_audit() -> None:
    fixture = _load_fixture()
    static_audit = _static_tests_audit_text()

    assert fixture["recommended_next_branch"] == "audit-lima-waiting-on-consumer-proof-blocker-static-tests"
    assert f"`{fixture['recommended_next_branch']}`" in static_audit
