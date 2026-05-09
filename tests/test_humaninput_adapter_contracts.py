"""Shape tests for describe-only HumanInput adapter contracts."""

from __future__ import annotations


def test_humaninput_adapter_contract_imports() -> None:
    from lima.contracts import (
        AdapterDesignProtocol,
        HumanInputAdapterDesign,
        HumanInputAdapterMapping,
        HumanInputAdapterSurface,
    )

    assert AdapterDesignProtocol is not None
    assert HumanInputAdapterDesign is not None
    assert HumanInputAdapterMapping is not None
    assert HumanInputAdapterSurface is not None


def test_humaninput_adapter_surface_expected_values_exist() -> None:
    from lima.contracts import HumanInputAdapterSurface

    expected_values = {
        "chat_message",
        "voice_transcript",
        "meeting_prompt",
        "sparkbud_prompt",
        "workstation_command",
        "operator_console",
        "terminal_request",
        "approval_response",
        "mcp_request",
        "robot_request",
        "frontend_chat",
        "unknown",
    }

    assert {surface.value for surface in HumanInputAdapterSurface} == expected_values


def test_humaninput_adapter_mapping_instantiates() -> None:
    from lima.contracts import HumanInputAdapterMapping, HumanInputAdapterSurface

    mapping = HumanInputAdapterMapping(
        surface=HumanInputAdapterSurface.CHAT_MESSAGE,
        source_path="backend/app/api/routes/chat/messages.py",
        source_name="create_room_message",
        human_input_source="text",
        shell_id="sparkbot-chat",
        actor_ref="current_user.id",
        session_ref="room_id",
        source_ref="message_id",
        privacy_class="private",
        redaction_class="summary_only",
        risk_notes="May contain commands or sensitive text.",
        shortcut_risks=("raw_chat_to_tool", "inline_bot_response"),
        notes="Describe-only mapping for future adapter review.",
        metadata={"phase": "1.11"},
    )

    assert mapping.surface is HumanInputAdapterSurface.CHAT_MESSAGE
    assert mapping.human_input_source == "text"
    assert mapping.shortcut_risks == ("raw_chat_to_tool", "inline_bot_response")


def test_humaninput_adapter_design_instantiates() -> None:
    from lima.contracts import (
        HumanInputAdapterDesign,
        HumanInputAdapterMapping,
        HumanInputAdapterSurface,
    )

    mapping = HumanInputAdapterMapping(
        surface=HumanInputAdapterSurface.VOICE_TRANSCRIPT,
        source_path="backend/app/api/routes/chat/voice.py",
        source_name="voice_message",
        human_input_source="voice",
        shell_id="sparkbot-voice",
        actor_ref="current_user.id",
        session_ref="room_id",
        source_ref="transcript_ref",
        privacy_class="private",
        redaction_class="reference_only",
        shortcut_risks=("voice_to_stream_chat_with_tools",),
    )
    design = HumanInputAdapterDesign(
        design_id="sparkbot-humaninput-phase-1-11",
        source_system="sparkbot",
        mappings=(mapping,),
        blocked_shortcuts=("stream_chat_with_tools direct extraction",),
        lineage_notes=("lineage IDs are planned but not persisted",),
        privacy_notes=("voice transcripts prefer transcript refs",),
        created_at="2026-05-09T00:00:00Z",
    )

    assert design.source_system == "sparkbot"
    assert design.mappings == (mapping,)
    assert "stream_chat_with_tools direct extraction" in design.blocked_shortcuts


def test_adapter_design_protocol_is_describe_only() -> None:
    from lima.contracts import AdapterDesignProtocol

    public_callables = {
        name
        for name, value in AdapterDesignProtocol.__dict__.items()
        if not name.startswith("_") and callable(value)
    }
    forbidden_methods = {
        "adapt",
        "execute",
        "run",
        "call_model",
        "call_tool",
        "wire_route",
        "send",
        "persist",
        "open_terminal",
    }

    assert public_callables == {"describe_mappings", "describe_design"}
    assert public_callables.isdisjoint(forbidden_methods)
