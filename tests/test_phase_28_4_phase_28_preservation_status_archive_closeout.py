"""Preservation status archive closeout tests for Phase 28.4."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_28_4_PHASE_28_PRESERVATION_STATUS_ARCHIVE_CLOSEOUT.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_28_4_phase_28_preservation_status_archive_closeout.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_28_4_is_archive_closeout_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "28.4"
    assert fixture["runtime_code_modified"] is False
    assert "archive closeout only" in phase_doc
    assert "does not implement runtime behavior" in phase_doc


def test_phase_28_0_through_28_3_are_archived() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["archived_phases"] == ["28.0", "28.1", "28.2", "28.3"]
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    for phase in fixture["archived_phases"]:
        assert f"Phase {phase}" in phase_doc


def test_phase_27_audit_result_is_pass() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase_27_audit_result"] == "PASS"
    assert "Phase 27 audit result: PASS" in PHASE_DOC_PATH.read_text(encoding="utf-8")


def test_archive_results_explain_pause_is_not_default() -> None:
    archive = _load_json(PHASE_FIXTURE_PATH)["archive_results"]
    assert archive["phase_28_remained_docs_tests_fixtures_only"] is True
    assert archive["runtime_files_changed"] is False
    assert archive["tests_support_changed"] is False
    assert archive["runtime_behavior_changed"] is False
    assert archive["phase_5_runtime_bridge_remains_gated"] is True
    assert archive["continued_preservation_pause_is_safe"] is True
    assert archive["continued_preservation_pause_is_sharpest_default"] is False
    assert archive["concrete_test_only_gap_found"] is False
    assert archive["specific_pause_risk_found"] is False


def test_phase_29_recommendation_is_no_code_design_review() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["recommended_phase_29_direction"] == (
        "docs_tests_fixtures_only_no_code_design_review_for_next_narrow_runtime_slice"
    )
    assert "This is not runtime implementation approval" in PHASE_DOC_PATH.read_text(
        encoding="utf-8"
    )


def test_phase_29_approval_question_preserves_forbidden_scope() -> None:
    question = _load_json(PHASE_FIXTURE_PATH)["phase_29_approval_question"]
    assert "docs/tests/fixtures-only no-code design review" in question
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


def test_boundary_results_show_no_forbidden_behavior_and_phase_29_gate() -> None:
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
    assert boundary["phase_29_requires_explicit_approval"] is True


def test_stop_after_phase_28_4() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "Stop after Phase 28.4" in phase_doc
    assert "Phase 29 requires explicit approval" in phase_doc


def test_no_phase_28_4_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_28_4*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_28_4*"))
