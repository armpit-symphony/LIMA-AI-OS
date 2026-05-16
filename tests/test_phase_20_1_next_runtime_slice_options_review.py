"""Static checks for Phase 20.1 next runtime slice options review."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_20_1_NEXT_RUNTIME_SLICE_OPTIONS_REVIEW.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_20_1_next_runtime_slice_options_review.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_docs_tests_fixtures_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "20.1"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False


def test_all_options_are_reviewed() -> None:
    options = _load_json(PHASE_FIXTURE_PATH)["options_reviewed"]
    assert set(options) == {
        "candidate_provenance_hardening",
        "candidate_lifecycle_metadata",
        "replay_staleness_marker_normalization",
        "candidate_error_taxonomy",
        "pause_and_preserve",
        "sparkbot_integration_boundary_planning_instead_of_runtime_work",
    }


def test_exactly_one_runtime_slice_is_recommended() -> None:
    options = _load_json(PHASE_FIXTURE_PATH)["options_reviewed"]
    recommended = [option for option, decision in options.items() if decision == "recommended"]
    assert recommended == ["candidate_provenance_hardening"]


def test_recommended_slice_constraints_preserve_boundaries() -> None:
    constraints = set(_load_json(PHASE_FIXTURE_PATH)["recommended_slice_constraints"])
    assert "normalize_and_validate_provenance_metadata_only" in constraints
    assert "operate_only_on_existing_non_executing_candidates" in constraints
    assert "no_humaninput_runtime_bridge" in constraints
    assert "no_sparkbot_wiring" in constraints
    assert "no_execution" in constraints
    assert "no_dispatch" in constraints
    assert "no_audit_persistence" in constraints
    assert "no_external_side_effects" in constraints


def test_phase_document_does_not_approve_phase_twenty_one() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "recommends exactly one future runtime slice without implementing it" in phase_doc
    assert "Phase 20.1 does not approve Phase 21" in phase_doc
    assert "must not create a HumanInput runtime bridge" in phase_doc


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["humaninput_runtime_bridge_added"] is False
    assert boundary["live_adapter_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True


def test_no_phase_twenty_one_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_20_1*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_20_1*"))
