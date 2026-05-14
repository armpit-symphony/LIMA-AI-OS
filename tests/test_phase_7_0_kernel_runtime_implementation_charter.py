"""Static checks for Phase 7.0 kernel runtime implementation charter."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_7_0_KERNEL_RUNTIME_IMPLEMENTATION_CHARTER.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_7_0_kernel_runtime_implementation_charter.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_declares_no_code_charter_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "7.0"
    assert fixture["non_runtime"] is True
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["no_code_charter_only"] is True


def test_smallest_future_runtime_slice_is_not_approved_now() -> None:
    slice_def = _load_json(PHASE_FIXTURE_PATH)["future_smallest_runtime_slice"]
    assert slice_def["name"] == "non_executing_kernel_intake_to_candidate_coordinator"
    assert slice_def["approved_for_implementation_now"] is False
    assert slice_def["accepts_only_typed_explicit_inputs"] is True
    assert slice_def["produces_non_executable_candidate_metadata"] is True


def test_future_runtime_slice_blocks_execution_and_side_effects() -> None:
    slice_def = _load_json(PHASE_FIXTURE_PATH)["future_smallest_runtime_slice"]
    assert slice_def["parses_raw_natural_language"] is False
    assert slice_def["executes_tools"] is False
    assert slice_def["enforces_approval"] is False
    assert slice_def["persists_audit"] is False
    assert slice_def["calls_models"] is False
    assert slice_def["calls_network_services"] is False
    assert slice_def["mutates_files"] is False
    assert slice_def["wires_sparkbot"] is False
    assert slice_def["touches_physical_world_drivers"] is False


def test_runtime_constraints_preserve_guardian_and_sparkbot_boundaries() -> None:
    constraints = _load_json(PHASE_FIXTURE_PATH)["future_runtime_slice_constraints"]
    assert constraints["candidate_metadata_cannot_authorize_itself"] is True
    assert constraints["guardiandecision_future_authority_boundary"] is True
    assert constraints["approval_state_descriptive_until_later_approved_enforcement_phase"] is True
    assert constraints["sparkbot_reference_spec_until_future_integration_approval"] is True
    assert constraints["robo_os_physical_world_behavior_blocked"] is True


def test_runtime_preconditions_are_required_before_code() -> None:
    preconditions = set(_load_json(PHASE_FIXTURE_PATH)["preconditions_before_runtime_code"])
    assert "eligible_and_forbidden_files_mapped" in preconditions
    assert "tests_specified_before_implementation" in preconditions
    assert "rollback_expectations_defined" in preconditions
    assert "audit_proof_requirements_defined" in preconditions
    assert "allowed_input_output_shapes_defined" in preconditions
    assert "explicit_phil_runtime_scope_approval" in preconditions


def test_ready_only_for_phase_seven_one_file_eligibility_map() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["ready_for"] == [
        "phase_7_1_docs_tests_fixtures_only_first_runtime_slice_eligibility_map"
    ]
    assert "runtime_behavior" in fixture["not_ready_for"]
    assert "lima_changes" in fixture["not_ready_for"]
    assert "approval_enforcement" in fixture["not_ready_for"]
    assert "shell_browser_network_file_mutation_robotics_physical_world_side_effects" in fixture["not_ready_for"]


def test_doc_keeps_runtime_implementation_blocked() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "no-code kernel runtime implementation charter lane" in phase_doc
    assert "does not implement runtime behavior" in phase_doc
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "Phase 7.0 does not approve that implementation" in phase_doc
    assert "Runtime implementation remains blocked" in phase_doc


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["runtime_behavior_added"] is False
    assert boundary["files_under_lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["helper_behavior_changed"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["intentcompiler_runtime_changed"] is False
    assert boundary["guardiandecision_runtime_changed"] is False
    assert boundary["execution_added"] is False
    assert boundary["physical_world_action_added"] is False


def test_no_phase_seven_zero_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_7_0*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_7_0*"))
