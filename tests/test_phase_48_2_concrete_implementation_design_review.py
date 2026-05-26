"""Phase 48.2 concrete implementation design review tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_48_2_CONCRETE_IMPLEMENTATION_DESIGN_REVIEW.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_48_2_concrete_implementation_design_review.json"
)
CANDIDATE_FUTURE_FILES = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "typed_bridge_acceptance_preview_only_positive.json",
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "typed_bridge_acceptance_fail_closed_approval_bypass.json",
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "typed_bridge_acceptance_fail_closed_runtime_claim.json",
    REPO_ROOT / "tests" / "test_typed_bridge_acceptance_preview_only.py",
)


def _load_json(path: Path) -> dict[str, Any]:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_phase_48_2_fixture_exists_and_is_design_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "48.2"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["concrete_implementation_design_review_only"] is True
    assert fixture["implementation_approved"] is False
    assert fixture["runtime_test_harness_created"] is False
    assert fixture["actual_acceptance_tests_created"] is False
    assert fixture["executable_acceptance_tests_created"] is False
    assert fixture["phase_48_1_anchor"] == "616a692c6dba59b2d43953582251747aeb39396f"
    assert fixture["phase_48_1_tag"] == "phase-48.1-implementation-gate-readiness-review"
    assert fixture["reviewed_phase"] == "48.1"


def test_phase_48_2_proposed_first_lane_is_design_only_and_unapproved() -> None:
    lane = _load_json(PHASE_FIXTURE_PATH)["proposed_first_implementation_lane"]
    assert lane["name"] == "first_concrete_typed_bridge_acceptance_test_design"
    assert lane["candidate_status"] == "design_only"
    assert lane["implementation_approved"] is False
    intent = set(lane["candidate_implementation_intent"])
    assert "create_executable_proof_later_only_if_separately_approved" in intent
    assert "prove_typed_bridge_contract_shape_without_runtime_authority" in intent
    assert "preserve_non_authoritative_preview_posture" in intent
    assert "avoid_runtime_side_effects" in intent
    assert "avoid_sparkbot_shell_live_wiring" in intent
    assert "avoid_robotics_iot_physical_world_behavior" in intent


def test_phase_48_2_candidate_allowed_files_are_referenced_but_not_created() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    allowed = set(fixture["candidate_future_allowed_files"])
    assert "tests/fixtures/runtime_extraction/typed_bridge_acceptance_preview_only_positive.json" in allowed
    assert (
        "tests/fixtures/runtime_extraction/typed_bridge_acceptance_fail_closed_approval_bypass.json"
        in allowed
    )
    assert (
        "tests/fixtures/runtime_extraction/typed_bridge_acceptance_fail_closed_runtime_claim.json"
        in allowed
    )
    assert "tests/test_typed_bridge_acceptance_preview_only.py" in allowed
    assert fixture["candidate_future_allowed_files_created_in_phase_48_2"] is False
    for candidate in CANDIDATE_FUTURE_FILES:
        assert not candidate.exists()


def test_phase_48_2_forbidden_file_scope_is_explicit() -> None:
    forbidden = set(_load_json(PHASE_FIXTURE_PATH)["candidate_future_forbidden_files"])
    assert "lima/" in forbidden
    assert "tests/support/" in forbidden
    assert "Sparkbot Shell paths" in forbidden
    assert "adapters/" in forbidden
    assert "drivers/" in forbidden
    assert "persistence/" in forbidden
    assert "runtime dispatch paths" in forbidden
    assert "robotics/IoT/drone/humanoid paths" in forbidden
    assert "shell/browser/network/file mutation paths" in forbidden
    assert "background workers" in forbidden
    assert "queues" in forbidden
    assert "daemons" in forbidden
    assert "subprocesses" in forbidden
    assert "threads" in forbidden
    assert "database writes" in forbidden


def test_phase_48_2_behavior_boundaries_block_runtime_and_action_surfaces() -> None:
    boundaries = _load_json(PHASE_FIXTURE_PATH)["candidate_future_behavior_boundaries"]
    for key in (
        "real_intentcompiler_behavior",
        "guardian_decision_creation",
        "approval_enforcement",
        "execution_dispatch_persistence",
        "model_tool_driver_external_calls",
        "sparkbot_runtime_integration",
        "guardian_approval_enforcement_claims",
        "robotics_physical_world_behavior",
        "hidden_side_effects",
    ):
        assert boundaries[key] is False


def test_phase_48_2_sparkbot_shell_implications_remain_mock_display_only() -> None:
    shell = _load_json(PHASE_FIXTURE_PATH)["sparkbot_shell_implications"]
    assert shell["mock_display_non_authoritative_only"] is True
    assert shell["lima_vocabulary_allowed_as_preview_guidance"] is True
    assert shell["sparkbot_shell_files_changed"] is False
    ui_language = set(shell["can_prepare_ui_language_for"])
    assert "consumer_profile" in ui_language
    assert "embodiment_profile" in ui_language
    assert "approval_posture" in ui_language
    assert "evidence_refs" in ui_language
    assert "preview_state" in ui_language
    assert "blocked_state" in ui_language
    must_not_claim = set(shell["must_not_claim"])
    assert "lima_runtime_integration" in must_not_claim
    assert "guardian_approval_enforcement" in must_not_claim
    assert "dispatch" in must_not_claim
    assert "execution" in must_not_claim
    assert "persistence" in must_not_claim
    assert "adapter_calls" in must_not_claim
    assert "robotics_iot_control_through_lima" in must_not_claim


def test_phase_48_2_future_approval_packet_and_stop_conditions_are_complete() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    packet = set(fixture["required_future_approval_packet"])
    stop_conditions = set(fixture["stop_conditions"])
    assert "explicit_phil_approval" in packet
    assert "exact_allowed_file_list" in packet
    assert "exact_forbidden_file_list" in packet
    assert "rollback_plan" in packet
    assert "validation_checklist" in packet
    assert "independent_pre_merge_audit" in packet
    assert "post_merge_verification_plan" in packet
    assert "active_allowance_scan" in packet
    assert "hidden_side_effect_scan" in packet
    assert (
        "confirmation_no_runtime_lima_tests_support_sparkbot_shell_changes_unless_explicitly_approved"
        in packet
    )
    assert "unapproved_lima_change" in stop_conditions
    assert "unapproved_tests_support_change" in stop_conditions
    assert "sparkbot_shell_file_change" in stop_conditions
    assert "runtime_behavior" in stop_conditions
    assert "runtime_harness_creation_or_activation" in stop_conditions
    assert "executable_acceptance_tests_created_in_phase_48_2" in stop_conditions
    assert "guardian_decision_creation" in stop_conditions
    assert "approval_enforcement" in stop_conditions
    assert "execution_dispatch_persistence" in stop_conditions
    assert "model_tool_driver_external_calls" in stop_conditions
    assert "robotics_physical_world_behavior" in stop_conditions
    assert "active_implementation_approval_flag_true" in stop_conditions
    assert "failed_validation" in stop_conditions
    assert "dirty_worktree" in stop_conditions
    assert "base_or_tag_mismatch" in stop_conditions


def test_phase_48_2_boundary_results_preserve_all_blocked_surfaces() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    for key in (
        "runtime_bridge_behavior_added",
        "runtime_test_harness_active",
        "actual_acceptance_test_harness_behavior_added",
        "executable_acceptance_tests_created",
        "lima_changes",
        "tests_support_changes",
        "sparkbot_shell_changed",
        "sparkbot_wiring_added",
        "humaninput_bridge_behavior_added",
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


def test_phase_48_2_recommends_pause_or_readiness_review_not_implementation() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["recommended_next_lane"] in {
        "pause_preserve",
        "phase_48_3_docs_tests_fixtures_only_design_readiness_review",
    }
    assert fixture["implementation_approved"] is False
    assert fixture["runtime_implementation_recommended"] is False
    assert fixture["next_runtime_implementation_approved"] is False
    assert fixture["runtime_or_harness_implementation_approved"] is False
    assert fixture["runtime_gap_found"] is False
    assert fixture["runtime_change_needed"] is False
    assert fixture["lima_change_needed"] is False
    assert fixture["tests_support_change_needed"] is False


def test_phase_48_2_stays_out_of_runtime_tests_support_and_sparkbot_shell_paths() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["sparkbot_shell_changed"] is False
    assert fixture["runtime_behavior_changed"] is False
    assert not list((REPO_ROOT / "lima").rglob("*phase_48_2*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_48_2*"))


def test_phase_48_2_doc_declares_design_only_and_runtime_block() -> None:
    text = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "This phase is docs/tests/fixtures-only." in text
    assert "This phase is not implementation." in text
    assert "This phase does not modify `lima/`." in text
    assert "This phase does not modify `tests/support/`." in text
    assert "This phase does not modify Sparkbot Shell." in text
    assert "Phase 48.2 does not create them" in text
    assert "Runtime implementation remains blocked" in text
