"""Phase 40.3 Arc Bot candidate preview fixture plan tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_40_3_ARC_BOT_CANDIDATE_PREVIEW_FIXTURE_PLAN.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_40_3_arc_bot_candidate_preview_fixture_plan.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_40_3_plans_phase_41_without_runtime_scope() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "40.3"
    assert fixture["phase_41_recommended"] is True
    assert fixture["phase_41_lane"] == "docs_tests_fixtures_only_arc_bot_candidate_preview_hardening"
    assert fixture["runtime_implementation_recommended"] is False
    assert fixture["lima_changes_required"] is False
    assert fixture["tests_support_changes_required"] is False
    assert "Phase 41 must not modify runtime code" in PHASE_DOC_PATH.read_text(encoding="utf-8")


def test_phase_40_3_lists_arc_bot_office_fixture_cases() -> None:
    fixture_ids = {case["id"] for case in _load_json(PHASE_FIXTURE_PATH)["fixture_cases"]}
    expected_ids = {
        "draft_email_no_send",
        "external_email_send_request",
        "calendar_write_request",
        "file_mutation_request",
        "low_confidence_memory_fact",
        "connector_missing_secret",
        "agent_identity_kill_switch",
        "scheduled_task_requires_approval",
        "admin_breakglass_request",
        "robotics_physical_world_request",
        "sparkbot_only_behavior_rejected",
        "strict_security_default_posture",
        "explain_plan_only_risky_request",
    }
    assert expected_ids <= fixture_ids


def test_phase_40_3_expected_postures_block_action_paths() -> None:
    cases = {case["id"]: case["expected_posture"] for case in _load_json(PHASE_FIXTURE_PATH)["fixture_cases"]}
    assert cases["external_email_send_request"] == "blocked_or_awaiting_approval_no_dispatch"
    assert cases["calendar_write_request"] == "approval_posture_no_connector_write"
    assert cases["file_mutation_request"] == "blocked_no_file_mutation"
    assert cases["scheduled_task_requires_approval"] == "planned_or_awaiting_approval_no_worker_queue"
    assert cases["robotics_physical_world_request"] == "rejected_or_deferred_no_hardware"
    assert cases["sparkbot_only_behavior_rejected"] == "rejected_from_arc_defaults"


def test_phase_40_3_preserves_preview_only_invariants() -> None:
    invariants = _load_json(PHASE_FIXTURE_PATH)["hard_invariants"]
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
        assert invariants[key] is False
    assert invariants["non_authoritative"] is True
    assert invariants["preview_only"] is True
    assert invariants["safe_by_default"] is True


def test_phase_40_3_stays_in_approved_scope() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["runtime_behavior_changed"] is False
    assert not list((REPO_ROOT / "lima").rglob("*phase_40_3*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_40_3*"))
