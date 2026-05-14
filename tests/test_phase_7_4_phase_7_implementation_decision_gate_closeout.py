"""Static checks for Phase 7.4 implementation decision gate closeout."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_7_4_PHASE_7_IMPLEMENTATION_DECISION_GATE_CLOSEOUT.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_7_4_phase_7_implementation_decision_gate_closeout.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_declares_implementation_decision_gate_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "7.4"
    assert fixture["non_runtime"] is True
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["implementation_decision_gate_closeout_only"] is True


def test_completed_phase_seven_scope_lists_prior_phases() -> None:
    completed = _load_json(PHASE_FIXTURE_PATH)["completed_phase_7_scope"]
    assert completed == [
        "phase_7_0_kernel_runtime_implementation_charter",
        "phase_7_1_first_runtime_slice_eligibility_map",
        "phase_7_2_kernel_runtime_safety_preconditions",
        "phase_7_3_runtime_implementation_test_plan",
    ]


def test_phase_seven_decisions_keep_runtime_slice_narrow_and_test_gated() -> None:
    decisions = _load_json(PHASE_FIXTURE_PATH)["phase_7_decisions"]
    assert decisions["smallest_future_runtime_slice"] == "non_executing_kernel_intake_to_candidate_coordinator"
    assert decisions["eligible_files_are_future_candidates_only"] is True
    assert decisions["forbidden_execution_surfaces_remain_blocked"] is True
    assert decisions["targeted_tests_required_before_runtime_code"] is True
    assert decisions["negative_tests_required_before_runtime_code"] is True
    assert decisions["rollback_expectations_required"] is True
    assert decisions["audit_proof_required"] is True
    assert decisions["positive_tests_limited_to_non_executable_candidate_metadata"] is True


def test_unimplemented_list_keeps_all_runtime_surfaces_closed() -> None:
    unimplemented = set(_load_json(PHASE_FIXTURE_PATH)["unimplemented"])
    assert "runtime_behavior" in unimplemented
    assert "lima_changes" in unimplemented
    assert "tests_support_changes" in unimplemented
    assert "helper_behavior_changes" in unimplemented
    assert "sparkbot_import_or_wiring" in unimplemented
    assert "live_adapter" in unimplemented
    assert "runtime_humaninput_to_intentenvelope_bridge" in unimplemented
    assert "approval_enforcement" in unimplemented
    assert "execution" in unimplemented
    assert "audit_persistence" in unimplemented
    assert "shell_browser_network_file_mutation_robotics_physical_world_side_effects" in unimplemented


def test_decision_options_require_explicit_phil_approval() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    options = set(fixture["implementation_decision_options"])
    assert fixture["requires_explicit_phil_approval_before_runtime_code"] is True
    assert fixture["phase_5_runtime_bridge_remains_gated"] is True
    assert "stop_phase_7_and_audit_archive_no_code_charter_lane" in options
    assert "phase_8_no_code_implementation_design_review" in options
    assert "narrow_first_runtime_slice_implementation_limited_to_phase_7_1_eligible_files_and_phase_7_2_7_3_preconditions" in options
    assert "sparkbot_integration_boundary_planning" in options
    assert "robo_os_physical_world_boundary_planning" in options
    assert "pause_and_preserve_current_state" in options


def test_not_ready_for_blocks_unapproved_phase_eight_and_runtime_work() -> None:
    blocked = set(_load_json(PHASE_FIXTURE_PATH)["not_ready_for"])
    assert "phase_8_without_explicit_approval" in blocked
    assert "runtime_behavior" in blocked
    assert "lima_changes" in blocked
    assert "tests_support_changes" in blocked
    assert "sparkbot_import_or_wiring" in blocked
    assert "approval_enforcement" in blocked
    assert "execution" in blocked
    assert "audit_persistence" in blocked
    assert "shell_browser_network_file_mutation_robotics_physical_world_side_effects" in blocked


def test_doc_stops_at_explicit_implementation_decision_gate() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "It is docs/tests/fixtures only" in phase_doc
    assert "does not implement runtime behavior" in phase_doc
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "Phil must explicitly choose the next step" in phase_doc
    assert "No Phase 8" in phase_doc


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["runtime_behavior_added"] is False
    assert boundary["files_under_lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["helper_behavior_changed"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["intentcompiler_runtime_changed"] is False
    assert boundary["guardiandecision_runtime_changed"] is False
    assert boundary["execution_added"] is False
    assert boundary["physical_world_action_added"] is False


def test_no_phase_seven_four_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_7_4*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_7_4*"))
