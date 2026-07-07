"""V1 consumer evidence envelope for governed dry-run outputs.

This module normalizes already-sanitized consumer-side evidence records from
Sparkbot and Arc-Bot-shell into one LIMA-readable envelope shape. It does not
execute providers, tools, connectors, files, browsers, networks, or approval
flows. It also does not persist evidence.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import asdict, dataclass
from typing import Any


ALLOWED_CONSUMERS = frozenset({"sparkbot", "arc_bot_shell"})
ALLOWED_EVIDENCE_MODES = frozenset({"message_metadata", "projection_only"})
FORBIDDEN_TRUE_CLAIM_KEYS = frozenset(
    {
        "approval_token_issued",
        "connector_invoked",
        "execution_allowed",
        "file_mutation_executed",
        "model_request_dispatched",
        "network_action_executed",
        "provider_model_routed",
        "side_effects_allowed",
        "tool_executed",
    }
)
AUTHORITY_KEYS = frozenset(
    {
        "approval",
        "approval_id",
        "approval_token",
        "approved",
        "approved_by",
        "guardian_decision",
        "operator_pin",
        "pin",
    }
)
RAW_PAYLOAD_KEYS = frozenset(
    {
        "file_contents",
        "human_input",
        "message_text",
        "prompt",
        "raw_file_contents",
        "raw_human_input",
        "raw_prompt",
        "raw_text",
        "transcript",
    }
)


class V1ConsumerEvidenceEnvelopeError(ValueError):
    """Raised when consumer evidence cannot be accepted safely."""


@dataclass(frozen=True)
class V1ConsumerEvidenceEnvelope:
    """LIMA-readable envelope for one governed dry-run consumer evidence record."""

    record_type: str
    consumer: str
    evidence_mode: str
    source_record_type: str
    source_ref: str
    lima_request_id: str
    lima_decision_id: str
    lima_audit_event_id: str
    lima_lineage_id: str
    dry_run: bool = True
    execution_allowed: bool = False
    side_effects_allowed: bool = False
    provider_model_routed: bool = False
    tool_executed: bool = False
    file_mutation_executed: bool = False
    network_action_executed: bool = False
    connector_invoked: bool = False
    approval_token_issued: bool = False
    proof_not_authority: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_v1_consumer_evidence_envelope(
    *,
    consumer: str,
    evidence_mode: str,
    source_ref: str,
    consumer_record: Mapping[str, Any],
) -> V1ConsumerEvidenceEnvelope:
    """Build a safe LIMA envelope from sanitized consumer dry-run evidence."""

    if not isinstance(consumer_record, Mapping) or not consumer_record:
        raise V1ConsumerEvidenceEnvelopeError("consumer_record must be a non-empty mapping")

    _reject_raw_or_authority_claims(consumer_record)
    normalized_consumer = _allowed(consumer, ALLOWED_CONSUMERS, "consumer")
    normalized_mode = _allowed(evidence_mode, ALLOWED_EVIDENCE_MODES, "evidence_mode")
    source_ref_text = _required_text(source_ref, "source_ref")

    return V1ConsumerEvidenceEnvelope(
        record_type="v1_consumer_governed_dry_run_evidence_envelope",
        consumer=normalized_consumer,
        evidence_mode=normalized_mode,
        source_record_type=_required_text(
            consumer_record.get("record_type") or "consumer_governed_dry_run_record",
            "source_record_type",
        ),
        source_ref=source_ref_text,
        lima_request_id=_first_required(
            consumer_record,
            "lima_request_id",
            "request_id",
        ),
        lima_decision_id=_first_required(
            consumer_record,
            "lima_decision_id",
            "decision_id",
        ),
        lima_audit_event_id=_first_required(
            consumer_record,
            "lima_audit_event_id",
            "audit_event_id",
        ),
        lima_lineage_id=_first_required(
            consumer_record,
            "lima_lineage_id",
            "lineage_id",
        ),
    )


def _reject_raw_or_authority_claims(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            if isinstance(key, str):
                normalized_key = key.strip().lower()
                if normalized_key in RAW_PAYLOAD_KEYS:
                    raise V1ConsumerEvidenceEnvelopeError("raw consumer payloads are not accepted")
                if normalized_key in AUTHORITY_KEYS:
                    raise V1ConsumerEvidenceEnvelopeError("consumer authority claims are not accepted")
                if normalized_key in FORBIDDEN_TRUE_CLAIM_KEYS and nested is not False:
                    raise V1ConsumerEvidenceEnvelopeError("consumer evidence cannot claim execution")
            _reject_raw_or_authority_claims(nested)
    elif isinstance(value, (list, tuple, set, frozenset)):
        for nested in value:
            _reject_raw_or_authority_claims(nested)


def _allowed(value: Any, allowed: frozenset[str], field_name: str) -> str:
    text = _required_text(value, field_name).lower().replace("-", "_")
    if text not in allowed:
        raise V1ConsumerEvidenceEnvelopeError(f"{field_name} is not allowed")
    return text


def _first_required(record: Mapping[str, Any], *keys: str) -> str:
    for key in keys:
        value = record.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    raise V1ConsumerEvidenceEnvelopeError(f"missing required evidence field: {'/'.join(keys)}")


def _required_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise V1ConsumerEvidenceEnvelopeError(f"{field_name} is required")
    return value.strip()