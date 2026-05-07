"""Model Harness contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol

from .guardian import GuardianDecision
from .toolpack import ToolExposureDecision


@dataclass(frozen=True)
class ModelRequest:
    prompt: str
    model_hint: str | None = None
    tool_pack_scope: tuple[str, ...] = ()
    selected_tools: tuple[str, ...] = ()
    tool_exposure: ToolExposureDecision | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ModelResponse:
    content: str
    model_used: str
    stop_reason: str | None = None
    usage: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


class HarnessProtocol(Protocol):
    """Model routing and scoped tool planning surface."""

    async def complete(self, request: ModelRequest, decision: GuardianDecision) -> ModelResponse:
        """Run a consequential model call only with a Guardian decision_id."""
        ...

    async def plan_tool_call(self, request: ModelRequest) -> Any:
        """Plan from selected tools only, without executing the tool call."""
        ...

    async def execute_guarded_tool_call(self, tool_call: Any, decision: GuardianDecision) -> Any:
        """Execute a tool call only with a Guardian decision_id."""
        ...
