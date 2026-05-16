"""Static checks for Phase 21.0 runtime slice preflight."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_21_0_RUNTIME_SLICE_PREFLIGHT_AUDIT_ELIGIBLE_FILE_CONFIRMATION.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_21_0_runtime_slice_preflight_audit_eligible_file_confirmation.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_confirms_exact_eligible_runtime_files() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "21.0"
    assert fixture["runtime_code_modified"] is False
    assert fixture["eligible_runtime_files"] == [
        "lima/kernel/intake_candidate.py",
        "lima/kernel/candidate_status.py",
    ]
    assert fixture["preflight_result"] == "phase_20_2_file_touch_map_is_unambiguous"


def test_phase_confirms_forbidden_runtime_files() -> None:
    forbidden = set(_load_json(PHASE_FIXTURE_PATH)["forbidden_runtime_files"])
    assert "lima/kernel/__init__.py" in forbidden
    assert "new_runtime_modules" in forbidden
    assert "all_other_lima_files" in forbidden
    assert "tests/support" in forbidden


def test_phase_document_preserves_runtime_boundary() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "does not implement runtime behavior" in phase_doc
    assert "`lima/kernel/intake_candidate.py`" in phase_doc
    assert "`lima/kernel/candidate_status.py`" in phase_doc
    assert "`lima/kernel/__init__.py`" in phase_doc
    assert "must not create a HumanInput runtime bridge" in phase_doc
    assert "hidden side effects" in phase_doc


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
    assert boundary["shell_browser_network_file_mutation_robotics_physical_world_added"] is False
    assert boundary["background_worker_queue_daemon_subprocess_thread_database_write_added"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True


def test_no_phase_twenty_one_zero_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_21_0*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_21_0*"))
