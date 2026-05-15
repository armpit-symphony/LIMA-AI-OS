"""Static checks for Phase 15.0 acceptance-gate implementation proposal charter."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_15_0_ACCEPTANCE_GATE_IMPLEMENTATION_PROPOSAL_CHARTER.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_15_0_acceptance_gate_implementation_proposal_charter.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_proposal_charter_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "15.0"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False
    assert fixture["actual_future_acceptance_tests_implemented"] is False


def test_phase_fourteen_inputs_are_listed() -> None:
    inputs = set(_load_json(PHASE_FIXTURE_PATH)["phase_14_inputs"])
    assert inputs == {
        "phase_14_0_acceptance_gate_test_design_charter",
        "phase_14_1_static_forbidden_pattern_test_design",
        "phase_14_2_runtime_contract_test_design",
        "phase_14_3_threat_fixture_acceptance_test_design",
        "phase_14_4_future_runtime_acceptance_gate_closeout",
    }


def test_allowed_outputs_are_future_proposal_metadata() -> None:
    outputs = set(_load_json(PHASE_FIXTURE_PATH)["phase_15_allowed_outputs"])
    assert "future_static_forbidden_pattern_test_files_and_names" in outputs
    assert "future_runtime_contract_test_files_and_names" in outputs
    assert "future_threat_fixture_test_files_and_names" in outputs
    assert "future_regression_boundary_test_files_and_names" in outputs
    assert "future_no_sparkbot_no_humaninput_bridge_test_files_and_names" in outputs
    assert "future_fixture_names_and_content_requirements" in outputs


def test_proposal_readiness_is_not_implementation_approval() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["proposal_readiness_meaning"] == "ready_to_request_later_explicit_test_only_implementation_approval"
    not_ready = set(fixture["proposal_readiness_does_not_mean"])
    assert "future_acceptance_tests_implemented_now" in not_ready
    assert "runtime_work_approved" in not_ready
    assert "lima_changes_approved" in not_ready
    assert "tests_support_changes_approved" in not_ready
    assert "execution_dispatch_persistence_or_physical_world_action_approved" in not_ready


def test_phase_document_blocks_actual_acceptance_test_implementation() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "It does not implement the future acceptance tests" in phase_doc
    assert "does not implement actual future acceptance tests" in phase_doc
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["actual_future_acceptance_tests_implemented"] is False
    assert boundary["candidate_status_expanded"] is False
    assert boundary["intake_candidate_expanded"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["humaninput_runtime_bridge_added"] is False
    assert boundary["live_adapter_added"] is False
    assert boundary["approval_enforcement_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True


def test_no_phase_fifteen_zero_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_15_0*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_15_0*"))
