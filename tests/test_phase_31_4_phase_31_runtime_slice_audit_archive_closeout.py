"""Phase 31 runtime slice audit archive tests for Phase 31.4."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_31_4_PHASE_31_RUNTIME_SLICE_AUDIT_ARCHIVE_CLOSEOUT.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_31_4_phase_31_runtime_slice_audit_archive_closeout.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_31_4_archives_phase_31_audit_lane() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "31.4"
    assert fixture["phase_30_audit_result"] == "PASS"
    assert fixture["runtime_code_modified"] is False
    assert fixture["completed_phases"] == ["31.0", "31.1", "31.2", "31.3"]
    assert "completed docs/tests/fixtures-only audit/archive" in phase_doc


def test_archive_records_no_phase_31_runtime_file_changes() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase_30_runtime_files_changed"] == [
        "lima/kernel/runtime_state.py",
        "lima/kernel/__init__.py",
    ]
    assert fixture["runtime_state_py_changed_in_phase_31"] is False
    assert fixture["kernel_init_changed_in_phase_31"] is False
    assert fixture["forbidden_lima_files_changed_in_phase_31"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["runtime_behavior_changed_in_phase_31"] is False


def test_archive_confirms_runtime_boundaries_remain_gated() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase_5_runtime_bridge_remains_gated"] is True
    assert fixture["execution_approval_dispatch_persistence_absent"] is True
    assert fixture["sparkbot_wiring_imports_absent"] is True
    assert fixture["shell_browser_network_file_robotics_physical_world_absent"] is True
    assert fixture["blocking_safety_regression_found"] is False


def test_remaining_gaps_are_non_blocking_and_gated() -> None:
    gaps = set(_load_json(PHASE_FIXTURE_PATH)["remaining_gaps"])
    assert "additional_nested_suspicious_metadata_fixtures_only_if_concrete_gap_identified" in gaps
    assert "future_runtime_slice_requires_no_code_design_review_and_explicit_approval" in gaps
    assert "humaninput_sparkbot_robo_os_boundary_planning_remains_separate_and_gated" in gaps


def test_phase_32_recommendation_and_question_are_preserved() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    question = fixture["phase_32_approval_question"]
    assert fixture["recommended_phase_32_direction"] == (
        "docs_tests_fixtures_only_design_review_for_next_narrow_runtime_slice"
    )
    assert "Do you approve Phase 32" in question
    assert "docs/tests/fixtures-only design review" in question
    assert "no new runtime implementation" in question
    assert "no new `lima/` changes" in question
    assert "no `tests/support/` changes" in question
    assert "no Sparkbot wiring" in question
    assert "no HumanInput runtime bridge behavior" in question
    assert "no execution" in question
    assert "no dispatch" in question
    assert "no hidden side effects" in question


def test_no_phase_31_4_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_31_4*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_31_4*"))
