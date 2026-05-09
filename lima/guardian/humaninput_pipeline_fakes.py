"""Test-only bridge from HumanInput records to the fake Guardian pipeline."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from lima.contracts.guardian import ConsequentialActionRequest, ConsequentialActionType
from lima.contracts.intent import HumanInput

from .pipeline_fakes import FakeGuardianPipeline, FakeGuardianPipelineResult


@dataclass(frozen=True)
class HumanInputPipelineBridgeConfig:
    default_action_type: ConsequentialActionType | str = ConsequentialActionType.UNKNOWN
    default_risk_class: str = "medium"
    default_target_ref: str | None = None
    default_requested_tool_pack: str | None = None
    default_timestamp: str = "2026-01-01T00:00:00Z"


class HumanInputFakePipelineBridge:
    """Build test-only Guardian requests from explicit HumanInput metadata."""

    def __init__(
        self,
        pipeline: FakeGuardianPipeline,
        config: HumanInputPipelineBridgeConfig | None = None,
    ) -> None:
        self.pipeline = pipeline
        self.config = config or HumanInputPipelineBridgeConfig()

    def evaluate_human_input(self, human_input: HumanInput) -> FakeGuardianPipelineResult:
        request = self._request_from_human_input(human_input)
        return self.pipeline.evaluate_request(request)

    def _request_from_human_input(
        self,
        human_input: HumanInput,
    ) -> ConsequentialActionRequest:
        metadata = human_input.metadata
        action_type = self._action_type(metadata.get("action_type"))
        risk_class = self._risk_class(metadata)
        target_ref = self._optional_str(
            metadata.get("target_ref"),
            self.config.default_target_ref,
        )
        requested_tool_pack = self._optional_str(
            metadata.get("requested_tool_pack"),
            self.config.default_requested_tool_pack,
        )

        return ConsequentialActionRequest(
            request_id=self._request_id(human_input, metadata),
            intent_id=None,
            input_id=human_input.input_id,
            actor_id=human_input.actor_id,
            shell_id=human_input.shell_id,
            action_type=action_type,
            target_ref=target_ref,
            requested_tool_pack=requested_tool_pack,
            risk_class=risk_class,
            typed_args=self._typed_args(metadata),
            evidence_refs=self._evidence_refs(metadata),
            metadata=self._request_metadata(human_input),
        )

    def _action_type(self, value: object) -> ConsequentialActionType:
        if value is None:
            return self._configured_action_type()
        if isinstance(value, ConsequentialActionType):
            return value
        if isinstance(value, str):
            normalized = value.lower()
            for action_type in ConsequentialActionType:
                if normalized in {action_type.value, action_type.name.lower()}:
                    return action_type
        return ConsequentialActionType.UNKNOWN

    def _configured_action_type(self) -> ConsequentialActionType:
        configured = self.config.default_action_type
        if isinstance(configured, ConsequentialActionType):
            return configured
        if configured is None:
            return ConsequentialActionType.UNKNOWN
        return self._action_type(configured)

    def _risk_class(self, metadata: Mapping[str, Any]) -> str:
        value = metadata.get("risk_class")
        if isinstance(value, str) and value:
            return value
        return self.config.default_risk_class

    def _request_id(
        self,
        human_input: HumanInput,
        metadata: Mapping[str, Any],
    ) -> str:
        value = metadata.get("request_id")
        if isinstance(value, str) and value:
            return value
        return f"fake-humaninput:{human_input.input_id}"

    def _typed_args(self, metadata: Mapping[str, Any]) -> Mapping[str, Any]:
        value = metadata.get("typed_args")
        if isinstance(value, Mapping):
            return dict(value)
        return {}

    def _evidence_refs(self, metadata: Mapping[str, Any]) -> Sequence[str]:
        value = metadata.get("evidence_refs")
        if isinstance(value, str):
            return (value,)
        if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
            return tuple(item for item in value if isinstance(item, str))
        return ()

    def _optional_str(self, value: object, default: str | None) -> str | None:
        if isinstance(value, str) and value:
            return value
        return default

    def _request_metadata(self, human_input: HumanInput) -> Mapping[str, Any]:
        metadata = human_input.metadata
        return {
            "bridge": "humaninput_fake_pipeline",
            "test_only": True,
            "non_executing": True,
            "human_input_source": human_input.source.value,
            "content_ref": human_input.content_ref,
            "confidence": human_input.confidence,
            "privacy_class": human_input.privacy_class,
            "redaction_class": metadata.get("redaction_class"),
            "session_ref": metadata.get("session_ref"),
            "source_ref": metadata.get("source_ref"),
            "trusted_context_ref": metadata.get("trusted_context_ref"),
            "autonomy_notes": metadata.get("autonomy_notes"),
            "timestamp": self.config.default_timestamp,
        }
