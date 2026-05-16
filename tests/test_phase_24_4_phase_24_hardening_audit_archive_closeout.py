"""Archive closeout tests for Phase 24.4."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_24_4_PHASE_24_HARDENING_AUDIT_ARCHIVE_CLOSEOUT.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_24_4_phase_24_hardening_audit_archive_closeout.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_24_4_is_archive_closeout_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "24.4"
    assert fixture["runtime_code_modified"] is False
    assert "archive closeout only" in phase_doc
    assert "does not implement runtime behavior" in phase_doc


def test_phase_24_0_through_24_3_are_archived() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["archived_phases"] == ["24.0", "24.1", "24.2", "24.3"]
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    for phase in fixture["archived_phases"]:
        assert f"Phase {phase}" in phase_doc


def test_archive_results_preserve_boundaries() -> None:
    archive_results = _load_json(PHASE_FIXTURE_PATH)["archive_results"]
    assert archive_results["phase_23_remained_test_only"] is True
    assert archive_results["phase_24_remained_docs_tests_fixtures_only"] is True
    assert archive_results["runtime_files_changed"] is False
    assert archive_results["tests_support_changed"] is False
    assert archive_results["phase_5_runtime_bridge_remains_gated"] is True


def test_recommended_phase_25_direction_is_test_only_hardening() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["recommended_phase_25_direction"] == (
        "test_only_cross_api_candidate_invariant_matrix_hardening"
    )


def test_phase_25_approval_question_preserves_forbidden_scope() -> None:
    question = _load_json(PHASE_FIXTURE_PATH)["phase_25_approval_question"]
    assert "test-only hardening lane" in question
    assert "cross-API candidate invariant matrix" in question
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


def test_boundary_results_show_no_forbidden_behavior_and_phase_25_gate() -> None:
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
    assert boundary["phase_25_requires_explicit_approval"] is True


def test_phase_doc_stops_after_phase_24_4() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "Stop after Phase 24.4" in phase_doc
    assert "Phase 25 requires explicit approval" in phase_doc


def test_no_phase_24_4_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_24_4*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_24_4*"))
