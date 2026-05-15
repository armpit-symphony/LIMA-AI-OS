"""Static checks for Phase 12.3 next lane recommendation matrix."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_12_3_NEXT_LANE_RECOMMENDATION_MATRIX.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_12_3_next_lane_recommendation_matrix.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_docs_tests_fixtures_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "12.3"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False


def test_matrix_includes_all_phase_twelve_options() -> None:
    options = {entry["option"] for entry in _load_json(PHASE_FIXTURE_PATH)["recommendation_matrix"]}
    assert options == {
        "pause_and_preserve",
        "future_runtime_slice_design",
        "sparkbot_boundary_planning",
        "robo_os_physical_world_planning",
        "threat_model_derived_test_planning",
    }


def test_only_threat_model_test_planning_is_recommended_next() -> None:
    matrix = _load_json(PHASE_FIXTURE_PATH)["recommendation_matrix"]
    recommended = [entry for entry in matrix if entry["recommendation"] == "recommended_next"]
    assert recommended == [
        {
            "option": "threat_model_derived_test_planning",
            "recommendation": "recommended_next",
            "implementation_approved": False,
        }
    ]
    assert all(entry["implementation_approved"] is False for entry in matrix)


def test_explicit_non_recommendations_block_runtime_and_integration() -> None:
    blocked = set(_load_json(PHASE_FIXTURE_PATH)["explicit_non_recommendations"])
    assert "runtime_implementation" in blocked
    assert "sparkbot_wiring" in blocked
    assert "humaninput_runtime_bridge" in blocked
    assert "robo_os_driver_behavior" in blocked
    assert "live_adapter" in blocked
    assert "approval_enforcement" in blocked
    assert "execution" in blocked
    assert "dispatch" in blocked
    assert "audit_persistence" in blocked
    assert "shell_browser_network_file_mutation_robotics_physical_world_action" in blocked


def test_phase_document_records_matrix_and_gate() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "Recommendation Matrix" in phase_doc
    assert "Threat-model-derived test planning" in phase_doc
    assert "does not modify `lima/`" in phase_doc
    assert "does not wire Sparkbot" in phase_doc
    assert "does not execute" in phase_doc
    assert "Phase 12.4 should close Phase 12 at a decision gate" in phase_doc


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["humaninput_runtime_bridge_added"] is False
    assert boundary["live_adapter_added"] is False
    assert boundary["approval_enforcement_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False


def test_no_phase_twelve_three_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_12_3*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_12_3*"))
