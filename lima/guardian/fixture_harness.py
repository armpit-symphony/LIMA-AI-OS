"""Non-production harness for LIMA-owned adapter fixtures."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field, replace
from typing import Any

from lima.adapters import (
    SparkbotChatInputPayload,
    SparkbotHumanInputAdapter,
    SparkbotMeetingInputPayload,
    SparkbotOperatorInputPayload,
    SparkbotVoiceInputPayload,
)
from lima.contracts.guardian import ConsequentialActionType
from lima.contracts.intent import HumanInput

from .humaninput_pipeline_fakes import HumanInputFakePipelineBridge
from .pipeline_fakes import FakeGuardianPipelineResult


@dataclass(frozen=True)
class AdapterFixtureHarnessResult:
    fixture_id: str
    source_surface: str
    human_input: HumanInput
    pipeline_result: FakeGuardianPipelineResult
    expected_humaninput_source: str
    status: str
    metadata: Mapping[str, Any] = field(default_factory=dict)


class AdapterFixtureHarness:
    """Run synthetic payload fixtures through the adapter and fake pipeline."""

    def __init__(
        self,
        adapter: SparkbotHumanInputAdapter,
        bridge: HumanInputFakePipelineBridge,
    ) -> None:
        self.adapter = adapter
        self.bridge = bridge

    def run_fixture(self, fixture: Mapping[str, Any]) -> AdapterFixtureHarnessResult:
        fixture_id = self._required_str(fixture, "fixture_id")
        source_surface = self._required_str(fixture, "source_surface")
        payload = self._payload(fixture)
        human_input = self._adapt_fixture(fixture_id, source_surface, payload)
        pipeline_result = self.bridge.evaluate_human_input(human_input)
        return AdapterFixtureHarnessResult(
            fixture_id=fixture_id,
            source_surface=source_surface,
            human_input=human_input,
            pipeline_result=pipeline_result,
            expected_humaninput_source=self._required_str(
                fixture,
                "expected_humaninput_source",
            ),
            status=pipeline_result.status,
            metadata={
                "fixture_harness": "nonproduction_adapter_fixture",
                "test_only": True,
                "non_production": True,
                "non_executing": True,
                "fixture_mirror_only": True,
                "source_surface": source_surface,
                "fixture_id": fixture_id,
                "pipeline_status": pipeline_result.status,
                "pipeline_lineage_id": pipeline_result.lineage_id,
            },
        )

    def run_fixtures(
        self,
        fixtures: Sequence[Mapping[str, Any]],
    ) -> Sequence[AdapterFixtureHarnessResult]:
        return tuple(self.run_fixture(fixture) for fixture in fixtures)

    def _adapt_fixture(
        self,
        fixture_id: str,
        source_surface: str,
        payload: Mapping[str, Any],
    ) -> HumanInput:
        if source_surface.startswith("chat_"):
            return self._with_bridge_metadata(
                self.adapter.adapt_chat_payload(
                    SparkbotChatInputPayload(
                        message_id=str(payload.get("message_id") or fixture_id),
                        actor_ref=self._required_str(payload, "actor_ref"),
                        shell_id=self._required_str(payload, "shell_id"),
                        session_ref=self._optional_str(payload.get("session_ref")),
                        text=self._optional_str(payload.get("content")),
                        source_ref=self._optional_str(
                            payload.get("room_id") or payload.get("client_msg_id"),
                        ),
                        metadata=self._payload_metadata(
                            fixture_id=fixture_id,
                            source_surface=source_surface,
                        ),
                    )
                )
            )

        if source_surface.startswith("voice_"):
            return self._with_bridge_metadata(
                self.adapter.adapt_voice_payload(
                    SparkbotVoiceInputPayload(
                        transcript_ref=self._required_str(payload, "transcript_ref"),
                        actor_ref=self._required_str(payload, "actor_ref"),
                        shell_id=self._required_str(payload, "shell_id"),
                        session_ref=self._optional_str(payload.get("session_ref")),
                        confidence=self._optional_float(payload.get("confidence")),
                        metadata=self._payload_metadata(
                            fixture_id=fixture_id,
                            source_surface=source_surface,
                            voice_recognition_performed=False,
                        ),
                    )
                )
            )

        if source_surface.startswith("meeting_"):
            return self._with_bridge_metadata(
                self.adapter.adapt_meeting_payload(
                    SparkbotMeetingInputPayload(
                        meeting_id=self._required_str(payload, "meeting_id"),
                        room_id=self._optional_str(payload.get("room_id")),
                        actor_ref=self._required_str(payload, "actor_ref"),
                        shell_id=self._required_str(payload, "shell_id"),
                        prompt=self._optional_str(payload.get("prompt")),
                        prompt_ref=self._optional_str(
                            payload.get("prompt_ref")
                            or payload.get("content_markdown_ref"),
                        ),
                        metadata=self._payload_metadata(
                            fixture_id=fixture_id,
                            source_surface=source_surface,
                        ),
                    )
                )
            )

        metadata = self._operator_metadata(
            fixture_id=fixture_id,
            source_surface=source_surface,
            payload=payload,
        )
        return self._with_bridge_metadata(
            self.adapter.adapt_operator_payload(
                SparkbotOperatorInputPayload(
                    actor_ref=self._required_str(payload, "actor_ref"),
                    shell_id=self._required_str(payload, "shell_id"),
                    session_ref=self._optional_str(payload.get("session_ref")),
                    command=self._optional_str(
                        payload.get("requested_action") or payload.get("user_request"),
                    ),
                    command_ref=self._optional_str(
                        payload.get("command_ref") or payload.get("requested_action_ref"),
                    ),
                    metadata=metadata,
                )
            )
        )

    def _operator_metadata(
        self,
        *,
        fixture_id: str,
        source_surface: str,
        payload: Mapping[str, Any],
    ) -> Mapping[str, Any]:
        if source_surface.startswith("robotics_"):
            return self._payload_metadata(
                fixture_id=fixture_id,
                source_surface=source_surface,
                action_type=ConsequentialActionType.ROBOT_ACTION.value,
                risk_class="critical",
                target_ref=self._optional_str(payload.get("robot_id")),
                requested_tool_pack="robo",
                safety_critical=True,
                physical_action_performed=False,
            )
        if source_surface.startswith("mcp_"):
            return self._payload_metadata(
                fixture_id=fixture_id,
                source_surface=source_surface,
                action_type=ConsequentialActionType.TOOL_CALL.value,
                risk_class="high",
                target_ref=self._optional_str(
                    payload.get("manifest_id") or payload.get("run_id"),
                ),
                requested_tool_pack="unknown",
                tool_execution_performed=False,
                unsupported_nonexecuting=False,
            )
        if "terminal" in source_surface:
            return self._payload_metadata(
                fixture_id=fixture_id,
                source_surface=source_surface,
                action_type=ConsequentialActionType.TERMINAL_COMMAND.value,
                risk_class="critical",
                target_ref=self._optional_str(payload.get("station_id")),
                requested_tool_pack="terminal",
                terminal_opened=False,
            )
        return self._payload_metadata(
            fixture_id=fixture_id,
            source_surface=source_surface,
        )

    def _payload_metadata(
        self,
        *,
        fixture_id: str,
        source_surface: str,
        **extra: Any,
    ) -> Mapping[str, Any]:
        metadata: dict[str, Any] = {
            "fixture_id": fixture_id,
            "source_surface": source_surface,
            "fixture_harness": "nonproduction_adapter_fixture",
            "fixture_mirror_only": True,
            "test_only": True,
            "non_production": True,
            "non_executing": True,
            "model_call_performed": False,
            "tool_execution_performed": False,
            "driver_call_performed": False,
            "persistence_performed": False,
            "intent_inference_performed": False,
        }
        metadata.update(extra)
        return metadata

    def _with_bridge_metadata(self, human_input: HumanInput) -> HumanInput:
        payload_metadata = human_input.metadata.get("payload_metadata")
        if not isinstance(payload_metadata, Mapping):
            return human_input

        bridge_keys = (
            "action_type",
            "risk_class",
            "target_ref",
            "requested_tool_pack",
            "typed_args",
            "evidence_refs",
            "non_executing",
            "test_only",
            "non_production",
            "fixture_mirror_only",
        )
        bridge_metadata = {
            key: payload_metadata[key]
            for key in bridge_keys
            if key in payload_metadata
        }
        if not bridge_metadata:
            return human_input
        return replace(
            human_input,
            metadata={
                **dict(human_input.metadata),
                **bridge_metadata,
            },
        )

    def _payload(self, fixture: Mapping[str, Any]) -> Mapping[str, Any]:
        payload = fixture.get("payload")
        if not isinstance(payload, Mapping):
            raise ValueError("fixture payload must be a mapping")
        return payload

    def _required_str(self, mapping: Mapping[str, Any], key: str) -> str:
        value = mapping.get(key)
        if not isinstance(value, str) or not value:
            raise ValueError(f"{key} must be a non-empty string")
        return value

    def _optional_str(self, value: object) -> str | None:
        if isinstance(value, str) and value:
            return value
        return None

    def _optional_float(self, value: object) -> float | None:
        if isinstance(value, (float, int)):
            return float(value)
        return None
