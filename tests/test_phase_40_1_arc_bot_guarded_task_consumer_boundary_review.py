"""Phase 40.1 Arc Bot guarded task consumer boundary tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_40_1_ARC_BOT_GUARDED_TASK_CONSUMER_BOUNDARY_REVIEW.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_40_1_arc_bot_guarded_task_consumer_boundary_review.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_40_1_preserves_arc_bot_as_primary_consumer() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "40.1"
    assert fixture["sparkbot_reference_evidence_only"] is True
    assert fixture["primary_guarded_task_consumer"] == "arc_bot_lima_ai_office"
    assert fixture["lima_ai_os_runtime_safety_substrate_target"] is True
    assert "Arc Bot / LIMA AI Office is the primary guarded task-oriented office consumer" in PHASE_DOC_PATH.read_text(encoding="utf-8")


def test_phase_40_1_rejects_sparkbot_workstation_inheritance() -> None:
    not_values = set(_load_json(PHASE_FIXTURE_PATH)["arc_bot_is_not"])
    assert "full_personal_workstation_bot" in not_values
    assert "shell_browser_live_terminal_code_execution_surface" in not_values
    assert "sparkbot_clone" in not_values
    assert "humaninput_runtime_bridge" in not_values
    assert "robotics_physical_world_controller" in not_values


def test_phase_40_1_sets_stricter_default_posture() -> None:
    posture = set(_load_json(PHASE_FIXTURE_PATH)["stricter_default_posture"])
    assert "external_writes_require_approval_posture" in posture
    assert "secrets_blocked_or_breakglass_required" in posture
    assert "admin_actions_blocked_or_breakglass_required" in posture
    assert "scheduled_work_planned_or_awaiting_approval" in posture
    assert "physical_world_robotics_rejected_or_deferred" in posture


def test_phase_40_1_defines_consumer_boundary_fields() -> None:
    fields = set(_load_json(PHASE_FIXTURE_PATH)["consumer_boundary_fields"])
    assert "task_intake" in fields
    assert "operator_approval_boundary" in fields
    assert "explain_plan_required" in fields
    assert "audit_evidence_ref" in fields
    assert "connector_health" in fields
    assert "physical_world_posture" in fields


def test_phase_40_1_stays_in_approved_scope() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["runtime_behavior_changed"] is False
    assert not list((REPO_ROOT / "lima").rglob("*phase_40_1*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_40_1*"))
