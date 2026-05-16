"""Candidate runtime slice inventory tests for Phase 32.1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_32_1_CANDIDATE_RUNTIME_SLICE_INVENTORY.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_32_1_candidate_runtime_slice_inventory.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_32_1_remains_docs_tests_fixtures_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "32.1"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_implementation_approved"] is False
    assert fixture["lima_changes_allowed"] is False
    assert fixture["tests_support_changes_allowed"] is False
    assert "does not approve Phase 33 implementation" in phase_doc


def test_phase_32_1_reviews_all_requested_candidate_options() -> None:
    options = set(_load_json(PHASE_FIXTURE_PATH)["candidate_options_reviewed"])
    assert options == {
        "runtime_state_test_only_hardening",
        "second_read_only_runtime_inspection_slice",
        "non_executing_candidate_preview_helper",
        "candidate_status_read_only_normalization_hardening",
        "humaninput_bridge_boundary_planning_only",
        "sparkbot_integration_boundary_planning_only",
        "pause_and_preserve_state",
    }


def test_phase_32_1_recommends_test_only_phase_33() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["recommended_phase_33_direction"] == "runtime_state_test_only_hardening"
    assert fixture["recommended_phase_33_is_runtime_implementation"] is False
    assert "tests/test_phase_33_*.py" in fixture["recommended_phase_33_allowed_paths"]
    assert "docs/PHASE_33_*.md" in fixture["recommended_phase_33_allowed_paths"]


def test_phase_32_1_forbids_runtime_and_integration_expansion() -> None:
    forbidden = _load_json(PHASE_FIXTURE_PATH)["recommended_phase_33_forbidden"]
    assert forbidden["lima_changes"] is True
    assert forbidden["tests_support_changes"] is True
    assert forbidden["runtime_implementation"] is True
    assert forbidden["sparkbot_wiring"] is True
    assert forbidden["humaninput_runtime_bridge"] is True
    assert forbidden["live_adapter"] is True
    assert forbidden["approval_execution_dispatch_persistence"] is True
    assert forbidden["shell_browser_network_file_robotics_physical_world"] is True
    assert forbidden["external_service_calls"] is True
    assert (
        forbidden[
            "background_workers_queues_daemons_subprocesses_threads_database_writes_hidden_side_effects"
        ]
        is True
    )


def test_no_phase_32_1_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_32_1*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_32_1*"))
