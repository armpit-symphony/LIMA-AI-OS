"""Narrow runtime slice candidate inventory tests for Phase 29.1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_29_1_NARROW_RUNTIME_SLICE_CANDIDATE_INVENTORY.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_29_1_narrow_runtime_slice_candidate_inventory.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_29_1_is_candidate_inventory_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "29.1"
    assert fixture["runtime_code_modified"] is False
    assert "candidate inventory only" in phase_doc
    assert "does not implement runtime behavior" in phase_doc


def test_all_future_slice_options_are_reviewed() -> None:
    options = _load_json(PHASE_FIXTURE_PATH)["options_reviewed"]
    assert options["A"] == "read_only_runtime_state_inspection_slice"
    assert options["B"] == "non_executing_humaninput_to_intentenvelope_candidate_construction_slice"
    assert options["C"] == "candidate_status_normalization_slice_only"
    assert options["D"] == "guardiandecision_read_only_preview_slice"
    assert options["E"] == "continue_docs_tests_only_hardening_if_no_slice_safe"
    assert options["F"] == "pause_and_preserve_if_no_slice_meets_eligibility"


def test_read_only_runtime_state_inspection_is_recommended() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["recommended_option"] == "A"
    assert fixture["recommended_future_slice"] == "read_only_runtime_state_inspection_slice"
    assert "Phase 29 recommends Option A" in PHASE_DOC_PATH.read_text(encoding="utf-8")


def test_recommendation_rationale_preserves_non_executing_boundary() -> None:
    rationale = set(_load_json(PHASE_FIXTURE_PATH)["recommendation_rationale"])
    assert "deterministic_local_only_inspectable_output" in rationale
    assert "no_humaninput_bridge" in rationale
    assert "no_guardiandecision_runtime_behavior" in rationale
    assert "no_status_semantics_expansion" in rationale
    assert "no_dispatch" in rationale
    assert "no_persistence_writes" in rationale
    assert "no_external_side_effects" in rationale


def test_rejected_options_have_clear_reasons() -> None:
    rejected = _load_json(PHASE_FIXTURE_PATH)["rejected_options"]
    assert rejected["B"] == "phase_5_humaninput_runtime_bridge_remains_gated"
    assert rejected["C"] == "candidate_status_normalization_already_exists_no_immediate_expansion_need"
    assert rejected["D"] == "guardiandecision_runtime_behavior_remains_blocked"
    assert rejected["E"] == "no_concrete_immediate_test_only_gap_found"
    assert rejected["F"] == "no_specific_documented_risk_requires_another_pause"


def test_next_phase_is_safety_boundary_design() -> None:
    assert _load_json(PHASE_FIXTURE_PATH)["next_phase"] == "29.2"
    assert "Continue only to Phase 29.2" in PHASE_DOC_PATH.read_text(encoding="utf-8")


def test_no_phase_29_1_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_29_1*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_29_1*"))
