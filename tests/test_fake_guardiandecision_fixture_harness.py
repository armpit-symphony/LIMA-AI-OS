"""Tests for the fake GuardianDecision fixture harness."""

from __future__ import annotations

import ast
from pathlib import Path

from tests.helpers.fake_guardiandecision_fixture_harness import (
    load_fake_guardiandecision_fixtures,
    run_fake_guardiandecision_fixture_regression,
    validate_fake_decision_shape,
    validate_test_only_status,
)


FIXTURE_ROOT = Path(__file__).parent / "fixtures" / "fake_guardian_decisions"
HELPER_PATH = Path(__file__).parent / "helpers" / "fake_guardiandecision_fixture_harness.py"

FORBIDDEN_NAMES = {
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
    "authorize",
    "allow_production",
}


def _fixtures() -> list[dict]:
    return load_fake_guardiandecision_fixtures(FIXTURE_ROOT)


def _report():
    return run_fake_guardiandecision_fixture_regression(_fixtures())


def test_harness_loads_all_fake_guardian_decision_fixture_files() -> None:
    fixtures = _fixtures()

    assert len(fixtures) > 0
    assert all(fixture["fixture_id"] for fixture in fixtures)
    assert len({fixture["fixture_id"] for fixture in fixtures}) == len(fixtures)


def test_fake_decision_shapes_validate_and_statuses_are_test_only() -> None:
    for fixture in _fixtures():
        assert validate_fake_decision_shape(fixture) == ()
        assert validate_test_only_status(fixture) is True
        assert fixture["expected_fake_guardian_decision"]["decision_status"].endswith(
            "_test_only"
        )


def test_allow_test_only_fixtures_remain_non_production() -> None:
    report = _report()
    allow_results = [result for result in report.results if result.status == "allow_test_only"]

    assert report.allow_test_only > 0
    assert allow_results
    for result in allow_results:
        assert "allow_test_only is not production authorization" in result.safety_notes
        assert "no execution" in result.safety_notes
        assert result.metadata["no_approval_metadata"] is True
        assert result.metadata["no_execution"] is True


def test_needs_approval_test_only_fixtures_remain_non_approving() -> None:
    fixtures = [
        fixture
        for fixture in _fixtures()
        if fixture["expected_fake_guardian_decision"]["decision_status"]
        == "needs_approval_test_only"
    ]
    report = _report()
    needs_approval_results = [
        result for result in report.results if result.status == "needs_approval_test_only"
    ]

    assert report.needs_approval_test_only > 0
    assert len(needs_approval_results) == len(fixtures)
    for fixture, result in zip(fixtures, needs_approval_results):
        decision = fixture["expected_fake_guardian_decision"]
        keys = _all_keys(fixture)

        assert decision["requires_approval"] is True
        assert decision["approval_ref"] is not None
        assert decision["approval_ref"].startswith("fixture-approval-ref:")
        assert "approval_ref is reference only" in result.safety_notes
        assert "no ApprovalMetadata" in result.safety_notes
        assert "approval_metadata" not in keys
        assert "approval_granted" not in keys


def test_blocked_and_safety_critical_fixtures_remain_non_authorizing() -> None:
    fixtures = _fixtures()
    report = _report()
    blocked_results = [result for result in report.results if result.status == "blocked_test_only"]
    safety_results = [
        result
        for result in report.results
        if result.fixture_type == "safety_critical_fake_guardian_decision"
    ]

    assert report.blocked_test_only > 0
    assert report.safety_critical > 0
    assert blocked_results
    assert safety_results

    for result in blocked_results:
        assert "blocked_test_only is non-authorizing" in result.safety_notes
        assert "safety flags present" in result.safety_notes

    for fixture in fixtures:
        decision = fixture["expected_fake_guardian_decision"]
        if (
            fixture["fixture_type"] == "safety_critical_fake_guardian_decision"
            or decision["risk_class"] in {"critical", "safety_critical"}
        ):
            assert decision["allow"] is False
            assert decision["safety_flags"]
            assert (
                decision["metadata"].get("requires_later_guardian_policy_approval_review")
                is True
                or decision["metadata"].get("owner_autonomy_override_allowed") is False
                or decision["metadata"].get("approval_ref_is_reference_only") is True
            )
            assert decision["metadata"]["no_execution"] is True


def test_expired_revoked_superseded_fixtures_remain_non_executable() -> None:
    report = _report()

    assert report.expired_test_only > 0
    assert report.revoked_test_only > 0
    assert report.superseded_test_only > 0

    for result in report.results:
        if result.status in {
            "expired_test_only",
            "revoked_test_only",
            "superseded_test_only",
        }:
            assert f"{result.status} is not executable" in result.safety_notes
            assert f"{result.status} is not production authorization" in result.safety_notes
            assert result.metadata["not_executable"] is True
            assert result.metadata["not_production_authorization"] is True
            if result.status == "superseded_test_only":
                assert "supersedes_decision_id is reference only" in result.safety_notes


def test_forbidden_methods_and_imports_are_absent() -> None:
    tree = ast.parse(HELPER_PATH.read_text(encoding="utf-8"))
    defined_names = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
    }
    imported_names = {
        alias.name.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    }

    assert FORBIDDEN_NAMES.isdisjoint(defined_names)
    assert "sparkbot" not in imported_names
    assert "app" not in imported_names
    assert "requests" not in imported_names
    assert "subprocess" not in imported_names
    assert "sqlite3" not in imported_names


def test_report_counts_are_accurate_for_current_fixture_suite() -> None:
    fixtures = _fixtures()
    report = _report()
    statuses = [
        fixture["expected_fake_guardian_decision"]["decision_status"] for fixture in fixtures
    ]

    assert report.total == len(fixtures)
    assert report.allow_test_only == statuses.count("allow_test_only")
    assert report.deny_test_only == statuses.count("deny_test_only")
    assert report.needs_approval_test_only == statuses.count("needs_approval_test_only")
    assert report.blocked_test_only == statuses.count("blocked_test_only")
    assert report.needs_review_test_only == statuses.count("needs_review_test_only")
    assert report.expired_test_only == statuses.count("expired_test_only")
    assert report.revoked_test_only == statuses.count("revoked_test_only")
    assert report.superseded_test_only == statuses.count("superseded_test_only")
    assert report.failed == 0
    assert len(report.results) == len(fixtures)
    assert report.metadata["test_only"] is True
    assert report.metadata["no_real_guardian_decision"] is True
    assert report.metadata["no_policy_evaluation"] is True
    assert report.metadata["no_approval_recording"] is True
    assert report.metadata["no_action_approval"] is True
    assert report.metadata["no_tool_or_model_calls"] is True
    assert report.metadata["no_audit_persistence"] is True
    assert report.metadata["no_sparkbot_calls"] is True


def _all_keys(value) -> set[str]:
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
