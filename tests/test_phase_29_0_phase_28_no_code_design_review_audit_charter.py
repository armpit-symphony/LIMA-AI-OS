"""No-code design review audit charter tests for Phase 29.0."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_29_0_PHASE_28_NO_CODE_DESIGN_REVIEW_AUDIT_CHARTER.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_29_0_phase_28_no_code_design_review_audit_charter.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_29_0_is_design_review_audit_charter_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "29.0"
    assert fixture["runtime_code_modified"] is False
    assert "design review audit charter only" in phase_doc
    assert "does not implement runtime behavior" in phase_doc


def test_phase_28_0_through_28_4_are_in_audit_scope() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["audited_phases"] == ["28.0", "28.1", "28.2", "28.3", "28.4"]
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    for phase in fixture["audited_phases"]:
        assert f"Phase {phase}" in phase_doc


def test_review_purpose_covers_design_readiness() -> None:
    purpose = set(_load_json(PHASE_FIXTURE_PATH)["review_purpose"])
    assert "identify_candidate_options" in purpose
    assert "recommend_one_future_slice" in purpose
    assert "define_strict_eligibility_criteria" in purpose
    assert "define_non_goals" in purpose
    assert "preserve_safety_invariants" in purpose
    assert "define_required_test_only_evidence" in purpose
    assert "prepare_phase_30_approval_question" in purpose


def test_boundary_blocks_runtime_and_forbidden_scope() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary"]
    assert boundary["runtime_implementation_approved"] is False
    assert boundary["lima_changes_allowed"] is False
    assert boundary["tests_support_changes_allowed"] is False
    assert boundary["sparkbot_wiring_allowed"] is False
    assert boundary["humaninput_runtime_bridge_allowed"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True


def test_next_phase_is_candidate_inventory() -> None:
    assert _load_json(PHASE_FIXTURE_PATH)["next_phase"] == "29.1"
    assert "Continue only to Phase 29.1" in PHASE_DOC_PATH.read_text(encoding="utf-8")


def test_no_phase_29_0_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_29_0*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_29_0*"))
