"""Preservation audit charter tests for Phase 27.0."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_27_0_PHASE_26_PRESERVATION_AUDIT_CHARTER.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_27_0_phase_26_preservation_audit_charter.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_27_0_is_preservation_audit_charter_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "27.0"
    assert fixture["runtime_code_modified"] is False
    assert "preservation audit charter only" in phase_doc
    assert "does not implement runtime behavior" in phase_doc


def test_phase_26_0_through_26_4_are_in_audit_scope() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["audited_phases"] == ["26.0", "26.1", "26.2", "26.3", "26.4"]
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    for phase in fixture["audited_phases"]:
        assert f"Phase {phase}" in phase_doc


def test_preservation_intent_keeps_runtime_gated() -> None:
    intent = set(_load_json(PHASE_FIXTURE_PATH)["preservation_intent"])
    assert "pause_before_runtime_expansion" in intent
    assert "preserve_current_known_good_runtime_test_state" in intent
    assert "keep_small_runtime_slice_non_executing" in intent
    assert "keep_phase_5_runtime_bridge_gated" in intent


def test_phase_27_lane_is_defined() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase_27_lane"] == [
        "27.0_preservation_audit_charter",
        "27.1_current_runtime_test_state_preservation_record",
        "27.2_gated_runtime_boundary_review",
        "27.3_next_lane_risk_decision_matrix",
        "27.4_preservation_archive_closeout",
    ]
    assert fixture["next_phase"] == "27.1"


def test_boundary_results_preserve_no_forbidden_behavior() -> None:
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


def test_no_phase_27_0_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_27_0*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_27_0*"))
