"""Static checks for the V1 final readiness reconciliation audit."""

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
    / "v1_final_readiness_reconciliation_audit.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_final_readiness_reconciliation_audit_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["audit_id"] == "v1_final_readiness_reconciliation_audit"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["date"] == "2026-06-28"
    assert fixture["branch"] == "docs-v1-post-g60-readiness-and-next-lane-matrix"
    assert fixture["source_lima_commit_before_reconciliation"] == (
        "a829c6b9a3e34d0923a35810a84fc1e287df6604"
    )
    assert fixture["audit_verdict"] == (
        "PASS_CANDIDATE_READY_FOR_FIRST_CONSUMER_HARNESS_TESTING_CUTOVER_AUTHORIZATION_REQUIRED"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_final_readiness_reconciliation_audit_records_pass_scope() -> None:
    results = _load_fixture()["reconciliation_results"]

    assert results["g61_operator_decision_approve_recorded"] is True
    assert results["bounded_g61_proof_closed"] is True
    assert results["public_sparkbot_smoke_tests_passed"] == 8
    assert results["accessible_sparkbot_smoke_tests_passed"] == 8
    assert results["arc_bot_shell_smoke_tests_passed"] == 8
    assert results["arc_bot_shell_clean_checkpoint_commit"] == (
        "99a4ba4955f13626c2176a2c44592000029a16c3"
    )
    assert results["arc_bot_shell_current_head_descends_from_clean_checkpoint"] is True
    assert results["sparkbot_shell_clean_checkpoint_recorded"] is True
    assert results["lima_compileall_passed"] is True
    assert results["lima_full_suite_tests_passed"] == 5391
    assert results["circular_final_readiness_checklist_blocker_reconciled"] is True
    assert results["ready_for_first_consumer_harness_testing"] is True
    assert results["release_candidate_cutover_authorized"] is False
    assert results["explicit_branch_tag_cutover_operator_authorization_recorded"] is False


def test_v1_final_readiness_reconciliation_audit_preserves_boundaries() -> None:
    boundaries = _load_fixture()["boundaries_preserved"]

    assert (
        boundaries[
            "final_readiness_reconciliation_pass_for_first_consumer_harness_testing_recorded_by_artifact"
        ]
        is True
    )

    for key, value in boundaries.items():
        if key == (
            "final_readiness_reconciliation_pass_for_first_consumer_harness_testing_recorded_by_artifact"
        ):
            continue
        assert value is False, key


def test_v1_final_readiness_reconciliation_audit_records_current_validation() -> None:
    validation = _load_fixture()["post_reconciliation_validation"]

    assert validation["focused_reconciliation_and_status_tests_passed"] == 13
    assert validation["adjacent_readiness_tests_passed"] == 44
    assert validation["lima_compileall_passed"] is True
    assert validation["full_lima_suite_tests_passed"] == 5405
    assert validation["release_or_cutover_authority_created_by_validation"] is False


def test_v1_final_readiness_reconciliation_audit_next_actions_are_gated() -> None:
    assert _load_fixture()["next_required_actions"] == [
        "refresh_release_candidate_acceptance_checklist_cutover_runbook_and_final_blocker_register_against_reconciliation_verdict",
        "rerun_lima_focused_full_compileall_and_diff_hygiene_after_reconciliation_artifact_commit",
        "require_explicit_operator_authorization_before_branch_tag_cutover_v1_readiness_product_or_production_claim",
    ]


def test_v1_final_readiness_reconciliation_audit_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["reconciliation_audit"]).read_text(
        encoding="utf-8"
    )

    assert "# V1 Final Readiness Reconciliation Audit" in text
    assert fixture["source_lima_commit_before_reconciliation"] in text
    assert fixture["audit_verdict"] in text
    assert "reconciles the circular state" in text
    assert "ready for first-consumer harness testing" in text
    assert "release-candidate branch, release tag, cutover" in text
    assert "explicit operator authorization" in text
    assert "99a4ba4955f13626c2176a2c44592000029a16c3" in text
    assert "passed with 5391 tests" in text
    assert "Post-Reconciliation Validation Executed" in text
    assert "passed, 13 tests" in text
    assert "passed, 44 tests" in text
    assert "passed, 5405 tests" in text
    assert "Circular final-readiness/checklist blocker | reconciled" in text
    assert "Cutover authorization | blocked" in text
    assert "Release-candidate branch authorized by this artifact: no." in text
    assert "Release-candidate tag authorized by this artifact: no." in text
    assert "Release cutover authorized by this artifact: no." in text
    assert "V1.0.0 completion claimed by this artifact: no." in text
    assert "Product readiness claimed by this artifact: no." in text
    assert "Production readiness claimed by this artifact: no." in text


def test_v1_final_readiness_reconciliation_audit_has_no_sensitive_markers() -> None:
    fixture = _load_fixture()
    output = json.dumps(fixture, sort_keys=True)
    output += (REPO_ROOT / fixture["documents"]["reconciliation_audit"]).read_text(
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
