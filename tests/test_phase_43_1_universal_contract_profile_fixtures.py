"""Phase 43.1 universal contract profile fixture corpus tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_43_1_universal_contract_profile_fixtures.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_43_1_fixture_corpus_is_docs_tests_fixtures_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "43.1"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["fixture_data_only"] is True
    assert fixture["runtime_implementation_approved"] is False
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["runtime_behavior_changed"] is False


def test_phase_43_1_includes_all_universal_profile_cases() -> None:
    fixture_ids = {case["id"] for case in _load_json(PHASE_FIXTURE_PATH)["cases"]}
    assert fixture_ids == {
        "arc_bot_office_task_profile",
        "sparkbot_reference_profile",
        "generic_automation_agent_profile",
        "coding_agent_profile",
        "research_agent_profile",
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
        "malicious_consumer_profile_trying_to_grant_approval",
        "malicious_embodiment_profile_trying_to_allow_execution",
        "malformed_profile_data",
        "unknown_model_provider_data",
        "nested_bypass_wording",
    }


def test_phase_43_1_cases_carry_required_safe_control_flags() -> None:
    required_flags = _load_json(PHASE_FIXTURE_PATH)["required_case_flags"]
    for case in _load_json(PHASE_FIXTURE_PATH)["cases"]:
        assert case["control_flags"] == required_flags
        assert case["expected_profile_state"] in {"proposed", "needs_review", "blocked"}
        assert isinstance(case["expected_blocked_claims"], list)
        assert case["profile_kind"] in {
            "consumer_profile",
            "embodiment_action_profile",
            "adversarial_profile",
        }


def test_phase_43_1_risky_and_adversarial_profiles_fail_closed() -> None:
    cases = {case["id"]: case for case in _load_json(PHASE_FIXTURE_PATH)["cases"]}
    blocked_ids = {
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
        "malicious_consumer_profile_trying_to_grant_approval",
        "malicious_embodiment_profile_trying_to_allow_execution",
        "malformed_profile_data",
        "unknown_model_provider_data",
        "nested_bypass_wording",
    }
    for case_id in blocked_ids:
        assert cases[case_id]["expected_profile_state"] == "blocked"
        assert cases[case_id]["expected_blocked_claims"]


def test_phase_43_1_safe_planning_profiles_do_not_claim_runtime_authority() -> None:
    cases = {case["id"]: case for case in _load_json(PHASE_FIXTURE_PATH)["cases"]}
    for case_id in (
        "arc_bot_office_task_profile",
        "sparkbot_reference_profile",
        "generic_automation_agent_profile",
        "coding_agent_profile",
        "research_agent_profile",
    ):
        assert cases[case_id]["expected_profile_state"] in {"proposed", "needs_review"}
        assert cases[case_id]["control_flags"]["execution_allowed"] is False
        assert cases[case_id]["control_flags"]["approval_granted"] is False
        assert cases[case_id]["control_flags"]["dispatch_allowed"] is False
        assert cases[case_id]["control_flags"]["persistence_allowed"] is False
        assert cases[case_id]["control_flags"]["lima_grants_approval"] is False


def test_phase_43_1_stays_out_of_runtime_and_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_43_1*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_43_1*"))
