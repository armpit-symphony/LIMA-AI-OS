"""Runtime slice regression and gap review tests for Phase 31.2."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_31_2_RUNTIME_SLICE_REGRESSION_AND_GAP_REVIEW.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_31_2_runtime_slice_regression_and_gap_review.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_31_2_is_regression_and_gap_review_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "31.2"
    assert fixture["runtime_code_modified"] is False
    assert "regression and gap review only" in phase_doc
    assert "does not implement new runtime behavior" in phase_doc


def test_phase_31_2_records_no_runtime_file_changes() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["runtime_state_py_changed_in_phase_31"] is False
    assert fixture["kernel_init_changed_in_phase_31"] is False


def test_regression_coverage_reviewed_is_meaningful() -> None:
    coverage = set(_load_json(PHASE_FIXTURE_PATH)["regression_coverage_reviewed"])
    assert "deterministic_output" in coverage
    assert "missing_input_safe" in coverage
    assert "malformed_input_safe" in coverage
    assert "unknown_status_safe" in coverage
    assert "bypass_wording_resistance" in coverage
    assert "no_input_mutation" in coverage
    assert "non_authoritative_advisory_output" in coverage
    assert "non_execution_invariants" in coverage
    assert "dispatch_and_persistence_disallowed" in coverage
    assert "phase_5_runtime_bridge_gated" in coverage
    assert "sparkbot_absent" in coverage
    assert "live_adapter_absent" in coverage
    assert "forbidden_imports_and_calls_absent" in coverage


def test_remaining_gaps_are_non_blocking_and_gated() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    gaps = set(fixture["remaining_non_blocking_gaps"])
    assert fixture["blocking_safety_regression_found"] is False
    assert "additional_nested_suspicious_metadata_fixtures_could_harden_runtime_state_tests" in gaps
    assert "future_no_code_design_review_could_evaluate_second_advisory_field_family" in gaps
    assert "humaninput_bridge_planning_remains_separate_and_gated" in gaps
    assert "sparkbot_integration_boundary_planning_remains_separate_and_gated" in gaps
    assert "robo_os_physical_world_boundary_planning_remains_separate_and_gated" in gaps


def test_phase_32_implication_does_not_default_to_implementation() -> None:
    implication = _load_json(PHASE_FIXTURE_PATH)["phase_32_implication"]
    assert implication["default_to_runtime_implementation"] is False
    assert implication["recommended_direction"] == (
        "docs_tests_fixtures_only_design_review_for_next_narrow_runtime_slice"
    )
    assert implication["test_only_hardening_fallback_only_if_concrete_gap_found"] is True


def test_no_phase_31_2_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_31_2*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_31_2*"))
