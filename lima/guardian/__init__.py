"""Guardian implementation namespace reserved for future extraction."""

from .approval_fakes import FakeApprovalRecorder
from .decision_fakes import FakeGuardianDecisionEvaluator
from .fakes import FakeAuthProvider, FakeBreakglassProvider, FakeVaultProvider
from .policy_fakes import FakePolicyRiskEvaluator
from .spine_fakes import FakeSpineAuditRecorder

__all__ = [
    "FakeApprovalRecorder",
    "FakeAuthProvider",
    "FakeBreakglassProvider",
    "FakeGuardianDecisionEvaluator",
    "FakePolicyRiskEvaluator",
    "FakeSpineAuditRecorder",
    "FakeVaultProvider",
]
