"""Phase 48.1 implementation gate readiness review tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_48_1_IMPLEMENTATION_GATE_READINESS_REVIEW.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_48_1_implementation_gate_readiness_review.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_phase_48_1_fixture_exists_and_is_docs_only_review() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "48.1"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["implementation_gate_readiness_review_only"] is True
    assert fixture["runtime_test_harness_created"] is False
    assert fixture["actual_acceptance_tests_created"] is False
    assert fixture["executable_acceptance_tests_created"] is False
    assert fixture["phase_48_0_anchor"] == "b935dfd034adff9678087417710b2db08dd0bdca"
    assert fixture["phase_48_0_tag"] == "phase-48.0-implementation-gate-decision-charter"


def test_phase_48_1_reviewed_evidence_includes_phase_44_through_48_0() -> None:
    reviewed = set(_load_json(PHASE_FIXTURE_PATH)["reviewed_evidence"])
    assert "phase_44_typed_bridge_design_fixture_review_archive_lane" in reviewed
    assert "phase_45_acceptance_test_design_matrix_readiness_archive_lane" in reviewed
    assert "phase_46_static_implementation_plan_dry_run_readiness_archive_lane" in reviewed
    assert "phase_47_static_preflight_checklist_readiness_archive_lane" in reviewed
    assert "phase_48_0_implementation_gate_decision_charter" in reviewed


def test_phase_48_1_readiness_answers_stay_complete_and_non_approving() -> None:
    readiness = _load_json(PHASE_FIXTURE_PATH)["readiness_results"]
    assert readiness["gate_charter_complete_enough_for_future_implementation_decision"] is True
    assert readiness["approval_requirements_explicit"] is True
    assert readiness["stop_conditions_complete"] is True
    assert readiness["file_scope_requirements_clear"] is True
    assert readiness["rollback_requirements_clear"] is True
    assert readiness["protects_lima_from_unapproved_runtime_and_action_surfaces"] is True
    assert (
        readiness[
            "sparkbot_shell_preview_can_use_non_authoritative_mock_display_only_contract_guidance"
        ]
        is True
    )
    assert readiness["no_sev_1_readiness_gaps"] is True
    assert readiness["no_sev_2_readiness_gaps"] is True
    assert readiness["implementation_approval_granted"] is False


def test_phase_48_1_sparkbot_shell_alignment_is_mock_only_and_non_authoritative() -> None:
    alignment = _load_json(PHASE_FIXTURE_PATH)["sparkbot_shell_preview_alignment"]
    allowed = set(alignment["allowed"])
    prohibited = set(alignment["prohibited"])
    assert "public_open_source_preview_material" in allowed
    assert "non_authoritative_vocabulary_alignment" in allowed
    assert "mock_display_only_contract_guidance" in allowed
    assert "sparkbot_shell_modification" in prohibited
    assert "lima_runtime_wiring" in prohibited
    assert "authoritative_contract_claims" in prohibited
    assert "approval_or_execution_authority_claims" in prohibited
    assert "runtime_behavior_changes" in prohibited


def test_phase_48_1_preconditions_and_stop_conditions_remain_fail_closed() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    preconditions = set(fixture["future_implementation_preconditions"])
    stop_conditions = set(fixture["stop_conditions"])
    assert "explicit_phil_approval" in preconditions
    assert "named_allowed_files" in preconditions
    assert "named_forbidden_files" in preconditions
    assert "validated_rollback_plan" in preconditions
    assert "independent_pre_merge_audit" in preconditions
    assert "post_merge_verification_plan" in preconditions
    assert "no_hidden_side_effects" in preconditions
    assert "no_physical_world_behavior_unless_separately_approved" in preconditions
    assert "guardian_ownership_boundary_preserved" in preconditions
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


def test_phase_48_1_boundary_flags_keep_runtime_and_action_surfaces_blocked() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    for key in (
        "runtime_bridge_behavior_added",
        "runtime_test_harness_active",
        "actual_acceptance_test_harness_behavior_added",
        "executable_acceptance_tests_created",
        "lima_changes",
        "tests_support_changes",
        "sparkbot_shell_modified",
        "sparkbot_wiring_added",
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


def test_phase_48_1_recommended_next_lane_is_pause_or_docs_only_review() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["recommended_next_lane"] == (
        "pause_preserve_or_phase_48_2_docs_tests_fixtures_only_concrete_implementation_"
        "design_review_requires_explicit_phil_approval"
    )
    assert fixture["implementation_approved"] is False
    assert fixture["runtime_implementation_recommended"] is False
    assert fixture["next_runtime_implementation_approved"] is False
    assert fixture["runtime_or_harness_implementation_approved"] is False
    assert fixture["runtime_gap_found"] is False
    assert fixture["runtime_change_needed"] is False
    assert fixture["lima_change_needed"] is False
    assert fixture["tests_support_change_needed"] is False


def test_phase_48_1_stays_out_of_runtime_tests_support_and_sparkbot_shell_paths() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["sparkbot_shell_changed"] is False
    assert fixture["runtime_behavior_changed"] is False
    assert not list((REPO_ROOT / "lima").rglob("*phase_48_1*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_48_1*"))


def test_phase_48_1_doc_declares_readiness_review_only_and_runtime_block() -> None:
    text = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "reviews whether the Phase 48.0 implementation gate decision charter" in text
    assert "This phase is docs/tests/fixtures-only." in text
    assert "does not modify `lima/`" in text
    assert "does not modify `tests/support/`" in text
    assert "does not modify Sparkbot Shell" in text
    assert "Runtime implementation remains blocked" in text
