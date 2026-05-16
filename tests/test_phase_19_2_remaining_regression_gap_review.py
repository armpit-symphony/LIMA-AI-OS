"""Static checks for Phase 19.2 remaining regression gap review."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_19_2_REMAINING_REGRESSION_GAP_REVIEW.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_19_2_remaining_regression_gap_review.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_docs_tests_fixtures_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "19.2"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False


def test_remaining_gaps_are_explicit() -> None:
    gaps = set(_load_json(PHASE_FIXTURE_PATH)["remaining_gaps"])
    assert "no_new_runtime_slice_defined" in gaps
    assert "static_tests_are_not_runtime_monitors" in gaps
    assert "synthetic_fixtures_do_not_exercise_live_adapters_or_external_services" in gaps
    assert "future_integration_behavior_requires_separate_design" in gaps
    assert "phase_5_humaninput_runtime_bridge_remains_gated" in gaps


def test_gap_treatment_blocks_direct_runtime_expansion() -> None:
    treatment = set(_load_json(PHASE_FIXTURE_PATH)["gap_treatment"])
    assert "do_not_proceed_directly_to_runtime_expansion" in treatment
    assert "allow_future_no_code_design_lane_if_explicitly_approved" in treatment
    assert "keep_sparkbot_and_robo_os_boundary_planning_separate" in treatment


def test_phase_document_keeps_integration_lanes_separate() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "Sparkbot and Robo-OS integration boundaries remain planning topics" in phase_doc
    assert "Phase 5 HumanInput runtime bridge behavior remains gated" in phase_doc
    assert "does not approve Phase 20" in phase_doc


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["humaninput_runtime_bridge_added"] is False
    assert boundary["live_adapter_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True
    assert boundary["phase_20_approved"] is False


def test_no_phase_nineteen_two_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_19_2*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_19_2*"))
