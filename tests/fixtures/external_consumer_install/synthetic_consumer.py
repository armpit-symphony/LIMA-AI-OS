"""Synthetic external consumer for LIMA import verification.

This fixture imports only LIMA public APIs and performs dry-run evaluations.
It is not Sparkbot, Arc Bot, shell wiring, or production integration.
"""

from __future__ import annotations

from lima.kernel import (
    CapabilityProfile,
    ExecutionResult,
    KernelRequest,
    LimaKernel,
    SimulatedDiscoveryAdapter,
)


NON_EXECUTION_FALSE_FIELDS = (
    "executable",
    "execution_allowed",
    "side_effects_allowed",
    "dispatch_allowed",
    "persistence_allowed",
    "model_calls_allowed",
    "model_calls_executed",
    "live_discovery_executed",
    "connection_attempted",
    "pairing_attempted",
    "credentials_used",
    "session_opened",
    "device_control_executed",
    "physical_world_allowed",
    "physical_world_executed",
    "guardian_decision_created",
    "approval_enforced",
    "humaninput_bridge_active",
    "sparkbot_wiring_active",
    "robo_os_wiring_active",
    "adapter_active",
    "tool_execution_allowed",
    "driver_execution_allowed",
    "scheduler_active",
    "external_calls_allowed",
)


def build_planning_request() -> KernelRequest:
    return KernelRequest(
        request_id="external-consumer-planning-001",
        shell_id="synthetic-external-consumer",
        actor_id="redacted-consumer-actor",
        session_id="redacted-consumer-session",
        normalized_intent={
            "action_category": "planning",
            "task_type": "dependency_import_preview",
            "risk_class": "low",
            "summary": "redacted external consumer planning preview",
            "input_origin": "synthetic_external_consumer",
            "execution_mode": "dry_run",
        },
        capability_profile=CapabilityProfile(profile_id="external-consumer-default-deny"),
        source_surface={
            "surface": "synthetic_external_consumer",
            "privacy_class": "synthetic",
            "contains_raw_prompt": False,
            "contains_secret": False,
            "contains_unsafe_payload": False,
        },
        metadata={
            "synthetic": True,
            "external_consumer_import_proof": True,
        },
    )


def build_simulated_discovery_request() -> KernelRequest:
    return KernelRequest(
        request_id="external-consumer-simulated-discovery-001",
        shell_id="synthetic-external-consumer",
        actor_id="redacted-consumer-actor",
        session_id="redacted-consumer-session",
        normalized_intent={
            "action_category": "ble_discovery",
            "requested_capability": "ble_discovery",
            "task_type": "simulated_dependency_preview",
            "risk_class": "low",
            "summary": "redacted external consumer simulated BLE preview",
            "input_origin": "synthetic_external_consumer",
            "execution_mode": "dry_run",
            "connection_type": "ble",
            "discovery_mode": "simulated",
            "dry_run": True,
            "simulated_only": True,
            "include_simulated_surfaces": True,
            "target_hint": "synthetic_ble_fixture",
        },
        capability_profile=CapabilityProfile(
            profile_id="external-consumer-simulated-discovery",
            ble_discovery=True,
        ),
        source_surface={
            "surface": "synthetic_external_consumer",
            "privacy_class": "synthetic",
            "contains_raw_prompt": False,
            "contains_secret": False,
            "contains_unsafe_payload": False,
        },
        metadata={
            "synthetic": True,
            "external_consumer_import_proof": True,
        },
    )


def assert_non_execution(result: ExecutionResult) -> None:
    assert result.dry_run is True
    for field_name in NON_EXECUTION_FALSE_FIELDS:
        assert getattr(result, field_name) is False


def run_planning_preview() -> ExecutionResult:
    result = LimaKernel().evaluate(build_planning_request())
    assert_non_execution(result)
    return result


def run_simulated_discovery_preview() -> ExecutionResult:
    result = LimaKernel().evaluate(
        build_simulated_discovery_request(),
        simulated_discovery_adapter=SimulatedDiscoveryAdapter(),
    )
    assert_non_execution(result)
    return result
