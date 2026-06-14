"""Static case checks for V1-G6 haptic intent metadata."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = REPO_ROOT / "tests" / "fixtures" / "runtime_extraction"
CASE_NAMES = (
    "v1_g6_received_soft_ack_intent.json",
    "v1_g6_thinking_progress_pulse_intent.json",
    "v1_g6_preview_ready_light_tap_intent.json",
    "v1_g6_blocked_warning_intent.json",
    "v1_g6_needs_approval_attention_intent.json",
    "v1_g6_completed_success_intent.json",
    "v1_g6_failed_safe_error_intent.json",
    "v1_g6_deferred_neutral_hold_intent.json",
    "v1_g6_forged_device_haptic_claim_fail_closed.json",
)


def _load_json(path: Path) -> dict[str, Any]:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _cases() -> list[dict[str, Any]]:
    return [_load_json(FIXTURE_DIR / name) for name in CASE_NAMES]


def test_v1_g6_case_fixture_files_exist() -> None:
    for fixture_name in CASE_NAMES:
        assert (FIXTURE_DIR / fixture_name).exists()


def test_v1_g6_cases_cover_required_state_families() -> None:
    state_to_family = {
        case["source_response_state"]: case["haptic_intent"]["haptic_intent_family"]
        for case in _cases()
        if case["case_family"] == "haptic_intent_static_state_mapping"
    }
    assert state_to_family == {
        "received": "soft_ack",
        "thinking": "progress_pulse",
        "preview_ready": "light_tap",
        "blocked": "warning",
        "needs_approval": "attention",
        "completed": "success",
        "failed_safe": "error_alert",
        "deferred": "neutral_hold",
    }


def test_v1_g6_positive_state_cases_are_non_device_specific() -> None:
    forbidden = {
        "actuator_id",
        "device_id",
        "vibration_command",
        "motor_pattern",
        "os_haptic_api",
        "execute_haptic_now",
        "hardware_target",
        "physical_feedback_command",
    }
    for case in _cases():
        if case["case_family"] != "haptic_intent_static_state_mapping":
            continue
        intent = case["haptic_intent"]
        assert forbidden.isdisjoint(intent)
        assert case["static_review_result"]["accepted_as_static_evidence"] is True
        assert case["static_review_result"]["accepted_as_device_behavior"] is False
        gates = case["haptic_boundary_gates"]
        assert gates["shell_owns_haptics"] is True
        assert gates["lima_owns_device_haptics"] is False
        assert gates["non_device_specific_intent"] is True
        assert gates["accessibility_respected"] is True
        assert gates["fallback_state_defined"] is True
        assert gates["no_actuator_or_device_target"] is True
        assert gates["no_os_or_hardware_api"] is True


def test_v1_g6_forged_device_haptic_claim_fails_closed() -> None:
    forged = [
        case
        for case in _cases()
        if case["case_id"] == "v1_g6_forged_device_haptic_claim_fail_closed"
    ][0]
    claimed = forged["claimed_device_behavior"]
    assert claimed["actuator_id"] == "claimed-phone-linear-actuator"
    assert claimed["vibration_command"] == "vibrate-now"
    assert claimed["execute_haptic_now"] is True
    assert claimed["lima_owns_device_haptics"] is True
    assert claimed["shell_rendering_bypassed"] is True
    assert forged["static_review_result"]["accepted_as_device_behavior"] is False
    assert forged["static_review_result"]["forged_device_haptic_claim_rejected"] is True
    assert forged["packet_status"] == "blocked"
    assert forged["kernel_status"] == "blocked"
    blocked = set(forged["expected_blocked_claims"])
    assert "device_vibration_command" in blocked
    assert "actuator_id_claim" in blocked
    assert "execute_haptic_now_claim" in blocked
    assert "lima_device_haptics_ownership_claim" in blocked
    assert "shell_rendering_bypass_claim" in blocked


def test_v1_g6_cases_never_trigger_runtime_or_physical_behavior() -> None:
    for case in _cases():
        flags = case["control_flags"]
        assert flags["non_authoritative"] is True
        assert flags["safe_by_default"] is True
        assert flags["local_only"] is True
        assert flags["deterministic"] is True
        assert flags["haptic_intent_metadata_defined"] is True
        for key in (
            "haptic_device_behavior_allowed",
            "device_vibration_allowed",
            "tactile_hardware_allowed",
            "os_haptic_api_allowed",
            "actuator_command_allowed",
            "shell_rendering_invoked",
            "provider_model_routing_active",
            "provider_model_call_allowed",
            "guardian_decision_created",
            "approval_granted",
            "approval_enforcement_active",
            "execution_allowed",
            "dispatch_allowed",
            "persistence_allowed",
            "external_calls_allowed",
            "tool_calls_allowed",
            "driver_calls_allowed",
            "adapter_calls_allowed",
            "file_mutation_allowed",
            "connector_mutation_allowed",
            "audit_persistence_allowed",
            "browser_file_network_device_robotics_allowed",
            "physical_world_allowed",
            "runtime_test_harness_active",
        ):
            assert flags[key] is False


def test_v1_g6_case_suite_does_not_touch_runtime_or_support_paths() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*v1_g6*"))
    support = REPO_ROOT / "tests" / "support"
    if support.exists():
        assert not list(support.rglob("*v1_g6*"))
