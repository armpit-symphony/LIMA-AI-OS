"""Remaining gap review tests for Phase 24.2."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_24_2_REMAINING_CANDIDATE_INVARIANT_GAP_REVIEW.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_24_2_remaining_candidate_invariant_gap_review.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_24_2_is_docs_tests_fixtures_only_gap_review() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "24.2"
    assert fixture["runtime_code_modified"] is False
    assert fixture["gap_result"] == "planning_inputs_only"
    assert "docs/tests/fixtures-only gap review" in phase_doc
    assert "does not implement runtime behavior" in phase_doc


def test_remaining_gaps_are_named_as_planning_inputs() -> None:
    gaps = set(_load_json(PHASE_FIXTURE_PATH)["remaining_gaps"])
    assert "broader_nested_provenance_fixture_matrix" in gaps
    assert "cross_api_candidate_regression_matrix" in gaps
    assert "static_import_and_call_pattern_review" in gaps
    assert "replay_staleness_timestamp_lineage_matrix" in gaps
    assert "future_no_code_next_runtime_slice_design_question" in gaps


def test_gap_review_does_not_approve_forbidden_scope() -> None:
    not_approved = set(_load_json(PHASE_FIXTURE_PATH)["not_approved"])
    assert "runtime_implementation" in not_approved
    assert "lima_changes" in not_approved
    assert "tests_support_changes" in not_approved
    assert "sparkbot_integration" in not_approved
    assert "humaninput_runtime_bridge" in not_approved
    assert "live_adapter" in not_approved
    assert "approval_enforcement" in not_approved
    assert "execution" in not_approved
    assert "dispatch" in not_approved
    assert "audit_persistence" in not_approved
    assert "physical_world_behavior" in not_approved


def test_boundary_results_show_no_forbidden_behavior() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["humaninput_runtime_bridge_added"] is False
    assert boundary["live_adapter_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["approval_enforcement_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_behavior_added"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True


def test_phase_doc_gates_phase_24_3_and_runtime_expansion() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "Phase 24.3 may evaluate next-lane options only" in phase_doc
    assert "Runtime expansion remains blocked" in phase_doc


def test_no_phase_24_2_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_24_2*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_24_2*"))
