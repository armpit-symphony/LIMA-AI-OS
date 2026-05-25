"""Phase 47.2 static acceptance-test checklist readiness review tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_47_2_STATIC_ACCEPTANCE_TEST_CHECKLIST_READINESS_REVIEW.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_47_2_static_acceptance_test_checklist_readiness_review.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_phase_47_2_fixture_exists_and_is_docs_only_readiness_review() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "47.2"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["readiness_review_only"] is True
    assert fixture["runtime_test_harness_created"] is False
    assert fixture["actual_acceptance_tests_created"] is False
    assert fixture["executable_acceptance_tests_created"] is False
    assert fixture["phase_47_1_anchor"] == "e377000ee87867485fdfe79449dd0b69c51c6a38"
    assert (
        fixture["phase_47_1_tag"]
        == "phase-47.1-static-acceptance-test-implementation-checklist"
    )


def test_phase_47_2_readiness_results_confirm_checklist_scope_and_evidence() -> None:
    readiness = _load_json(PHASE_FIXTURE_PATH)["checklist_readiness_results"]
    assert readiness["phase_47_0_decision_b_carried_forward"] is True
    assert readiness["docs_tests_fixtures_only_checklist_only_scope"] is True
    assert readiness["phase_44_45_46_47_0_evidence_confirmed"] is True
    assert readiness["blocks_lima_and_tests_support"] is True
    assert readiness["blocks_runtime_harness_creation_or_activation"] is True
    assert readiness["blocks_actual_or_executable_acceptance_tests"] is True
    assert readiness["future_phil_approval_gates_explicit"] is True
    assert readiness["runtime_implementation_recommended"] is False
    assert readiness["runtime_implementation_approved"] is False
    assert readiness["sev_1_blockers"] == []
    assert readiness["sev_2_readiness_gaps"] == []


def test_phase_47_2_readiness_decision_recommends_archive_closeout_only() -> None:
    decision = _load_json(PHASE_FIXTURE_PATH)["readiness_decision"]
    assert decision["decision"] == "ready_for_docs_tests_fixtures_only_static_archive_closeout"
    assert decision["phase_47_3_archive_closeout_recommended"] is True
    assert decision["runtime_or_harness_implementation_approved"] is False


def test_phase_47_2_future_approval_gates_include_required_phil_controls() -> None:
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


def test_phase_47_2_boundary_results_preserve_all_blocked_runtime_and_action_surfaces() -> None:
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


def test_phase_47_2_recommends_phase_47_3_and_blocks_runtime_implementation() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["recommended_next_lane"] == (
        "phase_47_3_docs_tests_fixtures_only_static_acceptance_test_checklist_archive_closeout"
    )
    assert fixture["runtime_implementation_recommended"] is False
    assert fixture["next_runtime_implementation_approved"] is False
    assert fixture["runtime_or_harness_implementation_approved"] is False
    assert fixture["runtime_gap_found"] is False
    assert fixture["runtime_change_needed"] is False
    assert fixture["lima_change_needed"] is False
    assert fixture["tests_support_change_needed"] is False


def test_phase_47_2_stays_out_of_runtime_and_tests_support_paths() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["runtime_behavior_changed"] is False
    assert not list((REPO_ROOT / "lima").rglob("*phase_47_2*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_47_2*"))


def test_phase_47_2_doc_declares_readiness_review_only_and_runtime_block() -> None:
    text = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "docs/tests/fixtures-only static readiness-review metadata" in text
    assert "does not create or activate a runtime test harness" in text
    assert "does not add actual or executable runtime bridge acceptance tests" in text
    assert "Runtime implementation remains blocked" in text
