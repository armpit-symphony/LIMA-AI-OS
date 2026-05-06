"""Human intent contracts for the LIMA Runtime control plane."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Mapping, Protocol, Sequence


class HumanInputSource(str, Enum):
    TEXT = "text"
    VOICE = "voice"
    CONSOLE = "console"
    GESTURE = "gesture"
    FUTURE_BCI = "future_bci"


class RiskClass(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class IntentStatus(str, Enum):
    RECEIVED = "received"
    NORMALIZED = "normalized"
    NEEDS_CLARIFICATION = "needs_clarification"
    COMPILED = "compiled"
    SUBMITTED_TO_GUARDIAN = "submitted_to_guardian"
    APPROVED = "approved"
    DENIED = "denied"
    ESCALATED = "escalated"
    EXPIRED = "expired"
    SUPERSEDED = "superseded"


class IntentType(str, Enum):
    ASK_INFORMATION = "ask_information"
    CREATE_PLAN = "create_plan"
    DRAFT_CONTENT = "draft_content"
    SCHEDULE_TASK = "schedule_task"
    RUN_TOOL = "run_tool"
    OPERATE_FILE = "operate_file"
    BROWSE_WEB = "browse_web"
    SEND_MESSAGE = "send_message"
    CONTROL_ROBOT = "control_robot"
    ADMINISTER_SYSTEM = "administer_system"
    APPROVE_ACTION = "approve_action"
    DENY_ACTION = "deny_action"
    UNKNOWN = "unknown"


class ApprovalLevel(str, Enum):
    NONE = "none"
    CONFIRM = "confirm"
    GUARDIAN_REVIEW = "guardian_review"
    OPERATOR_PIN = "operator_pin"
    BREAKGLASS = "breakglass"


@dataclass(frozen=True)
class EvidenceRequirement:
    evidence_id: str
    kind: str
    description: str
    required: bool = True
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class HumanInput:
    input_id: str
    source: HumanInputSource
    actor_id: str
    shell_id: str
    content_ref: str | None = None
    raw_text: str | None = None
    timestamp: datetime | None = None
    locale: str = "en"
    confidence: float | None = None
    privacy_class: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class IntentEnvelope:
    intent_id: str
    source_input_id: str
    actor_id: str
    shell_id: str
    normalized_text: str
    intent_type: str
    typed_args: Mapping[str, Any] = field(default_factory=dict)
    confidence: float = 0.0
    risk_class: RiskClass = RiskClass.MEDIUM
    ambiguity_flags: Sequence[str] = field(default_factory=tuple)
    required_evidence: Sequence[str] = field(default_factory=tuple)
    required_approval_level: str | None = None
    proposed_tool_packs: Sequence[str] = field(default_factory=tuple)
    created_at: datetime | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ClarificationRequest:
    clarification_id: str
    intent_id: str
    question: str
    choices: Sequence[str] = field(default_factory=tuple)
    reason: str | None = None
    blocking: bool = True


@dataclass(frozen=True)
class IntentCompilationResult:
    input: HumanInput
    intent: IntentEnvelope | None = None
    clarification: ClarificationRequest | None = None
    status: IntentStatus = IntentStatus.RECEIVED
    warnings: Sequence[str] = field(default_factory=tuple)
    metadata: Mapping[str, Any] = field(default_factory=dict)


class IntentCompilerProtocol(Protocol):
    """Compile human input into typed intent without executing or approving it."""

    def compile(self, input: HumanInput, context: Mapping[str, Any]) -> IntentEnvelope:
        """Normalize human input into a typed intent envelope for Guardian."""
        ...

    def clarify(self, intent: IntentEnvelope) -> ClarificationRequest | None:
        """Return a blocking clarification request for ambiguous intent."""
        ...

    def revise(self, intent: IntentEnvelope, user_reply: HumanInput) -> IntentEnvelope:
        """Revise an intent envelope using a follow-up human reply."""
        ...
