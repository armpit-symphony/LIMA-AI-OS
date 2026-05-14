"""Static checks for Phase 7.2 kernel runtime safety preconditions."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_7_2_KERNEL_RUNTIME_SAFETY_PRECONDITIONS.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_7_2_kernel_runtime_safety_preconditions.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_declares_safety_preconditions_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "7.2"
    assert fixture["non_runtime"] is True
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["safety_preconditions_only"] is True


def test_test_preconditions_cover_negative_and_import_boundary_cases() -> None:
    preconditions = set(_load_json(PHASE_FIXTURE_PATH)["test_preconditions"])
    assert "targeted_tests_for_every_future_runtime_file" in preconditions
    assert "negative_tests_for_missing_typed_input" in preconditions
    assert "negative_tests_for_raw_natural_language_parsing_attempts" in preconditions
    assert "negative_tests_for_execution_approval_audit_and_side_effects" in preconditions
    assert "import_boundary_tests_for_no_sparkbot_coupling" in preconditions
    assert "full_suite_passing_before_merge" in preconditions


def test_rollback_preconditions_block_irreversible_changes() -> None:
    rollback = _load_json(PHASE_FIXTURE_PATH)["rollback_preconditions"]
    assert rollback["future_runtime_slice_independently_revertible"] is True
    assert rollback["irreversible_migration_allowed"] is False
    assert rollback["persistent_schema_change_allowed"] is False
    assert rollback["external_side_effect_allowed"] is False
    assert rollback["docs_tests_fixtures_state_recoverable"] is True


def test_audit_proof_preconditions_remain_test_evidence_only() -> None:
    audit = _load_json(PHASE_FIXTURE_PATH)["audit_proof_preconditions"]
    assert audit["candidate_output_requires_provenance_metadata"] is True
    assert audit["candidate_output_requires_non_executable_markers"] is True
    assert audit["candidate_output_identifies_future_guardian_review_boundary"] is True
    assert audit["audit_proof_test_evidence_only_until_persistence_approved"] is True


def test_input_output_shape_preconditions_block_permissions_and_handoff() -> None:
    shape = _load_json(PHASE_FIXTURE_PATH)["input_output_shape_preconditions"]
    assert shape["input_typed_explicit_metadata_only"] is True
    assert shape["input_fails_closed_if_required_fields_missing"] is True
    assert shape["output_non_executable_candidate_metadata_only"] is True
    assert shape["output_includes_approval_permission"] is False
    assert shape["output_includes_execution_permission"] is False
    assert shape["output_includes_driver_handoff"] is False
    assert shape["output_includes_persistence_authority"] is False


def test_safety_gate_preconditions_keep_runtime_blocked() -> None:
    gates = _load_json(PHASE_FIXTURE_PATH)["safety_gate_preconditions"]
    assert gates["phase_5_runtime_bridge_gate_active"] is True
    assert gates["phase_7_1_file_map_honored"] is True
    assert gates["guardiandecision_future_authority"] is True
    assert gates["approval_enforcement_blocked"] is True
    assert gates["execution_blocked"] is True
    assert gates["sparkbot_wiring_blocked"] is True
    assert gates["physical_world_behavior_blocked"] is True


def test_ready_only_for_phase_seven_three_test_plan() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["ready_for"] == [
        "phase_7_3_docs_tests_fixtures_only_runtime_implementation_test_plan"
    ]
    assert "runtime_behavior" in fixture["not_ready_for"]
    assert "lima_changes" in fixture["not_ready_for"]
    assert "approval_enforcement" in fixture["not_ready_for"]


def test_doc_keeps_preconditions_non_runtime() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "It is docs/tests/fixtures only" in phase_doc
    assert "does not implement runtime behavior" in phase_doc
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "Runtime implementation remains blocked" in phase_doc


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["runtime_behavior_added"] is False
    assert boundary["files_under_lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["helper_behavior_changed"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["execution_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False


def test_no_phase_seven_two_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_7_2*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_7_2*"))
