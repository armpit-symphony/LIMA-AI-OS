"""Gated runtime boundary review tests for Phase 27.2."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_27_2_GATED_RUNTIME_BOUNDARY_REVIEW.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_27_2_gated_runtime_boundary_review.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_27_2_is_boundary_review_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "27.2"
    assert fixture["runtime_code_modified"] is False
    assert "boundary review only" in phase_doc
    assert "does not implement runtime behavior" in phase_doc


def test_runtime_boundary_remains_non_executing() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["runtime_boundary"]
    assert boundary["candidate_construction_non_executing"] is True
    assert boundary["status_normalization_non_executing"] is True
    assert boundary["candidate_validation_non_executing"] is True
    assert boundary["provenance_hardening_non_executing"] is True
    assert boundary["approval_absent"] is True
    assert boundary["execution_absent"] is True
    assert boundary["dispatch_absent"] is True
    assert boundary["persistence_absent"] is True
    assert boundary["external_system_calls_absent"] is True


def test_integration_boundary_remains_gated() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["integration_boundary"]
    assert boundary["sparkbot_integration_absent"] is True
    assert boundary["humaninput_runtime_bridge_absent_and_gated"] is True
    assert boundary["live_adapters_absent"] is True
    assert boundary["robo_os_physical_world_behavior_absent"] is True
    assert boundary["intentcompiler_runtime_behavior_unchanged"] is True
    assert boundary["guardiandecision_runtime_behavior_unchanged"] is True


def test_operational_boundary_has_no_background_or_hidden_side_effects() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["operational_boundary"]
    assert boundary["background_workers_absent"] is True
    assert boundary["queues_absent"] is True
    assert boundary["daemons_absent"] is True
    assert boundary["subprocesses_absent"] is True
    assert boundary["threads_absent"] is True
    assert boundary["database_writes_absent"] is True
    assert boundary["hidden_side_effects_absent"] is True


def test_next_phase_is_risk_decision_matrix() -> None:
    assert _load_json(PHASE_FIXTURE_PATH)["next_phase"] == "27.3"
    assert "Continue only to Phase 27.3" in PHASE_DOC_PATH.read_text(encoding="utf-8")


def test_no_phase_27_2_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_27_2*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_27_2*"))
