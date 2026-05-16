"""Static checks for Phase 20.0 post-regression runtime slice design charter."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_20_0_POST_REGRESSION_RUNTIME_SLICE_DESIGN_CHARTER.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_20_0_post_regression_runtime_slice_design_charter.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_docs_tests_fixtures_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "20.0"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False


def test_phase_twenty_uses_phase_eighteen_and_nineteen_inputs() -> None:
    inputs = set(_load_json(PHASE_FIXTURE_PATH)["design_inputs"])
    assert "phase_18_candidate_api_regression_tests" in inputs
    assert "phase_18_acceptance_boundary_fixtures" in inputs
    assert "phase_18_forbidden_integration_regression_tests" in inputs
    assert "phase_19_regression_coverage_review" in inputs
    assert "phase_19_remaining_regression_gap_review" in inputs
    assert "phase_19_archive_closeout" in inputs


def test_all_candidate_slice_options_are_listed() -> None:
    options = set(_load_json(PHASE_FIXTURE_PATH)["candidate_slice_options"])
    assert options == {
        "candidate_provenance_hardening",
        "candidate_lifecycle_metadata",
        "replay_staleness_marker_normalization",
        "candidate_error_taxonomy",
        "pause_and_preserve",
        "sparkbot_integration_boundary_planning_instead_of_runtime_work",
    }


def test_required_design_outputs_are_declared() -> None:
    outputs = set(_load_json(PHASE_FIXTURE_PATH)["required_design_outputs"])
    assert "exact_future_file_touch_map" in outputs
    assert "future_acceptance_test_requirements" in outputs
    assert "rollback_and_audit_proof_requirements" in outputs
    assert "phase_21_decision_gate" in outputs


def test_phase_document_preserves_no_code_gate() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "does not implement runtime code" in phase_doc
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "Phase 20.0 does not approve Phase 21" in phase_doc
    assert "Phase 5 HumanInput runtime bridge remains gated" in phase_doc


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
    assert boundary["phase_21_approved"] is False


def test_no_phase_twenty_zero_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_20_0*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_20_0*"))
