"""Static checks for Phase 14.4 future runtime acceptance gate closeout."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_14_4_FUTURE_RUNTIME_ACCEPTANCE_GATE_CLOSEOUT.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_14_4_future_runtime_acceptance_gate_closeout.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_closeout_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "14.4"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False
    assert fixture["boundary_results"]["acceptance_gate_tests_implemented"] is False


def test_completed_phase_fourteen_scope_is_listed() -> None:
    completed = set(_load_json(PHASE_FIXTURE_PATH)["completed_phase_14_scope"])
    assert completed == {
        "phase_14_0_acceptance_gate_test_design_charter",
        "phase_14_1_static_forbidden_pattern_test_design",
        "phase_14_2_runtime_contract_test_design",
        "phase_14_3_threat_fixture_acceptance_test_design",
    }


def test_future_acceptance_gate_requirements_cover_static_contract_and_fixture_rules() -> None:
    requirements = set(_load_json(PHASE_FIXTURE_PATH)["future_acceptance_gate_requirements"])
    assert "execution_allowed_false" in requirements
    assert "side_effects_allowed_false" in requirements
    assert "approval_state_never_approved" in requirements
    assert "provenance_preserved" in requirements
    assert "malformed_unknown_stale_replayed_safe" in requirements
    assert "operator_admin_phil_trusted_wording_does_not_bypass_safety" in requirements
    assert "fixtures_synthetic_inert_non_runtime_side_effect_free" in requirements
    assert "phase_5_humaninput_runtime_bridge_remains_gated" in requirements


def test_phase_fifteen_remains_gated() -> None:
    gate = _load_json(PHASE_FIXTURE_PATH)["phase_15_gate"]
    assert gate["phase_15_approved"] is False
    assert gate["recommended_direction"] == "docs_tests_fixtures_only_acceptance_gate_implementation_proposal_or_readiness_lane"
    assert "Do you approve Phase 15" in gate["approval_question"]
    assert "runtime implementation" in gate["approval_question"]
    assert "lima/ changes" in gate["approval_question"]
    assert "physical-world action" in gate["approval_question"]


def test_phase_document_blocks_runtime_and_acceptance_gate_implementation() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "does not implement acceptance-gate tests" in phase_doc
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "Phase 15 is not approved by this closeout" in phase_doc


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["acceptance_gate_tests_implemented"] is False
    assert boundary["candidate_status_expanded"] is False
    assert boundary["intake_candidate_expanded"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["humaninput_runtime_bridge_added"] is False
    assert boundary["live_adapter_added"] is False
    assert boundary["intentcompiler_runtime_changed"] is False
    assert boundary["guardiandecision_runtime_changed"] is False
    assert boundary["approval_enforcement_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True


def test_no_phase_fourteen_four_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_14_4*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_14_4*"))
