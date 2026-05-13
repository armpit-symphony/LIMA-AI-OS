"""Static checks for Phase 5.0 scope charter."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_5_0_PHASE_5_SCOPE_CHARTER_HUMANINPUT_INTENTENVELOPE_BOUNDARY_DECISION_RECORD.md"
)
FIXTURE_PATH = (
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


def test_fixture_is_valid_phase_five_zero_charter() -> None:
    fixture = _load_json(FIXTURE_PATH)
    assert fixture["phase"] == "5.0"
    assert fixture["status"] == (
        "non_runtime_phase_5_scope_charter_humaninput_intentenvelope_boundary_decision_record"
    )
    assert fixture["non_runtime"] is True
    assert fixture["docs_tests_fixtures_only"] is True


def test_doc_exists_and_states_phase_five_is_planning_only() -> None:
    assert PHASE_DOC_PATH.exists()
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "non-runtime planning only" in phase_doc
    assert "does not approve implementation" in phase_doc
    assert "not an execution command" in phase_doc
    assert "not automatic permission" in phase_doc


def test_phase_four_twenty_source_is_recorded() -> None:
    fixture = _load_json(FIXTURE_PATH)
    assert fixture["source_phase"] == "4.20"
    assert fixture["source_tag"] == "phase-4.20-phase-5-gate-implementation-readiness-closeout"
    assert fixture["source_merge_commit"] == "fc7735c80b3016ee675150a9f1c024f38f2cb34a"


def test_scope_allows_planning_but_not_implementation_or_bridge_code() -> None:
    scope = _load_json(FIXTURE_PATH)["phase_5_scope"]
    assert scope["begins_as_non_runtime_planning"] is True
    assert scope["may_propose_narrow_future_test_only_bridge_harness_lane"] is True
    assert scope["implementation_approved"] is False
    assert scope["live_runtime_approved"] is False
    assert scope["test_only_bridge_code_approved"] is False


def test_human_ux_flow_preserves_not_executable_operator_request() -> None:
    flow = _load_json(FIXTURE_PATH)["human_ux_flow"]
    assert all(flow.values())
    assert flow["humaninput_is_operator_originated_request_envelope"] is True
    assert flow["humaninput_is_not_execution_command"] is True
    assert flow["must_preserve_not_executable_yet_status"] is True


def test_approval_trust_and_autonomy_do_not_bypass_guardian() -> None:
    fixture = _load_json(FIXTURE_PATH)
    approval = fixture["approval_semantics"]
    trust = fixture["trust_and_autonomy"]
    assert all(approval.values())
    assert all(trust.values())
    assert approval["no_automatic_escalation_from_human_input_to_execution"] is True
    assert approval["no_default_trust_bypass_for_operator_input"] is True
    assert trust["operator_intent_is_not_automatic_permission"] is True
    assert trust["kernel_must_classify_gate_and_require_decision_boundaries"] is True


def test_safety_boundary_blocks_side_effects_and_live_actions() -> None:
    safety = _load_json(FIXTURE_PATH)["safety_boundary"]
    assert all(safety.values())
    assert safety["no_shell_execution"] is True
    assert safety["no_browser_execution"] is True
    assert safety["no_robotics_behavior"] is True
    assert safety["no_file_mutation"] is True
    assert safety["no_network_action"] is True
    assert safety["no_external_side_effect"] is True


def test_ready_for_is_limited_to_contract_proposal_or_review() -> None:
    assert set(_load_json(FIXTURE_PATH)["ready_for"]) == {
        "phase_5_1_humaninput_to_intentenvelope_contract_proposal",
        "further_non_runtime_review",
    }


def test_not_ready_for_blocks_runtime_bridge_and_authority_paths() -> None:
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


def test_no_phase_five_zero_runtime_bridge_or_lima_files_exist() -> None:
    forbidden_paths = [
        REPO_ROOT / "lima" / "intent_compiler.py",
        REPO_ROOT / "lima" / "humaninput_to_intentenvelope.py",
        REPO_ROOT / "tests" / "support" / "humaninput_to_intentenvelope_bridge.py",
        REPO_ROOT / "tests" / "helpers" / "humaninput_to_intentenvelope_bridge.py",
    ]
    assert not any(path.exists() for path in forbidden_paths)
