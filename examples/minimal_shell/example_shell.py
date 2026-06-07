"""Minimal inert shell proof for consuming LIMA as a local dependency.

This example accepts no raw user text and performs no model, tool, file,
network, connector, device, robot, drone, or physical-world action.
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
    """Build already-normalized planning metadata for the minimal shell proof."""

    return KernelRequest(
        request_id="example-planning-001",
        shell_id="minimal-example-shell",
        actor_id="example-actor",
        session_id="example-session",
        normalized_intent={
            "action_category": "planning",
            "summary": "prepare a dry-run task plan",
            "risk_class": "low",
        },
        capability_profile=CapabilityProfile(profile_id="example-default-deny"),
        source_surface={
            "surface": "minimal_example_shell",
            "privacy_class": "synthetic",
        },
    )


def build_simulated_discovery_request() -> KernelRequest:
    """Build normalized simulated BLE discovery metadata for the proof."""

    return KernelRequest(
        request_id="example-simulated-discovery-001",
        shell_id="minimal-example-shell",
        actor_id="example-actor",
        session_id="example-session",
        normalized_intent={
            "action_category": "ble_discovery",
            "requested_capability": "ble_discovery",
            "connection_type": "ble",
            "discovery_mode": "simulated",
            "dry_run": True,
            "simulated_only": True,
            "include_simulated_surfaces": True,
            "risk_class": "low",
            "target_hint": "synthetic_ble_fixture",
        },
        capability_profile=CapabilityProfile(
            profile_id="example-simulated-discovery",
            ble_discovery=True,
        ),
        source_surface={
            "surface": "minimal_example_shell",
            "privacy_class": "synthetic",
        },
    )


def assert_non_execution_invariants(result: ExecutionResult) -> None:
    """Assert that a LIMA result remains dry-run and non-executing."""

    assert result.dry_run is True
    for field_name in NON_EXECUTION_FALSE_FIELDS:
        assert getattr(result, field_name) is False


def summarize_result(result: ExecutionResult) -> dict[str, object]:
    """Return a small redacted summary suitable for shell display."""

    simulated_discovery = result.metadata.get("simulated_discovery")
    return {
        "request_id": result.request_id,
        "state": result.state,
        "reason_code": result.guardian_summary.reason_code,
        "dry_run": result.dry_run,
        "event_refs": result.event_refs,
        "redacted_audit_summary": result.redacted_audit_summary,
        "simulated_discovery": simulated_discovery,
    }


def run_planning_preview() -> dict[str, object]:
    """Run a planning preview through LIMA with no execution authority."""

    result = LimaKernel().evaluate(build_planning_request())
    assert_non_execution_invariants(result)
    return summarize_result(result)


def run_simulated_discovery_preview() -> dict[str, object]:
    """Run explicit simulated discovery through LIMA and the inert adapter."""

    result = LimaKernel().evaluate(
        build_simulated_discovery_request(),
        simulated_discovery_adapter=SimulatedDiscoveryAdapter(),
    )
    assert_non_execution_invariants(result)
    return summarize_result(result)


def main() -> None:
    """Print redacted dry-run summaries for local manual inspection."""

    for summary in (run_planning_preview(), run_simulated_discovery_preview()):
        print(summary)


if __name__ == "__main__":
    main()
