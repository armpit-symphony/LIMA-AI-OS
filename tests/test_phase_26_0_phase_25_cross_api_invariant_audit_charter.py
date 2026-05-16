"""Audit charter tests for Phase 26.0."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_26_0_PHASE_25_CROSS_API_INVARIANT_AUDIT_CHARTER.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_26_0_phase_25_cross_api_invariant_audit_charter.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_26_0_is_docs_tests_fixtures_only_audit_charter() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "26.0"
    assert fixture["runtime_code_modified"] is False
    assert "audit charter only" in phase_doc
    assert "does not implement runtime behavior" in phase_doc


def test_phase_25_0_through_25_5_are_in_audit_scope() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["audited_phases"] == ["25.0", "25.1", "25.2", "25.3", "25.4", "25.5"]
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    for phase in fixture["audited_phases"]:
        assert f"Phase {phase}" in phase_doc


def test_audit_focus_covers_cross_api_candidate_invariants() -> None:
    focus = set(_load_json(PHASE_FIXTURE_PATH)["audit_focus"])
    assert "candidate_construction_invariants" in focus
    assert "candidate_status_normalization_invariants" in focus
    assert "candidate_validation_invariants" in focus
    assert "provenance_hardening_invariants" in focus
    assert "phase_25_remained_test_only" in focus
    assert "phase_5_runtime_bridge_remains_gated" in focus


def test_phase_26_lane_is_defined_and_stays_gated() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase_26_lane"] == [
        "26.0_audit_charter",
        "26.1_cross_api_invariant_coverage_review",
        "26.2_remaining_cross_api_gap_review",
        "26.3_next_lane_decision_matrix",
        "26.4_archive_closeout",
    ]
    assert fixture["next_phase"] == "26.1"


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
    assert (
        boundary["shell_browser_network_file_mutation_robotics_physical_world_behavior_added"]
        is False
    )
    assert boundary["external_service_calls_added"] is False
    assert boundary["background_worker_queue_daemon_subprocess_thread_database_write_added"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True


def test_no_phase_26_0_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_26_0*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_26_0*"))
