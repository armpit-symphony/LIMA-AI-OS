"""Extraction readiness review contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Sequence


class ReadinessStatus(str, Enum):
    READY = "ready"
    READY_WITH_CONSTRAINTS = "ready_with_constraints"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"


class ReadinessArea(str, Enum):
    ARCHITECTURE = "architecture"
    CONTRACTS = "contracts"
    GUARDIAN = "guardian"
    HARNESS = "harness"
    TOOL_PACKS = "tool_packs"
    APPROVALS = "approvals"
    SPINE_AUDIT = "spine_audit"
    PRIVACY = "privacy"
    ROBOTICS = "robotics"
    TERMINAL = "terminal"
    PERSISTENCE = "persistence"
    ADAPTERS = "adapters"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class ExtractionReadinessRecord:
    area: ReadinessArea | str
    status: ReadinessStatus | str
    score: int
    blockers: Sequence[str] = ()
    ready_items: Sequence[str] = ()
    next_action: str = ""
    metadata: Mapping[str, Any] = field(default_factory=dict)
