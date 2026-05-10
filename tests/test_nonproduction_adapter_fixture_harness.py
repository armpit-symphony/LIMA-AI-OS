"""Tests for the non-production adapter fixture harness."""

from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any

from lima.adapters import SparkbotHumanInputAdapter
from lima.contracts.events import AuditStatus
from lima.contracts.guardian import ConsequentialActionType, GuardianDecisionStatus
from lima.contracts.intent import HumanInputSource
from lima.guardian import (
    AdapterFixtureHarness,
    FakeApprovalRecorder,
    FakeGuardianDecisionEvaluator,
    FakeGuardianPipeline,
    FakePolicyRiskEvaluator,
    FakeSpineAuditRecorder,
    HumanInputFakePipelineBridge,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = REPO_ROOT / "tests" / "fixtures" / "sparkbot_payloads"
HARNESS_PATH = REPO_ROOT / "lima" / "guardian" / "fixture_harness.py"

FORBIDDEN_HARNESS_METHODS = {
    "execute",
    "enforce",
    "run_live",
    "wire_route",
    "call_model",
    "call_tool",
    "call_driver",
    "open_terminal",
    "import_sparkbot",
    "stream_chat_with_tools",
    "execute_tool",
    "persist",
    "save_to_db",
    "deploy",
    "trigger_robot",
}

FORBIDDEN_IMPORT_MODULES = {
    "aiohttp",
    "anthropic",
    "app.api.routes",
    "app.crud",
    "app.models",
    "app.services",
    "app",
    "backend",
    "backend.app",
    "boto3",
    "fastapi",
    "google.generativeai",
    "httpx",
    "openai",
    "pty",
    "redis",
    "requests",
    "socket",
    "sparkbot",
    "sqlalchemy",
    "sqlite",
    "sqlite3",
    "stripe",
    "subprocess",
    "terminal",
    "robo",
}

FORBIDDEN_IMPORTED_SYMBOLS = {
    "APIRouter",
    "ChatUser",
    "FastAPI",
    "WebSocket",
    "execute_tool",
    "stream_chat_with_tools",
}

FORBIDDEN_SOURCE_STRINGS = {
    "APIRouter",
    "ChatUser",
    "FastAPI",
    "Robo",
    "WebSocket",
    "aiohttp",
    "anthropic",
    "app.api.routes",
    "app.crud",
    "app.models",
    "app.services",
    "backend.app",
    "boto3",
    "call_driver",
    "call_model",
    "call_tool",
    "execute_tool",
    "google.generativeai",
    "getenv",
    "httpx",
    "import_sparkbot",
    "openai",
    "open(",
    "os.environ",
    "persist(",
    "redis",
    "requests",
    "run_live",
    "save_to_db",
    "socket",
    "sqlalchemy",
    "sqlite",
    "stripe",
    "stream_chat_with_tools",
    "subprocess",
    "wire_route",
}


def _load_fixture_file(name: str) -> list[dict[str, Any]]:
    with (FIXTURE_ROOT / name).open(encoding="utf-8") as handle:
        data = json.load(handle)
    assert isinstance(data, list)
    return data


def _make_harness() -> tuple[AdapterFixtureHarness, FakeSpineAuditRecorder]:
    spine = FakeSpineAuditRecorder()
    pipeline = FakeGuardianPipeline(
        policy_evaluator=FakePolicyRiskEvaluator(),
        decision_evaluator=FakeGuardianDecisionEvaluator(),
        approval_recorder=FakeApprovalRecorder(),
        spine_recorder=spine,
    )
    return (
        AdapterFixtureHarness(
            adapter=SparkbotHumanInputAdapter(),
            bridge=HumanInputFakePipelineBridge(pipeline),
        ),
        spine,
    )


def _assert_fake_lineage_exists(result: Any, spine: FakeSpineAuditRecorder) -> None:
    events = spine.get_lineage(result.pipeline_result.lineage_id)
    lineage = spine.get_lineage_record(result.pipeline_result.lineage_id)
    assert events
    assert lineage is not None
    assert lineage.metadata["fake_pipeline"] is True
    assert lineage.metadata["non_executing"] is True
    assert result.pipeline_result.event_ids
    assert result.pipeline_result.metadata["non_executing"] is True


def test_chat_fixture_runs_through_humaninput_and_fake_pipeline() -> None:
    harness, spine = _make_harness()
    results = harness.run_fixtures(_load_fixture_file("chat_payloads.json"))

    assert results
    for result in results:
        assert result.human_input.source is HumanInputSource.TEXT
        assert result.expected_humaninput_source == "text"
        assert result.metadata["non_executing"] is True
        assert result.human_input.metadata["payload_metadata"]["non_executing"] is True
        assert result.pipeline_result.request.action_type is ConsequentialActionType.UNKNOWN
        assert result.pipeline_result.guardian_decision.status is GuardianDecisionStatus.DENIED
        assert result.pipeline_result.status == AuditStatus.DENIED.value
        _assert_fake_lineage_exists(result, spine)


def test_voice_fixture_preserves_transcript_confidence_and_uses_fake_pipeline() -> None:
    harness, spine = _make_harness()
    results = harness.run_fixtures(_load_fixture_file("voice_payloads.json"))

    assert results
    for result in results:
        payload = result.human_input.metadata["payload_metadata"]
        assert result.human_input.source is HumanInputSource.VOICE
        assert result.expected_humaninput_source == "voice"
        assert result.human_input.content_ref is not None
        assert result.human_input.confidence is not None
        assert payload["voice_recognition_performed"] is False
        assert payload["intent_inference_performed"] is False
        _assert_fake_lineage_exists(result, spine)


def test_meeting_fixture_preserves_meeting_metadata() -> None:
    harness, spine = _make_harness()
    results = harness.run_fixtures(_load_fixture_file("meeting_payloads.json"))

    assert results
    for result in results:
        metadata = result.human_input.metadata
        assert result.human_input.source is HumanInputSource.TEXT
        assert result.expected_humaninput_source == "text"
        assert metadata["meeting_id"] == "fixture-meeting"
        assert metadata["room_id"] == "fixture-room"
        assert metadata["payload_metadata"]["non_executing"] is True
        _assert_fake_lineage_exists(result, spine)


def test_operator_fixture_stays_console_and_non_executing() -> None:
    harness, spine = _make_harness()
    results = harness.run_fixtures(_load_fixture_file("operator_payloads.json"))

    assert results
    for result in results:
        payload = result.human_input.metadata["payload_metadata"]
        assert result.human_input.source is HumanInputSource.CONSOLE
        assert result.expected_humaninput_source == "console"
        assert payload["non_executing"] is True
        assert payload["terminal_opened"] is False
        assert result.pipeline_result.request.action_type is ConsequentialActionType.TERMINAL_COMMAND
        assert result.pipeline_result.request.risk_class == "critical"
        assert result.pipeline_result.guardian_decision.status is GuardianDecisionStatus.NEEDS_OPERATOR_PIN
        assert result.pipeline_result.status == AuditStatus.NEEDS_APPROVAL.value
        _assert_fake_lineage_exists(result, spine)


def test_mcp_approval_fixtures_are_non_executing_tool_call_records() -> None:
    harness, spine = _make_harness()
    results = harness.run_fixtures(_load_fixture_file("mcp_approval_payloads.json"))

    assert results
    for result in results:
        payload = result.human_input.metadata["payload_metadata"]
        assert result.human_input.source is HumanInputSource.CONSOLE
        assert payload["tool_execution_performed"] is False
        assert payload["non_executing"] is True
        assert result.pipeline_result.request.action_type is ConsequentialActionType.TOOL_CALL
        assert result.pipeline_result.request.risk_class == "high"
        assert result.pipeline_result.guardian_decision.status is GuardianDecisionStatus.NEEDS_HUMAN_CONFIRMATION
        assert result.pipeline_result.status == AuditStatus.NEEDS_APPROVAL.value
        _assert_fake_lineage_exists(result, spine)


def test_robot_fixtures_are_safety_critical_and_not_auto_approved() -> None:
    harness, spine = _make_harness()
    results = harness.run_fixtures(_load_fixture_file("robot_request_payloads.json"))

    assert results
    for result in results:
        payload = result.human_input.metadata["payload_metadata"]
        lineage = spine.get_lineage_record(result.pipeline_result.lineage_id)
        assert result.human_input.source is HumanInputSource.CONSOLE
        assert payload["safety_critical"] is True
        assert payload["physical_action_performed"] is False
        assert payload["driver_call_performed"] is False
        assert result.pipeline_result.request.action_type is ConsequentialActionType.ROBOT_ACTION
        assert result.pipeline_result.request.risk_class == "critical"
        assert result.pipeline_result.guardian_decision.status is GuardianDecisionStatus.NEEDS_OPERATOR_PIN
        assert result.pipeline_result.guardian_decision.status is not GuardianDecisionStatus.APPROVED
        assert result.pipeline_result.status == AuditStatus.NEEDS_APPROVAL.value
        assert lineage is not None
        assert lineage.contains_safety_critical is True
        _assert_fake_lineage_exists(result, spine)


def test_harness_boundary_has_no_forbidden_methods_or_imports() -> None:
    public_callables = {
        name
        for name, value in AdapterFixtureHarness.__dict__.items()
        if not name.startswith("_") and callable(value)
    }
    class_methods = {
        name
        for name, value in AdapterFixtureHarness.__dict__.items()
        if callable(value)
    }
    assert public_callables == {"run_fixture", "run_fixtures"}
    assert public_callables.isdisjoint(FORBIDDEN_HARNESS_METHODS)
    assert class_methods.isdisjoint(FORBIDDEN_HARNESS_METHODS)

    source = HARNESS_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported_modules: list[str] = []
    imported_symbols: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_modules.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_modules.append(node.module)
            imported_symbols.extend(alias.name for alias in node.names)

    imported_text = "\n".join(imported_modules).lower()
    violations = [
        forbidden
        for forbidden in FORBIDDEN_IMPORT_MODULES
        if forbidden in imported_text
    ]
    assert violations == []
    symbol_violations = [
        imported
        for imported in imported_symbols
        if imported in FORBIDDEN_IMPORTED_SYMBOLS
    ]
    assert symbol_violations == []

    source_violations = [
        forbidden for forbidden in FORBIDDEN_SOURCE_STRINGS if forbidden in source
    ]
    assert source_violations == []
