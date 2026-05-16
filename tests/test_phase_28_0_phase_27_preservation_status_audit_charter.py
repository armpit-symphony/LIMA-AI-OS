"""Preservation status audit charter tests for Phase 28.0."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_28_0_PHASE_27_PRESERVATION_STATUS_AUDIT_CHARTER.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_28_0_phase_27_preservation_status_audit_charter.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_28_0_is_preservation_status_audit_charter_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "28.0"
    assert fixture["runtime_code_modified"] is False
    assert "preservation status audit charter only" in phase_doc
    assert "does not implement runtime behavior" in phase_doc


def test_phase_27_0_through_27_4_are_in_audit_scope() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["audited_phases"] == ["27.0", "27.1", "27.2", "27.3", "27.4"]
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    for phase in fixture["audited_phases"]:
        assert f"Phase {phase}" in phase_doc


def test_anti_loop_constraint_is_explicit() -> None:
    constraint = _load_json(PHASE_FIXTURE_PATH)["anti_loop_constraint"]
    assert constraint["endless_preservation_loop_allowed"] is False
    assert constraint["phase_29_must_make_sharper_decision"] is True
    assert constraint["continued_pause_requires_specific_documented_risk"] is True
    assert "must not become an endless preservation loop" in PHASE_DOC_PATH.read_text(
        encoding="utf-8"
    )


def test_allowed_phase_29_decision_types_are_sharper() -> None:
    decision_types = set(_load_json(PHASE_FIXTURE_PATH)["allowed_phase_29_decision_types"])
    assert "no_code_design_review_for_next_narrow_runtime_slice" in decision_types
    assert "additional_test_only_hardening_if_concrete_gap_exists" in decision_types
    assert "continued_pause_if_specific_risk_is_documented" in decision_types


def test_phase_28_lane_is_defined() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase_28_lane"] == [
        "28.0_preservation_status_audit_charter",
        "28.1_stable_runtime_test_state_review",
        "28.2_preservation_pause_justification_review",
        "28.3_phase_29_decision_readiness_matrix",
        "28.4_preservation_status_archive_closeout",
    ]
    assert fixture["next_phase"] == "28.1"


def test_boundary_results_preserve_no_runtime_or_support_change() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True


def test_no_phase_28_0_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_28_0*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_28_0*"))
