"""Static checks for Phase 12.4 decision gate closeout."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_12_4_PHASE_12_DECISION_GATE_CLOSEOUT.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_12_4_phase_12_decision_gate_closeout.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_docs_tests_fixtures_only_closeout() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "12.4"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False
    assert fixture["phase_13_requires_explicit_phil_approval"] is True


def test_phase_twelve_zero_through_three_are_listed_complete() -> None:
    completed = _load_json(PHASE_FIXTURE_PATH)["completed_phase_12_scope"]
    assert completed == [
        "phase_12_0_post_phase_11_runtime_slice_review",
        "phase_12_1_next_direction_options_runtime_sparkbot_robo_os_pause",
        "phase_12_2_threat_model_and_safety_gap_review",
        "phase_12_3_next_lane_recommendation_matrix",
    ]


def test_recommended_next_lane_is_threat_model_test_planning_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase_12_result"] == "planning_only_decision_gate"
    assert fixture["recommended_next_lane"] == "docs_tests_fixtures_only_threat_model_derived_test_planning"
    question = fixture["next_approval_question"]
    assert "docs/tests/fixtures-only threat-model-derived test planning lane" in question
    assert "forbidding runtime implementation" in question
    assert "Sparkbot wiring" in question
    assert "physical-world action" in question


def test_still_blocked_includes_all_forbidden_runtime_and_integration_scope() -> None:
    blocked = set(_load_json(PHASE_FIXTURE_PATH)["still_blocked"])
    assert "runtime_implementation" in blocked
    assert "lima_changes" in blocked
    assert "tests_support_changes" in blocked
    assert "sparkbot_wiring" in blocked
    assert "humaninput_runtime_bridge" in blocked
    assert "live_adapter" in blocked
    assert "intentcompiler_runtime_behavior" in blocked
    assert "guardiandecision_runtime_behavior" in blocked
    assert "approval_enforcement" in blocked
    assert "execution" in blocked
    assert "dispatch" in blocked
    assert "audit_persistence" in blocked
    assert "shell_browser_network_file_mutation_robotics_physical_world_action" in blocked


def test_phase_document_closes_lane_and_stops_before_phase_thirteen() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "closes the Phase 12 docs/tests/fixtures-only planning lane" in phase_doc
    assert "Phase 12 was planning only" in phase_doc
    assert "Do you approve Phase 13" in phase_doc
    assert "The repo should stop here before Phase 13" in phase_doc


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["candidate_status_expanded"] is False
    assert boundary["intake_candidate_expanded"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["humaninput_runtime_bridge_added"] is False
    assert boundary["live_adapter_added"] is False
    assert boundary["approval_enforcement_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True


def test_no_phase_twelve_four_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_12_4*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_12_4*"))
