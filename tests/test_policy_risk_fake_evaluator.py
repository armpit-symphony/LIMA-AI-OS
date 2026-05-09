"""Tests for the in-memory policy/risk fake evaluator."""


def _public_callables(provider: type) -> set[str]:
    return {
        name
        for name, value in provider.__dict__.items()
        if not name.startswith("_") and callable(value)
    }


def _policy(*rules):
    from lima.contracts import ToolPackRiskPolicy

    return ToolPackRiskPolicy(
        policy_id="policy-1",
        policy_version="phase-1.5-fake",
        shell_id="test-shell",
        rules=rules,
        created_at="fake",
    )


def _context(
    requested_pack: str,
    risk_class: str,
    requested_tool: str | None = None,
    decision_id: str | None = "guardian-decision-ref-1",
):
    from lima.contracts import PolicyEvaluationContext

    return PolicyEvaluationContext(
        shell_id="test-shell",
        actor_id="actor-1",
        intent_id="intent-1",
        decision_id=decision_id,
        requested_pack=requested_pack,
        requested_tool=requested_tool,
        action_type="tool_call",
        risk_class=risk_class,
        metadata={"test_only": True},
    )


def test_low_risk_allowed_pack_returns_policy_decision() -> None:
    from lima.contracts import PolicyExposure, ToolPackRiskRule
    from lima.guardian import FakePolicyRiskEvaluator

    rule = ToolPackRiskRule(
        pack_name="files",
        default_risk_class="low",
        default_exposure=PolicyExposure.ALLOW,
    )
    evaluator = FakePolicyRiskEvaluator(policy=_policy(rule))
    decision = evaluator.evaluate(_context("files", "low", "list_files"))

    assert decision.policy_decision_id
    assert decision.allowed is True
    assert decision.policy_id == "policy-1"
    assert decision.decision_id == "guardian-decision-ref-1"
    assert decision.pack_name == "files"
    assert decision.tool_name == "list_files"
    assert decision.risk_class == "low"


def test_unknown_pack_denies_by_default() -> None:
    from lima.guardian import FakePolicyRiskEvaluator

    decision = FakePolicyRiskEvaluator(policy=_policy()).evaluate(
        _context("unknown-pack", "low", "unknown_tool")
    )

    assert decision.allowed is False
    assert "unknown" in (decision.reason or "")
    assert "default" in (decision.reason or "")
    assert decision.constraints["unknown_pack"] is True


def test_terminal_critical_pack_does_not_auto_allow() -> None:
    from lima.contracts import PolicyExposure, ToolPackRiskRule
    from lima.guardian import FakePolicyRiskEvaluator

    rule = ToolPackRiskRule(
        pack_name="terminal",
        default_risk_class="critical",
        default_exposure=PolicyExposure.ALLOW,
        required_approval_level="operator_pin",
    )
    decision = FakePolicyRiskEvaluator(policy=_policy(rule)).evaluate(
        _context("terminal", "critical", "terminal_send")
    )

    assert decision.allowed is False
    assert decision.approval_level == "operator_pin"
    assert decision.constraints["critical_like"] is True


def test_robo_critical_pack_does_not_auto_allow() -> None:
    from lima.contracts import PolicyExposure, ToolPackRiskRule
    from lima.guardian import FakePolicyRiskEvaluator

    rule = ToolPackRiskRule(
        pack_name="robo",
        default_risk_class="critical",
        default_exposure=PolicyExposure.ALLOW,
        required_approval_level="breakglass",
    )
    decision = FakePolicyRiskEvaluator(policy=_policy(rule)).evaluate(
        _context("robo", "critical", "move_arm")
    )

    assert decision.allowed is False
    assert decision.approval_level == "breakglass"
    assert decision.constraints["critical_like"] is True


def test_operator_pin_and_breakglass_rules_do_not_auto_allow() -> None:
    from lima.contracts import PolicyExposure, ToolPackRiskRule
    from lima.guardian import FakePolicyRiskEvaluator

    pin_rule = ToolPackRiskRule(
        pack_name="admin",
        default_risk_class="critical",
        default_exposure=PolicyExposure.REQUIRE_OPERATOR_PIN,
        required_approval_level="operator_pin",
        requires_operator_pin=True,
    )
    breakglass_rule = ToolPackRiskRule(
        pack_name="payments",
        default_risk_class="critical",
        default_exposure=PolicyExposure.REQUIRE_BREAKGLASS,
        required_approval_level="breakglass",
        requires_breakglass=True,
    )
    evaluator = FakePolicyRiskEvaluator(policy=_policy(pin_rule, breakglass_rule))
    pin_decision = evaluator.evaluate(_context("admin", "critical", "admin_change"))
    breakglass_decision = evaluator.evaluate(_context("payments", "critical", "send_payment"))

    assert pin_decision.allowed is False
    assert pin_decision.approval_level == "operator_pin"
    assert "Guardian decision" in (pin_decision.reason or "")
    assert breakglass_decision.allowed is False
    assert breakglass_decision.approval_level == "breakglass"
    assert "Guardian decision" in (breakglass_decision.reason or "")


def test_policy_decision_does_not_replace_guardian_decision() -> None:
    from lima.contracts import GuardianDecision, PolicyDecision, PolicyExposure, ToolPackRiskRule
    from lima.guardian import FakePolicyRiskEvaluator

    rule = ToolPackRiskRule(
        pack_name="files",
        default_risk_class="low",
        default_exposure=PolicyExposure.ALLOW,
    )
    decision = FakePolicyRiskEvaluator(policy=_policy(rule)).evaluate(
        _context("files", "low", "list_files")
    )

    assert isinstance(decision, PolicyDecision)
    assert not isinstance(decision, GuardianDecision)
    assert decision.decision_id == "guardian-decision-ref-1"


def test_fake_policy_evaluator_records_decisions_in_memory() -> None:
    from lima.contracts import PolicyExposure, ToolPackRiskRule
    from lima.guardian import FakePolicyRiskEvaluator

    rule = ToolPackRiskRule(
        pack_name="files",
        default_risk_class="low",
        default_exposure=PolicyExposure.ALLOW,
    )
    evaluator = FakePolicyRiskEvaluator(policy=_policy(rule))
    first = evaluator.evaluate(_context("files", "low", "list_files"))
    second = evaluator.evaluate(_context("missing", "medium", "missing_tool"))

    assert evaluator.describe_policy().policy_id == "policy-1"
    assert evaluator.list_decisions() == (first, second)


def test_fake_policy_evaluator_forbidden_live_methods_are_absent() -> None:
    from lima.guardian import FakePolicyRiskEvaluator

    forbidden_methods = {
        "execute",
        "enforce",
        "authorize_execution",
        "call_tool",
        "call_model",
        "call_driver",
        "approve_and_execute",
        "bypass",
    }

    assert _public_callables(FakePolicyRiskEvaluator).isdisjoint(forbidden_methods)
