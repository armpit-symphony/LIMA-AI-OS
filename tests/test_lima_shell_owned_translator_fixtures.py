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


FIXTURE_PATH = (
    pathlib.Path(__file__).resolve().parent
    / "fixtures"
    / "shell_owned_translator"
    / "shell_translator_fixtures.json"
)
ALLOWED_TRANSLATION_STATES = {"translated", "blocked", "needs_clarification"}
REQUIRED_REDACTION_FLAGS = {
    "raw_text_forwarded",
    "attachments_forwarded",
    "connector_payload_forwarded",
    "credential_material_forwarded",
}
FORBIDDEN_VALUE_MARKERS = (
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


def _load_document() -> Mapping[str, Any]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _iter_cases() -> list[Mapping[str, Any]]:
    document = _load_document()
    assert document["schema_version"] == "0.1"
    assert document["fixture_scope"] == "synthetic_shell_owned_translator_fixtures_only"
    return list(document["fixtures"])


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
            "shell_owned_translator_fixture": True,
            "synthetic": True,
            "task_refs": tuple(context_refs.get("task_refs", ())),
            "document_refs": tuple(context_refs.get("document_refs", ())),
            "connector_refs": tuple(context_refs.get("connector_refs", ())),
        },
    )


def _assert_no_raw_sensitive_values(value: Any) -> None:
    if isinstance(value, Mapping):
        for nested_value in value.values():
            _assert_no_raw_sensitive_values(nested_value)
        return
    if isinstance(value, list):
        for item in value:
            _assert_no_raw_sensitive_values(item)
        return
    if not isinstance(value, str):
        return
    folded = value.lower()
    assert not any(marker in folded for marker in FORBIDDEN_VALUE_MARKERS)


def _assert_redaction_summary_safe(output: Mapping[str, Any]) -> None:
    summary = output["redaction_summary"]
    assert REQUIRED_REDACTION_FLAGS <= set(summary)
    for flag in REQUIRED_REDACTION_FLAGS:
        assert summary[flag] is False


def _assert_non_execution_result(result: ExecutionResult) -> None:
    assert result.dry_run is True
    for field_name in NON_EXECUTION_FALSE_FIELDS:
        assert getattr(result, field_name) is False


def test_shell_owned_translator_fixtures_are_synthetic_and_redacted() -> None:
    document = _load_document()
    assert document["schema_version"] == "0.1"
    assert document["fixture_scope"].startswith("synthetic_")
    _assert_no_raw_sensitive_values(document)


def test_translation_states_and_redaction_flags_are_safe() -> None:
    for case in _iter_cases():
        output = case["translator_output"]
        assert output["translation_state"] in ALLOWED_TRANSLATION_STATES
        _assert_redaction_summary_safe(output)
        assert case["translator_input"]["raw_input_state"]["raw_text_forwarded"] is False
        assert case["translator_input"]["raw_input_state"]["credential_material_present"] is False
        assert case["translator_input"]["raw_input_state"]["unsafe_payload_present"] is False


def test_only_translated_outputs_are_mapped_to_kernel_request() -> None:
    for case in _iter_cases():
        output = case["translator_output"]
        if output["translation_state"] != "translated":
            assert output["normalized_request"] is None
            assert case["expected_kernel_called"] is False
            continue

        kernel_request = _build_kernel_request(output["normalized_request"])
        assert isinstance(kernel_request, KernelRequest)
        assert kernel_request.metadata["shell_owned_translator_fixture"] is True
        assert kernel_request.normalized_intent["execution_mode"] == "dry_run"
        assert kernel_request.source_surface["contains_raw_prompt"] is False
        assert kernel_request.source_surface["contains_secret"] is False
        assert kernel_request.source_surface["contains_unsafe_payload"] is False


def test_translated_outputs_evaluate_as_dry_run_kernel_results() -> None:
    for case in _iter_cases():
        output = case["translator_output"]
        if output["translation_state"] != "translated":
            continue

        request = _build_kernel_request(output["normalized_request"])
        adapter = (
            SimulatedDiscoveryAdapter()
            if request.normalized_intent.get("include_simulated_surfaces") is True
            else None
        )
        result = LimaKernel().evaluate(request, simulated_discovery_adapter=adapter)

        assert case["expected_kernel_called"] is True
        assert result.state == case["expected_kernel_state"]
        assert result.guardian_summary.reason_code == case["expected_reason_code"]
        _assert_non_execution_result(result)


def test_blocked_and_clarification_outputs_do_not_call_kernel() -> None:
    non_translated_cases = [
        case for case in _iter_cases() if case["translator_output"]["translation_state"] != "translated"
    ]
    assert non_translated_cases
    for case in non_translated_cases:
        output = case["translator_output"]
        assert output["normalized_request"] is None
        assert case["expected_kernel_called"] is False
        assert case["expected_kernel_state"] is None
        assert case["expected_reason_code"] is None


def test_translated_simulated_discovery_output_returns_synthetic_surface_only() -> None:
    case = next(
        fixture_case
        for fixture_case in _iter_cases()
        if fixture_case["fixture_id"] == "arc-translated-simulated-discovery"
    )
    request = _build_kernel_request(case["translator_output"]["normalized_request"])
    result = LimaKernel().evaluate(request, simulated_discovery_adapter=SimulatedDiscoveryAdapter())

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
