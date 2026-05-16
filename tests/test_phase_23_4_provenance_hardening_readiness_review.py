"""Readiness review tests for Phase 23.4."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_23_4_PROVENANCE_HARDENING_READINESS_REVIEW.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_23_4_provenance_hardening_readiness_review.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_23_4_is_readiness_review_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "23.4"
    assert fixture["runtime_code_modified"] is False
    assert fixture["readiness_result"] == "ready_for_phase_23_archive_closeout"
    assert "docs/tests/fixtures-only readiness review" in phase_doc
    assert "does not implement runtime behavior" in phase_doc


def test_phase_23_0_through_23_3_are_reviewed() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["reviewed_phases"] == ["23.0", "23.1", "23.2", "23.3"]
    assert "phase_23_1_candidate_provenance_regression_tests" in fixture["coverage_reviewed"]
    assert "phase_23_2_suspicious_provenance_fixture_hardening" in fixture["coverage_reviewed"]
    assert "phase_23_3_bypass_wording_provenance_tests" in fixture["coverage_reviewed"]


def test_readiness_review_preserves_static_test_limitations() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert "static_and_test_scope_only" in fixture["limitations"]
    assert "does_not_approve_runtime_expansion" in fixture["limitations"]
    assert "does_not_add_runtime_behavior" in fixture["limitations"]


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
    assert boundary["phase_24_remains_gated"] is True


def test_phase_document_gates_archive_and_phase_24() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "Phase 23.5 may archive Phase 23 only" in phase_doc
    assert "Phase 24 remains gated" in phase_doc


def test_no_phase_23_4_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_23_4*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_23_4*"))
