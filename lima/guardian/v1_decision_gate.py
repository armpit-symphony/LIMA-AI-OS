"""V1 GuardianDecision preflight gate.

This module reviews V1 typed requests and returns non-executing
GuardianDecision metadata. It does not approve execution, issue approval
tokens, persist audit data, route providers, wire shells, or invoke any
external system.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Final

from lima.contracts.guardian import (
    ConsequentialActionRequest,
    ConsequentialActionType,
    GuardianDecision,
    GuardianDecisionStatus,
)


SAFE_ACTION_CATEGORIES: Final[frozenset[str]] = frozenset(
    {"informational", "planning", "drafting"}
)
OPERATOR_APPROVAL_CATEGORIES: Final[frozenset[str]] = frozenset(
    {"admin", "file_mutation", "shell"}
)
FUTURE_POLICY_CATEGORIES: Final[frozenset[str]] = frozenset(
    {"browser_network", "model_call", "robotics_physical_world", "tool_call"}
)
FORGED_AUTHORITY_KEYS: Final[frozenset[str]] = frozenset(
    {
        "approval",
        "approval_id",
        "approval_token",
        "approved",
        "decision",
        "decision_id",
        "guardian_decision",
        "guardian_decision_ref",
        "operator_pin",
        "pin",
    }
)


class V1GuardianDecisionGateError(ValueError):
    """Raised when a typed request cannot be reviewed by the V1 gate."""


def review_v1_runtime_request(request: ConsequentialActionRequest) -> GuardianDecision:
    """Return deterministic, non-executing GuardianDecision preflight metadata."""

    if not isinstance(request, ConsequentialActionRequest):
        raise V1GuardianDecisionGateError("request must be a ConsequentialActionRequest")

    _reject_forged_authority(request.metadata)
    action_category = str(request.metadata.get("v1_action_category", "")).strip().lower()
    status, approval_level, reason = _classify_request(request, action_category)
    decision_id = f"v1-decision:{request.request_id}"
    audit_linkage = _decision_audit_linkage(request, decision_id)

    return GuardianDecision(
        decision_id=decision_id,
        request_id=request.request_id,
        intent_id=request.intent_id,
        input_id=request.input_id,
        actor_id=request.actor_id,
        shell_id=request.shell_id,
        action_type=request.action_type,
        target_ref=request.target_ref,
        risk_class=request.risk_class,
        status=status,
        approval_level=approval_level,
        allowed_tool_packs=(),
        constraints={
            "v1_preflight_only": True,
            "non_executing": True,
            "execution_allowed": False,
            "side_effects_allowed": False,
            "approval_token_issued": False,
            "provider_model_routed": False,
            "shell_wired": False,
            "persistent": False,
        },
        evidence_refs=request.evidence_refs,
        policy_version="v1-g11-preflight",
        created_at="v1-g11-local",
        decided_at="v1-g11-local",
        decided_by="lima.v1_guardian_decision_gate",
        reason=reason,
        metadata={
            "v1_runtime_slice": "typed_request_guardian_decision_preflight",
            "v1_action_category": action_category,
            "destructive": bool(request.typed_args.get("destructive")),
            "audit_evidence_linkage": audit_linkage,
            "non_persistent": True,
            "approval_token_issued": False,
        },
    )


def _classify_request(
    request: ConsequentialActionRequest,
    action_category: str,
) -> tuple[GuardianDecisionStatus, str | None, str]:
    if _request_is_forged_or_executable(request):
        return (
            GuardianDecisionStatus.DENIED,
            None,
            "v1 gate denies forged or executable request metadata",
        )

    if action_category in SAFE_ACTION_CATEGORIES and request.risk_class in {"low", "read_only"}:
        return (
            GuardianDecisionStatus.APPROVED,
            None,
            "v1 gate reviewed safe non-executing request",
        )

    if action_category in OPERATOR_APPROVAL_CATEGORIES:
        return (
            GuardianDecisionStatus.NEEDS_OPERATOR_PIN,
            "operator_pin",
            "v1 gate requires operator approval and does not execute",
        )

    if action_category in FUTURE_POLICY_CATEGORIES:
        return (
            GuardianDecisionStatus.DENIED,
            None,
            "v1 gate blocks future-policy action without routing or execution",
        )

    if request.action_type is ConsequentialActionType.UNKNOWN:
        return (
            GuardianDecisionStatus.DENIED,
            None,
            "v1 gate denies unknown action type",
        )

    return (
        GuardianDecisionStatus.DENIED,
        None,
        "v1 gate denies unrecognized action category",
    )


def _request_is_forged_or_executable(request: ConsequentialActionRequest) -> bool:
    metadata = request.metadata
    if metadata.get("execution_allowed") is not False:
        return True
    if metadata.get("side_effects_allowed") is not False:
        return True
    if metadata.get("approval_token_issued") is not False:
        return True
    if request.typed_args.get("approved") is True:
        return True
    return False


def _reject_forged_authority(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            if isinstance(key, str) and key.strip().lower() in FORGED_AUTHORITY_KEYS:
                raise V1GuardianDecisionGateError(
                    "caller-supplied authority metadata is not accepted"
                )
            _reject_forged_authority(nested)
    elif isinstance(value, (list, tuple, set, frozenset)):
        for nested in value:
            _reject_forged_authority(nested)


def _decision_audit_linkage(
    request: ConsequentialActionRequest,
    decision_id: str,
) -> dict[str, Any]:
    request_linkage = request.metadata.get("audit_evidence_linkage")
    if not isinstance(request_linkage, Mapping):
        request_linkage = {}
    return {
        "lineage_id": request_linkage.get("lineage_id")
        or f"v1-lineage:{request.request_id}",
        "decision_id": decision_id,
        "request_id": request.request_id,
        "input_id": request.input_id,
        "intent_id": request.intent_id,
        "actor_id": request.actor_id,
        "shell_id": request.shell_id,
        "action_type": request.action_type.value,
        "target_ref": request.target_ref,
        "risk_class": request.risk_class,
        "evidence_refs": tuple(request.evidence_refs),
        "redacted_summary": request_linkage.get("redacted_summary")
        or "v1-g11-redacted-preflight-summary",
        "persistent": False,
    }
