"""Future implementation eligibility matrix tests for Phase 29.3."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_29_3_FUTURE_IMPLEMENTATION_ELIGIBILITY_MATRIX.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_29_3_future_implementation_eligibility_matrix.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_29_3_is_eligibility_design_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "29.3"
    assert fixture["runtime_code_modified"] is False
    assert "eligibility design only" in phase_doc
    assert "does not implement runtime behavior" in phase_doc


def test_future_file_scope_is_exact_and_excludes_candidate_files() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    eligible = set(fixture["future_eligible_runtime_files"])
    forbidden = set(fixture["future_forbidden_runtime_files"])
    assert eligible == {
        "lima/kernel/runtime_state.py",
        "lima/kernel/__init__.py_only_if_safe_public_export_required",
    }
    assert "lima/kernel/intake_candidate.py" in forbidden
    assert "lima/kernel/candidate_status.py" in forbidden
    assert "all_other_lima_files" in forbidden
    assert "sparkbot_files" in forbidden
    assert "intentcompiler_runtime_behavior" in forbidden
    assert "guardiandecision_runtime_behavior" in forbidden


def test_eligibility_criteria_require_approval_tests_rollback_and_audit() -> None:
    criteria = _load_json(PHASE_FIXTURE_PATH)["eligibility_criteria"]
    assert criteria["explicit_phil_approval_required"] is True
    assert criteria["exact_runtime_file_scope_required"] is True
    assert criteria["tests_before_runtime_edits"] is True
    assert criteria["rollback_can_remove_runtime_state_and_export"] is True
    assert criteria["audit_proof_required"] is True
    assert criteria["phase_5_runtime_bridge_remains_gated"] is True


def test_eligibility_criteria_preserve_read_only_non_authoritative_boundary() -> None:
    criteria = _load_json(PHASE_FIXTURE_PATH)["eligibility_criteria"]
    assert criteria["deterministic_local_only_read_only"] is True
    assert criteria["non_authoritative_output_only"] is True
    assert criteria["already_existing_non_executing_candidate_state_only"] is True
    assert criteria["execution_allowed_remains_false"] is True
    assert criteria["side_effects_allowed_remains_false"] is True
    assert criteria["approval_state_never_approved"] is True
    assert criteria["unsafe_state_surfaces_blocked_invalid_not_ready_or_needs_review"] is True
    assert criteria["dangerous_wording_does_not_change_output"] is True


def test_future_acceptance_tests_cover_side_effect_and_integration_absence() -> None:
    tests = set(_load_json(PHASE_FIXTURE_PATH)["required_future_acceptance_tests"])
    assert "input_candidate_state_not_mutated" in tests
    assert "no_sparkbot_import_or_wiring" in tests
    assert "no_humaninput_runtime_bridge" in tests
    assert "no_live_adapter" in tests
    assert "no_execution_dispatch_approval_persistence_or_side_effects" in tests


def test_phase_30_approval_question_preserves_all_required_forbidden_scope() -> None:
    question = _load_json(PHASE_FIXTURE_PATH)["phase_30_approval_question"]
    assert "Do you approve Phase 30" in question
    assert "read-only runtime state inspection" in question
    assert "lima/kernel/runtime_state.py" in question
    assert "lima/kernel/__init__.py" in question
    assert "lima/kernel/intake_candidate.py" in question
    assert "lima/kernel/candidate_status.py" in question
    assert "tests/support/" in question
    assert "Sparkbot wiring" in question
    assert "HumanInput runtime bridge behavior" in question
    assert "approval enforcement" in question
    assert "execution" in question
    assert "dispatch" in question
    assert "audit persistence" in question
    assert "hidden side effects" in question


def test_no_phase_29_3_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_29_3*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_29_3*"))
