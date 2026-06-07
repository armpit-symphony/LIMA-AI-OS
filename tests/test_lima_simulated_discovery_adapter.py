"""Tests for the deterministic simulated discovery adapter."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from lima.kernel import (
    DiscoveryAdapterRequest,
    SimulatedDiscoveryAdapter,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
DISCOVERY_PATH = REPO_ROOT / "lima" / "kernel" / "discovery.py"


def _request(**overrides: object) -> DiscoveryAdapterRequest:
    values = {
        "request_id": "req-simulated-discovery",
        "actor_id": "actor-ref",
        "shell_id": "shell-ref",
        "session_id": "session-ref",
        "source_surface": {"surface": "unit_test", "privacy_class": "private"},
        "target_hint": "synthetic target",
        "connection_type": "wifi",
        "discovery_mode": "simulated",
        "dry_run": True,
        "simulated_only": True,
        "metadata": {"synthetic": True},
    }
    values.update(overrides)
    return DiscoveryAdapterRequest(**values)


def _assert_non_execution_invariants(result: object) -> None:
    assert result.executable is False
    assert result.execution_allowed is False
    assert result.side_effects_allowed is False
    assert result.dispatch_allowed is False
    assert result.persistence_allowed is False
    assert result.dry_run is True
    assert result.simulated_only is True
    assert result.live_discovery_executed is False
    assert result.connection_attempted is False
    assert result.pairing_attempted is False
    assert result.credentials_used is False
    assert result.session_opened is False
    assert result.device_control_executed is False
    assert result.physical_world_executed is False


def test_simulated_discovery_public_imports_are_available() -> None:
    from lima.kernel import (  # noqa: PLC0415
        DiscoveryAdapterManifest,
        DiscoveryAdapterResult,
        DiscoveryAdapterSurface,
    )

    assert DiscoveryAdapterManifest is not None
    assert DiscoveryAdapterRequest is not None
    assert DiscoveryAdapterResult is not None
    assert DiscoveryAdapterSurface is not None
    assert SimulatedDiscoveryAdapter is not None


def test_simulated_adapter_returns_deterministic_fake_surfaces() -> None:
    adapter = SimulatedDiscoveryAdapter()
    first = adapter.simulate(_request(connection_type="wifi"))
    second = adapter.simulate(_request(connection_type="wifi"))

    assert first.to_dict() == second.to_dict()
    assert first.state == "proposed"
    assert first.blocked_reason is None
    assert first.event_refs == ("discovery-adapter-event:1", "discovery-adapter-event:2")
    assert len(first.events) == 2
    assert len(first.surfaces) == 1
    assert first.surfaces[0].surface_id == "simulated-wifi-preview"
    assert first.surfaces[0].redacted_label == "Simulated WiFi preview"
    _assert_non_execution_invariants(first)


@pytest.mark.parametrize(
    ("connection_type", "surface_id"),
    (
        ("wifi", "simulated-wifi-preview"),
        ("ble", "simulated-ble-preview"),
        ("lan", "simulated-lan-preview"),
        ("iot", "simulated-iot-preview"),
    ),
)
def test_returned_surfaces_are_synthetic_inert_and_simulated(
    connection_type: str, surface_id: str
) -> None:
    result = SimulatedDiscoveryAdapter().simulate(_request(connection_type=connection_type))

    surface = result.surfaces[0]
    assert surface.surface_id == surface_id
    assert surface.synthetic is True
    assert surface.inert is True
    assert surface.simulated is True
    assert surface.connectable is False
    assert surface.controllable is False
    assert surface.physical_world is False
    _assert_non_execution_invariants(result)


def test_adapter_rejects_non_simulated_request() -> None:
    result = SimulatedDiscoveryAdapter().simulate(_request(simulated_only=False))

    assert result.state == "blocked"
    assert result.blocked_reason == "simulated_only_required"
    assert result.surfaces == ()
    _assert_non_execution_invariants(result)


def test_adapter_rejects_dry_run_false() -> None:
    result = SimulatedDiscoveryAdapter().simulate(_request(dry_run=False))

    assert result.state == "blocked"
    assert result.blocked_reason == "dry_run_required"
    assert result.surfaces == ()
    _assert_non_execution_invariants(result)


@pytest.mark.parametrize("mode", ("live", "scan", "discover", "connection", "pairing"))
def test_adapter_rejects_live_discovery_modes(mode: str) -> None:
    result = SimulatedDiscoveryAdapter().simulate(_request(discovery_mode=mode))

    assert result.state == "blocked"
    assert result.blocked_reason == "live_discovery_mode_blocked"
    _assert_non_execution_invariants(result)


def test_adapter_rejects_connection_attempt() -> None:
    result = SimulatedDiscoveryAdapter().simulate(
        _request(metadata={"operator_note": "auto-connect and open session"})
    )

    assert result.state == "blocked"
    assert result.blocked_reason == "connection_attempt_blocked"
    _assert_non_execution_invariants(result)


def test_adapter_rejects_pairing() -> None:
    result = SimulatedDiscoveryAdapter().simulate(_request(metadata={"action": "pair device"}))

    assert result.state == "blocked"
    assert result.blocked_reason == "pairing_blocked"
    _assert_non_execution_invariants(result)


def test_adapter_rejects_credential_ref() -> None:
    result = SimulatedDiscoveryAdapter().simulate(_request(credential_ref="vault-ref-only"))

    assert result.state == "blocked"
    assert result.blocked_reason == "credential_ref_not_supported"
    _assert_non_execution_invariants(result)


@pytest.mark.parametrize(
    "metadata",
    (
        {"password": "raw-password"},
        {"token": "raw-token"},
        {"api_key": "raw-key"},
        {"headers": {"authorization": "raw-header"}},
    ),
)
def test_adapter_rejects_raw_credential_like_fields(metadata: dict[str, object]) -> None:
    result = SimulatedDiscoveryAdapter().simulate(_request(metadata=metadata))
    result_text = str(result.to_dict())

    assert result.state == "blocked"
    assert result.blocked_reason == "raw_credential_like_field_blocked"
    assert "raw-password" not in result_text
    assert "raw-token" not in result_text
    assert "raw-key" not in result_text
    assert "raw-header" not in result_text
    _assert_non_execution_invariants(result)


@pytest.mark.parametrize(
    "metadata",
    (
        {"request": "robot control path"},
        {"request": "drone endpoint control"},
        {"request": "physical actuator movement"},
    ),
)
def test_adapter_rejects_robot_drone_and_physical_world_control(metadata: dict[str, object]) -> None:
    result = SimulatedDiscoveryAdapter().simulate(_request(connection_type="wifi", metadata=metadata))

    assert result.state == "blocked"
    assert result.blocked_reason == "physical_world_request_blocked"
    _assert_non_execution_invariants(result)


def test_adapter_rejects_unsupported_connection_type() -> None:
    result = SimulatedDiscoveryAdapter().simulate(_request(connection_type="unknown"))

    assert result.state == "blocked"
    assert result.blocked_reason == "unsupported_simulated_connection_type"
    _assert_non_execution_invariants(result)


def test_event_output_is_redacted_and_in_memory_only() -> None:
    result = SimulatedDiscoveryAdapter().simulate(
        _request(target_hint="private password token serial location")
    )

    assert result.state == "blocked"
    result_dict = result.to_dict()
    assert "private password token serial location" not in str(result_dict)
    for event in result.events:
        assert event.in_memory_only is True
        assert event.durable is False
        assert event.contains_secret is False
        assert event.contains_raw_scan_dump is False
        assert event.contains_physical_location is False


def test_discovery_module_has_no_forbidden_imports_or_calls() -> None:
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

    tree = ast.parse(DISCOVERY_PATH.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".")[0] not in forbidden_imports
        if isinstance(node, ast.ImportFrom) and node.module:
            assert node.module.split(".")[0] not in forbidden_imports
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            assert node.func.id not in forbidden_calls


def test_no_live_or_shell_wiring_strings_in_discovery_module() -> None:
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

    text = DISCOVERY_PATH.read_text(encoding="utf-8")
    for forbidden in forbidden_strings:
        assert forbidden not in text
