"""Phase 47.3 static acceptance-test checklist archive closeout tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_47_3_STATIC_ACCEPTANCE_TEST_CHECKLIST_ARCHIVE_CLOSEOUT.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_47_3_static_acceptance_test_checklist_archive_closeout.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_phase_47_3_fixture_exists_and_is_docs_only_archive_closeout() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "47.3"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["archive_closeout_only"] is True
    assert fixture["runtime_test_harness_created"] is False
    assert fixture["actual_acceptance_tests_created"] is False
    assert fixture["executable_acceptance_tests_created"] is False
    assert fixture["phase_47_2_anchor"] == "5b923d44d19f96b3db705cbe040e0c8430aeee9a"
    assert (
        fixture["phase_47_2_tag"]
        == "phase-47.2-static-acceptance-test-checklist-readiness-review"
    )


def test_phase_47_3_archive_results_confirm_completed_stack_and_no_sev_1_or_sev_2() -> None:
    result = _load_json(PHASE_FIXTURE_PATH)["archive_closeout_results"]
    assert result["phase_47_0_preflight_review_completed"] is True
    assert result["phase_47_1_static_implementation_checklist_completed"] is True
    assert result["phase_47_2_checklist_readiness_review_completed"] is True
    assert result["no_sev_1_readiness_gaps"] is True
    assert result["no_sev_2_readiness_gaps"] is True
    assert isinstance(result["sev_3_cleanup_notes"], list)
    assert result["runtime_implementation_recommended"] is False
    assert result["future_runtime_implementation_approved"] is False
    assert result["future_implementation_requires_explicit_phil_approval"] is True


def test_phase_47_3_future_approval_gates_include_required_phil_controls() -> None:
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


def test_phase_47_3_boundary_results_preserve_all_blocked_runtime_and_action_surfaces() -> None:
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


def test_phase_47_3_recommends_merge_tag_gate_and_blocks_runtime_implementation() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["recommended_next_lane"] == (
        "merge_tag_approval_gate_for_phase_47_static_acceptance_test_lane_then_"
        "separate_explicit_phil_approval_for_any_future_implementation_lane"
    )
    assert fixture["runtime_implementation_recommended"] is False
    assert fixture["next_runtime_implementation_approved"] is False
    assert fixture["runtime_or_harness_implementation_approved"] is False
    assert fixture["runtime_gap_found"] is False
    assert fixture["runtime_change_needed"] is False
    assert fixture["lima_change_needed"] is False
    assert fixture["tests_support_change_needed"] is False


def test_phase_47_3_stays_out_of_runtime_and_tests_support_paths() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["runtime_behavior_changed"] is False
    assert not list((REPO_ROOT / "lima").rglob("*phase_47_3*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_47_3*"))


def test_phase_47_3_doc_declares_archive_closeout_only_and_runtime_block() -> None:
    text = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "archives docs/tests/fixtures-only static acceptance-test implementation" in text
    assert "does not create or activate a runtime test harness" in text
    assert "does not add actual or executable runtime bridge acceptance tests" in text
    assert "Runtime implementation is not recommended" in text
