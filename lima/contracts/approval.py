"""Approval metadata contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Protocol, Sequence


class ApprovalStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    DENIED = "denied"
    EXPIRED = "expired"
    REVOKED = "revoked"
    SUPERSEDED = "superseded"


class ApprovalMethod(str, Enum):
    CHAT_CONFIRMATION = "chat_confirmation"
    VOICE_CONFIRMATION = "voice_confirmation"
    UI_BUTTON = "ui_button"
    OPERATOR_PIN = "operator_pin"
    HARDWARE_KEY = "hardware_key"
    SIGNED_TOKEN = "signed_token"
    BREAKGLASS = "breakglass"
    DELEGATED_ADMIN = "delegated_admin"
    POLICY_AUTO_APPROVAL = "policy_auto_approval"
    EXTERNAL_SYSTEM = "external_system"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class ApprovalMetadata:
    approval_id: str
    decision_id: str
    input_id: str | None
    intent_id: str | None
    actor_id: str
    shell_id: str
    approved_by: str | None
    approval_level: str | None
    approval_method: ApprovalMethod | str
    status: ApprovalStatus
    risk_class: str
    action_type: str | None
    target_ref: str | None
    tool_pack: str | None
    selected_tools: Sequence[str] = field(default_factory=tuple)
    constraints: Mapping[str, Any] = field(default_factory=dict)
    evidence_refs: Sequence[str] = field(default_factory=tuple)
    policy_version: str | None = None
    created_at: str = ""
    expires_at: str | None = None
    revoked_at: str | None = None
    superseded_by: str | None = None
    reason: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ApprovalScope:
    decision_id: str
    actor_id: str
    shell_id: str
    action_type: str | None
    target_ref: str | None
    tool_pack: str | None
    selected_tools: Sequence[str] = field(default_factory=tuple)
    risk_class: str = "high"
    constraints: Mapping[str, Any] = field(default_factory=dict)
    expires_at: str | None = None
    policy_version: str | None = None


class ApprovalProtocol(Protocol):
    """Describe and record approval metadata without executing actions."""

    def describe_required_approval(self, scope: ApprovalScope) -> ApprovalMetadata | None:
        """Return required approval metadata for a scope, if already known."""
        ...

    def record_approval(self, approval: ApprovalMetadata) -> None:
        """Record approval evidence without executing the approved action."""
        ...
