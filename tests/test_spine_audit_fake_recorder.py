"""Tests for the in-memory Spine/Audit fake recorder."""

from datetime import datetime, timezone


def _public_callables(provider: type) -> set[str]:
    return {
        name
        for name, value in provider.__dict__.items()
        if not name.startswith("_") and callable(value)
    }


def _event(event_id: str, lineage_id: str = "lineage-1", status=None):
    from lima.contracts import AuditEventType, AuditStatus, SpineEvent

    return SpineEvent(
        event_id=event_id,
        event_type=AuditEventType.GUARDIAN_DECISION,
        source="fake-test",
        created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        lineage_id=lineage_id,
        status=status or AuditStatus.RECEIVED,
        actor_id="actor-1",
        shell_id="test-shell",
        input_id="input-1",
        intent_id="intent-1",
        decision_id="decision-1",
        approval_id="approval-1",
        policy_decision_id="policy-decision-1",
        risk_class="high",
        evidence_refs=("evidence-ref-1",),
        redacted_summary="Redacted contract-test event.",
    )


def _lineage(lineage_id: str = "lineage-1", status=None):
    from lima.contracts import AuditLineageRecord, AuditStatus

    return AuditLineageRecord(
        lineage_id=lineage_id,
        root_event_id="event-root",
        latest_event_id="event-latest",
        input_id="input-1",
        intent_id="intent-1",
        decision_id="decision-1",
        approval_id="approval-1",
        policy_decision_id="policy-decision-1",
        exposure_id="exposure-1",
        execution_id=None,
        actor_id="actor-1",
        shell_id="test-shell",
        risk_class="high",
        status=status or AuditStatus.BLOCKED,
        created_at="2026-01-01T00:00:00Z",
        redacted_summary="Redacted lineage summary.",
        metadata={"test_only": True},
    )


def test_fake_recorder_records_spine_event_by_lineage() -> None:
    from lima.guardian import FakeSpineAuditRecorder

    event = _event("event-1")
    recorder = FakeSpineAuditRecorder()

    assert recorder.append_event(event) is event
    assert recorder.get_lineage(event.lineage_id) == (event,)
    assert recorder.list_events() == (event,)


def test_fake_recorder_records_audit_lineage_record() -> None:
    from lima.guardian import FakeSpineAuditRecorder

    lineage = _lineage()
    recorder = FakeSpineAuditRecorder()
    recorder.record_lineage(lineage)

    assert recorder.get_lineage_record(lineage.lineage_id) is lineage
    assert recorder.get_lineage_record("missing-lineage") is None
    assert recorder.list_lineages() == (lineage,)


def test_denied_blocked_and_failed_events_remain_auditable() -> None:
    from lima.contracts import AuditStatus
    from lima.guardian import FakeSpineAuditRecorder

    denied = _event("event-denied", status=AuditStatus.DENIED)
    blocked = _event("event-blocked", status=AuditStatus.BLOCKED)
    failed = _event("event-failed", status=AuditStatus.FAILED)
    recorder = FakeSpineAuditRecorder()

    for event in (denied, blocked, failed):
        recorder.append_event(event)

    assert recorder.get_lineage("lineage-1") == (denied, blocked, failed)


def test_privacy_metadata_is_preserved_without_raw_content() -> None:
    from lima.contracts import (
        AuditEventType,
        AuditStatus,
        DataReference,
        PrivacyClass,
        RedactionClass,
        RetentionClass,
        SpineEvent,
        VisibilityClass,
    )
    from lima.guardian import FakeSpineAuditRecorder

    content_ref = DataReference(
        ref_id="content-ref-1",
        ref_type="summary",
        uri=None,
        privacy_class=PrivacyClass.PRIVATE,
        redaction_class=RedactionClass.SUMMARY_ONLY,
        retention_class=RetentionClass.SHORT,
        visibility_class=VisibilityClass.OPERATOR_VIEW,
        content_hash="hash-ref-only",
        created_at="2026-01-01T00:00:00Z",
    )
    event = SpineEvent(
        event_id="event-private",
        event_type=AuditEventType.HUMAN_INPUT,
        source="fake-test",
        created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        lineage_id="lineage-private",
        status=AuditStatus.RECEIVED,
        actor_id="actor-1",
        shell_id="test-shell",
        privacy_class=PrivacyClass.PRIVATE.value,
        redaction_class=RedactionClass.SUMMARY_ONLY.value,
        retention_class=RetentionClass.SHORT.value,
        visibility_class=VisibilityClass.OPERATOR_VIEW.value,
        content_refs=(content_ref,),
        evidence_refs=("evidence-ref-1",),
        redacted_summary="Private input summarized for test.",
    )
    recorder = FakeSpineAuditRecorder()
    recorder.append_event(event)
    recorded = recorder.get_lineage("lineage-private")[0]

    assert recorded.content_refs == (content_ref,)
    assert recorded.redacted_summary == "Private input summarized for test."
    assert recorded.privacy_class == PrivacyClass.PRIVATE.value
    assert recorded.contains_secret is False


def test_fake_recorder_records_closure_and_tasks_in_memory() -> None:
    from lima.contracts import TaskRecord
    from lima.guardian import FakeSpineAuditRecorder

    task = TaskRecord(
        task_id="task-1",
        title="Contract test task",
        status="blocked",
        created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        updated_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        lineage_ids=("lineage-1",),
    )
    recorder = FakeSpineAuditRecorder()

    assert recorder.create_task(task) == task.task_id
    recorder.close_lineage("lineage-1", "blocked")

    assert recorder.get_task(task.task_id) is task
    assert recorder.list_tasks() == (task,)
    assert recorder.get_lineage_closure("lineage-1") == "blocked"


def test_fake_recorder_forbidden_persistence_and_execution_methods_are_absent() -> None:
    from lima.guardian import FakeSpineAuditRecorder

    forbidden_methods = {
        "execute",
        "enforce",
        "approve",
        "deny",
        "call_tool",
        "call_model",
        "call_driver",
        "persist",
        "save_to_db",
        "write_file",
        "open_db",
        "upload",
        "send",
    }

    assert _public_callables(FakeSpineAuditRecorder).isdisjoint(forbidden_methods)
