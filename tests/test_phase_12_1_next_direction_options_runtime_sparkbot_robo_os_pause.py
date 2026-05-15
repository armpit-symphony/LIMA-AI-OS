"""Static checks for Phase 12.1 next-direction options."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_12_1_NEXT_DIRECTION_OPTIONS_RUNTIME_SPARKBOT_ROBO_OS_PAUSE.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_12_1_next_direction_options_runtime_sparkbot_robo_os_pause.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_docs_tests_fixtures_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "12.1"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False


def test_all_expected_options_are_reviewed_without_implementation_approval() -> None:
    options = _load_json(PHASE_FIXTURE_PATH)["options_reviewed"]
    names = {option["name"] for option in options}
    assert names == {
        "pause_and_preserve",
        "future_narrow_runtime_slice_design",
        "sparkbot_integration_boundary_planning",
        "robo_os_physical_world_boundary_planning",
        "threat_model_security_test_strengthening",
    }
    assert all(option["implementation_approved"] is False for option in options)


def test_directional_finding_prefers_threat_model_before_any_lane() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["directional_finding"] == "continue_to_threat_model_and_safety_gap_review"
    assert fixture["next_phase"] == "phase_12_2_threat_model_and_safety_gap_review"


def test_not_approved_list_blocks_runtime_and_integration() -> None:
    not_approved = set(_load_json(PHASE_FIXTURE_PATH)["not_approved"])
    assert "runtime_implementation" in not_approved
    assert "sparkbot_wiring" in not_approved
    assert "robo_os_driver_behavior" in not_approved
    assert "humaninput_runtime_bridge" in not_approved
    assert "live_adapter" in not_approved
    assert "approval_enforcement" in not_approved
    assert "execution" in not_approved
    assert "dispatch" in not_approved
    assert "audit_persistence" in not_approved
    assert "physical_world_action" in not_approved


def test_phase_document_says_options_are_planning_only() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "docs/tests/fixtures only" in phase_doc
    assert "without imports, wiring, or production integration" in phase_doc
    assert "simulation-first and approval-blocked by default" in phase_doc
    assert "should not begin as integration work" in phase_doc


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


def test_no_phase_twelve_one_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_12_1*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_12_1*"))
