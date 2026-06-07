from __future__ import annotations

import ast
import importlib.util
import json
import pathlib
import tomllib
from typing import Any, Mapping

import lima
from lima.kernel import ExecutionResult, LimaKernel


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURE_DIR = REPO_ROOT / "tests" / "fixtures" / "external_consumer_install"
CONSUMER_PATH = FIXTURE_DIR / "synthetic_consumer.py"
METADATA_PATH = FIXTURE_DIR / "consumer_metadata.json"
PYPROJECT_PATH = REPO_ROOT / "pyproject.toml"
ALLOWED_IMPORT_ROOTS = {"__future__", "lima"}
FORBIDDEN_IMPORT_ROOTS = {
    "arc",
    "arcbot",
    "bluetooth",
    "bleak",
    "browser",
    "dbus",
    "fastapi",
    "matter",
    "mdns",
    "mqtt",
    "openai",
    "openrouter",
    "ollama",
    "paho",
    "pip",
    "playwright",
    "pybluez",
    "robo",
    "robo_os",
    "serial",
    "socket",
    "sparkbot",
    "subprocess",
    "threading",
    "usb",
    "venv",
    "webbrowser",
}
FORBIDDEN_SOURCE_MARKERS = {
    "pip install",
    "python -m build",
    "subprocess.",
    "socket.",
    "threading.",
    "openai",
    "credential_ref",
    "password=",
    "token=",
    "secret=",
    "api_key=",
}
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


def _load_metadata() -> Mapping[str, Any]:
    return json.loads(METADATA_PATH.read_text(encoding="utf-8"))


def _load_consumer_module():
    spec = importlib.util.spec_from_file_location("synthetic_lima_external_consumer", CONSUMER_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _assert_non_execution_result(result: ExecutionResult) -> None:
    assert result.dry_run is True
    for field_name in NON_EXECUTION_FALSE_FIELDS:
        assert getattr(result, field_name) is False


def _import_roots(path: pathlib.Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        if isinstance(node, ast.ImportFrom) and node.module:
            roots.add(node.module.split(".")[0])
    return roots


def test_package_metadata_and_public_imports_are_available() -> None:
    pyproject = tomllib.loads(PYPROJECT_PATH.read_text(encoding="utf-8"))

    assert pyproject["project"]["name"] == "lima-runtime"
    assert pyproject["project"]["version"] == "0.0.1"
    assert pyproject["tool"]["setuptools"]["packages"]["find"]["include"] == ["lima*"]
    assert lima is not None
    assert LimaKernel is not None


def test_external_consumer_metadata_is_mode_a_local_only() -> None:
    metadata = _load_metadata()

    assert metadata["schema_version"] == "0.1"
    assert metadata["verification_mode"] == "subprocess_free_import_verification"
    assert metadata["imports_allowed"] == ["lima", "lima.kernel"]
    assert metadata["expected_package_name"] == "lima-runtime"
    assert metadata["expected_kernel_import"] == "LimaKernel"
    assert metadata["expected_result"]["dry_run"] is True
    assert metadata["expected_result"]["executable"] is False
    assert metadata["expected_result"]["execution_allowed"] is False
    assert all(metadata["forbidden"].values())


def test_synthetic_external_consumer_imports_only_lima_public_api() -> None:
    import_roots = _import_roots(CONSUMER_PATH)

    assert import_roots <= ALLOWED_IMPORT_ROOTS
    assert not (import_roots & FORBIDDEN_IMPORT_ROOTS)


def test_synthetic_external_consumer_source_avoids_forbidden_surfaces() -> None:
    source = CONSUMER_PATH.read_text(encoding="utf-8").lower()

    assert not any(marker in source for marker in FORBIDDEN_SOURCE_MARKERS)


def test_synthetic_external_consumer_planning_preview_is_dry_run() -> None:
    consumer = _load_consumer_module()
    result = consumer.run_planning_preview()

    assert result.state == "proposed"
    assert result.guardian_summary.reason_code == "text_preview_or_planning_proposed"
    _assert_non_execution_result(result)


def test_synthetic_external_consumer_simulated_discovery_is_synthetic_only() -> None:
    consumer = _load_consumer_module()
    result = consumer.run_simulated_discovery_preview()

    assert result.state == "proposed"
    assert result.guardian_summary.reason_code == (
        "simulated_connection_discovery_proposed:ble_discovery"
    )
    _assert_non_execution_result(result)
    assert result.metadata["simulated_discovery"]["surfaces"] == (
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


def test_synthetic_external_consumer_builds_already_normalized_metadata() -> None:
    consumer = _load_consumer_module()
    request = consumer.build_planning_request()

    assert request.normalized_intent["execution_mode"] == "dry_run"
    assert request.normalized_intent["input_origin"] == "synthetic_external_consumer"
    assert "raw_text" not in request.normalized_intent
    assert "prompt" not in request.normalized_intent
    assert request.source_surface["contains_raw_prompt"] is False
    assert request.source_surface["contains_secret"] is False
    assert request.source_surface["contains_unsafe_payload"] is False
