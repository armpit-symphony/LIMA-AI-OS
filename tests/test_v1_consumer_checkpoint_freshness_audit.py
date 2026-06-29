"""Static checks for the V1 consumer checkpoint freshness audit."""

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
    / "v1_consumer_checkpoint_freshness_audit.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_consumer_checkpoint_freshness_audit_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["audit_id"] == "v1_consumer_checkpoint_freshness_audit"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["date"] == "2026-06-28"
    assert fixture["branch"] == "docs-v1-post-g60-readiness-and-next-lane-matrix"
    assert fixture["source_lima_commit_before_audit"] == "58c26d8755cfe0cfd555433a4b8908ed304b74d1"
    assert fixture["source_lima_commit_before_audit_refresh"] == "58c26d8755cfe0cfd555433a4b8908ed304b74d1"
    assert fixture["audit_verdict"] == (
        "PASS_CONSUMER_CHECKPOINT_FRESHNESS_CANDIDATE_ONLY_CUTOVER_STILL_BLOCKED"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_consumer_checkpoint_freshness_audit_records_current_checkpoints() -> None:
    checkpoints = _load_fixture()["consumer_checkpoints"]

    assert checkpoints["public_sparkbot"] == {
        "local_path": "C:\\Users\\limap\\Sparkbot-public",
        "branch": "v1-g56-runtime-authority-chain-audit",
        "commit": "ae5cc9c563ea2b0f08c91af03164a78b4b20e3e2",
        "local_status_clean": True,
        "tracking_origin": False,
        "evidence_role": "public_candidate_smoke_checkpoint",
    }
    assert checkpoints["accessible_sparkbot"] == {
        "local_path": "C:\\Users\\limap\\Sparkbot",
        "branch": "v1-g56-consumer-fake-executor-provider-sdk-network-egress-smoke",
        "commit": "ddaa4ccaacd328ddcc1f00a040c2c140abee428e",
        "local_status_clean": True,
        "tracking_origin": True,
        "evidence_role": "accessible_candidate_smoke_checkpoint",
    }
    assert checkpoints["sparkbot_shell"] == {
        "local_path": "C:\\Users\\limap\\Sparkbot_shell",
        "branch": "sparkbot-shell-work-settings-runtime-preview",
        "commit": "548b6d6aa6cde98b261e867c0c2db86ddbfa83dc",
        "local_status_clean": True,
        "tracking_origin": True,
        "evidence_role": "shell_checkpoint_only",
    }
    assert checkpoints["arc_bot_shell"] == {
        "local_path": "C:\\Users\\limap\\Arc-Bot-shell",
        "branch": "v1-g56-consumer-fake-executor-provider-sdk-network-egress-smoke",
        "commit": "40fc474b0e09580a82f90518ebe341e2c98cd644",
        "local_status_clean": True,
        "tracking_origin": True,
        "recorded_clean_checkpoint_proof_commit": (
            "99a4ba4955f13626c2176a2c44592000029a16c3"
        ),
        "current_head_descends_from_recorded_clean_checkpoint": True,
        "evidence_role": "arc_candidate_smoke_checkpoint_clean_descendant",
    }


def test_v1_consumer_checkpoint_freshness_audit_records_command_results() -> None:
    commands = _load_fixture()["commands_executed"]

    assert commands["public_sparkbot_diff_check_passed"] is True
    assert commands["accessible_sparkbot_diff_check_passed"] is True
    assert commands["sparkbot_shell_diff_check_passed"] is True
    assert commands["arc_bot_shell_diff_check_passed"] is True
    assert commands["public_sparkbot_fake_executor_smoke_tests_passed"] == 8
    assert commands["accessible_sparkbot_fake_executor_smoke_tests_passed"] == 8
    assert commands["arc_bot_shell_fake_executor_smoke_tests_passed"] == 8
    assert commands["sparkbot_shell_fake_executor_smoke_tests_available_in_this_lane"] is False

    validation = _load_fixture()["post_audit_lima_validation_refresh"]
    assert validation["focused_consumer_checkpoint_tests_passed"] == 16
    assert validation["broader_v1_readiness_status_tests_passed"] == 56
    assert validation["compileall_lima_passed"] is True
    assert validation["full_lima_suite_tests_passed"] == 5435
    assert validation["cutover_operator_choice_created_by_validation"] is False
    assert (
        validation[
            "release_branch_tag_cutover_or_readiness_authority_created_by_validation"
        ]
        is False
    )
    assert (
        validation[
            "runtime_provider_network_credential_connector_or_physical_world_behavior_added_by_validation"
        ]
        is False
    )


def test_v1_consumer_checkpoint_freshness_audit_preserves_boundaries() -> None:
    fixture = _load_fixture()

    for key, value in fixture["boundaries_preserved"].items():
        assert value is False, key

    assert fixture["current_valid_cutover_operator_choice_count"] == 0
    assert fixture["next_required_action"] == "record_exactly_one_valid_cutover_operator_choice"


def test_v1_consumer_checkpoint_freshness_audit_records_post_58c_refresh() -> None:
    refresh = _load_fixture()["post_58c_consumer_freshness_refresh"]

    assert refresh["source_lima_commit_before_refresh"] == (
        "58c26d8755cfe0cfd555433a4b8908ed304b74d1"
    )
    assert refresh["focused_current_goal_consumer_freshness_tests_passed"] == 16
    assert refresh["broader_readiness_status_tests_passed"] == 56
    assert refresh["compileall_lima_passed"] is True
    assert refresh["full_lima_suite_tests_passed"] == 5435
    assert refresh["cutover_operator_choice_created_by_refresh"] is False
    assert refresh["release_branch_tag_cutover_or_readiness_authority_created_by_refresh"] is False
    assert refresh["runtime_provider_network_credential_connector_or_physical_world_behavior_added_by_refresh"] is False


def test_v1_consumer_checkpoint_freshness_audit_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["audit"]).read_text(encoding="utf-8")

    assert "# V1 Consumer Checkpoint Freshness Audit" in text
    assert fixture["source_lima_commit_before_audit"] in text
    assert fixture["audit_verdict"] in text
    assert "ae5cc9c563ea2b0f08c91af03164a78b4b20e3e2" in text
    assert "ddaa4ccaacd328ddcc1f00a040c2c140abee428e" in text
    assert "548b6d6aa6cde98b261e867c0c2db86ddbfa83dc" in text
    assert "40fc474b0e09580a82f90518ebe341e2c98cd644" in text
    assert "99a4ba4955f13626c2176a2c44592000029a16c3" in text
    assert "descends from the recorded clean-checkpoint proof commit" in text
    assert "passed, 8 tests" in text
    assert "Sparkbot_shell has no LIMA fake-executor smoke command in this audit lane" in text
    assert "Post-Audit LIMA Validation Refresh" in text
    assert "passed, 16 tests" in text
    assert "passed, 56 tests" in text
    assert "passed, 5435 tests" in text
    assert "This LIMA validation refresh creates no cutover operator choice" in text
    assert "Post-58c Consumer Freshness Supplement" in text
    assert "passed, 16 tests" in text
    assert "passed, 56 tests" in text
    assert "passed, 5435 tests" in text
    assert "Release-candidate branch created by this audit: no." in text
    assert "Consumer repositories modified by this audit: no." in text
    assert "valid cutover operator choice count remains `0`" in text
    assert "Machine action: `record_exactly_one_valid_cutover_operator_choice`" in text


def test_v1_consumer_checkpoint_freshness_audit_has_no_sensitive_markers() -> None:
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
