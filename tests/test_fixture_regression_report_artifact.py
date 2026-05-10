"""Tests for review-only fixture regression report artifacts."""

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
    FixtureRegressionReport,
    FixtureRegressionResult,
    fixture_regression_report_to_dict,
    fixture_regression_report_to_markdown,
    load_payload_fixtures,
    run_fixture_regression,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = REPO_ROOT / "tests" / "fixtures" / "sparkbot_payloads"
HELPER_PATH = REPO_ROOT / "tests" / "helpers" / "fixture_regression_harness.py"

FORBIDDEN_SOURCE_STRINGS = {
    "save_to_db",
    "write_file",
    "upload(",
    "send(",
    "stream_chat_with_tools",
    "execute_tool",
    "import_sparkbot",
    "os.environ",
    "getenv",
    "inspect_sparkbot",
    "call_model",
    "call_tool",
    "call_driver",
}

FORBIDDEN_IMPORT_FRAGMENTS = {
    "sparkbot",
    "fastapi",
    "websocket",
    "requests",
    "httpx",
    "aiohttp",
    "sqlite",
    "sqlalchemy",
    "redis",
    "boto3",
    "stripe",
    "subprocess",
    "terminal",
    "pty",
    "openai",
    "anthropic",
    "google.generativeai",
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


def _run_report() -> Any:
    fixtures = load_payload_fixtures(FIXTURE_ROOT)
    return run_fixture_regression(fixtures, _make_harness())


def test_fixture_regression_markdown_report_is_reviewable() -> None:
    report = _run_report()
    markdown = fixture_regression_report_to_markdown(report)

    assert "# Fixture Regression Report" in markdown
    assert "## Gate Context" in markdown
    assert f"- total: {report.total}" in markdown
    assert f"- executed: {report.executed}" in markdown
    assert f"- unsupported_nonexecuting: {report.unsupported_nonexecuting}" in markdown
    assert f"- failed: {report.failed}" in markdown
    assert "- Gate status: pass" in markdown
    assert "- Sparkbot commit:" in markdown
    assert "No Sparkbot drift review supplied to report helper." in markdown
    assert "- Production adapter status: blocked" in markdown
    assert "non-production review artifact only" in markdown
    assert "not audit persistence" in markdown
    assert "not production telemetry" in markdown
    assert "not Guardian evidence" in markdown
    assert "not production authorization" in markdown
    assert "not runtime state" in markdown
    assert "production adapter blocked" in markdown
    for result in report.results:
        assert result.fixture_id in markdown


def test_fixture_regression_dict_report_matches_regression_counts() -> None:
    report = _run_report()
    artifact = fixture_regression_report_to_dict(report)

    assert artifact["schema_version"] == "fixture-regression-report/v1"
    assert artifact["total"] == report.total
    assert artifact["executed"] == report.executed
    assert artifact["unsupported_nonexecuting"] == report.unsupported_nonexecuting
    assert artifact["failed"] == report.failed
    assert artifact["gate_status"] == "pass"
    assert artifact["sparkbot_commit"] is None
    assert artifact["drift_summary"]["status"] == "not_checked"
    assert artifact["boundary_status"]["adapter_boundary_tests"] == "required"
    assert artifact["boundary_status"]["fixture_regression"] == "required"
    assert artifact["boundary_status"]["unsupported_categories_explicit"] is True
    assert (
        artifact["boundary_status"]["critical_unknown_auto_approval_blocked"] is True
    )
    assert artifact["production_adapter_status"] == "blocked"
    assert artifact["reviewed_at"] is None
    assert artifact["reviewer_notes"] is None
    assert len(artifact["results"]) == report.total
    assert "safety_notice" in artifact
    assert "not audit persistence" in artifact["safety_notice"]
    assert "not production telemetry" in artifact["safety_notice"]
    assert "not Guardian evidence" in artifact["safety_notice"]
    assert "not production authorization" in artifact["safety_notice"]
    assert "not runtime state" in artifact["safety_notice"]


def test_fixture_regression_report_helpers_do_not_write_files_by_default() -> None:
    report = _run_report()

    markdown = fixture_regression_report_to_markdown(report)
    artifact = fixture_regression_report_to_dict(report)

    assert isinstance(markdown, str)
    assert isinstance(artifact, dict)


def test_fixture_regression_report_accepts_explicit_gate_context() -> None:
    report = _run_report()

    artifact = fixture_regression_report_to_dict(
        report,
        sparkbot_commit="synthetic-reviewed-commit",
        drift_summary={"status": "reviewed", "notes": "Synthetic drift review."},
        gate_status="needs_review",
        boundary_status={"adapter_boundary_tests": "passed"},
        reviewed_at="2026-05-10",
        reviewer_notes="Synthetic review notes.",
    )
    markdown = fixture_regression_report_to_markdown(
        report,
        sparkbot_commit="synthetic-reviewed-commit",
        drift_summary={"status": "reviewed", "notes": "Synthetic drift review."},
        gate_status="needs_review",
        boundary_status={"adapter_boundary_tests": "passed"},
        reviewed_at="2026-05-10",
        reviewer_notes="Synthetic review notes.",
    )

    assert artifact["gate_status"] == "needs_review"
    assert artifact["sparkbot_commit"] == "synthetic-reviewed-commit"
    assert artifact["drift_summary"]["status"] == "reviewed"
    assert artifact["boundary_status"]["adapter_boundary_tests"] == "passed"
    assert artifact["production_adapter_status"] == "blocked"
    assert artifact["reviewed_at"] == "2026-05-10"
    assert artifact["reviewer_notes"] == "Synthetic review notes."
    assert "- Gate status: needs_review" in markdown
    assert "- Sparkbot commit: synthetic-reviewed-commit" in markdown
    assert "Synthetic drift review." in markdown
    assert "- Reviewed at: 2026-05-10" in markdown


def test_fixture_regression_report_exposes_safety_semantics() -> None:
    artifact = fixture_regression_report_to_dict(_run_report())

    robot_results = [
        result
        for result in artifact["results"]
        if str(result["source_surface"]).startswith("robotics_")
    ]
    unknown_results = [
        result for result in artifact["results"] if result["metadata"]["action_type"] == "unknown"
    ]
    mcp_results = [
        result
        for result in artifact["results"]
        if str(result["source_surface"]).startswith("mcp_")
    ]

    assert robot_results
    assert unknown_results
    assert mcp_results
    assert all(result["decision_status"] != "approved" for result in robot_results)
    assert all(result["decision_status"] != "approved" for result in unknown_results)
    assert all(
        "physical_action_not_performed" in result["safety_notes"]
        for result in robot_results
    )
    assert all(
        "mcp_tool_request_not_executed" in result["safety_notes"]
        for result in mcp_results
    )
    assert artifact["boundary_status"]["critical_unknown_auto_approval_blocked"] is True


def test_fixture_regression_report_gate_status_exposes_failed_counts() -> None:
    failed_report = FixtureRegressionReport(
        total=1,
        executed=0,
        unsupported_nonexecuting=0,
        failed=1,
        results=(
            FixtureRegressionResult(
                fixture_id="synthetic-failed-fixture",
                source_surface="chat_message_stream",
                status=FAILED,
                humaninput_source=None,
                pipeline_status=None,
                decision_status=None,
                unsupported_reason=None,
                safety_notes=("fixture_regression_failed",),
                metadata={"action_type": "unknown", "risk_class": "critical"},
            ),
        ),
        metadata={"test_only": True},
    )

    derived = fixture_regression_report_to_dict(failed_report)
    explicit = fixture_regression_report_to_dict(failed_report, gate_status="pass")

    assert derived["gate_status"] == "fail"
    assert derived["failed"] == 1
    assert explicit["gate_status"] == "pass"
    assert explicit["failed"] == 1
    assert explicit["results"][0]["status"] == FAILED


def test_fixture_regression_report_gate_status_needs_review_for_unsupported() -> None:
    report = run_fixture_regression(
        (
            {
                "fixture_id": "unsupported-report-fixture",
                "source_surface": "unknown_surface",
                "payload": {},
                "expected_humaninput_source": "text",
            },
        ),
        _make_harness(),
    )
    artifact = fixture_regression_report_to_dict(report)

    assert artifact["gate_status"] == "needs_review"
    assert artifact["unsupported_nonexecuting"] == 1
    assert artifact["boundary_status"]["unsupported_categories_explicit"] is True


def test_fixture_regression_report_helper_has_no_forbidden_imports_or_methods() -> None:
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
