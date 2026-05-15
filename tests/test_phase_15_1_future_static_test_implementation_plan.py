"""Static checks for Phase 15.1 future static test implementation plan."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_15_1_FUTURE_STATIC_TEST_IMPLEMENTATION_PLAN.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_15_1_future_static_test_implementation_plan.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_plan_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "15.1"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False
    assert fixture["actual_future_static_tests_implemented"] is False
    assert fixture["scanner_utilities_added"] is False


def test_future_static_test_file_is_named_but_not_created() -> None:
    future_files = _load_json(PHASE_FIXTURE_PATH)["proposed_future_test_files"]
    assert future_files == ["tests/test_acceptance_static_forbidden_patterns.py"]
    assert not (REPO_ROOT / "tests" / "test_acceptance_static_forbidden_patterns.py").exists()


def test_future_static_tests_cover_forbidden_patterns() -> None:
    names = {entry["name"] for entry in _load_json(PHASE_FIXTURE_PATH)["proposed_future_static_tests"]}
    assert names == {
        "test_runtime_files_have_no_sparkbot_imports",
        "test_runtime_files_have_no_live_adapter_imports",
        "test_runtime_files_have_no_humaninput_bridge_imports",
        "test_runtime_files_have_no_execution_or_dispatch_calls",
        "test_runtime_files_have_no_approval_or_audit_persistence_calls",
        "test_runtime_files_have_no_authority_claims",
    }


def test_future_scanner_constraints_block_runtime_or_side_effects() -> None:
    constraints = _load_json(PHASE_FIXTURE_PATH)["future_scanner_constraints"]
    assert constraints["stdlib_only"] is True
    assert constraints["explicit_file_set_only"] is True
    assert constraints["production_scanner_not_allowed"] is True
    assert constraints["runtime_import_execution_not_allowed"] is True
    assert constraints["subprocess_not_allowed"] is True
    assert constraints["network_not_allowed"] is True
    assert constraints["filesystem_mutation_not_allowed"] is True


def test_phase_document_blocks_static_test_implementation() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "without implementing it" in phase_doc
    assert "does not implement actual future static acceptance tests" in phase_doc
    assert "does not add scanner utilities" in phase_doc
    assert "This file is proposed for a later explicitly approved phase only" in phase_doc


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["actual_future_static_tests_implemented"] is False
    assert boundary["scanner_utilities_added"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["humaninput_runtime_bridge_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True


def test_no_phase_fifteen_one_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_15_1*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_15_1*"))
