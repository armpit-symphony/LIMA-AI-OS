"""Archive closeout tests for Phase 37.4."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_37_4_PHASE_37_CANDIDATE_PREVIEW_AUDIT_ARCHIVE_CLOSEOUT.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_37_4_phase_37_candidate_preview_audit_archive_closeout.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_37_4_archives_completed_phase_37_lane() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "37.4"
    assert fixture["phase_36_audit_result"] == "PASS"
    assert fixture["phase_37_result"] == "PASS"
    assert fixture["completed_phases"] == ["37.0", "37.1", "37.2", "37.3", "37.4"]
    assert "Phase 37 result: PASS." in PHASE_DOC_PATH.read_text(encoding="utf-8")


def test_phase_37_4_remains_docs_tests_fixtures_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_files_changed_in_phase_37"] == []
    assert fixture["runtime_behavior_changed_after_phase_36"] is False
    assert fixture["tests_support_changed_in_phase_37"] is False
    assert fixture["stale_prior_phase_tests_changed_in_phase_37"] is False


def test_phase_37_4_confirms_runtime_files_unchanged_after_phase_36() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["candidate_preview_changed_after_phase_36"] is False
    assert fixture["kernel_init_changed_after_phase_36"] is False
    assert fixture["runtime_state_changed_in_phase_37"] is False
    assert fixture["intake_candidate_changed_in_phase_37"] is False
    assert fixture["candidate_status_changed_in_phase_37"] is False


def test_phase_37_4_confirms_forbidden_behavior_absent() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    forbidden_absence_flags = [
        "execution_absent",
        "approval_enforcement_absent",
        "approval_grant_behavior_absent",
        "dispatch_absent",
        "persistence_absent",
        "audit_persistence_absent",
        "sparkbot_wiring_imports_absent",
        "humaninput_runtime_bridge_absent",
        "live_adapters_absent",
        "intentcompiler_runtime_behavior_changes_absent",
        "guardiandecision_runtime_behavior_changes_absent",
        "shell_browser_network_file_mutation_absent",
        "robotics_physical_world_behavior_absent",
        "external_calls_absent",
        "background_work_absent",
        "subprocesses_threads_queues_daemons_absent",
        "database_writes_hidden_side_effects_absent",
    ]
    assert all(fixture[flag] is True for flag in forbidden_absence_flags)
    assert fixture["phase_5_runtime_bridge_gated"] is True


def test_phase_37_4_recommends_pause_without_new_approval_question() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["remaining_gaps"] == []
    assert fixture["recommended_next_direction"] == "pause_and_preserve_current_runtime_test_state"
    assert fixture["phase_38_approval_question_required"] is False
    doc_text = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "Pause and preserve the current runtime/test state." in doc_text
    assert "No Phase 38 approval question is required by this closeout" in doc_text


def test_no_phase_37_4_files_exist_under_lima_tests_support_or_old_phase_tests() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_37_4*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_37_4*"))
    assert not list((REPO_ROOT / "tests").glob("test_phase_35_*phase_37_4*"))
