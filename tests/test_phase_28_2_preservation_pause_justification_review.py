"""Preservation pause justification review tests for Phase 28.2."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_28_2_PRESERVATION_PAUSE_JUSTIFICATION_REVIEW.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_28_2_preservation_pause_justification_review.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_28_2_is_pause_justification_review_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "28.2"
    assert fixture["runtime_code_modified"] is False
    assert "pause justification review only" in phase_doc
    assert "does not implement runtime behavior" in phase_doc


def test_pause_review_does_not_find_specific_pause_risk() -> None:
    review = _load_json(PHASE_FIXTURE_PATH)["pause_review"]
    assert review["current_state_stable_and_preserved"] is True
    assert review["concrete_phase_29_test_only_gap_found"] is False
    assert review["specific_documented_risk_requires_continued_pause"] is False
    assert review["continued_pause_safe_but_not_default_recommendation"] is True
    assert "no specific documented risk requires another automatic preservation pause" in (
        PHASE_DOC_PATH.read_text(encoding="utf-8").lower()
    )


def test_phase_29_implication_is_no_code_design_not_runtime() -> None:
    implication = _load_json(PHASE_FIXTURE_PATH)["phase_29_implication"]
    assert implication["recommended_direction"] == (
        "docs_tests_fixtures_only_no_code_design_review_for_next_narrow_runtime_slice"
    )
    assert implication["runtime_implementation_approved"] is False
    assert implication["lima_changes_allowed"] is False
    assert implication["tests_support_changes_allowed"] is False
    assert implication["phase_5_runtime_bridge_remains_gated"] is True


def test_forbidden_scope_remains_preserved() -> None:
    forbidden = set(_load_json(PHASE_FIXTURE_PATH)["forbidden_scope_preserved"])
    assert "runtime_behavior" in forbidden
    assert "sparkbot_wiring" in forbidden
    assert "humaninput_runtime_bridge" in forbidden
    assert "live_adapters" in forbidden
    assert "approval_enforcement" in forbidden
    assert "execution" in forbidden
    assert "dispatch" in forbidden
    assert "audit_persistence" in forbidden
    assert "physical_world_behavior" in forbidden


def test_next_phase_is_phase_29_decision_readiness_matrix() -> None:
    assert _load_json(PHASE_FIXTURE_PATH)["next_phase"] == "28.3"
    assert "Continue only to Phase 28.3" in PHASE_DOC_PATH.read_text(encoding="utf-8")


def test_no_phase_28_2_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_28_2*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_28_2*"))
