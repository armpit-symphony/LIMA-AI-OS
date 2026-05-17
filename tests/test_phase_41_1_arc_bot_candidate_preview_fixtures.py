"""Phase 41.1 Arc Bot candidate preview fixture corpus tests."""

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
    / "phase_41_1_arc_bot_candidate_preview_fixtures.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_41_1_fixture_corpus_is_docs_tests_fixtures_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "41.1"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["fixture_data_only"] is True
    assert fixture["runtime_implementation_approved"] is False
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["runtime_behavior_changed"] is False


def test_phase_41_1_includes_all_arc_bot_fixture_cases() -> None:
    fixture_ids = {case["id"] for case in _load_json(PHASE_FIXTURE_PATH)["cases"]}
    assert fixture_ids == {
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


def test_phase_41_1_cases_carry_required_safe_control_flags() -> None:
    for case in _load_json(PHASE_FIXTURE_PATH)["cases"]:
        candidate_data = case["candidate_data"]
        assert candidate_data["execution_allowed"] is False
        assert candidate_data["side_effects_allowed"] is False
        assert candidate_data["approval_granted"] is False
        assert candidate_data["dispatch_allowed"] is False
        assert candidate_data["persistence_allowed"] is False
        assert case["expected_preview_state"] in {"proposed", "needs_review", "blocked"}
        assert isinstance(case["expected_blocked_claims"], list)


def test_phase_41_1_risky_cases_have_safe_expected_postures() -> None:
    cases = {case["id"]: case for case in _load_json(PHASE_FIXTURE_PATH)["cases"]}
    for risky_id in (
        "external_email_send_request",
        "calendar_write_request",
        "file_mutation_request",
        "low_confidence_memory_fact",
        "scheduled_task_requires_approval",
        "admin_breakglass_request",
        "robotics_physical_world_request",
        "sparkbot_only_behavior_rejected",
        "explain_plan_only_risky_request",
    ):
        assert cases[risky_id]["expected_preview_state"] == "blocked"
        assert cases[risky_id]["expected_blocked_claims"]
    assert cases["draft_email_no_send"]["expected_preview_state"] == "proposed"
    assert cases["strict_security_default_posture"]["expected_preview_state"] == "needs_review"


def test_phase_41_1_stays_in_approved_scope() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_41_1*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_41_1*"))
