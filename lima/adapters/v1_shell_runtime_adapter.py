"""V1 shell consumer adapter for governed runtime preflight.

This module gives Sparkbot, Arc-Bot-shell, and future shells one small
normalized-input boundary into LIMA's governed preflight runner. It accepts
structured, already-normalized request metadata only. It does not accept raw
prompts, execute tools, call providers, mutate files, invoke connectors, or
issue approval authority.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
import hashlib
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from lima.kernel import V1GovernedPreflightResult


ALLOWED_CONSUMERS = frozenset({"sparkbot", "arc_bot_shell", "lima_office"})
ALLOWED_ACTION_CATEGORIES = frozenset(
    {
        "admin",
        "browser_network",
        "drafting",
        "file_mutation",
        "informational",
        "model_call",
        "planning",
        "physical_world",
        "shell",
        "tool_call",
    }
)
RAW_INPUT_KEYS = frozenset(
    {
        "human_input",
        "raw_human_input",
        "raw_text",
        "transcript",
        "message_text",
        "prompt",
        "raw_prompt",
        "file_contents",
        "raw_file_contents",
    }
)
FORGED_AUTHORITY_KEYS = frozenset(
    {
        "approval",
        "approval_id",
        "approval_token",
        "approved",
        "approved_by",
        "decision",
        "decision_id",
        "guardian_decision",
        "guardian_decision_ref",
        "operator_pin",
        "pin",
    }
)
FORBIDDEN_TRUE_CLAIM_KEYS = frozenset(
    {
        "action_executed",
        "browser_action_executed",
        "connector_invoked",
        "consumer_runtime_called",
        "execution_allowed",
        "file_mutation_executed",
        "model_request_dispatched",
        "network_action_executed",
        "physical_world_invoked",
        "provider_model_routed",
        "shell_wired",
        "side_effects_allowed",
        "tool_executed",
    }
)


class V1ShellRuntimeAdapterError(ValueError):
    """Raised when shell consumer metadata cannot enter LIMA safely."""


@dataclass(frozen=True)
class V1ShellRuntimeInput:
    """Structured shell request metadata accepted by the V1 adapter."""

    input_id: str
    consumer: str
    actor_id: str
    shell_id: str
    tenant_ref: str
    normalized_request: str
    requested_action: str
    action_category: str
    source_channel: str = "default"
    intent_id: str | None = None
    target_ref: str | None = None
    session_ref: str | None = None
    evidence_refs: Sequence[str] = ()
    content_refs: Sequence[str] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class V1ShellGovernedRuntimeResponse:
    """Safe shell-facing response for one governed LIMA preflight."""

    candidate: Mapping[str, Any]
    preflight: V1GovernedPreflightResult
    response: Mapping[str, Any]


def build_v1_shell_runtime_candidate(shell_input: V1ShellRuntimeInput) -> dict[str, Any]:
    """Build a LIMA candidate from safe shell-normalized metadata."""

    if not isinstance(shell_input, V1ShellRuntimeInput):
        raise V1ShellRuntimeAdapterError("shell_input must be V1ShellRuntimeInput")

    _reject_raw_or_authority_metadata(shell_input.metadata)
    consumer = _allowed_token(shell_input.consumer, ALLOWED_CONSUMERS, "consumer")
    action_category = _allowed_token(
        shell_input.action_category,
        ALLOWED_ACTION_CATEGORIES,
        "action_category",
    )
    input_id = _required_text(shell_input.input_id, "input_id")
    actor_id = _required_text(shell_input.actor_id, "actor_id")
    shell_id = _required_text(shell_input.shell_id, "shell_id")
    tenant_ref = _required_text(shell_input.tenant_ref, "tenant_ref")
    normalized_request = _bounded_text(shell_input.normalized_request, "normalized_request")
    requested_action = _bounded_text(shell_input.requested_action, "requested_action")
    source_channel = _required_text(shell_input.source_channel, "source_channel")
    evidence_refs = _string_sequence(shell_input.evidence_refs, "evidence_refs")
    content_refs = _string_sequence(shell_input.content_refs, "content_refs")
    target_ref = _optional_text(shell_input.target_ref)
    intent_id = _optional_text(shell_input.intent_id)
    session_ref = _optional_text(shell_input.session_ref)

    candidate_id = _stable_id(
        f"candidate:{consumer}",
        f"{input_id}:{actor_id}:{shell_id}:{requested_action}:{target_ref or ''}",
    )
    default_evidence_refs = evidence_refs or (f"shell-input:{consumer}:{input_id}",)

    return {
        "candidate_id": candidate_id,
        "intake_id": input_id,
        "source": consumer,
        "source_channel": source_channel,
        "operator_intent": normalized_request,
        "normalized_request": normalized_request,
        "requested_action": requested_action,
        "action_category": action_category,
        "risk_tier": "low" if action_category in {"informational", "planning", "drafting"} else "high",
        "approval_state": "proposed"
        if action_category in {"informational", "planning", "drafting"}
        else "approval_required",
        "blocked_reason": "shell_request_requires_guardian_preflight",
        "provenance": {
            "actor_id": actor_id,
            "shell_id": shell_id,
            "tenant_ref": tenant_ref,
            "intent_id": intent_id,
            "target_ref": target_ref,
            "session_ref": session_ref,
            "consumer": consumer,
            "evidence_refs": default_evidence_refs,
        },
        "target_ref": target_ref,
        "evidence_refs": default_evidence_refs,
        "executable": False,
        "execution_allowed": False,
        "side_effects_allowed": False,
        "approved": False,
        "freshness": "fresh",
        "replay_status": "not_replayed",
        "metadata": {
            "adapter": "v1_shell_runtime_adapter",
            "consumer": consumer,
            "session_ref": session_ref,
            "content_refs": content_refs,
            "shell_metadata": dict(shell_input.metadata),
            "candidate_only": True,
            "guardian_preflight_required": True,
            "proof_not_authority": True,
        },
    }


def run_v1_shell_governed_preflight(
    shell_input: V1ShellRuntimeInput,
    *,
    audit_store: Any | None = None,
    occurred_at: str | None = None,
    event_id: str | None = None,
) -> V1ShellGovernedRuntimeResponse:
    """Run one safe shell-normalized request through LIMA governed preflight."""

    from lima.kernel import run_v1_governed_preflight

    candidate = build_v1_shell_runtime_candidate(shell_input)
    preflight = run_v1_governed_preflight(
        candidate,
        tenant_ref=shell_input.tenant_ref,
        actor_ref=f"actor:{shell_input.actor_id}",
        occurred_at=occurred_at,
        event_id=event_id,
        content_refs=shell_input.content_refs,
        audit_store=audit_store,
    )
    response = {
        "record_type": "v1_shell_governed_runtime_response",
        "consumer": candidate["source"],
        "candidate_id": candidate["candidate_id"],
        "request_id": preflight.request.request_id,
        "decision_id": preflight.decision.decision_id,
        "decision_status": preflight.decision.status.value,
        "audit_event_id": preflight.audit_event_record["event_id"],
        "lineage_id": preflight.audit_lineage_record["lineage_id"],
        "audit_store_appended": bool(preflight.audit_store_acks),
        "execution_allowed": False,
        "side_effects_allowed": False,
        "provider_model_routed": False,
        "shell_wired": False,
        "tool_executed": False,
        "file_mutation_executed": False,
        "network_action_executed": False,
        "connector_invoked": False,
        "proof_not_authority": True,
        "metadata": {
            "v1_runtime_slice": "shell_governed_preflight_adapter",
            "operator_to_shell_to_lima_step_completed": True,
            "next_step_requires_explicit_execution_authority": True,
        },
    }
    return V1ShellGovernedRuntimeResponse(
        candidate=candidate,
        preflight=preflight,
        response=response,
    )


def _reject_raw_or_authority_metadata(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            if isinstance(key, str):
                normalized_key = key.strip().lower()
                if normalized_key in RAW_INPUT_KEYS:
                    raise V1ShellRuntimeAdapterError("raw shell payloads are not accepted")
                if normalized_key in FORGED_AUTHORITY_KEYS:
                    raise V1ShellRuntimeAdapterError("caller authority claims are not accepted")
                if normalized_key in FORBIDDEN_TRUE_CLAIM_KEYS and nested is not False:
                    raise V1ShellRuntimeAdapterError("shell metadata cannot claim execution")
            _reject_raw_or_authority_metadata(nested)
    elif isinstance(value, (list, tuple, set, frozenset)):
        for nested in value:
            _reject_raw_or_authority_metadata(nested)


def _allowed_token(value: Any, allowed: frozenset[str], field_name: str) -> str:
    normalized = _required_text(value, field_name).strip().lower().replace("-", "_")
    if normalized not in allowed:
        raise V1ShellRuntimeAdapterError(f"{field_name} is not allowed")
    return normalized


def _required_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise V1ShellRuntimeAdapterError(f"{field_name} is required")
    return value.strip()


def _bounded_text(value: Any, field_name: str) -> str:
    text = _required_text(value, field_name)
    if len(text) > 512:
        raise V1ShellRuntimeAdapterError(f"{field_name} exceeds bounded metadata limit")
    return text


def _optional_text(value: Any) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        return None
    return value.strip()


def _string_sequence(value: Sequence[str], field_name: str) -> tuple[str, ...]:
    if isinstance(value, (str, bytes, bytearray)) or not isinstance(value, Sequence):
        raise V1ShellRuntimeAdapterError(f"{field_name} must be a sequence")
    return tuple(str(item).strip() for item in value if str(item).strip())


def _stable_id(prefix: str, value: str) -> str:
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]
    return f"{prefix}:{digest}"
