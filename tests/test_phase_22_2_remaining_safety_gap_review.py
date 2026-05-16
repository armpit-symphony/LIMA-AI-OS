"""Static safety gap review checks for Phase 22.2."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_22_2_REMAINING_SAFETY_GAP_REVIEW.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_22_2_remaining_safety_gap_review.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_22_2_is_docs_tests_fixtures_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "22.2"
    assert fixture["runtime_code_modified"] is False
    assert fixture["boundary_results"]["lima_modified"] is False
    assert fixture["boundary_results"]["tests_support_modified"] is False


def test_remaining_safety_gaps_are_test_or_planning_gaps() -> None:
    gaps = set(_load_json(PHASE_FIXTURE_PATH)["remaining_safety_gaps"])
    assert "nested_provenance_authority_claim_fixture_coverage" in gaps
    assert "shared_construction_normalization_validation_regression_matrix" in gaps
    assert "broader_static_forbidden_pattern_tests" in gaps
    assert "separate_sparkbot_and_robo_os_boundary_planning" in gaps


def test_non_gaps_rule_out_immediate_runtime_work() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["recommended_gap_response"] == "test_only_hardening_before_any_runtime_expansion"
    assert "no_immediate_runtime_work_needed" in fixture["non_gaps"]
    assert "candidate_provenance_slice_remains_non_executing" in fixture["non_gaps"]


def test_phase_document_does_not_approve_phase_23() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "docs/tests/fixtures only" in phase_doc
    assert "No immediate runtime work is needed" in phase_doc
    assert "does not approve Phase 23" in phase_doc
    assert "does not modify `lima/`" in phase_doc


def test_boundary_results_remain_closed() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
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


def test_no_phase_22_2_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_22_2*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_22_2*"))
