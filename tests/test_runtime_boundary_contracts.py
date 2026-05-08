"""Contract-shape tests for runtime boundary records."""


def test_runtime_boundary_contract_imports() -> None:
    from lima.contracts import (
        BoundaryClassification,
        BoundaryMapProtocol,
        ExtractionStatus,
        RuntimeBoundaryRecord,
    )

    assert BoundaryClassification.SHELL_ADAPTER.value == "shell_adapter"
    assert BoundaryClassification.GUARDIAN_CONTRACT.value == "guardian_contract"
    assert BoundaryClassification.DRIVER_CANDIDATE.value == "driver_candidate"
    assert BoundaryClassification.DO_NOT_EXTRACT_YET.value == "do_not_extract_yet"
    assert BoundaryClassification.DEPRECATED_OR_UNSAFE_SHORTCUT.value == "deprecated_or_unsafe_shortcut"
    assert ExtractionStatus.READY_FOR_ADAPTER_DESIGN.value == "ready_for_adapter_design"
    assert ExtractionStatus.NEEDS_DECISION_GATE.value == "needs_decision_gate"
    assert ExtractionStatus.NEEDS_PRIVACY_REVIEW.value == "needs_privacy_review"
    assert ExtractionStatus.DO_NOT_EXTRACT_YET.value == "do_not_extract_yet"
    assert all(
        item is not None
        for item in (
            BoundaryMapProtocol,
            RuntimeBoundaryRecord,
        )
    )


def test_runtime_boundary_record_is_shape_only() -> None:
    from lima.contracts import BoundaryClassification, BoundaryMapProtocol, ExtractionStatus, RuntimeBoundaryRecord

    record = RuntimeBoundaryRecord(
        source_repo="Sparkbot",
        source_path="backend/app/api/routes/chat/llm.py",
        surface_name="stream_chat_with_tools",
        current_role="Chat, model routing, tool planning, and guarded execution are close together.",
        classification=BoundaryClassification.DEPRECATED_OR_UNSAFE_SHORTCUT,
        future_lima_location="Sparkbot shell adapter plus LIMA Harness and ToolPack contracts",
        required_contracts=(
            "HumanInput",
            "IntentEnvelope",
            "GuardianDecision",
            "ToolPackScope",
            "Spine/Audit lineage",
            "Redaction/privacy",
        ),
        risk_level="critical",
        extraction_status=ExtractionStatus.DO_NOT_EXTRACT_YET,
        notes="Preserve user-facing behavior, not raw chat-to-tool coupling.",
        metadata={"inspected_ref": "origin/main"},
    )
    public_callables = {
        name
        for name, value in BoundaryMapProtocol.__dict__.items()
        if not name.startswith("_") and callable(value)
    }

    assert record.classification is BoundaryClassification.DEPRECATED_OR_UNSAFE_SHORTCUT
    assert record.extraction_status is ExtractionStatus.DO_NOT_EXTRACT_YET
    assert "GuardianDecision" in record.required_contracts
    assert public_callables == {"list_records"}
    assert "execute" not in public_callables
    assert "extract" not in public_callables
    assert "migrate" not in public_callables
