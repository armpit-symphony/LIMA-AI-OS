"""Static checks for Phase 14.1 static forbidden-pattern test design."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_14_1_STATIC_FORBIDDEN_PATTERN_TEST_DESIGN.md"
PHASE_FIXTURE_PATH = REPO_ROOT / "tests" / "fixtures" / "runtime_extraction" / "phase_14_1_static_forbidden_pattern_test_design.json"


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_design_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "14.1"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False
    assert fixture["static_scanner_implementation_added"] is False


def test_future_test_names_are_concrete() -> None:
    names = {entry["name"] for entry in _load_json(PHASE_FIXTURE_PATH)["future_test_designs"]}
    assert names == {
        "test_runtime_slice_has_no_forbidden_imports",
        "test_runtime_slice_has_no_forbidden_side_effect_calls",
        "test_runtime_slice_has_no_forbidden_boundary_names",
        "test_runtime_slice_has_no_authority_claims",
    }


def test_expected_assertions_cover_forbidden_static_patterns() -> None:
    assertions = " ".join(entry["expected_assertion"] for entry in _load_json(PHASE_FIXTURE_PATH)["future_test_designs"])
    assert "sparkbot" in assertions
    assert "live_adapter" in assertions
    assert "dispatch" in assertions
    assert "persistence" in assertions
    assert "humaninput_bridge" in assertions
    assert "guardiandecision" in assertions


def test_phase_document_blocks_scanner_or_runtime_implementation() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "does not add static scanner implementation" in phase_doc
    assert "must not import Sparkbot" in phase_doc
    assert "mutate files" in phase_doc
    assert "execute tools" in phase_doc


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["static_scanner_added"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["humaninput_runtime_bridge_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False


def test_no_phase_fourteen_one_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_14_1*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_14_1*"))
