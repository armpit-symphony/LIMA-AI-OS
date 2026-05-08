"""Audit and runtime event contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Literal, Mapping, Sequence


class AuditEventType(str, Enum):
    HUMAN_INPUT = "human_input"
    INTENT_COMPILED = "intent_compiled"
    CLARIFICATION_REQUESTED = "clarification_requested"
    GUARDIAN_DECISION = "guardian_decision"
    APPROVAL_RECORDED = "approval_recorded"
    POLICY_EVALUATED = "policy_evaluated"
    TOOL_EXPOSURE_DECIDED = "tool_exposure_decided"
    MODEL_CALL_PLANNED = "model_call_planned"
    MODEL_CALL_COMPLETED = "model_call_completed"
    TOOL_CALL_PLANNED = "tool_call_planned"
    TOOL_CALL_COMPLETED = "tool_call_completed"
    DRIVER_COMMAND_PLANNED = "driver_command_planned"
    DRIVER_COMMAND_COMPLETED = "driver_command_completed"
    TERMINAL_COMMAND_PLANNED = "terminal_command_planned"
    TERMINAL_COMMAND_COMPLETED = "terminal_command_completed"
    ROBOT_ACTION_PLANNED = "robot_action_planned"
    ROBOT_ACTION_COMPLETED = "robot_action_completed"
    TASK_CREATED = "task_created"
    TASK_UPDATED = "task_updated"
    SCHEDULED_ACTION_REQUESTED = "scheduled_action_requested"
    SCHEDULED_ACTION_EXECUTED = "scheduled_action_executed"
    RESULT_RECORDED = "result_recorded"
    AUDIT_WARNING = "audit_warning"
    AUDIT_ERROR = "audit_error"
    LINEAGE_CLOSED = "lineage_closed"


class AuditStatus(str, Enum):
    RECEIVED = "received"
    PLANNED = "planned"
    APPROVED = "approved"
    DENIED = "denied"
    ESCALATED = "escalated"
    NEEDS_CONFIRMATION = "needs_confirmation"
    NEEDS_APPROVAL = "needs_approval"
    EXECUTING = "executing"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELED = "canceled"
    EXPIRED = "expired"
    REVOKED = "revoked"
    SUPERSEDED = "superseded"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class AuditLineageRecord:
    lineage_id: str
    root_event_id: str | None
    latest_event_id: str | None
    input_id: str | None
    intent_id: str | None
    decision_id: str | None
    approval_id: str | None
    policy_decision_id: str | None
    exposure_id: str | None
    execution_id: str | None
    actor_id: str
    shell_id: str
    risk_class: str | None
    status: AuditStatus | str
    created_at: str
    updated_at: str | None = None
    closed_at: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SpineAuditEvent:
    event_id: str
    lineage_id: str
    event_type: AuditEventType | str
    status: AuditStatus | str
    timestamp: str
    actor_id: str
    shell_id: str
    input_id: str | None = None
    intent_id: str | None = None
    decision_id: str | None = None
    approval_id: str | None = None
    policy_decision_id: str | None = None
    exposure_id: str | None = None
    execution_id: str | None = None
    parent_event_id: str | None = None
    root_event_id: str | None = None
    action_type: str | None = None
    target_ref: str | None = None
    tool_pack: str | None = None
    selected_tools: Sequence[str] = field(default_factory=tuple)
    risk_class: str | None = None
    approval_level: str | None = None
    policy_version: str | None = None
    evidence_refs: Sequence[str] = field(default_factory=tuple)
    result_ref: str | None = None
    error_ref: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


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
class ApprovalAuditEvent(AuditEvent):
    approval_id: str = ""
    approval_level: str | None = None
    approval_method: str | None = None
    status: str = ""
    risk_class: str = ""
    action_type: str | None = None
    target_ref: str | None = None
    tool_pack: str | None = None
    selected_tools: tuple[str, ...] = ()
    policy_version: str | None = None


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
