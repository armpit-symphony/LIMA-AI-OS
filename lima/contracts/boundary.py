"""Runtime boundary map contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Protocol, Sequence


class BoundaryClassification(str, Enum):
    SHELL_ADAPTER = "shell_adapter"
    HUMAN_INPUT_ADAPTER = "human_input_adapter"
    INTENT_BOUNDARY = "intent_boundary"
    GUARDIAN_CONTRACT = "guardian_contract"
    HARNESS_CONTRACT = "harness_contract"
    TOOL_PACK_CANDIDATE = "tool_pack_candidate"
    POLICY_CANDIDATE = "policy_candidate"
    APPROVAL_CANDIDATE = "approval_candidate"
    SPINE_AUDIT_CANDIDATE = "spine_audit_candidate"
    PRIVACY_REDACTION_CANDIDATE = "privacy_redaction_candidate"
    DRIVER_CANDIDATE = "driver_candidate"
    SYSTEM_SERVICE = "system_service"
    PERSISTENCE_CANDIDATE = "persistence_candidate"
    DO_NOT_EXTRACT_YET = "do_not_extract_yet"
    DEPRECATED_OR_UNSAFE_SHORTCUT = "deprecated_or_unsafe_shortcut"
    UNKNOWN = "unknown"


class ExtractionStatus(str, Enum):
    READY_FOR_ADAPTER_DESIGN = "ready_for_adapter_design"
    NEEDS_CONTRACT_REVIEW = "needs_contract_review"
    NEEDS_PACK_CLASSIFICATION = "needs_pack_classification"
    NEEDS_PRIVACY_REVIEW = "needs_privacy_review"
    NEEDS_DECISION_GATE = "needs_decision_gate"
    NEEDS_APPROVAL_METADATA = "needs_approval_metadata"
    NEEDS_LINEAGE_MAPPING = "needs_lineage_mapping"
    DO_NOT_EXTRACT_YET = "do_not_extract_yet"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class RuntimeBoundaryRecord:
    source_repo: str
    source_path: str
    surface_name: str
    current_role: str
    classification: BoundaryClassification | str
    future_lima_location: str
    required_contracts: Sequence[str]
    risk_level: str
    extraction_status: ExtractionStatus | str
    notes: str
    metadata: Mapping[str, Any] = field(default_factory=dict)


class BoundaryMapProtocol(Protocol):
    """Describe inspected runtime boundaries without extracting implementation."""

    def list_records(self) -> Sequence[RuntimeBoundaryRecord]:
        """Return contract-level boundary records."""
        ...
