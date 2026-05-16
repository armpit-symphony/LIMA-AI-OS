"""Phase 29 decision readiness matrix tests for Phase 28.3."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_28_3_PHASE_29_DECISION_READINESS_MATRIX.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_28_3_phase_29_decision_readiness_matrix.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_28_3_is_decision_readiness_review_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "28.3"
    assert fixture["runtime_code_modified"] is False
    assert "decision readiness review only" in phase_doc
    assert "does not implement runtime behavior" in phase_doc


def test_all_phase_29_options_are_reviewed() -> None:
    options = _load_json(PHASE_FIXTURE_PATH)["options_reviewed"]
    assert options["A"] == "no_code_design_review_for_next_narrow_runtime_slice"
    assert options["B"] == "additional_test_only_hardening_only_if_concrete_gap_found"
    assert options["C"] == "sparkbot_integration_boundary_planning_only"
    assert options["D"] == "robo_os_physical_world_boundary_planning_only"
    assert options["E"] == "continue_preservation_pause_only_if_specific_documented_risk"
    assert options["F"] == "future_runtime_design_proposal_not_implementation"


def test_phase_29_recommendation_is_no_code_design_review() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["recommended_option"] == "A"
    assert fixture["recommended_phase_29_direction"] == (
        "docs_tests_fixtures_only_no_code_design_review_for_next_narrow_runtime_slice"
    )
    assert "Phase 29 should be Option A" in PHASE_DOC_PATH.read_text(encoding="utf-8")


def test_other_defaults_are_not_selected_without_evidence() -> None:
    reasons = _load_json(PHASE_FIXTURE_PATH)["why_not_other_defaults"]
    assert reasons["additional_test_only_hardening_not_recommended"] == (
        "no_concrete_immediate_gap_found"
    )
    assert reasons["continued_pause_not_recommended"] == (
        "no_specific_documented_risk_requires_another_pause"
    )


def test_phase_29_approval_question_preserves_no_runtime_scope() -> None:
    question = _load_json(PHASE_FIXTURE_PATH)["phase_29_approval_question"]
    assert "docs/tests/fixtures-only no-code design review" in question
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


def test_boundary_results_keep_phase_29_gated() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["runtime_implementation_approved"] is False
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True
    assert boundary["phase_29_requires_explicit_approval"] is True


def test_no_phase_28_3_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_28_3*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_28_3*"))
