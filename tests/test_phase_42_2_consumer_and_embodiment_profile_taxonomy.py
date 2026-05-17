"""Phase 42.2 consumer and embodiment profile taxonomy tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_42_2_CONSUMER_AND_EMBODIMENT_PROFILE_TAXONOMY.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_42_2_consumer_and_embodiment_profile_taxonomy.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_42_2_lists_universal_consumer_profiles() -> None:
    profiles = set(_load_json(PHASE_FIXTURE_PATH)["consumer_profiles"])
    assert "arc_bot_lima_office" in profiles
    assert "sparkbot_public" in profiles
    assert "generic_chatbot" in profiles
    assert "automation_agent" in profiles
    assert "coding_agent" in profiles
    assert "research_agent" in profiles
    assert "robot_controller" in profiles
    assert "drone_controller" in profiles
    assert "humanoid_controller" in profiles
    assert "iot_controller" in profiles


def test_phase_42_2_demotes_arc_bot_and_keeps_sparkbot_showcase_only() -> None:
    roles = _load_json(PHASE_FIXTURE_PATH)["consumer_profile_roles"]
    assert roles["arc_bot_lima_office"] == "example_guarded_office_agent_profile"
    assert roles["sparkbot_public"] == "open_source_showcase_shell_and_reference_profile"
    text = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "Arc Bot / LIMA Office is one guarded office-agent profile." in text
    assert "Sparkbot Public is an open-source showcase shell" in text


def test_phase_42_2_lists_embodiment_profiles_and_action_classes() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    embodiment_profiles = set(fixture["embodiment_action_profiles"])
    action_classes = set(fixture["universal_action_classes"])
    assert "text_only" in embodiment_profiles
    assert "office_workflow" in embodiment_profiles
    assert "browser" in embodiment_profiles
    assert "shell" in embodiment_profiles
    assert "file_system" in embodiment_profiles
    assert "network_api" in embodiment_profiles
    assert "database" in embodiment_profiles
    assert "scheduled_background_work" in embodiment_profiles
    assert "iot_device" in embodiment_profiles
    assert "mobile_robot" in embodiment_profiles
    assert "drone" in embodiment_profiles
    assert "humanoid" in embodiment_profiles
    assert "physical_world_actuator" in embodiment_profiles
    assert "emergency_stop" in embodiment_profiles
    assert "robot_motion" in action_classes
    assert "physical_world_action" in action_classes
    assert "iot_device_action" in action_classes
    assert "human_proximity_action" in action_classes


def test_phase_42_2_records_adapter_boundary_without_implementation() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    boundaries = set(fixture["adapter_boundary_taxonomy"])
    assert "planning_only" in boundaries
    assert "contract_preview" in boundaries
    assert "guardian_gated_adapter_required" in boundaries
    assert "paid_embodiment_unlock_required" in boundaries
    assert "blocked_without_explicit_approval" in boundaries
    assert fixture["robotics_iot_posture"] == "profile_vocabulary_blocked_or_deferred_no_hardware_calls"
    assert fixture["profile_vocabulary_grants_runtime_authority"] is False


def test_phase_42_2_stays_docs_tests_fixtures_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["runtime_behavior_changed"] is False
    assert not list((REPO_ROOT / "lima").rglob("*phase_42_2*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_42_2*"))
