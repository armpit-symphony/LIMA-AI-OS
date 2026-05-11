"""Tests for the consolidated Guardian request safety gate documentation."""

from __future__ import annotations

from pathlib import Path


DOC_PATH = (
    Path(__file__).resolve().parents[1] / "docs" / "GUARDIAN_REQUEST_SAFETY_GATE.md"
)

REQUIRED_TEST_NAMES = {
    "tests/test_guardian_request_test_fixtures.py",
    "tests/test_guardian_request_fixture_harness.py",
    "tests/test_contract_imports.py",
    "tests/test_adapter_boundaries.py",
    "tests/test_intent_envelope_fixture_harness.py",
}

REQUIRED_FORBIDDEN_BEHAVIORS = {
    "real GuardianDecision creation",
    "Guardian enforcement",
    "policy enforcement",
    "approval enforcement",
    "ApprovalMetadata recording",
    "action approval",
    "tool execution",
    "model calls",
    "audit persistence",
    "real IntentCompiler",
    "natural-language inference",
    "`raw_text` parsing",
    "production Sparkbot wiring",
    "`stream_chat_with_tools`",
    "`execute_tool`",
    "terminal/PTY",
    "Robo-OS physical action",
    "live auth/session lookup",
    "trusted device enforcement",
    "autonomy enforcement",
    "redaction runtime",
    "production Guardian request behavior",
}


def test_guardian_request_safety_gate_doc_exists_and_lists_required_tests() -> None:
    assert DOC_PATH.is_file()
    text = DOC_PATH.read_text(encoding="utf-8")

    for test_name in REQUIRED_TEST_NAMES:
        assert test_name in text


def test_guardian_request_safety_gate_doc_states_core_rules() -> None:
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "Guardian request is not GuardianDecision." in text
    assert "Guardian request is not approval." in text
    assert "`requested_tool_packs` are requests only." in text
    assert "`requested_tool_packs` are not `allowed_tool_packs`." in text
    assert "`requested_tool_packs` are not `granted_tool_packs`." in text
    assert "`approval_requirement_ref` is descriptive only." in text
    assert "`autonomy_context_ref` is passive only." in text
    assert "privacy/redaction metadata is not enforcement." in text
    assert "no ApprovalMetadata recording" in text
    assert "no audit persistence expected/created" in text


def test_guardian_request_safety_gate_doc_lists_forbidden_behaviors() -> None:
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "## Forbidden Behaviors" in text
    for forbidden_behavior in REQUIRED_FORBIDDEN_BEHAVIORS:
        assert forbidden_behavior in text


def test_guardian_request_safety_gate_doc_lists_review_and_blocking_rules() -> None:
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "## PR Blocking Conditions" in text
    assert "Guardian request is treated as GuardianDecision" in text
    assert "Guardian request is treated as approval" in text
    assert "`requested_tool_packs` become granted/allowed tools" in text
    assert "`approval_requirement_ref` becomes ApprovalMetadata" in text
    assert "ApprovalMetadata is recorded" in text
    assert "audit persistence is added" in text
    assert "required Guardian request fixture tests fail" in text

    assert "## Manual Review Requirements" in text
    assert "new Guardian request fields" in text
    assert "`requested_tool_packs` semantics" in text
    assert "`approval_requirement_ref` semantics" in text
    assert "`autonomy_context_ref` semantics" in text
    assert "any request to move toward real Guardian enforcement" in text


def test_guardian_request_safety_gate_doc_blocks_real_decision_until_review() -> None:
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "## Exit Criteria for Real GuardianDecision Discussion" in text
    assert "explicit readiness review" in text
    assert "Phil/operator approval" in text
