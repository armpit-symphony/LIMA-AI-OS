from __future__ import annotations

import inspect
from typing import Any, Mapping

import pytest

from lima.harness import (
    V1LiveProviderModelCallExecutionError,
    execute_v1_live_provider_model_call,
)


DECISION_ID = "guardian-decision:test-v1-1-loopback-ollama"
ENDPOINT = "http://127.0.0.1:11434"
MODEL = "qwen2.5:7b"


def _request(**overrides: Any) -> dict[str, Any]:
    request = {
        "request_id": "arc-action:test-v1-1-loopback-ollama",
        "runtime_consumer": "arc_bot_shell",
        "requested_action": "arc.local_model_preview",
        "guardian_decision": {
            "decision_id": DECISION_ID,
            "status": "allow",
            "allowed": True,
            "requires_approval": False,
        },
        "executor_ref": "arc_loopback_ollama_executor",
        "executor_kind": "loopback_ollama",
        "network_scope": "loopback_only",
        "credentials_used": False,
        "external_side_effects": False,
        "endpoint": ENDPOINT,
        "model": MODEL,
        "normalized_request": {
            "actor_id": "operator:test",
            "shell_id": "arc:test",
            "task_ref": "task:test-v1-1-loopback-ollama",
            "summary": "Bounded local preview.",
        },
        "evidence_refs": ["evidence:arc-guardian:test-v1-1-loopback-ollama"],
    }
    request.update(overrides)
    return request


def _success_result(**overrides: Any) -> dict[str, Any]:
    result = {
        "provider": "ollama",
        "model": MODEL,
        "output_text": "Deterministic local Ollama-shaped preview.",
        "endpoint": ENDPOINT,
        "network_called": True,
        "network_scope": "loopback_only",
        "ollama_called": True,
        "credentials_used": False,
        "external_side_effects": False,
        "duration_ms": 123,
        "status": "completed",
        "error_category": None,
        "error_message": None,
    }
    result.update(overrides)
    return result


def _unavailable_result(
    error_category: str = "service_unavailable",
    error_message: str = "Ollama service unavailable",
) -> dict[str, Any]:
    return {
        "provider": "ollama",
        "model": MODEL,
        "endpoint": ENDPOINT,
        "network_called": True,
        "network_scope": "loopback_only",
        "ollama_called": True,
        "credentials_used": False,
        "external_side_effects": False,
        "duration_ms": 25,
        "status": "unavailable",
        "error_category": error_category,
        "error_message": error_message,
    }


def test_valid_loopback_ollama_request_invokes_once_and_preserves_lineage() -> None:
    calls: list[Mapping[str, Any]] = []

    def executor(payload: Mapping[str, Any]) -> Mapping[str, Any]:
        calls.append(payload)
        return _success_result()

    result = execute_v1_live_provider_model_call(_request(), executor)

    assert len(calls) == 1
    assert calls[0]["executor_kind"] == "loopback_ollama"
    assert calls[0]["guardian_decision_id"] == DECISION_ID
    assert calls[0]["guardian_decision"]["decision_id"] == DECISION_ID
    assert calls[0]["endpoint"] == ENDPOINT
    assert calls[0]["model"] == MODEL
    assert calls[0]["network_scope"] == "loopback_only"
    assert calls[0]["credentials_used"] is False
    assert calls[0]["external_side_effects"] is False
    assert result["guardian_decision_id"] == DECISION_ID
    assert result["guardian_decision"]["decision_id"] == DECISION_ID
    assert result["evidence"]["guardian_decision_id"] == DECISION_ID
    assert result["executor_kind"] == "loopback_ollama"
    assert result["provider"] == "ollama"
    assert result["model"] == MODEL
    assert result["endpoint"] == ENDPOINT
    assert result["network_called"] is True
    assert result["network_scope"] == "loopback_only"
    assert result["ollama_called"] is True
    assert result["credentials_used"] is False
    assert result["external_side_effects"] is False
    assert result["duration_ms"] == 123
    assert result["status"] == "completed"
    assert result["output_text"]
    assert result["error_category"] is None
    assert result["error_message"] is None


