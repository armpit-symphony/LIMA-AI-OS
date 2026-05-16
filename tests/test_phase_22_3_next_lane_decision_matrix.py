"""Decision matrix checks for Phase 22.3."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_22_3_NEXT_LANE_DECISION_MATRIX.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_22_3_next_lane_decision_matrix.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_22_3_is_no_code_decision_matrix() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "22.3"
    assert fixture["runtime_code_modified"] is False
    assert fixture["boundary_results"]["lima_modified"] is False
    assert fixture["boundary_results"]["tests_support_modified"] is False


def test_decision_matrix_recommends_exactly_one_direction() -> None:
    options = _load_json(PHASE_FIXTURE_PATH)["options"]
    recommended = [
        option["direction"]
        for option in options.values()
        if option["recommendation"] == "recommend"
    ]
    assert recommended == ["test_only_hardening_for_provenance_candidate_invariants"]


def test_runtime_and_integration_options_are_deferred() -> None:
    options = _load_json(PHASE_FIXTURE_PATH)["options"]
    assert options["option_a"]["recommendation"] == "defer"
    assert options["option_c"]["recommendation"] == "defer"
    assert options["option_d"]["recommendation"] == "defer"
    assert options["option_e"]["recommendation"] == "acceptable_fallback"


def test_phase_23_approval_question_preserves_forbidden_scope() -> None:
    question = _load_json(PHASE_FIXTURE_PATH)["phase_23_approval_question"]
    assert "test-only hardening lane" in question
    assert "runtime implementation" in question
    assert "lima/ changes" in question
    assert "tests/support/ changes" in question
    assert "Sparkbot wiring" in question
    assert "HumanInput runtime bridge behavior" in question
    assert "physical-world action" in question


def test_phase_document_matches_recommendation_and_gate() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "test-only hardening lane for provenance and candidate invariants" in phase_doc
    assert "This phase is docs/tests/fixtures only" in phase_doc
    assert "does not modify `lima/`" in phase_doc
    assert "Do you approve Phase 23" in phase_doc


def test_no_phase_22_3_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_22_3*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_22_3*"))
