from __future__ import annotations

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


FIXTURE_DIR = pathlib.Path(__file__).resolve().parent / "fixtures" / "sparkbot_arc_request_metadata"
FIXTURE_FILES = (
    FIXTURE_DIR / "sparkbot_normalized_request_fixtures.json",
    FIXTURE_DIR / "arc_normalized_request_fixtures.json",
)
REQUIRED_TOP_LEVEL_FIELDS = {
    "schema_version",
    "request_id",
    "shell",
    "actor",
    "session",
    "normalized_intent",
    "capability_profile",
    "source_surface",
    "context_refs",
}
REQUIRED_INTENT_FIELDS = {
    "action_category",
    "risk_class",
    "execution_mode",
    "input_origin",
}
REQUIRED_SOURCE_SURFACE_FIELDS = {
    "surface",
    "privacy_class",
    "contains_raw_prompt",
    "contains_secret",
    "contains_unsafe_payload",
}
FORBIDDEN_RAW_MARKERS = (
    "api_key",
    "authorization",
    "bearer ",
    "cookie",
    "password",
    "pairing_code",
    "raw_chat",
    "raw_prompt",
    "raw_provider",
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


def _load_fixture_documents() -> list[Mapping[str, Any]]:
    return [json.loads(path.read_text(encoding="utf-8")) for path in FIXTURE_FILES]


def _iter_fixture_cases() -> list[Mapping[str, Any]]:
    cases: list[Mapping[str, Any]] = []
    for document in _load_fixture_documents():
        assert document["schema_version"] == "0.1"
        assert document["fixture_scope"].endswith("_normalized_metadata_only")
        cases.extend(document["fixtures"])
    return cases


def _build_kernel_request(normalized_request: Mapping[str, Any]) -> KernelRequest:
    profile_data = dict(normalized_request["capability_profile"])
    context_refs = normalized_request["context_refs"]
    return KernelRequest(
        request_id=str(normalized_request["request_id"]),
        shell_id=str(normalized_request["shell"]["shell_id"]),
        actor_id=str(normalized_request["actor"]["actor_id"]),
        session_id=str(normalized_request["session"]["session_id"]),
        normalized_intent=dict(normalized_request["normalized_intent"]),
        capability_profile=CapabilityProfile(**profile_data),
        actor_context=dict(normalized_request["actor"]),
        shell_context=dict(normalized_request["shell"]),
        session_context=dict(normalized_request["session"]),
        memory_refs=tuple(context_refs.get("memory_refs", ())),
        source_surface=dict(normalized_request["source_surface"]),
        metadata={
            "schema_version": normalized_request["schema_version"],
            "fixture_only": True,
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


def _assert_required_metadata(normalized_request: Mapping[str, Any]) -> None:
    assert REQUIRED_TOP_LEVEL_FIELDS <= set(normalized_request)
    assert normalized_request["shell"]["shell_id"]
    assert normalized_request["shell"]["shell_type"] in {"sparkbot", "arc"}
    assert normalized_request["actor"]["actor_id"]
    assert normalized_request["actor"]["actor_type"] in {"human", "service", "supervisor"}
    assert normalized_request["session"]["session_id"]
    assert REQUIRED_INTENT_FIELDS <= set(normalized_request["normalized_intent"])
    assert normalized_request["normalized_intent"]["execution_mode"] == "dry_run"
    assert REQUIRED_SOURCE_SURFACE_FIELDS <= set(normalized_request["source_surface"])
    assert normalized_request["source_surface"]["contains_raw_prompt"] is False
    assert normalized_request["source_surface"]["contains_secret"] is False
    assert normalized_request["source_surface"]["contains_unsafe_payload"] is False


def _assert_no_raw_sensitive_payloads(value: Any) -> None:
    if isinstance(value, Mapping):
        for nested_value in value.values():
            _assert_no_raw_sensitive_payloads(nested_value)
        return
    if isinstance(value, list):
        for item in value:
            _assert_no_raw_sensitive_payloads(item)
        return
    if not isinstance(value, str):
        return
    folded = value.lower()
    assert not any(marker in folded for marker in FORBIDDEN_RAW_MARKERS)


def test_sparkbot_arc_fixture_documents_are_synthetic_only() -> None:
    for document in _load_fixture_documents():
        assert document["schema_version"] == "0.1"
        assert document["fixture_scope"].startswith("synthetic_")
        assert document["fixture_scope"].endswith("_normalized_metadata_only")
        _assert_no_raw_sensitive_payloads(document)


def test_sparkbot_arc_fixtures_have_required_contract_metadata() -> None:
    for fixture_case in _iter_fixture_cases():
        _assert_required_metadata(fixture_case["request"])


def test_sparkbot_arc_fixtures_map_to_kernel_request_without_runtime_changes() -> None:
    for fixture_case in _iter_fixture_cases():
        kernel_request = _build_kernel_request(fixture_case["request"])

        assert isinstance(kernel_request, KernelRequest)
        assert kernel_request.metadata["fixture_only"] is True
        assert kernel_request.metadata["synthetic"] is True
        assert kernel_request.normalized_intent["execution_mode"] == "dry_run"
        assert kernel_request.source_surface["contains_raw_prompt"] is False
        assert kernel_request.source_surface["contains_secret"] is False
        assert kernel_request.source_surface["contains_unsafe_payload"] is False


def test_sparkbot_arc_fixtures_evaluate_as_dry_run_results() -> None:
    for fixture_case in _iter_fixture_cases():
        kernel_request = _build_kernel_request(fixture_case["request"])
        adapter = (
            SimulatedDiscoveryAdapter()
            if kernel_request.normalized_intent.get("include_simulated_surfaces") is True
            else None
        )
        result = LimaKernel().evaluate(
            kernel_request,
            simulated_discovery_adapter=adapter,
        )

        assert result.state == fixture_case["expected_state"]
        assert result.guardian_summary.reason_code == fixture_case["expected_reason_code"]
        _assert_non_execution_result(result)


def test_sparkbot_arc_simulated_fixture_returns_synthetic_surface_only() -> None:
    fixture_case = next(
        case
        for case in _iter_fixture_cases()
        if case["fixture_id"] == "sparkbot-simulated-discovery-preview"
    )
    result = LimaKernel().evaluate(
        _build_kernel_request(fixture_case["request"]),
        simulated_discovery_adapter=SimulatedDiscoveryAdapter(),
    )

    simulated_discovery = result.metadata["simulated_discovery"]
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
