"""Human intent contracts for the LIMA Runtime control plane."""

from __future__ import annotations

from dataclasses import dataclass, field
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


@dataclass(frozen=True)
class HumanInput:
    input_id: str
    source: HumanInputSource
    actor_id: str
    shell_id: str
    content_ref: str | None = None
    raw_text: str | None = None
    locale: str = "en"
    confidence: float | None = None
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
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ClarificationRequest:
    clarification_id: str
    intent_id: str
    question: str
    choices: Sequence[str] = field(default_factory=tuple)
    reason: str | None = None
    blocking: bool = True


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
