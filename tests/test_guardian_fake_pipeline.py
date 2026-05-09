"""Tests for the in-memory Guardian fake pipeline."""


def _public_callables(provider: type) -> set[str]:
    return {
        name
        for name, value in provider.__dict__.items()
        if not name.startswith("_") and callable(value)
    }


def _request(
    request_id: str,
    action_type,
    risk_class: str,
    requested_tool_pack: str | None,
):
    from lima.contracts import ConsequentialActionRequest

    return ConsequentialActionRequest(
        request_id=request_id,
        intent_id=f"intent-{request_id}",
        input_id=f"input-{request_id}",
        actor_id="actor-1",
        shell_id="test-shell",
        action_type=action_type,
        target_ref=f"target-{request_id}",
        requested_tool_pack=requested_tool_pack,
        risk_class=risk_class,
        typed_args={"summary_ref": f"args-{request_id}"},
        evidence_refs=(f"evidence-{request_id}",),
        metadata={"requested_tool": f"tool-{request_id}", "test_only": True},
    )


def _policy(*rules):
    from lima.contracts import ToolPackRiskPolicy

    return ToolPackRiskPolicy(
        policy_id="policy-1",
        policy_version="phase-1.8-fake",
        shell_id="test-shell",
        rules=rules,
        created_at="fake",
    )


def _pipeline(*rules):
    from lima.guardian import (
        FakeApprovalRecorder,
        FakeGuardianDecisionEvaluator,
        FakeGuardianPipeline,
        FakePolicyRiskEvaluator,
        FakeSpineAuditRecorder,
    )

    spine = FakeSpineAuditRecorder()
    pipeline = FakeGuardianPipeline(
        policy_evaluator=FakePolicyRiskEvaluator(policy=_policy(*rules)),
        decision_evaluator=FakeGuardianDecisionEvaluator(),
        approval_recorder=FakeApprovalRecorder(),
        spine_recorder=spine,
    )
    return pipeline, spine


def test_low_risk_allowed_request_records_fake_lineage_without_execution() -> None:
    from lima.contracts import (
        AuditStatus,
        ConsequentialActionType,
        GuardianDecisionStatus,
        PolicyExposure,
        ToolPackRiskRule,
    )

    rule = ToolPackRiskRule(
        pack_name="files",
        default_risk_class="low",
        default_exposure=PolicyExposure.ALLOW,
    )
    pipeline, spine = _pipeline(rule)
    request = _request(
        "low-1",
        ConsequentialActionType.FILE_OPERATION,
        "low",
        "files",
    )

    result = pipeline.evaluate_request(request)

    assert result.policy_decision.allowed is True
    assert result.guardian_decision.decision_id
    assert result.guardian_decision.status is GuardianDecisionStatus.APPROVED
    assert result.guardian_decision.request_id == request.request_id
    assert result.guardian_decision.actor_id == request.actor_id
    assert result.guardian_decision.shell_id == request.shell_id
    assert result.guardian_decision.action_type is request.action_type
    assert result.lineage_id
    assert result.status == AuditStatus.SUCCEEDED.value
    assert result.approval is None
    assert result.metadata["non_executing"] is True
    assert len(spine.get_lineage(result.lineage_id)) >= 3
    assert spine.get_lineage_record(result.lineage_id).decision_id == result.guardian_decision.decision_id


def test_critical_terminal_request_does_not_auto_approve() -> None:
    from lima.contracts import (
        ConsequentialActionType,
        GuardianDecisionStatus,
        PolicyExposure,
        ToolPackRiskRule,
    )

    rule = ToolPackRiskRule(
        pack_name="terminal",
        default_risk_class="critical",
        default_exposure=PolicyExposure.ALLOW,
        required_approval_level="operator_pin",
    )
    pipeline, spine = _pipeline(rule)
    request = _request(
        "terminal-1",
        ConsequentialActionType.TERMINAL_COMMAND,
        "critical",
        "terminal",
    )

    result = pipeline.evaluate_request(request)

    assert result.policy_decision.allowed is False
    assert result.guardian_decision.status is not GuardianDecisionStatus.APPROVED
    assert result.guardian_decision.status is GuardianDecisionStatus.NEEDS_OPERATOR_PIN
    assert result.approval is not None
    assert result.approval.decision_id == result.guardian_decision.decision_id
    assert result.approval.status.value == "pending"
    assert spine.get_lineage(result.lineage_id)
    assert spine.get_lineage_record(result.lineage_id).approval_id == result.approval.approval_id
    assert result.metadata["non_executing"] is True


def test_robot_request_does_not_auto_approve_and_records_lineage() -> None:
    from lima.contracts import (
        ConsequentialActionType,
        GuardianDecisionStatus,
        PolicyExposure,
        ToolPackRiskRule,
    )

    rule = ToolPackRiskRule(
        pack_name="robo",
        default_risk_class="critical",
        default_exposure=PolicyExposure.ALLOW,
        required_approval_level="breakglass",
    )
    pipeline, spine = _pipeline(rule)
    request = _request(
        "robot-1",
        ConsequentialActionType.ROBOT_ACTION,
        "critical",
        "robo",
    )

    result = pipeline.evaluate_request(request)

    assert result.guardian_decision.status is not GuardianDecisionStatus.APPROVED
    assert result.approval is not None
    assert result.lineage_id
    assert spine.get_lineage_record(result.lineage_id).decision_id == result.guardian_decision.decision_id


def test_unknown_action_is_denied_and_auditable() -> None:
    from lima.contracts import ConsequentialActionType, GuardianDecisionStatus

    pipeline, spine = _pipeline()
    request = _request(
        "unknown-1",
        ConsequentialActionType.UNKNOWN,
        "medium",
        None,
    )

    result = pipeline.evaluate_request(request)

    assert result.policy_decision.allowed is False
    assert result.guardian_decision.status is GuardianDecisionStatus.DENIED
    assert result.status == "denied"
    assert spine.get_lineage(result.lineage_id)
    assert spine.get_lineage_record(result.lineage_id).status == "denied"


def test_approval_metadata_is_evidence_not_authorization() -> None:
    from lima.contracts import ApprovalMetadata, ConsequentialActionType, GuardianDecision

    pipeline, _spine = _pipeline()
    request = _request(
        "approval-evidence-1",
        ConsequentialActionType.TERMINAL_COMMAND,
        "critical",
        "terminal",
    )

    result = pipeline.evaluate_request(request)

    assert isinstance(result.approval, ApprovalMetadata)
    assert not isinstance(result.approval, GuardianDecision)
    assert result.approval.decision_id == result.guardian_decision.decision_id
    assert result.approval.status.value == "pending"
    assert "authorize_execution" not in _public_callables(type(result.approval))


def test_fake_pipeline_forbidden_live_methods_are_absent() -> None:
    from lima.guardian import FakeGuardianPipeline

    forbidden_methods = {
        "execute",
        "enforce",
        "run",
        "call_tool",
        "call_model",
        "call_driver",
        "approve_and_execute",
        "authorize_execution",
        "bypass",
        "persist",
        "save_to_db",
        "open_db",
        "write_file",
        "send",
    }

    assert _public_callables(FakeGuardianPipeline).isdisjoint(forbidden_methods)
