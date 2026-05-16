"""Phase 31 next-slice design audit charter tests for Phase 32.0."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_32_0_PHASE_31_NEXT_SLICE_DESIGN_AUDIT_CHARTER.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_32_0_phase_31_next_slice_design_audit_charter.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_32_0_is_design_audit_charter_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "32.0"
    assert fixture["phase_31_audit_result"] == "PASS"
    assert fixture["runtime_code_modified"] is False
    assert "audit charter and design-lane opening only" in phase_doc
    assert "does not implement new runtime behavior" in phase_doc


def test_phase_31_audit_verified_no_runtime_or_support_changes() -> None:
    verified = _load_json(PHASE_FIXTURE_PATH)["phase_31_verified"]
    assert verified["clean_synced_main"] is True
    assert verified["merge_commits_exist"] is True
    assert verified["tags_exist"] is True
    assert verified["runtime_files_changed"] is False
    assert verified["runtime_state_py_changed"] is False
    assert verified["kernel_init_changed"] is False
    assert verified["intake_candidate_changed"] is False
    assert verified["candidate_status_changed"] is False
    assert verified["other_forbidden_lima_files_changed"] is False
    assert verified["tests_support_changed"] is False


def test_phase_31_audit_verified_no_forbidden_behavior() -> None:
    verified = _load_json(PHASE_FIXTURE_PATH)["phase_31_verified"]
    assert verified["sparkbot_wiring_imports_added"] is False
    assert verified["humaninput_runtime_bridge_added"] is False
    assert verified["live_adapter_added"] is False
    assert verified["intentcompiler_runtime_behavior_changed"] is False
    assert verified["guardiandecision_runtime_behavior_changed"] is False
    assert verified["execution_approval_dispatch_audit_persistence_added"] is False
    assert verified["shell_browser_network_file_robotics_physical_world_behavior_added"] is False
    assert verified["external_service_calls_added"] is False
    assert (
        verified[
            "background_workers_queues_daemons_subprocesses_threads_database_writes_hidden_side_effects_added"
        ]
        is False
    )


def test_phase_31_validation_is_recorded_as_passing() -> None:
    verified = _load_json(PHASE_FIXTURE_PATH)["phase_31_verified"]
    assert verified["phase_31_targeted_tests_passed"] is True
    assert verified["full_suite_passed"] is True
    assert verified["compileall_lima_passed"] is True
    assert verified["git_diff_check_passed"] is True


def test_phase_32_scope_is_no_code_design_review_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase_32_scope"] == "docs_tests_fixtures_only_design_review"
    assert fixture["phase_32_runtime_implementation_approved"] is False


def test_no_phase_32_0_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_32_0*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_32_0*"))
