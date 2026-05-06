"""Spine ledger contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Literal, Protocol


@dataclass(frozen=True)
class SpineEvent:
    event_id: str
    event_type: str
    source: str
    created_at: datetime
    payload: dict[str, Any] = field(default_factory=dict)
    correlation_id: str | None = None


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

    def append_event(self, event: SpineEvent) -> str:
        """Append an immutable event and return its event identifier."""
        ...

    def create_task(self, task: TaskRecord) -> str:
        """Create a task record in the ledger."""
        ...

    def update_task(self, task: TaskRecord) -> None:
        """Update task state."""
        ...

    def get_lineage(self, task_id: str) -> tuple[SpineEvent, ...]:
        """Return events linked to a task."""
        ...
