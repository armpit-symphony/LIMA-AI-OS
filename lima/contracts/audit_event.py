"""Audit event contract for the governed dry-run runtime kernel."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence


@dataclass(frozen=True)
class GovernedAuditEvent:
    """Non-persistent audit event carried on every governed decision."""

    event_id: str
    request_id: str
    decision_id: str
    consumer: str
    actor_id: str
    surface: str
    status: str
    reason_codes: Sequence[str] = field(default_factory=tuple)
    evidence_refs: Sequence[str] = field(default_factory=tuple)
    source_policy: str = "lima.guardian.policy_adapter:v0.1"
    executable: bool = False
    execution_allowed: bool = False
    side_effects_allowed: bool = False
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.executable or self.execution_allowed or self.side_effects_allowed:
            raise ValueError("governed audit events cannot authorize execution or side effects")

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "request_id": self.request_id,
            "decision_id": self.decision_id,
            "consumer": self.consumer,
            "actor_id": self.actor_id,
            "surface": self.surface,
            "status": self.status,
            "reason_codes": tuple(self.reason_codes),
            "evidence_refs": tuple(self.evidence_refs),
            "source_policy": self.source_policy,
            "executable": False,
            "execution_allowed": False,
            "side_effects_allowed": False,
            "metadata": dict(self.metadata),
        }
