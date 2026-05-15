"""Static checks for Phase 10.5 design lane archive closeout."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_10_5_PHASE_10_NEXT_RUNTIME_SLICE_DESIGN_LANE_AUDIT_ARCHIVE_CLOSEOUT.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_10_5_phase_10_next_runtime_slice_design_lane_audit_archive_closeout.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_docs_tests_fixtures_only_archive() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "10.5"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False
    assert fixture["phase_11_runtime_implementation_approved_now"] is False
    assert fixture["phase_11_requires_explicit_phil_approval"] is True


def test_phase_ten_zero_through_four_are_listed_complete() -> None:
    completed = _load_json(PHASE_FIXTURE_PATH)["completed_phase_10_scope"]
    assert completed == [
        "phase_10_0_post_phase_9_runtime_slice_review",
        "phase_10_1_next_runtime_slice_design_options",
        "phase_10_2_exact_file_touch_map_for_next_runtime_slice",
        "phase_10_3_acceptance_test_and_rollback_plan",
        "phase_10_4_phase_10_runtime_expansion_approval_gate_closeout",
    ]


def test_phase_ten_is_archived_as_no_code_design_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase_10_added"] == [
        "docs",
        "fixtures",
        "static_tests",
        "roadmap_state_updates",
        "future_phase_11_design_package",
    ]
    not_added = set(fixture["phase_10_did_not_add"])
    assert "runtime_behavior" in not_added
    assert "lima_changes" in not_added
    assert "lima/kernel/candidate_status.py" in not_added
    assert "sparkbot_wiring" in not_added
    assert "humaninput_runtime_bridge" in not_added
    assert "live_adapter" in not_added
    assert "approval_enforcement" in not_added
    assert "execution" in not_added
    assert "dispatch" in not_added
    assert "audit_persistence" in not_added


def test_candidate_status_py_was_not_added() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert "lima/kernel/candidate_status.py" in fixture["phase_10_did_not_add"]
    assert fixture["boundary_results"]["candidate_status_added"] is False


def test_phase_eleven_question_and_phase_five_gate_are_preserved() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    question = fixture["exact_phase_11_approval_question"]
    assert fixture["phase_5_runtime_bridge_remains_gated"] is True
    assert "candidate validation and candidate status normalization" in question
    assert "lima/kernel/intake_candidate.py" in question
    assert "lima/kernel/__init__.py" in question
    assert "lima/kernel/candidate_status.py" in question
    assert "HumanInput runtime bridge behavior" in question
    assert "Sparkbot wiring" in question
    assert "approval enforcement" in question
    assert "execution" in question
    assert "dispatch" in question
    assert "audit persistence" in question
    assert "physical-world action" in question


def test_phase_document_blocks_phase_eleven_without_explicit_approval() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "archives Phase 10 as a completed no-code design lane" in phase_doc
    assert "Phase 11 remains gated and requires explicit Phil approval" in phase_doc
    assert "Phase 10 is archived as no-code design only" in phase_doc
    assert "does not add `lima/kernel/candidate_status.py`" in phase_doc


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["helper_behavior_changed"] is False
    assert boundary["candidate_status_added"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["humaninput_runtime_bridge_added"] is False
    assert boundary["live_adapter_added"] is False
    assert boundary["intentcompiler_runtime_behavior_changed"] is False
    assert boundary["guardiandecision_runtime_behavior_changed"] is False
    assert boundary["approval_enforcement_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False


def test_no_phase_ten_five_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_10_5*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_10_5*"))
