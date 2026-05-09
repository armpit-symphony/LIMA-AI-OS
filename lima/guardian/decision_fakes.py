"""In-memory Guardian decision evaluator fakes for contract validation."""

from __future__ import annotations

from collections.abc import Sequence

from lima.contracts.guardian import (
    ConsequentialActionRequest,
    ConsequentialActionType,
    GuardianDecision,
    GuardianDecisionStatus,
)


_CRITICAL_ACTION_TYPES = {
    ConsequentialActionType.TERMINAL_COMMAND,
    ConsequentialActionType.ROBOT_ACTION,
    ConsequentialActionType.PAYMENT_ACTION,
    ConsequentialActionType.DEPLOY_ACTION,
    ConsequentialActionType.SECRET_ACCESS,
}
_CRITICAL_ACTION_VALUES = {action_type.value for action_type in _CRITICAL_ACTION_TYPES}


def _action_type_key(action_type: ConsequentialActionType | str) -> str:
    if isinstance(action_type, ConsequentialActionType):
        return action_type.value
    return str(action_type)


class FakeGuardianDecisionEvaluator:
    """In-memory Guardian decision evaluator for tests."""

    def __init__(
        self,
        policy_version: str = "fake-policy-v1",
        default_actor: str | None = None,
        critical_requires_breakglass: bool = False,
        medium_requires_confirmation: bool = False,
        created_at: str = "fake",
    ) -> None:
        self.policy_version = policy_version
        self.default_actor = default_actor
        self.critical_requires_breakglass = critical_requires_breakglass
        self.medium_requires_confirmation = medium_requires_confirmation
        self.created_at = created_at
        self._decisions: dict[str, GuardianDecision] = {}

    def evaluate_action(self, request: ConsequentialActionRequest) -> GuardianDecision:
        status, approval_level, reason = self._classify_request(request)
        decision_id = f"fake-guardian:{request.request_id}:{len(self._decisions) + 1}"
        decision = GuardianDecision(
            decision_id=decision_id,
            request_id=request.request_id,
            intent_id=request.intent_id,
            input_id=request.input_id,
            actor_id=request.actor_id or self.default_actor or "fake-actor",
            shell_id=request.shell_id,
            action_type=request.action_type,
            target_ref=request.target_ref,
            risk_class=request.risk_class,
            status=status,
            approval_level=approval_level,
            allowed_tool_packs=self._allowed_tool_packs(request, status),
            constraints={
                "fake_evaluator": True,
                "in_memory_only": True,
                "non_executing": True,
            },
            evidence_refs=request.evidence_refs,
            policy_version=self.policy_version,
            created_at=self.created_at,
            decided_at=self.created_at,
            decided_by="fake-guardian",
            reason=reason,
            metadata={
                "fake_evaluator": "guardian_decision",
                "requested_tool_pack": request.requested_tool_pack,
            },
        )
        self.record_decision(decision)
        return decision

    def record_decision(self, decision: GuardianDecision) -> None:
        self._decisions[decision.decision_id] = decision

    def get_decision(self, decision_id: str) -> GuardianDecision | None:
        return self._decisions.get(decision_id)

    def list_decisions(self) -> Sequence[GuardianDecision]:
        return tuple(self._decisions.values())

    def _classify_request(
        self,
        request: ConsequentialActionRequest,
    ) -> tuple[GuardianDecisionStatus, str | None, str]:
        risk_class = request.risk_class.lower()
        action_type = _action_type_key(request.action_type)
        if action_type == ConsequentialActionType.UNKNOWN.value:
            return (
                GuardianDecisionStatus.DENIED,
                None,
                "fake evaluator denies unknown action type",
            )

        if risk_class == "blocked":
            return (
                GuardianDecisionStatus.DENIED,
                None,
                "fake evaluator denies blocked risk class",
            )

        if risk_class == "critical" or action_type in _CRITICAL_ACTION_VALUES:
            if self.critical_requires_breakglass:
                return (
                    GuardianDecisionStatus.NEEDS_BREAKGLASS,
                    "breakglass",
                    "fake evaluator requires breakglass for critical action",
                )
            return (
                GuardianDecisionStatus.NEEDS_OPERATOR_PIN,
                "operator_pin",
                "fake evaluator requires operator PIN for critical action",
            )

        if risk_class == "high":
            return (
                GuardianDecisionStatus.NEEDS_HUMAN_CONFIRMATION,
                "confirm",
                "fake evaluator requires confirmation for high risk action",
            )

        if risk_class == "medium" and self.medium_requires_confirmation:
            return (
                GuardianDecisionStatus.NEEDS_HUMAN_CONFIRMATION,
                "confirm",
                "fake evaluator requires confirmation for medium risk action",
            )

        if risk_class in {"read_only", "low", "medium"}:
            return (
                GuardianDecisionStatus.APPROVED,
                None,
                "fake evaluator approved low-risk contract request",
            )

        return (
            GuardianDecisionStatus.ESCALATED,
            "guardian_review",
            "fake evaluator escalates unrecognized risk class",
        )

    def _allowed_tool_packs(
        self,
        request: ConsequentialActionRequest,
        status: GuardianDecisionStatus,
    ) -> tuple[str, ...]:
        if status is not GuardianDecisionStatus.APPROVED or request.requested_tool_pack is None:
            return ()
        return (request.requested_tool_pack,)