@pytest.mark.parametrize(
    ("configured", "normalized"),
    [
        ("http://127.0.0.1:11434", "http://127.0.0.1:11434"),
        ("http://localhost:11434", "http://localhost:11434"),
        ("http://localhost:11434/", "http://localhost:11434"),
    ],
)
def test_approved_loopback_endpoints_are_normalized(
    configured: str,
    normalized: str,
) -> None:
    result = execute_v1_live_provider_model_call(
        _request(endpoint=configured),
        lambda payload: _success_result(endpoint=normalized),
    )

    assert result["endpoint"] == normalized


@pytest.mark.parametrize(
    "endpoint",
    [
        "http://0.0.0.0:11434",
        "http://192.168.1.20:11434",
        "http://10.0.0.20:11434",
        "http://8.8.8.8:11434",
        "http://ollama.example.com:11434",
        "http://user:password@127.0.0.1:11434",
        "http://127.0.0.1:11434/api/generate",
        "http://127.0.0.1:11434?model=qwen",
        "http://127.0.0.1:11434#fragment",
        "https://127.0.0.1:11434",
        "http://127.0.0.1",
        "http://127.0.0.1:not-a-port",
        "",
    ],
)
def test_non_base_or_non_loopback_endpoint_rejected_before_executor(
    endpoint: str,
) -> None:
    calls = 0

    def executor(payload: Mapping[str, Any]) -> Mapping[str, Any]:
        nonlocal calls
        calls += 1
        return _success_result()

    with pytest.raises(V1LiveProviderModelCallExecutionError):
        execute_v1_live_provider_model_call(
            _request(endpoint=endpoint),
            executor,
        )

    assert calls == 0


@pytest.mark.parametrize(
    "guardian_decision",
    [
        None,
        {},
        {
            "decision_id": "",
            "status": "allow",
            "allowed": True,
            "requires_approval": False,
        },
        {
            "decision_id": DECISION_ID,
            "status": "deny",
            "allowed": False,
            "requires_approval": False,
        },
        {
            "decision_id": DECISION_ID,
            "status": "approval_required",
            "allowed": False,
            "requires_approval": True,
        },
    ],
)
def test_invalid_guardian_decision_rejected_before_executor(
    guardian_decision: Any,
) -> None:
    calls = 0

    def executor(payload: Mapping[str, Any]) -> Mapping[str, Any]:
        nonlocal calls
        calls += 1
        return _success_result()

    request = _request()
    if guardian_decision is None:
        request.pop("guardian_decision")
    else:
        request["guardian_decision"] = guardian_decision

    with pytest.raises(V1LiveProviderModelCallExecutionError):
        execute_v1_live_provider_model_call(request, executor)

    assert calls == 0


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("requested_action", "arc.preview_operator_response"),
        ("executor_kind", None),
        ("executor_kind", "network"),
        ("network_scope", "lan"),
        ("credentials_used", True),
        ("credentials_used", None),
        ("external_side_effects", True),
        ("external_side_effects", None),
        ("endpoint", None),
        ("model", ""),
        ("model", None),
    ],
)
def test_invalid_loopback_precondition_rejected_before_executor(
    field_name: str,
    value: Any,
) -> None:
    calls = 0

    def executor(payload: Mapping[str, Any]) -> Mapping[str, Any]:
        nonlocal calls
        calls += 1
        return _success_result()

    request = _request()
    if value is None:
        request.pop(field_name)
    else:
        request[field_name] = value

    with pytest.raises(V1LiveProviderModelCallExecutionError):
        execute_v1_live_provider_model_call(request, executor)

    assert calls == 0


@pytest.mark.parametrize(
    "unsafe_result",
    [
        {},
        {"provider": "ollama"},
        _success_result(provider="openai"),
        _success_result(model="another-model"),
        _success_result(endpoint="http://localhost:11434"),
        _success_result(endpoint="http://192.168.1.20:11434"),
        _success_result(network_called=False),
        _success_result(network_scope="lan"),
        _success_result(ollama_called=False),
        _success_result(credentials_used=True),
        _success_result(external_side_effects=True),
        _success_result(duration_ms=-1),
        _success_result(output_text=""),
        _success_result(status="failed"),
        _success_result(error_category="timeout"),
        _success_result(error_message="unexpected error"),
    ],
)
def test_malformed_or_unsafe_loopback_result_is_rejected(
    unsafe_result: dict[str, Any],
) -> None:
    calls = 0

    def executor(payload: Mapping[str, Any]) -> Mapping[str, Any]:
        nonlocal calls
        calls += 1
        return unsafe_result

    with pytest.raises(V1LiveProviderModelCallExecutionError):
        execute_v1_live_provider_model_call(_request(), executor)

    assert calls == 1


