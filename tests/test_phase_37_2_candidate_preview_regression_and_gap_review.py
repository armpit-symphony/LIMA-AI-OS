"""Candidate preview regression and gap review tests for Phase 37.2."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_37_2_CANDIDATE_PREVIEW_REGRESSION_AND_GAP_REVIEW.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_37_2_candidate_preview_regression_and_gap_review.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_37_2_adds_no_runtime_behavior() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "37.2"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_behavior_added_in_phase_37_2"] is False
    assert fixture["runtime_files_changed_in_phase_37_2"] == []
    assert "does not modify `lima/`" in phase_doc


def test_regression_and_blocking_gap_are_absent() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["regression_found"] is False
    assert fixture["blocking_gap_found"] is False
    assert fixture["runtime_change_needed"] is False
    assert fixture["lima_change_needed"] is False
    assert fixture["tests_support_change_needed"] is False
    assert fixture["stale_prior_phase_test_adjustment_needed"] is False
    assert fixture["forbidden_behavior_needed"] is False


def test_candidate_preview_properties_remain_preserved() -> None:
    properties = _load_json(PHASE_FIXTURE_PATH)["candidate_preview_properties_preserved"]
    assert all(properties.values())
    assert properties["non_authoritative"] is True
    assert properties["non_executing"] is True
    assert properties["side_effect_free"] is True


def test_no_immediate_test_only_hardening_need_is_recorded() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["immediate_hardening_needed"] is False
    assert "concrete future gap" in fixture["potential_future_hardening"]


def test_no_phase_37_2_files_exist_under_lima_tests_support_or_old_phase_tests() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_37_2*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_37_2*"))
    assert not list((REPO_ROOT / "tests").glob("test_phase_35_*phase_37_2*"))
