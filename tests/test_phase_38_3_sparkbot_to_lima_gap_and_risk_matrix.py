"""Phase 38.3 Sparkbot-to-LIMA gap and risk matrix tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_38_3_SPARKBOT_TO_LIMA_GAP_AND_RISK_MATRIX.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_38_3_sparkbot_to_lima_gap_and_risk_matrix.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_38_3_identifies_current_lima_support() -> None:
    support = set(_load_json(PHASE_FIXTURE_PATH)["current_lima_support"])
    assert "runtime_state_read_only_inspection" in support
    assert "candidate_preview_non_executing_preview" in support
    doc_text = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "`runtime_state` can inspect caller-provided state" in doc_text
    assert "`candidate_preview` can preview caller-provided candidate-shaped data" in doc_text


def test_phase_38_3_records_sparkbot_shaped_fixture_gaps() -> None:
    gaps = set(_load_json(PHASE_FIXTURE_PATH)["gaps"])
    assert "owner_local_read_posture_fixture_coverage" in gaps
    assert "breakglass_vault_posture_fixture_coverage" in gaps
    assert "mcp_robo_manifest_fixture_coverage" in gaps
    assert "robotics_simulation_and_real_hardware_fixture_coverage" in gaps
    assert "memory_trust_pending_approval_fixture_coverage" in gaps


def test_phase_38_3_rejects_runtime_or_integration_next_steps() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    not_recommended = set(fixture["not_recommended"])
    assert "runtime_implementation" in not_recommended
    assert "sparkbot_wiring_imports" in not_recommended
    assert "approval_enforcement" in not_recommended
    assert "execution" in not_recommended
    assert "robotics_physical_world_behavior" in not_recommended
    assert fixture["phase_39_runtime_implementation_recommended"] is False
    assert fixture["phase_39_lima_changes_required"] is False


def test_phase_38_3_recommends_test_only_candidate_preview_hardening() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert (
        fixture["recommended_phase_39_direction"]
        == "test_only_candidate_preview_hardening_with_sparkbot_shaped_fixtures"
    )
    cases = set(fixture["phase_39_fixture_cases"])
    assert "owner_local_routine_read_request" in cases
    assert "strict_security_risky_write_request" in cases
    assert "breakglass_required_vault_request" in cases
    assert "mcp_explain_plan_request" in cases
    assert "real_hardware_robot_motion_request" in cases
    assert "low_confidence_memory_write_pending_approval" in cases


def test_phase_38_3_stays_docs_tests_fixtures_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert not list((REPO_ROOT / "lima").rglob("*phase_38_3*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_38_3*"))
