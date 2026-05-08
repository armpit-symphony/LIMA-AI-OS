"""Tool-pack risk policy contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Protocol, Sequence


class PolicyExposure(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    REQUIRE_CONFIRMATION = "require_confirmation"
    REQUIRE_GUARDIAN_REVIEW = "require_guardian_review"
    REQUIRE_OPERATOR_PIN = "require_operator_pin"
    REQUIRE_BREAKGLASS = "require_breakglass"


@dataclass(frozen=True)
class ToolPackRiskRule:
    pack_name: str
    default_risk_class: str
    read_risk_class: str | None = None
    write_risk_class: str | None = None
    destructive_risk_class: str | None = None
    default_exposure: PolicyExposure = PolicyExposure.DENY
    required_approval_level: str | None = None
    requires_decision: bool = True
    requires_explicit_confirmation: bool = False
    requires_operator_pin: bool = False
    requires_breakglass: bool = False
    requires_audit: bool = True
    constraints: Mapping[str, Any] = field(default_factory=dict)
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ToolPackRiskPolicy:
    policy_id: str
    policy_version: str
    shell_id: str | None
    rules: Sequence[ToolPackRiskRule]
    default_unknown_risk: str = "critical"
    unknown_default_exposure: PolicyExposure = PolicyExposure.DENY
    created_at: str = ""
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class PolicyEvaluationContext:
    shell_id: str
    actor_id: str
    intent_id: str | None
    decision_id: str | None
    requested_pack: str
    requested_tool: str | None
    action_type: str | None
    risk_class: str | None
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class PolicyDecision:
    policy_decision_id: str
    policy_id: str
    decision_id: str | None
    allowed: bool
    pack_name: str
    tool_name: str | None
    risk_class: str
    approval_level: str | None
    reason: str | None
    constraints: Mapping[str, Any] = field(default_factory=dict)
    metadata: Mapping[str, Any] = field(default_factory=dict)


class PolicyProtocol(Protocol):
    """Describe and evaluate policy without executing tools."""

    def describe_policy(self) -> ToolPackRiskPolicy:
        """Return the policy contract currently in scope."""
        ...

    def evaluate(self, context: PolicyEvaluationContext) -> PolicyDecision:
        """Evaluate exposure policy for a pack/tool/action request."""
        ...
