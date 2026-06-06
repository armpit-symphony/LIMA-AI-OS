"""Connection intent classification tests for the minimal LIMA Kernel."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

import pytest

from lima.kernel import CapabilityProfile, KernelRequest, LimaKernel


REPO_ROOT = Path(__file__).resolve().parents[1]
KERNEL_PATHS = (
    REPO_ROOT / "lima" / "kernel" / "kernel.py",
    REPO_ROOT / "lima" / "kernel" / "plugin_contract.py",
)


def _profile(**enabled: bool) -> CapabilityProfile:
    return CapabilityProfile(**enabled)


def _connection_request(
    capability: str,
    *,
    profile: CapabilityProfile | None = None,
    domain: str = "local_metadata",
    mode: str = "passive",
    risk: str = "low",
    summary: str = "redacted connection metadata preview",
    extra: dict[str, Any] | None = None,
) -> KernelRequest:
    normalized_intent: dict[str, Any] = {
        "action_category": capability,
        "requested_capability": capability,
        "discovery_domain": domain,
        "discovery_mode": mode,
        "risk_class": risk,
        "summary": summary,
    }
    if extra:
        normalized_intent.update(extra)
    return KernelRequest(
        request_id=f"req-{capability}",
        shell_id="test-shell",
        actor_id="actor-ref",
        session_id="session-ref",
        normalized_intent=normalized_intent,
        capability_profile=profile or CapabilityProfile(),
        source_surface={"surface": "connection_test", "privacy_class": "private"},
    )


def _assert_dry_run_only(result: object) -> None:
    assert result.executable is False
    assert result.execution_allowed is False
    assert result.side_effects_allowed is False
    assert result.dispatch_allowed is False
    assert result.persistence_allowed is False
    assert result.dry_run is True
    assert result.model_calls_executed is False
    assert result.live_discovery_executed is False
    assert result.connection_attempted is False
    assert result.pairing_attempted is False
    assert result.credentials_used is False
    assert result.session_opened is False
    assert result.device_control_executed is False
    assert result.physical_world_executed is False
    assert result.tool_execution_allowed is False
    assert result.driver_execution_allowed is False
    assert result.scheduler_active is False
    assert result.external_calls_allowed is False


def test_safe_passive_metadata_preview_returns_proposed_dry_run() -> None:
    result = LimaKernel().evaluate(
        _connection_request(
            "connection_discovery",
            profile=_profile(connection_discovery=True),
            domain="local_metadata",
            mode="passive",
        )
    )

    assert result.state == "proposed"
    assert result.guardian_summary.reason_code.startswith("connection_discovery_metadata_proposed")
    assert result.event_refs == ("kernel-event:1", "kernel-event:2")
    _assert_dry_run_only(result)


def test_simulated_wifi_discovery_returns_safe_dry_run_result() -> None:
    result = LimaKernel().evaluate(
        _connection_request(
            "wifi_discovery",
            profile=_profile(wifi_discovery=True),
            domain="wifi",
            mode="simulated",
            risk="low",
        )
    )

    assert result.state in {"proposed", "approval_required"}
    assert result.guardian_summary.decision_ref is None
    _assert_dry_run_only(result)


def test_wifi_discovery_with_disabled_capability_blocks() -> None:
    result = LimaKernel().evaluate(
        _connection_request("wifi_discovery", profile=CapabilityProfile(), domain="wifi")
    )

    assert result.state == "blocked"
    assert result.blocked_reason == "disabled_capability_blocked:wifi_discovery"
    _assert_dry_run_only(result)


@pytest.mark.parametrize(
    ("capability", "domain"),
    (
        ("bluetooth_discovery", "bluetooth"),
        ("ble_discovery", "ble"),
    ),
)
def test_bluetooth_and_ble_discovery_remain_dry_run_only(
    capability: str,
    domain: str,
) -> None:
    result = LimaKernel().evaluate(
        _connection_request(
            capability,
            profile=_profile(**{capability: True}),
            domain=domain,
            mode="simulated",
        )
    )

    assert result.state in {"proposed", "approval_required"}
    _assert_dry_run_only(result)


def test_lan_scan_blocks() -> None:
    result = LimaKernel().evaluate(
        _connection_request(
            "network_discovery",
            profile=_profile(network_discovery=True),
            domain="lan",
            mode="live",
            summary="scan LAN for devices",
        )
    )

    assert result.state == "blocked"
    assert result.blocked_reason == "unauthenticated_network_scan_blocked"
    _assert_dry_run_only(result)


@pytest.mark.parametrize(
    ("capability", "domain"),
    (
        ("usb_discovery", "usb"),
        ("serial_discovery", "serial"),
        ("mqtt_discovery", "mqtt"),
        ("matter_discovery", "matter"),
        ("mdns_discovery", "mdns"),
    ),
)
def test_protocol_and_bus_discovery_never_executes(capability: str, domain: str) -> None:
    result = LimaKernel().evaluate(
        _connection_request(
            capability,
            profile=_profile(**{capability: True}),
            domain=domain,
            mode="live",
            risk="medium",
        )
    )

    assert result.state in {"approval_required", "blocked"}
    _assert_dry_run_only(result)


@pytest.mark.parametrize(
    ("capability", "reason"),
    (
        ("connection_attempt", "connection_or_physical_capability_blocked:connection_attempt"),
        ("device_pairing", "connection_or_physical_capability_blocked:device_pairing"),
        ("credential_use", "connection_or_physical_capability_blocked:credential_use"),
        ("iot_control", "connection_or_physical_capability_blocked:iot_control"),
        ("device_control", "connection_or_physical_capability_blocked:device_control"),
        (
            "physical_world_actuation",
            "connection_or_physical_capability_blocked:physical_world_actuation",
        ),
    ),
)
def test_connection_control_and_physical_capabilities_block(
    capability: str,
    reason: str,
) -> None:
    result = LimaKernel().evaluate(
        _connection_request(capability, profile=_profile(**{capability: True}))
    )

    assert result.state == "blocked"
    assert result.blocked_reason == reason
    _assert_dry_run_only(result)


def test_credential_wording_blocks_before_discovery_result() -> None:
    result = LimaKernel().evaluate(
        _connection_request(
            "wifi_discovery",
            profile=_profile(wifi_discovery=True),
            domain="wifi",
            summary="use password token header to inspect wifi",
        )
    )

    assert result.state == "blocked"
    assert result.blocked_reason == "credential_use_request_blocked"
    _assert_dry_run_only(result)


def test_auto_connect_blocks() -> None:
    result = LimaKernel().evaluate(
        _connection_request(
            "connection_discovery",
            profile=_profile(connection_discovery=True),
            summary="auto-connect to available local device",
        )
    )

    assert result.state == "blocked"
    assert result.blocked_reason == "auto_connect_request_blocked"
    _assert_dry_run_only(result)


def test_try_everything_blocks() -> None:
    result = LimaKernel().evaluate(
        _connection_request(
            "connection_discovery",
            profile=_profile(connection_discovery=True),
            summary="try everything until something connects",
        )
    )

    assert result.state == "blocked"
    assert result.blocked_reason == "try_everything_connection_request_blocked"
    _assert_dry_run_only(result)


def test_unknown_connection_type_blocks() -> None:
    result = LimaKernel().evaluate(
        _connection_request(
            "connection_discovery",
            profile=_profile(connection_discovery=True),
            domain="unknown_mesh",
        )
    )

    assert result.state == "blocked"
    assert result.blocked_reason == "unknown_connection_type_blocked"
    _assert_dry_run_only(result)


@pytest.mark.parametrize(
    "capability",
    ("robotics_endpoint_discovery", "drone_endpoint_discovery"),
)
def test_robot_and_drone_endpoints_block(capability: str) -> None:
    result = LimaKernel().evaluate(
        _connection_request(capability, profile=_profile(**{capability: True}))
    )

    assert result.state == "blocked"
    assert result.blocked_reason == f"connection_or_physical_capability_blocked:{capability}"
    _assert_dry_run_only(result)


def test_connection_events_are_redacted_and_in_memory_only() -> None:
    kernel = LimaKernel()
    result = kernel.evaluate(
        _connection_request(
            "connection_discovery",
            profile=_profile(connection_discovery=True),
            summary=(
                "private SSID password token header raw Bluetooth MAC "
                "192.168.1.1 serial number pairing code"
            ),
        )
    )

    assert result.state == "blocked"
    assert result.event_refs == ("kernel-event:1", "kernel-event:2")
    assert [event.event_type for event in kernel.events] == [
        "connection_discovery_requested",
        "connection_discovery_blocked",
    ]
    for event in kernel.events:
        event_text = str(event.to_dict()).lower()
        assert event.in_memory_only is True
        assert event.durable is False
        assert event.contains_secret is False
        assert event.contains_raw_prompt is False
        assert event.contains_unsafe_payload is False
        assert "password" not in event_text
        assert "token" not in event_text
        assert "192.168" not in event_text
        assert "pairing code" not in event_text
    _assert_dry_run_only(result)


def test_connection_classifier_introduces_no_live_api_imports_or_calls() -> None:
    forbidden_imports = {
        "asyncio",
        "bleak",
        "bluetooth",
        "dbus",
        "http",
        "matter",
        "mdns",
        "multiprocessing",
        "openai",
        "os",
        "paho",
        "pathlib",
        "pyserial",
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
        "discover",
        "enumerate",
        "eval",
        "exec",
        "open",
        "pair",
        "scan",
        "socket",
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


def test_connection_classifier_has_no_wiring_or_adapter_strings() -> None:
    forbidden_strings = (
        "backend.app",
        "app.crud",
        "app.models",
        "ArcBot",
        "SparkbotHumanInputAdapter(",
        "robo_os_adapter(",
        "requests.",
        "subprocess",
        "threading",
        "socket.",
        "sqlite3",
        "BluetoothSocket",
        "serial.Serial",
        "paho.mqtt",
        "zeroconf",
        "Matter",
    )

    for path in KERNEL_PATHS:
        text = path.read_text(encoding="utf-8")
        for forbidden in forbidden_strings:
            assert forbidden not in text
