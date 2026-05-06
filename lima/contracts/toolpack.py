"""Tool-pack contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    description: str
    input_schema: dict[str, Any] = field(default_factory=dict)
    risk_tags: tuple[str, ...] = ()
    requires_approval: bool = True


@dataclass(frozen=True)
class ToolPackManifest:
    pack_id: str
    name: str
    tools: tuple[ToolDefinition, ...] = ()
    description: str | None = None


class ToolPackProtocol(Protocol):
    """A scoped collection of tools exposed to the Harness."""

    def manifest(self) -> ToolPackManifest:
        """Return tool-pack metadata and definitions."""
        ...

    def list_tools(self) -> tuple[ToolDefinition, ...]:
        """List tools in this pack."""
        ...
