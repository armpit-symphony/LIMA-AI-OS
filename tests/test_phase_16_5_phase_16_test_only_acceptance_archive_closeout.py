"""Static checks for Phase 16.5 test-only acceptance archive closeout."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_16_5_PHASE_16_TEST_ONLY_ACCEPTANCE_ARCHIVE_CLOSEOUT.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_16_5_phase_16_test_only_acceptance_archive_closeout.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_archive_closeout_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "16.5"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False


def test_completed_phase_sixteen_scope_is_listed() -> None:
    completed = set(_load_json(PHASE_FIXTURE_PATH)["completed_phase_16_scope"])
    assert completed == {
        "phase_16_0_test_only_acceptance_implementation_charter",
        "phase_16_1_static_forbidden_pattern_acceptance_tests",
        "phase_16_2_runtime_contract_acceptance_tests",
        "phase_16_3_threat_fixture_acceptance_tests",
        "phase_16_4_test_only_acceptance_implementation_readiness_review",
    }


def test_archive_lists_what_phase_sixteen_added_and_did_not_add() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    added = set(fixture["phase_16_added"])
    did_not_add = set(fixture["phase_16_did_not_add"])
    assert "test_only_acceptance_tests_under_tests" in added
    assert "synthetic_threat_fixture_matrix" in added
    assert "lima_changes" in did_not_add
    assert "tests_support_changes" in did_not_add
    assert "runtime_behavior_changes" in did_not_add
    assert "sparkbot_wiring" in did_not_add
    assert "humaninput_runtime_bridge" in did_not_add
    assert "execution" in did_not_add
    assert "dispatch" in did_not_add
    assert "audit_persistence" in did_not_add
    assert "physical_world_side_effects" in did_not_add


def test_phase_seventeen_gate_is_explicit() -> None:
    gate = _load_json(PHASE_FIXTURE_PATH)["phase_17_gate"]
    assert gate["phase_17_approved"] is False
    assert "docs_tests_fixtures_only_acceptance_gate_audit_archive" in gate["recommended_direction"]
    assert "Do you approve Phase 17" in gate["approval_question"]
    assert "runtime implementation" in gate["approval_question"]
    assert "lima/ changes" in gate["approval_question"]
    assert "tests/support/ changes" in gate["approval_question"]
    assert "physical-world action" in gate["approval_question"]


def test_phase_document_preserves_forbidden_scope() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "does not change runtime behavior" in phase_doc
    assert "Phase 17 is not approved by this closeout" in phase_doc


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["helper_behavior_changed"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["humaninput_runtime_bridge_added"] is False
    assert boundary["live_adapter_added"] is False
    assert boundary["approval_enforcement_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True


def test_no_phase_sixteen_five_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_16_5*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_16_5*"))
