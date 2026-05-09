"""Neutral Sparkbot-style payload conversion into LIMA HumanInput records."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Any, Mapping

from lima.contracts.intent import HumanInput, HumanInputSource
from lima.contracts.privacy import PrivacyClass, RedactionClass


@dataclass(frozen=True)
class SparkbotChatInputPayload:
    message_id: str
    actor_ref: str
    shell_id: str
    session_ref: str | None = None
    text: str | None = None
    text_ref: str | None = None
    source_ref: str | None = None
    trusted_context_ref: str | None = None
    autonomy_notes: Mapping[str, Any] = field(default_factory=dict)
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SparkbotVoiceInputPayload:
    transcript_ref: str
    actor_ref: str
    shell_id: str
    session_ref: str | None = None
    confidence: float | None = None
    trusted_context_ref: str | None = None
    autonomy_notes: Mapping[str, Any] = field(default_factory=dict)
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SparkbotMeetingInputPayload:
    meeting_id: str
    actor_ref: str
    shell_id: str
    room_id: str | None = None
    prompt: str | None = None
    prompt_ref: str | None = None
    trusted_context_ref: str | None = None
    autonomy_notes: Mapping[str, Any] = field(default_factory=dict)
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SparkbotOperatorInputPayload:
    actor_ref: str
    shell_id: str
    session_ref: str | None = None
    command: str | None = None
    command_ref: str | None = None
    trusted_context_ref: str | None = None
    autonomy_notes: Mapping[str, Any] = field(default_factory=dict)
    metadata: Mapping[str, Any] = field(default_factory=dict)


def _build_input_id(prefix: str, *parts: str | None) -> str:
    """Build a stable local input id without touching outside systems."""

    material = "\x1f".join(part for part in parts if part)
    digest = hashlib.sha256(f"{prefix}\x1f{material}".encode("utf-8")).hexdigest()
    return f"{prefix}-{digest[:16]}"


def _base_metadata(
    *,
    surface: str,
    privacy_class: PrivacyClass,
    redaction_class: RedactionClass,
    trusted_context_ref: str | None,
    autonomy_notes: Mapping[str, Any],
    payload_metadata: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "adapter": "sparkbot_humaninput",
        "surface": surface,
        "non_production": True,
        "privacy_class": privacy_class.value,
        "redaction_class": redaction_class.value,
        "trusted_context_ref": trusted_context_ref,
        "autonomy_notes": dict(autonomy_notes),
        "autonomy_metadata_passive": True,
        "payload_metadata": dict(payload_metadata),
    }


class SparkbotHumanInputAdapter:
    """Pure conversion skeleton for neutral payloads."""

    def adapt_chat_payload(self, payload: SparkbotChatInputPayload) -> HumanInput:
        redaction_class = (
            RedactionClass.REFERENCE_ONLY
            if payload.text is None and payload.text_ref
            else RedactionClass.SUMMARY_ONLY
        )
        metadata = _base_metadata(
            surface="chat_message",
            privacy_class=PrivacyClass.PRIVATE,
            redaction_class=redaction_class,
            trusted_context_ref=payload.trusted_context_ref,
            autonomy_notes=payload.autonomy_notes,
            payload_metadata=payload.metadata,
        )
        metadata.update(
            {
                "message_id": payload.message_id,
                "session_ref": payload.session_ref,
                "source_ref": payload.source_ref,
            }
        )
        return HumanInput(
            input_id=_build_input_id(
                "sparkbot-chat",
                payload.message_id,
                payload.source_ref,
                payload.text_ref,
                payload.text,
            ),
            source=HumanInputSource.TEXT,
            actor_id=payload.actor_ref,
            shell_id=payload.shell_id,
            content_ref=payload.text_ref,
            raw_text=payload.text,
            privacy_class=PrivacyClass.PRIVATE.value,
            metadata=metadata,
        )

    def adapt_voice_payload(self, payload: SparkbotVoiceInputPayload) -> HumanInput:
        metadata = _base_metadata(
            surface="voice_transcript",
            privacy_class=PrivacyClass.PRIVATE,
            redaction_class=RedactionClass.REFERENCE_ONLY,
            trusted_context_ref=payload.trusted_context_ref,
            autonomy_notes=payload.autonomy_notes,
            payload_metadata=payload.metadata,
        )
        metadata.update(
            {
                "session_ref": payload.session_ref,
                "transcript_ref": payload.transcript_ref,
                "contains_biometric_signal": True,
                "biometric_handling_note": "voice evidence may require biometric handling",
            }
        )
        return HumanInput(
            input_id=_build_input_id(
                "sparkbot-voice",
                payload.transcript_ref,
                payload.actor_ref,
                payload.session_ref,
            ),
            source=HumanInputSource.VOICE,
            actor_id=payload.actor_ref,
            shell_id=payload.shell_id,
            content_ref=payload.transcript_ref,
            raw_text=None,
            confidence=payload.confidence,
            privacy_class=PrivacyClass.PRIVATE.value,
            metadata=metadata,
        )

    def adapt_meeting_payload(self, payload: SparkbotMeetingInputPayload) -> HumanInput:
        redaction_class = (
            RedactionClass.REFERENCE_ONLY
            if payload.prompt is None and payload.prompt_ref
            else RedactionClass.SUMMARY_ONLY
        )
        metadata = _base_metadata(
            surface="meeting_prompt",
            privacy_class=PrivacyClass.CONFIDENTIAL,
            redaction_class=redaction_class,
            trusted_context_ref=payload.trusted_context_ref,
            autonomy_notes=payload.autonomy_notes,
            payload_metadata=payload.metadata,
        )
        metadata.update(
            {
                "meeting_id": payload.meeting_id,
                "room_id": payload.room_id,
            }
        )
        return HumanInput(
            input_id=_build_input_id(
                "sparkbot-meeting",
                payload.meeting_id,
                payload.room_id,
                payload.prompt_ref,
                payload.prompt,
            ),
            source=HumanInputSource.TEXT,
            actor_id=payload.actor_ref,
            shell_id=payload.shell_id,
            content_ref=payload.prompt_ref,
            raw_text=payload.prompt,
            privacy_class=PrivacyClass.CONFIDENTIAL.value,
            metadata=metadata,
        )

    def adapt_operator_payload(self, payload: SparkbotOperatorInputPayload) -> HumanInput:
        metadata = _base_metadata(
            surface="operator_console",
            privacy_class=PrivacyClass.CONFIDENTIAL,
            redaction_class=RedactionClass.REFERENCE_ONLY,
            trusted_context_ref=payload.trusted_context_ref,
            autonomy_notes=payload.autonomy_notes,
            payload_metadata=payload.metadata,
        )
        metadata.update(
            {
                "session_ref": payload.session_ref,
            }
        )
        return HumanInput(
            input_id=_build_input_id(
                "sparkbot-operator",
                payload.actor_ref,
                payload.shell_id,
                payload.session_ref,
                payload.command_ref,
                payload.command,
            ),
            source=HumanInputSource.CONSOLE,
            actor_id=payload.actor_ref,
            shell_id=payload.shell_id,
            content_ref=payload.command_ref,
            raw_text=payload.command,
            privacy_class=PrivacyClass.CONFIDENTIAL.value,
            metadata=metadata,
        )
