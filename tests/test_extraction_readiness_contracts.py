"""Contract-shape tests for extraction readiness records."""


def test_extraction_readiness_contract_imports() -> None:
    from lima.contracts import ExtractionReadinessRecord, ReadinessArea, ReadinessStatus

    assert ReadinessStatus.READY.value == "ready"
    assert ReadinessStatus.READY_WITH_CONSTRAINTS.value == "ready_with_constraints"
    assert ReadinessStatus.BLOCKED.value == "blocked"
    assert ReadinessArea.ARCHITECTURE.value == "architecture"
    assert ReadinessArea.GUARDIAN.value == "guardian"
    assert ReadinessArea.ROBOTICS.value == "robotics"
    assert ReadinessArea.TERMINAL.value == "terminal"
    assert ExtractionReadinessRecord is not None


def test_extraction_readiness_record_is_shape_only() -> None:
    from lima.contracts import ExtractionReadinessRecord, ReadinessArea, ReadinessStatus

    record = ExtractionReadinessRecord(
        area=ReadinessArea.GUARDIAN,
        status=ReadinessStatus.READY_WITH_CONSTRAINTS,
        score=6,
        blockers=("Sparkbot app.crud/app.models coupling",),
        ready_items=("import-boundary audit",),
        next_action="Create Guardian Suite decoupling audit.",
        metadata={"first_phase_1_branch": "phase-1-0-guardian-suite-decoupling-audit"},
    )

    public_callables = {
        name
        for name, value in ExtractionReadinessRecord.__dict__.items()
        if not name.startswith("_") and callable(value)
    }

    assert record.area is ReadinessArea.GUARDIAN
    assert record.status is ReadinessStatus.READY_WITH_CONSTRAINTS
    assert record.score == 6
    assert "Sparkbot app.crud/app.models coupling" in record.blockers
    assert "execute" not in public_callables
    assert "extract" not in public_callables
    assert "migrate" not in public_callables
