"""Static checks for Phase 13.0 threat-derived test planning charter."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_13_0_THREAT_DERIVED_TEST_PLANNING_CHARTER.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_13_0_threat_derived_test_planning_charter.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_docs_tests_fixtures_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "13.0"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False


def test_charter_converts_phase_twelve_two_threats() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["source_phase"] == "12.2"
    threats = set(fixture["source_threats"])
    assert "candidate_status_mistaken_for_approval" in threats
    assert "humaninput_runtime_bridge_pressure" in threats
    assert "sparkbot_boundary_planning_drifting_into_wiring" in threats
    assert "robo_os_planning_drifting_into_driver_behavior" in threats
    assert "operator_admin_phil_trusted_bypass" in threats
    assert "shell_browser_network_file_robotics_escalation" in threats


def test_planning_outputs_match_phase_thirteen_lane() -> None:
    outputs = set(_load_json(PHASE_FIXTURE_PATH)["planning_outputs"])
    assert outputs == {
        "static_forbidden_pattern_test_requirements",
        "runtime_contract_test_requirements",
        "threat_fixture_matrix",
        "future_acceptance_gate_closeout",
    }


def test_phase_document_blocks_runtime_and_integration_work() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "docs/tests/fixtures-only threat-model-derived test planning lane" in phase_doc
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "does not wire Sparkbot" in phase_doc
    assert "does not execute" in phase_doc
    assert "does not dispatch" in phase_doc


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["candidate_status_expanded"] is False
    assert boundary["intake_candidate_expanded"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["humaninput_runtime_bridge_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True


def test_no_phase_thirteen_zero_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_13_0*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_13_0*"))
