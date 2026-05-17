"""Phase 35 design review archive closeout tests for Phase 35.4."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_35_4_PHASE_35_DESIGN_REVIEW_ARCHIVE_CLOSEOUT.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_35_4_phase_35_design_review_archive_closeout.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_35_4_archives_design_review_without_runtime_approval() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "35.4"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_implementation_approved"] is False
    assert fixture["runtime_files_changed_in_phase_35"] == []
    assert fixture["phase_36_approval_question_preserved"] is True
    assert "Phase 36 requires explicit Phil approval" in phase_doc


def test_phase_35_completed_phases_are_archived() -> None:
    phases = _load_json(PHASE_FIXTURE_PATH)["phase_35_completed_phases"]
    assert phases == [
        "35.0_phase_34_second_slice_design_audit_charter",
        "35.1_second_runtime_slice_candidate_inventory",
        "35.2_second_slice_safety_and_scope_comparison",
        "35.3_phase_36_eligibility_and_test_plan_matrix",
        "35.4_phase_35_design_review_archive_closeout",
    ]


def test_phase_35_reviewed_all_candidate_second_runtime_slices() -> None:
    reviewed = _load_json(PHASE_FIXTURE_PATH)["candidate_second_runtime_slices_reviewed"]
    assert len(reviewed) == 8
    assert "C_non_executing_candidate_preview_helper" in reviewed
    assert "F_humaninput_bridge_boundary_planning_only" in reviewed
    assert "G_sparkbot_integration_boundary_planning_only" in reviewed


def test_phase_36_file_scope_remains_explicit_and_bounded() -> None:
    scope = _load_json(PHASE_FIXTURE_PATH)["phase_36_file_scope_if_approved"]
    assert scope["allowed_runtime_files"] == [
        "lima/kernel/candidate_preview.py",
        "lima/kernel/__init__.py_if_safe_public_export_required",
    ]
    assert "lima/kernel/runtime_state.py" in scope["forbidden_runtime_files"]
    assert "lima/kernel/intake_candidate.py" in scope["forbidden_runtime_files"]
    assert "lima/kernel/candidate_status.py" in scope["forbidden_runtime_files"]
    assert scope["tests_support_changes_allowed"] is False


def test_phase_36_acceptance_requirements_preserve_boundaries() -> None:
    requirements = set(_load_json(PHASE_FIXTURE_PATH)["phase_36_acceptance_test_requirements"])
    assert "execution_allowed_false" in requirements
    assert "side_effects_allowed_false" in requirements
    assert "approval_false_or_blocked" in requirements
    assert "dispatch_false_or_blocked" in requirements
    assert "persistence_false_or_blocked" in requirements
    assert "phase_5_humaninput_runtime_bridge_gated" in requirements
    assert "sparkbot_wiring_absent" in requirements
    assert "live_adapters_absent" in requirements
    assert "external_calls_and_hidden_side_effects_absent" in requirements
    assert "tests_support_unchanged" in requirements


def test_phase_36_stop_conditions_cover_forbidden_scope() -> None:
    stop_conditions = set(_load_json(PHASE_FIXTURE_PATH)["phase_36_stop_conditions_include"])
    assert "forbidden_lima_changes" in stop_conditions
    assert "tests_support_changes" in stop_conditions
    assert "humaninput_runtime_bridge_behavior" in stop_conditions
    assert "sparkbot_wiring" in stop_conditions
    assert "execution" in stop_conditions
    assert "persistence_or_audit_persistence" in stop_conditions
    assert "robotics_or_physical_world_behavior" in stop_conditions
    assert "workers_queues_daemons_subprocesses_threads_database_writes_hidden_side_effects" in stop_conditions


def test_no_phase_35_4_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_35_4*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_35_4*"))
