"""Static checks for Phase 19.4 regression audit archive closeout."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_19_4_PHASE_19_REGRESSION_AUDIT_ARCHIVE_CLOSEOUT.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_19_4_phase_19_regression_audit_archive_closeout.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_docs_tests_fixtures_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "19.4"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False


def test_phase_nineteen_completed_scope_is_archived() -> None:
    completed = set(_load_json(PHASE_FIXTURE_PATH)["completed_scope"])
    assert completed == {
        "phase_19_0_phase_18_regression_hardening_audit_charter",
        "phase_19_1_regression_coverage_review",
        "phase_19_2_remaining_regression_gap_review",
        "phase_19_3_next_lane_decision_matrix",
    }


def test_closeout_lists_what_phase_nineteen_did_and_did_not_add() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert set(fixture["phase_19_added"]) == {
        "docs",
        "fixtures",
        "static_tests",
        "roadmap_state_updates",
    }
    not_added = set(fixture["phase_19_not_added"])
    assert "runtime_behavior" in not_added
    assert "lima_changes" in not_added
    assert "tests_support_changes" in not_added
    assert "sparkbot_wiring" in not_added
    assert "humaninput_runtime_bridge" in not_added
    assert "execution" in not_added
    assert "dispatch" in not_added
    assert "audit_persistence" in not_added


def test_phase_twenty_direction_and_approval_question_are_preserved() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert (
        fixture["recommended_phase_20_direction"]
        == "docs_tests_fixtures_only_no_code_design_lane_for_next_narrow_runtime_slice"
    )
    assert fixture["phase_20_approved"] is False
    assert "Do you approve Phase 20" in fixture["exact_phase_20_approval_question"]
    assert "still forbidding runtime implementation" in fixture["exact_phase_20_approval_question"]


def test_phase_document_preserves_gate_and_forbidden_scope() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "Phase 20 remains unapproved" in phase_doc
    assert "It must not begin without explicit Phil approval" in phase_doc
    assert "No `lima/` changes" in phase_doc
    assert "No `tests/support/` changes" in phase_doc
    assert "No HumanInput runtime bridge" in phase_doc


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["humaninput_runtime_bridge_added"] is False
    assert boundary["live_adapter_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True


def test_no_phase_nineteen_four_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_19_4*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_19_4*"))
