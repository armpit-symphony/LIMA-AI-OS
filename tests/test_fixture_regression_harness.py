"""Tests for the fixture regression harness."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

from lima.adapters import SparkbotHumanInputAdapter
from lima.guardian import (
    AdapterFixtureHarness,
    FakeApprovalRecorder,
    FakeGuardianDecisionEvaluator,
    FakeGuardianPipeline,
    FakePolicyRiskEvaluator,
    FakeSpineAuditRecorder,
    HumanInputFakePipelineBridge,
)

from tests.helpers.fixture_regression_harness import (
    FAILED,
    PASSED,
    UNSUPPORTED_NONEXECUTING,
    FixtureRegressionReport,
    group_fixtures_by_surface,
    load_payload_fixtures,
    run_fixture_regression,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = REPO_ROOT / "tests" / "fixtures" / "sparkbot_payloads"
HELPER_PATH = REPO_ROOT / "tests" / "helpers" / "fixture_regression_harness.py"

FORBIDDEN_IMPORT_FRAGMENTS = {
    "aiohttp",
    "anthropic",
    "app.",
    "backend.",
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
    "stripe",
    "subprocess",
    "terminal",
}

FORBIDDEN_SOURCE_STRINGS = {
    "APIRouter",
    "ChatUser",
    "FastAPI",
    "WebSocket",
    "call_driver",
    "call_model",
    "call_tool",
    "execute_tool",
    "getenv",
    "import_sparkbot",
    "open(",
    "os.environ",
    "save_to_db",
    "stream_chat_with_tools",
    "wire_route",
}


def _make_harness() -> AdapterFixtureHarness:
    pipeline = FakeGuardianPipeline(
        policy_evaluator=FakePolicyRiskEvaluator(),
        decision_evaluator=FakeGuardianDecisionEvaluator(),
        approval_recorder=FakeApprovalRecorder(),
        spine_recorder=FakeSpineAuditRecorder(),
    )
    return AdapterFixtureHarness(
        adapter=SparkbotHumanInputAdapter(),
        bridge=HumanInputFakePipelineBridge(pipeline),
    )


def _run_all_fixtures() -> tuple[list[dict[str, Any]], FixtureRegressionReport]:
    fixtures = load_payload_fixtures(FIXTURE_ROOT)
    return fixtures, run_fixture_regression(fixtures, _make_harness())


def test_loads_all_fixture_files_and_groups_by_surface() -> None:
    fixtures = load_payload_fixtures(FIXTURE_ROOT)
    grouped = group_fixtures_by_surface(fixtures)

    assert len(fixtures) > 0
    assert len(grouped) >= 11
    assert "chat_message_stream" in grouped
    assert "frontend_chat_body_variant" in grouped
    assert "robotics_command" in grouped
    for fixture in fixtures:
        assert fixture["fixture_id"]
        assert fixture["source_surface"]


def test_regression_report_runs_all_current_fixtures_without_failures() -> None:
    fixtures, report = _run_all_fixtures()

    assert report.total == len(fixtures)
    assert report.executed == len(fixtures)
    assert report.unsupported_nonexecuting == 0
    assert report.failed == 0
    assert report.metadata["test_only"] is True
    assert report.metadata["non_production"] is True
    assert report.metadata["non_executing"] is True
    assert all(result.status == PASSED for result in report.results)


def test_unsupported_categories_are_explicit_and_never_pass_silently() -> None:
    report = run_fixture_regression(
        (
            {
                "fixture_id": "unsupported-fixture",
                "source_surface": "unknown_surface",
                "payload": {},
                "expected_humaninput_source": "text",
            },
        ),
        _make_harness(),
    )

    assert report.total == 1
    assert report.executed == 0
    assert report.unsupported_nonexecuting == 1
    assert report.failed == 0
    result = report.results[0]
    assert result.status == UNSUPPORTED_NONEXECUTING
    assert result.unsupported_reason
    assert result.humaninput_source is None
    assert result.pipeline_status is None
    assert "unsupported_nonexecuting" in result.safety_notes


def test_critical_robot_and_unknown_paths_do_not_auto_approve() -> None:
    _, report = _run_all_fixtures()

    guarded = [
        result
        for result in report.results
        if result.source_surface.startswith(("robotics_", "operator_"))
        or result.metadata["action_type"] == "unknown"
    ]
    assert guarded
    for result in guarded:
        assert result.decision_status != "approved"
        assert "not_auto_approved" in result.safety_notes


def test_passive_metadata_remains_passive_without_authority_or_model_calls() -> None:
    _, report = _run_all_fixtures()

    passive_results = [
        result
        for result in report.results
        if result.source_surface.startswith(("auth_session_", "model_routing_"))
    ]
    assert passive_results
    for result in passive_results:
        assert result.status == PASSED
        assert result.metadata["model_call_performed"] is False
        assert result.metadata["tool_execution_performed"] is False
        assert result.metadata["driver_call_performed"] is False
        assert result.metadata["persistence_performed"] is False
        assert result.decision_status != "approved"
        assert any(
            note in result.safety_notes
            for note in (
                "auth_session_refs_not_authority",
                "model_routing_metadata_passive",
            )
        )


def test_mcp_and_robot_fixtures_remain_non_executing() -> None:
    _, report = _run_all_fixtures()
    special_results = [
        result
        for result in report.results
        if result.source_surface.startswith(("mcp_", "robotics_"))
    ]

    assert special_results
    for result in special_results:
        assert result.status == PASSED
        assert result.metadata["tool_execution_performed"] is False
        assert result.metadata["driver_call_performed"] is False
        assert result.metadata["persistence_performed"] is False
        assert result.decision_status != "approved"
        if result.source_surface.startswith("mcp_"):
            assert "mcp_tool_request_not_executed" in result.safety_notes
        if result.source_surface.startswith("robotics_"):
            assert "robot_safety_critical" in result.safety_notes
            assert "physical_action_not_performed" in result.safety_notes


def test_regression_helper_has_no_runtime_imports_or_persistence_paths() -> None:
    source = HELPER_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported_modules: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_modules.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_modules.append(node.module)

    imported_text = "\n".join(imported_modules).lower()
    assert [
        fragment
        for fragment in FORBIDDEN_IMPORT_FRAGMENTS
        if fragment in imported_text
    ] == []
    assert [text for text in FORBIDDEN_SOURCE_STRINGS if text in source] == []
    assert FAILED == "failed"
