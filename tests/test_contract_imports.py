"""Import validation for Phase 0 contracts."""


def test_public_contract_imports() -> None:
    import lima
    from lima import contracts
    from lima.contracts import (
        ApprovalEvent,
        AuditEvent,
        ClarificationRequest,
        DriverCapability,
        DriverCommand,
        DriverEvent,
        DriverProtocol,
        DriverResult,
        GuardianContext,
        GuardianDecision,
        GuardianProtocol,
        HarnessProtocol,
        HumanInput,
        HumanInputSource,
        IntentCompilerProtocol,
        IntentEnvelope,
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
            AuditEvent,
            ClarificationRequest,
            DriverCapability,
            DriverCommand,
            DriverEvent,
            DriverProtocol,
            DriverResult,
            GuardianContext,
            GuardianProtocol,
            HarnessProtocol,
            HumanInput,
            HumanInputSource,
            IntentCompilerProtocol,
            IntentEnvelope,
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
    from lima.contracts import (
        ClarificationRequest,
        HumanInput,
        HumanInputSource,
        IntentEnvelope,
        RiskClass,
    )

    human_input = HumanInput(
        input_id="input-1",
        source=HumanInputSource.TEXT,
        actor_id="operator-1",
        shell_id="sparkbot",
        raw_text="Summarize the latest audit events.",
        confidence=0.99,
    )
    intent = IntentEnvelope(
        intent_id="intent-1",
        source_input_id=human_input.input_id,
        actor_id=human_input.actor_id,
        shell_id=human_input.shell_id,
        normalized_text="summarize latest audit events",
        intent_type="audit.summarize",
        risk_class=RiskClass.LOW,
    )
    clarification = ClarificationRequest(
        clarification_id="clarification-1",
        intent_id=intent.intent_id,
        question="Which audit window should be summarized?",
        choices=("last_hour", "today"),
    )

    assert HumanInputSource.FUTURE_BCI.value == "future_bci"
    assert RiskClass.CRITICAL.value == "critical"
    assert intent.source_input_id == human_input.input_id
    assert clarification.blocking is True
