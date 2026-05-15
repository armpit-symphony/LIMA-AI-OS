"""Static checks for Phase 15.4 test-only implementation readiness gate closeout."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_15_4_TEST_ONLY_IMPLEMENTATION_READINESS_GATE_CLOSEOUT.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_15_4_test_only_implementation_readiness_gate_closeout.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_closeout_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "15.4"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False
    assert fixture["actual_future_acceptance_tests_implemented"] is False
    assert fixture["actual_future_acceptance_fixtures_added"] is False


def test_completed_phase_fifteen_scope_is_listed() -> None:
    completed = set(_load_json(PHASE_FIXTURE_PATH)["completed_phase_15_scope"])
    assert completed == {
        "phase_15_0_acceptance_gate_implementation_proposal_charter",
        "phase_15_1_future_static_test_implementation_plan",
        "phase_15_2_future_runtime_contract_test_implementation_plan",
        "phase_15_3_future_threat_fixture_test_implementation_plan",
    }


def test_readiness_outcome_is_limited_to_later_test_only_implementation() -> None:
    outcome = _load_json(PHASE_FIXTURE_PATH)["readiness_outcome"]
    assert outcome["phase_14_designed_tests_ready_for_later_explicitly_approved_test_only_implementation"] is True
    assert outcome["runtime_implementation_approved"] is False
    assert outcome["lima_changes_approved"] is False
    assert outcome["tests_support_changes_approved"] is False
    assert outcome["sparkbot_integration_approved"] is False
    assert outcome["humaninput_runtime_bridge_approved"] is False
    assert outcome["live_adapter_approved"] is False
    assert outcome["approval_enforcement_approved"] is False
    assert outcome["execution_dispatch_persistence_or_physical_world_action_approved"] is False


def test_future_phase_sixteen_scope_is_gated_and_test_only() -> None:
    scope = _load_json(PHASE_FIXTURE_PATH)["future_phase_16_candidate_scope"]
    assert scope["phase_16_approved"] is False
    assert "tests/test_acceptance_static_forbidden_patterns.py" in scope["allowed_if_later_approved"]
    assert "tests/test_acceptance_runtime_contract_invariants.py" in scope["allowed_if_later_approved"]
    assert "tests/test_acceptance_threat_fixtures.py" in scope["allowed_if_later_approved"]
    assert "tests/fixtures/runtime_extraction/acceptance_*.json" in scope["allowed_if_later_approved"]
    assert scope["must_remain_test_only_and_fixture_only"] is True
    assert scope["must_not_modify_lima"] is True
    assert scope["must_not_modify_tests_support"] is True
    assert scope["must_not_add_runtime_behavior"] is True
    assert scope["must_not_add_approval_enforcement_execution_dispatch_audit_persistence_or_physical_world_action"] is True


def test_phase_sixteen_approval_question_preserves_boundaries() -> None:
    question = _load_json(PHASE_FIXTURE_PATH)["phase_16_approval_question"]
    assert "Do you approve Phase 16" in question
    assert "test-only acceptance-gate implementation lane" in question
    assert "runtime implementation" in question
    assert "lima/ changes" in question
    assert "tests/support/ changes" in question
    assert "Sparkbot wiring" in question
    assert "HumanInput runtime bridge" in question
    assert "physical-world action" in question


def test_phase_document_blocks_phase_sixteen_work() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "Phase 16 is not approved by this closeout" in phase_doc
    assert "does not implement actual future acceptance tests" in phase_doc
    assert "does not add future acceptance fixtures" in phase_doc
    assert "must not modify `lima/`" in phase_doc
    assert "must not modify `tests/support/`" in phase_doc


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["actual_future_acceptance_tests_implemented"] is False
    assert boundary["actual_future_acceptance_fixtures_added"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["humaninput_runtime_bridge_added"] is False
    assert boundary["live_adapter_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True


def test_no_phase_fifteen_four_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_15_4*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_15_4*"))
