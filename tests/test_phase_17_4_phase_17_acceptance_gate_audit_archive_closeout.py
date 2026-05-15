"""Static checks for Phase 17.4 acceptance-gate audit archive closeout."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_17_4_PHASE_17_ACCEPTANCE_GATE_AUDIT_ARCHIVE_CLOSEOUT.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_17_4_phase_17_acceptance_gate_audit_archive_closeout.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_archive_closeout_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "17.4"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False


def test_completed_phase_seventeen_scope_is_listed() -> None:
    completed = set(_load_json(PHASE_FIXTURE_PATH)["completed_phase_17_scope"])
    assert completed == {
        "phase_17_0_phase_16_acceptance_test_audit_charter",
        "phase_17_1_acceptance_test_coverage_review",
        "phase_17_2_remaining_safety_gap_review",
        "phase_17_3_next_lane_decision_matrix",
    }


def test_archive_result_keeps_phase_sixteen_test_only() -> None:
    archive = _load_json(PHASE_FIXTURE_PATH)["archive_result"]
    assert archive["phase_16_acceptance_tests_archived"] is True
    assert archive["phase_16_acceptance_tests_remain_test_only"] is True
    assert archive["phase_16_tests_strengthen_gate"] is True
    assert archive["runtime_implementation_approved"] is False
    assert archive["lima_changes_approved"] is False
    assert archive["tests_support_changes_approved"] is False
    assert archive["sparkbot_wiring_approved"] is False
    assert archive["humaninput_runtime_bridge_approved"] is False
    assert archive["approval_enforcement_approved"] is False
    assert archive["physical_world_behavior_approved"] is False


def test_phase_eighteen_gate_preserves_exact_recommended_direction() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["recommended_phase_18_direction"].startswith("test_only_regression_hardening_lane")
    gate = fixture["phase_18_gate"]
    assert gate["phase_18_approved"] is False
    assert "Do you approve Phase 18" in gate["approval_question"]
    assert "test-only regression hardening lane" in gate["approval_question"]
    assert "tests/docs/fixtures only" in gate["approval_question"]
    assert "runtime implementation" in gate["approval_question"]
    assert "lima/ changes" in gate["approval_question"]
    assert "tests/support/ changes" in gate["approval_question"]
    assert "physical-world action" in gate["approval_question"]


def test_phase_document_preserves_closeout_boundaries() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "does not change runtime behavior" in phase_doc
    assert "Phase 18 is not approved by this closeout" in phase_doc
    assert "test-only regression hardening lane" in phase_doc


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["humaninput_runtime_bridge_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True


def test_no_phase_seventeen_four_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_17_4*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_17_4*"))
