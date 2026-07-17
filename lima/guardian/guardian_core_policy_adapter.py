"""Guardian Core-backed policy adapter for LIMA governed dry-run requests.

This adapter is the boundary between LIMA's public ``GovernedRequest`` contract
and Guardian Suite's pure ``guardian_core.policy`` seam. It never executes a
tool; it only asks Guardian Core for policy semantics and maps those semantics
into LIMA's non-executing ``GovernedDecision`` statuses.
"""

from __future__ import annotations

from dataclasses import replace
from typing import Any, Callable, Final, Mapping

from lima.contracts.governed_request import GovernedRequest
from lima.guardian.policy_adapter import (
    PolicyAdapterDecision,
    evaluate_policy as evaluate_static_policy,
    map_guardian_semantic,
)


GUARDIAN_CORE_SOURCE_POLICY: Final[str] = "guardian_core.policy"
STATIC_FALLBACK_SOURCE_POLICY: Final[str] = "lima_static_policy_fallback"
SOURCE_POLICY: Final[str] = STATIC_FALLBACK_SOURCE_POLICY

_READ_CATEGORIES: Final[frozenset[str]] = frozenset(
    {"read", "status", "informational", "planning", "drafting", "preview"}
)
_CONFIRM_CATEGORIES: Final[frozenset[str]] = frozenset(
    {"external_write", "tool_call", "file_mutation"}
)
_DENY_CATEGORIES: Final[frozenset[str]] = frozenset(
    {"shell", "model_call", "connector_call", "physical_world", "unknown"}
)


def evaluate_policy(request: GovernedRequest) -> PolicyAdapterDecision:
    """Evaluate a request through Guardian Core or an explicit static fallback."""

    try:
        decide_tool_use = _load_guardian_core_decider()
    except ModuleNotFoundError:
        return _static_fallback_decision(request, ("guardian_core_unavailable",))

    tool_name, args, extra_policies = _guardian_core_input_for_request(request)
    try:
        core_decision = decide_tool_use(
            tool_name,
            args,
            room_execution_allowed=bool(
                request.trust_context.get("room_execution_allowed")
                or request.trust_context.get("execution_gate_present")
            ),
            is_operator=bool(request.trust_context.get("is_operator")),
            is_privileged=bool(request.trust_context.get("is_privileged")),
            extra_policies=extra_policies,
        )
    except Exception as exc:
        return PolicyAdapterDecision(
            guardian_semantic="deny",
            status="denied",
            allowed=False,
            requires_approval=False,
            risk_level="blocked",
            reason_codes=("guardian_core_policy_error", "fail_closed", str(exc)),
            source_policy=GUARDIAN_CORE_SOURCE_POLICY,
        )

    return _map_core_decision(core_decision)


def _load_guardian_core_decider() -> Callable[..., Any]:
    from guardian_core.policy import decide_tool_use

    return decide_tool_use


def _static_fallback_decision(
    request: GovernedRequest,
    extra_reason_codes: tuple[str, ...] = (),
) -> PolicyAdapterDecision:
    decision = evaluate_static_policy(request)
    return replace(
        decision,
        source_policy=STATIC_FALLBACK_SOURCE_POLICY,
        reason_codes=tuple(decision.reason_codes)
        + extra_reason_codes
        + ("static_policy_fallback",),
    )


def _map_core_decision(core_decision: Any) -> PolicyAdapterDecision:
    semantic = str(getattr(core_decision, "action", "") or "deny").strip().lower()
    mapped = map_guardian_semantic(semantic)
    high_risk = bool(getattr(core_decision, "high_risk", False))
    reason = str(getattr(core_decision, "reason", "") or "").strip()
    reason_codes = tuple(mapped.reason_codes)
    if reason:
        reason_codes = reason_codes + (_reason_code(reason),)
    if high_risk and mapped.risk_level != "blocked":
        risk_level = "high" if mapped.status == "privileged_required" else "medium"
    else:
        risk_level = mapped.risk_level
    return PolicyAdapterDecision(
        guardian_semantic=mapped.guardian_semantic,
        status=mapped.status,
        allowed=mapped.allowed,
        requires_approval=mapped.requires_approval,
        risk_level=risk_level,
        reason_codes=reason_codes,
        source_policy=GUARDIAN_CORE_SOURCE_POLICY,
    )


def _guardian_core_input_for_request(
    request: GovernedRequest,
) -> tuple[str, Mapping[str, Any], Mapping[str, Mapping[str, Any]]]:
    category = _fold(request.action_category)
    requested_tool = _fold(request.tool_name) or "lima_unknown_action"
    args = {
        "requested_action": request.requested_action,
        "action_category": category,
        "tool_args": dict(request.tool_args),
        "trust_context": dict(request.trust_context),
    }

    if category in _READ_CATEGORIES:
        return requested_tool, args, {
            requested_tool: _policy("read", "lima_preview", "allow", "read")
        }

    if category in _CONFIRM_CATEGORIES:
        return requested_tool, args, {
            requested_tool: _policy(
                "write",
                "lima_side_effect_preview",
                "confirm",
                "write_external",
                True,
            )
        }

    if category == "credential_access":
        tool_name = requested_tool if "credential" in requested_tool else "lima_credential_reveal"
        return tool_name, args, {
            tool_name: _policy(
                "admin",
                "credential",
                "privileged_reveal",
                "credential_reveal",
                True,
            )
        }

    if category == "shell":
        return "server_read_command", args, {}

    if category in _DENY_CATEGORIES:
        return requested_tool, args, {
            requested_tool: _policy("admin", category or "unknown", "deny", "deny", True)
        }

    return requested_tool, args, {
        requested_tool: _policy("admin", "unknown", "deny", "deny", True)
    }


def _policy(
    scope: str,
    resource: str,
    default_action: str,
    action_type: str,
    high_risk: bool = False,
) -> Mapping[str, Any]:
    return {
        "scope": scope,
        "resource": resource,
        "default_action": default_action,
        "action_type": action_type,
        "high_risk": high_risk,
    }


def _reason_code(value: str) -> str:
    normalized = "".join(ch if ch.isalnum() else "_" for ch in value.lower())
    while "__" in normalized:
        normalized = normalized.replace("__", "_")
    return normalized.strip("_")[:80] or "guardian_core_reason"


def _fold(value: Any) -> str:
    return str(value or "").strip().lower()


__all__ = [
    "GUARDIAN_CORE_SOURCE_POLICY",
    "STATIC_FALLBACK_SOURCE_POLICY",
    "SOURCE_POLICY",
    "evaluate_policy",
]
