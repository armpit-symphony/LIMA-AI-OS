"""Non-executing LIMA Kernel coordination primitives."""

from .candidate_status import (
    ALLOWED_CANDIDATE_STATUSES,
    CandidateStatusError,
    normalize_candidate_status,
    validate_candidate,
)
from .candidate_preview import CandidatePreview, preview_candidate
from .discovery import (
    DiscoveryAdapterManifest,
    DiscoveryAdapterRequest,
    DiscoveryAdapterResult,
    DiscoveryAdapterSurface,
    SimulatedDiscoveryAdapter,
)
from .intake_candidate import IntakeCandidateError, build_intake_candidate
from .kernel import LimaKernel
from .plugin_contract import (
    CapabilityProfile,
    ExecutionResult,
    GuardianStubDecision,
    KernelEvent,
    KernelRequest,
)
from .runtime_state import RuntimeStateSnapshot, inspect_runtime_state

__all__ = [
    "ALLOWED_CANDIDATE_STATUSES",
    "CapabilityProfile",
    "CandidatePreview",
    "CandidateStatusError",
    "DiscoveryAdapterManifest",
    "DiscoveryAdapterRequest",
    "DiscoveryAdapterResult",
    "DiscoveryAdapterSurface",
    "ExecutionResult",
    "GuardianStubDecision",
    "IntakeCandidateError",
    "KernelEvent",
    "KernelRequest",
    "LimaKernel",
    "RuntimeStateSnapshot",
    "SimulatedDiscoveryAdapter",
    "build_intake_candidate",
    "inspect_runtime_state",
    "normalize_candidate_status",
    "preview_candidate",
    "validate_candidate",
]
