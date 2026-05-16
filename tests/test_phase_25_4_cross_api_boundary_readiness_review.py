"""Readiness review tests for Phase 25.4."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_25_4_CROSS_API_BOUNDARY_READINESS_REVIEW.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_25_4_cross_api_boundary_readiness_review.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_25_4_is_readiness_review_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "25.4"
    assert fixture["runtime_code_modified"] is False
    assert fixture["readiness_result"] == "ready_for_phase_25_archive_closeout"
    assert "docs/tests/fixtures-only readiness review" in phase_doc


def test_phase_25_0_through_25_3_are_reviewed() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["reviewed_phases"] == ["25.0", "25.1", "25.2", "25.3"]
    confirmed = set(fixture["confirmed_results"])
    assert "cross_api_matrix_fixtures_exist" in confirmed
    assert "candidate_construction_non_executing" in confirmed
    assert "status_normalization_non_executing" in confirmed
    assert "candidate_validation_non_executing" in confirmed
    assert "provenance_and_status_handling_safe" in confirmed


def test_boundary_results_show_no_forbidden_behavior_and_phase_26_gate() -> None:
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
    assert boundary["phase_26_requires_explicit_approval"] is True


def test_phase_doc_gates_phase_25_5() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "Phase 25.5 may archive Phase 25 only" in phase_doc
    assert "Phase 26 requires explicit approval" in phase_doc


def test_no_phase_25_4_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_25_4*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_25_4*"))
