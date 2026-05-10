"""Tests for the consolidated IntentEnvelope safety gate documentation."""

from __future__ import annotations

from pathlib import Path


DOC_PATH = (
    Path(__file__).resolve().parents[1] / "docs" / "INTENTENVELOPE_SAFETY_GATE.md"
)

REQUIRED_TEST_NAMES = {
    "tests/test_intent_envelope_test_fixtures.py",
    "tests/test_intent_envelope_fixture_harness.py",
    "tests/test_contract_imports.py",
    "tests/test_adapter_boundaries.py",
}

REQUIRED_FORBIDDEN_BEHAVIORS = {
    "real IntentCompiler implementation",
    "natural-language inference",
    "`raw_text` parsing",
    "model calls",
    "hidden parser",
    "heuristic free-text interpretation",
    "tool execution",
    "GuardianDecision creation",
    "production Sparkbot wiring",
    "`stream_chat_with_tools`",
    "`execute_tool`",
    "terminal/PTY",
    "Robo-OS physical action",
    "audit persistence",
    "real Guardian / policy / approval enforcement",
}


def test_intentenvelope_safety_gate_doc_exists_and_lists_required_tests() -> None:
    assert DOC_PATH.is_file()
    text = DOC_PATH.read_text(encoding="utf-8")

    for test_name in REQUIRED_TEST_NAMES:
        assert test_name in text


def test_intentenvelope_safety_gate_doc_states_core_rules() -> None:
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "`raw_text` is inert" in text
    assert "Explicit typed metadata is required" in text
    assert "IntentEnvelope is not authorization." in text
    assert "GuardianDecision remains mandatory" in text
    assert "real IntentCompiler" in text
    assert "natural-language inference" in text


def test_intentenvelope_safety_gate_doc_lists_review_and_blocking_rules() -> None:
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "## Forbidden Behaviors" in text
    for forbidden_behavior in REQUIRED_FORBIDDEN_BEHAVIORS:
        assert forbidden_behavior in text

    assert "## PR Blocking Conditions" in text
    assert "`raw_text` is parsed or interpreted" in text
    assert "IntentEnvelope is treated as authorization" in text
    assert "required intent fixture tests fail" in text

    assert "## Manual Review Requirements" in text
    assert "new IntentEnvelope fields" in text
    assert "any IntentCompiler-related code" in text
    assert "any natural-language handling" in text


def test_intentenvelope_safety_gate_doc_blocks_real_compiler_until_review() -> None:
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "## Exit Criteria for Real IntentCompiler Discussion" in text
    assert "explicit readiness review" in text
    assert "Phil/operator approval" in text
