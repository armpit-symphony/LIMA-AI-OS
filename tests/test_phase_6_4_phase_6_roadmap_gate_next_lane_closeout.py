"""Static checks for Phase 6.4 roadmap gate and next-lane closeout."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_6_4_PHASE_6_ROADMAP_GATE_NEXT_LANE_CLOSEOUT.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_6_4_phase_6_roadmap_gate_next_lane_closeout.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_declares_roadmap_gate_closeout_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "6.4"
    assert fixture["non_runtime"] is True
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["roadmap_gate_closeout_only"] is True


def test_completed_phase_six_scope_lists_all_prior_planning_phases() -> None:
    completed = _load_json(PHASE_FIXTURE_PATH)["completed_phase_6_scope"]
    assert completed == [
        "phase_6_0_post_phase_5_roadmap_reorientation",
        "phase_6_1_lima_kernel_lifecycle_planning",
        "phase_6_2_intentenvelope_guardiandecision_lifecycle_boundary_map",
        "phase_6_3_approval_audit_memory_boundary_planning",
    ]


def test_planned_boundaries_keep_kernel_candidates_and_guardian_separate() -> None:
    boundaries = _load_json(PHASE_FIXTURE_PATH)["planned_boundaries"]
    assert boundaries["lima_runtime_kernel_under_shells_and_drivers"] is True
    assert boundaries["humaninput_intent_context_not_execution_permission"] is True
    assert boundaries["intentenvelope_candidates_non_executable"] is True
    assert boundaries["intentenvelope_candidates_cannot_authorize_themselves"] is True
    assert boundaries["guardiandecision_future_authority_not_implemented"] is True
    assert boundaries["approval_state_descriptive_only"] is True


def test_phase_six_closeout_keeps_runtime_surfaces_unimplemented() -> None:
    unimplemented = set(_load_json(PHASE_FIXTURE_PATH)["unimplemented"])
    assert "runtime_humaninput_to_intentenvelope_bridge" in unimplemented
    assert "live_adapter_behavior" in unimplemented
    assert "runtime_intentcompiler_behavior" in unimplemented
    assert "runtime_guardiandecision_behavior" in unimplemented
    assert "approval_enforcement" in unimplemented
    assert "audit_persistence" in unimplemented
    assert "memory_io" in unimplemented
    assert "robo_os_physical_world_behavior" in unimplemented


def test_next_scope_options_require_operator_selection() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    options = set(fixture["next_scope_options"])
    assert fixture["requires_explicit_phil_approval_before_next_phase"] is True
    assert fixture["no_phase_6_5_or_phase_7_approved"] is True
    assert "stop_phase_6_and_audit_archive_planning_lane" in options
    assert "docs_tests_fixtures_only_sparkbot_integration_boundary_planning" in options
    assert "docs_tests_fixtures_only_robo_os_physical_world_boundary_planning" in options
    assert "docs_tests_fixtures_only_kernel_runtime_implementation_charter_no_code" in options
    assert "broader_sparkpit_labs_product_roadmap_planning" in options


def test_not_ready_for_blocks_runtime_and_side_effecting_work() -> None:
    blocked = set(_load_json(PHASE_FIXTURE_PATH)["not_ready_for"])
    assert "runtime_behavior" in blocked
    assert "helper_behavior_changes" in blocked
    assert "sparkbot_import_or_wiring" in blocked
    assert "real_intentcompiler" in blocked
    assert "real_guardiandecision" in blocked
    assert "approval_enforcement" in blocked
    assert "execution" in blocked
    assert "audit_persistence" in blocked
    assert "memory_io" in blocked
    assert "physical_world_action" in blocked


def test_doc_declares_no_next_phase_is_approved() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "does not implement runtime behavior" in phase_doc
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "No Phase 6.5 or Phase 7 work is approved" in phase_doc
    assert "Phil must explicitly choose the next lane" in phase_doc
    assert "remain blocked until Phil explicitly approves a new scope" in phase_doc


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["runtime_behavior_added"] is False
    assert boundary["files_under_lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["helper_behavior_changed"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["intentcompiler_runtime_changed"] is False
    assert boundary["guardiandecision_runtime_changed"] is False
    assert boundary["approval_enforcement_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["memory_io_added"] is False
    assert boundary["physical_world_action_added"] is False


def test_no_phase_six_four_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_6_4*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_6_4*"))
