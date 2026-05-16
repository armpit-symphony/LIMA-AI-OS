"""Closeout checks for the Phase 22 decision gate."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_22_4_PHASE_22_DECISION_GATE_CLOSEOUT.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_22_4_phase_22_decision_gate_closeout.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_22_4_closes_no_code_decision_lane() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "22.4"
    assert fixture["runtime_code_modified"] is False
    assert fixture["completed_phase_22_scope"] == [
        "phase_22_0_post_phase_21_runtime_slice_audit_charter",
        "phase_22_1_candidate_provenance_coverage_review",
        "phase_22_2_remaining_safety_gap_review",
        "phase_22_3_next_lane_decision_matrix",
    ]


def test_phase_23_direction_and_gate_are_preserved() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["recommended_phase_23_direction"] == (
        "test_only_hardening_for_provenance_candidate_invariants"
    )
    assert fixture["phase_23_requires_explicit_phil_approval"] is True
    question = fixture["phase_23_approval_question"]
    assert "test-only hardening lane" in question
    assert "runtime implementation" in question
    assert "lima/ changes" in question
    assert "tests/support/ changes" in question
    assert "hidden side effects" in question


def test_phase_document_requires_stop_before_phase_23() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "docs/tests/fixtures-only Phase 22 decision lane" in phase_doc
    assert "Stop after Phase 22.4" in phase_doc
    assert "Phase 23 must not begin without explicit Phil approval" in phase_doc
    assert "does not modify `lima/`" in phase_doc


def test_boundary_results_show_no_forbidden_behavior() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["humaninput_runtime_bridge_added"] is False
    assert boundary["live_adapter_added"] is False
    assert boundary["intentcompiler_runtime_behavior_changed"] is False
    assert boundary["guardiandecision_runtime_behavior_changed"] is False
    assert boundary["approval_enforcement_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["shell_browser_network_file_mutation_robotics_physical_world_added"] is False
    assert boundary["background_worker_queue_daemon_subprocess_thread_database_write_added"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True


def test_no_phase_22_4_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_22_4*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_22_4*"))
