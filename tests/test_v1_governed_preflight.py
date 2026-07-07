"""Runtime tests for the V1 governed preflight runner."""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

import pytest

from lima.contracts.guardian import GuardianDecisionStatus
from lima.kernel import V1GovernedPreflightError, run_v1_governed_preflight
from lima.persistence import V1LocalAuditStore


def _candidate(**overrides: Any) -> dict[str, Any]:
    candidate = {
        "candidate_id": "candidate:sparkbot:status-summary",
        "intake_id": "intake:sparkbot:001",
        "source": "sparkbot_shell",
        "source_channel": "workspace",
        "operator_intent": "summarize status note",
        "normalized_request": "summarize status note",
        "requested_action": "summarize status",
        "action_category": "informational",
        "risk_tier": "low",
        "approval_state": "proposed",
        "blocked_reason": "non_executable_candidate_requires_future_guardian_review",
        "provenance": {
            "actor_id": "user-123",
            "shell_id": "sparkbot-shell",
            "intent_id": "intent:sparkbot:status-summary",
            "target_ref": "note:status",
            "evidence_refs": ["evidence:sparkbot:status-summary"],
        },
        "target_ref": "note:status",
        "evidence_refs": ["evidence:sparkbot:status-summary"],
        "executable": False,
        "execution_allowed": False,
        "side_effects_allowed": False,
        "approved": False,
        "freshness": "fresh",
        "replay_status": "not_replayed",
    }
    candidate.update(overrides)
    return candidate


def test_v1_governed_preflight_composes_request_guardian_and_audit_records() -> None:
    result = run_v1_governed_preflight(
        _candidate(),
        tenant_ref="tenant:local",
        occurred_at="2026-06-30T12:00:00Z",
        event_id="event:v1-preflight:001",
    )

    assert result.request.request_id == "v1-request:candidate-sparkbot-status-summary"
    assert result.decision.status is GuardianDecisionStatus.APPROVED
    assert result.audit_event_record["record_type"] == "v1_audit_event"
    assert result.audit_event_record["event_id"] == "event:v1-preflight:001"
    assert result.audit_event_record["decision_id"] == result.decision.decision_id
    assert result.audit_lineage_record["record_type"] == "v1_audit_lineage"
    assert result.audit_lineage_record["lineage_id"] == result.audit_event_record["lineage_id"]
    assert result.execution_allowed is False
    assert result.side_effects_allowed is False
    assert result.provider_model_routed is False
    assert result.shell_wired is False
    assert result.audit_store_acks == ()


def test_v1_governed_preflight_can_append_to_explicit_local_audit_store() -> None:
    with TemporaryDirectory(prefix="lima-v1-preflight-") as temp_dir:
        audit_store = V1LocalAuditStore(Path(temp_dir) / "audit-store")
        result = run_v1_governed_preflight(
            _candidate(),
            tenant_ref="tenant:local",
            occurred_at="2026-06-30T12:00:00Z",
            event_id="event:v1-preflight:store",
            audit_store=audit_store,
        )

        assert len(result.audit_store_acks) == 2
        assert all(ack["stored"] is True for ack in result.audit_store_acks)
        assert audit_store.get_by_event_id(
            "event:v1-preflight:store",
            tenant_ref="tenant:local",
            shell_id="sparkbot-shell",
        ) == result.audit_event_record
        assert result.audit_store_acks[0]["execution_allowed"] is False


def test_v1_governed_preflight_rejects_invalid_audit_context() -> None:
    with pytest.raises(V1GovernedPreflightError, match="tenant_ref"):
        run_v1_governed_preflight(_candidate(), tenant_ref="")

