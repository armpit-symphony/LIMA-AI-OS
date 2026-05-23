"""Phase 43.4 universal contract hardening archive tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_43_4_UNIVERSAL_CONTRACT_HARDENING_ARCHIVE_CLOSEOUT.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_43_4_universal_contract_hardening_archive_closeout.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_43_4_archives_all_phase_43_phases() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "43.4"
    assert fixture["test_only_hardening_archived"] is True
    assert fixture["completed_phases"] == ["43.0", "43.1", "43.2", "43.3", "43.4"]
    assert fixture["docs_tests_fixtures_only"] is True


def test_phase_43_4_records_universal_profile_coverage() -> None:
    coverage = set(_load_json(PHASE_FIXTURE_PATH)["coverage_added"])
    assert "arc_bot_office_task_profile" in coverage
    assert "sparkbot_reference_profile" in coverage
    assert "generic_automation_agent_profile" in coverage
    assert "browser_action_profile" in coverage
    assert "shell_action_profile" in coverage
    assert "file_mutation_profile" in coverage
    assert "network_api_action_profile" in coverage
    assert "scheduled_background_work_profile" in coverage
    assert "iot_device_action_profile" in coverage
    assert "drone_action_profile" in coverage
    assert "humanoid_action_profile" in coverage
    assert "robot_motion_profile" in coverage
    assert "emergency_stop_profile" in coverage
    assert "malicious_consumer_profile_trying_to_grant_approval" in coverage
    assert "malicious_embodiment_profile_trying_to_allow_execution" in coverage
    assert "nested_bypass_wording" in coverage


def test_phase_43_4_archives_candidate_preview_boundary() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["candidate_preview_boundary"]
    assert boundary["deterministic"] is True
    assert boundary["read_only"] is True
    assert boundary["local_only"] is True
    assert boundary["non_authoritative"] is True
    assert boundary["safe_by_default"] is True
    for key in (
        "execution_allowed",
        "side_effects_allowed",
        "approval_granted",
        "dispatch_allowed",
        "persistence_allowed",
        "humaninput_bridge_active",
        "sparkbot_wiring_active",
        "live_adapter_active",
        "external_calls_allowed",
        "robotics_allowed",
        "physical_world_allowed",
    ):
        assert boundary[key] is False


def test_phase_43_4_finds_no_runtime_gap_and_stops_at_merge_tag_gate() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["remaining_gaps"] == []
    assert fixture["runtime_gap_found"] is False
    assert fixture["runtime_change_needed"] is False
    assert fixture["runtime_implementation_recommended"] is False
    assert fixture["recommended_next_direction"] == "stop_at_merge_tag_approval_gate_for_phase_43_stack"
    text = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "No runtime change is needed." in text
    assert "Stop at the merge/tag approval gate" in text


def test_phase_43_4_stays_in_approved_scope() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["candidate_preview_changed"] is False
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["runtime_behavior_changed"] is False
    assert not list((REPO_ROOT / "lima").rglob("*phase_43_4*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_43_4*"))
