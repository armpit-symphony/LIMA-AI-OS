from __future__ import annotations

import ast
import json
import pathlib
from typing import Any, Mapping

from lima.kernel import (
    CapabilityProfile,
    ExecutionResult,
    KernelRequest,
    LimaKernel,
    SimulatedDiscoveryAdapter,
)


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    pathlib.Path(__file__).resolve().parent
    / "fixtures"
    / "sparkbot_boundary_handoff"
    / "handoff_fixture.json"
)
THIS_TEST_PATH = pathlib.Path(__file__)
REQUIRED_EVIDENCE_FIELDS = {
    "branch_name",
    "lima_package_or_import_method",
    "lima_commit_or_version",
    "normalized_request_fixture",
    "dry_run_execution_result_sample",
    "non_execution_invariant_checklist",
    "proof_no_raw_chat_sent_to_lima",
    "proof_no_production_route_wired",
    "proof_no_model_tool_connector_storage_action",
    "proof_no_background_worker_or_scheduler_triggered",
    "proof_no_external_send",
    "proof_no_device_robot_drone_physical_world_action",
}
FORBIDDEN_IMPORT_ROOTS = {
    "arc",
    "arcbot",
    "bluetooth",
    "bleak",
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
FORBIDDEN_VALUE_MARKERS = (
    "api_key",
    "authorization",
    "bearer ",
    "cookie",
    "password",
    "pairing_code",
    "private_ssid",
    "raw scan",
    "secret",
    "token",
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


def _load_fixture() -> Mapping[str, Any]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _iter_cases() -> list[Mapping[str, Any]]:
    fixture = _load_fixture()
    assert fixture["schema_version"] == "0.1"
    assert fixture["fixture_scope"] == "synthetic_sparkbot_boundary_handoff_fixture_only"
    return list(fixture["fixtures"])


def _build_kernel_request(normalized_request: Mapping[str, Any]) -> KernelRequest:
    context_refs = normalized_request["context_refs"]
    return KernelRequest(
        request_id=normalized_request["request_id"],
        shell_id=normalized_request["shell"]["shell_id"],
        actor_id=normalized_request["actor"]["actor_id"],
        session_id=normalized_request["session"]["session_id"],
        normalized_intent=dict(normalized_request["normalized_intent"]),
        capability_profile=CapabilityProfile(**dict(normalized_request["capability_profile"])),
        actor_context=dict(normalized_request["actor"]),
        shell_context=dict(normalized_request["shell"]),
        session_context=dict(normalized_request["session"]),
        memory_refs=tuple(context_refs.get("memory_refs", ())),
        source_surface=dict(normalized_request["source_surface"]),
        metadata={
            "schema_version": normalized_request["schema_version"],
            "sparkbot_boundary_handoff_fixture": True,
            "synthetic": True,
            "task_refs": tuple(context_refs.get("task_refs", ())),
            "document_refs": tuple(context_refs.get("document_refs", ())),
            "connector_refs": tuple(context_refs.get("connector_refs", ())),
        },
    )


def _assert_non_execution_result(result: ExecutionResult) -> None:
    assert result.dry_run is True
    for field_name in NON_EXECUTION_FALSE_FIELDS:
        assert getattr(result, field_name) is False


def _assert_no_sensitive_values(value: Any) -> None:
    if isinstance(value, Mapping):
        for nested_value in value.values():
            _assert_no_sensitive_values(nested_value)
        return
    if isinstance(value, list):
        for item in value:
            _assert_no_sensitive_values(item)
        return
    if not isinstance(value, str):
        return
    folded = value.lower()
    assert not any(marker in folded for marker in FORBIDDEN_VALUE_MARKERS)


def _import_roots(path: pathlib.Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        if isinstance(node, ast.ImportFrom) and node.module:
            roots.add(node.module.split(".")[0])
    return roots


def test_sparkbot_handoff_fixture_declares_no_repo_or_runtime_wiring() -> None:
    fixture = _load_fixture()

    assert fixture["public_sparkbot_repo_touched"] is False
    assert fixture["arc_bot_repo_touched"] is False
    assert fixture["lima_runtime_behavior_changed"] is False
    assert fixture["sparkbot_integration_implemented"] is False
    assert fixture["production_readiness_claimed"] is False


def test_sparkbot_handoff_checklist_shape_is_archive_ready() -> None:
    fixture = _load_fixture()

    assert set(fixture["required_sparkbot_side_evidence"]) == REQUIRED_EVIDENCE_FIELDS
    proof = fixture["allowed_future_sparkbot_proof"]
    assert proof["sparkbot_owned_branch"] == "sparkbot-lima-dry-run-boundary-proof"
    assert proof["normalized_metadata_only"] is True
    assert proof["dry_run_only"] is True
    assert proof["must_not_wire_production_route"] is True
    assert proof["must_not_call_model"] is True
    assert proof["must_not_execute_tool"] is True
    assert proof["must_not_access_connector"] is True
    assert proof["must_not_persist"] is True
    assert proof["must_not_send_external_message"] is True
    assert proof["must_not_touch_device_or_physical_world"] is True


def test_sparkbot_handoff_fixture_values_are_redacted_and_synthetic() -> None:
    fixture = _load_fixture()

    _assert_no_sensitive_values(fixture)
    assert all(fixture["forbidden_inputs_to_lima"].values())


def test_sparkbot_handoff_fixture_maps_to_kernel_request() -> None:
    for case in _iter_cases():
        request = _build_kernel_request(case["request"])

        assert isinstance(request, KernelRequest)
        assert request.shell_context["shell_type"] == "sparkbot"
        assert request.normalized_intent["execution_mode"] == "dry_run"
        assert request.metadata["sparkbot_boundary_handoff_fixture"] is True
        assert request.source_surface["contains_raw_prompt"] is False
        assert request.source_surface["contains_secret"] is False
        assert request.source_surface["contains_unsafe_payload"] is False


def test_sparkbot_handoff_fixtures_evaluate_as_dry_run_only() -> None:
    for case in _iter_cases():
        request = _build_kernel_request(case["request"])
        adapter = SimulatedDiscoveryAdapter() if case["requires_simulated_adapter"] else None
        result = LimaKernel().evaluate(request, simulated_discovery_adapter=adapter)

        assert case["expected_kernel_called"] is True
        assert result.state == case["expected_state"]
        assert result.guardian_summary.reason_code == case["expected_reason_code"]
        _assert_non_execution_result(result)


def test_sparkbot_handoff_simulated_discovery_surface_is_synthetic_only() -> None:
    case = next(
        fixture_case
        for fixture_case in _iter_cases()
        if fixture_case["fixture_id"] == "sparkbot-handoff-simulated-discovery-preview"
    )
    result = LimaKernel().evaluate(
        _build_kernel_request(case["request"]),
        simulated_discovery_adapter=SimulatedDiscoveryAdapter(),
    )

    surface = result.metadata["simulated_discovery"]["surfaces"][0]
    assert surface["surface_id"] == case["expected_synthetic_surface_id"]
    assert surface["synthetic"] is True
    assert surface["inert"] is True
    assert surface["simulated"] is True
    assert surface["connectable"] is False
    assert surface["controllable"] is False
    assert surface["physical_world"] is False


def test_sparkbot_handoff_test_file_does_not_import_sparkbot_or_live_surfaces() -> None:
    import_roots = _import_roots(THIS_TEST_PATH)

    assert not (import_roots & FORBIDDEN_IMPORT_ROOTS)
