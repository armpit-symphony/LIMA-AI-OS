"""Static checks for Phase 10.3 acceptance test and rollback plan."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_10_3_ACCEPTANCE_TEST_AND_ROLLBACK_PLAN.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_10_3_acceptance_test_and_rollback_plan.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_no_code_acceptance_and_rollback_plan_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "10.3"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False
    assert fixture["phase_11_runtime_implementation_approved_now"] is False


def test_acceptance_tests_require_non_authoritative_candidate_safety() -> None:
    tests = set(_load_json(PHASE_FIXTURE_PATH)["required_future_acceptance_tests"])
    assert "valid_phase_9_style_candidates_validate_without_authority" in tests
    assert "missing_execution_allowed_rejected_or_blocked" in tests
    assert "missing_side_effects_allowed_rejected_or_blocked" in tests
    assert "execution_allowed_true_rejected_or_blocked" in tests
    assert "side_effects_allowed_true_rejected_or_blocked" in tests
    assert "approval_state_approved_rejected_or_blocked" in tests
    assert "normalized_status_only_proposed_needs_review_or_blocked" in tests
    assert "provenance_preserved" in tests


def test_acceptance_tests_keep_forbidden_runtime_behavior_absent() -> None:
    tests = set(_load_json(PHASE_FIXTURE_PATH)["required_future_acceptance_tests"])
    assert "humaninput_runtime_bridge_absent" in tests
    assert "sparkbot_import_or_wiring_absent" in tests
    assert "live_adapter_absent" in tests
    assert "intentcompiler_and_guardiandecision_runtime_behavior_unchanged" in tests
    assert "approval_execution_dispatch_audit_persistence_and_side_effects_absent" in tests
    assert "operator_admin_phil_trusted_wording_does_not_bypass_safety" in tests


def test_rollback_plan_is_source_only_and_validation_heavy() -> None:
    rollback = set(_load_json(PHASE_FIXTURE_PATH)["rollback_plan"])
    assert "revert_phase_11_merge_commit" in rollback
    assert "confirm_only_phase_10_2_eligible_runtime_files_were_affected" in rollback
    assert "confirm_intake_candidate_still_non_executing" in rollback
    assert "confirm_imports_side_effect_free" in rollback
    assert "rerun_full_suite" in rollback
    assert "rerun_compileall_lima" in rollback
    assert "rerun_git_diff_check" in rollback


def test_audit_proof_requires_file_scope_and_side_effect_review() -> None:
    proof = set(_load_json(PHASE_FIXTURE_PATH)["audit_proof_required"])
    assert "exact_runtime_files_changed" in proof
    assert "proof_no_files_outside_phase_10_2_map_changed" in proof
    assert "validation_output" in proof
    assert "full_suite_output" in proof
    assert "compileall_output" in proof
    assert "diff_check_output" in proof
    assert "side_effect_review" in proof
    assert "import_review" in proof
    assert "phase_5_runtime_bridge_still_gated" in proof
    assert "approval_execution_dispatch_audit_persistence_physical_world_absent" in proof


def test_phase_document_says_no_runtime_slice_is_implemented() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "It does not implement that slice" in phase_doc
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "source-only Git revert" in phase_doc


def test_next_phase_is_runtime_expansion_approval_gate() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["next_phase"] == "phase_10_4_phase_10_runtime_expansion_approval_gate_closeout"


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["helper_behavior_changed"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["live_adapter_added"] is False
    assert boundary["approval_enforcement_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False


def test_no_phase_ten_three_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_10_3*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_10_3*"))
