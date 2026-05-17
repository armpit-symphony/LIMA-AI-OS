"""Phase 39.1 Sparkbot-shaped fixture tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_39_1_sparkbot_shaped_candidate_preview_fixtures.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_39_1_contains_all_required_sparkbot_shaped_cases() -> None:
    cases = {case["case_id"] for case in _load_json(PHASE_FIXTURE_PATH)["cases"]}
    assert cases == {
        "owner_local_routine_read_request",
        "strict_security_risky_write_request",
        "breakglass_required_vault_request",
        "mcp_explain_plan_request",
        "robo_os_simulation_request",
        "real_hardware_robot_motion_request",
        "agent_identity_kill_switch_true",
        "low_confidence_memory_write_pending_approval",
    }


def test_phase_39_1_fixtures_are_caller_provided_data_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["fixtures_are_caller_provided_data_only"] is True
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["tests_support_changed"] is False


def test_phase_39_1_each_case_expects_blocked_inert_preview() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    for case in fixture["cases"]:
        assert case["expected_preview_state"] == "blocked"
        assert case["expected_blocked_claims"]
        candidate = case["candidate"]
        assert candidate["execution_allowed"] is False
        assert candidate["side_effects_allowed"] is False
        assert candidate["approval_state"] == "proposed"
        assert candidate["dispatch_allowed"] is False
        assert candidate["persistence_allowed"] is False


def test_phase_39_1_records_required_inert_flags() -> None:
    flags = _load_json(PHASE_FIXTURE_PATH)["expected_inert_flags"]
    assert flags["non_authoritative"] is True
    assert flags["read_only"] is True
    assert flags["execution_allowed"] is False
    assert flags["approval_granted"] is False
    assert flags["dispatch_allowed"] is False
    assert flags["persistence_allowed"] is False
    assert flags["sparkbot_wiring_active"] is False
    assert flags["robotics_allowed"] is False
    assert flags["physical_world_allowed"] is False


def test_phase_39_1_files_are_not_under_runtime_or_support_paths() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_39_1*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_39_1*"))
