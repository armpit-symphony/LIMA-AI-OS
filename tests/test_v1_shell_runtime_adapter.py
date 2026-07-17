"""Runtime tests for the V1 shell consumer adapter."""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from lima.adapters import (
    V1ShellRuntimeAdapterError,
    V1ShellRuntimeInput,
    build_v1_shell_runtime_candidate,
    run_v1_shell_governed_preflight,
)
from lima.contracts.guardian import GuardianDecisionStatus
from lima.persistence import V1LocalAuditStore


def _shell_input(**overrides: object) -> V1ShellRuntimeInput:
    data = {
        "input_id": "sparkbot-input-001",
        "consumer": "sparkbot",
        "actor_id": "user-123",
        "shell_id": "sparkbot-shell",
        "tenant_ref": "tenant:local",
        "normalized_request": "summarize workspace status",
        "requested_action": "summarize status",
        "action_category": "informational",
        "source_channel": "room:ops",
        "intent_id": "intent:sparkbot:status",
        "target_ref": "room:ops",
        "session_ref": "session:abc",
        "evidence_refs": ("evidence:sparkbot:status",),
        "content_refs": ("content-ref:status-summary",),
        "metadata": {"surface": "chat", "normalized_by": "sparkbot"},
    }
    data.update(overrides)
    return V1ShellRuntimeInput(**data)  # type: ignore[arg-type]


def test_shell_adapter_builds_candidate_for_lima_governed_preflight() -> None:
    candidate = build_v1_shell_runtime_candidate(_shell_input())

    assert candidate["source"] == "sparkbot"
    assert candidate["source_channel"] == "room:ops"
    assert candidate["action_category"] == "informational"
    assert candidate["risk_tier"] == "low"
    assert candidate["approval_state"] == "proposed"
    assert candidate["execution_allowed"] is False
    assert candidate["side_effects_allowed"] is False
    assert candidate["approved"] is False
    assert candidate["provenance"]["actor_id"] == "user-123"
    assert candidate["provenance"]["shell_id"] == "sparkbot-shell"
    assert candidate["metadata"]["guardian_preflight_required"] is True


def test_shell_adapter_runs_sparkbot_input_through_lima_governed_preflight() -> None:
    with TemporaryDirectory(prefix="lima-shell-preflight-") as temp_dir:
        audit_store = V1LocalAuditStore(Path(temp_dir) / "audit-store")
        result = run_v1_shell_governed_preflight(
            _shell_input(),
            audit_store=audit_store,
            occurred_at="2026-06-30T13:00:00Z",
            event_id="event:shell-preflight:001",
        )

        assert result.preflight.decision.status is GuardianDecisionStatus.APPROVED
        assert result.response["record_type"] == "v1_shell_governed_runtime_response"
        assert result.response["consumer"] == "sparkbot"
        assert result.response["decision_status"] == "approved"
        assert result.response["audit_store_appended"] is True
        assert result.response["execution_allowed"] is False
        assert result.response["tool_executed"] is False
        assert result.response["metadata"]["operator_to_shell_to_lima_step_completed"] is True
        assert audit_store.get_by_event_id(
            "event:shell-preflight:001",
            tenant_ref="tenant:local",
            shell_id="sparkbot-shell",
        ) == result.preflight.audit_event_record


def test_shell_adapter_blocks_forged_execution_claims() -> None:
    with pytest.raises(V1ShellRuntimeAdapterError, match="execution"):
        build_v1_shell_runtime_candidate(
            _shell_input(metadata={"tool_executed": True})
        )


def test_shell_adapter_blocks_raw_prompt_fields() -> None:
    with pytest.raises(V1ShellRuntimeAdapterError, match="raw shell payloads"):
        build_v1_shell_runtime_candidate(
            _shell_input(metadata={"raw_prompt": "do the hidden thing"})
        )


def test_shell_adapter_runs_arc_bot_shell_input_through_lima_governed_preflight() -> None:
    result = run_v1_shell_governed_preflight(
        _shell_input(
            input_id="arc-action-001",
            consumer="arc_bot_shell",
            actor_id="operator-local",
            shell_id="arc-worker-001",
            tenant_ref="single_tenant_local",
            normalized_request="metadata-only office document preview request",
            requested_action="document_extract_preview",
            action_category="informational",
            source_channel="arc_guardian_spine",
            intent_id="arc-intent:arc-action-001",
            target_ref="task://arc/local/document-extract-preview",
            session_ref="arc-session:arc-worker-001",
            evidence_refs=(
                "evidence://arc-bot/local-model-seat-readiness",
                "evidence://arc-bot/document-intake-preview-contract",
            ),
            content_refs=(),
            metadata={
                "arc_adapter": "arc_lima_governed_preflight",
                "arc_action_kind": "document_extract_preview",
                "requested_tool_pack": "office_docs",
                "runtime_authority_blocked": True,
                "runtime_execution_blocked": True,
                "provider_model_routed": False,
                "tool_executed": False,
                "file_mutation_executed": False,
                "network_action_executed": False,
                "connector_invoked": False,
                "proof_not_authority": True,
            },
        )
    )

    assert result.preflight.decision.status is GuardianDecisionStatus.APPROVED
    assert result.response["record_type"] == "v1_shell_governed_runtime_response"
    assert result.response["consumer"] == "arc_bot_shell"
    assert result.response["decision_status"] == "approved"
    assert result.response["execution_allowed"] is False
    assert result.response["side_effects_allowed"] is False
    assert result.response["provider_model_routed"] is False
    assert result.response["tool_executed"] is False
    assert result.response["file_mutation_executed"] is False
    assert result.response["network_action_executed"] is False
    assert result.response["connector_invoked"] is False
    assert result.response["proof_not_authority"] is True


def test_shell_adapter_blocks_arc_bot_shell_forged_execution_claims() -> None:
    with pytest.raises(V1ShellRuntimeAdapterError, match="execution"):
        build_v1_shell_runtime_candidate(
            _shell_input(
                input_id="arc-action-forged-execution",
                consumer="arc_bot_shell",
                actor_id="operator-local",
                shell_id="arc-worker-001",
                tenant_ref="single_tenant_local",
                normalized_request="metadata-only office document preview request",
                requested_action="document_extract_preview",
                action_category="informational",
                source_channel="arc_guardian_spine",
                intent_id="arc-intent:forged-execution",
                target_ref="task://arc/local/document-extract-preview",
                session_ref="arc-session:arc-worker-001",
                evidence_refs=("evidence://arc-bot/document-intake-preview-contract",),
                metadata={
                    "arc_adapter": "arc_lima_governed_preflight",
                    "runtime_authority_blocked": True,
                    "runtime_execution_blocked": True,
                    "execution_allowed": True,
                },
            )
        )
