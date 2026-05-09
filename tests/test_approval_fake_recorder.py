"""Tests for the in-memory approval metadata fake recorder."""


def _public_callables(provider: type) -> set[str]:
    return {
        name
        for name, value in provider.__dict__.items()
        if not name.startswith("_") and callable(value)
    }


def _scope(decision_id: str = "decision-1"):
    from lima.contracts import ApprovalScope

    return ApprovalScope(
        decision_id=decision_id,
        actor_id="actor-1",
        shell_id="test-shell",
        action_type="terminal_command",
        target_ref="terminal:session-1",
        tool_pack="terminal",
        selected_tools=("terminal_send",),
        risk_class="critical",
        constraints={"metadata_only": True},
        expires_at="2026-01-01T00:05:00Z",
        policy_version="fake-policy-v1",
    )


def _approval(
    approval_id: str = "approval-1",
    decision_id: str = "decision-1",
    method=None,
    status=None,
):
    from lima.contracts import ApprovalMetadata, ApprovalMethod, ApprovalStatus

    return ApprovalMetadata(
        approval_id=approval_id,
        decision_id=decision_id,
        input_id="input-1",
        intent_id="intent-1",
        actor_id="actor-1",
        shell_id="test-shell",
        approved_by=None,
        approval_level="operator_pin",
        approval_method=method or ApprovalMethod.UI_BUTTON,
        status=status or ApprovalStatus.PENDING,
        risk_class="critical",
        action_type="terminal_command",
        target_ref="terminal:session-1",
        tool_pack="terminal",
        selected_tools=("terminal_send",),
        constraints={"metadata_only": True},
        evidence_refs=("approval-evidence-ref",),
        policy_version="fake-policy-v1",
        created_at="2026-01-01T00:00:00Z",
        expires_at="2026-01-01T00:05:00Z",
        reason="Fake approval metadata for contract tests.",
        metadata={"test_only": True},
    )


def test_fake_recorder_records_approval_metadata() -> None:
    from lima.guardian import FakeApprovalRecorder

    approval = _approval()
    recorder = FakeApprovalRecorder()
    recorder.record_approval(approval)

    assert recorder.get_approval(approval.approval_id) is approval
    assert recorder.get_approval("missing-approval") is None
    assert recorder.list_approvals() == (approval,)


def test_describe_required_approval_records_scope_without_enforcement() -> None:
    from lima.guardian import FakeApprovalRecorder

    scope = _scope()
    recorder = FakeApprovalRecorder()
    required = recorder.describe_required_approval(scope)

    assert required is None
    assert recorder.get_scope(scope.decision_id) is scope
    assert recorder.list_scopes() == (scope,)


def test_describe_required_approval_returns_configured_metadata() -> None:
    from lima.guardian import FakeApprovalRecorder

    scope = _scope()
    approval = _approval(decision_id=scope.decision_id)
    recorder = FakeApprovalRecorder(approvals=(approval,))

    assert recorder.describe_required_approval(scope) is approval
    assert recorder.get_scope(scope.decision_id) is scope


def test_approval_metadata_does_not_replace_guardian_decision() -> None:
    from lima.contracts import ApprovalMetadata, GuardianDecision
    from lima.guardian import FakeApprovalRecorder

    approval = _approval()
    recorder = FakeApprovalRecorder()
    recorder.record_approval(approval)
    recorded = recorder.get_approval(approval.approval_id)

    assert isinstance(recorded, ApprovalMetadata)
    assert not isinstance(recorded, GuardianDecision)
    assert recorded.decision_id == "decision-1"


def test_breakglass_style_metadata_is_recorded_only() -> None:
    from lima.contracts import ApprovalMethod, ApprovalStatus
    from lima.guardian import FakeApprovalRecorder

    approval = _approval(
        approval_id="approval-breakglass-1",
        method=ApprovalMethod.BREAKGLASS,
        status=ApprovalStatus.PENDING,
    )
    recorder = FakeApprovalRecorder()
    recorder.record_approval(approval)

    forbidden_methods = {"open_live_session", "bypass", "execute", "enforce"}

    assert recorder.get_approval(approval.approval_id) is approval
    assert recorder.get_approval(approval.approval_id).approval_method is ApprovalMethod.BREAKGLASS
    assert _public_callables(FakeApprovalRecorder).isdisjoint(forbidden_methods)


def test_fake_approval_recorder_forbidden_live_methods_are_absent() -> None:
    from lima.guardian import FakeApprovalRecorder

    forbidden_methods = {
        "execute",
        "enforce",
        "verify_pin",
        "check_pin",
        "login",
        "approve_and_execute",
        "authorize_execution",
        "open_breakglass",
        "open_live_session",
        "bypass",
        "issue_token",
        "sign_token",
    }

    assert _public_callables(FakeApprovalRecorder).isdisjoint(forbidden_methods)
