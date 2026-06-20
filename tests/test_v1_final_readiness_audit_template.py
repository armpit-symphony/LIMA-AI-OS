"""Static checks for the V1 final readiness audit template."""

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
    / "v1_final_readiness_audit_template.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_final_readiness_template_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["template_id"] == "v1_final_readiness_audit_template"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["date"] == "2026-06-20"
    assert fixture["branch"] == "docs-v1-final-readiness-audit-template"
    assert fixture["source_lima_commit_before_template"] == (
        "8270cb1a6b6cfb1c36746d7ee5c7a1f8ed78cfd5"
    )
    assert fixture["template_verdict"] == "READY_TO_RUN_AFTER_UNBLOCKS"

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_final_readiness_template_requires_unblocks_before_pass() -> None:
    fixture = _load_fixture()

    assert fixture["required_unblocks_before_pass"] == {
        "public_sparkbot_publication_proven": False,
        "exactly_one_v1_g57_operator_decision_recorded": False,
        "g57_implementation_complete_if_approved": False,
    }
    assert fixture["required_repository_evidence"] == [
        "lima_ai_os_branch_and_commit_under_audit",
        "public_sparkbot_branch_and_target_publication_proof",
        "accessible_sparkbot_branch_and_pushed_commit",
        "arc_bot_shell_pushed_g56_commit_and_local_drift_exclusion_state",
        "g57_decision_state",
        "g57_implementation_state_if_approved",
    ]


def test_v1_final_readiness_template_validation_commands_cover_all_repos() -> None:
    commands = _load_fixture()["required_validation_commands"]

    assert set(commands) == {
        "public_sparkbot",
        "accessible_sparkbot",
        "arc_bot_shell",
        "lima_ai_os",
    }
    assert "test_sparkbot_lima_v1_g56_fake_executor" in commands["public_sparkbot"][0]
    assert commands["public_sparkbot"][1] == "git diff --check"
    assert "test_sparkbot_lima_v1_g56_fake_executor" in commands[
        "accessible_sparkbot"
    ][0]
    assert "test_arc_bot_shell_lima_v1_g56_fake_executor" in commands[
        "arc_bot_shell"
    ][0]
    assert commands["lima_ai_os"] == [
        "python -m compileall lima",
        "python -m pytest -q tests -p no:cacheprovider",
        "git diff --check",
    ]


def test_v1_final_readiness_template_pass_and_fail_criteria_are_explicit() -> None:
    fixture = _load_fixture()

    assert fixture["pass_criteria"] == [
        "public_sparkbot_branch_publication_proven",
        "public_sparkbot_g56_smoke_passes_after_publication",
        "accessible_sparkbot_g56_smoke_passes",
        "arc_bot_shell_g56_smoke_passes",
        "arc_bot_shell_local_drift_resolved_or_excluded",
        "g57_decision_state_resolved",
        "if_g57_approved_then_g57_implementation_and_closeout_pass",
        "lima_compileall_passes",
        "lima_full_suite_passes",
        "all_diff_checks_pass",
        "all_evidence_sanitized",
        "no_forbidden_behavior_or_readiness_claim_added_outside_final_audit_scope",
    ]
    assert fixture["fail_criteria"] == [
        "public_sparkbot_publication_still_blocked",
        "no_valid_g57_operator_decision_recorded",
        "g57_implementation_begins_without_approve_v1_g57",
        "consumer_or_lima_validation_fails",
        "raw_sensitive_or_patch_content_persisted",
        "forbidden_provider_network_secret_fallback_connector_physical_or_production_behavior_appears",
    ]


def test_v1_final_readiness_template_preserves_boundaries() -> None:
    boundaries = _load_fixture()["boundaries_preserved"]

    for key, value in boundaries.items():
        assert value is False, key


def test_v1_final_readiness_template_future_output_shape_is_bounded() -> None:
    fixture = _load_fixture()

    assert fixture["future_final_audit_output_files"] == [
        "docs/audits/V1_FINAL_READINESS_AUDIT.md",
        "tests/fixtures/runtime_extraction/v1_final_readiness_audit.json",
        "tests/test_v1_final_readiness_audit.py",
    ]
    assert fixture["allowed_future_pass_verdict"] == (
        "PASS_CANDIDATE_READY_FOR_FIRST_CONSUMER_TESTING"
    )
    assert fixture["production_readiness_claim_allowed"] is False


def test_v1_final_readiness_template_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (
        REPO_ROOT / fixture["documents"]["final_readiness_audit_template"]
    ).read_text(encoding="utf-8")

    assert "# V1 Final Readiness Audit Template" in text
    assert fixture["source_lima_commit_before_template"] in text
    assert "READY_TO_RUN_AFTER_UNBLOCKS" in text
    assert "public Sparkbot branch publication is proven" in text
    assert "exactly one V1-G57 operator decision is recorded" in text
    assert "Final audit executed by this template: no." in text
    assert "PASS_CANDIDATE_READY_FOR_FIRST_CONSUMER_TESTING" in text
    assert "must not claim production readiness" in text


def test_v1_final_readiness_template_has_no_sensitive_markers() -> None:
    fixture = _load_fixture()
    output = json.dumps(fixture, sort_keys=True)
    output += (
        REPO_ROOT / fixture["documents"]["final_readiness_audit_template"]
    ).read_text(encoding="utf-8")

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
