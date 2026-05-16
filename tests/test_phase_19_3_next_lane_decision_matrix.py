"""Static checks for Phase 19.3 next-lane decision matrix."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_19_3_NEXT_LANE_DECISION_MATRIX.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_19_3_next_lane_decision_matrix.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_docs_tests_fixtures_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "19.3"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False


def test_all_phase_twenty_options_are_evaluated() -> None:
    options = _load_json(PHASE_FIXTURE_PATH)["evaluated_options"]
    assert set(options) == {"option_a", "option_b", "option_c", "option_d", "option_e"}
    assert options["option_a"]["direction"] == "no_code_design_lane_for_next_narrow_runtime_slice"
    assert options["option_b"]["direction"] == "additional_test_only_regression_hardening"
    assert options["option_c"]["direction"] == "sparkbot_integration_boundary_planning"
    assert options["option_d"]["direction"] == "robo_os_physical_world_boundary_planning"
    assert options["option_e"]["direction"] == "pause_and_preserve_current_runtime_test_state"


def test_recommended_direction_is_no_code_design_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert (
        fixture["recommended_phase_20_direction"]
        == "docs_tests_fixtures_only_no_code_design_lane_for_next_narrow_runtime_slice"
    )
    assert fixture["phase_20_implementation_approved"] is False
    assert fixture["phase_20_requires_explicit_phil_approval"] is True


def test_phase_document_preserves_phase_twenty_approval_boundary() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "does not approve runtime implementation" in phase_doc
    assert "Phase 20 must still require explicit Phil approval" in phase_doc
    assert "must forbid runtime implementation" in phase_doc
    assert "HumanInput runtime bridge behavior" in phase_doc


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


def test_no_phase_nineteen_three_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_19_3*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_19_3*"))
