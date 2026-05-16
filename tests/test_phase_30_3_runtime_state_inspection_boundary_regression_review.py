"""Runtime state inspection boundary regression review tests for Phase 30.3."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_30_3_RUNTIME_STATE_INSPECTION_BOUNDARY_REGRESSION_REVIEW.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_30_3_runtime_state_inspection_boundary_regression_review.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_30_3_is_regression_review_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "30.3"
    assert fixture["runtime_code_modified"] is False
    assert "regression review only" in phase_doc
    assert "does not implement new runtime behavior" in phase_doc


def test_review_confirms_only_approved_runtime_files() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["approved_runtime_files_reviewed"] == [
        "lima/kernel/runtime_state.py",
        "lima/kernel/__init__.py",
    ]
    assert fixture["forbidden_runtime_files_changed"] is False
    assert fixture["tests_support_changed"] is False


def test_boundary_remains_read_only_non_executing_and_safe() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["runtime_state_inspection_boundary"]
    assert boundary["deterministic"] is True
    assert boundary["local_only"] is True
    assert boundary["read_only"] is True
    assert boundary["non_authoritative"] is True
    assert boundary["non_executing"] is True
    assert boundary["side_effect_free"] is True
    assert boundary["safe_by_default_missing_or_malformed"] is True
    assert boundary["safe_by_default_unknown_values"] is True
    assert boundary["bypass_wording_resistant"] is True


def test_forbidden_behavior_remains_absent() -> None:
    absent = _load_json(PHASE_FIXTURE_PATH)["forbidden_behavior_absent"]
    assert absent["candidate_creation"] is True
    assert absent["candidate_mutation"] is True
    assert absent["humaninput_runtime_bridge"] is True
    assert absent["intent_envelope_creation"] is True
    assert absent["guardian_decision_creation"] is True
    assert absent["approval"] is True
    assert absent["execution"] is True
    assert absent["dispatch"] is True
    assert absent["audit_persistence"] is True
    assert absent["external_system_calls"] is True
    assert absent["sparkbot_wiring"] is True
    assert absent["background_work"] is True
    assert absent["physical_world_behavior"] is True


def test_regression_coverage_confirms_phase_30_2_acceptance_obligations() -> None:
    coverage = set(_load_json(PHASE_FIXTURE_PATH)["regression_coverage_confirmed"])
    assert "deterministic_output" in coverage
    assert "no_input_mutation" in coverage
    assert "missing_input_safe" in coverage
    assert "malformed_input_safe" in coverage
    assert "unknown_status_safe" in coverage
    assert "bypass_wording_safe" in coverage
    assert "execution_disallowed" in coverage
    assert "side_effects_disallowed" in coverage
    assert "approval_not_approved" in coverage
    assert "dispatch_disallowed" in coverage
    assert "persistence_disallowed" in coverage
    assert "phase_5_runtime_bridge_gated" in coverage
    assert "sparkbot_absent" in coverage
    assert "live_adapter_absent" in coverage
    assert "forbidden_imports_and_calls_absent" in coverage


def test_no_phase_30_3_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_30_3*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_30_3*"))
