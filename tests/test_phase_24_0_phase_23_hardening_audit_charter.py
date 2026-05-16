"""Audit charter tests for Phase 24.0."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_24_0_PHASE_23_HARDENING_AUDIT_CHARTER.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_24_0_phase_23_hardening_audit_charter.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_24_0_is_docs_tests_fixtures_only_audit_charter() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "24.0"
    assert fixture["scope"] == "docs_tests_fixtures_only"
    assert fixture["runtime_code_modified"] is False
    assert "audit charter only" in phase_doc
    assert "does not implement runtime behavior" in phase_doc


def test_phase_24_0_audits_phase_23_hardening_package() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["audited_package"] == "phase_23_test_only_hardening"
    assert "provenance_preservation" in fixture["audit_focus"]
    assert "bypass_wording_resistance" in fixture["audit_focus"]
    assert "non_executing_candidate_invariants" in fixture["audit_focus"]


def test_phase_24_lane_is_declared() -> None:
    lane = _load_json(PHASE_FIXTURE_PATH)["phase_24_lane"]
    assert lane == [
        "24.0_hardening_audit_charter",
        "24.1_provenance_hardening_coverage_review",
        "24.2_remaining_candidate_invariant_gap_review",
        "24.3_next_lane_decision_matrix",
        "24.4_hardening_audit_archive_closeout",
    ]


def test_boundary_results_show_no_forbidden_behavior() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["humaninput_runtime_bridge_added"] is False
    assert boundary["live_adapter_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["approval_enforcement_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_behavior_added"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True


def test_phase_doc_gates_phase_24_1_and_runtime_expansion() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "Phase 24.1 may review Phase 23 provenance hardening coverage only" in phase_doc
    assert "Runtime expansion remains blocked" in phase_doc


def test_no_phase_24_0_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_24_0*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_24_0*"))
