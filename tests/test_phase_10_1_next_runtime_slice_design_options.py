"""Static checks for Phase 10.1 next runtime slice design options."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_10_1_NEXT_RUNTIME_SLICE_DESIGN_OPTIONS.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_10_1_next_runtime_slice_design_options.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_no_code_design_options_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "10.1"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False
    assert fixture["recommended_future_slice"]["runtime_implementation_approved_now"] is False


def test_all_requested_options_are_evaluated_without_approval() -> None:
    options = {option["id"]: option for option in _load_json(PHASE_FIXTURE_PATH)["evaluated_options"]}
    assert set(options) == {
        "candidate_validation",
        "candidate_status_normalization",
        "candidate_lifecycle_metadata",
        "intake_error_taxonomy",
        "provenance_hardening",
        "no_further_runtime_work_yet",
    }
    assert all(option["runtime_implementation_approved"] is False for option in options.values())


def test_recommended_slice_remains_non_executing_and_requires_phase_eleven_approval() -> None:
    recommended = _load_json(PHASE_FIXTURE_PATH)["recommended_future_slice"]
    assert recommended["id"] == "candidate_validation_and_status_normalization"
    assert recommended["phase_11_approval_required"] is True
    assert recommended["must_remain_non_executing"] is True
    assert recommended["must_preserve_phase_5_runtime_bridge_gate"] is True
    assert recommended["must_keep_execution_allowed_false"] is True
    assert recommended["must_keep_side_effects_allowed_false"] is True
    assert recommended["must_keep_approval_state_never_approved"] is True


def test_forbidden_behaviors_remain_blocked() -> None:
    forbidden = set(_load_json(PHASE_FIXTURE_PATH)["forbidden_behavior"])
    assert "humaninput_runtime_bridge" in forbidden
    assert "sparkbot_wiring" in forbidden
    assert "live_adapter" in forbidden
    assert "intentcompiler_runtime_behavior" in forbidden
    assert "guardiandecision_runtime_behavior" in forbidden
    assert "approval_enforcement" in forbidden
    assert "execution" in forbidden
    assert "dispatch" in forbidden
    assert "audit_persistence" in forbidden
    assert "shell_browser_network_file_mutation_robotics_physical_world_behavior" in forbidden


def test_phase_document_states_design_only_and_no_phase_eleven_approval() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "no-code design phase only" in phase_doc
    assert "No Phase 11 runtime implementation is approved" in phase_doc
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc


def test_next_phase_is_file_touch_map() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["next_phase"] == "phase_10_2_exact_file_touch_map_for_next_runtime_slice"


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["helper_behavior_changed"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["live_adapter_added"] is False
    assert boundary["approval_enforcement_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False


def test_no_phase_ten_one_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_10_1*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_10_1*"))
