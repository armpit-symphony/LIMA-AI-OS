from __future__ import annotations

import json
from typing import Any, Mapping

from lima.harness import execute_v1_live_provider_model_call


DECISION_ID = 'guardian-decision:test-v0-9'
executor_calls: list[Mapping[str, Any]] = []


def fake_executor(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    executor_calls.append(payload)
    return {
        'provider': 'fake_local_model',
        'model': 'fake-preview-model',
        'output_text': 'Deterministic LIMA runtime preview.',
        'network_called': False,
        'credentials_used': False,
        'ollama_called': False,
    }


runtime_request = {
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
    'executor_kind': 'fake',
    'normalized_request': {
        'actor_id': 'operator:test',
        'shell_id': 'arc:test',
        'task_ref': 'task:test-v0-9',
    },
    'evidence_refs': ['evidence:arc-guardian:test-v0-9'],
}

result = execute_v1_live_provider_model_call(runtime_request, fake_executor)

assert len(executor_calls) == 1
assert executor_calls[0]['guardian_decision_id'] == DECISION_ID
assert result['guardian_decision_id'] == DECISION_ID
assert result['evidence']['guardian_decision_id'] == DECISION_ID
assert result['network_called'] is False
assert result['credentials_used'] is False
assert result['ollama_called'] is False

print(json.dumps(result, sort_keys=True))
