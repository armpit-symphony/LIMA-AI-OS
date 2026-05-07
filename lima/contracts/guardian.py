"""Guardian trust-boundary contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Literal, Mapping, Protocol, Sequence

GuardianAction = Literal["allow", "deny", "approval_required", "route"]
RiskLevel = Literal["read_only", "low", "medium", "high", "blocked"]


class GuardianDecisionStatus(str, Enum):
    APPROVED = "approved"
    DENIED = "denied"
    NEEDS_CLARIFICATION = "needs_clarification"
    NEEDS_HUMAN_CONFIRMATION = "needs_human_confirmation"
    NEEDS_OPERATOR_PIN = "needs_operator_pin"
    NEEDS_BREAKGLASS = "needs_breakglass"
    ESCALATED = "escalated"
    EXPIRED = "expired"
    REVOKED = "revoked"
    SUPERSEDED = "superseded"


class ConsequentialActionType(str, Enum):
    MODEL_CALL = "model_call"
    TOOL_CALL = "tool_call"
    DRIVER_COMMAND = "driver_command"
    TERMINAL_COMMAND = "terminal_command"
    FILE_OPERATION = "file_operation"
    BROWSER_ACTION = "browser_action"
    NETWORK_ACTION = "network_action"
    SEND_MESSAGE = "send_message"
    ADMIN_ACTION = "admin_action"
    PAYMENT_ACTION = "payment_action"
    ROBOT_ACTION = "robot_action"
    DEPLOY_ACTION = "deploy_action"
    SECRET_ACCESS = "secret_access"
    MEMORY_WRITE = "memory_write"
    TASK_MUTATION = "task_mutation"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class GuardianContext:
    """Request context used by Guardian to classify an operation."""

    actor_id: str
    shell_id: str
    session_id: str | None = None
    allowed_tool_packs: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ConsequentialActionRequest:
    """Structured request for Guardian review before consequential execution."""

    request_id: str
    intent_id: str | None
    input_id: str | None
    actor_id: str
    shell_id: str
    action_type: ConsequentialActionType
    target_ref: str | None
    requested_tool_pack: str | None
    risk_class: str
    typed_args: Mapping[str, Any] = field(default_factory=dict)
    evidence_refs: Sequence[str] = field(default_factory=tuple)
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class GuardianDecision:
    """Guardian decision identity for consequential execution and audit."""

    decision_id: str
    request_id: str | None
    intent_id: str | None
    input_id: str | None
    actor_id: str
    shell_id: str
    action_type: ConsequentialActionType
    target_ref: str | None
    risk_class: str
    status: GuardianDecisionStatus
    approval_level: str | None
    allowed_tool_packs: Sequence[str] = field(default_factory=tuple)
    constraints: Mapping[str, Any] = field(default_factory=dict)
    evidence_refs: Sequence[str] = field(default_factory=tuple)
    policy_version: str | None = None
    created_at: str = ""
    expires_at: str | None = None
    decided_at: str | None = None
    decided_by: str | None = None
    reason: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class GuardianDecisionRef:
    """Small reference carried by downstream events and execution requests."""

    decision_id: str
    status: GuardianDecisionStatus
    expires_at: str | None = None


class GuardianProtocol(Protocol):
    """Guardian is the mandatory syscall gate for external action."""

    def evaluate_action(self, request: ConsequentialActionRequest) -> GuardianDecision:
        """Evaluate a consequential action request before execution."""
        ...

    def classify_model_call(self, request: Any, context: GuardianContext) -> GuardianDecision:
        """Classify a model request before the Harness calls a model provider."""
        ...

    def classify_tool_call(self, tool_call: Any, context: GuardianContext) -> GuardianDecision:
        """Classify a tool call before any driver or tool pack executes it."""
        ...

    def require_approval(self, decision: GuardianDecision, context: GuardianContext) -> GuardianDecision:
        """Create or refresh approval state for an approval-required decision."""
        ...

    def record_decision(self, decision: GuardianDecision) -> None:
        """Record a Guardian decision before any approved execution proceeds."""
        ...
