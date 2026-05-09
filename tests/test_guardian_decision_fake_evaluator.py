"""Tests for the in-memory Guardian decision fake evaluator."""


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
    requested_tool_pack: str | None = None,
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
        metadata={"test_only": True},
    )


def test_low_risk_request_is_approved_with_decision_identity() -> None:
    from lima.contracts import ConsequentialActionType, GuardianDecisionStatus
    from lima.guardian import FakeGuardianDecisionEvaluator

    request = _request(
        request_id="low-1",
        action_type=ConsequentialActionType.FILE_OPERATION,
        risk_class="low",
        requested_tool_pack="files",
    )
    evaluator = FakeGuardianDecisionEvaluator()
    decision = evaluator.evaluate_action(request)

    assert decision.decision_id
    assert decision.status is GuardianDecisionStatus.APPROVED
    assert decision.request_id == request.request_id
    assert decision.actor_id == request.actor_id
    assert decision.shell_id == request.shell_id
    assert decision.action_type is request.action_type
    assert decision.allowed_tool_packs == ("files",)


def test_critical_terminal_request_is_not_auto_approved() -> None:
    from lima.contracts import ConsequentialActionType, GuardianDecisionStatus
    from lima.guardian import FakeGuardianDecisionEvaluator

    request = _request(
        request_id="terminal-1",
        action_type=ConsequentialActionType.TERMINAL_COMMAND,
        risk_class="critical",
        requested_tool_pack="terminal",
    )
    decision = FakeGuardianDecisionEvaluator().evaluate_action(request)

    assert decision.status is GuardianDecisionStatus.NEEDS_OPERATOR_PIN
    assert decision.status is not GuardianDecisionStatus.APPROVED
    assert decision.approval_level == "operator_pin"
    assert decision.allowed_tool_packs == ()


def test_robot_action_request_is_not_auto_approved() -> None:
    from lima.contracts import ConsequentialActionType, GuardianDecisionStatus
    from lima.guardian import FakeGuardianDecisionEvaluator

    request = _request(
        request_id="robot-1",
        action_type=ConsequentialActionType.ROBOT_ACTION,
        risk_class="critical",
        requested_tool_pack="robo",
    )
    decision = FakeGuardianDecisionEvaluator().evaluate_action(request)

    assert decision.status in {
        GuardianDecisionStatus.NEEDS_OPERATOR_PIN,
        GuardianDecisionStatus.NEEDS_BREAKGLASS,
        GuardianDecisionStatus.ESCALATED,
        GuardianDecisionStatus.NEEDS_HUMAN_CONFIRMATION,
    }
    assert decision.status is not GuardianDecisionStatus.APPROVED


def test_unknown_action_request_is_denied() -> None:
    from lima.contracts import ConsequentialActionType, GuardianDecisionStatus
    from lima.guardian import FakeGuardianDecisionEvaluator

    request = _request(
        request_id="unknown-1",
        action_type=ConsequentialActionType.UNKNOWN,
        risk_class="medium",
    )
    decision = FakeGuardianDecisionEvaluator().evaluate_action(request)

    assert decision.status is GuardianDecisionStatus.DENIED
    assert decision.reason == "fake evaluator denies unknown action type"


def test_fake_evaluator_records_decisions_in_memory() -> None:
    from lima.contracts import ConsequentialActionType
    from lima.guardian import FakeGuardianDecisionEvaluator

    evaluator = FakeGuardianDecisionEvaluator()
    first = evaluator.evaluate_action(
        _request("record-1", ConsequentialActionType.FILE_OPERATION, "low")
    )
    second = evaluator.evaluate_action(
        _request("record-2", ConsequentialActionType.NETWORK_ACTION, "high")
    )

    assert evaluator.get_decision(first.decision_id) is first
    assert evaluator.get_decision(second.decision_id) is second
    assert evaluator.get_decision("missing-decision") is None
    assert evaluator.list_decisions() == (first, second)


def test_fake_evaluator_forbidden_live_methods_are_absent() -> None:
    from lima.guardian import FakeGuardianDecisionEvaluator

    forbidden_methods = {
        "execute",
        "enforce",
        "run",
        "call_tool",
        "call_model",
        "call_driver",
        "approve_and_execute",
        "bypass",
    }

    assert _public_callables(FakeGuardianDecisionEvaluator).isdisjoint(forbidden_methods)
