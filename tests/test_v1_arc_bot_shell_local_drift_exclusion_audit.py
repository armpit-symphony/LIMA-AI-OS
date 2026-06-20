"""Static checks for the V1 Arc-Bot-shell local drift exclusion audit."""

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
    / "v1_arc_bot_shell_local_drift_exclusion_audit.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_arc_drift_audit_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["audit_id"] == "v1_arc_bot_shell_local_drift_exclusion_audit"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["date"] == "2026-06-20"
    assert fixture["audit_branch"] == "audit-v1-arc-bot-shell-local-drift-exclusion"
    assert fixture["source_lima_commit_before_audit"] == (
        "2c3b7c95e8b5b46eb7089d1df90de7ce7472a569"
    )
    assert fixture["audit_verdict"] == "PASS_G56_EVIDENCE_EXCLUDED_FROM_LOCAL_DRIFT"

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_arc_drift_audit_records_sanitized_arc_state() -> None:
    state = _load_fixture()["arc_bot_shell_state"]

    assert state == {
        "local_path": "C:\\Users\\limap\\Arc-Bot-shell",
        "branch": "v1-g56-consumer-fake-executor-provider-sdk-network-egress-smoke",
        "pushed_commit": "ec06e7670f18eeae192fc0f995b6ffd07481d8c9",
        "tracked_modified_file_count": 26,
        "untracked_file_count": 45,
        "raw_diffs_read_or_persisted": False,
        "raw_file_contents_read_or_persisted": False,
    }


def test_v1_arc_drift_audit_excludes_approved_g56_files_from_drift() -> None:
    approved = _load_fixture()["approved_g56_files"]

    assert approved == {
        "test_path": (
            "tests/test_arc_bot_shell_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.py"
        ),
        "fixture_path": (
            "tests/fixtures/arc_bot_shell_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.json"
        ),
        "test_exists": True,
        "fixture_exists": True,
        "test_has_local_diff": False,
        "fixture_has_local_diff": False,
        "test_is_untracked": False,
        "fixture_is_untracked": False,
    }


def test_v1_arc_drift_audit_records_validation() -> None:
    validation = _load_fixture()["validation"]

    assert validation["arc_g56_fake_executor_smoke"] == {
        "command": (
            "python -m pytest -q "
            "tests\\test_arc_bot_shell_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.py "
            "-p no:cacheprovider"
        ),
        "passed": True,
        "tests_passed": 8,
    }
    assert validation["arc_diff_check"] == {
        "command": "git diff --check",
        "passed": True,
        "warnings": "line_ending_conversion_warnings_only",
    }


def test_v1_arc_drift_audit_accepts_only_exclusion_evidence() -> None:
    fixture = _load_fixture()

    assert fixture["evidence_accepted"] == [
        "arc_g56_fake_executor_proof_tied_to_pushed_commit",
        "local_dirty_files_outside_approved_g56_smoke_test_and_fixture",
        "local_dirty_files_not_accepted_as_lima_v1_proof",
        "dirty_files_require_separate_arc_ownership_cleanup_commit_or_future_audit",
    ]
    assert fixture["blocker_register_effect"] == {
        "v1_b4_reduced_by_exclusion_audit": True,
        "arc_bot_shell_clean": False,
        "dirty_files_accepted_as_v1_proof": False,
        "final_release_readiness_gate_closed": False,
    }


def test_v1_arc_drift_audit_boundaries_remain_false() -> None:
    boundaries = _load_fixture()["boundary_results"]

    for key, value in boundaries.items():
        assert value is False, key


def test_v1_arc_drift_audit_remaining_gates_and_stops_are_preserved() -> None:
    fixture = _load_fixture()

    assert fixture["remaining_open_gates"] == [
        "public_sparkbot_branch_publication",
        "exact_v1_g57_operator_decision",
        "v1_g57_implementation_only_if_approved",
        "final_v1_readiness_audit_after_remaining_gates_close",
    ]
    assert fixture["stop_conditions_preserved"] == [
        "revert_or_clean_unrelated_arc_work_without_explicit_instruction",
        "use_current_arc_dirty_files_as_v1_proof_without_separate_approval_or_audit",
        "public_sparkbot_push_without_write_credentials",
        "v1_g57_implementation_without_exact_approval",
        "consumer_repo_edit_from_audit_lane",
        "runtime_or_public_api_change_from_audit_lane",
        "secret_credential_token_sdk_endpoint_network_or_fallback_required",
        "raw_sensitive_or_patch_content_persistence",
        "v1_product_production_or_completion_claim",
    ]


def test_v1_arc_drift_audit_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["arc_drift_audit"]).read_text(
        encoding="utf-8"
    )

    assert "# V1 Arc-Bot-shell Local Drift Exclusion Audit" in text
    assert fixture["source_lima_commit_before_audit"] in text
    assert "PASS_G56_EVIDENCE_EXCLUDED_FROM_LOCAL_DRIFT" in text
    assert "Tracked modified file count: 26" in text
    assert "Untracked file count: 45" in text
    assert "Raw diffs read or persisted: no" in text
    assert "Approved G56 smoke test local diff status: clean" in text
    assert "Arc-Bot-shell dirty worktree cleaned by this audit: no." in text
    assert "does not close the final release-readiness gate by itself" in text


def test_v1_arc_drift_audit_has_no_sensitive_markers() -> None:
    fixture = _load_fixture()
    output = json.dumps(fixture, sort_keys=True)
    output += (REPO_ROOT / fixture["documents"]["arc_drift_audit"]).read_text(
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
