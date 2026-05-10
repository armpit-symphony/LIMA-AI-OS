"""Tests for the test-only Guardian request fixture harness."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

from tests.helpers.guardian_request_fixture_harness import (
    FORBIDDEN_SHAPE_FIELDS,
    REQUIRED_REQUEST_FIELDS,
    STATUS_APPROVAL_REQUIRED,
    STATUS_FAILED,
    STATUS_INVALID,
    STATUS_NEEDS_REVIEW,
    STATUS_SAFETY_CRITICAL,
    STATUS_VALID,
    load_guardian_request_fixtures,
    run_guardian_request_fixture_regression,
    validate_expected_guardian_request_shape,
    validate_explicit_request,
)


FIXTURE_ROOT = Path(__file__).parent / "fixtures" / "guardian_requests"
HARNESS_PATH = Path(__file__).parent / "helpers" / "guardian_request_fixture_harness.py"


def _fixtures_by_type(fixture_type: str) -> list[dict[str, Any]]:
    return [
        fixture
        for fixture in load_guardian_request_fixtures(FIXTURE_ROOT)
        if fixture["fixture_type"] == fixture_type
    ]


def _all_keys(value: Any) -> set[str]:
    if isinstance(value, dict):
        keys = set(value)
        for item in value.values():
            keys.update(_all_keys(item))
        return keys
    if isinstance(value, list):
        keys: set[str] = set()
        for item in value:
            keys.update(_all_keys(item))
        return keys
    return set()


def test_loads_all_guardian_request_fixture_files() -> None:
    fixtures = load_guardian_request_fixtures(FIXTURE_ROOT)

    assert len(fixtures) == 19
    assert all(fixture["fixture_id"] for fixture in fixtures)
    assert {
        "valid_guardian_request",
        "invalid_guardian_request",
        "safety_critical_guardian_request",
        "approval_required_guardian_request",
    } <= {fixture["fixture_type"] for fixture in fixtures}


def test_valid_fixtures_pass_request_shape_validation() -> None:
    valid_fixtures = _fixtures_by_type("valid_guardian_request")

    assert len(valid_fixtures) == 4
    for fixture in valid_fixtures:
        explicit_request = fixture["explicit_request"]
        expected_request = fixture["expected_guardian_request"]

        assert validate_explicit_request(fixture) == ()
        assert validate_expected_guardian_request_shape(fixture) is True
        assert set(REQUIRED_REQUEST_FIELDS) <= set(explicit_request)
        assert set(REQUIRED_REQUEST_FIELDS) <= set(expected_request)
        assert "requested_tool_packs" in explicit_request
        assert "allowed_tool_packs" not in _all_keys(fixture)
        assert "granted_tool_packs" not in _all_keys(fixture)


def test_invalid_fixtures_report_missing_request_fields() -> None:
    report = run_guardian_request_fixture_regression(
        _fixtures_by_type("invalid_guardian_request")
    )

    assert report.total == 5
    assert report.valid == 0
    assert report.invalid == 3
    assert report.needs_review == 2
    assert report.failed == 0
    for result in report.results:
        assert result.status in {
            STATUS_INVALID,
            STATUS_NEEDS_REVIEW,
            "clarification_needed",
        }
        assert result.status != STATUS_VALID
        assert result.missing_request_fields
        assert result.request_shape_valid is False


def test_safety_critical_fixtures_remain_non_authorizing() -> None:
    report = run_guardian_request_fixture_regression(
        _fixtures_by_type("safety_critical_guardian_request")
    )

    assert report.total == 4
    assert report.safety_critical == 4
    assert report.failed == 0
    for result in report.results:
        safety_notes = " ".join(result.safety_notes)
        assert result.status == STATUS_SAFETY_CRITICAL
        assert "Guardian/policy/approval review" in safety_notes
        assert "no authorization" in safety_notes
        assert "no auto-approval" in safety_notes
        assert "guardian_decision" not in result.metadata


def test_approval_required_fixtures_remain_descriptive() -> None:
    report = run_guardian_request_fixture_regression(
        _fixtures_by_type("approval_required_guardian_request")
    )

    assert report.total == 6
    assert report.approval_required == 6
    assert report.failed == 0
    for fixture, result in zip(
        _fixtures_by_type("approval_required_guardian_request"),
        report.results,
        strict=True,
    ):
        expected_request = fixture["expected_guardian_request"]
        keys = _all_keys(fixture)
        safety_notes = " ".join(result.safety_notes)

        assert result.status == STATUS_APPROVAL_REQUIRED
        assert expected_request["approval_requirement_ref"]
        assert expected_request["metadata"]["approval_requirement_is_descriptive"] is True
        assert "approval_requirement_ref remains descriptive" in safety_notes
        assert FORBIDDEN_SHAPE_FIELDS.isdisjoint(keys)


def test_passive_metadata_remains_passive() -> None:
    for fixture in load_guardian_request_fixtures(FIXTURE_ROOT):
        explicit_request = fixture["explicit_request"]
        expected_request = fixture["expected_guardian_request"]
        keys = _all_keys(fixture)

        assert "allowed_tool_packs" not in keys
        assert "granted_tool_packs" not in keys
        assert "approval_granted" not in keys
        assert "passive" in explicit_request.get("autonomy_context_ref", "")
        assert "enforcement" not in explicit_request["privacy_class"]
        assert "enforcement" not in explicit_request["redaction_class"]

        if expected_request is not None:
            assert "passive" in expected_request["autonomy_context_ref"]
            assert expected_request["privacy_class"] == fixture["privacy_class"]
            assert expected_request["redaction_class"] == fixture["redaction_class"]


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
        "create_guardian_decision",
        "decide",
        "enforce",
        "approve",
        "approve_action",
        "record_approval",
        "execute",
        "execute_tool",
        "call_tool",
        "call_model",
        "persist",
        "save_to_db",
        "write_audit",
        "import_sparkbot",
        "infer",
        "parse",
    }

    assert all(forbidden not in imported_text for forbidden in forbidden_imports)
    assert forbidden_method_names.isdisjoint(function_names)
    assert forbidden_method_names.isdisjoint(attribute_names)


def test_report_counts_are_accurate_for_current_fixture_suite() -> None:
    fixtures = load_guardian_request_fixtures(FIXTURE_ROOT)
    report = run_guardian_request_fixture_regression(fixtures)

    assert report.total == len(fixtures)
    assert report.valid == 4
    assert report.invalid == 3
    assert report.needs_review == 2
    assert report.safety_critical == 4
    assert report.approval_required == 6
    assert report.failed == 0
    assert report.metadata["test_only"] is True
    assert report.metadata["guardian_request_is_not_decision"] is True
    assert report.metadata["guardian_request_is_not_approval"] is True
    assert report.metadata["no_enforcement"] is True
    assert report.metadata["no_audit_persistence"] is True


def test_no_decision_approval_or_side_effect_fields_in_results() -> None:
    report = run_guardian_request_fixture_regression(
        load_guardian_request_fixtures(FIXTURE_ROOT)
    )

    for result in report.results:
        assert result.status != STATUS_FAILED
        assert "no GuardianDecision" not in result.metadata
        assert "no_approval" in result.metadata
        assert result.metadata["no_execution"] is True
