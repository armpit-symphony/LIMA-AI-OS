"""Static checks for Phase 7.5 no-code charter audit archive closeout."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_7_5_PHASE_7_NO_CODE_KERNEL_RUNTIME_CHARTER_AUDIT_ARCHIVE_CLOSEOUT.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_7_5_phase_7_no_code_kernel_runtime_charter_audit_archive_closeout.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_declares_audit_archive_closeout_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "7.5"
    assert fixture["non_runtime"] is True
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["audit_archive_closeout_only"] is True


def test_completed_phase_seven_scope_lists_phase_seven_zero_through_seven_four() -> None:
    completed = _load_json(PHASE_FIXTURE_PATH)["completed_phase_7_scope"]
    assert completed == [
        "phase_7_0_kernel_runtime_implementation_charter",
        "phase_7_1_first_runtime_slice_eligibility_map",
        "phase_7_2_kernel_runtime_safety_preconditions",
        "phase_7_3_runtime_implementation_test_plan",
        "phase_7_4_phase_7_implementation_decision_gate_closeout",
    ]


def test_phase_seven_archive_lists_added_artifact_types_only() -> None:
    added = set(_load_json(PHASE_FIXTURE_PATH)["added"])
    assert added == {
        "docs",
        "fixtures",
        "static_tests",
        "roadmap_state_updates",
    }


def test_phase_seven_archive_lists_runtime_surfaces_not_added() -> None:
    not_added = set(_load_json(PHASE_FIXTURE_PATH)["not_added"])
    assert "runtime_behavior" in not_added
    assert "lima_runtime_changes" in not_added
    assert "tests_support_changes" in not_added
    assert "helper_behavior_changes" in not_added
    assert "sparkbot_import_or_wiring" in not_added
    assert "live_adapter" in not_added
    assert "runtime_humaninput_to_intentenvelope_bridge" in not_added
    assert "intentcompiler_runtime_behavior" in not_added
    assert "guardiandecision_runtime_behavior" in not_added
    assert "approval_enforcement" in not_added
    assert "execution" in not_added
    assert "audit_persistence" in not_added
    assert "shell_browser_network_file_mutation_robotics_physical_world_side_effects" in not_added


def test_phase_seven_archive_keeps_runtime_and_phase_five_bridge_gated() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase_7_archived_as_no_code_charter_planning_only"] is True
    assert fixture["runtime_implementation_approved"] is False
    assert fixture["phase_5_runtime_bridge_remains_gated"] is True
    assert fixture["future_runtime_code_requires_new_explicit_phil_approval"] is True
    assert fixture["requires_explicit_phil_approval_before_next_phase"] is True


def test_next_options_are_clear_and_require_explicit_approval() -> None:
    options = set(_load_json(PHASE_FIXTURE_PATH)["recommended_next_options"])
    assert options == {
        "phase_8_no_code_implementation_design_review",
        "narrow_first_runtime_slice_implementation_later_only_after_explicit_approval",
        "sparkbot_integration_boundary_planning",
        "robo_os_physical_world_boundary_planning",
        "pause_and_preserve_current_state",
    }


def test_not_ready_for_blocks_phase_eight_and_runtime_side_effecting_work() -> None:
    blocked = set(_load_json(PHASE_FIXTURE_PATH)["not_ready_for"])
    assert "phase_8_without_explicit_approval" in blocked
    assert "runtime_behavior" in blocked
    assert "lima_changes" in blocked
    assert "tests_support_changes" in blocked
    assert "helper_behavior_changes" in blocked
    assert "sparkbot_import_or_wiring" in blocked
    assert "live_adapter_code" in blocked
    assert "runtime_humaninput_to_intentenvelope_bridge" in blocked
    assert "intentcompiler_runtime_behavior" in blocked
    assert "guardiandecision_runtime_behavior" in blocked
    assert "approval_enforcement" in blocked
    assert "execution" in blocked
    assert "audit_persistence" in blocked
    assert "shell_browser_network_file_mutation_robotics_physical_world_side_effects" in blocked


def test_doc_archives_phase_seven_and_requires_explicit_next_approval() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "Phase 7.5 archives Phase 7 as a completed no-code kernel runtime implementation charter lane" in phase_doc
    assert "does not implement runtime behavior" in phase_doc
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "Phase 7 is archived as a no-code implementation charter only" in phase_doc
    assert "Phase 5 runtime bridge work remains gated" in phase_doc
    assert "Future runtime code requires a new explicit Phil approval" in phase_doc
    assert "No Phase 8" in phase_doc


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["runtime_behavior_added"] is False
    assert boundary["files_under_lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["helper_behavior_changed"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["live_adapter_added"] is False
    assert boundary["runtime_bridge_added"] is False
    assert boundary["intentcompiler_runtime_changed"] is False
    assert boundary["guardiandecision_runtime_changed"] is False
    assert boundary["approval_enforcement_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False


def test_no_phase_seven_five_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_7_5*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_7_5*"))
