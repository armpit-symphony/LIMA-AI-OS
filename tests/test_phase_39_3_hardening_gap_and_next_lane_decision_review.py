"""Phase 39.3 hardening gap and next-lane decision tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_39_3_HARDENING_GAP_AND_NEXT_LANE_DECISION_REVIEW.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_39_3_hardening_gap_and_next_lane_decision_review.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_39_3_records_no_runtime_gap_found() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "39.3"
    assert fixture["phase_39_2_runtime_gap_found"] is False
    assert "Phase 39.2 found no runtime gap." in PHASE_DOC_PATH.read_text(encoding="utf-8")


def test_phase_39_3_confirms_all_sparkbot_shaped_cases_were_covered() -> None:
    cases = set(_load_json(PHASE_FIXTURE_PATH)["sparkbot_shaped_cases_covered"])
    assert "owner_local_routine_read_request" in cases
    assert "strict_security_risky_write_request" in cases
    assert "breakglass_required_vault_request" in cases
    assert "mcp_explain_plan_request" in cases
    assert "robo_os_simulation_request" in cases
    assert "real_hardware_robot_motion_request" in cases
    assert "agent_identity_kill_switch_true" in cases
    assert "low_confidence_memory_write_pending_approval" in cases


def test_phase_39_3_recommends_closeout_then_pause() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["recommended_next_step"] == "phase_39_4_archive_and_closeout"
    assert fixture["recommended_after_closeout"] == "pause_and_preserve_current_runtime_test_state"
    assert fixture["phil_approval_required_after_closeout"] is False
    assert fixture["next_lane_options"]["runtime_implementation"] == "not_recommended_not_approved"


def test_phase_39_3_keeps_scope_closed() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert not list((REPO_ROOT / "lima").rglob("*phase_39_3*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_39_3*"))
