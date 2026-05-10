"""Test-only regression helpers for LIMA-owned payload fixtures."""

from __future__ import annotations

import json
from collections import defaultdict
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from lima.guardian import AdapterFixtureHarness


PASSED = "passed"
UNSUPPORTED_NONEXECUTING = "unsupported_nonexecuting"
FAILED = "failed"
GATE_PASS = "pass"
GATE_FAIL = "fail"
GATE_NEEDS_REVIEW = "needs_review"
REPORT_SCHEMA_VERSION = "fixture-regression-report/v1"
SAFETY_NOTICE = (
    "non-production review artifact only",
    "not audit persistence",
    "not production telemetry",
    "not Guardian evidence",
    "not production authorization",
    "not runtime state",
    "no Sparkbot imports",
    "no execution",
    "production adapter blocked",
)

SUPPORTED_SURFACE_PREFIXES = (
    "auth_session_",
    "chat_",
    "frontend_chat",
    "mcp_",
    "meeting_",
    "model_routing_",
    "operator_",
    "robotics_",
    "sparkbud_",
    "voice_",
    "workstation_",
)


@dataclass(frozen=True)
class FixtureRegressionResult:
    fixture_id: str
    source_surface: str
    status: str
    humaninput_source: str | None
    pipeline_status: str | None
    decision_status: str | None
    unsupported_reason: str | None
    safety_notes: Sequence[str] = field(default_factory=tuple)
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class FixtureRegressionReport:
    total: int
    executed: int
    unsupported_nonexecuting: int
    failed: int
    results: Sequence[FixtureRegressionResult] = field(default_factory=tuple)
    metadata: Mapping[str, Any] = field(default_factory=dict)


