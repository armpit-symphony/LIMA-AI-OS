"""Tests for LIMA-owned synthetic Sparkbot payload fixture mirrors."""

from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any

from lima.adapters import (
    SparkbotChatInputPayload,
    SparkbotHumanInputAdapter,
    SparkbotMeetingInputPayload,
    SparkbotOperatorInputPayload,
    SparkbotVoiceInputPayload,
)
from lima.contracts.intent import HumanInputSource


FIXTURE_ROOT = Path(__file__).resolve().parent / "fixtures" / "sparkbot_payloads"
FIXTURE_FILES = (
    "chat_payloads.json",
    "voice_payloads.json",
    "meeting_payloads.json",
    "operator_payloads.json",
    "mcp_approval_payloads.json",
    "robot_request_payloads.json",
    "frontend_chat_payloads.json",
    "workstation_payloads.json",
    "sparkbud_payloads.json",
    "auth_session_context_payloads.json",
    "model_routing_context_payloads.json",
)
REQUIRED_KEYS = {
    "fixture_id",
    "source_surface",
    "sparkbot_reference_path",
    "inspected_commit",
    "payload",
    "expected_humaninput_source",
    "privacy_class",
    "redaction_class",
    "notes",
}
DRIFT_KEYS = {
    "shape_version",
    "reviewed_at",
    "reviewed_against",
    "drift_status",
    "drift_notes",
}
CURRENT_SPARKBOT_COMMIT = "4a08838ba500fec4ef85c163b3249a2db80da9d6"
DRIFT_STATUSES = {"current", "needs_review", "stale", "unknown"}
SECRET_VALUE_MARKERS = (
    "api_key",
    "password",
    "secret",
    "sk-",
    "ghp_",
    "private_key",
    "bearer ",
)
SECRET_FIELD_NAMES = {
    "api_key",
    "auth_token",
    "access_token",
    "refresh_token",
    "password",
    "secret",
    "private_key",
}


def _load_fixture_file(name: str) -> list[dict[str, Any]]:
    path = FIXTURE_ROOT / name
    data = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(data, list)
    return data


def _all_fixtures() -> list[dict[str, Any]]:
    fixtures: list[dict[str, Any]] = []
    for name in FIXTURE_FILES:
        fixtures.extend(_load_fixture_file(name))
    return fixtures


def _adapt_fixture(fixture: dict[str, Any]):
    adapter = SparkbotHumanInputAdapter()
    payload = fixture["payload"]
    surface = fixture["source_surface"]

    if surface.startswith(
        (
            "chat_",
            "frontend_chat",
            "sparkbud_",
            "auth_session_",
            "model_routing_",
        )
    ):
        return adapter.adapt_chat_payload(
            SparkbotChatInputPayload(
                message_id=str(payload.get("message_id") or fixture["fixture_id"]),
                actor_ref=str(payload["actor_ref"]),
                shell_id=str(payload["shell_id"]),
                session_ref=payload.get("session_ref"),
                text=(
                    payload.get("content")
                    or payload.get("message")
                    or payload.get("body")
                    or payload.get("draft_prompt")
                ),
                source_ref=(
                    payload.get("room_id")
                    or payload.get("client_msg_id")
                    or payload.get("source_ref")
                    or payload.get("launch_context_ref")
                ),
                trusted_context_ref=payload.get("trusted_context_ref"),
                metadata={
                    "fixture_id": fixture["fixture_id"],
                    "source_surface": surface,
                    "fixture_mirror_only": True,
                    "model_call_performed": False,
                    "tool_execution_performed": False,
                },
            )
        )

    if surface.startswith("voice_"):
        return adapter.adapt_voice_payload(
            SparkbotVoiceInputPayload(
                transcript_ref=str(payload["transcript_ref"]),
                actor_ref=str(payload["actor_ref"]),
                shell_id=str(payload["shell_id"]),
                session_ref=payload.get("session_ref"),
                confidence=payload.get("confidence"),
                trusted_context_ref=payload.get("trusted_context_ref"),
                metadata={
                    "fixture_id": fixture["fixture_id"],
                    "source_surface": surface,
                    "fixture_mirror_only": True,
                    "voice_recognition_performed": False,
                },
            )
        )

    if surface.startswith("meeting_"):
        return adapter.adapt_meeting_payload(
            SparkbotMeetingInputPayload(
                meeting_id=str(payload["meeting_id"]),
                room_id=payload.get("room_id"),
                actor_ref=str(payload["actor_ref"]),
                shell_id=str(payload["shell_id"]),
                prompt=payload.get("prompt"),
                prompt_ref=payload.get("prompt_ref") or payload.get("content_markdown_ref"),
                trusted_context_ref=payload.get("trusted_context_ref"),
                metadata={
                    "fixture_id": fixture["fixture_id"],
                    "source_surface": surface,
                    "fixture_mirror_only": True,
                },
            )
        )

    return adapter.adapt_operator_payload(
        SparkbotOperatorInputPayload(
            actor_ref=str(payload["actor_ref"]),
            shell_id=str(payload["shell_id"]),
            session_ref=payload.get("session_ref"),
            command=payload.get("requested_action") or payload.get("user_request"),
            command_ref=payload.get("command_ref") or payload.get("requested_action_ref"),
            trusted_context_ref=payload.get("trusted_context_ref"),
            metadata={
                "fixture_id": fixture["fixture_id"],
                "source_surface": surface,
                "fixture_mirror_only": True,
            },
        )
    )


def test_fixture_files_exist_and_are_valid_json() -> None:
    assert (FIXTURE_ROOT / "README.md").is_file()
    for name in FIXTURE_FILES:
        path = FIXTURE_ROOT / name
        assert path.is_file()
        assert isinstance(json.loads(path.read_text(encoding="utf-8")), list)


