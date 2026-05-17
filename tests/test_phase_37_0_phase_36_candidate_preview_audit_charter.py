"""Phase 36 candidate preview audit charter tests for Phase 37.0."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_37_0_PHASE_36_CANDIDATE_PREVIEW_AUDIT_CHARTER.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_37_0_phase_36_candidate_preview_audit_charter.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_37_0_opens_docs_tests_fixtures_only_audit_lane() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "37.0"
    assert fixture["phase_36_audit_result"] == "PASS"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_behavior_added_in_phase_37_0"] is False
    assert fixture["runtime_files_changed_in_phase_37_0"] == []
    assert "does not add runtime behavior" in phase_doc


def test_phase_36_audit_records_exact_runtime_scope() -> None:
    verified = _load_json(PHASE_FIXTURE_PATH)["phase_36_verified"]
    assert verified["candidate_preview_py_added_as_approved_slice"] is True
    assert verified["kernel_init_changed_only_for_safe_export"] is True
    assert verified["runtime_state_py_changed"] is False
    assert verified["intake_candidate_py_changed"] is False
    assert verified["candidate_status_py_changed"] is False
    assert verified["other_forbidden_lima_files_changed"] is False
    assert verified["tests_support_changed"] is False


def test_phase_36_audit_records_narrow_stale_test_adjustment() -> None:
    verified = _load_json(PHASE_FIXTURE_PATH)["phase_36_verified"]
    assert (
        verified["stale_phase_35_test_adjustment_file"]
        == "tests/test_phase_35_1_second_runtime_slice_candidate_inventory.py"
    )
    assert verified["other_pre_phase_36_old_phase_tests_changed"] is False


def test_phase_36_audit_records_absent_forbidden_behavior() -> None:
    verified = _load_json(PHASE_FIXTURE_PATH)["phase_36_verified"]
    assert verified["sparkbot_wiring_imports_added"] is False
    assert verified["humaninput_runtime_bridge_added"] is False
    assert verified["live_adapter_added"] is False
    assert verified["intentcompiler_runtime_behavior_changed"] is False
    assert verified["guardiandecision_runtime_behavior_changed"] is False
    assert verified["approval_execution_dispatch_audit_persistence_added"] is False
    assert verified["shell_browser_network_file_robotics_physical_world_behavior_added"] is False
    assert verified["external_service_calls_added"] is False
    assert (
        verified[
            "background_workers_queues_daemons_subprocesses_threads_database_writes_hidden_side_effects_added"
        ]
        is False
    )


def test_phase_36_audit_records_validation_passes() -> None:
    verified = _load_json(PHASE_FIXTURE_PATH)["phase_36_verified"]
    assert verified["phase_36_targeted_tests_passed"] is True
    assert verified["full_suite_passed"] is True
    assert verified["compileall_lima_passed"] is True
    assert verified["git_diff_check_passed"] is True


def test_no_phase_37_0_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_37_0*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_37_0*"))
