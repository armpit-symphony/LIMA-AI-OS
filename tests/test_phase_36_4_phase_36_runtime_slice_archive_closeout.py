"""Phase 36 runtime slice archive closeout tests for Phase 36.4."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_36_4_PHASE_36_RUNTIME_SLICE_ARCHIVE_CLOSEOUT.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_36_4_phase_36_runtime_slice_archive_closeout.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_36_4_archives_without_new_runtime_behavior() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "36.4"
    assert fixture["runtime_behavior_added_in_phase_36_4"] is False
    assert fixture["runtime_files_changed_in_phase_36_4"] == []
    assert "Phase 37 requires explicit approval" in phase_doc


def test_phase_36_completed_phases_are_archived() -> None:
    phases = _load_json(PHASE_FIXTURE_PATH)["phase_36_completed_phases"]
    assert phases == [
        "36.0_phase_35_runtime_implementation_audit_charter",
        "36.1_candidate_preview_acceptance_design",
        "36.2_candidate_preview_runtime_implementation",
        "36.3_candidate_preview_boundary_regression_review",
        "36.4_phase_36_runtime_slice_archive_closeout",
    ]


def test_phase_36_runtime_file_scope_is_recorded() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase_36_runtime_files_changed"] == [
        "lima/kernel/candidate_preview.py",
        "lima/kernel/__init__.py",
    ]
    assert fixture["candidate_preview_py_added"] is True
    assert fixture["kernel_init_changed_for_safe_export"] is True
    assert fixture["runtime_state_py_changed"] is False
    assert fixture["intake_candidate_py_changed"] is False
    assert fixture["candidate_status_py_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["forbidden_lima_files_changed"] is False


def test_candidate_preview_safety_result_is_archived() -> None:
    safety = _load_json(PHASE_FIXTURE_PATH)["candidate_preview_safety_result"]
    assert all(safety.values())
    assert safety["non_authoritative"] is True
    assert safety["non_executing"] is True
    assert safety["execution_absent"] is True
    assert safety["approval_absent"] is True
    assert safety["dispatch_absent"] is True
    assert safety["persistence_absent"] is True
    assert safety["robotics_physical_world_absent"] is True


def test_stale_phase_35_test_adjustment_is_archived() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["stale_phase_35_test_adjusted"] is True
    assert (
        fixture["stale_phase_35_test_adjusted_file"]
        == "tests/test_phase_35_1_second_runtime_slice_candidate_inventory.py"
    )
    assert fixture["other_old_phase_tests_changed"] is False


def test_phase_37_recommendation_is_audit_archive_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert (
        fixture["recommended_phase_37_direction"]
        == "docs_tests_fixtures_only_audit_archive_next_lane_decision"
    )
    assert fixture["phase_37_approval_question_preserved"] is True


def test_no_phase_36_4_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_36_4*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_36_4*"))
