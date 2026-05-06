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


@dataclass(frozen=True)
class ApprovalEvent(AuditEvent):
    approval_id: str = ""
    status: Literal["pending", "approved", "denied", "expired"] = "pending"
    decision_id: str | None = None


@dataclass(frozen=True)
class ModelCallEvent(AuditEvent):
    model: str = ""
    route: str | None = None
    token_estimate: int | None = None
    decision_id: str | None = None


@dataclass(frozen=True)
class ToolCallEvent(AuditEvent):
    tool_name: str = ""
    decision_id: str | None = None
    approval_id: str | None = None
    result_status: str | None = None


@dataclass(frozen=True)
class DriverEvent(AuditEvent):
    driver_id: str = ""
    capability: str = ""
    decision_id: str | None = None
    telemetry_ref: str | None = None
