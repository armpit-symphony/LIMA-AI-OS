"""Public governed dry-run runtime API for LIMA consumers."""

from __future__ import annotations

from collections.abc import Mapping
import hashlib
import logging
from typing import Any

from lima.contracts.audit_event import GovernedAuditEvent
from lima.contracts.governed_decision import GovernedDecision
from lima.contracts.governed_request import GovernedRequest
from lima.governed_kernel.guardian_core_policy_adapter import SOURCE_POLICY, evaluate_policy


logger = logging.getLogger(__name__)


def run_governed_request(request: GovernedRequest | dict[str, Any]) -> GovernedDecision:
    """Evaluate a consumer request and return a non-executing governed decision."""

    try:
        governed_request = _coerce_request(request)
        governed_request.validate()
    except Exception:
        logger.exception("Governed request validation failed closed")
        return _fail_closed_decision(request)

    policy_decision = evaluate_policy(governed_request)
    decision_id = _stable_id("decision", governed_request.request_id)
    audit_event = GovernedAuditEvent(
        event_id=_stable_id("audit", f"{governed_request.request_id}:{decision_id}"),
        request_id=governed_request.request_id,
        decision_id=decision_id,
        consumer=governed_request.consumer,
        actor_id=governed_request.actor_id,
        surface=governed_request.surface,
        status=policy_decision.status,
        reason_codes=policy_decision.reason_codes,
        evidence_refs=tuple(governed_request.evidence_refs),
        source_policy=policy_decision.source_policy,
        metadata={
            "guardian_semantic": policy_decision.guardian_semantic,
            "dry_run_kernel": True,
            "no_execution_path": True,
        },
    )
    return GovernedDecision(
        decision_id=decision_id,
        request_id=governed_request.request_id,
        consumer=governed_request.consumer,
        status=policy_decision.status,
        allowed=policy_decision.allowed,
        requires_approval=policy_decision.requires_approval,
        risk_level=policy_decision.risk_level,
        reason_codes=policy_decision.reason_codes,
        source_policy=policy_decision.source_policy,
        audit_event=audit_event,
        metadata={
            "guardian_semantic": policy_decision.guardian_semantic,
            "dry_run_kernel": True,
            "request": governed_request.to_dict(),
        },
    )


def _coerce_request(request: GovernedRequest | dict[str, Any]) -> GovernedRequest:
    if isinstance(request, GovernedRequest):
        return request
    if isinstance(request, Mapping):
        return GovernedRequest.from_mapping(request)
    raise ValueError("request must be a GovernedRequest or mapping")


def _fail_closed_decision(raw_request: Any) -> GovernedDecision:
    request_id = _raw_text(raw_request, "request_id") or "malformed-request"
    consumer = _raw_text(raw_request, "consumer") or "unknown"
    actor_id = _raw_text(raw_request, "actor_id") or "unknown"
    surface = _raw_text(raw_request, "surface") or "unknown"
    decision_id = _stable_id("decision", f"{request_id}:fail-closed")
    audit_event = GovernedAuditEvent(
        event_id=_stable_id("audit", f"{request_id}:{decision_id}:fail-closed"),
        request_id=request_id,
        decision_id=decision_id,
        consumer=consumer,
        actor_id=actor_id,
        surface=surface,
        status="denied",
        reason_codes=("malformed_request", "fail_closed"),
        source_policy=SOURCE_POLICY,
        metadata={"dry_run_kernel": True, "no_execution_path": True},
    )
    return GovernedDecision(
        decision_id=decision_id,
        request_id=request_id,
        consumer=consumer,
        status="denied",
        allowed=False,
        requires_approval=False,
        risk_level="blocked",
        reason_codes=("malformed_request", "fail_closed"),
        source_policy=SOURCE_POLICY,
        audit_event=audit_event,
        metadata={"dry_run_kernel": True},
    )


def _raw_text(raw_request: Any, key: str) -> str | None:
    if isinstance(raw_request, Mapping):
        value = raw_request.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _stable_id(prefix: str, value: str) -> str:
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]
    return f"{prefix}:{digest}"
