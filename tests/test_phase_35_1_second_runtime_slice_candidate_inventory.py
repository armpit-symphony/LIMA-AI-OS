"""Second runtime slice candidate inventory tests for Phase 35.1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_35_1_SECOND_RUNTIME_SLICE_CANDIDATE_INVENTORY.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_35_1_second_runtime_slice_candidate_inventory.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_35_1_reviews_all_candidate_options() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "35.1"
    assert len(fixture["candidate_options_reviewed"]) == 8
    for option in ("A_", "B_", "C_", "D_", "E_", "F_", "G_", "H_"):
        assert any(candidate.startswith(option) for candidate in fixture["candidate_options_reviewed"])


def test_phase_35_1_keeps_inventory_no_code_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_implementation_approved"] is False
    assert fixture["runtime_files_changed_in_phase_35"] == []
    assert "Phase 35 does not touch it" in phase_doc


def test_leading_candidate_is_non_executing_preview_only() -> None:
    leading = _load_json(PHASE_FIXTURE_PATH)["leading_future_candidate"]
    assert leading["option"] == "C"
    assert leading["implementation_approved_now"] is False
    assert leading["deterministic"] is True
    assert leading["local_only"] is True
    assert leading["read_only"] is True
    assert leading["non_authoritative"] is True
    assert leading["non_executing"] is True
    assert leading["caller_provided_data_only"] is True
    assert leading["safe_by_default"] is True


def test_authority_adjacent_options_are_not_implementation_candidates() -> None:
    rejected = set(_load_json(PHASE_FIXTURE_PATH)["rejected_for_phase_36_implementation_without_more_evidence"])
    assert "D_read_only_candidate_status_normalization_wrapper" in rejected
    assert "E_guardiandecision_read_only_preview_planning_only" in rejected
    assert "F_humaninput_bridge_boundary_planning_only" in rejected
    assert "G_sparkbot_integration_boundary_planning_only" in rejected


def test_possible_future_file_scope_is_explicit_but_not_touched() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    scope = fixture["possible_future_phase_36_file_scope_to_evaluate_only"]
    assert "lima/kernel/candidate_preview.py" in scope
    assert "lima/kernel/__init__.py_if_safe_public_export_required" in scope
    assert fixture["runtime_implementation_approved"] is False
    assert fixture["runtime_files_changed_in_phase_35"] == []


def test_no_phase_35_1_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_35_1*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_35_1*"))
