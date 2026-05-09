"""In-memory approval metadata recorder fakes for contract validation."""

from __future__ import annotations

from collections.abc import Iterable, Sequence

from lima.contracts.approval import (
    ApprovalMetadata,
    ApprovalMethod,
    ApprovalProtocol,
    ApprovalScope,
    ApprovalStatus,
)


class FakeApprovalRecorder(ApprovalProtocol):
    """In-memory approval metadata recorder for tests."""

    def __init__(
        self,
        approvals: Iterable[ApprovalMetadata] = (),
        scopes: Iterable[ApprovalScope] = (),
        timestamp: str = "2026-01-01T00:00:00Z",
        default_status: ApprovalStatus = ApprovalStatus.PENDING,
        default_method: ApprovalMethod = ApprovalMethod.UI_BUTTON,
    ) -> None:
        self.timestamp = timestamp
        self.default_status = default_status
        self.default_method = default_method
        self._approvals = {approval.approval_id: approval for approval in approvals}
        self._scopes = {scope.decision_id: scope for scope in scopes}

    def describe_required_approval(self, scope: ApprovalScope) -> ApprovalMetadata | None:
        self.record_scope(scope)
        for approval in self._approvals.values():
            if approval.decision_id == scope.decision_id:
                return approval
        return None

    def record_approval(self, approval: ApprovalMetadata) -> None:
        self._approvals[approval.approval_id] = approval

    def record_scope(self, scope: ApprovalScope) -> None:
        self._scopes[scope.decision_id] = scope

    def get_approval(self, approval_id: str) -> ApprovalMetadata | None:
        return self._approvals.get(approval_id)

    def get_scope(self, decision_id: str) -> ApprovalScope | None:
        return self._scopes.get(decision_id)

    def list_approvals(self) -> Sequence[ApprovalMetadata]:
        return tuple(self._approvals.values())

    def list_scopes(self) -> Sequence[ApprovalScope]:
        return tuple(self._scopes.values())