@pytest.mark.parametrize(
    ("category", "message"),
    [
        ("service_unavailable", "Ollama service unavailable"),
        ("model_unavailable", "Configured Ollama model unavailable"),
        ("timeout", "Ollama request timed out"),
        ("malformed_response", "Ollama response was malformed"),
        ("executor_error", "Ollama executor failed safely"),
    ],
)
def test_controlled_unavailable_result_is_preserved(
    category: str,
    message: str,
) -> None:
    result = execute_v1_live_provider_model_call(
        _request(),
        lambda payload: _unavailable_result(category, message),
    )

    assert result["status"] == "unavailable"
    assert result["output_text"] == ""
    assert result["error_category"] == category
    assert result["error_message"] == message
    assert result["network_called"] is True
    assert result["network_scope"] == "loopback_only"
    assert result["ollama_called"] is True
    assert result["credentials_used"] is False
    assert result["external_side_effects"] is False
    assert result["evidence"]["error_category"] == category


@pytest.mark.parametrize(
    "unsafe_failure",
    [
        _unavailable_result("unknown", "Unknown failure"),
        _unavailable_result("timeout", "Traceback:\nraw details"),
        {**_unavailable_result(), "output_text": "partial output"},
        {**_unavailable_result(), "network_called": False},
        {**_unavailable_result(), "ollama_called": False},
    ],
)
def test_unsafe_controlled_failure_is_rejected(
    unsafe_failure: dict[str, Any],
) -> None:
    with pytest.raises(V1LiveProviderModelCallExecutionError):
        execute_v1_live_provider_model_call(
            _request(),
            lambda payload: unsafe_failure,
        )


def test_executor_exception_is_controlled_without_raw_trace() -> None:
    def executor(payload: Mapping[str, Any]) -> Mapping[str, Any]:
        raise RuntimeError("raw-secret-value-must-not-escape")

    with pytest.raises(
        V1LiveProviderModelCallExecutionError,
        match="provider executor failed",
    ) as exc_info:
        execute_v1_live_provider_model_call(_request(), executor)

    assert exc_info.value.__cause__ is None
    assert "raw-secret" not in str(exc_info.value)


def test_explicit_fake_kind_remains_compatible() -> None:
    result = execute_v1_live_provider_model_call(
        {
            "request_id": "arc-action:explicit-fake",
            "runtime_consumer": "arc_bot_shell",
            "requested_action": "arc.local_model_preview",
            "guardian_decision": {
                "decision_id": DECISION_ID,
                "status": "allow",
                "allowed": True,
                "requires_approval": False,
            },
            "executor_ref": "in_process_fake_executor",
            "executor_kind": "fake",
            "normalized_request": {"summary": "bounded fake preview"},
        },
        lambda payload: {
            "provider": "fake_local_model",
            "model": "fake-preview-model",
            "output_text": "Deterministic preview.",
            "network_called": False,
            "credentials_used": False,
            "ollama_called": False,
        },
    )

    assert result["executor_kind"] == "fake"
    assert result["network_called"] is False
    assert result["ollama_called"] is False


def test_fake_executor_kind_is_not_inferred_from_reference_substring() -> None:
    calls = 0
    request = _request(executor_ref="not_really_fake_executor")
    request.pop("executor_kind")

    def executor(payload: Mapping[str, Any]) -> Mapping[str, Any]:
        nonlocal calls
        calls += 1
        return _success_result()

    with pytest.raises(
        V1LiveProviderModelCallExecutionError,
        match="executor_kind is required",
    ):
        execute_v1_live_provider_model_call(request, executor)

    assert calls == 0


def test_runtime_module_has_no_arc_or_guardian_suite_imports() -> None:
    module = inspect.getmodule(execute_v1_live_provider_model_call)
    assert module is not None
    source = inspect.getsource(module)

    assert "from arc_bot_shell" not in source
    assert "import arc_bot_shell" not in source
    assert "LIMA-Guardian-Suite" not in source
    assert "from urllib.request" not in source
    assert "import requests" not in source
