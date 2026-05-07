"""Audit and runtime event contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Literal


@dataclass(frozen=True)
class AuditEvent:
    event_id: str
    actor_id: str
    shell_id: str
    event_type: str
    created_at: datetime
    metadata: dict[str, Any] = field(default_factory=dict)
    correlation_id: str | None = None
    decision_id: str | None = None
    intent_id: str | None = None
    input_id: str | None = None


@dataclass(frozen=True)
class DecisionAuditEvent(AuditEvent):
    action_type: str = ""
    target_ref: str | None = None
    risk_class: str = ""
    result_status: str | None = None
    evidence_refs: tuple[str, ...] = ()


@dataclass(frozen=True)
class ApprovalEvent(AuditEvent):
    approval_id: str = ""
    status: Literal["pending", "approved", "denied", "expired"] = "pending"


@dataclass(frozen=True)
class ModelCallEvent(AuditEvent):
    model: str = ""
    route: str | None = None
    token_estimate: int | None = None


@dataclass(frozen=True)
class ToolCallEvent(AuditEvent):
    tool_name: str = ""
    approval_id: str | None = None
    result_status: str | None = None


@dataclass(frozen=True)
class DriverEvent(AuditEvent):
    driver_id: str = ""
    capability: str = ""
    telemetry_ref: str | None = None


@dataclass(frozen=True)
class TerminalEvent(AuditEvent):
    terminal_id: str = ""
    command_ref: str | None = None
    risk_class: str = "critical"
    result_status: str | None = None


@dataclass(frozen=True)
class ToolExposureAuditEvent(AuditEvent):
    exposure_id: str = ""
    allowed_packs: tuple[str, ...] = ()
    denied_packs: tuple[str, ...] = ()
    selected_tools: tuple[str, ...] = ()
    risk_class: str = ""
