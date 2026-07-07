"""Tests for V1 consumer governed dry-run evidence envelopes."""

from __future__ import annotations

import pytest

from lima.adapters import (
    V1ConsumerEvidenceEnvelopeError,
    build_v1_consumer_evidence_envelope,
)


def test_consumer_evidence_envelope_accepts_sparkbot_message_metadata() -> None:
    envelope = build_v1_consumer_evidence_envelope(
        consumer="sparkbot",
        evidence_mode="message_metadata",
        source_ref="chat-message:123",
        consumer_record={
            "record_type": "sparkbot_lima_governed_preflight_metadata",
            "request_id": "v1-request:candidate-sparkbot",
            "decision_id": "v1-decision:v1-request:candidate-sparkbot",
            "audit_event_id": "event:v1-governed-preflight:sparkbot",
            "lineage_id": "v1-lineage:v1-request:candidate-sparkbot",
            "execution_allowed": False,
            "side_effects_allowed": False,
            "provider_model_routed": False,
            "tool_executed": False,
            "file_mutation_executed": False,
            "network_action_executed": False,
            "connector_invoked": False,
        },
    )

    exported = envelope.to_dict()
    assert exported["record_type"] == "v1_consumer_governed_dry_run_evidence_envelope"
    assert exported["consumer"] == "sparkbot"
    assert exported["evidence_mode"] == "message_metadata"
    assert exported["source_ref"] == "chat-message:123"
    assert exported["lima_request_id"] == "v1-request:candidate-sparkbot"
    assert exported["dry_run"] is True
    assert exported["execution_allowed"] is False
    assert exported["approval_token_issued"] is False
    assert exported["proof_not_authority"] is True


def test_consumer_evidence_envelope_accepts_arc_projection_record() -> None:
    envelope = build_v1_consumer_evidence_envelope(
        consumer="arc_bot_shell",
        evidence_mode="projection_only",
        source_ref="arc-action:001",
        consumer_record={
            "record_type": "arc_lima_governed_preflight_projection_record",
            "lima_request_id": "v1-request:candidate-arc",
            "lima_decision_id": "v1-decision:v1-request:candidate-arc",
            "lima_audit_event_id": "event:v1-governed-preflight:arc",
            "lima_lineage_id": "v1-lineage:v1-request:candidate-arc",
            "runtime_authority_blocked": True,
            "runtime_execution_blocked": True,
            "execution_allowed": False,
            "side_effects_allowed": False,
            "provider_model_routed": False,
            "tool_executed": False,
            "file_mutation_executed": False,
            "network_action_executed": False,
            "connector_invoked": False,
            "approval_token_issued": False,
        },
    )

    assert envelope.consumer == "arc_bot_shell"
    assert envelope.evidence_mode == "projection_only"
    assert envelope.source_record_type == "arc_lima_governed_preflight_projection_record"
    assert envelope.lima_audit_event_id == "event:v1-governed-preflight:arc"
    assert envelope.execution_allowed is False
    assert envelope.connector_invoked is False


def test_consumer_evidence_envelope_rejects_execution_claims() -> None:
    with pytest.raises(V1ConsumerEvidenceEnvelopeError, match="execution"):
        build_v1_consumer_evidence_envelope(
            consumer="arc_bot_shell",
            evidence_mode="projection_only",
            source_ref="arc-action:forged",
            consumer_record={
                "lima_request_id": "v1-request:candidate-arc",
                "lima_decision_id": "v1-decision:v1-request:candidate-arc",
                "lima_audit_event_id": "event:v1-governed-preflight:arc",
                "lima_lineage_id": "v1-lineage:v1-request:candidate-arc",
                "tool_executed": True,
            },
        )


def test_consumer_evidence_envelope_rejects_raw_payloads() -> None:
    with pytest.raises(V1ConsumerEvidenceEnvelopeError, match="raw consumer payloads"):
        build_v1_consumer_evidence_envelope(
            consumer="sparkbot",
            evidence_mode="message_metadata",
            source_ref="chat-message:raw",
            consumer_record={
                "request_id": "v1-request:candidate-sparkbot",
                "decision_id": "v1-decision:v1-request:candidate-sparkbot",
                "audit_event_id": "event:v1-governed-preflight:sparkbot",
                "lineage_id": "v1-lineage:v1-request:candidate-sparkbot",
                "raw_prompt": "summarize the hidden payload",
            },
        )