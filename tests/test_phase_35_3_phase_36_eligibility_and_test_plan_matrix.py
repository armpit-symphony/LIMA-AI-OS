"""Phase 36 eligibility and test plan matrix tests for Phase 35.3."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_35_3_PHASE_36_ELIGIBILITY_AND_TEST_PLAN_MATRIX.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_35_3_phase_36_eligibility_and_test_plan_matrix.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_35_3_is_design_only_and_preserves_approval_gate() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "35.3"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_implementation_approved"] is False
    assert fixture["runtime_files_changed_in_phase_35"] == []
    assert fixture["phase_36_approval_question_preserved"] is True
    assert "Do you approve Phase 36" in phase_doc


def test_phase_36_candidate_file_scope_is_explicit() -> None:
    candidate = _load_json(PHASE_FIXTURE_PATH)["phase_36_candidate"]
    assert candidate["allowed_runtime_files_if_approved_later"] == [
        "lima/kernel/candidate_preview.py",
        "lima/kernel/__init__.py_if_safe_public_export_required",
    ]
    assert "lima/kernel/runtime_state.py" in candidate["forbidden_runtime_files"]
    assert "lima/kernel/intake_candidate.py" in candidate["forbidden_runtime_files"]
    assert "lima/kernel/candidate_status.py" in candidate["forbidden_runtime_files"]
    assert candidate["tests_support_changes_allowed"] is False


def test_eligibility_requires_non_executing_local_read_only_behavior() -> None:
    criteria = _load_json(PHASE_FIXTURE_PATH)["eligibility_criteria"]
    assert criteria["deterministic"] is True
    assert criteria["local_only"] is True
    assert criteria["side_effect_free"] is True
    assert criteria["read_only"] is True
    assert criteria["non_authoritative"] is True
    assert criteria["non_executing"] is True
    assert criteria["caller_provided_data_only"] is True
    assert criteria["safe_by_default"] is True
    assert criteria["fully_testable_without_tests_support_changes"] is True


def test_acceptance_tests_cover_safety_and_boundary_requirements() -> None:
    requirements = set(_load_json(PHASE_FIXTURE_PATH)["acceptance_test_requirements"])
    assert "execution_allowed_false" in requirements
    assert "side_effects_allowed_false" in requirements
    assert "approval_false_or_blocked" in requirements
    assert "dispatch_false_or_blocked" in requirements
    assert "persistence_false_or_blocked" in requirements
    assert "phase_5_humaninput_runtime_bridge_gated" in requirements
    assert "sparkbot_wiring_absent" in requirements
    assert "external_calls_and_hidden_side_effects_absent" in requirements
    assert "only_approved_runtime_files_changed" in requirements
    assert "tests_support_unchanged" in requirements


def test_rollback_and_audit_proof_is_defined() -> None:
    proof = set(_load_json(PHASE_FIXTURE_PATH)["rollback_audit_proof"])
    assert "remove_lima_kernel_candidate_preview_py" in proof
    assert "remove_optional_kernel_init_export" in proof
    assert "remove_phase_36_docs_tests_fixtures" in proof
    assert "git_diff_name_only_against_pre_phase_36_main" in proof
    assert "forbidden_import_and_behavior_scan" in proof
    assert "targeted_tests_full_suite_compileall_diff_check_clean_status" in proof


def test_no_phase_35_3_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_35_3*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_35_3*"))
