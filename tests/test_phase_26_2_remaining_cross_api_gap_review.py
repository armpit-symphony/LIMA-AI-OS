"""Remaining gap review tests for Phase 26.2."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_26_2_REMAINING_CROSS_API_GAP_REVIEW.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_26_2_remaining_cross_api_gap_review.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_26_2_is_gap_review_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "26.2"
    assert fixture["runtime_code_modified"] is False
    assert "gap review only" in phase_doc
    assert "does not implement runtime behavior" in phase_doc


def test_remaining_gaps_are_planning_inputs_only() -> None:
    gaps = set(_load_json(PHASE_FIXTURE_PATH)["remaining_gaps"])
    assert "broader_property_style_or_matrix_generated_fixture_sweep" in gaps
    assert "consolidated_static_forbidden_pattern_checklist" in gaps
    assert "wider_import_boundary_regression_checks" in gaps
    assert "provenance_traceability_fixture_index" in gaps
    assert "phase_27_direction_decision" in gaps
    assert "future planning inputs only" in PHASE_DOC_PATH.read_text(encoding="utf-8")


def test_gap_review_does_not_approve_forbidden_scope() -> None:
    not_approved = set(_load_json(PHASE_FIXTURE_PATH)["not_approved"])
    assert "runtime_implementation" in not_approved
    assert "lima_changes" in not_approved
    assert "tests_support_changes" in not_approved
    assert "sparkbot_wiring" in not_approved
    assert "humaninput_runtime_bridge" in not_approved
    assert "live_adapters" in not_approved
    assert "approval_enforcement" in not_approved
    assert "execution" in not_approved
    assert "dispatch" in not_approved
    assert "audit_persistence" in not_approved
    assert "physical_world_behavior" in not_approved


def test_boundary_results_preserve_phase_5_gate() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True


def test_next_phase_is_decision_matrix() -> None:
    assert _load_json(PHASE_FIXTURE_PATH)["next_phase"] == "26.3"
    assert "Continue only to Phase 26.3" in PHASE_DOC_PATH.read_text(encoding="utf-8")


def test_no_phase_26_2_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_26_2*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_26_2*"))
