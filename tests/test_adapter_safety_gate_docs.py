"""Tests for the consolidated adapter safety gate documentation."""

from __future__ import annotations

from pathlib import Path


DOC_PATH = Path(__file__).resolve().parents[1] / "docs" / "ADAPTER_SAFETY_GATE.md"

REQUIRED_TEST_NAMES = {
    "tests/test_adapter_boundaries.py",
    "tests/test_sparkbot_payload_fixture_mirror.py",
    "tests/test_nonproduction_adapter_fixture_harness.py",
    "tests/test_fixture_regression_harness.py",
    "tests/test_fixture_regression_report_artifact.py",
    "tests/test_fixture_regression_gate_docs.py",
    "tests/test_sparkbot_humaninput_adapter_skeleton.py",
    "tests/test_humaninput_fake_pipeline_bridge.py",
}

REQUIRED_FORBIDDEN_IMPORTS = {
    "Sparkbot",
    "backend.app",
    "FastAPI",
    "WebSocket",
    "stream_chat_with_tools",
    "execute_tool",
    "subprocess",
    "openai",
}

REQUIRED_FORBIDDEN_BEHAVIORS = {
    "production Sparkbot route wiring",
    "live WebSocket adapter",
    "model/harness calls",
    "tool execution",
    "terminal/PTY",
    "Robo-OS physical action",
    "audit persistence",
    "real Guardian enforcement",
}


def test_adapter_safety_gate_doc_exists_and_lists_required_tests() -> None:
    assert DOC_PATH.is_file()
    text = DOC_PATH.read_text(encoding="utf-8")

    for test_name in REQUIRED_TEST_NAMES:
        assert test_name in text


def test_adapter_safety_gate_doc_lists_freshness_and_forbidden_rules() -> None:
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "## Required Sparkbot Freshness Check" in text
    assert "fetch Sparkbot `origin/main`" in text
    assert "dirty Sparkbot local worktree is not source of truth" in text
    assert "## Forbidden Imports" in text
    assert "## Forbidden Behaviors" in text
    for forbidden_import in REQUIRED_FORBIDDEN_IMPORTS:
        assert forbidden_import in text
    for forbidden_behavior in REQUIRED_FORBIDDEN_BEHAVIORS:
        assert forbidden_behavior in text


def test_adapter_safety_gate_doc_keeps_gate_non_authorizing() -> None:
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "Production adapter is NO-GO." in text
    assert "`gate_status` does not authorize production adapter work" in text
    assert "Regression report is not audit persistence." in text
    assert "References are not authority." in text
    assert "Fake pipeline is not production runtime." in text
