"""Phase 32 test-only hardening audit charter tests for Phase 33.0."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_33_0_PHASE_32_TEST_ONLY_HARDENING_AUDIT_CHARTER.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_33_0_phase_32_test_only_hardening_audit_charter.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_33_0_opens_test_only_hardening_lane() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "33.0"
    assert fixture["phase_32_audit_result"] == "PASS"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_implementation_approved"] is False
    assert fixture["runtime_files_changed_in_phase_33"] == []
    assert "does not implement runtime behavior" in phase_doc


def test_phase_32_audit_verified_no_runtime_or_support_changes() -> None:
    verified = _load_json(PHASE_FIXTURE_PATH)["phase_32_verified"]
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


def test_phase_32_audit_verified_no_forbidden_behavior() -> None:
    verified = _load_json(PHASE_FIXTURE_PATH)["phase_32_verified"]
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


def test_phase_32_validation_is_recorded_as_passing() -> None:
    verified = _load_json(PHASE_FIXTURE_PATH)["phase_32_verified"]
    assert verified["phase_32_targeted_tests_passed"] is True
    assert verified["full_suite_passed"] is True
    assert verified["compileall_lima_passed"] is True
    assert verified["git_diff_check_passed"] is True


def test_no_phase_33_0_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_33_0*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_33_0*"))
