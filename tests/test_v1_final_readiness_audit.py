"""Static checks for the V1 final readiness audit."""

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
    / "v1_final_readiness_audit.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_final_readiness_audit_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["audit_id"] == "v1_final_readiness_audit"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["date"] == "2026-06-28"
    assert fixture["branch"] == "docs-v1-post-g60-readiness-and-next-lane-matrix"
    assert fixture["lima_commit_under_audit"] == (
        "84189cc1d6d468da956818b6ffa5974e2e385389"
    )
    assert fixture["audit_verdict"] == (
        "BLOCKED_RELEASE_CANDIDATE_CHECKLIST_AND_CUTOVER_AUTHORITY_NOT_SATISFIED"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_final_readiness_audit_records_current_checkpoints() -> None:
    checkpoints = _load_fixture()["repository_checkpoints"]

    assert checkpoints["public_sparkbot"] == {
        "local_path": "C:\\Users\\limap\\Sparkbot-public",
        "branch": "v1-g56-runtime-authority-chain-audit",
        "commit": "ae5cc9c563ea2b0f08c91af03164a78b4b20e3e2",
        "clean": True,
    }
    assert checkpoints["accessible_sparkbot"] == {
        "local_path": "C:\\Users\\limap\\Sparkbot",
        "branch": "v1-g56-consumer-fake-executor-provider-sdk-network-egress-smoke",
        "commit": "ddaa4ccaacd328ddcc1f00a040c2c140abee428e",
        "clean": True,
    }
    assert checkpoints["sparkbot_shell"] == {
        "local_path": "C:\\Users\\limap\\Sparkbot_shell",
        "branch": "sparkbot-shell-work-settings-runtime-preview",
        "commit": "548b6d6aa6cde98b261e867c0c2db86ddbfa83dc",
        "clean": True,
    }
    assert checkpoints["arc_bot_shell"] == {
        "local_path": "C:\\Users\\limap\\Arc-Bot-shell",
        "branch": "v1-g56-consumer-fake-executor-provider-sdk-network-egress-smoke",
        "commit": "40fc474b0e09580a82f90518ebe341e2c98cd644",
        "clean": True,
        "recorded_clean_checkpoint_proof_commit": "99a4ba4955f13626c2176a2c44592000029a16c3",
        "current_head_descends_from_recorded_clean_checkpoint": True,
    }


def test_v1_final_readiness_audit_records_validation_results() -> None:
    validation = _load_fixture()["validation_results"]

    assert validation["public_sparkbot_g56_smoke"] == {"passed": True, "tests_passed": 8}
    assert validation["accessible_sparkbot_g56_smoke"] == {"passed": True, "tests_passed": 8}
    assert validation["arc_bot_shell_g56_smoke"] == {"passed": True, "tests_passed": 8}
    assert validation["sparkbot_shell_status"] == {
        "passed": True,
        "clean_tracking_branch": True,
    }
    assert validation["lima_compileall"] == {
        "command": "python -m compileall lima",
        "passed": True,
    }
    assert validation["lima_full_suite"] == {
        "command": "python -m pytest -q tests -p no:cacheprovider",
        "passed": True,
        "tests_passed": 5391,
    }

    for key, value in validation.items():
        if key.endswith("diff_check") or key.endswith("diff_check_before_audit_edits"):
            assert value["passed"] is True, key


def test_v1_final_readiness_audit_blocks_cutover_authority() -> None:
    fixture = _load_fixture()
    criteria = fixture["criteria_results"]

    assert criteria["g61_decision_approve_v1_g61_recorded"] is True
    assert criteria["g61_bounded_proof_and_closeout_complete"] is True
    assert criteria["consumer_smokes_pass"] is True
    assert criteria["arc_clean_checkpoint_usable"] is True
    assert criteria["lima_full_suite_passes"] is True
    assert criteria["release_candidate_acceptance_checklist_satisfied"] is True
    assert criteria["release_candidate_cutover_authorized"] is False
    assert criteria["explicit_branch_tag_cutover_operator_authorization_recorded"] is False
    assert fixture["next_required_actions"] == [
        "preserve_reconciled_release_candidate_acceptance_checklist_as_first_consumer_harness_testing_evidence_only",
        "keep_runbook_blocked_at_explicit_cutover_authorization",
        "record_exactly_one_valid_cutover_operator_choice_before_branch_tag_cutover_or_readiness_claim",
        "rerun_lima_focused_full_validation_and_diff_hygiene_after_further_readiness_artifact_change",
    ]


def test_v1_final_readiness_audit_preserves_false_boundaries() -> None:
    boundaries = _load_fixture()["boundaries_preserved"]

    assert boundaries["final_readiness_audit_executed_by_artifact"] is True
    for key, value in boundaries.items():
        if key != "final_readiness_audit_executed_by_artifact":
            assert value is False, key


def test_v1_final_readiness_audit_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["final_readiness_audit"]).read_text(
        encoding="utf-8"
    )

    assert "# V1 Final Readiness Audit" in text
    assert fixture["lima_commit_under_audit"] in text
    assert "BLOCKED_RELEASE_CANDIDATE_CHECKLIST_AND_CUTOVER_AUTHORITY_NOT_SATISFIED" in text
    assert "does not complete V1.0.0" in text
    assert "Sparkbot-public, accessible Sparkbot, and Arc-Bot-shell smoke tests pass" in text
    assert "Sparkbot_shell is clean" in text
    assert "current clean HEAD is a descendant of the recorded clean-checkpoint proof commit" in text
    assert "CHECKLIST_SATISFIED_FOR_FIRST_CONSUMER_HARNESS_TESTING_CUTOVER_AUTHORIZATION_REQUIRED" in text
    assert "CUTOVER_BLOCKED_AT_OPERATOR_AUTHORIZATION" in text
    assert "no explicit operator authorization for branch or tag creation is recorded" in text
    assert "40fc474b0e09580a82f90518ebe341e2c98cd644" in text
    assert "99a4ba4955f13626c2176a2c44592000029a16c3" in text
    assert "passed, 5391 tests" in text
    assert "Release-candidate acceptance checklist satisfied | pass with reconciliation" in text
    assert "Release-candidate cutover authorized | fail" in text
    assert "Final readiness pass claimed by this artifact: no." in text
    assert "Release-candidate checklist passed by this artifact: no." in text
    assert "Branch or tag action authorized by this artifact: no." in text
    assert "V1.0 completion, product readiness, or production readiness claimed: no." in text


def test_v1_final_readiness_audit_has_no_sensitive_markers() -> None:
    fixture = _load_fixture()
    output = json.dumps(fixture, sort_keys=True)
    output += (REPO_ROOT / fixture["documents"]["final_readiness_audit"]).read_text(
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
