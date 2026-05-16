"""Static checks for Phase 20.5 design lane archive closeout."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_20_5_PHASE_20_NEXT_RUNTIME_SLICE_DESIGN_LANE_AUDIT_ARCHIVE_CLOSEOUT.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_20_5_phase_20_next_runtime_slice_design_lane_audit_archive_closeout.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_docs_tests_fixtures_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "20.5"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False


def test_phase_twenty_completed_scope_is_archived() -> None:
    completed = set(_load_json(PHASE_FIXTURE_PATH)["completed_scope"])
    assert completed == {
        "phase_20_0_post_regression_runtime_slice_design_charter",
        "phase_20_1_next_runtime_slice_options_review",
        "phase_20_2_exact_file_touch_map_for_candidate_slice",
        "phase_20_3_acceptance_test_and_rollback_plan",
        "phase_20_4_phase_20_runtime_slice_approval_gate_closeout",
    }


def test_phase_twenty_is_archived_as_no_code_design_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert "future_phase_21_design_package" in fixture["phase_20_added"]
    not_added = set(fixture["phase_20_not_added"])
    assert "runtime_behavior" in not_added
    assert "lima_changes" in not_added
    assert "tests_support_changes" in not_added
    assert "sparkbot_wiring" in not_added
    assert "humaninput_runtime_bridge" in not_added
    assert "approval_enforcement" in not_added
    assert "execution" in not_added
    assert "dispatch" in not_added
    assert "audit_persistence" in not_added


def test_phase_twenty_one_runtime_implementation_is_not_approved() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase_21_approved"] is False
    assert "Do you approve Phase 21" in fixture["exact_phase_21_approval_question"]
    assert "candidate provenance hardening" in fixture["exact_phase_21_approval_question"]


def test_future_runtime_file_scope_and_forbidden_scope_are_preserved() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["future_eligible_runtime_files"] == [
        "lima/kernel/intake_candidate.py",
        "lima/kernel/candidate_status.py",
    ]
    forbidden = set(fixture["future_forbidden_runtime_scope"])
    assert "lima/kernel/__init__.py" in forbidden
    assert "new_runtime_modules" in forbidden
    assert "all_other_lima_files" in forbidden
    assert "tests/support_changes" in forbidden
    assert "sparkbot_wiring" in forbidden
    assert "humaninput_runtime_bridge" in forbidden
    assert "live_adapters" in forbidden
    assert "approval_enforcement" in forbidden
    assert "execution" in forbidden
    assert "dispatch" in forbidden
    assert "audit_persistence" in forbidden


def test_phase_document_preserves_explicit_phil_gate() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "Phase 21 remains gated and requires explicit Phil approval" in phase_doc
    assert "Phase 20.5 does not approve runtime implementation" in phase_doc
    assert "No `lima/` changes" in phase_doc
    assert "No `tests/support/` changes" in phase_doc


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["helper_behavior_changed"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["humaninput_runtime_bridge_added"] is False
    assert boundary["live_adapter_added"] is False
    assert boundary["intentcompiler_runtime_behavior_changed"] is False
    assert boundary["guardiandecision_runtime_behavior_changed"] is False
    assert boundary["approval_enforcement_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["shell_browser_network_file_mutation_robotics_physical_world_added"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True


def test_no_phase_twenty_five_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_20_5*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_20_5*"))
