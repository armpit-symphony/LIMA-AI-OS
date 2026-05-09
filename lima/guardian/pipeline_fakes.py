"""In-memory Guardian pipeline fakes for contract validation."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from lima.contracts.approval import (
    ApprovalMetadata,
    ApprovalMethod,
    ApprovalScope,
    ApprovalStatus,
)
from lima.contracts.events import AuditEventType, AuditLineageRecord, AuditStatus
from lima.contracts.guardian import (
    ConsequentialActionRequest,
    ConsequentialActionType,
    GuardianDecision,
    GuardianDecisionStatus,
)
from lima.contracts.policy import PolicyDecision, PolicyEvaluationContext
from lima.contracts.spine import SpineEvent

from .approval_fakes import FakeApprovalRecorder
from .decision_fakes import FakeGuardianDecisionEvaluator
from .policy_fakes import FakePolicyRiskEvaluator
from .spine_fakes import FakeSpineAuditRecorder


_APPROVAL_REQUIRED_STATUSES = {
    GuardianDecisionStatus.NEEDS_HUMAN_CONFIRMATION,
    GuardianDecisionStatus.NEEDS_OPERATOR_PIN,
    GuardianDecisionStatus.NEEDS_BREAKGLASS,
    GuardianDecisionStatus.ESCALATED,
}


@dataclass(frozen=True)
class FakeGuardianPipelineResult:
    """Fake pipeline result tying policy, decision, approval, and lineage records."""

    request: ConsequentialActionRequest
    policy_decision: PolicyDecision
    guardian_decision: GuardianDecision
    approval: ApprovalMetadata | None
    lineage_id: str
    event_ids: Sequence[str]
    status: str
    metadata: Mapping[str, Any] = field(default_factory=dict)


class FakeGuardianPipeline:
    """Compose fake Guardian components for in-memory contract tests."""

    def __init__(
        self,
        policy_evaluator: FakePolicyRiskEvaluator,
        decision_evaluator: FakeGuardianDecisionEvaluator,
        approval_recorder: FakeApprovalRecorder,
        spine_recorder: FakeSpineAuditRecorder,
        timestamp: str = "2026-01-01T00:00:00Z",
    ) -> None:
        self.policy_evaluator = policy_evaluator
        self.decision_evaluator = decision_evaluator
        self.approval_recorder = approval_recorder
        self.spine_recorder = spine_recorder
        self.timestamp = timestamp
        self._created_at = datetime(2026, 1, 1, tzinfo=timezone.utc)

    def evaluate_request(
        self,
        request: ConsequentialActionRequest,
    ) -> FakeGuardianPipelineResult:
        lineage_id = f"fake-lineage:{request.request_id}"
        policy_decision = self.policy_evaluator.evaluate(
            self._policy_context_from_request(request)
        )
        guardian_decision = self.decision_evaluator.evaluate_action(request)
        approval = self._record_approval_if_needed(request, guardian_decision)
        result_status = self._result_status(policy_decision, guardian_decision, approval)

        events = self._record_events(
            request=request,
            policy_decision=policy_decision,
            guardian_decision=guardian_decision,
            approval=approval,
            lineage_id=lineage_id,
            result_status=result_status,
        )
        self._record_lineage(
            request=request,
            policy_decision=policy_decision,
            guardian_decision=guardian_decision,
            approval=approval,
            lineage_id=lineage_id,
            event_ids=tuple(event.event_id for event in events),
            result_status=result_status,
        )

        return FakeGuardianPipelineResult(
            request=request,
            policy_decision=policy_decision,
            guardian_decision=guardian_decision,
            approval=approval,
            lineage_id=lineage_id,
            event_ids=tuple(event.event_id for event in events),
            status=result_status,
            metadata={
                "fake_pipeline": True,
                "in_memory_only": True,
                "non_executing": True,
            },
        )

    def _policy_context_from_request(
        self,
        request: ConsequentialActionRequest,
    ) -> PolicyEvaluationContext:
        requested_tool = request.metadata.get("requested_tool")
        if not isinstance(requested_tool, str):
            requested_tool = None
        return PolicyEvaluationContext(
            shell_id=request.shell_id,
            actor_id=request.actor_id,
            intent_id=request.intent_id,
            decision_id=None,
            requested_pack=request.requested_tool_pack or "unknown",
            requested_tool=requested_tool,
            action_type=request.action_type.value,
            risk_class=request.risk_class,
            metadata={
                "fake_pipeline": True,
                "request_id": request.request_id,
            },
        )

    def _record_approval_if_needed(
        self,
        request: ConsequentialActionRequest,
        decision: GuardianDecision,
    ) -> ApprovalMetadata | None:
        if decision.status not in _APPROVAL_REQUIRED_STATUSES:
            return None

        scope = ApprovalScope(
            decision_id=decision.decision_id,
            actor_id=decision.actor_id,
            shell_id=decision.shell_id,
            action_type=decision.action_type.value,
            target_ref=decision.target_ref,
            tool_pack=request.requested_tool_pack,
            risk_class=decision.risk_class,
            constraints={
                "fake_pipeline": True,
                "metadata_only": True,
                "non_executing": True,
            },
            policy_version=decision.policy_version,
        )
        existing = self.approval_recorder.describe_required_approval(scope)
        if existing is not None:
            return existing

        approval = ApprovalMetadata(
            approval_id=f"fake-approval:{decision.decision_id}",
            decision_id=decision.decision_id,
            input_id=decision.input_id,
            intent_id=decision.intent_id,
            actor_id=decision.actor_id,
            shell_id=decision.shell_id,
            approved_by=None,
            approval_level=decision.approval_level,
            approval_method=self._approval_method(decision),
            status=ApprovalStatus.PENDING,
            risk_class=decision.risk_class,
            action_type=decision.action_type.value,
            target_ref=decision.target_ref,
            tool_pack=request.requested_tool_pack,
            constraints={
                "fake_pipeline": True,
                "metadata_only": True,
                "non_executing": True,
            },
            evidence_refs=decision.evidence_refs,
            policy_version=decision.policy_version,
            created_at=self.timestamp,
            reason="Fake approval metadata recorded for contract pipeline tests.",
            metadata={
                "fake_recorder": "guardian_pipeline",
                "request_id": request.request_id,
            },
        )
        self.approval_recorder.record_approval(approval)
        return approval

    def _approval_method(self, decision: GuardianDecision) -> ApprovalMethod:
        if decision.status is GuardianDecisionStatus.NEEDS_OPERATOR_PIN:
            return ApprovalMethod.OPERATOR_PIN
        if decision.status is GuardianDecisionStatus.NEEDS_BREAKGLASS:
            return ApprovalMethod.BREAKGLASS
        if decision.status is GuardianDecisionStatus.ESCALATED:
            return ApprovalMethod.UNKNOWN
        return ApprovalMethod.UI_BUTTON

    def _record_events(
        self,
        request: ConsequentialActionRequest,
        policy_decision: PolicyDecision,
        guardian_decision: GuardianDecision,
        approval: ApprovalMetadata | None,
        lineage_id: str,
        result_status: str,
    ) -> Sequence[SpineEvent]:
        root_event_id = f"{lineage_id}:policy"
        events = [
            self._event(
                event_id=root_event_id,
                event_type=AuditEventType.POLICY_EVALUATED,
                status=AuditStatus.APPROVED if policy_decision.allowed else AuditStatus.NEEDS_APPROVAL,
                request=request,
                lineage_id=lineage_id,
                policy_decision=policy_decision,
                guardian_decision=None,
                approval=None,
                parent_event_id=None,
                root_event_id=root_event_id,
                summary="Fake policy decision recorded.",
            ),
            self._event(
                event_id=f"{lineage_id}:guardian",
                event_type=AuditEventType.GUARDIAN_DECISION,
                status=self._audit_status_for_decision(guardian_decision),
                request=request,
                lineage_id=lineage_id,
                policy_decision=policy_decision,
                guardian_decision=guardian_decision,
                approval=None,
                parent_event_id=root_event_id,
                root_event_id=root_event_id,
                summary="Fake Guardian decision recorded.",
            ),
        ]
        if approval is not None:
            events.append(
                self._event(
                    event_id=f"{lineage_id}:approval",
                    event_type=AuditEventType.APPROVAL_RECORDED,
                    status=AuditStatus.NEEDS_APPROVAL,
                    request=request,
                    lineage_id=lineage_id,
                    policy_decision=policy_decision,
                    guardian_decision=guardian_decision,
                    approval=approval,
                    parent_event_id=events[-1].event_id,
                    root_event_id=root_event_id,
                    summary="Fake approval metadata recorded.",
                )
            )
        events.append(
            self._event(
                event_id=f"{lineage_id}:result",
                event_type=AuditEventType.LINEAGE_CLOSED,
                status=result_status,
                request=request,
                lineage_id=lineage_id,
                policy_decision=policy_decision,
                guardian_decision=guardian_decision,
                approval=approval,
                parent_event_id=events[-1].event_id,
                root_event_id=root_event_id,
                summary="Fake pipeline lineage result recorded.",
            )
        )

        for event in events:
            self.spine_recorder.append_event(event)
        return tuple(events)

    def _event(
        self,
        event_id: str,
        event_type: AuditEventType,
        status: AuditStatus | str,
        request: ConsequentialActionRequest,
        lineage_id: str,
        policy_decision: PolicyDecision,
        guardian_decision: GuardianDecision | None,
        approval: ApprovalMetadata | None,
        parent_event_id: str | None,
        root_event_id: str,
        summary: str,
    ) -> SpineEvent:
        return SpineEvent(
            event_id=event_id,
            event_type=event_type,
            source="fake-guardian-pipeline",
            created_at=self._created_at,
            payload={
                "fake_pipeline": True,
                "non_executing": True,
                "policy_allowed": policy_decision.allowed,
            },
            lineage_id=lineage_id,
            status=status,
            actor_id=request.actor_id,
            shell_id=request.shell_id,
            input_id=request.input_id,
            intent_id=request.intent_id,
            decision_id=guardian_decision.decision_id if guardian_decision else None,
            approval_id=approval.approval_id if approval else None,
            policy_decision_id=policy_decision.policy_decision_id,
            parent_event_id=parent_event_id,
            root_event_id=root_event_id,
            action_type=request.action_type.value,
            target_ref=request.target_ref,
            tool_pack=request.requested_tool_pack,
            risk_class=request.risk_class,
            approval_level=guardian_decision.approval_level if guardian_decision else None,
            policy_version=guardian_decision.policy_version if guardian_decision else None,
            evidence_refs=request.evidence_refs,
            redacted_summary=summary,
            contains_secret=False,
            contains_biometric=False,
            contains_safety_critical=self._is_safety_critical(request),
        )

    def _record_lineage(
        self,
        request: ConsequentialActionRequest,
        policy_decision: PolicyDecision,
        guardian_decision: GuardianDecision,
        approval: ApprovalMetadata | None,
        lineage_id: str,
        event_ids: Sequence[str],
        result_status: str,
    ) -> None:
        record = AuditLineageRecord(
            lineage_id=lineage_id,
            root_event_id=event_ids[0] if event_ids else None,
            latest_event_id=event_ids[-1] if event_ids else None,
            input_id=request.input_id,
            intent_id=request.intent_id,
            decision_id=guardian_decision.decision_id,
            approval_id=approval.approval_id if approval else None,
            policy_decision_id=policy_decision.policy_decision_id,
            exposure_id=None,
            execution_id=None,
            actor_id=request.actor_id,
            shell_id=request.shell_id,
            risk_class=request.risk_class,
            status=result_status,
            created_at=self.timestamp,
            updated_at=self.timestamp,
            closed_at=self.timestamp,
            redacted_summary="Fake Guardian pipeline lineage summary.",
            contains_secret=False,
            contains_biometric=False,
            contains_safety_critical=self._is_safety_critical(request),
            metadata={
                "fake_pipeline": True,
                "non_executing": True,
            },
        )
        self.spine_recorder.record_lineage(record)
        self.spine_recorder.close_lineage(lineage_id, result_status)

    def _result_status(
        self,
        policy_decision: PolicyDecision,
        guardian_decision: GuardianDecision,
        approval: ApprovalMetadata | None,
    ) -> str:
        if guardian_decision.status is GuardianDecisionStatus.APPROVED and policy_decision.allowed:
            return AuditStatus.SUCCEEDED.value
        if guardian_decision.status is GuardianDecisionStatus.DENIED:
            return AuditStatus.DENIED.value
        if approval is not None:
            return AuditStatus.NEEDS_APPROVAL.value
        if guardian_decision.status is GuardianDecisionStatus.ESCALATED:
            return AuditStatus.ESCALATED.value
        return AuditStatus.BLOCKED.value

    def _audit_status_for_decision(self, decision: GuardianDecision) -> AuditStatus:
        if decision.status is GuardianDecisionStatus.APPROVED:
            return AuditStatus.APPROVED
        if decision.status is GuardianDecisionStatus.DENIED:
            return AuditStatus.DENIED
        if decision.status is GuardianDecisionStatus.NEEDS_HUMAN_CONFIRMATION:
            return AuditStatus.NEEDS_CONFIRMATION
        if decision.status in {
            GuardianDecisionStatus.NEEDS_OPERATOR_PIN,
            GuardianDecisionStatus.NEEDS_BREAKGLASS,
        }:
            return AuditStatus.NEEDS_APPROVAL
        if decision.status is GuardianDecisionStatus.ESCALATED:
            return AuditStatus.ESCALATED
        return AuditStatus.UNKNOWN

    def _is_safety_critical(self, request: ConsequentialActionRequest) -> bool:
        return request.risk_class == "critical" or request.action_type in {
            ConsequentialActionType.TERMINAL_COMMAND,
            ConsequentialActionType.ROBOT_ACTION,
            ConsequentialActionType.PAYMENT_ACTION,
            ConsequentialActionType.DEPLOY_ACTION,
            ConsequentialActionType.SECRET_ACCESS,
        }
