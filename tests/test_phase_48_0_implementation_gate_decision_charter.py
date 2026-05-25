"""Phase 48.0 implementation gate decision charter tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_48_0_IMPLEMENTATION_GATE_DECISION_CHARTER.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_48_0_implementation_gate_decision_charter.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_phase_48_0_fixture_exists_and_is_docs_only_charter() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "48.0"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["implementation_gate_charter_only"] is True
    assert fixture["runtime_test_harness_created"] is False
    assert fixture["actual_acceptance_tests_created"] is False
    assert fixture["executable_acceptance_tests_created"] is False
    assert fixture["phase_47_3_anchor"] == "6c08d23e6df72f3d0ba135336a3b89f13b48ef4a"
    assert (
        fixture["phase_47_3_tag"]
        == "phase-47.3-static-acceptance-test-checklist-archive-closeout"
    )


def test_phase_48_0_reviewed_evidence_includes_phase_44_through_47() -> None:
    reviewed = set(_load_json(PHASE_FIXTURE_PATH)["reviewed_evidence"])
    assert "phase_44_typed_bridge_design_fixture_review_archive_lane" in reviewed
    assert "phase_45_acceptance_test_design_matrix_readiness_archive_lane" in reviewed
    assert "phase_46_static_implementation_plan_dry_run_readiness_archive_lane" in reviewed
    assert "phase_47_static_preflight_checklist_readiness_archive_lane" in reviewed


def test_phase_48_0_current_decision_approves_no_implementation_surfaces() -> None:
    decision = _load_json(PHASE_FIXTURE_PATH)["current_decision"]
    for key in (
        "implementation_approved",
        "runtime_harness_approved",
        "executable_acceptance_tests_approved",
        "lima_changes_approved",
        "tests_support_changes_approved",
        "guardian_decision_creation_approved",
        "approval_enforcement_approved",
        "execution_dispatch_persistence_approved",
        "model_tool_driver_external_calls_approved",
        "robotics_physical_world_behavior_approved",
    ):
        assert decision[key] is False


def test_phase_48_0_future_options_include_pause_and_docs_only_choices() -> None:
    decisions = _load_json(PHASE_FIXTURE_PATH)["future_decision_options"]
    options = set(decisions["options"])
    assert decisions["default"] != "approve_first_concrete_acceptance_test_implementation_lane"
    assert decisions["implementation_lane_default"] is False
    assert "pause_preserve" in options
    assert "docs_only_implementation_gate_readiness_review" in options
    assert "docs_only_concrete_acceptance_test_implementation_design_review" in options
    assert "approve_limited_tests_support_design_only" in options
    assert "approve_first_concrete_acceptance_test_implementation_lane" in options
    assert "reject_runtime_path_continue_static_hardening" in options


def test_phase_48_0_future_preconditions_require_explicit_approval_and_file_scopes() -> None:
    preconditions = set(_load_json(PHASE_FIXTURE_PATH)["future_implementation_preconditions"])
    assert "explicit_phil_approval" in preconditions
    assert "named_allowed_files" in preconditions
    assert "named_forbidden_files" in preconditions
    assert "validated_rollback_plan" in preconditions
    assert "validation_checklist" in preconditions
    assert "independent_pre_merge_audit" in preconditions
    assert "post_merge_verification_plan" in preconditions
    assert "no_hidden_side_effects" in preconditions
    assert "no_physical_world_behavior_unless_separately_approved" in preconditions
    assert "guardian_ownership_boundary_preserved" in preconditions


def test_phase_48_0_stop_conditions_cover_forbidden_surfaces_and_repo_state() -> None:
    stop_conditions = set(_load_json(PHASE_FIXTURE_PATH)["stop_conditions"])
    assert "unapproved_lima_change" in stop_conditions
    assert "unapproved_tests_support_change" in stop_conditions
    assert "runtime_harness_creation_without_approval" in stop_conditions
    assert "executable_acceptance_tests_without_approval" in stop_conditions
    assert "guardian_decision_creation_without_approval" in stop_conditions
    assert "approval_enforcement_without_approval" in stop_conditions
    assert "execution_dispatch_persistence_without_approval" in stop_conditions
    assert "model_tool_driver_external_call_without_approval" in stop_conditions
    assert "sparkbot_arc_humaninput_live_adapter_wiring_without_approval" in stop_conditions
    assert "robotics_physical_world_behavior_without_approval" in stop_conditions
    assert "failed_validation" in stop_conditions
    assert "dirty_worktree" in stop_conditions
    assert "branch_head_mismatch" in stop_conditions
    assert "missing_base_or_tag_verification" in stop_conditions


def test_phase_48_0_boundary_results_preserve_all_blocked_runtime_and_action_surfaces() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    for key in (
        "runtime_bridge_behavior_added",
        "runtime_test_harness_active",
        "actual_acceptance_test_harness_behavior_added",
        "executable_acceptance_tests_created",
        "lima_changes",
        "tests_support_changes",
        "sparkbot_wiring_added",
        "arc_bot_implementation_added",
        "humaninput_bridge_behavior_added",
        "live_adapters_added",
        "real_intentcompiler_behavior_added",
        "real_guardian_request_runtime_behavior_added",
        "guardian_decision_created",
        "approval_enforcement_added",
        "execution_dispatch_persistence_added",
        "model_tool_driver_calls_added",
        "external_calls_added",
        "shell_browser_network_file_mutation_added",
        "robotics_physical_world_behavior_added",
        "hidden_side_effects_added",
    ):
        assert boundary[key] is False


def test_phase_48_0_recommends_pause_or_docs_only_next_lane_and_blocks_runtime() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["recommended_next_lane"] in {
        "pause_preserve",
        "phase_48_1_docs_tests_fixtures_only_implementation_gate_readiness_review",
    }
    assert fixture["implementation_approved"] is False
    assert fixture["runtime_implementation_recommended"] is False
    assert fixture["next_runtime_implementation_approved"] is False
    assert fixture["runtime_or_harness_implementation_approved"] is False
    assert fixture["runtime_gap_found"] is False
    assert fixture["runtime_change_needed"] is False
    assert fixture["lima_change_needed"] is False
    assert fixture["tests_support_change_needed"] is False


def test_phase_48_0_stays_out_of_runtime_and_tests_support_paths() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["runtime_behavior_changed"] is False
    assert not list((REPO_ROOT / "lima").rglob("*phase_48_0*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_48_0*"))


def test_phase_48_0_doc_declares_charter_only_and_runtime_block() -> None:
    text = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "docs/tests/fixtures-only decision charter" in text
    assert "does not create or activate a runtime test harness" in text
    assert "does not modify `lima/` or `tests/support/`" in text
    assert "Runtime implementation remains blocked" in text
