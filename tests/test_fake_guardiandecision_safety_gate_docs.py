"""Tests for the consolidated fake GuardianDecision safety gate documentation."""

from __future__ import annotations

from pathlib import Path


DOC_PATH = (
    Path(__file__).resolve().parents[1]
    / "docs"
    / "FAKE_GUARDIANDECISION_SAFETY_GATE.md"
)

REQUIRED_TEST_NAMES = {
    "tests/test_fake_guardiandecision_test_fixtures.py",
    "tests/test_fake_guardiandecision_fixture_harness.py",
    "tests/test_guardian_request_fixture_harness.py",
    "tests/test_guardian_request_test_fixtures.py",
    "tests/test_contract_imports.py",
    "tests/test_adapter_boundaries.py",
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
    "production GuardianDecision behavior",
}


def test_fake_guardiandecision_safety_gate_doc_exists_and_lists_required_tests() -> None:
    assert DOC_PATH.is_file()
    text = DOC_PATH.read_text(encoding="utf-8")

    for test_name in REQUIRED_TEST_NAMES:
        assert test_name in text


def test_fake_guardiandecision_safety_gate_doc_states_core_rules() -> None:
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "Fake GuardianDecision is test-only." in text
    assert "Fake GuardianDecision is not production authorization." in text
    assert "`allow_test_only` is not production allow." in text
    assert "`approval_ref` is not ApprovalMetadata." in text
    assert "`requires_approval` is not approval granted." in text
    assert "safety-critical fake decisions must not auto-approve." in text
    assert "expired/revoked/superseded fake decisions are not executable." in text
    assert "fake harness is not real Guardian." in text
    assert "real GuardianDecision remains blocked." in text
    assert "Spine/Audit records; it does not execute." in text


def test_fake_guardiandecision_safety_gate_doc_lists_forbidden_behaviors() -> None:
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "## Forbidden Behaviors" in text
    for forbidden_behavior in REQUIRED_FORBIDDEN_BEHAVIORS:
        assert forbidden_behavior in text


def test_fake_guardiandecision_safety_gate_doc_lists_review_and_blocking_rules() -> None:
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "## PR Blocking Conditions" in text
    assert "fake GuardianDecision is treated as real GuardianDecision" in text
    assert "fake GuardianDecision is treated as production authorization" in text
    assert "`allow_test_only` is treated as production allow" in text
    assert "`needs_approval_test_only` is treated as approval granted" in text
    assert "`approval_ref` becomes ApprovalMetadata" in text
    assert "ApprovalMetadata is recorded" in text
    assert "safety-critical fake decision auto-approves" in text
    assert "expired/revoked/superseded fake decision becomes executable" in text
    assert "audit persistence is added" in text
    assert "execution appears" in text

    assert "## Manual Review Requirements" in text
    assert "new fake GuardianDecision fields" in text
    assert "new `decision_status` values" in text
    assert "`approval_ref` semantics" in text
    assert "`tool_pack_refs` semantics" in text
    assert "lifecycle decision semantics: expired/revoked/superseded" in text
    assert "any request to move toward real GuardianDecision or enforcement" in text


def test_fake_guardiandecision_safety_gate_doc_blocks_real_decision_until_review() -> None:
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "## Exit Criteria for Real GuardianDecision Discussion" in text
    assert "explicit readiness review" in text
    assert "fake-to-real migration plan" in text
    assert "Phil/operator approval" in text
