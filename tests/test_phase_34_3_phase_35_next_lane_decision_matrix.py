"""Phase 35 next-lane decision matrix tests for Phase 34.3."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_34_3_PHASE_35_NEXT_LANE_DECISION_MATRIX.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_34_3_phase_35_next_lane_decision_matrix.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_34_3_is_docs_tests_fixtures_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "34.3"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_implementation_approved"] is False
    assert fixture["runtime_files_changed"] == []
    assert fixture["tests_support_changed"] is False
    assert "does not implement runtime behavior" in phase_doc


def test_phase_34_3_evidence_supports_no_code_design_review() -> None:
    evidence = _load_json(PHASE_FIXTURE_PATH)["phase_34_evidence"]
    assert evidence["phase_33_stayed_test_only"] is True
    assert evidence["phase_33_runtime_files_changed"] is False
    assert evidence["phase_33_tests_support_changed"] is False
    assert evidence["nested_suspicious_metadata_coverage_added"] is True
    assert evidence["runtime_state_gap_found"] is False
    assert evidence["remaining_immediate_test_gap_found"] is False


def test_phase_34_3_reviews_requested_phase_35_options() -> None:
    options = _load_json(PHASE_FIXTURE_PATH)["phase_35_options"]
    assert set(options) == {"A", "B", "C", "D", "E", "F"}
    assert options["A"] == "no_code_design_review_for_second_narrow_runtime_slice"
    assert options["F"] == "request_phil_approval_for_future_runtime_implementation_only_if_supported"


def test_phase_34_3_recommends_no_code_design_review_not_implementation() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert (
        fixture["recommended_phase_35_direction"]
        == "docs_tests_fixtures_only_no_code_design_review_for_second_narrow_runtime_slice"
    )
    assert fixture["immediate_runtime_implementation_recommended"] is False


def test_phase_34_3_preserves_phase_35_approval_question() -> None:
    question = _load_json(PHASE_FIXTURE_PATH)["approval_question"]
    assert question.startswith("Do you approve Phase 35 as a docs/tests/fixtures-only no-code design review")
    assert "no runtime implementation" in question
    assert "no new `lima/` changes" in question
    assert "no `tests/support/` changes" in question
    assert "no Sparkbot wiring" in question
    assert "no HumanInput runtime bridge behavior" in question
    assert "no hidden side effects" in question


def test_no_phase_34_3_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_34_3*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_34_3*"))
