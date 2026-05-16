"""Next-lane decision matrix tests for Phase 26.3."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_26_3_NEXT_LANE_DECISION_MATRIX.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_26_3_next_lane_decision_matrix.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_26_3_is_decision_review_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "26.3"
    assert fixture["runtime_code_modified"] is False
    assert "decision review only" in phase_doc
    assert "does not implement runtime behavior" in phase_doc


def test_all_recommended_phase_27_options_are_reviewed() -> None:
    options = _load_json(PHASE_FIXTURE_PATH)["options_reviewed"]
    assert options["A"] == "no_code_design_lane_for_next_narrow_runtime_slice"
    assert options["B"] == "additional_test_only_hardening"
    assert options["C"] == "sparkbot_integration_boundary_planning"
    assert options["D"] == "robo_os_physical_world_boundary_planning"
    assert options["E"] == "pause_and_preserve_current_runtime_test_state"


def test_exactly_one_phase_27_direction_is_recommended() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["recommended_option"] == "E"
    assert (
        fixture["recommended_phase_27_direction"]
        == "docs_tests_fixtures_only_preservation_and_roadmap_decision"
    )
    assert "Phase 27 should be Option E" in PHASE_DOC_PATH.read_text(encoding="utf-8")


def test_recommendation_rationale_keeps_runtime_expansion_gated() -> None:
    rationale = set(_load_json(PHASE_FIXTURE_PATH)["recommendation_rationale"])
    assert "phase_25_already_strengthened_cross_api_invariant_coverage" in rationale
    assert "phase_26_archives_the_evidence_path" in rationale
    assert "runtime_or_integration_expansion_requires_fresh_phil_decision" in rationale
    assert "phase_5_runtime_bridge_remains_gated" in rationale


def test_phase_27_approval_question_preserves_forbidden_scope() -> None:
    question = _load_json(PHASE_FIXTURE_PATH)["phase_27_approval_question"]
    assert "docs/tests/fixtures-only preservation" in question
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


def test_boundary_results_keep_phase_27_gated() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True
    assert boundary["phase_27_requires_explicit_approval"] is True


def test_next_phase_is_archive_closeout() -> None:
    assert _load_json(PHASE_FIXTURE_PATH)["next_phase"] == "26.4"
    assert "Continue only to Phase 26.4" in PHASE_DOC_PATH.read_text(encoding="utf-8")


def test_no_phase_26_3_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_26_3*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_26_3*"))
