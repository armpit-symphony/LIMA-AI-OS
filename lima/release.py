"""Installed release-candidate identity and non-execution boundaries."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Final


PACKAGE_VERSION: Final[str] = "0.1.0rc1"
RELEASE_STAGE: Final[str] = "candidate_only"
MAIN_BASE_SHA: Final[str] = "deea1c4f5b6d3455a7e97e4b621e22b8d22a6244"
SUPPORTED_ENTRYPOINTS: Final[tuple[str, ...]] = (
    "lima.runtime.run_governed_request",
)
SUPPORTED_CONSUMERS: Final[tuple[str, ...]] = ("sparkbot", "arc-bot")
GUARDIAN_POLICY_SEAM: Final[str] = "guardian_core.policy"
PACKAGED_NAMESPACES: Final[tuple[str, ...]] = (
    "lima",
    "lima.contracts",
    "lima.governed_kernel",
)


@dataclass(frozen=True)
class RecoveryCheckpoint:
    """A historical checkpoint consolidated on the release-candidate base."""

    capability: str
    commit: str


RECOVERY_LINEAGE: Final[tuple[RecoveryCheckpoint, ...]] = (
    RecoveryCheckpoint(
        capability="governed dry-run runtime kernel",
        commit="702b0554203f83002815362c7fce783e18ddbf03",
    ),
    RecoveryCheckpoint(
        capability="Guardian Core policy integration seam",
        commit="17fab7cbf8befa846444437fd1108847c42ff9c0",
    ),
    RecoveryCheckpoint(
        capability="consumer checkpoint recovery manifest",
        commit="cbddc3c763565c6958d46711abc6195a792a2868",
    ),
    RecoveryCheckpoint(
        capability="Arc consumer runtime baseline",
        commit="04eb204a710c4e8f5f15759fbbe31e831a9a6029",
    ),
)

BLOCKED_CAPABILITIES: Final[tuple[str, ...]] = (
    "approval_execution",
    "provider_calls",
    "tool_calls",
    "connector_calls",
    "network_calls",
    "file_mutation",
    "credential_access",
    "background_actions",
    "robotics",
    "physical_world_actions",
    "side_effects",
)


def get_release_candidate_manifest() -> dict[str, object]:
    """Return JSON-safe installed-package identity and boundary evidence."""

    return {
        "package": "lima-runtime",
        "version": PACKAGE_VERSION,
        "stage": RELEASE_STAGE,
        "main_base_sha": MAIN_BASE_SHA,
        "supported_entrypoints": list(SUPPORTED_ENTRYPOINTS),
        "supported_consumers": list(SUPPORTED_CONSUMERS),
        "guardian_policy_seam": GUARDIAN_POLICY_SEAM,
        "packaged_namespaces": list(PACKAGED_NAMESPACES),
        "guardian_core_required": False,
        "recovery_lineage": [asdict(checkpoint) for checkpoint in RECOVERY_LINEAGE],
        "blocked_capabilities": list(BLOCKED_CAPABILITIES),
        "execution_allowed": False,
        "side_effects_allowed": False,
        "production_ready": False,
    }
