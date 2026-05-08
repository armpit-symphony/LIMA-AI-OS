"""Import validation for Phase 0 contracts."""


def test_public_contract_imports() -> None:
    import lima
    from lima import contracts
    from lima.contracts import (
        ApprovalEvent,
        ApprovalLevel,
        AuditEvent,
        ClarificationRequest,
        ConsequentialActionRequest,
        ConsequentialActionType,
        DecisionAuditEvent,
        DriverCapability,
        DriverCommand,
        DriverEvent,
        DriverProtocol,
        DriverResult,
        EvidenceRequirement,
        GuardianContext,
        GuardianDecision,
        GuardianDecisionRef,
        GuardianDecisionStatus,
        GuardianProtocol,
        HarnessProtocol,
        HumanInput,
        HumanInputSource,
        IntentCompilationResult,
        IntentCompilerProtocol,
        IntentEnvelope,
        IntentStatus,
        IntentType,
        RiskClass,
        ModelCallEvent,
        ModelRequest,
        ModelResponse,
        PolicyDecision,
        PolicyEvaluationContext,
        PolicyExposure,
        PolicyProtocol,
        ShellManifest,
        ShellProtocol,
        SpineEvent,
        SpineProtocol,
        StorageProtocol,
        TaskRecord,
        TerminalEvent,
        ToolCallEvent,
        ToolDefinition,
        ToolExposureAuditEvent,
        ToolExposureDecision,
        ToolExposureRequest,
        ToolPackManifest,
        ToolPackName,
        ToolPackProtocol,
        ToolPackRiskPolicy,
        ToolPackRiskRule,
        ShellToolScope,
    )

    assert lima.__all__ == ["contracts"]
    assert contracts.GuardianDecision is GuardianDecision
    assert all(
        item is not None
        for item in (
            ApprovalEvent,
            ApprovalLevel,
            AuditEvent,
            ClarificationRequest,
            ConsequentialActionRequest,
            ConsequentialActionType,
            DecisionAuditEvent,
            DriverCapability,
            DriverCommand,
            DriverEvent,
            DriverProtocol,
            DriverResult,
            EvidenceRequirement,
            GuardianContext,
            GuardianProtocol,
            GuardianDecisionRef,
            GuardianDecisionStatus,
            HarnessProtocol,
            HumanInput,
            HumanInputSource,
            IntentCompilationResult,
            IntentCompilerProtocol,
            IntentEnvelope,
            IntentStatus,
            IntentType,
            RiskClass,
            ModelCallEvent,
            ModelRequest,
            ModelResponse,
            PolicyDecision,
            PolicyEvaluationContext,
            PolicyExposure,
            PolicyProtocol,
            ShellManifest,
            ShellProtocol,
            SpineEvent,
            SpineProtocol,
            StorageProtocol,
            TaskRecord,
            TerminalEvent,
            ToolCallEvent,
            ToolDefinition,
            ToolExposureAuditEvent,
            ToolExposureDecision,
            ToolExposureRequest,
            ToolPackManifest,
            ToolPackName,
            ToolPackProtocol,
            ToolPackRiskPolicy,
            ToolPackRiskRule,
            ShellToolScope,
        )
    )


def test_intent_contracts_instantiate() -> None:
    from datetime import datetime, timezone

    from lima.contracts import (
        ApprovalLevel,
        ClarificationRequest,
        EvidenceRequirement,
        HumanInput,
        HumanInputSource,
        IntentCompilationResult,
        IntentEnvelope,
        IntentStatus,
        IntentType,
        RiskClass,
    )

    human_input = HumanInput(
        input_id="input-1",
        source=HumanInputSource.TEXT,
        actor_id="operator-1",
        shell_id="sparkbot",
        raw_text="Summarize the latest audit events.",
        timestamp=datetime(2026, 5, 6, tzinfo=timezone.utc),
        confidence=0.99,
        privacy_class="internal",
    )
    intent = IntentEnvelope(
        intent_id="intent-1",
        source_input_id=human_input.input_id,
        actor_id=human_input.actor_id,
        shell_id=human_input.shell_id,
        normalized_text="summarize latest audit events",
        intent_type=IntentType.ASK_INFORMATION.value,
        risk_class=RiskClass.LOW,
        required_evidence=("audit_window",),
        required_approval_level=ApprovalLevel.NONE.value,
        created_at=datetime(2026, 5, 6, tzinfo=timezone.utc),
    )
    clarification = ClarificationRequest(
        clarification_id="clarification-1",
        intent_id=intent.intent_id,
        question="Which audit window should be summarized?",
        choices=("last_hour", "today"),
    )
    evidence = EvidenceRequirement(
        evidence_id="audit_window",
        kind="time_range",
        description="Time window for audit summary.",
    )
    compilation = IntentCompilationResult(
        input=human_input,
        intent=intent,
        clarification=clarification,
        status=IntentStatus.NEEDS_CLARIFICATION,
        warnings=("missing_time_range",),
    )

    assert HumanInputSource.FUTURE_BCI.value == "future_bci"
    assert RiskClass.CRITICAL.value == "critical"
    assert IntentStatus.SUBMITTED_TO_GUARDIAN.value == "submitted_to_guardian"
    assert IntentType.CONTROL_ROBOT.value == "control_robot"
    assert ApprovalLevel.GUARDIAN_REVIEW.value == "guardian_review"
    assert human_input.privacy_class == "internal"
    assert evidence.required is True
    assert compilation.intent is intent
    assert intent.created_at == human_input.timestamp
    assert intent.source_input_id == human_input.input_id
    assert clarification.blocking is True


