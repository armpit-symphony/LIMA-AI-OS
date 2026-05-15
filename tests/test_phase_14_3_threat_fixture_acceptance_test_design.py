"""Static checks for Phase 14.3 threat fixture acceptance test design."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_14_3_THREAT_FIXTURE_ACCEPTANCE_TEST_DESIGN.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_14_3_threat_fixture_acceptance_test_design.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_design_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "14.3"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False
    assert fixture["boundary_results"]["fixture_execution_code_added"] is False


def test_fixture_acceptance_test_names_are_concrete() -> None:
    names = {entry["name"] for entry in _load_json(PHASE_FIXTURE_PATH)["future_fixture_acceptance_tests"]}
    assert names == {
        "test_malformed_candidate_fixture_is_safe",
        "test_unknown_status_fixture_is_safe",
        "test_stale_candidate_fixture_is_blocked_or_invalid",
        "test_replayed_candidate_fixture_is_blocked_or_invalid",
        "test_approval_bypass_wording_fixture_does_not_authorize",
        "test_shell_command_attempt_fixture_is_non_executing",
        "test_browser_or_network_attempt_fixture_is_non_executing",
        "test_file_mutation_attempt_fixture_is_non_mutating",
        "test_robotics_or_physical_world_attempt_fixture_is_blocked",
        "test_sparkbot_integration_attempt_fixture_is_reference_only",
        "test_humaninput_bridge_attempt_fixture_is_gated",
    }


def test_fixture_families_cover_phase_thirteen_threats() -> None:
    families = {entry["fixture_family"] for entry in _load_json(PHASE_FIXTURE_PATH)["future_fixture_acceptance_tests"]}
    assert {
        "malformed_candidate",
        "unknown_status",
        "stale_candidate",
        "replayed_candidate",
        "approval_bypass_wording",
        "shell_command_attempt",
        "browser_or_network_attempt",
        "file_mutation_attempt",
        "robotics_or_physical_world_attempt",
        "sparkbot_integration_attempt",
        "humaninput_bridge_attempt",
    } <= families


def test_fixture_rules_keep_examples_synthetic_and_inert() -> None:
    rules = _load_json(PHASE_FIXTURE_PATH)["fixture_rules"]
    assert rules["synthetic"] is True
    assert rules["inert"] is True
    assert rules["non_runtime"] is True
    assert rules["no_live_shell_commands_for_execution"] is True
    assert rules["no_live_network_targets"] is True
    assert rules["no_private_operational_data"] is True
    assert rules["no_credentials"] is True
    assert rules["no_robot_instructions"] is True
    assert rules["no_approval_dispatch_or_persistence_implication"] is True


def test_phase_document_blocks_fixture_execution_implementation() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "does not add fixture-execution code" in phase_doc
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "All future fixtures must be synthetic, inert, and non-runtime" in phase_doc


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["fixture_execution_code_added"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["humaninput_runtime_bridge_added"] is False
    assert boundary["live_adapter_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True


def test_no_phase_fourteen_three_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_14_3*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_14_3*"))
