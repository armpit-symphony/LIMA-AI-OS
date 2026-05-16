"""Runtime slice safety boundary design tests for Phase 29.2."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_29_2_RUNTIME_SLICE_SAFETY_BOUNDARY_DESIGN.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_29_2_runtime_slice_safety_boundary_design.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_29_2_is_safety_boundary_design_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "29.2"
    assert fixture["runtime_code_modified"] is False
    assert "safety boundary design only" in phase_doc
    assert "does not implement runtime behavior" in phase_doc


def test_allowed_future_behavior_is_read_only_and_non_authoritative() -> None:
    allowed = set(_load_json(PHASE_FIXTURE_PATH)["allowed_future_behavior"])
    assert "deterministic_local_only_read_only_inspection" in allowed
    assert "inspect_already_existing_non_executing_runtime_candidate_state" in allowed
    assert "produce_non_authoritative_state_snapshot" in allowed
    assert "report_candidate_safety_flags" in allowed
    assert "report_blocked_not_ready_or_needs_review_signals" in allowed


def test_future_file_scope_is_narrow_and_explicit() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    eligible = set(fixture["future_eligible_runtime_files"])
    forbidden = set(fixture["future_forbidden_runtime_files"])
    assert "lima/kernel/runtime_state.py" in eligible
    assert "lima/kernel/__init__.py_only_if_safe_public_export_required" in eligible
    assert "lima/kernel/intake_candidate.py" in forbidden
    assert "lima/kernel/candidate_status.py" in forbidden
    assert "all_other_lima_files" in forbidden


def test_future_forbidden_behavior_blocks_authority_and_side_effects() -> None:
    forbidden = set(_load_json(PHASE_FIXTURE_PATH)["future_forbidden_behavior"])
    assert "mutate_candidate_state" in forbidden
    assert "create_candidates_from_humaninput" in forbidden
    assert "infer_intentenvelope_runtime_behavior" in forbidden
    assert "preview_guardiandecision_behavior" in forbidden
    assert "approval_enforcement" in forbidden
    assert "audit_persistence" in forbidden
    assert "dispatch" in forbidden
    assert "execution" in forbidden
    assert "external_system_calls" in forbidden
    assert "physical_world_action" in forbidden


def test_safety_invariants_preserve_candidate_guards() -> None:
    invariants = _load_json(PHASE_FIXTURE_PATH)["safety_invariants"]
    assert invariants["output_non_authoritative"] is True
    assert invariants["output_deterministic_local_only"] is True
    assert invariants["execution_allowed_remains_false"] is True
    assert invariants["side_effects_allowed_remains_false"] is True
    assert invariants["approval_state_never_approved"] is True
    assert invariants["unsafe_state_reported_blocked_invalid_not_ready_or_needs_review"] is True
    assert invariants["dangerous_wording_does_not_change_result"] is True
    assert invariants["phase_5_runtime_bridge_remains_gated"] is True


def test_no_phase_29_2_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_29_2*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_29_2*"))
