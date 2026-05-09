"""Tests for the non-production Sparkbot HumanInput adapter skeleton."""

from __future__ import annotations

import ast
from pathlib import Path

from lima.adapters import (
    SparkbotChatInputPayload,
    SparkbotHumanInputAdapter,
    SparkbotMeetingInputPayload,
    SparkbotOperatorInputPayload,
    SparkbotVoiceInputPayload,
)
from lima.contracts.intent import HumanInput, HumanInputSource


def test_chat_payload_maps_to_humaninput_text() -> None:
    adapter = SparkbotHumanInputAdapter()
    payload = SparkbotChatInputPayload(
        message_id="msg-1",
        actor_ref="actor-1",
        shell_id="sparkbot-shell",
        session_ref="room-1",
        text="Plan my week",
        text_ref="text-ref-1",
        source_ref="source-1",
        trusted_context_ref="trusted-session-1",
        autonomy_notes={"level": "trusted"},
        metadata={"client": "desktop"},
    )

    result = adapter.adapt_chat_payload(payload)

    assert isinstance(result, HumanInput)
    assert result.source is HumanInputSource.TEXT
    assert result.actor_id == "actor-1"
    assert result.shell_id == "sparkbot-shell"
    assert result.raw_text == "Plan my week"
    assert result.content_ref == "text-ref-1"
    assert result.metadata["message_id"] == "msg-1"
    assert result.metadata["session_ref"] == "room-1"
    assert result.metadata["source_ref"] == "source-1"
    assert result.metadata["trusted_context_ref"] == "trusted-session-1"
    assert result.metadata["autonomy_notes"] == {"level": "trusted"}
    assert result.metadata["privacy_class"] == "private"
    assert result.metadata["redaction_class"] == "summary_only"
    assert result.metadata["payload_metadata"] == {"client": "desktop"}


def test_voice_payload_maps_to_humaninput_voice() -> None:
    adapter = SparkbotHumanInputAdapter()
    payload = SparkbotVoiceInputPayload(
        transcript_ref="transcript-1",
        actor_ref="actor-voice",
        shell_id="sparkbot-voice",
        session_ref="room-voice",
        confidence=0.91,
        trusted_context_ref="trusted-voice",
    )

    result = adapter.adapt_voice_payload(payload)

    assert result.source is HumanInputSource.VOICE
    assert result.actor_id == "actor-voice"
    assert result.shell_id == "sparkbot-voice"
    assert result.raw_text is None
    assert result.content_ref == "transcript-1"
    assert result.confidence == 0.91
    assert result.metadata["transcript_ref"] == "transcript-1"
    assert result.metadata["privacy_class"] == "private"
    assert result.metadata["redaction_class"] == "reference_only"
    assert result.metadata["contains_biometric_signal"] is True


def test_meeting_payload_maps_to_humaninput_text() -> None:
    adapter = SparkbotHumanInputAdapter()
    payload = SparkbotMeetingInputPayload(
        meeting_id="meeting-1",
        room_id="room-2",
        actor_ref="actor-meeting",
        shell_id="sparkbot-meeting",
        prompt="Summarize decisions",
        prompt_ref="prompt-ref-1",
    )

    result = adapter.adapt_meeting_payload(payload)

    assert result.source is HumanInputSource.TEXT
    assert result.actor_id == "actor-meeting"
    assert result.shell_id == "sparkbot-meeting"
    assert result.raw_text == "Summarize decisions"
    assert result.content_ref == "prompt-ref-1"
    assert result.metadata["meeting_id"] == "meeting-1"
    assert result.metadata["room_id"] == "room-2"
    assert result.metadata["privacy_class"] == "confidential"


