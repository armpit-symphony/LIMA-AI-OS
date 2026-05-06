"""Shell contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


@dataclass(frozen=True)
class ShellManifest:
    shell_id: str
    name: str
    allowed_tool_packs: tuple[str, ...] = ()
    permissions: tuple[str, ...] = ()
    description: str | None = None
    metadata: dict[str, str] = field(default_factory=dict)


class ShellProtocol(Protocol):
    """User- or environment-facing runtime consumer."""

    def manifest(self) -> ShellManifest:
        """Return shell identity, tool-pack scope, and permissions."""
        ...

    def declare_tool_packs(self) -> tuple[str, ...]:
        """Declare allowed tool packs for this shell."""
        ...

    def declare_permissions(self) -> tuple[str, ...]:
        """Declare shell permissions requested from Guardian."""
        ...
