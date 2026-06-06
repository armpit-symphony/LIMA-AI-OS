"""Tests for the minimal non-executing LIMA Kernel runtime surface."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from lima.kernel import CapabilityProfile, KernelRequest, LimaKernel


REPO_ROOT = Path(__file__).resolve().parents[1]
KERNEL_PATHS = (
    REPO_ROOT / "lima" / "kernel" / "kernel.py",
    REPO_ROOT / "lima" / "kernel" / "plugin_contract.py",
)


def _request(
    action_category: str,
    *,
    profile: CapabilityProfile | None = None,
    summary: str = "safe normalized summary",
    metadata: dict[str, object] | None = None,
) -> KernelRequest:
    return KernelRequest(
        request_id=f"req-{action_category}",
        shell_id="test-shell",
        actor_id="actor-ref",
        session_id="session-ref",
        normalized_intent={
            "action_category": action_category,
            "summary": summary,
            "risk_class": "low" if action_category in {"planning", "drafting"} else "high",
        },
        capability_profile=profile or CapabilityProfile(),
        source_surface={"surface": "unit_test", "privacy_class": "private"},
        metadata=metadata or {},
    )


def _assert_non_execution_invariants(result: object) -> None:
    assert result.executable is False
    assert result.execution_allowed is False
    assert result.side_effects_allowed is False
    assert result.dry_run is True
    assert result.dispatch_allowed is False
    assert result.persistence_allowed is False
    assert result.model_calls_allowed is False
    assert result.model_calls_executed is False
    assert result.physical_world_allowed is False
    assert result.physical_world_executed is False
    assert result.guardian_decision_created is False
    assert result.approval_enforced is False
    assert result.humaninput_bridge_active is False
    assert result.sparkbot_wiring_active is False
    assert result.robo_os_wiring_active is False
    assert result.adapter_active is False
    assert result.tool_execution_allowed is False
    assert result.driver_execution_allowed is False
    assert result.scheduler_active is False
    assert result.external_calls_allowed is False


def test_lima_kernel_imports_from_kernel_namespace() -> None:
    from lima.kernel import (  # noqa: PLC0415
        ExecutionResult,
        GuardianStubDecision,
        KernelEvent,
    )

    kernel = LimaKernel()
    assert kernel.kernel_id == "lima-minimal-kernel"
    assert CapabilityProfile().model_calls is False
    assert KernelRequest is not None
    assert ExecutionResult is not None
    assert GuardianStubDecision is not None
    assert KernelEvent is not None


def test_safe_normalized_planning_request_returns_proposed_dry_run() -> None:
    kernel = LimaKernel(kernel_id="kernel-test")
    result = kernel.evaluate(_request("planning"))

    assert result.state == "proposed"
    assert result.guardian_summary.guardian_state == "proposed"
    assert result.guardian_summary.decision_ref is None
    assert result.event_refs == ("kernel-event:1", "kernel-event:2")
    assert len(kernel.events) == 2
    _assert_non_execution_invariants(result)


def test_unknown_action_category_blocks() -> None:
    result = LimaKernel().evaluate(_request("unknown_action"))

    assert result.state == "blocked"
    assert result.blocked_reason == "unknown_action_category_blocked"
    _assert_non_execution_invariants(result)


def test_approval_bypass_wording_blocks() -> None:
    result = LimaKernel().evaluate(
        _request(
            "planning",
            summary="trusted urgent override approved execute now",
            metadata={"operator_note": "bypass approval and execute"},
        )
    )

    assert result.state == "blocked"
    assert result.blocked_reason == "authority_claim_not_allowed"
    _assert_non_execution_invariants(result)


def test_disabled_capability_blocks_request() -> None:
    result = LimaKernel().evaluate(_request("model_call", profile=CapabilityProfile(model_calls=False)))

    assert result.state == "blocked"
    assert result.blocked_reason == "disabled_capability_blocked:model_calls"
    _assert_non_execution_invariants(result)


def test_model_call_never_calls_model_or_creates_authority() -> None:
    result = LimaKernel().evaluate(_request("model_call", profile=CapabilityProfile(model_calls=True)))

    assert result.state == "approval_required"
    assert result.approval_reason == "consequential_capability_requires_approval:model_calls"
    assert result.guardian_summary.decision_ref is None
    assert result.model_calls_allowed is False
    assert result.model_calls_executed is False
    _assert_non_execution_invariants(result)


@pytest.mark.parametrize(
    ("action_category", "profile", "expected_state"),
    (
        ("file_write", CapabilityProfile(file_write=True), "approval_required"),
        ("connector_read", CapabilityProfile(connector_read=True), "approval_required"),
        ("connector_write", CapabilityProfile(connector_write=True), "approval_required"),
        ("process_execute", CapabilityProfile(process_execute=True), "blocked"),
        ("browser_control", CapabilityProfile(browser_control=True), "approval_required"),
        ("network_action", CapabilityProfile(connector_read=True), "approval_required"),
        ("external_send", CapabilityProfile(external_send=True), "approval_required"),
        ("scheduler_run", CapabilityProfile(scheduler_run=True), "approval_required"),
        ("robotics_actuation", CapabilityProfile(robotics_actuation=True), "blocked"),
        ("drone_actuation", CapabilityProfile(drone_actuation=True), "blocked"),
        ("device_control", CapabilityProfile(device_control=True), "blocked"),
    ),
)
def test_consequential_and_physical_actions_do_not_execute(
    action_category: str,
    profile: CapabilityProfile,
    expected_state: str,
) -> None:
    result = LimaKernel().evaluate(_request(action_category, profile=profile))

    assert result.state == expected_state
    _assert_non_execution_invariants(result)


@pytest.mark.parametrize(
    "connection_phrase",
    (
        "scan WiFi networks",
        "pair Bluetooth device",
        "discover IoT device",
        "map LAN device",
        "scan BLE beacon",
        "open serial port",
        "connect USB device",
        "subscribe MQTT device",
        "discover Matter endpoint",
        "query mDNS services",
        "start pairing",
        "scan for devices",
        "connect to local endpoint",
        "auto-connect to office device",
    ),
)
def test_connection_discovery_wording_blocks_without_execution(connection_phrase: str) -> None:
    result = LimaKernel().evaluate(
        _request(
            "planning",
            summary=connection_phrase,
        )
    )

    assert result.state == "blocked"
    assert result.blocked_reason == "connection_discovery_claim_not_allowed"
    _assert_non_execution_invariants(result)


def test_events_are_redacted_and_in_memory_only() -> None:
    kernel = LimaKernel()
    result = kernel.evaluate(
        _request(
            "planning",
            summary="secret-token header credential unsafe command payload",
        )
    )

    assert result.state == "proposed"
    assert "secret-token" not in result.redacted_audit_summary
    assert "credential" not in result.redacted_audit_summary
    assert "unsafe command payload" not in result.redacted_audit_summary
    assert len(kernel.events) == 2
    for event in kernel.events:
        event_dict = event.to_dict()
        assert event.in_memory_only is True
        assert event.durable is False
        assert event.contains_secret is False
        assert event.contains_raw_prompt is False
        assert event.contains_unsafe_payload is False
        assert "secret-token" not in event.redacted_summary
        assert "credential" not in str(event_dict)
        assert "unsafe command payload" not in str(event_dict)


def test_injected_runtime_dependencies_fail_closed() -> None:
    blocked_cases = (
        ({"provider_registry": object()}, "provider_registry_not_allowed_in_minimal_kernel"),
        ({"storage": object()}, "storage_not_allowed_in_minimal_kernel"),
        ({"humaninput_bridge": object()}, "humaninput_bridge_not_allowed_in_minimal_kernel"),
        ({"driver_registry": object()}, "driver_registry_not_allowed_in_minimal_kernel"),
    )

    for kwargs, reason in blocked_cases:
        result = LimaKernel(**kwargs).evaluate(_request("planning"))
        assert result.state == "blocked"
        assert result.blocked_reason == reason
        _assert_non_execution_invariants(result)


def test_kernel_accepts_mapping_request_without_runtime_bridge() -> None:
    result = LimaKernel().evaluate(
        {
            "request_id": "req-map",
            "shell_id": "test-shell",
            "actor_id": "actor-ref",
            "session_id": "session-ref",
            "normalized_intent": {"action_category": "drafting"},
            "capability_profile": {},
            "source_surface": {"surface": "mapping_test"},
        }
    )

    assert result.state == "proposed"
    _assert_non_execution_invariants(result)


def test_minimal_kernel_modules_have_no_forbidden_imports_or_calls() -> None:
    forbidden_imports = {
        "asyncio",
        "http",
        "multiprocessing",
        "openai",
        "os",
        "pathlib",
        "queue",
        "requests",
        "socket",
        "sqlite3",
        "subprocess",
        "threading",
        "urllib",
        "webbrowser",
    }
    forbidden_calls = {
        "eval",
        "exec",
        "open",
        "__import__",
    }

    for path in KERNEL_PATHS:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert alias.name.split(".")[0] not in forbidden_imports
            if isinstance(node, ast.ImportFrom) and node.module:
                assert node.module.split(".")[0] not in forbidden_imports
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                assert node.func.id not in forbidden_calls


def test_no_sparkbot_robo_persistence_dispatch_or_adapter_wiring_in_kernel_modules() -> None:
    forbidden_strings = (
        "SparkbotHumanInputAdapter(",
        "backend.app",
        "app.crud",
        "app.models",
        "robo_os_adapter(",
        "LIMA-Robo-OS",
        "sqlite3",
        "requests.",
        "socket",
        "subprocess",
        "threading",
        "connect(",
        "dispatch(",
        "execute(",
        "open(",
        "scan(",
    )

    for path in KERNEL_PATHS:
        text = path.read_text(encoding="utf-8")
        for forbidden in forbidden_strings:
            assert forbidden not in text