def test_operator_payload_maps_to_humaninput_console() -> None:
    adapter = SparkbotHumanInputAdapter()
    payload = SparkbotOperatorInputPayload(
        actor_ref="operator-1",
        shell_id="sparkbot-operator",
        session_ref="session-operator",
        command="show status",
        command_ref="command-ref-1",
        metadata={"surface": "workstation"},
    )

    result = adapter.adapt_operator_payload(payload)

    assert result.source is HumanInputSource.CONSOLE
    assert result.actor_id == "operator-1"
    assert result.shell_id == "sparkbot-operator"
    assert result.raw_text == "show status"
    assert result.content_ref == "command-ref-1"
    assert result.metadata["session_ref"] == "session-operator"
    assert result.metadata["privacy_class"] == "confidential"
    assert result.metadata["redaction_class"] == "reference_only"
    assert result.metadata["payload_metadata"] == {"surface": "workstation"}


def test_autonomy_metadata_is_passive() -> None:
    adapter = SparkbotHumanInputAdapter()
    payload = SparkbotChatInputPayload(
        message_id="msg-passive",
        actor_ref="actor-passive",
        shell_id="sparkbot-shell",
        session_ref=None,
        text="Create a draft",
        text_ref=None,
        source_ref=None,
        trusted_context_ref="trusted-passive",
        autonomy_notes={"capability": "draft_content"},
    )

    result = adapter.adapt_chat_payload(payload)

    assert result.metadata["trusted_context_ref"] == "trusted-passive"
    assert result.metadata["autonomy_notes"] == {"capability": "draft_content"}
    assert result.metadata["autonomy_metadata_passive"] is True
    assert "approval_id" not in result.metadata
    assert "decision_id" not in result.metadata
    assert "guardian_decision" not in result.metadata
    assert "intent_id" not in result.metadata


def test_adapter_does_not_create_decision_or_event_records() -> None:
    adapter = SparkbotHumanInputAdapter()
    payload = SparkbotOperatorInputPayload(
        actor_ref="operator-2",
        shell_id="sparkbot-operator",
        command="inspect queue",
    )

    result = adapter.adapt_operator_payload(payload)

    assert type(result) is HumanInput
    source = (
        Path(__file__).resolve().parents[1]
        / "lima"
        / "adapters"
        / "sparkbot_humaninput.py"
    ).read_text(encoding="utf-8")
    assert "IntentEnvelope" not in source
    assert "GuardianDecision" not in source
    assert "ApprovalMetadata" not in source
    assert "PolicyDecision" not in source
    assert "SpineEvent" not in source


def test_forbidden_methods_absent() -> None:
    forbidden_methods = {
        "execute",
        "run",
        "call_model",
        "call_tool",
        "wire_route",
        "send",
        "persist",
        "open_terminal",
        "create_intent",
        "create_decision",
        "approve",
        "enforce",
    }
    public_callables = {
        name
        for name, value in SparkbotHumanInputAdapter.__dict__.items()
        if not name.startswith("_") and callable(value)
    }

    assert public_callables == {
        "adapt_chat_payload",
        "adapt_voice_payload",
        "adapt_meeting_payload",
        "adapt_operator_payload",
    }
    assert public_callables.isdisjoint(forbidden_methods)


def test_forbidden_imports_absent_in_lima_adapters() -> None:
    adapters_root = Path(__file__).resolve().parents[1] / "lima" / "adapters"
    forbidden_imports = {
        "Sparkbot",
        "sparkbot",
        "FastAPI",
        "WebSocket",
        "app.api.routes",
        "backend.app",
        "terminal",
        "pty",
        "Robo",
        "robo",
        "requests",
        "httpx",
        "urllib",
        "sqlite3",
        "sqlalchemy",
        "sqlmodel",
        "Session",
        "dotenv",
        "os",
    }
    forbidden_symbols = {
        "stream_chat_with_tools",
        "execute_tool",
    }
    violations: list[str] = []

    for path in sorted(adapters_root.rglob("*.py")):
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text)
        imported_modules: list[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_modules.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
                imported_modules.append(node.module)

        imported_text = "\n".join(imported_modules)
        for forbidden in forbidden_imports:
            if forbidden.lower() in imported_text.lower():
                violations.append(f"{path.name} imports {forbidden!r}")
        for forbidden in forbidden_symbols:
            if forbidden in text:
                violations.append(f"{path.name} contains {forbidden!r}")

    assert violations == []
