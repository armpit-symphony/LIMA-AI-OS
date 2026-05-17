"""Next-lane decision matrix tests for Phase 37.3."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_37_3_NEXT_LANE_DECISION_MATRIX.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_37_3_next_lane_decision_matrix.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_37_3_adds_no_runtime_behavior() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "37.3"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_behavior_added_in_phase_37_3"] is False
    assert fixture["runtime_files_changed_in_phase_37_3"] == []
    assert "does not modify `lima/`" in PHASE_DOC_PATH.read_text(encoding="utf-8")


def test_next_lane_options_are_reviewed() -> None:
    options = set(_load_json(PHASE_FIXTURE_PATH)["options_reviewed"])
    assert "A_additional_audit_archive" in options
    assert "B_additional_test_only_hardening" in options
    assert "C_no_code_design_review_for_third_runtime_slice" in options
    assert "D_humaninput_bridge_boundary_planning_only" in options
    assert "E_sparkbot_integration_boundary_planning_only" in options
    assert "F_pause_and_preserve_current_state" in options
    assert "G_request_future_runtime_implementation_approval" in options


def test_pause_and_preserve_is_recommended_without_runtime_approval() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert (
        fixture["recommended_next_direction"]
        == "pause_and_preserve_current_runtime_test_state_after_phase_37_4"
    )
    assert fixture["immediate_runtime_implementation_recommended"] is False
    assert fixture["additional_test_only_hardening_recommended"] is False
    assert fixture["no_code_design_review_recommended"] is False
    assert fixture["phil_approval_question_required_after_phase_37_4"] is False


def test_recommendation_reasons_are_grounded_in_clean_audit() -> None:
    reasons = _load_json(PHASE_FIXTURE_PATH)["recommendation_reasons"]
    assert all(reasons.values())
    assert reasons["phase_36_slice_clean"] is True
    assert reasons["no_regression_found"] is True
    assert reasons["no_blocking_gap_found"] is True
    assert reasons["forbidden_scope_not_needed"] is True


def test_no_phase_37_3_files_exist_under_lima_tests_support_or_old_phase_tests() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_37_3*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_37_3*"))
    assert not list((REPO_ROOT / "tests").glob("test_phase_35_*phase_37_3*"))
