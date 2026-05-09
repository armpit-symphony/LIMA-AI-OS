"""In-memory policy/risk evaluator fakes for contract validation."""

from __future__ import annotations

from collections.abc import Sequence

from lima.contracts.policy import (
    PolicyDecision,
    PolicyEvaluationContext,
    PolicyExposure,
    PolicyProtocol,
    ToolPackRiskPolicy,
    ToolPackRiskRule,
)


_CRITICAL_PACKS = {
    "terminal",
    "admin",
    "deploy",
    "payments",
    "robo",
    "secrets",
    "vault",
    "unknown",
}


class FakePolicyRiskEvaluator(PolicyProtocol):
    """In-memory policy/risk evaluator for tests."""

    def __init__(
        self,
        policy: ToolPackRiskPolicy | None = None,
        default_policy_id: str = "fake-policy",
        default_policy_version: str = "fake-policy-v1",
        timestamp: str = "fake",
    ) -> None:
        self._policy = policy or ToolPackRiskPolicy(
            policy_id=default_policy_id,
            policy_version=default_policy_version,
            shell_id=None,
            rules=(),
            created_at=timestamp,
            metadata={"fake_evaluator": True},
        )
        self.timestamp = timestamp
        self._decisions: list[PolicyDecision] = []

    def describe_policy(self) -> ToolPackRiskPolicy:
        return self._policy

    def evaluate(self, context: PolicyEvaluationContext) -> PolicyDecision:
        rule = self._find_rule(context.requested_pack)
        allowed, approval_level, reason, constraints = self._evaluate_rule(rule, context)
        decision = PolicyDecision(
            policy_decision_id=f"fake-policy:{context.requested_pack}:{len(self._decisions) + 1}",
            policy_id=self._policy.policy_id,
            decision_id=context.decision_id,
            allowed=allowed,
            pack_name=context.requested_pack,
            tool_name=context.requested_tool,
            risk_class=self._risk_class(rule, context),
            approval_level=approval_level,
            reason=reason,
            constraints=constraints,
            metadata={
                "fake_evaluator": "policy_risk",
                "policy_version": self._policy.policy_version,
                "timestamp": self.timestamp,
            },
        )
        self._decisions.append(decision)
        return decision

    def list_decisions(self) -> Sequence[PolicyDecision]:
        return tuple(self._decisions)

    def _find_rule(self, requested_pack: str) -> ToolPackRiskRule | None:
        for rule in self._policy.rules:
            if rule.pack_name == requested_pack:
                return rule
        return None

    def _evaluate_rule(
        self,
        rule: ToolPackRiskRule | None,
        context: PolicyEvaluationContext,
    ) -> tuple[bool, str | None, str, dict[str, object]]:
        risk_class = self._risk_class(rule, context)
        pack_name = context.requested_pack
        if rule is None:
            return (
                False,
                None,
                "unknown pack/tool denied by default",
                {
                    "unknown_pack": True,
                    "default_exposure": self._policy.unknown_default_exposure.value,
                },
            )

        if pack_name in _CRITICAL_PACKS or risk_class in {"high", "critical", "blocked"}:
            return (
                False,
                rule.required_approval_level,
                "high or critical pack requires separate Guardian decision and approval",
                {
                    "critical_like": True,
                    "requires_guardian_decision": rule.requires_decision,
                    "required_exposure": rule.default_exposure.value,
                },
            )

        if rule.default_exposure is PolicyExposure.DENY:
            return (
                False,
                rule.required_approval_level,
                "deny exposure rule",
                {"required_exposure": rule.default_exposure.value},
            )

        if rule.default_exposure is PolicyExposure.ALLOW:
            allowed = risk_class in {"read_only", "low"}
            reason = "low-risk allow rule" if allowed else "allow rule does not auto-allow this risk"
            return (
                allowed,
                rule.required_approval_level,
                reason,
                {
                    "required_exposure": rule.default_exposure.value,
                    "fake_low_risk_only": True,
                },
            )

        requirement = rule.default_exposure.value
        return (
            False,
            rule.required_approval_level or requirement,
            f"{requirement} required",
            {
                "required_exposure": requirement,
                "requires_confirmation": rule.requires_explicit_confirmation,
                "requires_operator_pin": rule.requires_operator_pin,
                "requires_breakglass": rule.requires_breakglass,
            },
        )

    def _risk_class(
        self,
        rule: ToolPackRiskRule | None,
        context: PolicyEvaluationContext,
    ) -> str:
        return context.risk_class or (rule.default_risk_class if rule else self._policy.default_unknown_risk)