def test_intent_compiler_protocol_is_non_executing() -> None:
    from lima.contracts import IntentCompilerProtocol

    public_callables = {
        name
        for name, value in IntentCompilerProtocol.__dict__.items()
        if not name.startswith("_") and callable(value)
    }

    assert public_callables == {"compile", "clarify", "revise"}


def test_guardian_decision_contracts_instantiate() -> None:
    from datetime import datetime, timezone

    from lima.contracts import (
        ConsequentialActionRequest,
        ConsequentialActionType,
        DecisionAuditEvent,
        GuardianDecision,
        GuardianDecisionRef,
        GuardianDecisionStatus,
        GuardianProtocol,
        TerminalEvent,
    )

    request = ConsequentialActionRequest(
        request_id="request-1",
        intent_id="intent-1",
        input_id="input-1",
        actor_id="operator-1",
        shell_id="sparkbot",
        action_type=ConsequentialActionType.TERMINAL_COMMAND,
        target_ref="terminal:session-1",
        requested_tool_pack="terminal",
        risk_class="critical",
        typed_args={"command_ref": "cmd-ref-1"},
        evidence_refs=("transcript-1",),
    )
    decision = GuardianDecision(
        decision_id="decision-1",
        request_id=request.request_id,
        intent_id=request.intent_id,
        input_id=request.input_id,
        actor_id=request.actor_id,
        shell_id=request.shell_id,
        action_type=request.action_type,
        target_ref=request.target_ref,
        risk_class=request.risk_class,
        status=GuardianDecisionStatus.NEEDS_OPERATOR_PIN,
        approval_level="operator_pin",
        allowed_tool_packs=("terminal",),
        constraints={"dry_run_first": True},
        evidence_refs=request.evidence_refs,
        policy_version="phase-0.7",
        created_at="2026-05-06T00:00:00Z",
        reason="Terminal commands are critical risk.",
    )
    decision_ref = GuardianDecisionRef(
        decision_id=decision.decision_id,
        status=decision.status,
        expires_at=decision.expires_at,
    )
    audit_event = DecisionAuditEvent(
        event_id="event-1",
        actor_id=request.actor_id,
        shell_id=request.shell_id,
        event_type="guardian.decision",
        created_at=datetime(2026, 5, 6, tzinfo=timezone.utc),
        decision_id=decision.decision_id,
        intent_id=request.intent_id,
        input_id=request.input_id,
        action_type=request.action_type.value,
        target_ref=request.target_ref,
        risk_class=request.risk_class,
        result_status=decision.status.value,
        evidence_refs=tuple(request.evidence_refs),
    )
    terminal_event = TerminalEvent(
        event_id="event-2",
        actor_id=request.actor_id,
        shell_id=request.shell_id,
        event_type="terminal.command",
        created_at=datetime(2026, 5, 6, tzinfo=timezone.utc),
        decision_id=decision.decision_id,
        intent_id=request.intent_id,
        input_id=request.input_id,
        terminal_id="session-1",
        command_ref="cmd-ref-1",
    )

    public_callables = {
        name
        for name, value in GuardianProtocol.__dict__.items()
        if not name.startswith("_") and callable(value)
    }

    assert GuardianDecisionStatus.APPROVED.value == "approved"
    assert GuardianDecisionStatus.REVOKED.value == "revoked"
    assert ConsequentialActionType.ROBOT_ACTION.value == "robot_action"
    assert ConsequentialActionType.TERMINAL_COMMAND.value == "terminal_command"
    assert request.action_type is ConsequentialActionType.TERMINAL_COMMAND
    assert decision.decision_id == "decision-1"
    assert decision_ref.decision_id == decision.decision_id
    assert audit_event.decision_id == decision.decision_id
    assert terminal_event.risk_class == "critical"
    assert "evaluate_action" in public_callables
    assert "record_decision" in public_callables
    assert "execute" not in public_callables


