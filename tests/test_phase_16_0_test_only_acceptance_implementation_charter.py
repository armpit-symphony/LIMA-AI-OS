"""Static checks for Phase 16.0 test-only acceptance implementation charter."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_16_0_TEST_ONLY_ACCEPTANCE_IMPLEMENTATION_CHARTER.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_16_0_test_only_acceptance_implementation_charter.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_test_only_charter() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "16.0"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False


def test_phase_fifteen_inputs_are_listed() -> None:
    inputs = set(_load_json(PHASE_FIXTURE_PATH)["phase_15_inputs"])
    assert inputs == {
        "phase_15_1_future_static_test_implementation_plan",
        "phase_15_2_future_runtime_contract_test_implementation_plan",
        "phase_15_3_future_threat_fixture_test_implementation_plan",
        "phase_15_4_test_only_implementation_readiness_gate_closeout",
    }


def test_approved_groups_match_phase_sixteen_lane() -> None:
    groups = set(_load_json(PHASE_FIXTURE_PATH)["approved_phase_16_implementation_groups"])
    assert groups == {
        "static_forbidden_pattern_acceptance_tests",
        "runtime_contract_acceptance_tests",
        "synthetic_threat_fixture_acceptance_tests",
        "test_only_implementation_readiness_review",
        "phase_16_archive_closeout",
    }


def test_allowed_behaviors_are_test_only() -> None:
    allowed = _load_json(PHASE_FIXTURE_PATH)["allowed_test_behaviors"]
    assert allowed["inspect_existing_runtime_source_text"] is True
    assert allowed["exercise_existing_non_executing_candidate_apis"] is True
    assert allowed["use_synthetic_phase_16_fixtures"] is True


def test_blocked_behaviors_prevent_side_effects() -> None:
    blocked = _load_json(PHASE_FIXTURE_PATH)["blocked_test_behaviors"]
    assert blocked["runtime_file_mutation"] is True
    assert blocked["tests_support_changes"] is True
    assert blocked["reusable_scanner_helper_added"] is True
    assert blocked["external_service_calls"] is True
    assert blocked["command_execution"] is True
    assert blocked["dispatch"] is True
    assert blocked["audit_persistence"] is True
    assert blocked["live_integration_path_creation"] is True


def test_phase_document_preserves_forbidden_scope() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "does not change runtime behavior" in phase_doc
    assert "does not wire Sparkbot" in phase_doc
    assert "does not execute" in phase_doc


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["helper_behavior_changed"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["humaninput_runtime_bridge_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True


def test_no_phase_sixteen_zero_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_16_0*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_16_0*"))
