"""Tests for fixture regression safety gate documentation."""

from __future__ import annotations

from pathlib import Path


DOC_PATH = (
    Path(__file__).resolve().parents[1]
    / "docs"
    / "PHASE_2_6_FIXTURE_REGRESSION_CI_GATE_DOCS.md"
)

REQUIRED_TEST_NAMES = {
    "tests/test_adapter_boundaries.py",
    "tests/test_sparkbot_payload_fixture_mirror.py",
    "tests/test_nonproduction_adapter_fixture_harness.py",
    "tests/test_fixture_regression_harness.py",
    "tests/test_sparkbot_humaninput_adapter_skeleton.py",
    "tests/test_humaninput_fake_pipeline_bridge.py",
}

REQUIRED_BLOCKING_LANGUAGE = {
    "fixture regression fails",
    "adapter boundary tests fail",
    "Sparkbot imports are introduced",
    "production wiring appears",
    "model/tool execution appears",
    "critical/unknown paths auto-approve",
    "unsupported categories pass silently",
    "drift metadata is stale without review",
    "fixtures contain secrets/real user data",
    "robot/MCP fixtures imply execution readiness",
}


def test_fixture_regression_ci_gate_doc_exists_and_lists_required_tests() -> None:
    assert DOC_PATH.is_file()
    text = DOC_PATH.read_text(encoding="utf-8")

    for test_name in REQUIRED_TEST_NAMES:
        assert test_name in text


def test_fixture_regression_ci_gate_doc_lists_pr_blocking_conditions() -> None:
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "## PR Blocking Conditions" in text
    for phrase in REQUIRED_BLOCKING_LANGUAGE:
        assert phrase in text


def test_fixture_regression_ci_gate_doc_keeps_gate_non_production() -> None:
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "Fixture regression is not production runtime." in text
    assert "This phase does not implement CI infrastructure." in text
    assert "no runtime behavior added" in text
