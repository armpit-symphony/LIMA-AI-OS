"""Current runtime/test preservation record tests for Phase 27.1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_27_1_CURRENT_RUNTIME_TEST_STATE_PRESERVATION_RECORD.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_27_1_current_runtime_test_state_preservation_record.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_27_1_is_preservation_record_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "27.1"
    assert fixture["runtime_code_modified"] is False
    assert "preservation record only" in phase_doc
    assert "does not implement runtime behavior" in phase_doc


def test_preserved_runtime_state_keeps_candidate_slice_constrained() -> None:
    state = _load_json(PHASE_FIXTURE_PATH)["preserved_runtime_state"]
    assert state["pure_in_process"] is True
    assert state["non_executing"] is True
    assert state["side_effect_free"] is True
    assert state["approval_free"] is True
    assert state["dispatch_free"] is True
    assert state["persistence_free"] is True
    assert state["authority_free"] is True
    assert state["execution_allowed_always_false"] is True
    assert state["side_effects_allowed_always_false"] is True
    assert state["approval_state_never_approved"] is True
    assert state["phase_5_runtime_bridge_remains_gated"] is True


def test_preserved_test_state_lists_existing_guardrails() -> None:
    tests = set(_load_json(PHASE_FIXTURE_PATH)["preserved_test_state"])
    assert "phase_16_acceptance_gate_tests" in tests
    assert "phase_18_regression_hardening" in tests
    assert "phase_23_provenance_hardening_tests" in tests
    assert "phase_25_cross_api_invariant_matrix_tests" in tests
    assert "phase_26_archive_checks" in tests


def test_pause_rationale_requires_fresh_phil_decision_for_expansion() -> None:
    rationale = set(_load_json(PHASE_FIXTURE_PATH)["pause_rationale"])
    assert "current_runtime_test_state_is_known_good" in rationale
    assert "runtime_expansion_requires_fresh_phil_decision" in rationale
    assert "sparkbot_robo_live_adapter_and_physical_world_lanes_remain_gated" in rationale
    assert "fresh explicit Phil decision" in PHASE_DOC_PATH.read_text(encoding="utf-8")


def test_boundary_results_show_no_runtime_or_support_change() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False


def test_no_phase_27_1_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_27_1*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_27_1*"))
