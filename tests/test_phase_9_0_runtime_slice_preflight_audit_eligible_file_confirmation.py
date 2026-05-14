"""Static checks for Phase 9.0 runtime slice preflight confirmation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_9_0_RUNTIME_SLICE_PREFLIGHT_AUDIT_ELIGIBLE_FILE_CONFIRMATION.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_9_0_runtime_slice_preflight_audit_eligible_file_confirmation.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_declares_preflight_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "9.0"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_behavior_added"] is False


def test_phase_eight_one_file_touch_map_is_explicit() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase_8_1_file_touch_map_is_explicit"] is True
    assert fixture["phase_9_0_decision"] == "continue_to_phase_9_1_acceptance_test_scaffolding"


def test_eligible_runtime_files_match_phase_eight_one_map() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["eligible_existing_runtime_files"] == [
        "lima/contracts/boundary.py",
        "lima/contracts/intent.py",
        "lima/contracts/guardian.py",
        "lima/contracts/events.py",
        "lima/contracts/privacy.py",
        "lima/__init__.py",
    ]
    assert fixture["eligible_new_runtime_files"] == [
        "lima/kernel/__init__.py",
        "lima/kernel/intake_candidate.py",
    ]


def test_phase_nine_two_requires_phase_nine_one_acceptance_tests_first() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert (
        fixture["phase_9_2_runtime_implementation_precondition"]
        == "phase_9_1_acceptance_tests_must_exist_first"
    )


def test_forbidden_scope_repeats_runtime_boundaries() -> None:
    forbidden_scope = set(_load_json(PHASE_FIXTURE_PATH)["forbidden_scope"])
    assert "tests/support/**" in forbidden_scope
    assert "sparkbot_import_or_wiring" in forbidden_scope
    assert "live_adapter" in forbidden_scope
    assert "humaninput_runtime_bridge" in forbidden_scope
    assert "approval_enforcement" in forbidden_scope
    assert "execution" in forbidden_scope
    assert "audit_persistence" in forbidden_scope
    assert "shell_browser_network_file_mutation_robotics_physical_world_side_effects" in forbidden_scope


def test_phase_doc_records_preflight_and_no_runtime_behavior() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "Phase 9.0 confirms the Phase 8.1 runtime file-touch map" in phase_doc
    assert "does not modify `lima/`" in phase_doc
    assert "does not implement runtime behavior" in phase_doc
    assert "file-touch map explicit enough to continue to Phase 9.1" in phase_doc


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["files_under_lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_added"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["live_adapter_added"] is False
    assert boundary["humaninput_runtime_bridge_added"] is False
    assert boundary["intentcompiler_runtime_changed"] is False
    assert boundary["guardiandecision_runtime_changed"] is False
    assert boundary["approval_enforcement_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False


def test_no_phase_nine_zero_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_9_0*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_9_0*"))
