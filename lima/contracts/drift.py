"""Describe-only payload drift review contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Protocol, Sequence


class DriftStatus(str, Enum):
    CURRENT = "current"
    NEEDS_REVIEW = "needs_review"
    STALE = "stale"
    UNKNOWN = "unknown"


class DriftDecision(str, Enum):
    NO_DRIFT = "no_drift"
    FIXTURE_UPDATE_REQUIRED = "fixture_update_required"
    CHANGED_NOT_ADAPTER_RELEVANT = "sparkbot_changed_not_adapter_relevant"
    REVIEW_BLOCKED_DIRTY_SOURCE = "review_blocked_dirty_source"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class PayloadFixtureDriftRecord:
    fixture_id: str
    source_surface: str
    sparkbot_reference_path: str
    inspected_commit: str
    reviewed_against: str
    drift_status: DriftStatus | str
    drift_decision: DriftDecision | str
    shape_version: str | None = None
    drift_notes: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class PayloadDriftReview:
    review_id: str
    sparkbot_commit: str
    local_worktree_dirty: bool
    fixture_records: Sequence[PayloadFixtureDriftRecord]
    decision: DriftDecision | str
    reviewed_at: str
    notes: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


class PayloadDriftReviewProtocol(Protocol):
    def describe_review(self) -> PayloadDriftReview:
        """Describe a payload drift review without importing or executing Sparkbot."""