def test_tool_pack_scoping_contracts_instantiate() -> None:
    from datetime import datetime, timezone

    from lima.contracts import (
        ModelRequest,
        ShellManifest,
        ShellToolScope,
        ToolExposureAuditEvent,
        ToolExposureDecision,
        ToolExposureRequest,
        ToolPackManifest,
        ToolPackName,
        ToolPackProtocol,
    )

    manifest = ToolPackManifest(
        pack_name=ToolPackName.TERMINAL,
        description="Terminal tools require critical approval.",
        default_risk_class="critical",
        allowed_action_types=("terminal_command",),
        requires_approval_level="operator_pin",
        tools=("terminal_send",),
        constraints={"deny_by_default": True},
    )
    shell_scope = ShellToolScope(
        shell_id="sparkbot",
        actor_id="operator-1",
        allowed_packs=(ToolPackName.MEMORY, ToolPackName.TERMINAL),
        denied_packs=(ToolPackName.PAYMENTS,),
        default_packs=(ToolPackName.MEMORY,),
        critical_packs=(ToolPackName.TERMINAL,),
        policy_version="phase-0.8",
    )
    shell_manifest = ShellManifest(
        shell_id=shell_scope.shell_id,
        name="Sparkbot",
        allowed_tool_packs=("memory", "terminal"),
        default_tool_packs=("memory",),
        denied_tool_packs=("payments",),
        critical_tool_packs=("terminal",),
    )
    exposure_request = ToolExposureRequest(
        request_id="exposure-request-1",
        shell_id=shell_scope.shell_id,
        actor_id="operator-1",
        intent_id="intent-1",
        decision_id="decision-1",
        requested_packs=(ToolPackName.TERMINAL,),
        requested_tools=("terminal_send",),
        risk_class="critical",
        context_refs=("terminal:session-1",),
    )
    exposure_decision = ToolExposureDecision(
        exposure_id="exposure-1",
        request_id=exposure_request.request_id,
        decision_id=exposure_request.decision_id,
        allowed_packs=(ToolPackName.TERMINAL,),
        denied_packs=(ToolPackName.PAYMENTS,),
        selected_tools=("terminal_send",),
        risk_class="critical",
        constraints={"requires_decision": True},
        reason="Terminal pack requires scoped approval.",
        policy_version="phase-0.8",
        created_at="2026-05-06T00:00:00Z",
    )
    model_request = ModelRequest(
        prompt="Prepare a guarded terminal plan.",
        tool_pack_scope=("terminal",),
        selected_tools=tuple(exposure_decision.selected_tools),
        tool_exposure=exposure_decision,
    )
    audit_event = ToolExposureAuditEvent(
        event_id="event-3",
        actor_id=exposure_request.actor_id,
        shell_id=exposure_request.shell_id,
        event_type="tool.exposure",
        created_at=datetime(2026, 5, 6, tzinfo=timezone.utc),
        decision_id=exposure_request.decision_id,
        intent_id=exposure_request.intent_id,
        exposure_id=exposure_decision.exposure_id,
        allowed_packs=("terminal",),
        denied_packs=("payments",),
        selected_tools=tuple(exposure_decision.selected_tools),
        risk_class=exposure_decision.risk_class,
    )
    public_callables = {
        name
        for name, value in ToolPackProtocol.__dict__.items()
        if not name.startswith("_") and callable(value)
    }

    assert ToolPackName.TERMINAL.value == "terminal"
    assert ToolPackName.PAYMENTS.value == "payments"
    assert ToolPackName.UNKNOWN.value == "unknown"
    assert manifest.requires_decision is True
    assert shell_manifest.default_tool_packs == ("memory",)
    assert shell_scope.critical_packs == (ToolPackName.TERMINAL,)
    assert exposure_request.decision_id == "decision-1"
    assert exposure_decision.selected_tools == ("terminal_send",)
    assert model_request.tool_exposure is exposure_decision
    assert audit_event.decision_id == exposure_decision.decision_id
    assert public_callables == {"declare_manifest", "list_tools"}
