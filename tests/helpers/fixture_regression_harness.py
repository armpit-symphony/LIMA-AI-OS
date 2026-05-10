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
