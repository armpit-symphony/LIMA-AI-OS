"""Static checks for Phase 4.20 Phase 5 gate closeout."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_4_20_PHASE_5_GATE_IMPLEMENTATION_READINESS_CLOSEOUT.md"
)
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_4_20_phase_5_gate_implementation_readiness_closeout.json"
)
PHASE_4_19_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_4_19_humaninput_to_intentenvelope_boundary_readiness_review.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_fixture_is_valid_phase_four_twenty_closeout() -> None:
    fixture = _load_json(FIXTURE_PATH)
    assert fixture["phase"] == "4.20"
    assert fixture["status"] == "non_runtime_phase_5_gate_implementation_readiness_closeout"
    assert fixture["non_runtime"] is True
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["phase_5_gate_reached"] is True
    assert fixture["phase_5_scope_preapproved"] is False


def test_doc_exists_and_stops_at_phase_five_gate() -> None:
    assert PHASE_DOC_PATH.exists()
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "Phase 5 gate is reached" in phase_doc
    assert "operator explicitly approves the Phase 5 lane scope" in phase_doc
    assert "not a bridge implementation" in phase_doc
    assert "not a real IntentCompiler" in phase_doc


def test_phase_nineteen_source_is_recorded() -> None:
    fixture = _load_json(FIXTURE_PATH)
    assert fixture["source_phase"] == "4.19"
    assert fixture["source_tag"] == (
        "phase-4.19-humaninput-to-intentenvelope-boundary-readiness-review"
    )
    assert fixture["source_merge_commit"] == "22f5988c475465645eed4a0d3205089dd7238fc3"


def test_closeout_is_metadata_only_and_requires_operator_decision() -> None:
    fixture = _load_json(FIXTURE_PATH)
    assert fixture["closeout_question"] == (
        "has_phase_4_reached_a_clear_phase_5_gate_and_what_operator_decisions_are_required"
    )
    assert all(fixture["closeout_is"].values())
    assert all(fixture["closeout_is_not"].values())
    assert fixture["closeout_is"]["operator_decision_required_before_phase_5"] is True


def test_phase_nineteen_readiness_remains_non_runtime() -> None:
    fixture = _load_json(PHASE_4_19_FIXTURE_PATH)
    assert fixture["phase"] == "4.19"
    assert fixture["non_runtime"] is True
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["ready_for"] == [
        "phase_4_20_phase_5_gate_implementation_readiness_closeout",
        "further_non_runtime_review",
    ]
    assert fixture["boundary_results"]["runtime_behavior_added"] is False
    assert fixture["boundary_results"]["test_only_bridge_code_added"] is False


def test_review_inputs_cover_humaninput_and_intentenvelope_lane() -> None:
    review_inputs = set(_load_json(FIXTURE_PATH)["review_inputs"])
    assert "phase_4_14_test_only_humaninput_adapter_harness_implementation" in review_inputs
    assert "phase_4_16_humaninput_boundary_lane_closeout_review" in review_inputs
    assert "phase_4_17_humaninput_to_intentenvelope_boundary_planning" in review_inputs
    assert "phase_4_18_humaninput_to_intentenvelope_boundary_schema_contract_proposal" in review_inputs
    assert "phase_4_19_humaninput_to_intentenvelope_boundary_readiness_review" in review_inputs
    assert "docs_INTENTENVELOPE_SAFETY_GATE" in review_inputs


def test_operator_decisions_are_explicit_before_phase_five() -> None:
    decisions = _load_json(FIXTURE_PATH)["operator_decisions_required"]
    assert "phase_5_lane_scope" in decisions
    assert "human_ux_flow" in decisions
    assert "approval_semantics" in decisions
    assert "trust_and_autonomy" in decisions
    assert "safety_boundary" in decisions
    assert "code_scope" in decisions


def test_ready_for_is_limited_to_operator_decision_or_non_runtime_review() -> None:
    assert set(_load_json(FIXTURE_PATH)["ready_for"]) == {
        "explicit_operator_phase_5_scope_decision",
        "future_explicitly_approved_phase_5_planning",
        "further_non_runtime_review",
    }


def test_not_ready_for_blocks_runtime_authority_bridge_and_physical_paths() -> None:
    not_ready_for = set(_load_json(FIXTURE_PATH)["not_ready_for"])
    assert "humaninput_to_intentenvelope_implementation" in not_ready_for
    assert "test_only_bridge_code" in not_ready_for
    assert "runtime_wiring" in not_ready_for
    assert "real_intentcompiler" in not_ready_for
    assert "real_guardiandecision" in not_ready_for
    assert "approval_enforcement" in not_ready_for
    assert "execution" in not_ready_for
    assert "audit_persistence" in not_ready_for
    assert "model_calls" in not_ready_for
    assert "tool_execution" in not_ready_for
    assert "physical_world_action" in not_ready_for
    assert "sparkbot_import_or_wiring" in not_ready_for


def test_boundary_results_show_no_runtime_bridge_or_blocked_behavior() -> None:
    boundary = _load_json(FIXTURE_PATH)["boundary_results"]
    assert boundary["runtime_behavior_added"] is False
    assert boundary["blocked_behavior_added"] is False
    assert boundary["files_under_lima_modified"] is False
    assert boundary["sparkbot_imported"] is False
    assert boundary["sparkbot_wired"] is False
    assert boundary["live_adapter_code_added"] is False
    assert boundary["test_only_bridge_code_added"] is False
    assert boundary["intentenvelope_created"] is False
    assert boundary["real_intentcompiler_added"] is False
    assert boundary["real_guardiandecision_added"] is False
    assert boundary["approval_enforcement_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False


def test_no_phase_four_twenty_runtime_bridge_or_lima_files_exist() -> None:
    forbidden_paths = [
        REPO_ROOT / "lima" / "intent_compiler.py",
        REPO_ROOT / "lima" / "humaninput_to_intentenvelope.py",
        REPO_ROOT / "tests" / "support" / "humaninput_to_intentenvelope_bridge.py",
        REPO_ROOT / "tests" / "helpers" / "humaninput_to_intentenvelope_bridge.py",
    ]
    assert not any(path.exists() for path in forbidden_paths)
