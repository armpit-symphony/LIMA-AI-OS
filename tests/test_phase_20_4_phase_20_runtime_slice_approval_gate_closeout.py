"""Static checks for Phase 20.4 runtime slice approval gate closeout."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_20_4_PHASE_20_RUNTIME_SLICE_APPROVAL_GATE_CLOSEOUT.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_20_4_phase_20_runtime_slice_approval_gate_closeout.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_docs_tests_fixtures_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "20.4"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False


def test_phase_twenty_completed_scope_is_archived() -> None:
    completed = set(_load_json(PHASE_FIXTURE_PATH)["completed_scope"])
    assert completed == {
        "phase_20_0_post_regression_runtime_slice_design_charter",
        "phase_20_1_next_runtime_slice_options_review",
        "phase_20_2_exact_file_touch_map_for_candidate_slice",
        "phase_20_3_acceptance_test_and_rollback_plan",
    }


def test_closeout_lists_what_phase_twenty_did_and_did_not_add() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert set(fixture["phase_20_added"]) == {
        "no_code_design_docs",
        "static_fixtures",
        "static_tests",
        "roadmap_state_updates",
    }
    not_added = set(fixture["phase_20_not_added"])
    assert "runtime_behavior" in not_added
    assert "lima_changes" in not_added
    assert "tests_support_changes" in not_added
    assert "candidate_provenance_implementation" in not_added
    assert "future_acceptance_test_implementation" in not_added
    assert "execution" in not_added
    assert "dispatch" in not_added
    assert "audit_persistence" in not_added


def test_phase_twenty_one_question_preserves_exact_scope() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    question = fixture["exact_phase_21_approval_question"]
    assert fixture["recommended_phase_21_direction"] == "candidate_provenance_hardening_runtime_slice"
    assert fixture["phase_21_approved"] is False
    assert "touching only lima/kernel/intake_candidate.py and lima/kernel/candidate_status.py" in question
    assert "forbidding lima/kernel/__init__.py" in question
    assert "tests/support changes" in question
    assert "hidden side effects" in question


def test_future_eligible_runtime_files_are_preserved() -> None:
    files = _load_json(PHASE_FIXTURE_PATH)["future_eligible_runtime_files"]
    assert files == [
        "lima/kernel/intake_candidate.py",
        "lima/kernel/candidate_status.py",
    ]


def test_phase_document_preserves_stop_gate() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "Phase 21 remains unapproved" in phase_doc
    assert "must not begin without explicit Phil approval" in phase_doc
    assert "No `lima/` changes" in phase_doc
    assert "No `tests/support/` changes" in phase_doc
    assert "No future acceptance-test implementation" in phase_doc


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


def test_no_phase_twenty_four_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_20_4*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_20_4*"))
