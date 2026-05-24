"""Phase 46.0 static acceptance-test implementation-plan template tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_46_0_STATIC_ACCEPTANCE_TEST_IMPLEMENTATION_PLAN_TEMPLATE.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_46_0_static_acceptance_test_implementation_plan_template.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_phase_46_0_fixture_exists_and_is_static_template_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "46.0"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["static_implementation_plan_template_only"] is True
    assert fixture["runtime_test_harness_created"] is False
    assert fixture["actual_acceptance_tests_created"] is False
    assert fixture["executable_acceptance_tests_created"] is False
    assert fixture["phase_45_3_anchor"] == "a81dadb20b8b22d10cf32f8ccdaae16987e6f48d"
    assert (
        fixture["phase_45_3_tag"]
        == "phase-45.3-typed-bridge-acceptance-test-archive-closeout"
    )


def test_phase_46_0_future_proof_requirements_cover_phase_45_matrix_boundaries() -> None:
    requirements = set(_load_json(PHASE_FIXTURE_PATH)["future_acceptance_test_proof_requirements"])
    assert "source_request_metadata_is_deterministic_input_metadata" in requirements
    assert "typed_intentenvelope_candidate_metadata_is_non_authoritative" in requirements
    assert "guardian_request_metadata_is_not_guardian_decision_authority" in requirements
    assert "guardian_decision_metadata_limited_to_absent_pending_blocked" in requirements
    assert "malicious_approval_claims_fail_closed" in requirements
    assert "forged_guardian_decision_claims_fail_closed" in requirements
    assert "missing_actor_tenant_lineage_metadata_fails_closed" in requirements
    assert "background_scheduling_claims_fail_closed" in requirements
    assert "adapter_external_call_claims_fail_closed" in requirements
    assert "model_tool_driver_call_claims_fail_closed" in requirements
    assert "execution_dispatch_persistence_claims_fail_closed" in requirements
    assert "robotics_physical_world_claims_fail_closed" in requirements
    assert "runtime_support_boundary_checks_remain_required" in requirements


def test_phase_46_0_declares_future_file_scope_but_approves_no_runtime_scope() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    eligible = set(fixture["future_eligible_file_scope_if_separately_approved"])
    assert "new_static_tests_under_tests" in eligible
    assert "new_inert_json_fixtures_under_tests_fixtures_runtime_extraction" in eligible
    assert "phase_documentation_under_docs" in eligible
    assert "readme_current_state_roadmap_decision_extraction_plan_updates" in eligible

    forbidden = set(fixture["forbidden_file_scope_without_separate_approval"])
    assert "lima_runtime_behavior_changes" in forbidden
    assert "tests_support_helper_behavior_changes" in forbidden
    assert "runtime_test_harness_creation_or_activation" in forbidden
    assert "actual_acceptance_test_harness_behavior" in forbidden
    assert "sparkbot_wiring" in forbidden
    assert "arc_bot_implementation" in forbidden
    assert "humaninput_bridge_behavior" in forbidden
    assert "real_intentcompiler_behavior" in forbidden
    assert "real_guardian_request_runtime_behavior" in forbidden
    assert "guardian_decision_creation" in forbidden
    assert "approval_enforcement" in forbidden
    assert "execution_dispatch_persistence" in forbidden
    assert "model_tool_driver_calls" in forbidden
    assert "robotics_hardware_physical_world_behavior" in forbidden


def test_phase_46_0_validation_and_rollback_gates_are_mandatory() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    validation = set(fixture["mandatory_validation_gates"])
    assert "python_version_check" in validation
    assert "json_fixture_validation" in validation
    assert "python_m_compileall_lima" in validation
    assert "python_m_pytest_q_tests_no_cacheprovider" in validation
    assert "git_diff_check" in validation
    assert "git_status_short_clean" in validation

    rollback = set(fixture["mandatory_rollback_gates"])
    assert "list_every_changed_file" in rollback
    assert "confirm_diff_limited_to_approved_file_scope" in rollback
    assert "confirm_no_unapproved_lima_path_change" in rollback
    assert "confirm_no_unapproved_tests_support_path_change" in rollback
    assert "confirm_no_hidden_side_effect_or_external_call_path" in rollback
    assert "keep_merge_and_tag_blocked_until_independent_audit_and_phil_approval" in rollback


def test_phase_46_0_phil_approval_gates_block_actual_implementation() -> None:
    approvals = set(_load_json(PHASE_FIXTURE_PATH)["phil_approval_required_before"])
    assert "actual_acceptance_test_implementation" in approvals
    assert "runtime_test_harness_creation" in approvals
    assert "lima_changes" in approvals
    assert "tests_support_changes" in approvals
    assert "real_typed_bridge_behavior" in approvals
    assert "real_intentcompiler_behavior" in approvals
    assert "real_guardian_request_runtime_behavior" in approvals
    assert "guardian_decision_creation" in approvals
    assert "approval_enforcement" in approvals
    assert "execution_dispatch_persistence" in approvals
    assert "model_tool_driver_calls" in approvals
    assert "external_calls" in approvals
    assert "robotics_hardware_physical_world_behavior" in approvals
    assert "merge" in approvals
    assert "tag" in approvals


def test_phase_46_0_boundary_results_preserve_all_blocked_runtime_surfaces() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    for key in (
        "runtime_bridge_behavior_added",
        "runtime_test_harness_active",
        "actual_acceptance_test_harness_behavior_added",
        "lima_changes",
        "tests_support_changes",
        "sparkbot_wiring_added",
        "arc_bot_implementation_added",
        "humaninput_bridge_behavior_added",
        "live_adapters_added",
        "intentcompiler_behavior_added",
        "guardian_request_runtime_behavior_added",
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


def test_phase_46_0_recommends_no_runtime_implementation() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["runtime_implementation_recommended"] is False
    assert fixture["next_runtime_implementation_approved"] is False
    assert fixture["runtime_gap_found"] is False
    assert fixture["runtime_change_needed"] is False
    assert fixture["lima_change_needed"] is False
    assert fixture["tests_support_change_needed"] is False
    assert (
        fixture["recommended_next_lane"]
        == "phase_46_1_docs_tests_fixtures_only_static_dry_run_plan_or_readiness_review"
    )
    assert fixture["next_phase"] == "46.1_requires_phil_approval"


def test_phase_46_0_stays_out_of_runtime_and_tests_support_paths() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["runtime_behavior_changed"] is False
    assert not list((REPO_ROOT / "lima").rglob("*phase_46_0*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_46_0*"))


def test_phase_46_0_doc_declares_template_only_and_runtime_block() -> None:
    text = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "docs/tests/fixtures-only static implementation-plan template lane" in text
    assert "does not create a runtime test harness" in text
    assert "No runtime implementation is recommended by Phase 46.0." in text
    assert "Runtime implementation remains blocked." in text
