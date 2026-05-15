"""Static checks for Phase 17.3 next-lane decision matrix."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_17_3_NEXT_LANE_DECISION_MATRIX.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_17_3_next_lane_decision_matrix.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_decision_matrix_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "17.3"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False


def test_all_phase_eighteen_options_are_evaluated() -> None:
    options = {entry["option"]: entry for entry in _load_json(PHASE_FIXTURE_PATH)["options"]}
    assert set(options) == {"A", "B", "C", "D", "E"}
    assert options["A"]["lane"] == "no_code_design_lane_for_next_narrow_runtime_slice"
    assert options["B"]["lane"] == "test_only_regression_hardening_lane"
    assert options["C"]["lane"] == "sparkbot_integration_boundary_planning"
    assert options["D"]["lane"] == "robo_os_physical_world_boundary_planning"
    assert options["E"]["lane"] == "pause_and_preserve_current_runtime_test_state"


def test_recommended_next_lane_is_test_only_regression_hardening() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["recommended_phase_18_direction"] == "test_only_regression_hardening_lane"
    options = {entry["option"]: entry for entry in fixture["options"]}
    assert options["B"]["recommendation"] == "recommended"
    assert options["B"]["risk"] == "lowest_active_next_step"


def test_phase_eighteen_requires_explicit_approval() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase_18_requires_explicit_phil_approval"] is True
    not_approved = set(fixture["not_approved_by_this_phase"])
    assert "runtime_implementation" in not_approved
    assert "lima_changes" in not_approved
    assert "tests_support_changes" in not_approved
    assert "sparkbot_wiring" in not_approved
    assert "humaninput_runtime_bridge" in not_approved
    assert "execution" in not_approved
    assert "audit_persistence" in not_approved
    assert "physical_world_behavior" in not_approved


def test_phase_document_preserves_phase_eighteen_gate() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "Option B is the safest active next lane" in phase_doc
    assert "does not approve runtime implementation" in phase_doc
    assert "Phase 18 requires explicit Phil approval" in phase_doc
    assert "without runtime expansion" in phase_doc


def test_no_phase_seventeen_three_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_17_3*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_17_3*"))
