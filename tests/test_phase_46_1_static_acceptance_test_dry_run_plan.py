"""Phase 46.1 static acceptance-test dry-run plan tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_46_1_STATIC_ACCEPTANCE_TEST_DRY_RUN_PLAN.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_46_1_static_acceptance_test_dry_run_plan.json"
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


def test_phase_46_1_fixture_exists_and_is_static_dry_run_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "46.1"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["static_dry_run_only"] is True
    assert fixture["runtime_test_harness_created"] is False
    assert fixture["actual_acceptance_tests_created"] is False
    assert fixture["executable_acceptance_tests_created"] is False
    assert fixture["phase_46_0_anchor"] == "aa99e0b6746820caa4e45b0763646ea5152cd84e"
    assert (
        fixture["phase_46_0_tag"]
        == "phase-46.0-static-acceptance-test-implementation-plan-template"
    )


def test_phase_46_1_required_dry_run_cases_exist() -> None:
    cases = _load_json(PHASE_FIXTURE_PATH)["dry_run_cases"]
    case_ids = {case["dry_run_case_id"] for case in cases}
    assert REQUIRED_DRY_RUN_CASE_IDS.issubset(case_ids)


def test_phase_46_1_every_dry_run_case_has_required_fields() -> None:
    for case in _load_json(PHASE_FIXTURE_PATH)["dry_run_cases"]:
        assert REQUIRED_DRY_RUN_CASE_FIELDS.issubset(case.keys())
        assert isinstance(case["future_candidate_files"], list)
        assert isinstance(case["forbidden_files"], list)
        assert isinstance(case["expected_checks"], list)
        assert isinstance(case["stop_conditions"], list)
        assert isinstance(case["rollback_requirements"], list)
        assert isinstance(case["boundary_flags"], dict)


def test_phase_46_1_candidate_patterns_and_forbidden_surfaces_preserve_boundaries() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    patterns = fixture["candidate_file_patterns"]
    assert "tests/test_typed_bridge_acceptance_*.py" in patterns
    assert "tests/fixtures/runtime_extraction/typed_bridge_acceptance_*.json" in patterns
    assert all(not p.startswith("lima/") for p in patterns)
    assert all(not p.startswith("tests/support/") for p in patterns)

    forbidden = set(fixture["forbidden_file_surfaces"])
    assert "lima/" in forbidden
    assert "tests/support/" in forbidden


def test_phase_46_1_stop_and_rollback_conditions_cover_forbidden_runtime_surfaces() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    stops = set(fixture["stop_conditions"])
    assert "any_lima_change" in stops
    assert "any_tests_support_change" in stops
    assert "runtime_test_harness_created" in stops
    assert "executable_runtime_bridge_acceptance_tests_created" in stops
    assert "actual_acceptance_test_harness_behavior_added" in stops
    assert "guardian_decision_created" in stops
    assert "approval_enforcement_added" in stops
    assert "execution_dispatch_persistence_added" in stops
    assert "external_model_tool_driver_calls_added" in stops
    assert "robotics_physical_world_behavior_added" in stops
    assert "failed_validation" in stops
    assert "unclear_approval_boundary" in stops

    rollback = set(fixture["rollback_requirements"])
    assert "stop_immediately_on_forbidden_scope" in rollback
    assert "revert_or_isolate_unapproved_files_before_continue" in rollback
    assert "keep_merge_and_tag_blocked_until_independent_audit_and_phil_approval" in rollback
    assert "report_failure_mode_and_boundary_risk" in rollback


def test_phase_46_1_boundary_flags_keep_runtime_and_action_surfaces_blocked() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    boundary = fixture["boundary_flags"]
    assert boundary["docs_tests_fixtures_only"] is True
    assert boundary["static_dry_run_only"] is True
    assert boundary["runtime_test_harness_created"] is False
    assert boundary["actual_acceptance_tests_created"] is False
    assert boundary["executable_acceptance_tests_created"] is False
    assert boundary["acceptance_test_harness_behavior_added"] is False
    assert boundary["runtime_bridge_behavior_added"] is False
    assert boundary["guardian_decision_created"] is False
    assert boundary["approval_enforcement_added"] is False
    assert boundary["execution_dispatch_persistence_added"] is False
    assert boundary["model_tool_driver_calls_added"] is False
    assert boundary["external_calls_added"] is False
    assert boundary["shell_browser_network_file_mutation_added"] is False
    assert boundary["robotics_physical_world_behavior_added"] is False
    assert boundary["hidden_side_effects_added"] is False
    assert boundary["runtime_implementation_recommended"] is False
    assert boundary["next_runtime_implementation_approved"] is False


def test_phase_46_1_recommends_docs_tests_fixtures_only_next_lane() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["recommended_next_lane"] == (
        "phase_46_2_docs_tests_fixtures_only_static_dry_run_readiness_review_or_archive_closeout"
    )
    assert fixture["runtime_implementation_recommended"] is False
    assert fixture["next_runtime_implementation_approved"] is False
    assert fixture["runtime_gap_found"] is False
    assert fixture["runtime_change_needed"] is False
    assert fixture["lima_change_needed"] is False
    assert fixture["tests_support_change_needed"] is False


def test_phase_46_1_stays_out_of_runtime_and_tests_support_paths() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["runtime_behavior_changed"] is False
    assert not list((REPO_ROOT / "lima").rglob("*phase_46_1*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_46_1*"))


def test_phase_46_1_doc_declares_dry_run_only_and_runtime_block() -> None:
    text = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "docs/tests/fixtures-only static dry-run plan lane" in text
    assert "does not create a runtime test harness" in text
    assert "Runtime implementation remains blocked" in text
