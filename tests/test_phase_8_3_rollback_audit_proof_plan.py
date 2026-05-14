"""Static checks for Phase 8.3 rollback and audit proof planning."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_8_3_ROLLBACK_AUDIT_PROOF_PLAN.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_8_3_rollback_audit_proof_plan.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_docs_tests_fixtures_only_rollback_audit_plan() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "8.3"
    assert fixture["non_runtime"] is True
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_approved"] is False


def test_rollback_requirements_keep_future_change_narrow_and_revertible() -> None:
    rollback = set(_load_json(PHASE_FIXTURE_PATH)["rollback_requirements"])
    assert "future_runtime_implementation_independently_revertible" in rollback
    assert "touch_only_phase_8_1_eligible_files" in rollback
    assert "clean_docs_tests_only_fallback_state" in rollback
    assert "exact_file_list_before_merge" in rollback
    assert "targeted_test_list" in rollback
    assert "forbidden_path_diff_review" in rollback
    assert "no_broad_refactor" in rollback
    assert "no_dependency_additions" in rollback
    assert "revert_command_note_for_merge_commit" in rollback
    assert "post_revert_validation_expectation" in rollback


def test_audit_proof_requirements_are_test_evidence_only_and_authority_free() -> None:
    audit = set(_load_json(PHASE_FIXTURE_PATH)["audit_proof_requirements"])
    assert "candidate_output_includes_provenance_metadata" in audit
    assert "candidate_output_includes_non_executable_markers" in audit
    assert "candidate_output_includes_source_boundary_metadata" in audit
    assert "candidate_output_includes_future_guardian_review_boundary_refs" in audit
    assert "candidate_output_includes_no_approval_authority" in audit
    assert "candidate_output_includes_no_execution_authority" in audit
    assert "candidate_output_includes_no_audit_persistence_authority" in audit
    assert "candidate_output_includes_no_driver_handoff_authority" in audit


def test_success_criteria_remain_non_executable_candidate_only() -> None:
    success = set(_load_json(PHASE_FIXTURE_PATH)["future_success_criteria"])
    assert "only_phase_8_1_eligible_files_touched" in success
    assert "typed_input_produces_candidate_metadata" in success
    assert "candidate_metadata_non_executable" in success
    assert "candidate_metadata_not_approved" in success
    assert "candidate_metadata_not_execution_ready" in success
    assert "future_guardian_review_boundary_explicit" in success
    assert "rollback_path_documented" in success


def test_failure_criteria_stop_on_runtime_escape_paths() -> None:
    failure = set(_load_json(PHASE_FIXTURE_PATH)["future_failure_criteria"])
    assert "forbidden_file_surface_needed" in failure
    assert "raw_natural_language_parsed" in failure
    assert "humaninput_runtime_bridge_behavior_appears" in failure
    assert "real_intentenvelope_behavior_appears" in failure
    assert "real_guardiandecision_behavior_appears" in failure
    assert "approval_enforcement_appears" in failure
    assert "execution_or_side_effects_appear" in failure
    assert "audit_persistence_appears" in failure
    assert "sparkbot_coupling_appears" in failure


def test_doc_says_audit_persistence_is_not_approved() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "It is docs/tests/fixtures only" in phase_doc
    assert "does not implement runtime behavior" in phase_doc
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "Audit proof remains test evidence only until audit persistence is separately approved" in phase_doc
    assert "Runtime implementation remains blocked" in phase_doc


def test_phase_five_runtime_bridge_remains_gated() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase_5_runtime_bridge_remains_gated"] is True
    assert fixture["next_phase"] == "phase_8_4_runtime_implementation_approval_gate_closeout"


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


def test_no_phase_eight_three_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_8_3*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_8_3*"))
