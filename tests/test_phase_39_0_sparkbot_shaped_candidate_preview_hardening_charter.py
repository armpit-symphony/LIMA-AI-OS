"""Phase 39.0 Sparkbot-shaped candidate preview hardening charter tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_39_0_SPARKBOT_SHAPED_CANDIDATE_PREVIEW_HARDENING_CHARTER.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_39_0_sparkbot_shaped_candidate_preview_hardening_charter.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_39_0_opens_test_only_hardening_lane() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "39.0"
    assert fixture["starting_phase_38_audit_result"] == "PASS"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_implementation_approved"] is False
    assert "This phase is docs/tests/fixtures-only" in PHASE_DOC_PATH.read_text(encoding="utf-8")


def test_phase_39_0_declares_required_fixture_cases() -> None:
    cases = set(_load_json(PHASE_FIXTURE_PATH)["required_fixture_cases"])
    assert "owner_local_routine_read_request" in cases
    assert "strict_security_risky_write_request" in cases
    assert "breakglass_required_vault_request" in cases
    assert "mcp_explain_plan_request" in cases
    assert "robo_os_simulation_request" in cases
    assert "real_hardware_robot_motion_request" in cases
    assert "agent_identity_kill_switch_true" in cases
    assert "low_confidence_memory_write_pending_approval" in cases


def test_phase_39_0_declares_inert_preview_outcome() -> None:
    outcome = _load_json(PHASE_FIXTURE_PATH)["required_preview_outcome"]
    assert outcome["non_authoritative"] is True
    assert outcome["read_only"] is True
    assert outcome["execution_allowed"] is False
    assert outcome["approval_granted"] is False
    assert outcome["dispatch_allowed"] is False
    assert outcome["persistence_allowed"] is False
    assert outcome["sparkbot_wiring_active"] is False
    assert outcome["robotics_allowed"] is False
    assert outcome["physical_world_allowed"] is False


def test_phase_39_0_stays_out_of_runtime_and_support_paths() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert not list((REPO_ROOT / "lima").rglob("*phase_39_0*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_39_0*"))
