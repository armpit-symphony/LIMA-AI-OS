"""In-memory Spine/Audit recorder fakes for contract validation."""

from __future__ import annotations

from collections.abc import Sequence

from lima.contracts.events import AuditLineageRecord
from lima.contracts.spine import SpineEvent, SpineProtocol, TaskRecord


class FakeSpineAuditRecorder(SpineProtocol):
    """In-memory Spine/Audit recorder for tests."""

    def __init__(
        self,
        events: Sequence[SpineEvent] = (),
        lineages: Sequence[AuditLineageRecord] = (),
        tasks: Sequence[TaskRecord] = (),
    ) -> None:
        self._events: list[SpineEvent] = list(events)
        self._lineages = {record.lineage_id: record for record in lineages}
        self._tasks = {task.task_id: task for task in tasks}
        self._lineage_closures: dict[str, str] = {}

    def append_event(self, event: SpineEvent) -> SpineEvent:
        self._events.append(event)
        return event

    def create_task(self, task: TaskRecord) -> str:
        self._tasks[task.task_id] = task
        return task.task_id

    def update_task(self, task: TaskRecord) -> None:
        self._tasks[task.task_id] = task

    def get_lineage(self, lineage_id: str) -> Sequence[SpineEvent]:
        return tuple(event for event in self._events if event.lineage_id == lineage_id)

    def close_lineage(self, lineage_id: str, status: str) -> None:
        self._lineage_closures[lineage_id] = status

    def record_lineage(self, record: AuditLineageRecord) -> None:
        self._lineages[record.lineage_id] = record

    def get_lineage_record(self, lineage_id: str) -> AuditLineageRecord | None:
        return self._lineages.get(lineage_id)

    def get_task(self, task_id: str) -> TaskRecord | None:
        return self._tasks.get(task_id)

    def get_lineage_closure(self, lineage_id: str) -> str | None:
        return self._lineage_closures.get(lineage_id)

    def list_events(self) -> Sequence[SpineEvent]:
        return tuple(self._events)

    def list_lineages(self) -> Sequence[AuditLineageRecord]:
        return tuple(self._lineages.values())

    def list_tasks(self) -> Sequence[TaskRecord]:
        return tuple(self._tasks.values())
