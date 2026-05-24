"""Phase 45.2 typed bridge acceptance-test matrix readiness review tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_45_2_TYPED_BRIDGE_ACCEPTANCE_TEST_MATRIX_READINESS_REVIEW.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_45_2_typed_bridge_acceptance_test_matrix_readiness_review.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_45_2_fixture_exists_and_opens_docs_only_readiness_review_lane() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "45.2"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["readiness_review_only"] is True
    assert fixture["runtime_test_harness_created"] is False
    assert fixture["phase_45_1_anchor"] == "1806a6ecddcb66106eb76da03e75664c8f17c27e"
    assert (
        fixture["phase_45_1_tag"]
        == "phase-45.1-typed-bridge-acceptance-test-fixture-matrix"
    )
    assert fixture["reviewed_phase"] == "45.1"


def test_phase_45_2_coverage_results_confirm_phase_45_0_families_and_matrix_coverage() -> None:
    coverage = _load_json(PHASE_FIXTURE_PATH)["coverage_results"]
    assert coverage["all_phase_45_0_required_future_test_families_mapped"] is True
    mapped = set(coverage["mapped_future_test_families"])
    assert "source_request_metadata_shape_tests" in mapped
    assert "typed_intentenvelope_candidate_shape_tests" in mapped
    assert "guardian_request_metadata_shape_tests" in mapped
    assert "guardian_decision_metadata_boundary_tests" in mapped
    assert "positive_non_authoritative_shape_tests" in mapped
    assert "negative_approval_bypass_tests" in mapped
    assert "negative_forged_guardian_decision_tests" in mapped
    assert "negative_missing_actor_tenant_lineage_tests" in mapped
    assert "negative_background_dispatch_tests" in mapped
    assert "negative_adapter_external_call_tests" in mapped
    assert "negative_model_tool_driver_call_tests" in mapped
    assert "negative_robotics_physical_world_tests" in mapped
    assert "runtime_support_boundary_path_tests" in mapped
    assert coverage["positive_rows_exist"] is True
    assert coverage["fail_closed_rows_exist"] is True
    assert coverage["runtime_support_boundary_row_exists"] is True


def test_phase_45_2_coverage_results_keep_non_executing_state_categories() -> None:
    coverage = _load_json(PHASE_FIXTURE_PATH)["coverage_results"]
    assert coverage["expected_bridge_states_non_executing_only"] is True
    assert coverage["expected_bridge_states"] == ["needs_review", "blocked"]
    assert coverage["guardian_decision_states_restricted"] is True
    assert coverage["expected_guardian_decision_states"] == [
        "absent",
        "pending",
        "blocked",
    ]


def test_phase_45_2_gap_results_support_docs_only_continuation() -> None:
    gaps = _load_json(PHASE_FIXTURE_PATH)["gap_results"]
    assert gaps["sev_1_blockers"] == []
    assert gaps["sev_2_fixture_readiness_gaps"] == []
    assert isinstance(gaps["sev_3_cleanup_notes"], list)
    assert gaps["continuation_recommended"] is True
    assert "No SEV-1 or SEV-2 readiness gap" in gaps["continuation_reason"]


def test_phase_45_2_boundary_results_preserve_all_blocked_runtime_surfaces() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    for key in (
        "runtime_bridge_behavior_added",
        "runtime_test_harness_active",
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


def test_phase_45_2_recommends_docs_only_next_lane_and_not_runtime_implementation() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["recommended_next_lane"] == (
        "phase_45_3_docs_tests_fixtures_only_archive_closeout_or_static_"
        "acceptance_test_implementation_plan"
    )
    assert fixture["runtime_implementation_recommended"] is False
    assert fixture["next_runtime_implementation_approved"] is False
    blocked = set(fixture["blocked_scope"])
    assert "runtime_implementation" in blocked
    assert "lima_changes" in blocked
    assert "tests_support_changes" in blocked
    assert "runtime_test_harness_creation" in blocked
    assert "model_tool_driver_calls" in blocked
    assert "robotics_hardware_control_physical_world_behavior" in blocked
    assert fixture["runtime_gap_found"] is False
    assert fixture["runtime_change_needed"] is False
    assert fixture["lima_change_needed"] is False
    assert fixture["tests_support_change_needed"] is False
    assert fixture["next_phase"] == "45.3_requires_phil_approval"


def test_phase_45_2_stays_out_of_runtime_and_tests_support_paths() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["runtime_behavior_changed"] is False
    assert not list((REPO_ROOT / "lima").rglob("*phase_45_2*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_45_2*"))


def test_phase_45_2_doc_declares_readiness_review_only_and_non_runtime_boundaries() -> None:
    text = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "docs/tests/fixtures-only no-code readiness review" in text
    assert "does not create or activate a runtime test harness" in text
    assert "No runtime implementation is recommended by Phase 45.2." in text
