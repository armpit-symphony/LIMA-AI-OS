"""Import validation for Phase 0 contracts."""


def test_public_contract_imports() -> None:
    import lima
    from lima import contracts
    from lima.contracts import (
        ApprovalEvent,
        AuditEvent,
        DriverCapability,
        DriverCommand,
        DriverEvent,
        DriverProtocol,
        DriverResult,
        GuardianContext,
        GuardianDecision,
        GuardianProtocol,
        HarnessProtocol,
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
            DriverCapability,
            DriverCommand,
            DriverEvent,
            DriverProtocol,
            DriverResult,
            GuardianContext,
            GuardianProtocol,
            HarnessProtocol,
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
