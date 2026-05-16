"""Static checks for Phase 19.0 regression hardening audit charter."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_19_0_PHASE_18_REGRESSION_HARDENING_AUDIT_CHARTER.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_19_0_phase_18_regression_hardening_audit_charter.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_docs_tests_fixtures_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "19.0"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False


def test_phase_eighteen_audit_scope_is_complete() -> None:
    scope = set(_load_json(PHASE_FIXTURE_PATH)["audit_scope"])
    assert scope == {
        "phase_18_0_regression_hardening_charter",
        "phase_18_1_candidate_api_regression_tests",
        "phase_18_2_acceptance_boundary_regression_fixtures",
        "phase_18_3_forbidden_integration_regression_tests",
        "phase_18_4_regression_hardening_readiness_review",
        "phase_18_5_phase_18_regression_hardening_archive_closeout",
    }


def test_phase_twenty_options_are_listed() -> None:
    options = set(_load_json(PHASE_FIXTURE_PATH)["phase_20_options"])
    assert "no_code_design_lane_for_next_narrow_runtime_slice" in options
    assert "additional_test_only_regression_hardening" in options
    assert "sparkbot_integration_boundary_planning" in options
    assert "robo_os_physical_world_boundary_planning" in options
    assert "pause_and_preserve_current_runtime_test_state" in options


def test_phase_document_preserves_boundaries_and_gate() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "without modifying `lima/`" in phase_doc
    assert "without modifying `tests/support/`" in phase_doc
    assert "without changing runtime behavior" in phase_doc
    assert "without wiring Sparkbot" in phase_doc
    assert "without adding a HumanInput runtime bridge" in phase_doc
    assert "Phase 19.0 does not approve Phase 20" in phase_doc


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["humaninput_runtime_bridge_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True
    assert boundary["phase_20_approved"] is False


def test_no_phase_nineteen_zero_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_19_0*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_19_0*"))
