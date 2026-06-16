"""Guardian implementation namespace reserved for future extraction."""

from .approval_fakes import FakeApprovalRecorder
from .decision_fakes import FakeGuardianDecisionEvaluator
from .fakes import FakeAuthProvider, FakeBreakglassProvider, FakeVaultProvider
from .humaninput_pipeline_fakes import (
    HumanInputFakePipelineBridge,
    HumanInputPipelineBridgeConfig,
)
from .fixture_harness import AdapterFixtureHarness, AdapterFixtureHarnessResult
from .pipeline_fakes import FakeGuardianPipeline, FakeGuardianPipelineResult
from .policy_fakes import FakePolicyRiskEvaluator
from .spine_fakes import FakeSpineAuditRecorder
from .v1_approval_enforcement import (
    V1ApprovalEnforcementError,
    enforce_v1_destructive_approval,
)
from .v1_decision_gate import V1GuardianDecisionGateError, review_v1_runtime_request
from .v1_file_mutation_policy import (
    V1FileMutationPolicyError,
    validate_v1_guarded_file_mutation_policy,
)

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
    "AdapterFixtureHarness",
    "AdapterFixtureHarnessResult",
    "HumanInputFakePipelineBridge",
    "HumanInputPipelineBridgeConfig",
    "V1ApprovalEnforcementError",
    "V1FileMutationPolicyError",
    "V1GuardianDecisionGateError",
    "enforce_v1_destructive_approval",
    "review_v1_runtime_request",
    "validate_v1_guarded_file_mutation_policy",
]
