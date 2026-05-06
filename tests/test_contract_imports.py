"""Import validation for Phase 0 contracts."""


def test_public_contract_imports() -> None:
    import lima
    from lima import contracts
    from lima.contracts import (
        ApprovalEvent,
        ApprovalLevel,
        AuditEvent,
        ClarificationRequest,
        DriverCapability,
        DriverCommand,
        DriverEvent,
        DriverProtocol,
        DriverResult,
        EvidenceRequirement,
        GuardianContext,
        GuardianDecision,
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
        ShellManifest,
        ShellProtocol,
        SpineEvent,
        SpineProtocol,
        StorageProtocol,
        TaskRecord,
        ToolCallEvent,
        ToolDefinition,
        ToolPackManifest,
        ToolPackProtocol,
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
            DriverCapability,
            DriverCommand,
            DriverEvent,
            DriverProtocol,
            DriverResult,
            EvidenceRequirement,
            GuardianContext,
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
            ShellManifest,
            ShellProtocol,
            SpineEvent,
            SpineProtocol,
            StorageProtocol,
            TaskRecord,
            ToolCallEvent,
            ToolDefinition,
            ToolPackManifest,
            ToolPackProtocol,
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
