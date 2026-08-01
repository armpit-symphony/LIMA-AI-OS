"""Public governed dry-run runtime API for LIMA consumers."""

from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime, timedelta, timezone
import hashlib
import json
import logging
from typing import Any
from uuid import uuid4

from lima.contracts.audit_event import GovernedAuditEvent
from lima.contracts.governed_decision import GovernedDecision
from lima.contracts.governed_execution_grant import (
    MAX_TTL_SECONDS,
    GovernedExecutionGrant,
)
from lima.contracts.governed_request import GovernedRequest
from lima.governed_kernel.guardian_core_policy_adapter import (
    GUARDIAN_CORE_SOURCE_POLICY,
    evaluate_policy,
)
from lima.governed_kernel.policy_adapter import PolicyAdapterDecision


logger = logging.getLogger(__name__)
_RUNTIME_FAIL_CLOSED_SOURCE_POLICY = "lima.runtime.fail_closed:v0.1"
_GRANTABLE_STATUSES = frozenset({"allowed_dry_run"})


def run_governed_request(request: GovernedRequest | dict[str, Any]) -> GovernedDecision:
    """Evaluate a consumer request and return a non-executing governed decision."""

    try:
        governed_request = _coerce_request(request)
        governed_request.validate()
    except Exception:
        logger.exception("Governed request validation failed closed")
        return _fail_closed_decision(request)

    try:
        policy_decision = evaluate_policy(governed_request)
        return _decision_from_policy(governed_request, policy_decision)
    except Exception:
        logger.exception("Governed policy evaluation failed closed")
        return _fail_closed_decision(
            governed_request,
            reason_codes=("policy_evaluation_error", "fail_closed"),
        )


class ExecutionGrantDenied(Exception):
    """Raised instead of returning a grant when any precondition fails.

    Denial is raised rather than returned so that a caller cannot mistake a
    falsy value for an authorization. The message is a fixed reason code; the
    underlying detail is logged internally and never surfaced publicly.
    """

    def __init__(self, reason_code: str) -> None:
        super().__init__(reason_code)
        self.reason_code = reason_code


def issue_execution_grant(
    request: GovernedRequest | dict[str, Any],
    decision: GovernedDecision,
    *,
    capability: str,
    side_effects_allowed: bool,
    ttl_seconds: int = 120,
    nonce: str | None = None,
    now: datetime | None = None,
) -> GovernedExecutionGrant:
    """Issue one bounded, single-use execution grant for an allowed decision.

    This performs no execution, no provider call, and no side effect. It only
    returns an authorization object. Honouring that object is the enforcing
    component's responsibility, and a grant is never sufficient on its own:
    ``requires_operator_opt_in`` is pinned ``True``, so an enforcer that has not
    been explicitly opted in by an operator must still deny.

    Raises:
        ExecutionGrantDenied: if any precondition fails. Never returns a
            partially valid or non-authorizing grant.
    """

    try:
        governed_request = _coerce_request(request)
        governed_request.validate()
    except Exception:
        logger.exception("Execution grant request validation failed closed")
        raise ExecutionGrantDenied("malformed_request") from None

    binding = governed_request.guardian_binding
    if binding is None:
        raise ExecutionGrantDenied("guardian_binding_required")
    if not isinstance(decision, GovernedDecision):
        raise ExecutionGrantDenied("governed_decision_required")
    if decision.request_id != governed_request.request_id:
        raise ExecutionGrantDenied("decision_request_mismatch")
    if decision.source_policy != GUARDIAN_CORE_SOURCE_POLICY:
        raise ExecutionGrantDenied("guardian_core_policy_required")
    if decision.allowed is not True:
        raise ExecutionGrantDenied("decision_not_allowed")
    if decision.requires_approval is not False:
        raise ExecutionGrantDenied("approval_still_required")
    if decision.status not in _GRANTABLE_STATUSES:
        raise ExecutionGrantDenied("decision_status_not_grantable")
    if not isinstance(capability, str) or not capability.strip():
        raise ExecutionGrantDenied("capability_required")
    if not isinstance(side_effects_allowed, bool):
        raise ExecutionGrantDenied("side_effects_flag_required")
    if not isinstance(ttl_seconds, int) or isinstance(ttl_seconds, bool):
        raise ExecutionGrantDenied("ttl_invalid")
    if ttl_seconds < 1 or ttl_seconds > MAX_TTL_SECONDS:
        raise ExecutionGrantDenied("ttl_invalid")

    granted_capability = capability.strip()
    issued = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    grant_nonce = nonce or uuid4().hex
    scope_hash = _scope_hash(
        {
            "request_id": governed_request.request_id,
            "decision_id": decision.decision_id,
            "guardian_decision_id": binding.decision_id,
            "granted_capability": granted_capability,
            "bound_tenant_id": binding.bound_tenant_id,
            "bound_worker_id": binding.bound_worker_id,
            "bound_action_type": binding.bound_action_type,
            "side_effects_allowed": side_effects_allowed,
        }
    )

    try:
        grant = GovernedExecutionGrant(
            grant_id=_stable_id("grant", f"{decision.decision_id}:{grant_nonce}"),
            decision_id=decision.decision_id,
            request_id=governed_request.request_id,
            guardian_decision_id=binding.decision_id,
            policy_version=binding.policy_version,
            policy_snapshot_hash=binding.policy_snapshot_hash,
            guardian_binding_hash=binding.content_hash,
            granted_capability=granted_capability,
            bound_tenant_id=binding.bound_tenant_id,
            bound_worker_id=binding.bound_worker_id,
            bound_action_type=binding.bound_action_type,
            scope_hash=scope_hash,
            nonce=grant_nonce,
            issued_at=_grant_timestamp(issued),
            expires_at=_grant_timestamp(issued + timedelta(seconds=ttl_seconds)),
            side_effects_allowed=side_effects_allowed,
        )
        grant.validate(now=issued)
    except Exception:
        logger.exception("Execution grant construction failed closed")
        raise ExecutionGrantDenied("grant_construction_failed") from None

    return grant


