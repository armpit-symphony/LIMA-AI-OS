"""Static checks for the V1 current candidate validation refresh audit."""

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
    / "v1_current_candidate_validation_refresh_audit.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_current_candidate_validation_refresh_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["audit_id"] == "v1_current_candidate_validation_refresh_audit"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["date"] == "2026-06-20"
    assert fixture["branch"] == "audit-v1-current-candidate-validation-refresh"
    assert fixture["source_lima_commit_before_audit"] == (
        "7666ef3c25fd4a95b6bb7ce94937185ed0bc54ed"
    )
    assert fixture["audit_verdict"] == (
        "LOCAL_CANDIDATE_VALIDATION_REFRESH_PASS_WITH_EXTERNAL_BLOCKERS"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_current_candidate_validation_refresh_records_repository_state() -> None:
    state = _load_fixture()["repository_state_under_refresh"]

    assert state["lima_ai_os"]["branch_before_audit"] == (
        "docs-v1-final-candidate-branch-index"
    )
    assert state["lima_ai_os"]["commit"] == (
        "7666ef3c25fd4a95b6bb7ce94937185ed0bc54ed"
    )
    assert state["public_sparkbot_target_checkout"]["commit"] == (
        "ae5cc9c563ea2b0f08c91af03164a78b4b20e3e2"
    )
    assert "target_push_still_blocked" in state["public_sparkbot_target_checkout"][
        "state"
    ]
    assert state["accessible_sparkbot_checkpoint"]["state"] == "clean_pushed_branch"
    assert "unrelated_local_drift_excluded" in state["arc_bot_shell_checkpoint"][
        "state"
    ]


def test_v1_current_candidate_validation_refresh_records_consumer_validation() -> None:
    results = _load_fixture()["consumer_validation_results"]

    assert results["public_sparkbot_target_checkout"]["smoke_result"] == "8 passed"
    assert results["public_sparkbot_target_checkout"]["diff_check_result"] == (
        "passed_clean"
    )
    assert results["accessible_sparkbot_checkpoint"]["smoke_result"] == "8 passed"
    assert results["accessible_sparkbot_checkpoint"]["diff_check_result"] == (
        "passed_clean"
    )
    assert results["arc_bot_shell_checkpoint"]["smoke_result"] == "8 passed"
    assert results["arc_bot_shell_checkpoint"]["diff_check_result"] == (
        "completed_with_crlf_warnings_from_unrelated_dirty_tracked_files"
    )

    assert "test_sparkbot_lima_v1_g56_fake_executor" in results[
        "public_sparkbot_target_checkout"
    ]["smoke_command"]
    assert "test_arc_bot_shell_lima_v1_g56_fake_executor" in results[
        "arc_bot_shell_checkpoint"
    ]["smoke_command"]


def test_v1_current_candidate_validation_refresh_keeps_external_blockers() -> None:
    fixture = _load_fixture()

    assert fixture["external_blockers_remaining"] == [
        "public_sparkbot_write_credential_and_branch_publication",
        "exactly_one_valid_v1_g57_operator_choice_recorded",
    ]
    assert fixture["evidence_interpretation"] == [
        "public_sparkbot_local_checkout_still_validates_fake_executor_path",
        "accessible_sparkbot_pushed_checkpoint_still_validates_fake_executor_path",
        "arc_bot_shell_pushed_checkpoint_still_validates_fake_executor_path",
        "arc_bot_shell_local_dirty_files_remain_excluded_from_v1_proof",
        "public_sparkbot_target_publication_gate_unchanged",
        "v1_g57_gate_unchanged",
    ]


def test_v1_current_candidate_validation_refresh_preserves_boundaries() -> None:
    boundaries = _load_fixture()["boundaries_preserved"]

    for key, value in boundaries.items():
        assert value is False, key


def test_v1_current_candidate_validation_refresh_stop_conditions_are_bounded() -> None:
    assert _load_fixture()["stop_conditions"] == [
        "public_sparkbot_push_without_write_credentials",
        "v1_g57_implementation_without_exact_approval",
        "treat_this_audit_as_g57_approval",
        "consumer_repo_edit_from_audit_lane",
        "runtime_or_public_api_change_from_audit_lane",
        "secret_credential_token_sdk_endpoint_network_or_fallback_required",
        "raw_sensitive_or_patch_content_persistence",
        "v1_product_production_or_completion_claim",
    ]


def test_v1_current_candidate_validation_refresh_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (
        REPO_ROOT
        / fixture["documents"]["current_candidate_validation_refresh_audit"]
    ).read_text(encoding="utf-8")

    assert "# V1 Current Candidate Validation Refresh Audit" in text
    assert fixture["source_lima_commit_before_audit"] in text
    assert "LOCAL_CANDIDATE_VALIDATION_REFRESH_PASS_WITH_EXTERNAL_BLOCKERS" in text
    assert "Public Sparkbot target checkout" in text
    assert "8 passed" in text
    assert "CRLF conversion warnings" in text
    assert "Public Sparkbot G56 branch pushed to `sparkpit-labs/Sparkbot` by this audit: no." in text
    assert "V1.0 completion, product readiness, or production readiness claimed: no." in text


def test_v1_current_candidate_validation_refresh_has_no_sensitive_markers() -> None:
    fixture = _load_fixture()
    output = json.dumps(fixture, sort_keys=True)
    output += (
        REPO_ROOT
        / fixture["documents"]["current_candidate_validation_refresh_audit"]
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
