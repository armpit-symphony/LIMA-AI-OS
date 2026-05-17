"""Candidate preview acceptance design tests for Phase 36.1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_36_1_CANDIDATE_PREVIEW_ACCEPTANCE_DESIGN.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_36_1_candidate_preview_acceptance_design.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_36_1_is_acceptance_design_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "36.1"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_implementation_added"] is False
    assert fixture["runtime_files_changed_in_phase_36_1"] == []
    assert "adds no runtime code" in phase_doc


def test_required_preview_fields_include_all_safety_flags() -> None:
    fields = set(_load_json(PHASE_FIXTURE_PATH)["required_preview_fields"])
    for field in {
        "non_authoritative",
        "execution_allowed",
        "side_effects_allowed",
        "approval_granted",
        "dispatch_allowed",
        "persistence_allowed",
        "phase_5_humaninput_runtime_bridge_gated",
        "humaninput_bridge_active",
        "sparkbot_wiring_active",
        "live_adapter_active",
        "external_calls_allowed",
        "robotics_allowed",
        "physical_world_allowed",
        "blocked_claims",
        "warnings",
    }:
        assert field in fields


def test_input_coverage_includes_suspicious_and_nested_cases() -> None:
    coverage = set(_load_json(PHASE_FIXTURE_PATH)["input_coverage"])
    assert "benign_caller_provided_input" in coverage
    assert "missing_input" in coverage
    assert "malformed_input" in coverage
    assert "unknown_status_values" in coverage
    assert "nested_suspicious_metadata" in coverage
    assert "bypass_wording" in coverage
    assert "robotics_physical_world_claims" in coverage


def test_required_safety_outcomes_keep_preview_inert() -> None:
    outcomes = _load_json(PHASE_FIXTURE_PATH)["required_safety_outcomes"]
    assert all(outcomes.values())
    assert outcomes["non_authoritative"] is True
    assert outcomes["non_executing"] is True
    assert outcomes["approval_free"] is True
    assert outcomes["dispatch_free"] is True
    assert outcomes["persistence_free"] is True
    assert outcomes["physical_world_free"] is True


def test_static_boundary_scan_is_required_before_runtime_lands() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["static_boundary_scan_required"] is True
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_36_1*"))