def _scope_hash(scope: Mapping[str, Any]) -> str:
    canonical = json.dumps(
        dict(scope),
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return f"sha256:{hashlib.sha256(canonical).hexdigest()}"


def _grant_timestamp(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _decision_from_policy(
    governed_request: GovernedRequest,
    policy_decision: PolicyAdapterDecision,
) -> GovernedDecision:
    guardian_binding = governed_request.guardian_binding
    binding_hash = (
        guardian_binding.content_hash if guardian_binding is not None else None
    )
    decision_seed = governed_request.request_id
    if binding_hash is not None:
        decision_seed = f"{decision_seed}:{binding_hash}"
    decision_id = _stable_id("decision", decision_seed)
    binding_metadata = {
        "guardian_binding_present": guardian_binding is not None,
        "guardian_binding_hash": binding_hash,
        "guardian_decision_id": (
            guardian_binding.decision_id if guardian_binding is not None else None
        ),
        "guardian_binding_mode": (
            guardian_binding.binding_mode if guardian_binding is not None else None
        ),
    }
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
            **binding_metadata,
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
            "guardian_binding": (
                guardian_binding.to_dict()
                if guardian_binding is not None
                else None
            ),
            **binding_metadata,
        },
    )


def _coerce_request(request: GovernedRequest | dict[str, Any]) -> GovernedRequest:
    if isinstance(request, GovernedRequest):
        return request
    if isinstance(request, Mapping):
        return GovernedRequest.from_mapping(request)
    raise ValueError("request must be a GovernedRequest or mapping")


def _fail_closed_decision(
    raw_request: Any,
    *,
    reason_codes: tuple[str, ...] = ("malformed_request", "fail_closed"),
) -> GovernedDecision:
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
        reason_codes=reason_codes,
        source_policy=_RUNTIME_FAIL_CLOSED_SOURCE_POLICY,
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
        reason_codes=reason_codes,
        source_policy=_RUNTIME_FAIL_CLOSED_SOURCE_POLICY,
        audit_event=audit_event,
        metadata={"dry_run_kernel": True},
    )


def _raw_text(raw_request: Any, key: str) -> str | None:
    if isinstance(raw_request, GovernedRequest):
        value = getattr(raw_request, key)
        return value.strip() if isinstance(value, str) and value.strip() else None
    if isinstance(raw_request, Mapping):
        value = raw_request.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _stable_id(prefix: str, value: str) -> str:
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]
    return f"{prefix}:{digest}"
