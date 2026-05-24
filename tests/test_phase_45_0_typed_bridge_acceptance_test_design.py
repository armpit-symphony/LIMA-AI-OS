"""Phase 45.0 typed bridge acceptance-test design tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_45_0_TYPED_BRIDGE_ACCEPTANCE_TEST_DESIGN.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_45_0_typed_bridge_acceptance_test_design.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_45_0_opens_no_code_acceptance_test_design_lane() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "45.0"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["acceptance_test_design_only"] is True
    assert fixture["runtime_test_harness_created"] is False
    assert fixture["phase_44_3_anchor"] == "6d169d50c775bfd307c350802efebebd3f708e78"
    assert fixture["phase_44_3_tag"] == "phase-44.3-typed-bridge-archive-closeout"


def test_phase_45_0_designs_future_bridge_chain_tests_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["future_bridge_chain_under_test"] == [
        "source_request_metadata",
        "typed_intentenvelope_candidate_metadata",
        "guardian_request_metadata",
        "future_guardian_decision_metadata",
        "still_no_execution",
    ]
    text = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "These are test requirements only." in text
    assert "does not create bridge behavior" in text


def test_phase_45_0_required_future_test_families_cover_positive_and_negative_cases() -> None:
    families = set(_load_json(PHASE_FIXTURE_PATH)["required_future_test_families"])
    assert "source_request_metadata_shape_tests" in families
    assert "typed_intentenvelope_candidate_shape_tests" in families
    assert "guardian_request_metadata_shape_tests" in families
    assert "guardian_decision_metadata_boundary_tests" in families
    assert "positive_non_authoritative_shape_tests" in families
    assert "negative_approval_bypass_tests" in families
    assert "negative_forged_guardian_decision_tests" in families
    assert "negative_missing_actor_tenant_lineage_tests" in families
    assert "negative_background_dispatch_tests" in families
    assert "negative_adapter_external_call_tests" in families
    assert "negative_model_tool_driver_call_tests" in families
    assert "negative_robotics_physical_world_tests" in families
    assert "runtime_support_boundary_path_tests" in families


def test_phase_45_0_required_future_inputs_cover_phase_44_bridge_cases() -> None:
    inputs = set(_load_json(PHASE_FIXTURE_PATH)["required_future_test_inputs"])
    assert "humaninput_request" in inputs
    assert "shell_request" in inputs
    assert "bot_request" in inputs
    assert "automation_request" in inputs
    assert "safe_draft_only_request" in inputs
    assert "ambiguous_clarification_request" in inputs
    assert "external_write_request" in inputs
    assert "tool_pack_scope_request" in inputs
    assert "scheduled_background_request" in inputs
    assert "physical_world_request" in inputs
    assert "emergency_stop_request" in inputs
    assert "malicious_approval_claim" in inputs
    assert "malicious_guardian_decision_claim" in inputs
    assert "missing_identity_or_lineage_metadata" in inputs


def test_phase_45_0_required_invariants_keep_authority_and_execution_blocked() -> None:
    invariants = _load_json(PHASE_FIXTURE_PATH)["required_invariants"]
    for key in (
        "non_authoritative",
        "safe_by_default",
        "local_only",
        "deterministic",
    ):
        assert invariants[key] is True
    for key in (
        "natural_language_direct_execution_allowed",
        "typed_intent_grants_authority",
        "guardian_request_is_decision",
        "guardian_decision_created",
        "guardian_decision_grants_approval",
        "execution_allowed",
        "dispatch_allowed",
        "persistence_allowed",
        "external_calls_allowed",
        "model_calls_allowed",
        "tool_calls_allowed",
        "driver_calls_allowed",
        "adapter_calls_allowed",
        "robotics_allowed",
        "physical_world_allowed",
        "audit_storage_written",
    ):
        assert invariants[key] is False


def test_phase_45_0_blocks_runtime_scope_and_recommends_no_implementation() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    blocked = set(fixture["blocked_scope"])
    assert "runtime_implementation" in blocked
    assert "lima_changes" in blocked
    assert "tests_support_changes" in blocked
    assert "sparkbot_wiring" in blocked
    assert "arc_bot_implementation" in blocked
    assert "humaninput_bridge_behavior" in blocked
    assert "real_intentcompiler_behavior" in blocked
    assert "real_guardian_request_runtime_behavior" in blocked
    assert "guardian_decision_creation" in blocked
    assert "model_tool_driver_calls" in blocked
    assert "robotics_hardware_control_physical_world_behavior" in blocked
    assert (
        "background_workers_queues_daemons_subprocesses_threads_database_writes_hidden_side_effects"
        in blocked
    )
    assert fixture["remaining_gaps"] == []
    assert fixture["runtime_gap_found"] is False
    assert fixture["runtime_change_needed"] is False
    assert fixture["lima_change_needed"] is False
    assert fixture["tests_support_change_needed"] is False
    assert fixture["next_runtime_implementation_recommended"] is False


def test_phase_45_0_stays_out_of_runtime_and_tests_support() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["runtime_behavior_changed"] is False
    assert not list((REPO_ROOT / "lima").rglob("*phase_45_0*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_45_0*"))
