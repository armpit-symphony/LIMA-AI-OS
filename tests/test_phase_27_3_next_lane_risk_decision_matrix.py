"""Next-lane risk decision matrix tests for Phase 27.3."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_27_3_NEXT_LANE_RISK_DECISION_MATRIX.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_27_3_next_lane_risk_decision_matrix.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_27_3_is_risk_decision_review_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "27.3"
    assert fixture["runtime_code_modified"] is False
    assert "risk decision review only" in phase_doc
    assert "does not implement runtime behavior" in phase_doc


def test_all_phase_28_options_are_reviewed() -> None:
    options = _load_json(PHASE_FIXTURE_PATH)["options_reviewed"]
    assert options["A"] == "continue_preservation_pause"
    assert options["B"] == "no_code_design_review_for_next_narrow_runtime_slice"
    assert options["C"] == "additional_test_only_hardening"
    assert options["D"] == "sparkbot_integration_boundary_planning_only"
    assert options["E"] == "robo_os_physical_world_boundary_planning_only"
    assert options["F"] == "future_runtime_design_proposal_not_implementation"


def test_exactly_one_phase_28_direction_is_recommended() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["recommended_option"] == "A"
    assert (
        fixture["recommended_phase_28_direction"]
        == "docs_tests_fixtures_only_preservation_status_review"
    )
    assert "Phase 28 should be Option A" in PHASE_DOC_PATH.read_text(encoding="utf-8")


def test_recommendation_rationale_preserves_pause() -> None:
    rationale = set(_load_json(PHASE_FIXTURE_PATH)["recommendation_rationale"])
    assert "current_runtime_test_state_is_known_good" in rationale
    assert "phase_5_runtime_bridge_remains_gated" in rationale
    assert "small_runtime_slice_remains_non_executing" in rationale
    assert "next_runtime_or_integration_direction_requires_new_phil_decision" in rationale


def test_phase_28_approval_question_preserves_forbidden_scope() -> None:
    question = _load_json(PHASE_FIXTURE_PATH)["phase_28_approval_question"]
    assert "docs/tests/fixtures-only preservation status review" in question
    assert "runtime implementation" in question
    assert "lima/ changes" in question
    assert "tests/support/ changes" in question
    assert "Sparkbot wiring" in question
    assert "HumanInput runtime bridge" in question
    assert "approval enforcement" in question
    assert "execution" in question
    assert "dispatch" in question
    assert "audit persistence" in question
    assert "physical-world action" in question
    assert "hidden side effects" in question


def test_boundary_results_keep_phase_28_gated() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True
    assert boundary["phase_28_requires_explicit_approval"] is True


def test_no_phase_27_3_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_27_3*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_27_3*"))
