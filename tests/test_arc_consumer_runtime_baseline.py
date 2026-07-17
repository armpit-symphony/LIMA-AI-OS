from __future__ import annotations

from pathlib import Path
import tomllib
from typing import Any

import pytest

from lima.harness import (
    V1LiveProviderModelCallExecutionError,
    execute_v1_live_provider_model_call,
)


DECISION_ID = 'guardian-decision:test-v0-9'


def test_arc_baseline_package_has_no_provider_dependency() -> None:
    pyproject = tomllib.loads(
        (Path(__file__).resolve().parents[1] / 'pyproject.toml').read_text(
            encoding='utf-8'
        )
    )

    assert pyproject['project']['dependencies'] == []


def _request(**overrides: Any) -> dict[str, Any]:
    request = {
        'request_id': 'arc-action:test-v0-9',
        'runtime_consumer': 'arc_bot_shell',
        'requested_action': 'arc.local_model_preview',
        'guardian_decision': {
            'decision_id': DECISION_ID,
            'status': 'allow',
            'allowed': True,
            'requires_approval': False,
        },
        'executor_ref': 'in_process_fake_executor',
        'normalized_request': {
            'actor_id': 'operator:test',
            'shell_id': 'arc:test',
            'task_ref': 'task:test-v0-9',
        },
        'evidence_refs': ['evidence:arc-guardian:test-v0-9'],
    }
    request.update(overrides)
    return request


def _fake_result(**overrides: Any) -> dict[str, Any]:
    result = {
        'provider': 'fake_local_model',
        'model': 'fake-preview-model',
        'output_text': 'Deterministic LIMA runtime preview.',
        'network_called': False,
        'credentials_used': False,
        'ollama_called': False,
    }
    result.update(overrides)
    return result


def test_installed_public_import_fake_executor_preserves_guardian_lineage() -> None:
    calls: list[dict[str, Any]] = []

    def fake_executor(payload: dict[str, Any]) -> dict[str, Any]:
        calls.append(payload)
        return _fake_result()

    result = execute_v1_live_provider_model_call(_request(), fake_executor)

    assert len(calls) == 1
    assert calls[0]['guardian_decision_id'] == DECISION_ID
    assert calls[0]['guardian_decision']['decision_id'] == DECISION_ID
    assert result['guardian_decision_id'] == DECISION_ID
    assert result['guardian_decision']['decision_id'] == DECISION_ID
    assert result['evidence']['guardian_decision_id'] == DECISION_ID
    assert result['executor_called'] is True
    assert result['network_called'] is False
    assert result['credentials_used'] is False
    assert result['ollama_called'] is False


@pytest.mark.parametrize(
    'guardian_decision',
    [
        None,
        {},
        {
            'decision_id': '',
            'status': 'allow',
            'allowed': True,
            'requires_approval': False,
        },
        {
            'decision_id': DECISION_ID,
            'status': 'deny',
            'allowed': False,
            'requires_approval': False,
        },
        {
            'decision_id': DECISION_ID,
            'status': 'approval_required',
            'allowed': False,
            'requires_approval': True,
        },
    ],
)
def test_invalid_guardian_decision_fails_closed_before_executor(
    guardian_decision: Any,
) -> None:
    calls = 0

    def fake_executor(payload: dict[str, Any]) -> dict[str, Any]:
        nonlocal calls
        calls += 1
        return _fake_result()

    request = _request()
    if guardian_decision is None:
        request.pop('guardian_decision')
    else:
        request['guardian_decision'] = guardian_decision

    with pytest.raises(V1LiveProviderModelCallExecutionError):
        execute_v1_live_provider_model_call(request, fake_executor)

    assert calls == 0


def test_malformed_runtime_request_fails_closed() -> None:
    with pytest.raises(V1LiveProviderModelCallExecutionError, match='normalized_request'):
        execute_v1_live_provider_model_call(
            _request(normalized_request=[]),
            lambda payload: _fake_result(),
        )


def test_unsupported_executor_fails_closed_before_call() -> None:
    calls = 0

    def unsupported_executor(payload: dict[str, Any]) -> dict[str, Any]:
        nonlocal calls
        calls += 1
        return _fake_result()

    with pytest.raises(V1LiveProviderModelCallExecutionError, match='unsupported executor'):
        execute_v1_live_provider_model_call(
            _request(executor_ref='ollama'),
            unsupported_executor,
        )

    assert calls == 0


def test_executor_exception_is_controlled() -> None:
    def failing_executor(payload: dict[str, Any]) -> dict[str, Any]:
        raise RuntimeError('fake failure')

    with pytest.raises(V1LiveProviderModelCallExecutionError, match='executor failed'):
        execute_v1_live_provider_model_call(_request(), failing_executor)


@pytest.mark.parametrize(
    'executor_result',
    [
        {},
        {'provider': 'fake_local_model'},
        _fake_result(network_called=True),
        _fake_result(credentials_used=True),
        _fake_result(ollama_called=True),
    ],
)
def test_malformed_or_unsafe_executor_result_is_controlled(
    executor_result: dict[str, Any],
) -> None:
    with pytest.raises(V1LiveProviderModelCallExecutionError):
        execute_v1_live_provider_model_call(
            _request(),
            lambda payload: executor_result,
        )
