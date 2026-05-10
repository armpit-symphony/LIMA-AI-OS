"""Tests for the test-only IntentEnvelope fixture harness."""

from __future__ import annotations

import ast
from copy import deepcopy
from pathlib import Path
from typing import Any

from tests.helpers.intent_envelope_fixture_harness import (
    REQUIRED_EXPLICIT_METADATA_FIELDS,
    STATUS_CLARIFICATION_NEEDED,
    STATUS_FAILED,
    STATUS_INVALID,
    STATUS_SAFETY_CRITICAL,
    STATUS_VALID,
    load_intent_fixtures,
    run_intent_fixture_regression,
    validate_expected_envelope_shape,
    validate_explicit_metadata,
)


FIXTURE_ROOT = Path(__file__).parent / "fixtures" / "intent_envelopes"
HARNESS_PATH = Path(__file__).parent / "helpers" / "intent_envelope_fixture_harness.py"


def _fixtures_by_type(fixture_type: str) -> list[dict[str, Any]]:
    return [
        fixture
        for fixture in load_intent_fixtures(FIXTURE_ROOT)
        if fixture["fixture_type"] == fixture_type
    ]


def test_loads_all_intent_fixture_files() -> None:
    fixtures = load_intent_fixtures(FIXTURE_ROOT)

    assert len(fixtures) == 15
    assert all(fixture["fixture_id"] for fixture in fixtures)
    assert {
        "typed_intent",
        "invalid_missing_metadata",
        STATUS_CLARIFICATION_NEEDED,
        "safety_critical_intent",
    } <= {fixture["fixture_type"] for fixture in fixtures}


def test_valid_typed_fixtures_pass_metadata_and_envelope_shape_validation() -> None:
    typed_fixtures = _fixtures_by_type("typed_intent")

    assert typed_fixtures
    for fixture in typed_fixtures:
        assert validate_explicit_metadata(fixture) == ()
        assert validate_expected_envelope_shape(fixture) is True
        assert fixture["expected_intent_envelope"]["metadata"]["source"] == (
            "explicit_metadata"
        )


def test_invalid_missing_metadata_fixtures_report_missing_fields() -> None:
    report = run_intent_fixture_regression(_fixtures_by_type("invalid_missing_metadata"))

    assert report.total == 3
    assert report.valid == 0
    assert report.invalid == 3
    assert report.failed == 0
    for result in report.results:
        assert result.status in {STATUS_INVALID, STATUS_CLARIFICATION_NEEDED}
        assert result.status != STATUS_VALID
        assert result.missing_metadata_fields
        assert result.envelope_shape_valid is False
        assert result.expected_status in {"invalid", "unknown", STATUS_CLARIFICATION_NEEDED}


def test_clarification_fixtures_report_clarification_needed() -> None:
    report = run_intent_fixture_regression(
        _fixtures_by_type(STATUS_CLARIFICATION_NEEDED)
    )

    assert report.total == 2
    assert report.clarification_needed == 2
    assert report.failed == 0
    assert all(result.status == STATUS_CLARIFICATION_NEEDED for result in report.results)


def test_safety_critical_fixtures_remain_non_authorizing() -> None:
    report = run_intent_fixture_regression(_fixtures_by_type("safety_critical_intent"))

    assert report.total == 4
    assert report.safety_critical == 4
    assert report.failed == 0
    for result in report.results:
        safety_notes = " ".join(result.safety_notes)
        assert result.status == STATUS_SAFETY_CRITICAL
        assert "Guardian/policy/approval review" in safety_notes
        assert "no authorization" in safety_notes
        assert "no auto-approval" in safety_notes
        assert "GuardianDecision" not in result.metadata


def test_raw_text_remains_inert_for_metadata_and_shape_validation() -> None:
    for fixture in load_intent_fixtures(FIXTURE_ROOT):
        changed = deepcopy(fixture)
        changed["raw_text"] = "This inert fixture text changed completely."

        assert validate_explicit_metadata(changed) == validate_explicit_metadata(fixture)
        assert validate_expected_envelope_shape(changed) == validate_expected_envelope_shape(
            fixture
        )


def test_forbidden_methods_and_imports_are_absent() -> None:
    tree = ast.parse(HARNESS_PATH.read_text(encoding="utf-8"))
    imported_modules: list[str] = []
    function_names: list[str] = []
    attribute_names: list[str] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_modules.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            imported_modules.append(node.module)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            function_names.append(node.name)
        elif isinstance(node, ast.Attribute):
            attribute_names.append(node.attr)

    imported_text = "\n".join(imported_modules).lower()
    forbidden_imports = {
        "sparkbot",
        "fastapi",
        "websocket",
        "stream_chat_with_tools",
        "execute_tool",
        "requests",
        "httpx",
        "aiohttp",
        "sqlite",
        "sqlalchemy",
        "openai",
        "anthropic",
        "google.generativeai",
    }
    forbidden_method_names = {
        "compile",
        "infer",
        "parse",
        "parse_intent",
        "infer_intent",
        "call_model",
        "call_tool",
        "execute",
        "approve",
        "create_guardian_decision",
        "authorize",
        "persist",
        "save_to_db",
        "import_sparkbot",
    }

    assert all(forbidden not in imported_text for forbidden in forbidden_imports)
    assert forbidden_method_names.isdisjoint(function_names)
    assert forbidden_method_names.isdisjoint(attribute_names)


def test_report_counts_are_accurate_for_current_fixture_suite() -> None:
    fixtures = load_intent_fixtures(FIXTURE_ROOT)
    report = run_intent_fixture_regression(fixtures)

    assert report.total == len(fixtures)
    assert report.valid == 6
    assert report.invalid == 3
    assert report.clarification_needed == 2
    assert report.safety_critical == 4
    assert report.failed == 0
    assert report.metadata["test_only"] is True
    assert report.metadata["explicit_metadata_only"] is True
    assert report.metadata["raw_text_inert"] is True
    assert report.metadata["no_guardian_decision"] is True


def test_current_valid_fixtures_require_all_explicit_metadata_fields() -> None:
    fixtures = _fixtures_by_type("typed_intent") + _fixtures_by_type(
        "safety_critical_intent"
    )

    assert fixtures
    for fixture in fixtures:
        explicit_metadata = fixture["explicit_metadata"]
        assert set(REQUIRED_EXPLICIT_METADATA_FIELDS) <= set(explicit_metadata)
        assert validate_explicit_metadata(fixture) == ()
        assert validate_expected_envelope_shape(fixture) is True


def test_no_guardian_decision_expected_or_created_in_harness_results() -> None:
    report = run_intent_fixture_regression(load_intent_fixtures(FIXTURE_ROOT))
    forbidden_keys = {
        "guardian_decision",
        "guardian_decision_id",
        "decision_id",
        "approval_metadata",
        "approval_id",
        "policy_decision",
        "execution_id",
    }

    for result in report.results:
        assert forbidden_keys.isdisjoint(result.metadata)
        assert "no GuardianDecision is created" in result.safety_notes
        assert result.status != STATUS_FAILED
