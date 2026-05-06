"""IO driver contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal, Protocol

from .guardian import GuardianDecision


@dataclass(frozen=True)
class DriverCapability:
    name: str
    description: str
    risk_level: Literal["read_only", "low", "medium", "high", "blocked"]
    requires_approval: bool = True
    supports_dry_run: bool = True


@dataclass(frozen=True)
class DriverCommand:
    command_id: str
    capability: str
    args: dict[str, Any] = field(default_factory=dict)
    dry_run: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class DriverResult:
    command_id: str
    success: bool
    result: dict[str, Any] = field(default_factory=dict)
    telemetry: dict[str, Any] = field(default_factory=dict)
    error: str | None = None


class DriverProtocol(Protocol):
    """External driver boundary. Execution requires Guardian approval."""

    def declare_capabilities(self) -> tuple[DriverCapability, ...]:
        """Declare available driver capabilities."""
        ...

    async def dry_run(self, command: DriverCommand) -> DriverResult:
        """Preview a command without external side effects."""
        ...

    async def execute(self, command: DriverCommand, decision: GuardianDecision) -> DriverResult:
        """Execute only after Guardian approval or allow decision."""
        ...
