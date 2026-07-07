"""Non-production adapter skeletons for LIMA-owned input boundaries."""

from .sparkbot_humaninput import (
    SparkbotChatInputPayload,
    SparkbotHumanInputAdapter,
    SparkbotMeetingInputPayload,
    SparkbotOperatorInputPayload,
    SparkbotVoiceInputPayload,
)
from .v1_consumer_integration_compatibility import (
    V1ConsumerIntegrationCompatibilityError,
    validate_v1_consumer_integration_compatibility_freeze,
)
from .v1_consumer_evidence_envelope import (
    V1ConsumerEvidenceEnvelope,
    V1ConsumerEvidenceEnvelopeError,
    build_v1_consumer_evidence_envelope,
)
from .v1_consumer_import_dry_run import (
    V1ConsumerImportDryRunError,
    validate_v1_consumer_integration_proof_to_import_dry_run,
)
from .v1_shell_runtime_adapter import (
    V1ShellGovernedRuntimeResponse,
    V1ShellRuntimeAdapterError,
    V1ShellRuntimeInput,
    build_v1_shell_runtime_candidate,
    run_v1_shell_governed_preflight,
)

__all__ = [
    "SparkbotChatInputPayload",
    "SparkbotHumanInputAdapter",
    "SparkbotMeetingInputPayload",
    "SparkbotOperatorInputPayload",
    "SparkbotVoiceInputPayload",
    "V1ConsumerEvidenceEnvelope",
    "V1ConsumerEvidenceEnvelopeError",
    "V1ConsumerImportDryRunError",
    "V1ConsumerIntegrationCompatibilityError",
    "V1ShellGovernedRuntimeResponse",
    "V1ShellRuntimeAdapterError",
    "V1ShellRuntimeInput",
    "build_v1_consumer_evidence_envelope",
    "build_v1_shell_runtime_candidate",
    "run_v1_shell_governed_preflight",
    "validate_v1_consumer_integration_proof_to_import_dry_run",
    "validate_v1_consumer_integration_compatibility_freeze",
]
