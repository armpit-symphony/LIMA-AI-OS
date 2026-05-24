"""Phase 46.2 static acceptance-test dry-run readiness review tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_46_2_STATIC_ACCEPTANCE_TEST_DRY_RUN_READINESS_REVIEW.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_46_2_static_acceptance_test_dry_run_readiness_review.json"
)

REQUIRED_DRY_RUN_CASE_IDS = {
    "source_request_metadata_shape_dry_run",
    "typed_intentenvelope_candidate_shape_dry_run",
    "guardian_request_metadata_shape_dry_run",
    "guardian_decision_boundary_dry_run",
    "positive_non_authoritative_shape_dry_run",
    "approval_bypass_fail_closed_dry_run",
    "forged_guardian_decision_fail_closed_dry_run",
    "missing_actor_tenant_lineage_fail_closed_dry_run",
    "background_dispatch_fail_closed_dry_run",
    "adapter_external_call_fail_closed_dry_run",
    "model_tool_driver_call_fail_closed_dry_run",
    "robotics_physical_world_fail_closed_dry_run",
    "runtime_support_boundary_path_dry_run",
}

REQUIRED_DRY_RUN_CASE_FIELDS = {
    "dry_run_case_id",
    "source_phase_reference",
    "future_test_family",
    "future_candidate_files",
    "forbidden_files",
    "expected_checks",
    "stop_conditions",
    "rollback_requirements",
    "expected_result",
    "boundary_flags",
}


def _load_json(path: Path) -> dict[str, Any]:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_phase_46_2_fixture_exists_and_opens_docs_only_readiness_review_lane() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "46.2"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["readiness_review_only"] is True
    assert fixture["runtime_test_harness_created"] is False
    assert fixture["actual_acceptance_tests_created"] is False
    assert fixture["executable_acceptance_tests_created"] is False
    assert fixture["phase_46_1_anchor"] == "bc1e5978f39e36c9e61f6a5f8cadb6b52ed2d965"
    assert fixture["phase_46_1_tag"] == "phase-46.1-static-acceptance-test-dry-run-plan"
    assert fixture["reviewed_phase"] == "46.1"


def test_phase_46_2_coverage_results_confirm_required_dry_run_case_and_field_coverage() -> None:
    coverage = _load_json(PHASE_FIXTURE_PATH)["coverage_results"]
    assert coverage["all_phase_46_1_required_dry_run_cases_exist"] is True
    assert REQUIRED_DRY_RUN_CASE_IDS.issubset(set(coverage["required_dry_run_cases"]))
    assert coverage["every_required_dry_run_case_has_required_fields"] is True
    assert REQUIRED_DRY_RUN_CASE_FIELDS.issubset(
        set(coverage["required_dry_run_case_fields"])
    )


def test_phase_46_2_coverage_results_confirm_candidate_only_and_forbidden_surfaces() -> None:
    coverage = _load_json(PHASE_FIXTURE_PATH)["coverage_results"]
    assert coverage["candidate_file_patterns_are_candidate_only"] is True
    patterns = coverage["candidate_file_patterns"]
    assert "tests/test_typed_bridge_acceptance_*.py" in patterns
    assert "tests/fixtures/runtime_extraction/typed_bridge_acceptance_*.json" in patterns
    assert all(not p.startswith("lima/") for p in patterns)
    assert all(not p.startswith("tests/support/") for p in patterns)

    assert coverage["forbidden_file_surfaces_explicit"] is True
    forbidden = set(coverage["forbidden_file_surfaces"])
    assert "lima/" in forbidden
    assert "tests/support/" in forbidden


def test_phase_46_2_coverage_results_confirm_stop_rollback_and_boundary_coverage() -> None:
    coverage = _load_json(PHASE_FIXTURE_PATH)["coverage_results"]
    assert coverage["stop_conditions_fail_closed"] is True
    covered_stops = set(coverage["covered_stop_conditions"])
    assert "any_lima_change" in covered_stops
    assert "any_tests_support_change" in covered_stops
    assert "runtime_test_harness_created" in covered_stops
    assert "actual_acceptance_test_harness_behavior_added" in covered_stops
    assert "executable_runtime_bridge_acceptance_tests_created" in covered_stops
    assert "guardian_decision_created" in covered_stops
    assert "approval_enforcement_added" in covered_stops
    assert "execution_dispatch_persistence_added" in covered_stops
    assert "external_model_tool_driver_calls_added" in covered_stops
    assert "robotics_physical_world_behavior_added" in covered_stops
    assert "failed_validation" in covered_stops
    assert "unclear_approval_boundary" in covered_stops

    assert coverage["rollback_requirements_explicit"] is True
    rollback = set(coverage["covered_rollback_requirements"])
    assert "stop_immediately_on_forbidden_scope" in rollback
    assert "revert_or_isolate_unapproved_files_before_continue" in rollback
    assert "keep_merge_and_tag_blocked_until_independent_audit_and_phil_approval" in rollback
    assert "report_failure_mode_and_boundary_risk" in rollback
    assert coverage["boundary_flags_preserve_blocked_surfaces"] is True


def test_phase_46_2_gap_results_allow_docs_only_continuation_without_runtime_recommendation() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    gaps = fixture["gap_results"]
    assert gaps["sev_1_blockers"] == []
    assert gaps["sev_2_readiness_gaps"] == []
    assert isinstance(gaps["sev_3_cleanup_notes"], list)
    assert gaps["continuation_recommended"] is True
    assert "No SEV-1 or SEV-2 readiness gap" in gaps["continuation_reason"]
    assert fixture["runtime_implementation_recommended"] is False
    assert fixture["next_runtime_implementation_approved"] is False
    assert fixture["recommended_next_lane"].startswith("phase_46_3_docs_tests_fixtures_only_")


def test_phase_46_2_boundary_results_preserve_all_blocked_runtime_surfaces() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    for key in (
        "runtime_bridge_behavior_added",
        "runtime_test_harness_active",
        "actual_acceptance_test_harness_behavior_added",
        "executable_acceptance_tests_created",
        "lima_changes",
        "tests_support_changes",
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


def test_phase_46_2_stays_out_of_runtime_and_tests_support_paths() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["runtime_behavior_changed"] is False
    assert not list((REPO_ROOT / "lima").rglob("*phase_46_2*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_46_2*"))


def test_phase_46_2_doc_declares_readiness_review_only_and_runtime_block() -> None:
    text = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "docs/tests/fixtures-only static readiness review" in text
    assert "does not create or activate a runtime test harness" in text
    assert "No runtime implementation is recommended by Phase 46.2." in text
    assert "Runtime implementation remains blocked." in text
