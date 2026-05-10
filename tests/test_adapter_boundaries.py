"""Boundary tests for LIMA adapter modules."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

from lima.adapters import (
    SparkbotChatInputPayload,
    SparkbotHumanInputAdapter,
    SparkbotMeetingInputPayload,
    SparkbotOperatorInputPayload,
    SparkbotVoiceInputPayload,
)
from lima.contracts import (
    ApprovalMetadata,
    ConsequentialActionRequest,
    GuardianDecision,
    HumanInput,
    IntentEnvelope,
    PolicyDecision,
    SpineEvent,
)


LIMA_ROOT = Path(__file__).resolve().parents[1] / "lima"
ADAPTER_ROOT = LIMA_ROOT / "adapters"

ALLOWED_SPARKBOT_ADAPTER_METHODS = {
    "adapt_chat_payload",
    "adapt_voice_payload",
    "adapt_meeting_payload",
    "adapt_operator_payload",
}

FORBIDDEN_IMPORT_MODULE_FRAGMENTS = {
    "sparkbot",
    "backend.app",
    "app.api.routes",
    "app.crud",
    "app.models",
    "app.services",
    "fastapi",
    "websocket",
    "requests",
    "httpx",
    "aiohttp",
    "sqlite",
    "sqlite3",
    "sqlalchemy",
    "redis",
    "boto3",
    "stripe",
    "unitree",
    "docker",
    "kubernetes",
    "openai",
    "anthropic",
    "google.generativeai",
    "subprocess",
    "pty",
    "terminal",
    "pathlib",
    "socket",
    "os",
    "robo",
}

FORBIDDEN_IMPORTED_SYMBOLS = {
    "APIRouter",
    "ChatUser",
    "Depends",
    "FastAPI",
    "Request",
    "WebSocket",
    "execute_tool",
    "stream_chat_with_tools",
}

FORBIDDEN_SOURCE_STRINGS = {
    "stream_chat_with_tools",
    "execute_tool",
    "app.api.routes",
    "backend.app",
    "app.crud",
    "app.models",
    "app.services",
    "ChatUser",
    "FastAPI",
    "WebSocket",
    "APIRouter",
    "Depends",
    "Request(",
    "os.environ",
    "getenv",
    "os.system",
    "subprocess",
    "terminal",
    "open(",
    "pathlib.Path",
    "socket",
    "requests",
    "httpx",
    "aiohttp",
    "sqlite",
    "sqlalchemy",
    "redis",
    "boto3",
    "stripe",
    "Robo",
    "robo",
    "LIMA-Robo-OS",
    "unitree",
    "docker",
    "kubernetes",
    "openai",
    "anthropic",
    "google.generativeai",
}

FORBIDDEN_METHOD_NAMES = {
    "execute",
    "run",
    "call_model",
    "call_tool",
    "execute_tool",
    "wire_route",
    "send",
    "persist",
    "save",
    "save_to_db",
    "open_db",
    "open_terminal",
    "create_intent",
    "create_decision",
    "create_guardian_decision",
    "approve",
    "enforce",
    "authorize",
    "authorize_execution",
    "call_driver",
    "trigger_robot",
    "deploy",
    "pay",
    "charge",
    "decrypt",
    "get_secret",
    "verify_pin",
    "login",
    "authenticate",
    "trust_device",
    "grant_autonomy",
    "infer_intent",
    "parse_intent",
    "call_intent_compiler",
}

FORBIDDEN_OUTPUT_TYPES = (
    IntentEnvelope,
    GuardianDecision,
    ApprovalMetadata,
    PolicyDecision,
    SpineEvent,
    ConsequentialActionRequest,
)


def _adapter_python_files() -> list[Path]:
    if not ADAPTER_ROOT.exists():
        return []
    return sorted(path for path in ADAPTER_ROOT.rglob("*.py") if "__pycache__" not in path.parts)


def _parsed_adapter_files() -> list[tuple[Path, ast.Module, str]]:
    parsed: list[tuple[Path, ast.Module, str]] = []
    for path in _adapter_python_files():
        assert path.resolve().is_relative_to(ADAPTER_ROOT.resolve())
        text = path.read_text(encoding="utf-8")
        parsed.append((path, ast.parse(text), text))
    return parsed


def _import_entries(tree: ast.Module) -> list[tuple[str, str]]:
    entries: list[tuple[str, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            entries.extend((alias.name, alias.asname or alias.name) for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            entries.extend((node.module, alias.name) for alias in node.names)
    return entries


def _adapter_results() -> list[HumanInput]:
    adapter = SparkbotHumanInputAdapter()
    return [
        adapter.adapt_chat_payload(
            SparkbotChatInputPayload(
                message_id="fixture-chat-message",
                actor_ref="fixture-user",
                shell_id="sparkbot",
                session_ref="fixture-session",
                text="fixture hello",
            )
        ),
        adapter.adapt_voice_payload(
            SparkbotVoiceInputPayload(
                transcript_ref="fixture-transcript-ref",
                actor_ref="fixture-user",
                shell_id="sparkbot",
                session_ref="fixture-session",
                confidence=0.7,
            )
        ),
        adapter.adapt_meeting_payload(
            SparkbotMeetingInputPayload(
                meeting_id="fixture-meeting",
                room_id="fixture-room",
                actor_ref="fixture-user",
                shell_id="sparkbot",
                prompt="fixture meeting prompt",
            )
        ),
        adapter.adapt_operator_payload(
            SparkbotOperatorInputPayload(
                actor_ref="fixture-user",
                shell_id="sparkbot",
                session_ref="fixture-session",
                command_ref="fixture-command-ref",
            )
        ),
    ]


def test_adapter_boundary_scan_is_limited_to_local_lima_adapters() -> None:
    files = _adapter_python_files()

    if not ADAPTER_ROOT.exists():
        assert files == []
        return

    assert files
    assert all(path.resolve().is_relative_to(ADAPTER_ROOT.resolve()) for path in files)
    assert all("Sparkbot" not in path.parts for path in files)


def test_adapter_modules_do_not_import_runtime_or_external_dependencies() -> None:
    violations: list[str] = []

    for path, tree, _ in _parsed_adapter_files():
        for module_name, imported_name in _import_entries(tree):
            module_lower = module_name.lower()
            for forbidden in FORBIDDEN_IMPORT_MODULE_FRAGMENTS:
                if forbidden in module_lower:
                    violations.append(f"{path.relative_to(LIMA_ROOT)} imports {module_name!r}")
            if imported_name in FORBIDDEN_IMPORTED_SYMBOLS:
                violations.append(f"{path.relative_to(LIMA_ROOT)} imports {imported_name!r}")

    assert violations == []


def test_adapter_modules_do_not_reference_runtime_execution_or_io_paths() -> None:
    violations: list[str] = []

    for path, _, text in _parsed_adapter_files():
        for forbidden in FORBIDDEN_SOURCE_STRINGS:
            if forbidden in text:
                violations.append(f"{path.relative_to(LIMA_ROOT)} contains {forbidden!r}")

    assert violations == []


def test_adapter_classes_do_not_expose_behavior_bearing_methods() -> None:
    violations: list[str] = []

    for path, tree, _ in _parsed_adapter_files():
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                method_names = {
                    item.name
                    for item in node.body
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
                }
                forbidden_methods = method_names & FORBIDDEN_METHOD_NAMES
                if forbidden_methods:
                    violations.append(
                        f"{path.relative_to(LIMA_ROOT)}:{node.name} exposes "
                        f"{sorted(forbidden_methods)!r}"
                    )

    assert violations == []


def test_current_sparkbot_adapter_exposes_only_allowed_adapt_methods() -> None:
    public_callables = {
        name
        for name, value in SparkbotHumanInputAdapter.__dict__.items()
        if not name.startswith("_") and callable(value)
    }

    assert public_callables == ALLOWED_SPARKBOT_ADAPTER_METHODS


def test_current_adapter_methods_return_humaninput_only() -> None:
    for result in _adapter_results():
        assert type(result) is HumanInput
        assert not isinstance(result, FORBIDDEN_OUTPUT_TYPES)


def test_adapter_outputs_do_not_create_policy_or_execution_metadata() -> None:
    forbidden_metadata = {
        "approval_id",
        "approval_metadata",
        "consequential_action_request",
        "decision_id",
        "guardian_decision",
        "intent_envelope",
        "intent_id",
        "policy_decision",
        "spine_event",
    }

    for result in _adapter_results():
        metadata: dict[str, Any] = dict(result.metadata)
        assert forbidden_metadata.isdisjoint(metadata)
        assert metadata["non_production"] is True
        assert metadata["autonomy_metadata_passive"] is True
