"""Static checks for Phase 15.2 future runtime contract test implementation plan."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_15_2_FUTURE_RUNTIME_CONTRACT_TEST_IMPLEMENTATION_PLAN.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_15_2_future_runtime_contract_test_implementation_plan.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_plan_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "15.2"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False
    assert fixture["actual_future_runtime_contract_tests_implemented"] is False


def test_future_runtime_contract_test_file_is_named_but_not_created() -> None:
    future_files = _load_json(PHASE_FIXTURE_PATH)["proposed_future_test_files"]
    assert future_files == ["tests/test_acceptance_runtime_contract_invariants.py"]
    assert not (REPO_ROOT / "tests" / "test_acceptance_runtime_contract_invariants.py").exists()


def test_future_runtime_contract_tests_cover_candidate_invariants() -> None:
    names = {entry["name"] for entry in _load_json(PHASE_FIXTURE_PATH)["proposed_future_runtime_contract_tests"]}
    assert names == {
        "test_candidate_execution_allowed_is_always_false",
        "test_candidate_side_effects_allowed_is_always_false",
        "test_candidate_approval_state_is_never_approved",
        "test_candidate_approved_flag_is_never_true",
        "test_candidate_provenance_is_preserved",
        "test_malformed_candidate_is_invalid_or_blocked",
        "test_unknown_status_is_invalid_blocked_or_needs_review",
        "test_stale_or_replayed_candidate_is_blocked_or_invalid",
        "test_operator_admin_phil_trusted_wording_does_not_bypass_safety",
        "test_candidate_contract_creates_no_intentenvelope_or_guardiandecision",
    }


def test_future_contract_scope_blocks_authority_and_mutation() -> None:
    scope = _load_json(PHASE_FIXTURE_PATH)["future_test_scope"]
    assert scope["may_exercise_existing_non_executing_runtime_candidate_status_apis_only_if_later_approved"] is True
    assert scope["runtime_behavior_not_allowed"] is True
    assert scope["candidate_module_mutation_not_allowed"] is True
    assert scope["helper_behavior_not_allowed"] is True
    assert scope["dispatch_not_allowed"] is True
    assert scope["audit_persistence_not_allowed"] is True
    assert scope["contract_test_success_is_not_authority"] is True


def test_phase_document_blocks_runtime_contract_test_implementation() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "without implementing it" in phase_doc
    assert "does not implement actual future runtime contract acceptance tests" in phase_doc
    assert "This file is proposed for a later explicitly approved phase only" in phase_doc
    assert "contract-test success as authority" in phase_doc


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["actual_future_runtime_contract_tests_implemented"] is False
    assert boundary["candidate_status_expanded"] is False
    assert boundary["intake_candidate_expanded"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["humaninput_runtime_bridge_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True


def test_no_phase_fifteen_two_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_15_2*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_15_2*"))
