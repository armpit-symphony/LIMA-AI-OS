"""Guardian trust-boundary contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal, Protocol

GuardianAction = Literal["allow", "deny", "approval_required", "route"]
RiskLevel = Literal["read_only", "low", "medium", "high", "blocked"]


@dataclass(frozen=True)
class GuardianContext:
    """Request context used by Guardian to classify an operation."""

    actor_id: str
    shell_id: str
    session_id: str | None = None
    allowed_tool_packs: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class GuardianDecision:
    """Guardian decision for a model call, tool call, or driver command."""

    decision_id: str
    action: GuardianAction
    risk_level: RiskLevel
    reason: str
    approval_token: str | None = None
    route_to: str | None = None
    audit_event_id: str | None = None


class GuardianProtocol(Protocol):
    """Guardian is the mandatory syscall gate for external action."""

    def classify_model_call(self, request: Any, context: GuardianContext) -> GuardianDecision:
        """Classify a model request before the Harness calls a model provider."""
        ...

    def classify_tool_call(self, tool_call: Any, context: GuardianContext) -> GuardianDecision:
        """Classify a tool call before any driver or tool pack executes it."""
        ...

    def require_approval(self, decision: GuardianDecision, context: GuardianContext) -> GuardianDecision:
        """Create or refresh approval state for an approval-required decision."""
        ...

    def record_decision(self, decision: GuardianDecision, context: GuardianContext) -> str:
        """Record a Guardian decision and return an audit event identifier."""
        ...
