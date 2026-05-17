"""Phase 35 runtime implementation audit charter tests for Phase 36.0."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_36_0_PHASE_35_RUNTIME_IMPLEMENTATION_AUDIT_CHARTER.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_36_0_phase_35_runtime_implementation_audit_charter.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_36_0_records_phase_35_audit_pass() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "36.0"
    assert fixture["phase_35_audit_result"] == "PASS"
    assert fixture["runtime_files_changed_in_phase_36_0"] == []


def test_phase_35_audit_preserved_no_runtime_or_support_changes() -> None:
    verified = _load_json(PHASE_FIXTURE_PATH)["phase_35_verified"]
    assert verified["runtime_files_changed"] is False
    assert verified["runtime_state_py_changed"] is False
    assert verified["kernel_init_changed"] is False
    assert verified["intake_candidate_changed"] is False
    assert verified["candidate_status_changed"] is False
    assert verified["other_forbidden_lima_files_changed"] is False
    assert verified["tests_support_changed"] is False


def test_phase_35_audit_preserved_no_forbidden_behavior() -> None:
    verified = _load_json(PHASE_FIXTURE_PATH)["phase_35_verified"]
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


def test_phase_36_allowed_and_forbidden_file_scope_is_explicit() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["approved_phase_36_runtime_files"] == [
        "lima/kernel/candidate_preview.py",
        "lima/kernel/__init__.py_if_safe_public_export_required",
    ]
    assert "lima/kernel/runtime_state.py" in fixture["forbidden_phase_36_existing_runtime_files"]
    assert "lima/kernel/intake_candidate.py" in fixture["forbidden_phase_36_existing_runtime_files"]
    assert "lima/kernel/candidate_status.py" in fixture["forbidden_phase_36_existing_runtime_files"]
    assert fixture["tests_support_changes_allowed"] is False


def test_phase_36_0_does_not_create_candidate_preview_yet() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "does not implement runtime behavior" in phase_doc
    assert not (REPO_ROOT / "lima" / "kernel" / "candidate_preview.py").exists()
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_36_0*"))
