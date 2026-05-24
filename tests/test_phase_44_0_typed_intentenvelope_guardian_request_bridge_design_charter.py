"""Phase 44.0 typed IntentEnvelope Guardian request bridge design tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_44_0_TYPED_INTENTENVELOPE_GUARDIAN_REQUEST_BRIDGE_DESIGN_CHARTER.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_44_0_typed_intentenvelope_guardian_request_bridge_design_charter.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_44_0_opens_no_code_bridge_charter() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "44.0"
    assert fixture["charter_only"] is True
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["phase_43_4_anchor"] == "493e1aa8c9f86ef7b733ff382549bf6a66593153"
    assert fixture["bridge_design_lane"] == "no_code_typed_intentenvelope_guardian_request_bridge"
    assert "This phase is docs/tests/fixtures-only." in phase_doc
    assert "natural language never directly executes" in phase_doc


def test_phase_44_0_defines_bridge_chain_without_authority() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["bridge_chain"] == [
        "humaninput_or_shell_bot_automation_request",
        "typed_intentenvelope_candidate",
        "guardian_request",
        "future_guardian_decision",
        "no_execution_yet",
    ]
    assert {
        "humaninput_request",
        "shell_request",
        "bot_request",
        "automation_request",
    } <= set(fixture["request_sources_to_support"])


def test_phase_44_0_lists_future_fixture_categories() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    categories = set(fixture["future_fixture_categories"])
    assert "safe_draft_only_natural_language_request" in categories
    assert "ambiguous_request_requires_clarification" in categories
    assert "external_write_request_requires_guardian_review" in categories
    assert "tool_pack_scope_request" in categories
    assert "scheduled_background_request_without_dispatch" in categories
    assert "physical_world_request_blocked_before_drivers" in categories
    assert "malicious_typed_intent_claiming_approval" in categories
    assert "malicious_guardian_request_claiming_decision_authority" in categories
    assert "missing_actor_tenant_or_lineage_metadata" in categories


def test_phase_44_0_preserves_bridge_invariants() -> None:
    invariants = _load_json(PHASE_FIXTURE_PATH)["required_bridge_invariants"]
    for key in (
        "approval_state_owned_by_future_guardian_policy",
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
        "execution_allowed",
        "side_effects_allowed",
        "approval_granted",
        "dispatch_allowed",
        "persistence_allowed",
        "humaninput_bridge_active",
        "sparkbot_wiring_active",
        "arc_bot_implementation_active",
        "live_adapter_active",
        "external_calls_allowed",
        "model_calls_allowed",
        "tool_calls_allowed",
        "driver_calls_allowed",
        "robotics_allowed",
        "physical_world_allowed",
        "audit_storage_written",
    ):
        assert invariants[key] is False


def test_phase_44_0_blocks_runtime_support_and_physical_world_scope() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    blocked_scope = set(fixture["blocked_scope"])
    assert "runtime_implementation" in blocked_scope
    assert "lima_changes" in blocked_scope
    assert "tests_support_changes" in blocked_scope
    assert "sparkbot_wiring" in blocked_scope
    assert "arc_bot_implementation" in blocked_scope
    assert "guardian_decision_creation" in blocked_scope
    assert "intentcompiler_runtime_behavior" in blocked_scope
    assert "guardian_request_runtime_behavior" in blocked_scope
    assert "model_tool_driver_dispatch" in blocked_scope
    assert "audit_persistence_storage" in blocked_scope
    assert "robotics_hardware_control_physical_world_behavior" in blocked_scope
    assert (
        "background_workers_queues_daemons_subprocesses_threads_database_writes_hidden_side_effects"
        in blocked_scope
    )
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["runtime_behavior_changed"] is False


def test_phase_44_0_files_do_not_appear_under_runtime_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_44_0*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_44_0*"))
