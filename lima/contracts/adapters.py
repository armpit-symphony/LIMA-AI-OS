"""Describe-only adapter contracts for HumanInput surface mapping."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Protocol, Sequence


class HumanInputAdapterSurface(str, Enum):
    CHAT_MESSAGE = "chat_message"
    VOICE_TRANSCRIPT = "voice_transcript"
    MEETING_PROMPT = "meeting_prompt"
    SPARKBUD_PROMPT = "sparkbud_prompt"
    WORKSTATION_COMMAND = "workstation_command"
    OPERATOR_CONSOLE = "operator_console"
    TERMINAL_REQUEST = "terminal_request"
    APPROVAL_RESPONSE = "approval_response"
    MCP_REQUEST = "mcp_request"
    ROBOT_REQUEST = "robot_request"
    FRONTEND_CHAT = "frontend_chat"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class HumanInputAdapterMapping:
    surface: HumanInputAdapterSurface | str
    source_path: str | None
    source_name: str
    human_input_source: str
    shell_id: str | None
    actor_ref: str | None
    session_ref: str | None
    source_ref: str | None
    privacy_class: str
    redaction_class: str
    risk_notes: str | None = None
    shortcut_risks: Sequence[str] = field(default_factory=tuple)
    notes: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class HumanInputAdapterDesign:
    design_id: str
    source_system: str
    mappings: Sequence[HumanInputAdapterMapping]
    blocked_shortcuts: Sequence[str] = field(default_factory=tuple)
    lineage_notes: Sequence[str] = field(default_factory=tuple)
    privacy_notes: Sequence[str] = field(default_factory=tuple)
    created_at: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


class AdapterDesignProtocol(Protocol):
    """Describe input adapter mappings without adapting or executing live data."""

    def describe_mappings(self) -> Sequence[HumanInputAdapterMapping]:
        """Return design-time HumanInput mapping records."""
        ...

    def describe_design(self) -> HumanInputAdapterDesign:
        """Return the full design-time adapter contract record."""
        ...