def test_each_fixture_has_required_shape() -> None:
    fixtures = _all_fixtures()
    assert fixtures

    for fixture in fixtures:
        assert REQUIRED_KEYS.issubset(fixture)
        assert DRIFT_KEYS.issubset(fixture)
        assert len(fixture["inspected_commit"]) == 40
        assert all(char in "0123456789abcdef" for char in fixture["inspected_commit"])
        assert isinstance(fixture["payload"], dict)
        assert fixture["expected_humaninput_source"] in {
            HumanInputSource.TEXT.value,
            HumanInputSource.VOICE.value,
            HumanInputSource.CONSOLE.value,
        }
        assert fixture["privacy_class"] in {"private", "confidential"}
        assert fixture["redaction_class"] in {"summary_only", "reference_only"}
        assert fixture["drift_status"] in DRIFT_STATUSES
        assert fixture["shape_version"] in {"phase-1.21", "phase-2.2"}
        assert fixture["reviewed_at"] in {"2026-05-09", "2026-05-10"}
        assert len(fixture["reviewed_against"]) == 40
        assert all(char in "0123456789abcdef" for char in fixture["reviewed_against"])


def test_fixture_readme_documents_boundary_rules() -> None:
    readme = (FIXTURE_ROOT / "README.md").read_text(encoding="utf-8").lower()

    for required in (
        "lima-owned synthetic mirrors",
        "production adapter work remains blocked",
        "no fixture imports sparkbot",
        "payload drift must be reviewed",
        "before real adapter work",
        "frontend chat variants",
        "workstation",
        "sparkbud",
        "auth/session context",
        "model-routing",
    ):
        assert required in readme


def test_fixtures_contain_no_obvious_secrets() -> None:
    def check_value(value: Any) -> None:
        if isinstance(value, dict):
            for key, nested in value.items():
                assert str(key).lower() not in SECRET_FIELD_NAMES
                check_value(nested)
        elif isinstance(value, list):
            for nested in value:
                check_value(nested)
        elif isinstance(value, str):
            lowered = value.lower()
            assert all(marker not in lowered for marker in SECRET_VALUE_MARKERS)

    for fixture in _all_fixtures():
        check_value(fixture)


def test_fixtures_use_synthetic_actor_session_and_message_values() -> None:
    for fixture in _all_fixtures():
        payload = fixture["payload"]
        if "actor_ref" in payload:
            assert payload["actor_ref"] == "fixture-user"
        if "session_ref" in payload:
            assert payload["session_ref"] == "fixture-session"
        if "room_id" in payload:
            assert payload["room_id"] == "fixture-room"
        if "content" in payload:
            assert str(payload["content"]).startswith("fixture ")
        if "requested_action" in payload:
            assert str(payload["requested_action"]).startswith("fixture ")
        if "user_request" in payload:
            assert str(payload["user_request"]).startswith("fixture ")


def test_phase_2_2_fixture_categories_exist_and_use_current_review_commit() -> None:
    expected_files = {
        "frontend_chat_payloads.json",
        "workstation_payloads.json",
        "sparkbud_payloads.json",
        "auth_session_context_payloads.json",
        "model_routing_context_payloads.json",
    }
    for name in expected_files:
        fixtures = _load_fixture_file(name)
        assert fixtures
        for fixture in fixtures:
            assert fixture["shape_version"] == "phase-2.2"
            assert fixture["reviewed_at"] == "2026-05-10"
            assert fixture["reviewed_against"] == CURRENT_SPARKBOT_COMMIT
            assert fixture["drift_status"] == "current"


def test_robot_fixtures_are_safety_critical_and_non_executing() -> None:
    for fixture in _load_fixture_file("robot_request_payloads.json"):
        notes = fixture["notes"].lower()
        assert "safety-critical" in notes
        assert "non-executing" in notes
        assert "physical action" in notes


def test_fixture_examples_adapt_to_expected_humaninput_source() -> None:
    forbidden_metadata = {
        "approval_id",
        "approval_metadata",
        "decision_id",
        "guardian_decision",
        "intent_id",
        "policy_decision",
    }

    for fixture in _all_fixtures():
        result = _adapt_fixture(fixture)
        assert result.source.value == fixture["expected_humaninput_source"]
        assert result.actor_id == fixture["payload"]["actor_ref"]
        assert result.shell_id == fixture["payload"]["shell_id"]
        assert result.metadata["payload_metadata"]["fixture_mirror_only"] is True
        assert forbidden_metadata.isdisjoint(result.metadata)


def test_fixture_tests_do_not_import_sparkbot_or_runtime_surfaces() -> None:
    test_source = Path(__file__).read_text(encoding="utf-8")
    tree = ast.parse(test_source)
    imported_modules: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_modules.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            imported_modules.append(node.module)

    imported_text = "\n".join(imported_modules)
    forbidden_import_fragments = {
        "backend.",
        "app.",
        "fastapi",
        "websocket",
        "requests",
        "httpx",
        "sqlite3",
        "sqlalchemy",
        "sqlmodel",
        "dotenv",
        "openai",
        "litellm",
    }
    forbidden_symbols = {
        "stream_chat_with_tools",
        "execute_tool",
        "GuardianDecision",
        "ApprovalMetadata",
        "PolicyDecision",
    }
    fixture_text = "\n".join(
        (FIXTURE_ROOT / name).read_text(encoding="utf-8") for name in FIXTURE_FILES
    )

    assert all(fragment not in imported_text.lower() for fragment in forbidden_import_fragments)
    assert all(symbol not in fixture_text for symbol in forbidden_symbols)
