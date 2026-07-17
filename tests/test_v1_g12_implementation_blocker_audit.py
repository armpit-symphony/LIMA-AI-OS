"""Static checks for the V1-G12 implementation blocker audit."""

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
    / "v1_g12_implementation_blocker_audit.json"
)
STATE_PATH = REPO_ROOT / "docs" / "CURRENT_PROJECT_STATE.md"


def _load_json(path: Path) -> dict[str, Any]:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g12_implementation_blocker_audit_docs_exist() -> None:
    fixture = _load_json(FIXTURE_PATH)
    assert fixture["gap_id"] == "V1-G12"
    assert fixture["audit_id"] == "v1_g12_implementation_blocker_audit"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g12-durable-audit-evidence-persistence-approval-request"
    assert fixture["source_commit_before_audit"] == "2cb9aab35c5a9ee8e1d2505a7fca06355fc90d05"
    assert fixture["docs_tests_fixtures_only"] is True

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g12_implementation_is_blocked_without_approval() -> None:
    fixture = _load_json(FIXTURE_PATH)
    assert fixture["audit_verdict"] == "implementation_blocked_pending_operator_decision"
    assert fixture["blocking_condition"] == "missing_valid_approve_v1_g12_decision_record"
    assert fixture["operator_approval_recorded"] is False
    assert fixture["runtime_implementation_approved"] is False
    assert fixture["required_approval_choice"] == "Approve-V1-G12"
    assert fixture["required_approval_branch"] == "v1-g12-durable-audit-evidence-persistence"
    assert (
        fixture["recommended_next_step"]
        == "record_exactly_one_valid_operator_choice_before_v1_g12_runtime_implementation"
    )


def test_v1_g12_decision_record_remains_empty() -> None:
    decision_record = _load_json(FIXTURE_PATH)["decision_record"]
    assert decision_record["recorded_choice"] is None
    assert decision_record["recorded_approval_wording"] is None
    assert decision_record["recorded_revision_request"] is None
    assert decision_record["recorded_pause_reason"] is None
    assert decision_record["approved_implementation_branch"] is None
    assert decision_record["runtime_implementation_approved"] is False


def test_v1_g12_valid_choices_are_exact() -> None:
    fixture = _load_json(FIXTURE_PATH)
    assert set(fixture["valid_operator_choices"]) == {
        "Approve-V1-G12",
        "Revise-V1-G12",
        "Pause",
    }


def test_v1_g12_can_only_continue_docs_tests_fixtures_without_operator() -> None:
    fixture = _load_json(FIXTURE_PATH)
    assert set(fixture["can_continue_without_operator"]) == {
        "docs_tests_fixtures_only_review",
        "operator_decision_recording",
    }

    blocked = set(fixture["cannot_continue_without_operator"])
    for blocked_item in (
        "v1_g12_runtime_implementation",
        "lima_runtime_file_changes",
        "durable_persistence_behavior",
        "storage_adapter_behavior",
        "query_api_behavior",
        "external_database_writes",
        "provider_model_routing",
        "shell_wiring_or_consumer_integration",
        "humaninput_bridge_activation",
        "connector_behavior",
        "browser_file_network_device_robotics_physical_world_behavior",
        "runtime_export_cleanup",
        "final_api_freeze",
    ):
        assert blocked_item in blocked


def test_v1_g12_blocker_audit_adds_no_runtime_behavior() -> None:
    boundary = _load_json(FIXTURE_PATH)["boundary_results"]
    for key in (
        "runtime_behavior_added",
        "durable_persistence_added",
        "storage_adapter_added",
        "query_api_added",
        "external_database_writes_added",
        "lima_runtime_files_changed",
        "tests_support_changed",
        "consumer_repos_touched",
        "sparkbot_touched",
        "sparkbot_shell_touched",
        "arc_bot_shell_touched",
        "lima_robo_os_touched",
        "lima_office_touched",
        "sparkbot_code_copied",
        "sparkbot_import_added",
        "provider_model_routing_added",
        "shell_wiring_added",
        "humaninput_bridge_activated",
        "connector_behavior_added",
        "browser_file_network_device_robotics_physical_world_added",
        "runtime_export_cleanup_approved",
        "final_freeze_approved",
        "v1_product_ready",
        "production_ready",
    ):
        assert boundary[key] is False


def test_v1_g12_blocker_audit_docs_match_fixture() -> None:
    fixture = _load_json(FIXTURE_PATH)
    audit_text = (REPO_ROOT / fixture["documents"]["implementation_blocker_audit"]).read_text(
        encoding="utf-8"
    )
    state_text = STATE_PATH.read_text(encoding="utf-8")

    for phrase in fixture["doc_required_phrases"]:
        assert phrase in audit_text

    assert "V1-G12 implementation blocker audit document" in state_text
    assert "V1-G12 implementation blocker status: active until `Approve-V1-G12` is recorded" in state_text
