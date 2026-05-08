"""Contract-shape tests for Spine/Audit lineage."""


def test_audit_lineage_contract_imports() -> None:
    from lima.contracts import (
        AuditEventType,
        AuditLineageRecord,
        AuditStatus,
        SpineAuditEvent,
        SpineEvent,
        SpineProtocol,
    )

    assert AuditEventType.HUMAN_INPUT.value == "human_input"
    assert AuditEventType.GUARDIAN_DECISION.value == "guardian_decision"
    assert AuditEventType.TOOL_EXPOSURE_DECIDED.value == "tool_exposure_decided"
    assert AuditEventType.TERMINAL_COMMAND_COMPLETED.value == "terminal_command_completed"
    assert AuditEventType.ROBOT_ACTION_COMPLETED.value == "robot_action_completed"
    assert AuditEventType.LINEAGE_CLOSED.value == "lineage_closed"
    assert AuditStatus.RECEIVED.value == "received"
    assert AuditStatus.APPROVED.value == "approved"
    assert AuditStatus.DENIED.value == "denied"
    assert AuditStatus.BLOCKED.value == "blocked"
    assert AuditStatus.FAILED.value == "failed"
    assert AuditStatus.SUPERSEDED.value == "superseded"
    assert all(
        item is not None
        for item in (
            AuditLineageRecord,
            SpineAuditEvent,
            SpineEvent,
            SpineProtocol,
        )
    )


def test_spine_audit_lineage_contracts_instantiate() -> None:
    from datetime import datetime, timezone

    from lima.contracts import (
        AuditEventType,
        AuditLineageRecord,
        AuditStatus,
        SpineAuditEvent,
        SpineEvent,
        SpineProtocol,
    )

    lineage = AuditLineageRecord(
        lineage_id="lineage-1",
        root_event_id="event-root",
        latest_event_id="event-terminal-completed",
        input_id="input-1",
        intent_id="intent-1",
        decision_id="decision-1",
        approval_id="approval-1",
        policy_decision_id="policy-decision-1",
        exposure_id="exposure-1",
        execution_id="execution-1",
        actor_id="operator-1",
        shell_id="sparkbot",
        risk_class="critical",
        status=AuditStatus.BLOCKED,
        created_at="2026-05-08T00:00:00Z",
        updated_at="2026-05-08T00:01:00Z",
        metadata={"redaction": "refs_only"},
    )
    audit_event = SpineAuditEvent(
        event_id="event-terminal-completed",
        lineage_id=lineage.lineage_id,
        event_type=AuditEventType.TERMINAL_COMMAND_COMPLETED,
        status=AuditStatus.BLOCKED,
        timestamp="2026-05-08T00:01:00Z",
        actor_id=lineage.actor_id,
        shell_id=lineage.shell_id,
        input_id=lineage.input_id,
        intent_id=lineage.intent_id,
        decision_id=lineage.decision_id,
        approval_id=lineage.approval_id,
        policy_decision_id=lineage.policy_decision_id,
        exposure_id=lineage.exposure_id,
        execution_id=lineage.execution_id,
        parent_event_id="event-terminal-planned",
        root_event_id=lineage.root_event_id,
        action_type="terminal_command",
        target_ref="terminal:session-1",
        tool_pack="terminal",
        selected_tools=("terminal_send",),
        risk_class=lineage.risk_class,
        approval_level="operator_pin",
        policy_version="phase-0.12",
        evidence_refs=("transcript-ref", "approval-ref"),
        result_ref="result-ref",
    )
    spine_event = SpineEvent(
        event_id=audit_event.event_id,
        event_type=audit_event.event_type,
        source="audit",
        created_at=datetime(2026, 5, 8, tzinfo=timezone.utc),
        lineage_id=audit_event.lineage_id,
        status=audit_event.status,
        actor_id=audit_event.actor_id,
        shell_id=audit_event.shell_id,
        input_id=audit_event.input_id,
        intent_id=audit_event.intent_id,
        decision_id=audit_event.decision_id,
        approval_id=audit_event.approval_id,
        policy_decision_id=audit_event.policy_decision_id,
        exposure_id=audit_event.exposure_id,
        execution_id=audit_event.execution_id,
        parent_event_id=audit_event.parent_event_id,
        root_event_id=audit_event.root_event_id,
        action_type=audit_event.action_type,
        target_ref=audit_event.target_ref,
        tool_pack=audit_event.tool_pack,
        selected_tools=audit_event.selected_tools,
        risk_class=audit_event.risk_class,
        approval_level=audit_event.approval_level,
        policy_version=audit_event.policy_version,
        evidence_refs=audit_event.evidence_refs,
        result_ref=audit_event.result_ref,
    )
    public_callables = {
        name
        for name, value in SpineProtocol.__dict__.items()
        if not name.startswith("_") and callable(value)
    }

    assert lineage.lineage_id == audit_event.lineage_id
    assert audit_event.decision_id == "decision-1"
    assert audit_event.approval_id == "approval-1"
    assert audit_event.selected_tools == ("terminal_send",)
    assert spine_event.lineage_id == lineage.lineage_id
    assert spine_event.decision_id == audit_event.decision_id
    assert spine_event.parent_event_id == "event-terminal-planned"
    assert spine_event.root_event_id == "event-root"
    assert public_callables == {
        "append_event",
        "create_task",
        "update_task",
        "get_lineage",
        "close_lineage",
    }
    assert "execute" not in public_callables
