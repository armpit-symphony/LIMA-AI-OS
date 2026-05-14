"""Static checks for Phase 8.1 exact runtime file-touch map."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_8_1_EXACT_RUNTIME_FILE_TOUCH_MAP.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_8_1_exact_runtime_file_touch_map.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_docs_tests_fixtures_only_file_touch_map() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "8.1"
    assert fixture["non_runtime"] is True
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_approved"] is False


def test_eligible_existing_files_are_exact_and_future_only() -> None:
    files = _load_json(PHASE_FIXTURE_PATH)["eligible_existing_files_future_only"]
    assert files == [
        "lima/contracts/boundary.py",
        "lima/contracts/intent.py",
        "lima/contracts/guardian.py",
        "lima/contracts/events.py",
        "lima/contracts/privacy.py",
        "lima/__init__.py",
    ]


def test_eligible_new_files_are_exact_and_marked_future_only() -> None:
    files = _load_json(PHASE_FIXTURE_PATH)["eligible_new_files_future_only"]
    assert files == [
        "lima/kernel/__init__.py",
        "lima/kernel/intake_candidate.py",
    ]
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "These files do not exist in Phase 8.1 and must not be created by this phase" in phase_doc


def test_forbidden_file_surfaces_include_runtime_execution_areas_and_tests_support() -> None:
    forbidden = set(_load_json(PHASE_FIXTURE_PATH)["forbidden_file_surfaces"])
    assert "lima/adapters/**" in forbidden
    assert "lima/guardian/**" in forbidden
    assert "lima/harness/**" in forbidden
    assert "lima/io/**" in forbidden
    assert "lima/persistence/**" in forbidden
    assert "lima/services/**" in forbidden
    assert "lima/shells/**" in forbidden
    assert "lima/spine/**" in forbidden
    assert "tests/support/**" in forbidden


def test_touch_rules_keep_future_slice_non_executing_and_authority_free() -> None:
    rules = _load_json(PHASE_FIXTURE_PATH)["touch_rules_for_later_approved_runtime_slice"]
    assert rules["only_named_eligible_files_may_be_touched"] is True
    assert rules["targeted_tests_required_for_every_touched_file"] is True
    assert rules["new_public_exports_must_stay_non_executing"] is True
    assert rules["candidate_outputs_must_be_non_executable"] is True
    assert rules["candidate_outputs_must_not_contain_authority"] is True
    assert rules["forbidden_surface_need_requires_stop_and_phil_approval"] is True


def test_doc_says_file_eligibility_is_not_current_approval() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "does not modify any runtime file" in phase_doc
    assert "Eligibility here is not approval to modify these files now" in phase_doc
    assert "These files do not exist in Phase 8.1 and must not be created by this phase" in phase_doc
    assert "Runtime implementation remains blocked" in phase_doc


def test_phase_five_runtime_bridge_remains_gated() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase_5_runtime_bridge_remains_gated"] is True
    assert fixture["next_phase"] == "phase_8_2_runtime_acceptance_test_design"


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["runtime_behavior_added"] is False
    assert boundary["files_under_lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["helper_behavior_changed"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["execution_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False


def test_no_phase_eight_one_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_8_1*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_8_1*"))
