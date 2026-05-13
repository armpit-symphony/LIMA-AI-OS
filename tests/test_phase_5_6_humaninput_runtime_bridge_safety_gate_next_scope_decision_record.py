"""Static checks for Phase 5.6 HumanInput runtime bridge safety gate."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_5_6_HUMANINPUT_RUNTIME_BRIDGE_SAFETY_GATE_NEXT_SCOPE_DECISION_RECORD.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_5_6_humaninput_runtime_bridge_safety_gate_next_scope_decision_record.json"
)
PHASE_5_5_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_5_5_test_only_bridge_harness_readiness_review.json"
)
PHASE_5_4_HELPER_PATH = (
    REPO_ROOT / "tests" / "support" / "test_only_humaninput_to_intentenvelope_bridge.py"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_fixture_declares_docs_tests_fixtures_only_safety_gate() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "5.6"
    assert fixture["status"] == "humaninput_runtime_bridge_safety_gate_next_scope_decision_record"
    assert fixture["non_runtime"] is True
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["safety_gate"] is True
    assert fixture["decision_record_only"] is True


def test_doc_keeps_phase_five_four_helper_test_only_and_blocks_runtime_reuse() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "The Phase 5.4 helper remains test-only" in phase_doc
    assert "must not be reused as runtime classifier logic" in phase_doc
    assert "Live HumanInput to IntentEnvelope behavior remains blocked" in phase_doc


def test_future_runtime_bridge_requires_explicit_phil_approval_and_design_first() -> None:
    decision = _load_json(PHASE_FIXTURE_PATH)["safety_gate_decision"]
    assert decision["future_runtime_bridge_requires_explicit_phil_approval"] is True
    assert decision["future_runtime_bridge_must_start_with_runtime_design_proposal"] is True
    assert decision["next_safe_lane_is_planning_or_design_only"] is True
    assert decision["live_runtime_humaninput_to_intentenvelope_approved"] is False


def test_humaninput_remains_context_not_permission_and_operator_words_do_not_bypass() -> None:
    decision = _load_json(PHASE_FIXTURE_PATH)["safety_gate_decision"]
    assert decision["humaninput_is_intent_context_not_execution_permission"] is True
    assert decision["operator_admin_phil_trusted_wording_cannot_bypass_approval"] is True


def test_next_scope_options_are_documented_but_not_preapproved() -> None:
    options = _load_json(PHASE_FIXTURE_PATH)["next_scope_options"]
    assert {option["id"] for option in options} == {"option_a", "option_b", "option_c", "option_d"}
    assert all(option["preapproved"] is False for option in options)
    assert {option["label"] for option in options} == {
        "stop_phase_5_and_audit_archive_lane",
        "docs_tests_fixtures_only_runtime_bridge_design_proposal",
        "runtime_threat_model_only",
        "defer_runtime_bridge_and_return_to_broader_os_roadmap_planning",
    }


def test_phase_five_seven_or_next_phase_is_gated() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    gate = fixture["phase_5_7_gate"]
    assert gate["gate_reached"] is True
    assert gate["phase_5_7_preapproved"] is False
    assert gate["requires_explicit_operator_scope_decision"] is True
    assert gate["live_runtime_implementation_approved"] is False
    assert set(fixture["ready_for"]) == {
        "explicit_operator_phase_5_7_scope_decision",
        "operator_choice_among_next_scope_options",
    }


def test_blocked_scope_keeps_runtime_execution_and_physical_actions_out() -> None:
    blocked = _load_json(PHASE_FIXTURE_PATH)["blocked_scope"]
    assert all(blocked.values())
    assert blocked["live_runtime_bridge_implementation"] is True
    assert blocked["helper_behavior_changes"] is True
    assert blocked["files_under_lima"] is True
    assert blocked["approval_enforcement"] is True
    assert blocked["execution"] is True
    assert blocked["audit_persistence"] is True
    assert blocked["shell_behavior"] is True
    assert blocked["browser_behavior"] is True
    assert blocked["network_behavior"] is True
    assert blocked["file_mutation"] is True
    assert blocked["robotics_behavior"] is True
    assert blocked["physical_world_action"] is True


def test_boundary_results_show_no_lima_tests_support_or_helper_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["files_under_lima_modified"] is False
    assert boundary["tests_support_helper_modified"] is False
    assert boundary["new_helper_implementation_added"] is False
    assert boundary["helper_behavior_changed"] is False
    assert boundary["runtime_behavior_added"] is False


def test_no_sparkbot_intentcompiler_or_guardiandecision_runtime_behavior_changed() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    boundary = fixture["boundary_results"]
    assert boundary["sparkbot_imported"] is False
    assert boundary["sparkbot_wired"] is False
    assert boundary["real_intentcompiler_added"] is False
    assert boundary["real_guardiandecision_added"] is False
    assert "real_intentcompiler" in fixture["not_ready_for"]
    assert "real_guardiandecision" in fixture["not_ready_for"]


def test_no_approval_execution_audit_or_side_effect_paths_added() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["approval_enforcement_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["external_side_effect_added"] is False
    assert boundary["physical_world_action_added"] is False


def test_phase_five_five_review_remains_source_and_helper_still_under_tests_support() -> None:
    phase_five_five = _load_json(PHASE_5_5_FIXTURE_PATH)
    assert phase_five_five["phase"] == "5.5"
    assert phase_five_five["review_subject"]["helper_behavior_changed_by_phase_5_5"] is False
    assert phase_five_five["review_subject"]["classifier_runtime_reuse_allowed"] is False
    assert PHASE_5_4_HELPER_PATH.exists()
    assert "tests/support" in PHASE_5_4_HELPER_PATH.as_posix()
    assert not (REPO_ROOT / "lima" / "test_only_humaninput_to_intentenvelope_bridge.py").exists()
