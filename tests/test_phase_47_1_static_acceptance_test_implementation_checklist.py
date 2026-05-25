"""Phase 47.1 static acceptance-test implementation checklist tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_47_1_STATIC_ACCEPTANCE_TEST_IMPLEMENTATION_CHECKLIST.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_47_1_static_acceptance_test_implementation_checklist.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_phase_47_1_fixture_exists_and_is_docs_only_checklist() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "47.1"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["checklist_only"] is True
    assert fixture["runtime_test_harness_created"] is False
    assert fixture["actual_acceptance_tests_created"] is False
    assert fixture["executable_acceptance_tests_created"] is False
    assert fixture["phase_47_0_anchor"] == "abff459cb6877f9ca07ce50da661ba395d710226"
    assert (
        fixture["phase_47_0_tag"]
        == "phase-47.0-static-acceptance-test-implementation-preflight-review"
    )
    assert fixture["phase_47_0_preflight_decision"] == "B"


def test_phase_47_1_checklist_readiness_basis_is_present_and_non_runtime() -> None:
    basis = _load_json(PHASE_FIXTURE_PATH)["checklist_readiness_basis"]
    assert basis["phase_44_archive_present"] is True
    assert basis["phase_45_archive_present"] is True
    assert basis["phase_46_archive_present"] is True
    assert basis["phase_47_0_preflight_complete"] is True
    assert basis["phase_47_0_runtime_or_harness_implementation_approved"] is False


def test_phase_47_1_implementation_checklist_is_complete_and_fail_closed() -> None:
    checklist = set(_load_json(PHASE_FIXTURE_PATH)["implementation_checklist_items"])
    assert "scope_docs_tests_fixtures_only_checklist_only" in checklist
    assert "phase_44_45_46_47_0_evidence_confirmed" in checklist
    assert "no_lima_or_tests_support_changes" in checklist
    assert "no_runtime_harness_created_or_active" in checklist
    assert "no_actual_or_executable_acceptance_tests_created" in checklist
    assert "forbidden_surfaces_explicit" in checklist
    assert "stop_conditions_fail_closed" in checklist
    assert "rollback_requirements_explicit" in checklist
    assert "validation_requirements_explicit" in checklist
    assert "future_phil_approval_gates_explicit" in checklist
    assert "runtime_not_recommended_or_approved" in checklist


def test_phase_47_1_future_approval_gates_include_required_phil_controls() -> None:
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


def test_phase_47_1_boundary_results_preserve_all_blocked_runtime_and_action_surfaces() -> None:
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


def test_phase_47_1_recommends_docs_only_next_lane_and_blocks_runtime() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["recommended_next_lane"] == (
        "phase_47_2_docs_tests_fixtures_only_static_acceptance_test_checklist_readiness_review"
    )
    assert fixture["runtime_implementation_recommended"] is False
    assert fixture["next_runtime_implementation_approved"] is False
    assert fixture["runtime_or_harness_implementation_approved"] is False
    assert fixture["runtime_gap_found"] is False
    assert fixture["runtime_change_needed"] is False
    assert fixture["lima_change_needed"] is False
    assert fixture["tests_support_change_needed"] is False


def test_phase_47_1_stays_out_of_runtime_and_tests_support_paths() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["runtime_behavior_changed"] is False
    assert not list((REPO_ROOT / "lima").rglob("*phase_47_1*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_47_1*"))


def test_phase_47_1_doc_declares_checklist_only_and_runtime_block() -> None:
    text = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "docs/tests/fixtures-only static checklist metadata" in text
    assert "does not create or activate a runtime test harness" in text
    assert "does not add actual or executable runtime bridge acceptance tests" in text
    assert "Runtime implementation remains blocked" in text
