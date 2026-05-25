"""Phase 47.0 static acceptance-test implementation preflight review tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_47_0_STATIC_ACCEPTANCE_TEST_IMPLEMENTATION_PREFLIGHT_REVIEW.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_47_0_static_acceptance_test_implementation_preflight_review.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_phase_47_0_fixture_exists_and_is_docs_only_preflight_review() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "47.0"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["preflight_review_only"] is True
    assert fixture["runtime_test_harness_created"] is False
    assert fixture["actual_acceptance_tests_created"] is False
    assert fixture["executable_acceptance_tests_created"] is False
    assert fixture["phase_46_3_anchor"] == "b7a55353f73a1634e176702ee653a03102ec4729"
    assert (
        fixture["phase_46_3_tag"]
        == "phase-46.3-static-acceptance-test-dry-run-archive-closeout"
    )


def test_phase_47_0_reviewed_stack_includes_phase_44_45_46_lanes() -> None:
    reviewed = set(_load_json(PHASE_FIXTURE_PATH)["reviewed_stack"])
    assert "phase_44_typed_bridge_design_fixture_review_archive_lane" in reviewed
    assert "phase_45_acceptance_test_design_matrix_readiness_archive_lane" in reviewed
    assert "phase_46_static_implementation_plan_dry_run_readiness_archive_lane" in reviewed


def test_phase_47_0_readiness_results_show_no_sev_1_or_sev_2_blocker() -> None:
    readiness = _load_json(PHASE_FIXTURE_PATH)["readiness_results"]
    assert readiness["design_requirements_exist"] is True
    assert readiness["fixture_matrix_exists"] is True
    assert readiness["dry_run_plan_exists"] is True
    assert readiness["readiness_reviews_no_sev_1_or_sev_2_gaps"] is True
    assert readiness["archive_closeouts_preserve_blocked_runtime_boundaries"] is True
    assert readiness["runtime_implementation_currently_approved"] is False
    assert readiness["sev_1_blockers"] == []
    assert readiness["sev_2_readiness_gaps"] == []


def test_phase_47_0_preflight_decision_does_not_approve_runtime_or_harness_implementation() -> None:
    decision = _load_json(PHASE_FIXTURE_PATH)["preflight_decision"]
    assert decision["selected_option"] in {"A", "B", "C"}
    assert decision["selected_option"] != "D"
    assert decision["runtime_or_harness_implementation_approved"] is False
    assert decision["concrete_acceptance_test_design_review_approved"] is False


def test_phase_47_0_future_approval_gates_include_required_phil_controls() -> None:
    gates = set(_load_json(PHASE_FIXTURE_PATH)["future_approval_gates"])
    assert "phil_approval_before_any_actual_acceptance_test_implementation" in gates
    assert "phil_approval_before_any_tests_support_change" in gates
    assert "phil_approval_before_any_lima_change" in gates
    assert "phil_approval_before_any_runtime_harness_creation_or_activation" in gates
    assert "phil_approval_before_any_real_bridge_behavior" in gates
    assert "phil_approval_before_guardian_decision_creation_or_approval_enforcement" in gates
    assert (
        "phil_approval_before_execution_dispatch_persistence_model_tool_driver_external_calls"
        in gates
    )
    assert "phil_approval_before_robotics_hardware_physical_world_behavior" in gates


def test_phase_47_0_boundary_results_preserve_all_blocked_runtime_and_action_surfaces() -> None:
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


def test_phase_47_0_recommends_docs_tests_fixtures_only_next_lane_and_blocks_runtime() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["recommended_next_lane"] == (
        "phase_47_1_docs_tests_fixtures_only_static_acceptance_test_implementation_checklist"
    )
    assert fixture["runtime_implementation_recommended"] is False
    assert fixture["next_runtime_implementation_approved"] is False
    assert fixture["runtime_gap_found"] is False
    assert fixture["runtime_change_needed"] is False
    assert fixture["lima_change_needed"] is False
    assert fixture["tests_support_change_needed"] is False


def test_phase_47_0_stays_out_of_runtime_and_tests_support_paths() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["runtime_behavior_changed"] is False
    assert not list((REPO_ROOT / "lima").rglob("*phase_47_0*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_47_0*"))


def test_phase_47_0_doc_declares_preflight_only_and_runtime_block() -> None:
    text = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "docs/tests/fixtures-only static preflight review" in text
    assert "does not create or activate a runtime test harness" in text
    assert "does not add actual or executable runtime bridge acceptance tests" in text
    assert "Runtime implementation remains blocked" in text
