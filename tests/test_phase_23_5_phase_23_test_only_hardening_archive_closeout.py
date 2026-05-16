"""Archive closeout tests for Phase 23.5."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_23_5_PHASE_23_TEST_ONLY_HARDENING_ARCHIVE_CLOSEOUT.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_23_5_phase_23_test_only_hardening_archive_closeout.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_23_5_is_archive_closeout_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "23.5"
    assert fixture["runtime_code_modified"] is False
    assert "docs/tests/fixtures-only archive closeout" in phase_doc
    assert "does not implement runtime behavior" in phase_doc


def test_phase_23_0_through_23_4_are_archived() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["archived_phases"] == ["23.0", "23.1", "23.2", "23.3", "23.4"]
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    for phase in fixture["archived_phases"]:
        assert f"Phase {phase}" in phase_doc


def test_phase_23_added_only_docs_fixtures_tests_and_metadata() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase_23_added"] == [
        "docs",
        "synthetic_fixtures",
        "test_only_acceptance_and_regression_coverage",
        "roadmap_state_decision_metadata",
    ]


def test_phase_23_did_not_add_forbidden_runtime_or_integration_behavior() -> None:
    not_added = set(_load_json(PHASE_FIXTURE_PATH)["phase_23_not_added"])
    assert "runtime_behavior" in not_added
    assert "lima_changes" in not_added
    assert "tests_support_changes" in not_added
    assert "sparkbot_wiring" in not_added
    assert "humaninput_runtime_bridge" in not_added
    assert "live_adapter" in not_added
    assert "approval_enforcement" in not_added
    assert "execution" in not_added
    assert "dispatch" in not_added
    assert "audit_persistence" in not_added
    assert "physical_world_behavior" in not_added


def test_boundary_results_show_phase_5_gated_and_phase_24_requires_approval() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["humaninput_runtime_bridge_added"] is False
    assert boundary["live_adapter_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["approval_enforcement_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_behavior_added"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True
    assert boundary["phase_24_requires_explicit_approval"] is True


def test_phase_24_approval_question_preserves_forbidden_scope() -> None:
    question = _load_json(PHASE_FIXTURE_PATH)["phase_24_approval_question"]
    assert "docs/tests/fixtures-only audit/archive" in question
    assert "runtime implementation" in question
    assert "lima/ changes" in question
    assert "tests/support/ changes" in question
    assert "Sparkbot wiring" in question
    assert "HumanInput runtime bridge" in question
    assert "approval enforcement" in question
    assert "execution" in question
    assert "dispatch" in question
    assert "audit persistence" in question
    assert "physical-world action" in question
    assert "hidden side effects" in question


def test_recommended_phase_24_direction_is_next_lane_decision() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["recommended_phase_24_direction"] == (
        "docs_tests_fixtures_only_audit_archive_and_next_lane_decision"
    )


def test_no_phase_23_5_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_23_5*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_23_5*"))
