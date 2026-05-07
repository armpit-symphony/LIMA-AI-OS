"""Tool-pack contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Protocol, Sequence


class ToolPackName(str, Enum):
    CORE = "core"
    MEMORY = "memory"
    FILES = "files"
    BROWSER = "browser"
    NETWORK = "network"
    COMMS = "comms"
    CALENDAR = "calendar"
    MEETING = "meeting"
    TERMINAL = "terminal"
    SYSTEM = "system"
    ADMIN = "admin"
    DEPLOY = "deploy"
    PAYMENTS = "payments"
    ROBO = "robo"
    SENSORS = "sensors"
    MODEL = "model"
    RESEARCH = "research"
    MODERATION = "moderation"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    description: str
    input_schema: Mapping[str, Any] = field(default_factory=dict)
    risk_tags: Sequence[str] = field(default_factory=tuple)
    requires_approval: bool = True


@dataclass(frozen=True)
class ToolPackManifest:
    pack_name: ToolPackName | str
    description: str
    default_risk_class: str
    allowed_action_types: Sequence[str] = field(default_factory=tuple)
    requires_decision: bool = True
    requires_approval_level: str | None = None
    tools: Sequence[str] = field(default_factory=tuple)
    constraints: Mapping[str, Any] = field(default_factory=dict)
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ShellToolScope:
    shell_id: str
    actor_id: str | None = None
    role_ref: str | None = None
    allowed_packs: Sequence[ToolPackName | str] = field(default_factory=tuple)
    denied_packs: Sequence[ToolPackName | str] = field(default_factory=tuple)
    default_packs: Sequence[ToolPackName | str] = field(default_factory=tuple)
    critical_packs: Sequence[ToolPackName | str] = field(default_factory=tuple)
    constraints: Mapping[str, Any] = field(default_factory=dict)
    policy_version: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ToolExposureRequest:
    request_id: str
    shell_id: str
    actor_id: str
    intent_id: str | None = None
    decision_id: str | None = None
    requested_packs: Sequence[ToolPackName | str] = field(default_factory=tuple)
    requested_tools: Sequence[str] = field(default_factory=tuple)
    risk_class: str = "medium"
    context_refs: Sequence[str] = field(default_factory=tuple)
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ToolExposureDecision:
    exposure_id: str
    request_id: str
    decision_id: str | None = None
    allowed_packs: Sequence[ToolPackName | str] = field(default_factory=tuple)
    denied_packs: Sequence[ToolPackName | str] = field(default_factory=tuple)
    selected_tools: Sequence[str] = field(default_factory=tuple)
    risk_class: str = "medium"
    constraints: Mapping[str, Any] = field(default_factory=dict)
    reason: str | None = None
    policy_version: str | None = None
    created_at: str = ""
    metadata: Mapping[str, Any] = field(default_factory=dict)


class ToolPackProtocol(Protocol):
    """A scoped collection of tools exposed to the Harness."""

    def declare_manifest(self) -> ToolPackManifest:
        """Return tool-pack metadata and definitions."""
        ...

    def list_tools(self) -> Sequence[str]:
        """List tool names in this pack without executing them."""
        ...
