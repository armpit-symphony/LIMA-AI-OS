"""Contract-shape tests for tool-pack risk policy."""


def test_policy_contract_imports() -> None:
    from lima.contracts import (
        PolicyDecision,
        PolicyEvaluationContext,
        PolicyExposure,
        PolicyProtocol,
        ToolPackRiskPolicy,
        ToolPackRiskRule,
    )

    assert PolicyExposure.ALLOW.value == "allow"
    assert PolicyExposure.DENY.value == "deny"
    assert PolicyExposure.REQUIRE_CONFIRMATION.value == "require_confirmation"
    assert PolicyExposure.REQUIRE_GUARDIAN_REVIEW.value == "require_guardian_review"
    assert PolicyExposure.REQUIRE_OPERATOR_PIN.value == "require_operator_pin"
    assert PolicyExposure.REQUIRE_BREAKGLASS.value == "require_breakglass"
    assert all(
        item is not None
        for item in (
            PolicyDecision,
            PolicyEvaluationContext,
            PolicyProtocol,
            ToolPackRiskPolicy,
            ToolPackRiskRule,
        )
    )


def test_tool_pack_risk_policy_contracts_instantiate() -> None:
    from lima.contracts import (
        PolicyDecision,
        PolicyEvaluationContext,
        PolicyExposure,
        PolicyProtocol,
        ToolPackRiskPolicy,
        ToolPackRiskRule,
    )

    rule = ToolPackRiskRule(
        pack_name="terminal",
        default_risk_class="critical",
        read_risk_class="critical",
        write_risk_class="critical",
        destructive_risk_class="critical",
        default_exposure=PolicyExposure.DENY,
        required_approval_level="operator_pin",
        requires_explicit_confirmation=True,
        requires_operator_pin=True,
        constraints={"deny_by_default": True},
    )
    policy = ToolPackRiskPolicy(
        policy_id="policy-1",
        policy_version="phase-0.10",
        shell_id="sparkbot",
        rules=(rule,),
        created_at="2026-05-08T00:00:00Z",
    )
    context = PolicyEvaluationContext(
        shell_id="sparkbot",
        actor_id="operator-1",
        intent_id="intent-1",
        decision_id="decision-1",
        requested_pack="terminal",
        requested_tool="terminal_send",
        action_type="terminal_command",
        risk_class="critical",
    )
    decision = PolicyDecision(
        policy_decision_id="policy-decision-1",
        policy_id=policy.policy_id,
        decision_id=context.decision_id,
        allowed=False,
        pack_name=context.requested_pack,
        tool_name=context.requested_tool,
        risk_class=context.risk_class or "critical",
        approval_level=rule.required_approval_level,
        reason="Terminal tools are denied by default.",
        constraints={"requires_operator_pin": True},
    )
    public_callables = {
        name
        for name, value in PolicyProtocol.__dict__.items()
        if not name.startswith("_") and callable(value)
    }

    assert rule.requires_decision is True
    assert rule.requires_audit is True
    assert policy.default_unknown_risk == "critical"
    assert policy.unknown_default_exposure is PolicyExposure.DENY
    assert context.decision_id == "decision-1"
    assert decision.allowed is False
    assert decision.pack_name == "terminal"
    assert public_callables == {"describe_policy", "evaluate"}
    assert "execute" not in public_callables
