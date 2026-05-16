"""Static checks for Phase 18.5 regression hardening archive closeout."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_18_5_PHASE_18_REGRESSION_HARDENING_ARCHIVE_CLOSEOUT.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_18_5_phase_18_regression_hardening_archive_closeout.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_archive_closeout_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "18.5"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False


def test_completed_phase_eighteen_scope_is_listed() -> None:
    completed = set(_load_json(PHASE_FIXTURE_PATH)["completed_phase_18_scope"])
    assert completed == {
        "phase_18_0_regression_hardening_charter",
        "phase_18_1_candidate_api_regression_tests",
        "phase_18_2_acceptance_boundary_regression_fixtures",
        "phase_18_3_forbidden_integration_regression_tests",
        "phase_18_4_regression_hardening_readiness_review",
    }


def test_archive_lists_what_phase_eighteen_added_and_did_not_add() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    added = set(fixture["phase_18_added"])
    did_not_add = set(fixture["phase_18_did_not_add"])
    assert "test_only_candidate_api_regression_coverage" in added
    assert "test_only_forbidden_integration_regression_checks" in added
    assert "synthetic_acceptance_boundary_regression_fixtures" in added
    assert "lima_changes" in did_not_add
    assert "tests_support_changes" in did_not_add
    assert "runtime_behavior_changes" in did_not_add
    assert "sparkbot_wiring" in did_not_add
    assert "humaninput_runtime_bridge" in did_not_add
    assert "execution" in did_not_add
    assert "dispatch" in did_not_add
    assert "audit_persistence" in did_not_add
    assert "physical_world_side_effects" in did_not_add


def test_phase_nineteen_gate_is_explicit() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["recommended_phase_19_direction"].startswith("docs_tests_fixtures_only")
    gate = fixture["phase_19_gate"]
    assert gate["phase_19_approved"] is False
    assert "Do you approve Phase 19" in gate["approval_question"]
    assert "docs/tests/fixtures-only" in gate["approval_question"]
    assert "runtime implementation" in gate["approval_question"]
    assert "lima/ changes" in gate["approval_question"]
    assert "tests/support/ changes" in gate["approval_question"]
    assert "physical-world action" in gate["approval_question"]


def test_phase_document_preserves_archive_boundaries() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "does not change runtime behavior" in phase_doc
    assert "Phase 19 is not approved by this closeout" in phase_doc


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["helper_behavior_changed"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["humaninput_runtime_bridge_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True


def test_no_phase_eighteen_five_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_18_5*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_18_5*"))
