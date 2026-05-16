"""Archive closeout tests for Phase 25.5."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_25_5_PHASE_25_TEST_ONLY_HARDENING_ARCHIVE_CLOSEOUT.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_25_5_phase_25_test_only_hardening_archive_closeout.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_25_5_is_archive_closeout_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "25.5"
    assert fixture["runtime_code_modified"] is False
    assert "archive closeout only" in phase_doc
    assert "does not implement runtime behavior" in phase_doc


def test_phase_25_0_through_25_4_are_archived() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["archived_phases"] == ["25.0", "25.1", "25.2", "25.3", "25.4"]
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    for phase in fixture["archived_phases"]:
        assert f"Phase {phase}" in phase_doc


def test_archive_results_preserve_boundaries() -> None:
    archive_results = _load_json(PHASE_FIXTURE_PATH)["archive_results"]
    assert archive_results["phase_25_remained_test_only"] is True
    assert archive_results["runtime_files_changed"] is False
    assert archive_results["tests_support_changed"] is False
    assert archive_results["cross_api_candidate_invariant_matrix_added"] is True
    assert archive_results["phase_5_runtime_bridge_remains_gated"] is True


def test_archived_coverage_lists_core_candidate_invariants() -> None:
    coverage = set(_load_json(PHASE_FIXTURE_PATH)["coverage_archived"])
    assert "candidate_construction_non_executing" in coverage
    assert "status_normalization_non_executing" in coverage
    assert "candidate_validation_non_executing" in coverage
    assert "valid_provenance_preserved" in coverage
    assert "unknown_status_blocked" in coverage
    assert "suspicious_provenance_invalid_or_blocked" in coverage
    assert "stale_replayed_candidates_invalid_or_blocked" in coverage
    assert "bypass_wording_not_approved" in coverage
    assert "risky_action_categories_need_review" in coverage


def test_phase_26_approval_question_preserves_forbidden_scope() -> None:
    question = _load_json(PHASE_FIXTURE_PATH)["phase_26_approval_question"]
    assert "docs/tests/fixtures-only audit/archive" in question
    assert "runtime implementation" in question
    assert "lima/ changes" in question
    assert "tests/support/ changes" in question
    assert "Sparkbot wiring" in question
    assert "HumanInput runtime bridge" in question
    assert "approval enforcement" in question
    assert "execution" in question
    assert "dispatch" in question
    assert "audit persistence" in question
    assert "physical-world action" in question
    assert "hidden side effects" in question


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


def test_phase_doc_stops_after_phase_25_5() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "Stop after Phase 25.5" in phase_doc
    assert "Phase 26 requires explicit approval" in phase_doc


def test_no_phase_25_5_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_25_5*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_25_5*"))
