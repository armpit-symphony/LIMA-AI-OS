"""Static checks for Phase 5.1 HumanInput to IntentEnvelope contract proposal."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_5_1_HUMANINPUT_TO_INTENTENVELOPE_CONTRACT_PROPOSAL.md"
)
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_5_1_humaninput_to_intentenvelope_contract_proposal.json"
)
PHASE_5_0_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_5_0_phase_5_scope_charter_humaninput_intentenvelope_boundary_decision_record.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_fixture_is_valid_phase_five_one_contract_proposal() -> None:
    fixture = _load_json(FIXTURE_PATH)
    assert fixture["phase"] == "5.1"
    assert fixture["status"] == "non_runtime_humaninput_to_intentenvelope_contract_proposal"
    assert fixture["non_runtime"] is True
    assert fixture["docs_tests_fixtures_only"] is True


def test_doc_exists_and_states_contract_is_not_bridge_or_compiler() -> None:
    assert PHASE_DOC_PATH.exists()
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "static non-runtime metadata" in phase_doc
    assert "not a bridge implementation" in phase_doc
    assert "not a real IntentCompiler" in phase_doc
    assert "must not implement it" in phase_doc


def test_phase_five_zero_source_is_recorded() -> None:
    fixture = _load_json(FIXTURE_PATH)
    assert fixture["source_phase"] == "5.0"
    assert fixture["source_tag"] == (
        "phase-5.0-phase-5-scope-charter-humaninput-intentenvelope-boundary-decision-record"
    )
    assert fixture["source_merge_commit"] == "46ade88b6f41edabc63af4b5236d3154a6d96450"


def test_phase_five_zero_charter_still_blocks_implementation() -> None:
    fixture = _load_json(PHASE_5_0_FIXTURE_PATH)
    scope = fixture["phase_5_scope"]
    assert scope["begins_as_non_runtime_planning"] is True
    assert scope["implementation_approved"] is False
    assert scope["test_only_bridge_code_approved"] is False


def test_contract_is_static_metadata_only_and_not_creation() -> None:
    fixture = _load_json(FIXTURE_PATH)
    assert all(fixture["contract_is"].values())
    assert all(fixture["contract_is_not"].values())
    assert fixture["contract_is_not"]["intentenvelope_created"] is True
    assert fixture["contract_is_not"]["approval_enforcement"] is True


def test_required_preserved_fields_cover_operator_request_and_safety_metadata() -> None:
    fields = set(_load_json(FIXTURE_PATH)["required_preserved_fields"])
    assert "humaninput_ref" in fields
    assert "source_metadata" in fields
    assert "operator_intent_summary" in fields
    assert "requested_action_type" in fields
    assert "risk_tier" in fields
    assert "required_approval_state" in fields
    assert "not_executable_yet" in fields
    assert "lineage_seed_refs" in fields


def test_candidate_states_are_descriptive_and_include_blocked_paths() -> None:
    states = set(_load_json(FIXTURE_PATH)["candidate_states"])
    assert states == {
        "proposed",
        "ready_for_review",
        "approval_required",
        "denied",
        "blocked_missing_metadata",
        "blocked_unsafe_request",
    }


def test_required_invariants_preserve_guardian_boundary() -> None:
    invariants = _load_json(FIXTURE_PATH)["required_invariants"]
    assert all(invariants.values())
    assert invariants["humaninput_is_not_execution_command"] is True
    assert invariants["intentenvelope_candidate_is_not_authorization"] is True
    assert invariants["operator_intent_is_not_automatic_permission"] is True
    assert invariants["guardian_decision_remains_required_before_consequential_behavior"] is True


def test_ready_for_is_limited_to_bridge_harness_proposal_or_review() -> None:
    assert set(_load_json(FIXTURE_PATH)["ready_for"]) == {
        "phase_5_2_test_only_bridge_harness_proposal",
        "further_non_runtime_review",
    }


def test_not_ready_for_blocks_runtime_bridge_authority_and_side_effect_paths() -> None:
    not_ready_for = set(_load_json(FIXTURE_PATH)["not_ready_for"])
    assert "humaninput_to_intentenvelope_implementation" in not_ready_for
    assert "test_only_bridge_code" in not_ready_for
    assert "runtime_wiring" in not_ready_for
    assert "real_intentcompiler" in not_ready_for
    assert "real_guardiandecision" in not_ready_for
    assert "approval_enforcement" in not_ready_for
    assert "execution" in not_ready_for
    assert "audit_persistence" in not_ready_for
    assert "physical_world_action" in not_ready_for


def test_boundary_results_show_no_runtime_or_blocked_behavior() -> None:
    boundary = _load_json(FIXTURE_PATH)["boundary_results"]
    assert all(value is False for value in boundary.values())


def test_no_phase_five_one_runtime_bridge_or_lima_files_exist() -> None:
    forbidden_paths = [
        REPO_ROOT / "lima" / "intent_compiler.py",
        REPO_ROOT / "lima" / "humaninput_to_intentenvelope.py",
        REPO_ROOT / "tests" / "support" / "humaninput_to_intentenvelope_bridge.py",
        REPO_ROOT / "tests" / "helpers" / "humaninput_to_intentenvelope_bridge.py",
    ]
    assert not any(path.exists() for path in forbidden_paths)
