"""Phase 42.4 universal runtime contract archive tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_42_4_UNIVERSAL_RUNTIME_CONTRACT_ARCHIVE_CLOSEOUT.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_42_4_universal_runtime_contract_archive_closeout.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_42_4_archives_universal_reframe() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "42.4"
    assert fixture["phase_42_reframed_from_arc_centered_to_universal_lima_ai_os"] is True
    assert fixture["arc_bot_role"] == "example_guarded_office_agent_consumer_profile_not_os_center"
    assert fixture["sparkbot_role"] == "reference_evidence_and_public_showcase_shell_only"
    text = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "Phase 42 was reframed from Arc-centered planning" in text
    assert "Arc Bot / LIMA Office is preserved as one example" in text


def test_phase_42_4_represents_future_profiles_and_product_split() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    profiles = set(fixture["future_consumer_embodiment_profiles_represented"])
    assert {"bots", "automation", "agents", "robots", "humanoids", "drones", "iot_devices"} <= profiles
    assert "lima_ai_os_universal_runtime_contract_vocabulary" in fixture["public_surface"]
    assert "sparkbot_public_showcase_compatible_reference_posture" in fixture["public_surface"]
    assert "arc_bot_lima_office_worker_bot_shell" in fixture["private_surface"]
    assert "paid_proprietary_robotics_iot_unlock_paths" in fixture["private_surface"]


def test_phase_42_4_recommends_phase_43_fixture_hardening_not_implementation() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase_43_recommended"] is True
    assert fixture["phase_43_lane"] == "docs_tests_fixtures_only_universal_contract_fixture_hardening"
    assert fixture["runtime_implementation_recommended"] is False
    categories = set(fixture["phase_43_fixture_categories"])
    assert "arc_bot_office_task_profile" in categories
    assert "sparkbot_reference_profile" in categories
    assert "drone_action_profile" in categories
    assert "humanoid_action_profile" in categories
    assert "robot_motion_profile" in categories
    assert "malicious_consumer_profile_trying_to_grant_approval" in categories
    assert "unknown_model_provider_data" in categories
    assert "nested_bypass_wording" in categories


def test_phase_42_4_preserves_hard_invariants() -> None:
    invariants = _load_json(PHASE_FIXTURE_PATH)["hard_invariants"]
    assert invariants["preview_only"] is True
    assert invariants["non_authoritative"] is True
    assert invariants["safe_by_default"] is True
    for key in (
        "execution_allowed",
        "side_effects_allowed",
        "approval_granted",
        "dispatch_allowed",
        "persistence_allowed",
        "humaninput_bridge_active",
        "sparkbot_wiring_active",
        "live_adapter_active",
        "external_calls_allowed",
        "robotics_allowed",
        "physical_world_allowed",
        "lima_grants_approval",
    ):
        assert invariants[key] is False


def test_phase_42_4_stays_docs_tests_fixtures_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["runtime_behavior_changed"] is False
    assert not list((REPO_ROOT / "lima").rglob("*phase_42_4*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_42_4*"))
