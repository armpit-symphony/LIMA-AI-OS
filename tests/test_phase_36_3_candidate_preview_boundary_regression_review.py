"""Candidate preview boundary regression review tests for Phase 36.3."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_36_3_CANDIDATE_PREVIEW_BOUNDARY_REGRESSION_REVIEW.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_36_3_candidate_preview_boundary_regression_review.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_36_3_adds_no_new_runtime_behavior() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "36.3"
    assert fixture["runtime_behavior_added_in_phase_36_3"] is False
    assert fixture["runtime_files_changed_in_phase_36_3"] == []
    assert "does not add new runtime behavior" in phase_doc


def test_phase_36_2_runtime_scope_was_exact() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase_36_2_approved_runtime_files_changed"] == [
        "lima/kernel/candidate_preview.py",
        "lima/kernel/__init__.py",
    ]
    assert fixture["phase_36_2_forbidden_runtime_files_changed"] == []
    assert fixture["runtime_state_py_changed"] is False
    assert fixture["intake_candidate_py_changed"] is False
    assert fixture["candidate_status_py_changed"] is False
    assert fixture["tests_support_changed"] is False


def test_candidate_preview_safety_evidence_is_preserved() -> None:
    evidence = _load_json(PHASE_FIXTURE_PATH)["candidate_preview_safety_evidence"]
    assert all(evidence.values())
    assert evidence["deterministic"] is True
    assert evidence["local_only"] is True
    assert evidence["read_only"] is True
    assert evidence["non_authoritative"] is True
    assert evidence["non_executing"] is True
    assert evidence["side_effect_free"] is True


def test_stale_phase_35_test_adjustment_is_documented_and_narrow() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["stale_phase_35_test_adjusted"] is True
    assert (
        fixture["stale_phase_35_test_adjusted_file"]
        == "tests/test_phase_35_1_second_runtime_slice_candidate_inventory.py"
    )
    assert "absolute non-existence assertion stale" in fixture[
        "stale_phase_35_test_adjustment_reason"
    ]
    assert fixture["other_old_phase_tests_changed"] is False


def test_no_phase_36_3_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_36_3*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_36_3*"))