def load_payload_fixtures(fixtures_dir: Path) -> list[dict[str, Any]]:
    """Load every JSON fixture object from a LIMA-owned fixture directory."""

    fixtures: list[dict[str, Any]] = []
    for path in sorted(fixtures_dir.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise ValueError(f"{path.name} must contain a JSON list")
        for item in data:
            if not isinstance(item, dict):
                raise ValueError(f"{path.name} contains a non-object fixture")
            fixtures.append(item)
    return fixtures


def group_fixtures_by_surface(
    fixtures: Sequence[Mapping[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for fixture in fixtures:
        source_surface = _fixture_str(fixture, "source_surface")
        grouped[source_surface].append(dict(fixture))
    return dict(grouped)


def run_fixture_regression(
    fixtures: Sequence[Mapping[str, Any]],
    harness: AdapterFixtureHarness,
) -> FixtureRegressionReport:
    results = tuple(_run_one_fixture(fixture, harness) for fixture in fixtures)
    return FixtureRegressionReport(
        total=len(results),
        executed=sum(1 for result in results if result.status == PASSED),
        unsupported_nonexecuting=sum(
            1 for result in results if result.status == UNSUPPORTED_NONEXECUTING
        ),
        failed=sum(1 for result in results if result.status == FAILED),
        results=results,
        metadata={
            "fixture_regression_harness": "test_only",
            "test_only": True,
            "non_production": True,
            "non_executing": True,
            "lima_owned_fixtures_only": True,
            "executed_means_fake_harness_processed": True,
        },
    )


def fixture_regression_report_to_dict(
    report: FixtureRegressionReport,
    *,
    sparkbot_commit: str | None = None,
    drift_summary: Mapping[str, Any] | None = None,
    gate_status: str | None = None,
    boundary_status: Mapping[str, Any] | None = None,
    production_adapter_status: str = "blocked",
    reviewed_at: str | None = None,
    reviewer_notes: str | None = None,
) -> Mapping[str, Any]:
    """Format a fixture regression report as a review-only dictionary."""

    resolved_gate_status = gate_status or _derive_gate_status(report)
    resolved_drift_summary = _drift_summary(drift_summary)
    resolved_boundary_status = _boundary_status(report, boundary_status)
    return {
        "schema_version": REPORT_SCHEMA_VERSION,
        "total": report.total,
        "executed": report.executed,
        "unsupported_nonexecuting": report.unsupported_nonexecuting,
        "failed": report.failed,
        "gate_status": resolved_gate_status,
        "sparkbot_commit": sparkbot_commit,
        "drift_summary": resolved_drift_summary,
        "boundary_status": resolved_boundary_status,
        "production_adapter_status": production_adapter_status,
        "reviewed_at": reviewed_at,
        "reviewer_notes": reviewer_notes,
        "results": [
            {
                "fixture_id": result.fixture_id,
                "source_surface": result.source_surface,
                "status": result.status,
                "humaninput_source": result.humaninput_source,
                "pipeline_status": result.pipeline_status,
                "decision_status": result.decision_status,
                "unsupported_reason": result.unsupported_reason,
                "safety_notes": tuple(result.safety_notes),
                "metadata": dict(result.metadata),
            }
            for result in report.results
        ],
        "metadata": dict(report.metadata),
        "safety_notice": tuple(SAFETY_NOTICE),
    }


def fixture_regression_report_to_markdown(
    report: FixtureRegressionReport,
    *,
    sparkbot_commit: str | None = None,
    drift_summary: Mapping[str, Any] | None = None,
    gate_status: str | None = None,
    boundary_status: Mapping[str, Any] | None = None,
    production_adapter_status: str = "blocked",
    reviewed_at: str | None = None,
    reviewer_notes: str | None = None,
) -> str:
    """Format a fixture regression report as markdown for human review."""

    resolved_gate_status = gate_status or _derive_gate_status(report)
    resolved_drift_summary = _drift_summary(drift_summary)
    resolved_boundary_status = _boundary_status(report, boundary_status)
    lines = [
        "# Fixture Regression Report",
        "",
        "## Summary",
        "",
        f"- total: {report.total}",
        f"- executed: {report.executed}",
        f"- unsupported_nonexecuting: {report.unsupported_nonexecuting}",
        f"- failed: {report.failed}",
        "",
        "## Gate Context",
        "",
        f"- Gate status: {_markdown_cell(resolved_gate_status)}",
        f"- Sparkbot commit: {_markdown_cell(sparkbot_commit)}",
        "- Drift summary:",
    ]
    lines.extend(
        f"  - {_markdown_cell(key)}: {_markdown_cell(value)}"
        for key, value in resolved_drift_summary.items()
    )
    lines.extend(
        [
            "- Boundary status:",
        ]
    )
    lines.extend(
        f"  - {_markdown_cell(key)}: {_markdown_cell(value)}"
        for key, value in resolved_boundary_status.items()
    )
    lines.extend(
        [
            f"- Production adapter status: {_markdown_cell(production_adapter_status)}",
            f"- Reviewed at: {_markdown_cell(reviewed_at)}",
            f"- Reviewer notes: {_markdown_cell(reviewer_notes)}",
            "",
            "## Status Summary",
            "",
            f"- passed: {sum(1 for result in report.results if result.status == PASSED)}",
            f"- unsupported_nonexecuting: {report.unsupported_nonexecuting}",
            f"- failed: {report.failed}",
            "",
            "## Fixture Results",
            "",
            (
                "| fixture_id | source_surface | status | humaninput_source | "
                "pipeline_status | decision_status | unsupported_reason | safety_notes |"
            ),
            "| --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for result in report.results:
        lines.append(
            "| "
            + " | ".join(
                _markdown_cell(value)
                for value in (
                    result.fixture_id,
                    result.source_surface,
                    result.status,
                    result.humaninput_source,
                    result.pipeline_status,
                    result.decision_status,
                    result.unsupported_reason,
                    ", ".join(result.safety_notes),
                )
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Safety Notice",
            "",
        ]
    )
    lines.extend(f"- {notice}" for notice in SAFETY_NOTICE)
    lines.append("- Report is not audit persistence.")
    lines.append("- Report is not production telemetry.")
    lines.append("- Report is not Guardian evidence.")
    lines.append("- Report is not production authorization.")
    lines.append("- Report is not runtime state.")
    lines.append("- Production adapter remains blocked.")
    return "\n".join(lines) + "\n"


def _run_one_fixture(
    fixture: Mapping[str, Any],
    harness: AdapterFixtureHarness,
) -> FixtureRegressionResult:
    fixture_id = _fixture_str(fixture, "fixture_id")
    source_surface = _fixture_str(fixture, "source_surface")
    if not _is_supported_surface(source_surface):
        return FixtureRegressionResult(
            fixture_id=fixture_id,
            source_surface=source_surface,
            status=UNSUPPORTED_NONEXECUTING,
            humaninput_source=None,
            pipeline_status=None,
            decision_status=None,
            unsupported_reason="No safe non-production harness mapping for source_surface.",
            safety_notes=("unsupported_nonexecuting", "no_external_action"),
            metadata=_base_metadata(fixture_id, source_surface),
        )

    try:
        result = harness.run_fixture(fixture)
    except (KeyError, TypeError, ValueError) as exc:
        return FixtureRegressionResult(
            fixture_id=fixture_id,
            source_surface=source_surface,
            status=FAILED,
            humaninput_source=None,
            pipeline_status=None,
            decision_status=None,
            unsupported_reason=None,
            safety_notes=("fixture_regression_failed",),
            metadata={
                **_base_metadata(fixture_id, source_surface),
                "error_type": type(exc).__name__,
                "error_message": str(exc),
            },
        )

    pipeline_result = result.pipeline_result
    human_input = result.human_input
    payload_metadata = human_input.metadata.get("payload_metadata")
    if not isinstance(payload_metadata, Mapping):
        payload_metadata = {}
    return FixtureRegressionResult(
        fixture_id=fixture_id,
        source_surface=source_surface,
        status=PASSED,
        humaninput_source=human_input.source.value,
        pipeline_status=str(pipeline_result.status),
        decision_status=_enum_value(pipeline_result.guardian_decision.status),
        unsupported_reason=None,
        safety_notes=_safety_notes(source_surface, payload_metadata, pipeline_result),
        metadata={
            **_base_metadata(fixture_id, source_surface),
            "action_type": pipeline_result.request.action_type.value,
            "risk_class": pipeline_result.request.risk_class,
            "lineage_id": pipeline_result.lineage_id,
            "fake_pipeline": pipeline_result.metadata.get("fake_pipeline") is True,
            "payload_non_executing": payload_metadata.get("non_executing") is True,
            "model_call_performed": payload_metadata.get("model_call_performed") is True,
            "tool_execution_performed": payload_metadata.get("tool_execution_performed")
            is True,
            "driver_call_performed": payload_metadata.get("driver_call_performed")
            is True,
            "persistence_performed": payload_metadata.get("persistence_performed")
            is True,
        },
    )


def _is_supported_surface(source_surface: str) -> bool:
    return source_surface.startswith(SUPPORTED_SURFACE_PREFIXES)


def _safety_notes(
    source_surface: str,
    payload_metadata: Mapping[str, Any],
    pipeline_result: Any,
) -> tuple[str, ...]:
    notes = ["non_executing", "fake_pipeline_only"]
    if source_surface.startswith("mcp_"):
        notes.append("mcp_tool_request_not_executed")
    if source_surface.startswith("robotics_"):
        notes.append("robot_safety_critical")
        notes.append("physical_action_not_performed")
    if source_surface.startswith("auth_session_"):
        notes.append("auth_session_refs_not_authority")
    if source_surface.startswith("model_routing_"):
        notes.append("model_routing_metadata_passive")
    if payload_metadata.get("autonomy_context_ref"):
        notes.append("autonomy_metadata_passive")
    if _enum_value(pipeline_result.guardian_decision.status) != "approved":
        notes.append("not_auto_approved")
    return tuple(notes)


def _base_metadata(fixture_id: str, source_surface: str) -> Mapping[str, Any]:
    return {
        "fixture_id": fixture_id,
        "source_surface": source_surface,
        "test_only": True,
        "non_production": True,
        "non_executing": True,
    }


def _fixture_str(fixture: Mapping[str, Any], key: str) -> str:
    value = fixture.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"{key} must be a non-empty string")
    return value


def _enum_value(value: Any) -> str:
    enum_value = getattr(value, "value", None)
    if isinstance(enum_value, str):
        return enum_value
    return str(value)


def _derive_gate_status(report: FixtureRegressionReport) -> str:
    if report.failed > 0:
        return GATE_FAIL
    if report.unsupported_nonexecuting > 0:
        return GATE_NEEDS_REVIEW
    return GATE_PASS


def _drift_summary(drift_summary: Mapping[str, Any] | None) -> Mapping[str, Any]:
    if drift_summary is not None:
        return dict(drift_summary)
    return {
        "status": "not_checked",
        "notes": "No Sparkbot drift review supplied to report helper.",
    }


def _boundary_status(
    report: FixtureRegressionReport,
    boundary_status: Mapping[str, Any] | None,
) -> Mapping[str, Any]:
    default_status = {
        "adapter_boundary_tests": "required",
        "fixture_regression": "required",
        "unsupported_categories_explicit": all(
            result.status != UNSUPPORTED_NONEXECUTING or bool(result.unsupported_reason)
            for result in report.results
        ),
        "critical_unknown_auto_approval_blocked": _critical_unknown_auto_approval_blocked(
            report
        ),
    }
    if boundary_status is None:
        return default_status
    return {**default_status, **dict(boundary_status)}


def _critical_unknown_auto_approval_blocked(report: FixtureRegressionReport) -> bool:
    guarded_results = [
        result
        for result in report.results
        if result.metadata.get("action_type") == "unknown"
        or str(result.metadata.get("risk_class")).lower() == "critical"
        or result.source_surface.startswith(("operator_", "robotics_"))
    ]
    return all(result.decision_status != "approved" for result in guarded_results)


def _markdown_cell(value: object) -> str:
    if value is None:
        return ""
    return str(value).replace("|", "\\|").replace("\n", " ")
