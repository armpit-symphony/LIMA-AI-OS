"""Phase 32 design review archive closeout tests for Phase 32.4."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_32_4_PHASE_32_DESIGN_REVIEW_ARCHIVE_CLOSEOUT.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_32_4_phase_32_design_review_archive_closeout.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_32_4_archives_completed_phase_32_scope() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "32.4"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_implementation_approved"] is False
    assert fixture["phase_32_completed_phases"] == ["32.0", "32.1", "32.2", "32.3"]
    assert "archives Phase 32 as a completed docs/tests/fixtures-only design review" in phase_doc


def test_phase_32_4_records_no_runtime_or_support_changes() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase_32_runtime_files_changed"] == []
    assert fixture["runtime_state_py_changed_in_phase_32"] is False
    assert fixture["kernel_init_changed_in_phase_32"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["runtime_behavior_changed"] is False


def test_phase_32_4_records_boundary_absence() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase_5_runtime_bridge_remains_gated"] is True
    assert fixture["execution_approval_dispatch_persistence_absent"] is True
    assert fixture["sparkbot_wiring_imports_absent"] is True
    assert fixture["shell_browser_network_file_robotics_physical_world_absent"] is True


def test_phase_32_4_records_all_candidate_slices_reviewed() -> None:
    reviewed = set(_load_json(PHASE_FIXTURE_PATH)["candidate_slices_reviewed"])
    assert reviewed == {
        "runtime_state_test_only_hardening",
        "second_read_only_runtime_inspection_slice",
        "non_executing_candidate_preview_helper",
        "candidate_status_read_only_normalization_hardening",
        "humaninput_bridge_boundary_planning_only",
        "sparkbot_integration_boundary_planning_only",
        "pause_and_preserve_state",
    }


def test_phase_32_4_recommends_test_only_phase_33() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["recommended_phase_33_direction"] == "test_only_runtime_state_hardening"
    assert fixture["recommended_phase_33_implementation_file_scope"] == []


def test_phase_32_4_preserves_exact_phase_33_approval_question() -> None:
    question = _load_json(PHASE_FIXTURE_PATH)["approval_question"]
    assert question.startswith("Do you approve Phase 33 as a test-only hardening lane")
    assert "no runtime implementation" in question
    assert "no new `lima/` changes" in question
    assert "no `tests/support/` changes" in question
    assert "no Sparkbot wiring" in question
    assert "no HumanInput runtime bridge behavior" in question
    assert "no hidden side effects" in question


def test_no_phase_32_4_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_32_4*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_32_4*"))
