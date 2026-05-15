"""Static checks for Phase 12.2 threat model and safety gap review."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_12_2_THREAT_MODEL_AND_SAFETY_GAP_REVIEW.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_12_2_threat_model_and_safety_gap_review.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_docs_tests_fixtures_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "12.2"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False


def test_threats_include_runtime_bridge_sparkbot_robo_and_bypass_risks() -> None:
    threats = set(_load_json(PHASE_FIXTURE_PATH)["threats_reviewed"])
    assert "candidate_status_mistaken_for_approval" in threats
    assert "candidate_validation_mistaken_for_guardian_decision" in threats
    assert "humaninput_runtime_bridge_pressure" in threats
    assert "sparkbot_boundary_planning_drifting_into_wiring" in threats
    assert "robo_os_planning_drifting_into_driver_behavior" in threats
    assert "operator_admin_phil_trusted_bypass" in threats
    assert "shell_browser_network_file_robotics_escalation" in threats


def test_safety_gaps_keep_phase_five_gate_and_runtime_expansion_blocked() -> None:
    gaps = set(_load_json(PHASE_FIXTURE_PATH)["safety_gaps"])
    assert "future_runtime_threat_model_test_plan_missing" in gaps
    assert "sparkbot_shell_boundary_not_threat_modeled" in gaps
    assert "robo_os_simulation_boundary_not_threat_modeled" in gaps
    assert "no_approved_runtime_expansion_beyond_candidate_status" in gaps
    assert "phase_5_humaninput_runtime_bridge_remains_gated" in gaps


def test_finding_leads_to_recommendation_matrix_not_implementation() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["finding"] == "produce_next_lane_recommendation_matrix_before_any_implementation"
    assert fixture["next_phase"] == "phase_12_3_next_lane_recommendation_matrix"


def test_phase_document_blocks_side_effects_and_runtime_expansion() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "docs/tests/fixtures only" in phase_doc
    assert "does not modify `lima/`" in phase_doc
    assert "does not wire Sparkbot" in phase_doc
    assert "does not add a HumanInput runtime bridge" in phase_doc
    assert "does not perform shell, browser, network, file mutation, robotics, or physical-world action" in phase_doc


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


def test_no_phase_twelve_two_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_12_2*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_12_2*"))
