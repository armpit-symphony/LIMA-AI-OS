"""Static checks for Phase 5.2 test-only bridge harness proposal."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_5_2_TEST_ONLY_BRIDGE_HARNESS_PROPOSAL.md"
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_5_2_test_only_bridge_harness_proposal.json"
)
PHASE_5_1_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_5_1_humaninput_to_intentenvelope_contract_proposal.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_fixture_is_valid_phase_five_two_proposal() -> None:
    fixture = _load_json(FIXTURE_PATH)
    assert fixture["phase"] == "5.2"
    assert fixture["status"] == "non_runtime_test_only_bridge_harness_proposal"
    assert fixture["non_runtime"] is True
    assert fixture["docs_tests_fixtures_only"] is True


def test_doc_exists_and_states_harness_is_not_implemented() -> None:
    assert PHASE_DOC_PATH.exists()
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "does not implement the harness" in phase_doc
    assert "not bridge code" in phase_doc
    assert "must not produce those dictionaries" in phase_doc
    assert "fail closed" in phase_doc


def test_phase_five_one_source_is_recorded() -> None:
    fixture = _load_json(FIXTURE_PATH)
    assert fixture["source_phase"] == "5.1"
    assert fixture["source_tag"] == "phase-5.1-humaninput-to-intentenvelope-contract-proposal"
    assert fixture["source_merge_commit"] == "dee3b6d866510f8319c4e34e821c2cfee59634c8"


def test_phase_five_one_contract_remains_metadata_only() -> None:
    fixture = _load_json(PHASE_5_1_FIXTURE_PATH)
    assert fixture["phase"] == "5.1"
    assert fixture["contract_is"]["static_contract_metadata_only"] is True
    assert fixture["contract_is_not"]["intentenvelope_created"] is True
    assert fixture["boundary_results"]["test_only_bridge_code_added"] is False


def test_proposal_is_not_harness_code_or_runtime_behavior() -> None:
    fixture = _load_json(FIXTURE_PATH)
    assert all(fixture["proposal_is"].values())
    assert all(fixture["proposal_is_not"].values())
    assert fixture["proposal_is_not"]["test_only_bridge_code"] is True
    assert fixture["proposal_is_not"]["intentenvelope_created"] is True


def test_proposed_inputs_cover_contract_required_metadata() -> None:
    inputs = set(_load_json(FIXTURE_PATH)["proposed_inputs"])
    assert "synthetic_humaninput_fixture_ref" in inputs
    assert "source_metadata" in inputs
    assert "operator_intent_summary" in inputs
    assert "requested_action_type" in inputs
    assert "risk_tier" in inputs
    assert "required_approval_state" in inputs
    assert "candidate_state" in inputs
    assert "lineage_seed_refs" in inputs
    assert "not_executable_yet" in inputs


def test_future_output_constraints_stay_test_only_and_non_executable() -> None:
    constraints = _load_json(FIXTURE_PATH)["future_output_constraints"]
    assert all(constraints.values())
    assert constraints["test_only"] is True
    assert constraints["non_runtime"] is True
    assert constraints["non_authorizing"] is True
    assert constraints["non_executable"] is True
    assert constraints["before_guardian_decision"] is True


def test_fail_closed_conditions_cover_missing_metadata_and_live_markers() -> None:
    conditions = set(_load_json(FIXTURE_PATH)["required_fail_closed_conditions"])
    assert "missing_synthetic_or_test_only_markers" in conditions
    assert "missing_not_executable_yet_marker" in conditions
    assert "missing_operator_intent_summary" in conditions
    assert "missing_required_approval_state" in conditions
    assert "live_runtime_or_prod_markers" in conditions
    assert "authorization_approval_execution_audit_or_guardian_decision_implication" in conditions


def test_ready_for_is_limited_to_readiness_review_or_review() -> None:
    assert set(_load_json(FIXTURE_PATH)["ready_for"]) == {
        "phase_5_3_test_only_bridge_harness_readiness_review",
        "further_non_runtime_review",
    }


def test_not_ready_for_blocks_implementation_runtime_and_side_effects() -> None:
    not_ready_for = set(_load_json(FIXTURE_PATH)["not_ready_for"])
    assert "test_only_bridge_harness_implementation" in not_ready_for
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


def test_no_phase_five_two_runtime_bridge_or_lima_files_exist() -> None:
    forbidden_paths = [
        REPO_ROOT / "lima" / "intent_compiler.py",
        REPO_ROOT / "lima" / "humaninput_to_intentenvelope.py",
        REPO_ROOT / "tests" / "support" / "humaninput_to_intentenvelope_bridge.py",
        REPO_ROOT / "tests" / "helpers" / "humaninput_to_intentenvelope_bridge.py",
    ]
    assert not any(path.exists() for path in forbidden_paths)
