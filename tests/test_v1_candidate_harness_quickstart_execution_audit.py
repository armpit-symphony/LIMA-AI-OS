"""Static checks for the V1 candidate harness quickstart execution audit."""

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
    / "v1_candidate_harness_quickstart_execution_audit.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_candidate_harness_quickstart_execution_audit_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["audit_id"] == "v1_candidate_harness_quickstart_execution_audit"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["date"] == "2026-06-21"
    assert fixture["branch"] == "docs-v1-post-g60-readiness-and-next-lane-matrix"
    assert fixture["source_lima_commit_before_audit"] == (
        "37626bf236bf96c8a57a3ca351668e90eeb0e651"
    )
    assert fixture["audit_verdict"] == (
        "PASS_LOCAL_CANDIDATE_HARNESS_QUICKSTART_WITH_G61_OPERATOR_BLOCKER"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_candidate_harness_quickstart_execution_audit_records_consumer_results() -> None:
    commands = _load_fixture()["executed_consumer_commands"]

    assert set(commands) == {
        "public_sparkbot",
        "accessible_sparkbot",
        "arc_bot_shell",
    }
    assert commands["public_sparkbot"]["local_path"] == "C:\\Users\\limap\\Sparkbot-public"
    assert commands["accessible_sparkbot"]["local_path"] == "C:\\Users\\limap\\Sparkbot"
    assert commands["arc_bot_shell"]["local_path"] == "C:\\Users\\limap\\Arc-Bot-shell"
    assert "test_sparkbot_lima_v1_g56_fake_executor" in commands["public_sparkbot"][
        "pytest_command"
    ]
    assert "test_sparkbot_lima_v1_g56_fake_executor" in commands["accessible_sparkbot"][
        "pytest_command"
    ]
    assert "test_arc_bot_shell_lima_v1_g56_fake_executor" in commands["arc_bot_shell"][
        "pytest_command"
    ]

    for name, result in commands.items():
        assert result["pytest_passed"] is True, name
        assert result["tests_passed"] == 8, name
        assert result["diff_check_command"] == "git diff --check", name
        assert result["diff_check_passed"] is True, name


def test_v1_candidate_harness_quickstart_execution_audit_records_latest_rerun_caveat() -> None:
    rerun = _load_fixture()["latest_local_rerun"]

    assert rerun["date"] == "2026-06-21"
    assert rerun["public_sparkbot_worktree_clean_before_rerun"] is True
    assert rerun["accessible_sparkbot_worktree_clean_before_rerun"] is True
    assert rerun["arc_bot_shell_worktree_clean_before_rerun"] is False
    assert "not clean-checkpoint evidence" in rerun["arc_bot_shell_dirty_worktree_caveat"]
    assert rerun["public_sparkbot_smoke_tests_passed"] == 8
    assert rerun["accessible_sparkbot_smoke_tests_passed"] == 8
    assert rerun["arc_bot_shell_smoke_tests_passed"] == 8
    assert rerun["arc_bot_shell_diff_check_passed_with_lf_crlf_warnings_only"] is True
    assert rerun["lima_focused_companion_handoff_current_gate_tests_passed"] == 73


def test_v1_candidate_harness_quickstart_execution_audit_records_same_turn_consumer_refresh() -> None:
    refresh = _load_fixture()["same_turn_consumer_smoke_refresh"]

    assert refresh["date"] == "2026-06-21"
    assert refresh["sandboxed_pytest_attempt_failed_before_test_execution"] is True
    assert refresh["approved_pytest_invocation"] == "python -B -m pytest"
    assert refresh["bytecode_artifacts_avoided"] is True
    assert refresh["public_sparkbot_smoke_tests_passed"] == 8
    assert refresh["public_sparkbot_diff_check_passed"] is True
    assert refresh["public_sparkbot_worktree_clean_after_refresh"] is True
    assert refresh["accessible_sparkbot_smoke_tests_passed"] == 8
    assert refresh["accessible_sparkbot_diff_check_passed"] is True
    assert refresh["accessible_sparkbot_worktree_clean_after_refresh"] is True
    assert refresh["arc_bot_shell_smoke_tests_passed"] == 8
    assert refresh["arc_bot_shell_diff_check_passed_with_lf_crlf_warnings_only"] is True
    assert refresh["arc_bot_shell_worktree_after_refresh"] == (
        "unchanged_pre_existing_unrelated_local_drift"
    )
    assert refresh["arc_bot_shell_clean_checkpoint_evidence_claimed"] is False
    assert refresh["release_candidate_or_g61_authority_created"] is False


def test_v1_candidate_harness_quickstart_execution_audit_accepts_only_bounded_evidence() -> None:
    assert _load_fixture()["evidence_accepted"] == [
        "public_sparkbot_quickstart_smoke_passed",
        "accessible_sparkbot_quickstart_smoke_passed",
        "arc_bot_shell_quickstart_smoke_passed",
        "same_turn_consumer_smoke_refresh_public_accessible_arc_8_each",
        "consumer_diff_hygiene_passed",
        "lima_focused_quickstart_execution_readiness_tests_passed",
        "lima_compile_and_full_suite_passed",
        "post_refresh_lima_validation_17_108_5360_passed",
        "latest_quickstart_artifact_refresh_7_64_133_5364_passed_without_consumer_rerun",
        "local_fake_executor_sanitized_fixture_smoke_only",
        "g61_operator_decision_packet_status_audit_confirms_awaiting_choice",
        "current_gate_consistency_audit_rejects_stale_release_candidate_claims",
        "future_final_readiness_audit_not_executed_or_passed",
        "arc_bot_shell_smoke_not_clean_checkpoint_while_local_drift_excluded",
        "g61_operator_decision_blocker_preserved",
    ]


def test_v1_candidate_harness_quickstart_execution_audit_records_lima_validation() -> None:
    validation = _load_fixture()["lima_side_validation"]

    assert validation["focused_candidate_harness_quickstart_execution_readiness_set"] == {
        "passed": True,
        "tests_passed": 73,
    }
    assert validation["compileall_lima"] == {
        "command": "python -m compileall lima",
        "passed": True,
    }
    assert validation["full_lima_suite"] == {
        "command": "python -m pytest -q tests -p no:cacheprovider",
        "passed": True,
        "tests_passed": 5359,
    }

    post_refresh = _load_fixture()["post_refresh_lima_validation"]
    assert post_refresh["date"] == "2026-06-21"
    assert post_refresh["focused_quickstart_handoff_execution_set"] == {
        "passed": True,
        "tests_passed": 17,
    }
    assert post_refresh["broader_v1_harness_readiness_set"] == {
        "passed": True,
        "tests_passed": 108,
    }
    assert post_refresh["compileall_lima"] == {
        "command": "python -m compileall lima",
        "passed": True,
    }
    assert post_refresh["full_lima_suite"] == {
        "command": "python -m pytest -q tests -p no:cacheprovider",
        "passed": True,
        "tests_passed": 5360,
    }

    latest_refresh = _load_fixture()["latest_quickstart_artifact_refresh_validation"]
    assert latest_refresh["date"] == "2026-06-21"
    assert latest_refresh["consumer_repositories_rerun"] is False
    assert latest_refresh["focused_candidate_harness_quickstart_set"] == {
        "passed": True,
        "tests_passed": 7,
    }
    assert latest_refresh["adjacent_harness_readiness_set"] == {
        "passed": True,
        "tests_passed": 64,
    }
    assert latest_refresh["broader_g61_readiness_regression_set"] == {
        "passed": True,
        "tests_passed": 133,
    }
    assert latest_refresh["compileall_lima"] == {
        "command": "python -m compileall lima",
        "passed": True,
    }
    assert latest_refresh["full_lima_suite"] == {
        "command": "python -m pytest -q tests -p no:cacheprovider",
        "passed": True,
        "tests_passed": 5364,
    }
    assert (
        latest_refresh[
            "release_candidate_final_readiness_arc_clean_checkpoint_production_or_g61_authority_created"
        ]
        is False
    )


def test_v1_candidate_harness_quickstart_execution_audit_preserves_false_boundaries() -> None:
    for key, value in _load_fixture()["required_false_boundaries"].items():
        assert value is False, key


def test_v1_candidate_harness_quickstart_execution_audit_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["execution_audit"]).read_text(
        encoding="utf-8"
    )

    assert "# V1 Candidate Harness Quickstart Execution Audit" in text
    assert fixture["source_lima_commit_before_audit"] in text
    assert "PASS_LOCAL_CANDIDATE_HARNESS_QUICKSTART_WITH_G61_OPERATOR_BLOCKER" in text
    assert "## Latest Local Rerun" in text
    assert "Arc-Bot-shell was not clean before rerun" in text
    assert "not clean-checkpoint evidence" in text
    assert "LIMA focused companion handoff/current-gate pytest rerun: 73 passed." in text
    assert "## Same-Turn Consumer Smoke Refresh" in text
    assert "Same-turn refresh date: 2026-06-21" in text
    assert "failed before test execution with a Windows runner error" in text
    assert "`python -B -m pytest`" in text
    assert "Public Sparkbot same-turn smoke refresh: 8 passed." in text
    assert "Accessible Sparkbot same-turn smoke refresh: 8 passed." in text
    assert "Arc-Bot-shell same-turn smoke refresh: 8 passed." in text
    assert "Public Sparkbot worktree after refresh: clean." in text
    assert "Accessible Sparkbot worktree after refresh: clean." in text
    assert "Arc-Bot-shell worktree after refresh: unchanged pre-existing unrelated local drift." in text
    assert (
        "Same-turn consumer smoke refresh confirms public Sparkbot, accessible "
        "Sparkbot, and Arc-Bot-shell still pass the current smoke path with 8 "
        "tests each."
    ) in text
    assert "Public Sparkbot target checkout" in text
    assert "Accessible Sparkbot checkpoint" in text
    assert "Arc-Bot-shell" in text
    assert "8 passed" in text
    assert "focused candidate harness quickstart execution/readiness pytest set" in text
    assert "73 passed" in text
    assert "5359 passed" in text
    assert "## Post-Refresh LIMA Validation" in text
    assert "After adding the same-turn consumer smoke refresh assertions" in text
    assert "focused quickstart/handoff execution pytest set | 17 passed" in text
    assert "broader V1 harness/readiness pytest set | 108 passed" in text
    assert "`python -m pytest -q tests -p no:cacheprovider` | 5360 passed" in text
    assert "## Latest Quickstart Artifact Refresh" in text
    assert "focused candidate harness quickstart pytest set | 7 passed" in text
    assert "adjacent harness/readiness pytest set | 64 passed" in text
    assert "broader G61/readiness regression pytest set | 133 passed" in text
    assert "`python -m pytest -q tests -p no:cacheprovider` | 5364 passed" in text
    assert "This refresh does not rerun consumer repositories" in text
    assert (
        "does not create release-candidate, final-readiness, Arc-Bot-shell "
        "clean-checkpoint, production, or G61 implementation authority"
    ) in text
    assert (
        "Post-refresh LIMA validation passes after adding the same-turn "
        "consumer smoke refresh assertions, including 17 focused "
        "quickstart/handoff tests, 108 broader V1 harness/readiness tests, "
        "compileall, and the full suite with 5360 tests."
    ) in text
    assert (
        "Latest quickstart artifact refresh validation passes after adding "
        "current evidence-to-preserve assertions, including 7 focused "
        "quickstart tests, 64 adjacent harness/readiness tests, 133 broader "
        "G61/readiness tests, compileall, and the full suite with 5364 tests."
    ) in text
    assert "V1_CURRENT_GATE_CONSISTENCY_AUDIT.md" in text
    assert "V1_RELEASE_CANDIDATE_CUTOVER_RUNBOOK.md" in text
    assert "V1_FINAL_READINESS_AUDIT_TEMPLATE.md" in text
    assert "V1_G61_OPERATOR_DECISION_PACKET_STATUS_AUDIT.md" in text
    assert "status audit confirms the packet is still awaiting exactly one valid operator choice" in text
    assert "stale blocker or release-candidate claims are rejected" in text
    assert "future final readiness audit was not executed or passed" in text
    assert "Arc-Bot-shell smoke remains compatibility evidence only" in text
    assert "Consumer diff hygiene commands pass in all three local consumer workspaces" in text
    assert "unrelated local changes were present before rerun" in text
    assert "V1-G61 implementation approval recorded by this audit: false." in text
    assert "Future final readiness audit executed by this audit: false." in text
    assert "Arc-Bot-shell clean-checkpoint evidence claimed by this audit: false." in text
    assert "Consumer repositories changed by this audit: false." in text
    assert "V1.0 completion, product-readiness, or production-readiness claimed: false." in text
    assert "Do not implement G61, create release-candidate artifacts, or claim V1/product/production readiness from this audit." in text


def test_v1_candidate_harness_quickstart_execution_audit_has_no_sensitive_markers() -> None:
    fixture = _load_fixture()
    output = json.dumps(fixture, sort_keys=True)
    output += (REPO_ROOT / fixture["documents"]["execution_audit"]).read_text(
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
