"""Contract-shape tests for approval metadata."""


def test_approval_contract_imports() -> None:
    from lima.contracts import (
        ApprovalAuditEvent,
        ApprovalMetadata,
        ApprovalMethod,
        ApprovalProtocol,
        ApprovalScope,
        ApprovalStatus,
    )

    assert ApprovalStatus.PENDING.value == "pending"
    assert ApprovalStatus.APPROVED.value == "approved"
    assert ApprovalStatus.DENIED.value == "denied"
    assert ApprovalStatus.EXPIRED.value == "expired"
    assert ApprovalStatus.REVOKED.value == "revoked"
    assert ApprovalStatus.SUPERSEDED.value == "superseded"
    assert ApprovalMethod.CHAT_CONFIRMATION.value == "chat_confirmation"
    assert ApprovalMethod.VOICE_CONFIRMATION.value == "voice_confirmation"
    assert ApprovalMethod.UI_BUTTON.value == "ui_button"
    assert ApprovalMethod.OPERATOR_PIN.value == "operator_pin"
    assert ApprovalMethod.HARDWARE_KEY.value == "hardware_key"
    assert ApprovalMethod.SIGNED_TOKEN.value == "signed_token"
    assert ApprovalMethod.BREAKGLASS.value == "breakglass"
    assert ApprovalMethod.DELEGATED_ADMIN.value == "delegated_admin"
    assert ApprovalMethod.POLICY_AUTO_APPROVAL.value == "policy_auto_approval"
    assert ApprovalMethod.EXTERNAL_SYSTEM.value == "external_system"
    assert ApprovalMethod.UNKNOWN.value == "unknown"
    assert all(
        item is not None
        for item in (
            ApprovalAuditEvent,
            ApprovalMetadata,
            ApprovalProtocol,
            ApprovalScope,
        )
    )


def test_approval_metadata_contracts_instantiate() -> None:
    from datetime import datetime, timezone

    from lima.contracts import (
        ApprovalAuditEvent,
        ApprovalMetadata,
        ApprovalMethod,
        ApprovalProtocol,
        ApprovalScope,
        ApprovalStatus,
    )

    scope = ApprovalScope(
        decision_id="decision-1",
        actor_id="operator-1",
        shell_id="sparkbot",
        action_type="terminal_command",
        target_ref="terminal:session-1",
        tool_pack="terminal",
        selected_tools=("terminal_send",),
        risk_class="critical",
        constraints={"dry_run_required": True},
        expires_at="2026-05-08T00:05:00Z",
        policy_version="phase-0.11",
    )
    approval = ApprovalMetadata(
        approval_id="approval-1",
        decision_id=scope.decision_id,
        input_id="input-1",
        intent_id="intent-1",
        actor_id=scope.actor_id,
        shell_id=scope.shell_id,
        approved_by="operator-1",
        approval_level="operator_pin",
        approval_method=ApprovalMethod.OPERATOR_PIN,
        status=ApprovalStatus.APPROVED,
        risk_class=scope.risk_class,
        action_type=scope.action_type,
        target_ref=scope.target_ref,
        tool_pack=scope.tool_pack,
        selected_tools=scope.selected_tools,
        constraints=scope.constraints,
        evidence_refs=("pin_challenge_ref",),
        policy_version=scope.policy_version,
        created_at="2026-05-08T00:00:00Z",
        expires_at=scope.expires_at,
        reason="Terminal command requires operator approval.",
    )
    audit_event = ApprovalAuditEvent(
        event_id="approval-event-1",
        actor_id=approval.actor_id,
        shell_id=approval.shell_id,
        event_type="approval.metadata",
        created_at=datetime(2026, 5, 8, tzinfo=timezone.utc),
        decision_id=approval.decision_id,
        intent_id=approval.intent_id,
        input_id=approval.input_id,
        approval_id=approval.approval_id,
        approval_level=approval.approval_level,
        approval_method=str(approval.approval_method.value),
        status=approval.status.value,
        risk_class=approval.risk_class,
        action_type=approval.action_type,
        target_ref=approval.target_ref,
        tool_pack=approval.tool_pack,
        selected_tools=tuple(approval.selected_tools),
        policy_version=approval.policy_version,
    )
    public_callables = {
        name
        for name, value in ApprovalProtocol.__dict__.items()
        if not name.startswith("_") and callable(value)
    }

    assert approval.decision_id == scope.decision_id
    assert approval.status is ApprovalStatus.APPROVED
    assert approval.approval_method is ApprovalMethod.OPERATOR_PIN
    assert approval.expires_at == scope.expires_at
    assert audit_event.approval_id == approval.approval_id
    assert audit_event.decision_id == approval.decision_id
    assert audit_event.selected_tools == ("terminal_send",)
    assert public_callables == {"describe_required_approval", "record_approval"}
    assert "execute" not in public_callables
