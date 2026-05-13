"""Static checks for Phase 5.10 runtime bridge implementation gate closeout."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_5_10_RUNTIME_BRIDGE_IMPLEMENTATION_GATE_CLOSEOUT_REVIEW.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_5_10_runtime_bridge_implementation_gate_closeout_review.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_fixture_declares_closeout_gate_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "5.10"
    assert fixture["status"] == "runtime_bridge_implementation_gate_closeout_review"
    assert fixture["non_runtime"] is True
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["closeout_review_only"] is True
    assert fixture["implementation_gate"] is True


def test_doc_says_no_runtime_or_helper_behavior_is_added() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "does not implement a runtime bridge" in phase_doc
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "does not change the Phase 5.4 helper" in phase_doc


def test_closeout_lists_all_designed_artifacts() -> None:
    designed = set(_load_json(PHASE_FIXTURE_PATH)["designed_artifacts"])
    assert designed == {
        "phase_5_6_safety_gate_next_scope_decision_record",
        "phase_5_7_runtime_bridge_design_proposal",
        "phase_5_8_runtime_bridge_threat_model",
        "phase_5_9_boundary_validation_matrix",
    }


def test_live_runtime_pieces_remain_unimplemented() -> None:
    unimplemented = set(_load_json(PHASE_FIXTURE_PATH)["still_unimplemented"])
    assert "live_humaninput_to_intentenvelope_runtime_bridge" in unimplemented
    assert "live_adapter_code" in unimplemented
    assert "runtime_classifier_logic" in unimplemented
    assert "real_intentcompiler_behavior" in unimplemented
    assert "real_guardiandecision_behavior" in unimplemented
    assert "approval_enforcement" in unimplemented
    assert "execution" in unimplemented
    assert "audit_persistence" in unimplemented
    assert "physical_world_action" in unimplemented


def test_future_runtime_implementation_requires_explicit_scope_and_guardian_review() -> None:
    requirements = set(_load_json(PHASE_FIXTURE_PATH)["future_runtime_implementation_requirements"])
    assert "separate_explicit_phil_approval" in requirements
    assert "narrow_runtime_implementation_scope" in requirements
    assert "guardian_review_handoff" in requirements
    assert "provenance_validation" in requirements
    assert "replay_and_staleness_handling" in requirements
    assert "malformed_input_rejection" in requirements
    assert "semantic_tests" in requirements
    assert "phase_5_4_helper_not_reused_as_runtime_classifier" in requirements


def test_closeout_decision_keeps_runtime_implementation_blocked() -> None:
    decision = _load_json(PHASE_FIXTURE_PATH)["closeout_decision"]
    assert decision["phase_5_design_lane_closed"] is True
    assert decision["runtime_implementation_approved"] is False
    assert decision["live_runtime_bridge_blocked"] is True
    assert decision["phase_5_should_stop_at_gate"] is True
    assert decision["requires_explicit_operator_decision_for_next_scope"] is True


def test_future_options_all_require_explicit_approval() -> None:
    options = set(_load_json(PHASE_FIXTURE_PATH)["future_options_requiring_explicit_approval"])
    assert options == {
        "more_docs_tests_fixtures_only_runtime_design_hardening",
        "narrow_test_only_runtime_boundary_prototype_outside_lima",
        "narrow_production_runtime_design_proposal_before_implementation",
        "defer_runtime_bridge_and_return_to_broader_os_roadmap_planning",
    }


def test_blocked_scope_preserves_runtime_boundaries() -> None:
    blocked = _load_json(PHASE_FIXTURE_PATH)["blocked_scope"]
    assert all(blocked.values())
    assert blocked["runtime_bridge_implementation"] is True
    assert blocked["files_under_lima"] is True
    assert blocked["tests_support_changes"] is True
    assert blocked["approval_enforcement"] is True
    assert blocked["execution"] is True
    assert blocked["physical_world_action"] is True


def test_ready_only_for_operator_next_scope_or_audit_archive() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert set(fixture["ready_for"]) == {
        "explicit_operator_next_scope_decision",
        "audit_archive_phase_5_design_lane",
    }
    assert "runtime_bridge_implementation_without_explicit_approval" in fixture["not_ready_for"]
    assert "phase_5_4_helper_runtime_reuse" in fixture["not_ready_for"]


def test_boundary_results_show_no_runtime_or_helper_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["runtime_behavior_added"] is False
    assert boundary["files_under_lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["helper_behavior_changed"] is False
    assert boundary["runtime_bridge_added"] is False


def test_no_phase_five_ten_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_5_10*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_5_10*"))
