"""Phase 34 next-lane decision matrix tests for Phase 33.3."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_33_3_PHASE_34_NEXT_LANE_DECISION_MATRIX.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_33_3_phase_34_next_lane_decision_matrix.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_33_3_is_docs_tests_fixtures_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "33.3"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_implementation_approved"] is False
    assert fixture["runtime_files_changed"] == []
    assert fixture["tests_support_changed"] is False
    assert "does not implement runtime behavior" in phase_doc


def test_phase_33_3_evidence_supports_archive_not_runtime_work() -> None:
    evidence = _load_json(PHASE_FIXTURE_PATH)["phase_33_evidence"]
    assert evidence["phase_32_audit_passed"] is True
    assert evidence["nested_suspicious_metadata_fixtures_added"] is True
    assert evidence["nested_metadata_regression_tests_added"] is True
    assert evidence["runtime_state_gap_found"] is False
    assert evidence["runtime_behavior_changed"] is False


def test_phase_33_3_recommends_phase_34_audit_archive() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert (
        fixture["recommended_phase_34_direction"]
        == "docs_tests_fixtures_only_audit_archive_for_phase_33_hardening"
    )
    assert fixture["immediate_runtime_implementation_recommended"] is False


def test_phase_33_3_reviews_all_requested_phase_34_options() -> None:
    options = _load_json(PHASE_FIXTURE_PATH)["phase_34_options"]
    assert set(options) == {"A", "B", "C", "D", "E", "F", "G"}
    assert options["A"] == "docs_tests_fixtures_only_audit_archive_for_phase_33_hardening"
    assert options["G"] == "request_phil_approval_for_future_runtime_implementation_only_if_supported"


def test_phase_33_3_preserves_phase_34_approval_question() -> None:
    question = _load_json(PHASE_FIXTURE_PATH)["approval_question"]
    assert question.startswith("Do you approve Phase 34 as a docs/tests/fixtures-only audit/archive lane")
    assert "no runtime implementation" in question
    assert "no new `lima/` changes" in question
    assert "no `tests/support/` changes" in question
    assert "no Sparkbot wiring" in question
    assert "no HumanInput runtime bridge behavior" in question
    assert "no hidden side effects" in question


def test_no_phase_33_3_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_33_3*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_33_3*"))
