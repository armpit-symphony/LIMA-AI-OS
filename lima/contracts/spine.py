"""Spine ledger contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Literal, Protocol, Sequence

from .events import AuditEventType, AuditStatus
from .privacy import DataReference


@dataclass(frozen=True)
class SpineEvent:
    event_id: str
    event_type: AuditEventType | str
    source: str
    created_at: datetime
    payload: dict[str, Any] = field(default_factory=dict)
    correlation_id: str | None = None
    lineage_id: str = ""
    status: AuditStatus | str = AuditStatus.UNKNOWN
    actor_id: str | None = None
    shell_id: str | None = None
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
    privacy_class: str | None = None
    redaction_class: str | None = None
    retention_class: str | None = None
    visibility_class: str | None = None
    content_refs: Sequence[DataReference] = field(default_factory=tuple)
    secret_refs: Sequence[str] = field(default_factory=tuple)
    redacted_summary: str | None = None
    contains_secret: bool = False
    contains_biometric: bool = False
    contains_safety_critical: bool = False
    data_subject_ref: str | None = None
    retention_expires_at: str | None = None


TaskStatus = Literal["candidate", "open", "blocked", "approval_waiting", "done", "archived"]


@dataclass(frozen=True)
class TaskRecord:
    task_id: str
    title: str
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    owner_id: str | None = None
    lineage_ids: tuple[str, ...] = ()


class SpineProtocol(Protocol):
    """Task/event/process ledger surface."""

    def append_event(self, event: SpineEvent) -> SpineEvent:
        """Append an immutable event record without executing actions."""
        ...

    def create_task(self, task: TaskRecord) -> str:
        """Create a task record in the ledger."""
        ...

    def update_task(self, task: TaskRecord) -> None:
        """Update task state."""
        ...

    def get_lineage(self, lineage_id: str) -> Sequence[SpineEvent]:
        """Return events linked to a lineage identifier."""
        ...

    def close_lineage(self, lineage_id: str, status: str) -> None:
        """Record lineage closure without implementing persistence."""
        ...
