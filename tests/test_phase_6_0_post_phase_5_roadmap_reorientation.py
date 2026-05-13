"""Static checks for Phase 6.0 post-Phase-5 roadmap reorientation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_6_0_POST_PHASE_5_ROADMAP_REORIENTATION.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_6_0_post_phase_5_roadmap_reorientation.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_declares_docs_tests_fixtures_only_planning() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "6.0"
    assert fixture["non_runtime"] is True
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["roadmap_planning_only"] is True


def test_phase_five_closeout_remains_archived_and_gated() -> None:
    closeout = _load_json(PHASE_FIXTURE_PATH)["phase_5_closeout_status"]
    assert closeout["phase_5_0_to_5_11_complete"] is True
    assert closeout["humaninput_bridge_design_lane_archived"] is True
    assert closeout["runtime_bridge_implementation_approved"] is False
    assert closeout["phase_5_helper_runtime_reuse_approved"] is False


def test_kernel_lifecycle_planning_is_selected_next_lane_without_implementation() -> None:
    lane = _load_json(PHASE_FIXTURE_PATH)["selected_next_architectural_lane"]
    assert lane["lane"] == "kernel_lifecycle_planning"
    assert lane["implementation_approved"] is False


def test_future_lanes_are_separated() -> None:
    lanes = set(_load_json(PHASE_FIXTURE_PATH)["future_lanes_to_separate"])
    assert {
        "kernel_lifecycle_planning",
        "intentenvelope_lifecycle",
        "guardiandecision_lifecycle",
        "approval_boundary_model",
        "audit_spine_memory_relationship",
        "sparkbot_integration_boundary",
        "robo_os_physical_world_boundary",
        "runtime_bridge_prerequisites",
    } <= lanes


def test_runtime_bridge_prerequisites_are_documented() -> None:
    prerequisites = set(_load_json(PHASE_FIXTURE_PATH)["runtime_bridge_prerequisites"])
    assert "kernel_lifecycle_boundaries" in prerequisites
    assert "intentenvelope_lifecycle_boundaries" in prerequisites
    assert "guardiandecision_lifecycle_boundaries" in prerequisites
    assert "explicit_operator_runtime_approval" in prerequisites


def test_ready_only_for_phase_six_one_planning() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["ready_for"] == [
        "phase_6_1_docs_tests_fixtures_only_kernel_lifecycle_planning"
    ]
    assert "runtime_bridge_implementation" in fixture["not_ready_for"]
    assert "real_intentcompiler" in fixture["not_ready_for"]
    assert "real_guardiandecision" in fixture["not_ready_for"]


def test_doc_keeps_runtime_and_side_effects_blocked() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "does not implement runtime behavior" in phase_doc
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "Runtime implementation remains blocked" in phase_doc


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["runtime_behavior_added"] is False
    assert boundary["files_under_lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["helper_behavior_changed"] is False
    assert boundary["runtime_bridge_added"] is False
    assert boundary["physical_world_action_added"] is False


def test_no_phase_six_zero_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_6_0*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_6_0*"))
