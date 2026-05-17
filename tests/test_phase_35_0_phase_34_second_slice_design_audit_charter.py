"""Phase 34 design audit charter tests for Phase 35.0."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_35_0_PHASE_34_SECOND_SLICE_DESIGN_AUDIT_CHARTER.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_35_0_phase_34_second_slice_design_audit_charter.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_35_0_opens_no_code_design_review_lane() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "35.0"
    assert fixture["phase_34_audit_result"] == "PASS"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_implementation_approved"] is False
    assert fixture["runtime_files_changed_in_phase_35"] == []
    assert "does not implement runtime behavior" in phase_doc


def test_phase_34_audit_verified_no_runtime_or_support_changes() -> None:
    verified = _load_json(PHASE_FIXTURE_PATH)["phase_34_verified"]
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


def test_phase_34_audit_verified_no_forbidden_behavior() -> None:
    verified = _load_json(PHASE_FIXTURE_PATH)["phase_34_verified"]
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


def test_phase_34_validation_and_runtime_state_safety_are_recorded() -> None:
    verified = _load_json(PHASE_FIXTURE_PATH)["phase_34_verified"]
    assert verified["phase_34_targeted_tests_passed"] is True
    assert verified["full_suite_passed"] is True
    assert verified["compileall_lima_passed"] is True
    assert verified["git_diff_check_passed"] is True
    assert verified["runtime_state_remains_read_only_non_authoritative_non_executing"] is True
    assert verified["nested_suspicious_metadata_hardening_remained_test_only"] is True
    assert verified["concrete_runtime_state_gap_remains"] is False


def test_no_phase_35_0_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_35_0*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_35_0*"))
