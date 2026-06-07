"""Tests for explicit LimaKernel simulated discovery adapter wiring."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from lima.kernel import (
    CapabilityProfile,
    DiscoveryAdapterManifest,
    DiscoveryAdapterResult,
    DiscoveryAdapterSurface,
    KernelRequest,
    LimaKernel,
    SimulatedDiscoveryAdapter,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
KERNEL_PATH = REPO_ROOT / "lima" / "kernel" / "kernel.py"


def _request(**intent_overrides: object) -> KernelRequest:
    intent = {
        "action_category": "ble_discovery",
        "requested_capability": "ble_discovery",
        "connection_type": "ble",
        "discovery_mode": "simulated",
        "dry_run": True,
        "simulated_only": True,
        "include_simulated_surfaces": True,
        "risk_class": "low",
        "target_hint": "synthetic_ble_fixture",
    }
    intent.update(intent_overrides)
    return KernelRequest(
        request_id="req-kernel-simulated-discovery",
        shell_id="shell-ref",
        actor_id="actor-ref",
        session_id="session-ref",
        normalized_intent=intent,
        capability_profile=CapabilityProfile(ble_discovery=True),
        source_surface={"surface": "unit_test", "privacy_class": "private"},
        metadata={},
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
    assert result.live_discovery_executed is False
    assert result.connection_attempted is False
    assert result.pairing_attempted is False
    assert result.credentials_used is False
    assert result.session_opened is False
    assert result.device_control_executed is False
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


def test_explicit_simulated_adapter_returns_synthetic_surfaces_in_dry_run_metadata() -> None:
    result = LimaKernel().evaluate(
        _request(),
        simulated_discovery_adapter=SimulatedDiscoveryAdapter(),
    )

    assert result.state == "proposed"
    assert result.blocked_reason is None
    assert result.metadata["simulated_adapter_used"] is True
    simulated = result.metadata["simulated_discovery"]
    assert simulated["adapter_id"] == "simulated-discovery-adapter"
    assert simulated["state"] == "proposed"
    assert simulated["event_refs"] == (
        "discovery-adapter-event:1",
        "discovery-adapter-event:2",
    )
    assert simulated["surfaces"] == (
        {
            "surface_id": "simulated-ble-preview",
            "connection_type": "ble",
            "synthetic": True,
            "inert": True,
            "simulated": True,
            "connectable": False,
            "controllable": False,
            "physical_world": False,
        },
    )
    assert "simulated_discovery_synthetic_only" in result.warnings
    _assert_non_execution_invariants(result)


def test_absent_adapter_returns_classification_only_when_surfaces_not_requested() -> None:
    result = LimaKernel().evaluate(_request(include_simulated_surfaces=False))

    assert result.state == "proposed"
    assert "simulated_discovery" not in result.metadata
    assert "simulated_adapter_used" not in result.metadata
    _assert_non_execution_invariants(result)


def test_absent_adapter_blocks_when_request_demands_simulated_surfaces() -> None:
    result = LimaKernel().evaluate(_request())

    assert result.state == "blocked"
    assert result.blocked_reason == "simulated_discovery_adapter_required"
    assert "simulated_discovery" not in result.metadata
    _assert_non_execution_invariants(result)


@pytest.mark.parametrize(
    ("field_name", "field_value"),
    (
        ("discovery_mode", "scan"),
        ("dry_run", False),
        ("simulated_only", False),
        ("target_hint", "connect to device"),
        ("target_hint", "pair device"),
        ("target_hint", "password token key"),
        ("target_hint", "robot drone actuator"),
        ("target_hint", "auto-connect to anything"),
        ("target_hint", "try everything"),
    ),
)
def test_explicit_adapter_blocks_non_strict_simulated_metadata(
    field_name: str, field_value: object
) -> None:
    result = LimaKernel().evaluate(
        _request(**{field_name: field_value}),
        simulated_discovery_adapter=SimulatedDiscoveryAdapter(),
    )

    assert result.state == "blocked"
    assert result.blocked_reason in {
        "strict_simulated_discovery_metadata_required",
        "auto_connect_request_blocked",
        "credential_use_request_blocked",
        "device_pairing_request_blocked",
        "simulated_discovery_adapter_blocked:connection_attempt_blocked",
        "try_everything_connection_request_blocked",
    }
    assert "simulated_discovery" not in result.metadata
    _assert_non_execution_invariants(result)


def test_disabled_capability_blocks_before_adapter_metadata_is_added() -> None:
    request = _request()
    request = KernelRequest(
        request_id=request.request_id,
        shell_id=request.shell_id,
        actor_id=request.actor_id,
        session_id=request.session_id,
        normalized_intent=request.normalized_intent,
        capability_profile=CapabilityProfile(ble_discovery=False),
        source_surface=request.source_surface,
    )

    result = LimaKernel().evaluate(
        request,
        simulated_discovery_adapter=SimulatedDiscoveryAdapter(),
    )

    assert result.state == "blocked"
    assert result.blocked_reason == "disabled_capability_blocked:ble_discovery"
    assert "simulated_discovery" not in result.metadata
    _assert_non_execution_invariants(result)


def test_invalid_simulated_adapter_manifest_blocks_without_invoking_adapter() -> None:
    class UnsafeAdapter:
        manifest = DiscoveryAdapterManifest(supports_live_discovery=True)

        def simulate(self, request: object) -> object:
            raise AssertionError("unsafe adapter should not be invoked")

    result = LimaKernel().evaluate(_request(), simulated_discovery_adapter=UnsafeAdapter())

    assert result.state == "blocked"
    assert result.blocked_reason == "invalid_simulated_discovery_adapter_manifest"
    assert "simulated_discovery" not in result.metadata
    _assert_non_execution_invariants(result)


def test_adapter_error_blocks_with_redacted_reason() -> None:
    class ErrorAdapter:
        manifest = DiscoveryAdapterManifest()

        def simulate(self, request: object) -> object:
            raise RuntimeError("raw token should not be returned")

    result = LimaKernel().evaluate(_request(), simulated_discovery_adapter=ErrorAdapter())

    assert result.state == "blocked"
    assert result.blocked_reason == "simulated_discovery_adapter_error"
    assert "raw token" not in str(result.to_dict())
    _assert_non_execution_invariants(result)


def test_unsafe_adapter_result_blocks() -> None:
    class UnsafeResultAdapter:
        manifest = DiscoveryAdapterManifest()

        def simulate(self, request: object) -> DiscoveryAdapterResult:
            return DiscoveryAdapterResult(
                request_id="req-unsafe",
                adapter_id="unsafe",
                adapter_type="simulated_discovery_adapter",
                state="proposed",
                redacted_summary="synthetic preview",
                event_refs=(),
                surfaces=(
                    DiscoveryAdapterSurface(
                        surface_id="unsafe-connectable-surface",
                        connection_type="ble",
                        redacted_label="Unsafe surface",
                        connectable=True,
                    ),
                ),
            )

    result = LimaKernel().evaluate(
        _request(),
        simulated_discovery_adapter=UnsafeResultAdapter(),
    )

    assert result.state == "blocked"
    assert result.blocked_reason == "unsafe_simulated_discovery_surface_blocked"
    assert "simulated_discovery" not in result.metadata
    _assert_non_execution_invariants(result)


def test_adapter_blocked_result_preserves_kernel_blocked_state() -> None:
    request = KernelRequest(
        request_id="req-unsupported-simulated-type",
        shell_id="shell-ref",
        actor_id="actor-ref",
        session_id="session-ref",
        normalized_intent={
            "action_category": "connection_discovery",
            "requested_capability": "connection_discovery",
            "connection_type": "network",
            "discovery_mode": "simulated",
            "dry_run": True,
            "simulated_only": True,
            "include_simulated_surfaces": True,
            "risk_class": "low",
        },
        capability_profile=CapabilityProfile(connection_discovery=True),
        source_surface={"surface": "unit_test", "privacy_class": "private"},
    )

    result = LimaKernel().evaluate(
        request,
        simulated_discovery_adapter=SimulatedDiscoveryAdapter(),
    )

    assert result.state == "blocked"
    assert result.blocked_reason == (
        "simulated_discovery_adapter_blocked:unsupported_simulated_connection_type"
    )
    assert "simulated_discovery" not in result.metadata
    _assert_non_execution_invariants(result)


def test_kernel_simulated_wiring_has_no_forbidden_imports_or_calls() -> None:
    forbidden_imports = {
        "asyncio",
        "bluetooth",
        "http",
        "multiprocessing",
        "openai",
        "os",
        "paho",
        "queue",
        "requests",
        "serial",
        "socket",
        "sqlite3",
        "subprocess",
        "threading",
        "urllib",
        "usb",
        "webbrowser",
        "zeroconf",
    }
    forbidden_calls = {
        "__import__",
        "connect",
        "eval",
        "exec",
        "open",
        "pair",
        "scan",
    }

    tree = ast.parse(KERNEL_PATH.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".")[0] not in forbidden_imports
        if isinstance(node, ast.ImportFrom) and node.module:
            assert node.module.split(".")[0] not in forbidden_imports
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            assert node.func.id not in forbidden_calls


def test_kernel_simulated_wiring_has_no_live_or_shell_wiring_strings() -> None:
    forbidden_strings = (
        "BluetoothSocket",
        "SparkbotHumanInputAdapter(",
        "backend.app",
        "connect(",
        "dispatch(",
        "execute(",
        "open(",
        "paho.mqtt",
        "requests.",
        "robo_os_adapter(",
        "scan(",
        "serial.Serial",
        "socket.",
        "subprocess",
        "threading",
        "zeroconf",
    )

    text = KERNEL_PATH.read_text(encoding="utf-8")
    for forbidden in forbidden_strings:
        assert forbidden not in text
