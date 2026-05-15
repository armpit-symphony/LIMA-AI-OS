"""Static checks for Phase 15.3 future threat fixture test implementation plan."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_15_3_FUTURE_THREAT_FIXTURE_TEST_IMPLEMENTATION_PLAN.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_15_3_future_threat_fixture_test_implementation_plan.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_plan_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "15.3"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False
    assert fixture["actual_future_threat_fixture_tests_implemented"] is False
    assert fixture["actual_future_threat_fixtures_added"] is False


def test_future_threat_fixture_test_file_is_named_but_not_created() -> None:
    future_files = _load_json(PHASE_FIXTURE_PATH)["proposed_future_test_files"]
    assert future_files == ["tests/test_acceptance_threat_fixtures.py"]
    assert not (REPO_ROOT / "tests" / "test_acceptance_threat_fixtures.py").exists()


def test_future_fixture_files_are_named_but_not_created() -> None:
    future_files = _load_json(PHASE_FIXTURE_PATH)["proposed_future_fixture_files"]
    assert len(future_files) == 11
    for future_file in future_files:
        assert future_file.startswith("tests/fixtures/runtime_extraction/acceptance_")
        assert not (REPO_ROOT / future_file).exists()


def test_future_threat_fixture_tests_cover_all_threat_families() -> None:
    names = set(_load_json(PHASE_FIXTURE_PATH)["proposed_future_threat_fixture_tests"])
    assert names == {
        "test_malformed_candidate_fixture_remains_invalid_or_blocked",
        "test_unknown_status_fixture_remains_invalid_blocked_or_needs_review",
        "test_stale_candidate_fixture_remains_non_executable",
        "test_replayed_candidate_fixture_remains_non_executable",
        "test_approval_bypass_wording_fixture_does_not_authorize",
        "test_shell_command_attempt_fixture_remains_non_executing",
        "test_browser_network_attempt_fixture_remains_non_executing",
        "test_file_mutation_attempt_fixture_remains_non_mutating",
        "test_robotics_physical_world_attempt_fixture_remains_blocked",
        "test_sparkbot_integration_attempt_fixture_remains_unwired",
        "test_humaninput_bridge_attempt_fixture_remains_gated",
    }


def test_future_fixture_content_requirements_keep_fixtures_safe() -> None:
    requirements = _load_json(PHASE_FIXTURE_PATH)["future_fixture_content_requirements"]
    assert requirements["synthetic"] is True
    assert requirements["inert"] is True
    assert requirements["non_runtime"] is True
    assert requirements["side_effect_free"] is True
    assert requirements["no_credentials"] is True
    assert requirements["no_private_hostnames"] is True
    assert requirements["no_deploy_configs"] is True
    assert requirements["no_live_shell_commands_for_execution"] is True
    assert requirements["no_live_network_targets"] is True
    assert requirements["no_real_file_mutation_targets"] is True
    assert requirements["no_robot_or_device_actuation_instructions"] is True
    assert requirements["not_authorization"] is True


def test_phase_document_blocks_threat_fixture_implementation() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "without implementing it" in phase_doc
    assert "does not implement actual future threat fixture tests" in phase_doc
    assert "does not add the future threat fixtures" in phase_doc
    assert "These files are proposed for a later explicitly approved phase only" in phase_doc


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["actual_future_threat_fixture_tests_implemented"] is False
    assert boundary["actual_future_threat_fixtures_added"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["humaninput_runtime_bridge_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True


def test_no_phase_fifteen_three_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_15_3*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_15_3*"))
