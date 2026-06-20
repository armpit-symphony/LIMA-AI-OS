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
    assert fixture["date"] == "2026-06-20"
    assert fixture["branch"] == (
        "docs-v1-public-sparkbot-g56-publication-resolved"
    )
    assert fixture["source_lima_commit_before_register_refresh"] == "cbc16dc"
    assert fixture["register_verdict"] == "STOPPED_AT_V1_G57_OPERATOR_DECISION"

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_final_blocker_register_records_verified_blockers() -> None:
    blockers = _load_fixture()["verified_blockers"]
    g57 = blockers["v1_g57_implementation"]

    assert g57["implementation_approval_recorded"] is False
    assert g57["valid_operator_choices"] == [
        "Approve-V1-G57",
        "Revise-V1-G57",
        "Pause",
    ]
    assert g57["required_unblock"] == (
        "record_exactly_one_valid_v1_g57_operator_choice"
    )


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


def test_v1_final_blocker_register_preserves_all_boundaries() -> None:
    boundaries = _load_fixture()["boundaries_preserved"]

    for key, value in boundaries.items():
        assert value is False, key


def test_v1_final_blocker_register_records_evidence_and_next_actions() -> None:
    fixture = _load_fixture()

    assert fixture["current_verified_evidence"] == [
        "v1_candidate_handoff_execution_audit_exists",
        "v1_arc_bot_shell_local_drift_exclusion_audit_exists",
        "v1_public_sparkbot_g56_publication_resolution_audit_exists",
        "public_sparkbot_local_g56_fake_executor_smoke_passed",
        "public_sparkbot_remote_g56_branch_visible_at_expected_commit",
        "accessible_sparkbot_g56_fake_executor_smoke_passed",
        "arc_bot_shell_g56_fake_executor_smoke_passed",
        "arc_bot_shell_approved_g56_test_and_fixture_clean",
        "lima_focused_g56_g57_readiness_status_tests_passed",
        "lima_full_suite_passed",
        "lima_diff_hygiene_passed",
    ]
    assert fixture["excluded_non_blocking_drift"] == {
        "arc_bot_shell_local_worktree": (
            "audited_excluded_from_pushed_g56_evidence"
        ),
        "dirty_files_cleaned_or_reverted": False,
        "dirty_files_accepted_as_v1_proof": False,
    }
    assert fixture["next_unblock_actions"] == [
        "record_exactly_one_v1_g57_operator_choice",
        "if_approve_v1_g57_is_recorded_implement_only_metadata_scope",
    ]


def test_v1_final_blocker_register_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["final_blocker_register"]).read_text(
        encoding="utf-8"
    )

    assert "# V1 Final Blocker Register" in text
    assert "STOPPED_AT_V1_G57_OPERATOR_DECISION" in text
    assert "V1_ARC_BOT_SHELL_LOCAL_DRIFT_EXCLUSION_AUDIT.md" in text
    assert "V1_PUBLIC_SPARKBOT_G56_PUBLICATION_RESOLUTION_AUDIT.md" in text
    assert "Public Sparkbot G56 branch pushed to `sparkpit-labs/Sparkbot`: yes." in text
    assert "Approve-V1-G57" in text
    assert "Arc-Bot-shell dirty files accepted as V1 proof by this register: no." in text
    assert "V1-G57 implementation approval recorded: no." in text
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
