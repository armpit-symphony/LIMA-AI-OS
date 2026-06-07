from __future__ import annotations

import ast
import importlib
import importlib.util
import pathlib
import tomllib

import lima
from lima.kernel import ExecutionResult, LimaKernel


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
EXAMPLE_PATH = REPO_ROOT / "examples" / "minimal_shell" / "example_shell.py"
PYPROJECT_PATH = REPO_ROOT / "pyproject.toml"
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
    "webbrowser",
}
FORBIDDEN_SOURCE_MARKERS = {
    "api_key=",
    "authorization=",
    "bleak",
    "credential_ref",
    "device_control(",
    "mqtt",
    "openai",
    "pairing_code=",
    "password=",
    "physical_world_executed = true",
    "robotics_actuation(",
    "secret=",
    "socket.",
    "subprocess.",
    "threading.",
    "token=",
    "usb.",
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


def _load_example_module():
    spec = importlib.util.spec_from_file_location("lima_minimal_example_shell", EXAMPLE_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _assert_non_execution_result(result: ExecutionResult) -> None:
    assert result.dry_run is True
    for field_name in NON_EXECUTION_FALSE_FIELDS:
        assert getattr(result, field_name) is False


def test_import_lima_and_kernel_public_api() -> None:
    assert lima is not None
    assert LimaKernel is not None


def test_example_shell_module_imports_from_repo_root() -> None:
    module = importlib.import_module("examples.minimal_shell.example_shell")
    assert module.run_planning_preview()["state"] == "proposed"


def test_package_metadata_declares_lima_runtime() -> None:
    pyproject = tomllib.loads(PYPROJECT_PATH.read_text(encoding="utf-8"))
    assert pyproject["project"]["name"] == "lima-runtime"
    assert pyproject["project"]["version"] == "0.0.1"
    assert pyproject["tool"]["setuptools"]["packages"]["find"]["include"] == ["lima*"]


def test_example_shell_imports_only_lima_kernel() -> None:
    source = EXAMPLE_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)
    import_roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            import_roots.update(alias.name.split(".")[0] for alias in node.names)
        if isinstance(node, ast.ImportFrom) and node.module:
            import_roots.add(node.module.split(".")[0])

    assert import_roots <= {"__future__", "lima"}
    assert not (import_roots & FORBIDDEN_IMPORT_ROOTS)


def test_example_shell_source_avoids_forbidden_runtime_markers() -> None:
    source = EXAMPLE_PATH.read_text(encoding="utf-8").lower()
    assert not any(marker in source for marker in FORBIDDEN_SOURCE_MARKERS)


def test_example_shell_builds_already_normalized_planning_request() -> None:
    example_shell = _load_example_module()
    request = example_shell.build_planning_request()

    assert request.normalized_intent["action_category"] == "planning"
    assert request.normalized_intent["risk_class"] == "low"
    assert "raw_text" not in request.normalized_intent
    assert "prompt" not in request.normalized_intent


def test_example_shell_planning_preview_returns_dry_run_result() -> None:
    example_shell = _load_example_module()
    request = example_shell.build_planning_request()
    result = LimaKernel().evaluate(request)

    assert result.state == "proposed"
    assert result.guardian_summary.reason_code == "text_preview_or_planning_proposed"
    _assert_non_execution_result(result)


def test_example_shell_simulated_path_returns_synthetic_surfaces_only() -> None:
    example_shell = _load_example_module()
    summary = example_shell.run_simulated_discovery_preview()

    assert summary["state"] == "proposed"
    simulated_discovery = summary["simulated_discovery"]
    assert simulated_discovery["state"] == "proposed"
    assert simulated_discovery["adapter_type"] == "simulated_discovery_adapter"
    assert simulated_discovery["event_refs"]
    assert simulated_discovery["surfaces"] == (
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


def test_example_shell_simulated_result_preserves_non_execution_invariants() -> None:
    example_shell = _load_example_module()
    request = example_shell.build_simulated_discovery_request()
    result = LimaKernel().evaluate(
        request,
        simulated_discovery_adapter=example_shell.SimulatedDiscoveryAdapter(),
    )

    _assert_non_execution_result(result)
    assert result.metadata["simulated_adapter_used"] is True
    assert result.metadata["simulated_discovery"]["surfaces"][0]["synthetic"] is True
