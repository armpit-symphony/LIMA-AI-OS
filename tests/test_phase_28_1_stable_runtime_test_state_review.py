"""Stable runtime/test state review tests for Phase 28.1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_28_1_STABLE_RUNTIME_TEST_STATE_REVIEW.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_28_1_stable_runtime_test_state_review.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_28_1_is_stable_state_review_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "28.1"
    assert fixture["runtime_code_modified"] is False
    assert "stable-state review only" in phase_doc
    assert "does not implement runtime behavior" in phase_doc


def test_stable_runtime_state_preserves_candidate_boundaries() -> None:
    state = _load_json(PHASE_FIXTURE_PATH)["stable_runtime_state"]
    assert state["candidate_construction_non_executing"] is True
    assert state["status_normalization_non_executing"] is True
    assert state["candidate_validation_non_executing"] is True
    assert state["provenance_hardening_non_executing"] is True
    assert state["phase_27_runtime_files_changed"] is False
    assert state["phase_28_1_runtime_files_changed"] is False
    assert state["tests_support_changed"] is False
    assert state["runtime_behavior_changed"] is False
    assert state["phase_5_runtime_bridge_remains_gated"] is True


def test_stable_test_state_finds_no_immediate_test_hardening_gap() -> None:
    state = _load_json(PHASE_FIXTURE_PATH)["stable_test_state"]
    assert state["deterministic_offline_tests_preserved"] is True
    assert state["phase_26_archive_checks_preserved"] is True
    assert state["phase_27_preservation_checks_preserved"] is True
    assert state["phase_28_status_review_checks_started"] is True
    assert state["concrete_phase_29_test_hardening_gap_found"] is False
    assert "does not reveal a concrete tests-only gap" in PHASE_DOC_PATH.read_text(
        encoding="utf-8"
    )


def test_boundary_confirmation_keeps_forbidden_behaviors_absent() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_confirmation"]
    assert boundary["sparkbot_wiring_absent"] is True
    assert boundary["robo_os_wiring_absent"] is True
    assert boundary["humaninput_runtime_bridge_absent"] is True
    assert boundary["live_adapter_absent"] is True
    assert boundary["approval_enforcement_absent"] is True
    assert boundary["execution_absent"] is True
    assert boundary["dispatch_absent"] is True
    assert boundary["audit_persistence_absent"] is True
    assert boundary["physical_world_behavior_absent"] is True
    assert boundary["hidden_side_effects_absent"] is True


def test_next_phase_is_pause_justification_review() -> None:
    assert _load_json(PHASE_FIXTURE_PATH)["next_phase"] == "28.2"
    assert "Continue only to Phase 28.2" in PHASE_DOC_PATH.read_text(encoding="utf-8")


def test_no_phase_28_1_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_28_1*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_28_1*"))
