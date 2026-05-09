"""Guardian implementation namespace reserved for future extraction."""

from .approval_fakes import FakeApprovalRecorder
from .decision_fakes import FakeGuardianDecisionEvaluator
from .fakes import FakeAuthProvider, FakeBreakglassProvider, FakeVaultProvider
from .pipeline_fakes import FakeGuardianPipeline, FakeGuardianPipelineResult
from .policy_fakes import FakePolicyRiskEvaluator
from .spine_fakes import FakeSpineAuditRecorder

__all__ = [
    "FakeApprovalRecorder",
    "FakeAuthProvider",
    "FakeBreakglassProvider",
    "FakeGuardianDecisionEvaluator",
    "FakeGuardianPipeline",
    "FakeGuardianPipelineResult",
    "FakePolicyRiskEvaluator",
    "FakeSpineAuditRecorder",
    "FakeVaultProvider",
]
