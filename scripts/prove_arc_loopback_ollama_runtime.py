from __future__ import annotations

import json
from typing import Any, Mapping

from lima.harness import execute_v1_live_provider_model_call


DECISION_ID = "guardian-decision:proof-v1-1-loopback-ollama"
ENDPOINT = "http://127.0.0.1:11434"
MODEL = "qwen2.5:7b"
executor_calls: list[Mapping[str, Any]] = []
real_network_calls = 0


def in_process_ollama_shaped_executor(
    payload: Mapping[str, Any],
) -> Mapping[str, Any]:
    executor_calls.append(payload)
    return {
        "provider": "ollama",
        "model": MODEL,
        "output_text": "Deterministic loopback Ollama contract proof.",
        "endpoint": ENDPOINT,
        "network_called": True,
        "network_scope": "loopback_only",
        "ollama_called": True,
        "credentials_used": False,
        "external_side_effects": False,
        "duration_ms": 7,
        "status": "completed",
        "error_category": None,
        "error_message": None,
    }


runtime_request = {
    "request_id": "arc-action:proof-v1-1-loopback-ollama",
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
        "actor_id": "operator:proof",
        "shell_id": "arc:proof",
        "task_ref": "task:proof-v1-1-loopback-ollama",
        "summary": "Bounded local preview contract proof.",
    },
    "evidence_refs": ["evidence:arc-guardian:proof-v1-1-loopback-ollama"],
}

result = execute_v1_live_provider_model_call(
    runtime_request,
    in_process_ollama_shaped_executor,
)

assert len(executor_calls) == 1
assert real_network_calls == 0
assert executor_calls[0]["executor_kind"] == "loopback_ollama"
assert executor_calls[0]["guardian_decision_id"] == DECISION_ID
assert result["guardian_decision_id"] == DECISION_ID
assert result["guardian_decision"]["decision_id"] == DECISION_ID
assert result["evidence"]["guardian_decision_id"] == DECISION_ID
assert result["executor_kind"] == "loopback_ollama"
assert result["endpoint"] == ENDPOINT
assert result["network_called"] is True
assert result["network_scope"] == "loopback_only"
assert result["ollama_called"] is True
assert result["credentials_used"] is False
assert result["external_side_effects"] is False
assert result["status"] == "completed"
assert result["output_text"]

print(
    json.dumps(
        {
            "executor_call_count": len(executor_calls),
            "real_network_calls": real_network_calls,
            "runtime_result": result,
        },
        sort_keys=True,
    )
)
