"""Phase 39.4 Sparkbot-shaped hardening archive tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_39_4_PHASE_39_SPARKBOT_SHAPED_HARDENING_ARCHIVE_CLOSEOUT.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_39_4_phase_39_sparkbot_shaped_hardening_archive_closeout.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_39_4_archives_completed_hardening_lane() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "39.4"
    assert fixture["completed_phases"] == ["39.0", "39.1", "39.2", "39.3", "39.4"]
    assert "Phase 39 completed:" in PHASE_DOC_PATH.read_text(encoding="utf-8")


def test_phase_39_4_records_all_coverage_added() -> None:
    coverage = set(_load_json(PHASE_FIXTURE_PATH)["coverage_added"])
    assert "owner_local_routine_read_request" in coverage
    assert "strict_security_risky_write_request" in coverage
    assert "breakglass_required_vault_request" in coverage
    assert "mcp_explain_plan_request" in coverage
    assert "robo_os_simulation_request" in coverage
    assert "real_hardware_robot_motion_request" in coverage
    assert "agent_identity_kill_switch_true" in coverage
    assert "low_confidence_memory_write_pending_approval" in coverage


def test_phase_39_4_confirms_no_runtime_gap_or_scope_expansion() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["runtime_gap_found"] is False
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["stale_prior_phase_tests_changed"] is False
    assert fixture["runtime_behavior_changed"] is False


def test_phase_39_4_confirms_boundaries_remain_closed() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase_5_runtime_bridge_gated"] is True
    assert fixture["execution_approval_dispatch_persistence_absent"] is True
    assert fixture["sparkbot_wiring_imports_absent"] is True
    assert fixture["live_adapters_absent"] is True
    assert fixture["shell_browser_network_file_mutation_absent"] is True
    assert fixture["robotics_physical_world_behavior_absent"] is True
    assert fixture["external_background_subprocess_thread_queue_daemon_database_hidden_side_effects_absent"] is True


def test_phase_39_4_recommends_pause_without_approval_question() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["remaining_gaps"] == []
    assert fixture["recommended_next_direction"] == "pause_and_preserve_current_runtime_test_state"
    assert fixture["next_approval_question_required"] is False


def test_phase_39_4_files_are_not_under_runtime_or_support_paths() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_39_4*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_39_4*"))
