"""Static checks for Phase 5.11 HumanInput bridge design lane archive closeout."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_5_11_PHASE_5_HUMANINPUT_BRIDGE_DESIGN_LANE_AUDIT_ARCHIVE_CLOSEOUT.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_5_11_phase_5_humaninput_bridge_design_lane_audit_archive_closeout.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_fixture_declares_docs_tests_fixtures_only_archive_closeout() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "5.11"
    assert fixture["status"] == "phase_5_humaninput_bridge_design_lane_audit_archive_closeout"
    assert fixture["non_runtime"] is True
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["audit_archive_closeout_only"] is True


def test_phase_five_zero_through_ten_are_listed_complete() -> None:
    completed = set(_load_json(PHASE_FIXTURE_PATH)["completed_phase_5_scope"])
    assert completed == {
        "phase_5_0_scope_charter_humaninput_intentenvelope_boundary_decision_record",
        "phase_5_1_humaninput_to_intentenvelope_contract_proposal",
        "phase_5_2_test_only_bridge_harness_proposal",
        "phase_5_3_test_only_bridge_harness_readiness_review",
        "phase_5_4_test_only_humaninput_to_intentenvelope_bridge_harness_implementation",
        "phase_5_5_test_only_bridge_harness_readiness_review",
        "phase_5_6_humaninput_runtime_bridge_safety_gate_next_scope_decision_record",
        "phase_5_7_humaninput_runtime_bridge_design_proposal",
        "phase_5_8_humaninput_runtime_bridge_threat_model",
        "phase_5_9_humaninput_runtime_bridge_boundary_validation_matrix",
        "phase_5_10_runtime_bridge_implementation_gate_closeout_review",
    }


def test_design_lane_is_archived_as_specification_only() -> None:
    decision = _load_json(PHASE_FIXTURE_PATH)["archive_decision"]
    assert decision["phase_5_7_to_5_10_archived_as_design_specification_only"] is True
    assert decision["phase_5_live_implementation_gated"] is True
    assert decision["future_runtime_work_requires_new_explicit_phil_approval"] is True


def test_phase_five_four_helper_remains_test_only_and_not_runtime_reusable() -> None:
    decision = _load_json(PHASE_FIXTURE_PATH)["archive_decision"]
    assert decision["phase_5_4_helper_remains_test_only"] is True
    assert decision["helper_classifier_runtime_reuse_approved"] is False


def test_added_and_not_added_scope_is_explicit() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert set(fixture["added"]) == {
        "docs",
        "runtime_extraction_fixtures",
        "static_boundary_readiness_tests",
        "phase_5_4_test_only_helper_under_tests_support",
    }
    assert {
        "runtime_bridge",
        "live_adapter",
        "lima_runtime_change",
        "sparkbot_wiring",
        "execution",
        "approval_enforcement",
        "audit_persistence",
        "physical_world_action",
    } <= set(fixture["not_added"])


def test_recommended_options_require_explicit_approval() -> None:
    options = _load_json(PHASE_FIXTURE_PATH)["recommended_next_options"]
    assert {option["id"] for option in options} == {"option_a", "option_b", "option_c", "option_d"}
    assert all(option["requires_explicit_approval"] is True for option in options)


def test_blocked_scope_preserves_runtime_boundaries() -> None:
    blocked = _load_json(PHASE_FIXTURE_PATH)["blocked_scope"]
    assert all(blocked.values())
    assert blocked["runtime_bridge_implementation"] is True
    assert blocked["live_adapter_code"] is True
    assert blocked["files_under_lima"] is True
    assert blocked["tests_support_changes"] is True
    assert blocked["helper_behavior_changes"] is True
    assert blocked["approval_enforcement"] is True
    assert blocked["execution"] is True
    assert blocked["physical_world_action"] is True


def test_not_ready_for_live_runtime_or_test_helper_reuse() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    not_ready = set(fixture["not_ready_for"])
    assert "runtime_bridge_implementation_without_explicit_approval" in not_ready
    assert "runtime_wiring" in not_ready
    assert "live_adapter_code" in not_ready
    assert "phase_5_4_helper_runtime_reuse" in not_ready
    assert "real_intentcompiler" in not_ready
    assert "real_guardiandecision" in not_ready


def test_boundary_results_show_no_forbidden_behavior_added() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["runtime_behavior_added"] is False
    assert boundary["files_under_lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["helper_behavior_changed"] is False
    assert boundary["new_helper_implementation_added"] is False
    assert boundary["runtime_bridge_added"] is False
    assert boundary["live_adapter_code_added"] is False
    assert boundary["sparkbot_imported"] is False
    assert boundary["sparkbot_wired"] is False
    assert boundary["real_intentcompiler_added"] is False
    assert boundary["real_guardiandecision_added"] is False
    assert boundary["approval_enforcement_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["external_side_effect_added"] is False
    assert boundary["physical_world_action_added"] is False


def test_no_phase_five_eleven_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_5_11*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_5_11*"))
