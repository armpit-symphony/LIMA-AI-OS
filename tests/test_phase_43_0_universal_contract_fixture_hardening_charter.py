"""Phase 43.0 universal contract fixture hardening charter tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_43_0_UNIVERSAL_CONTRACT_FIXTURE_HARDENING_CHARTER.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_43_0_universal_contract_fixture_hardening_charter.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_43_0_opens_charter_without_runtime_scope() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "43.0"
    assert fixture["charter_only"] is True
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["phase_42_4_anchor"] == "0ea33ea9e7ec59c937cd2ec3cbcc0dbc1e72436e"
    assert fixture["phase_43_lane"] == "docs_tests_fixtures_only_universal_contract_fixture_hardening"
    assert "Phase 43.0 is the charter only" in phase_doc
    assert "It authorizes only docs/tests/fixtures planning" in phase_doc


def test_phase_43_0_lists_universal_fixture_categories() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    consumer_profiles = set(fixture["consumer_profiles_to_cover"])
    embodiment_profiles = set(fixture["embodiment_action_profiles_to_cover"])
    adversarial_cases = set(fixture["adversarial_cases_to_cover"])
    assert {
        "arc_bot_office_task_profile",
        "sparkbot_reference_profile",
        "generic_automation_agent_profile",
        "coding_agent_profile",
        "research_agent_profile",
    } <= consumer_profiles
    assert {
        "browser_action_profile",
        "shell_action_profile",
        "file_mutation_profile",
        "network_api_action_profile",
        "scheduled_background_work_profile",
        "iot_device_action_profile",
        "drone_action_profile",
        "humanoid_action_profile",
        "robot_motion_profile",
        "emergency_stop_profile",
    } <= embodiment_profiles
    assert {
        "malicious_consumer_profile_trying_to_grant_approval",
        "malicious_embodiment_profile_trying_to_allow_execution",
        "malformed_profile_data",
        "unknown_model_provider_data",
        "nested_bypass_wording",
    } <= adversarial_cases


def test_phase_43_0_preserves_required_fixture_invariants() -> None:
    invariants = _load_json(PHASE_FIXTURE_PATH)["required_fixture_invariants"]
    for key in (
        "preview_only",
        "non_authoritative",
        "safe_by_default",
        "local_only",
        "deterministic",
    ):
        assert invariants[key] is True
    for key in (
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
        "robotics_allowed",
        "physical_world_allowed",
        "lima_grants_approval",
    ):
        assert invariants[key] is False


def test_phase_43_0_blocks_runtime_and_physical_world_scope() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    blocked_scope = set(fixture["blocked_scope"])
    assert "runtime_implementation" in blocked_scope
    assert "lima_changes" in blocked_scope
    assert "tests_support_changes" in blocked_scope
    assert "sparkbot_wiring" in blocked_scope
    assert "arc_bot_implementation" in blocked_scope
    assert "real_approval_enforcement" in blocked_scope
    assert "robotics_hardware_control_physical_world_behavior" in blocked_scope
    assert (
        "background_workers_queues_daemons_subprocesses_threads_database_writes_hidden_side_effects"
        in blocked_scope
    )
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["runtime_behavior_changed"] is False


def test_phase_43_0_files_do_not_appear_under_runtime_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_43_0*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_43_0*"))
