"""Consumer-facing decision contract for the governed dry-run runtime kernel."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

from .audit_event import GovernedAuditEvent


@dataclass(frozen=True)
class GovernedDecision:
    """Stable decision returned by the non-executing LIMA runtime API."""

    decision_id: str
    request_id: str
    consumer: str
    status: str
    allowed: bool
    requires_approval: bool
    risk_level: str
    reason_codes: Sequence[str]
    source_policy: str
    audit_event: GovernedAuditEvent
    executable: bool = False
    execution_allowed: bool = False
    side_effects_allowed: bool = False
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.executable or self.execution_allowed or self.side_effects_allowed:
            raise ValueError("governed decisions cannot authorize execution or side effects")

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "request_id": self.request_id,
            "consumer": self.consumer,
            "status": self.status,
            "allowed": self.allowed,
            "requires_approval": self.requires_approval,
            "risk_level": self.risk_level,
            "reason_codes": tuple(self.reason_codes),
            "source_policy": self.source_policy,
            "audit_event": self.audit_event.to_dict(),
            "executable": False,
            "execution_allowed": False,
            "side_effects_allowed": False,
            "metadata": dict(self.metadata),
        }
