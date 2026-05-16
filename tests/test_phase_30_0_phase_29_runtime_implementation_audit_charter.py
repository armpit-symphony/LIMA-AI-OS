"""Phase 29 runtime implementation audit charter tests for Phase 30.0."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_30_0_PHASE_29_RUNTIME_IMPLEMENTATION_AUDIT_CHARTER.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_30_0_phase_29_runtime_implementation_audit_charter.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_30_0_is_audit_charter_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "30.0"
    assert fixture["phase_29_audit_result"] == "PASS"
    assert fixture["runtime_code_modified"] is False
    assert "audit charter only" in phase_doc
    assert "does not implement runtime behavior" in phase_doc


def test_phase_29_audit_verified_no_forbidden_changes() -> None:
    verified = _load_json(PHASE_FIXTURE_PATH)["phase_29_verified"]
    assert verified["clean_synced_main"] is True
    assert verified["merge_commits_exist"] is True
    assert verified["tags_exist"] is True
    assert verified["lima_changed"] is False
    assert verified["tests_support_changed"] is False
    assert verified["runtime_behavior_changed"] is False
    assert verified["sparkbot_wiring_imports_added"] is False
    assert verified["humaninput_runtime_bridge_added"] is False
    assert verified["live_adapter_added"] is False
    assert verified["execution_approval_dispatch_audit_persistence_added"] is False
    assert verified["shell_browser_network_file_robotics_physical_world_behavior_added"] is False
    assert verified["external_service_calls_added"] is False


def test_phase_29_validation_is_recorded_as_passing() -> None:
    verified = _load_json(PHASE_FIXTURE_PATH)["phase_29_verified"]
    assert verified["phase_29_targeted_tests_passed"] is True
    assert verified["full_suite_passed"] is True
    assert verified["compileall_lima_passed"] is True
    assert verified["git_diff_check_passed"] is True


def test_phase_30_runtime_scope_is_exact_and_narrow() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    approved = set(fixture["approved_phase_30_runtime_scope"])
    forbidden = set(fixture["forbidden_phase_30_runtime_scope"])
    assert approved == {
        "lima/kernel/runtime_state.py",
        "lima/kernel/__init__.py_only_if_safe_public_export_required",
    }
    assert "lima/kernel/intake_candidate.py" in forbidden
    assert "lima/kernel/candidate_status.py" in forbidden
    assert "all_other_existing_lima_files" in forbidden
    assert "new_runtime_modules_outside_lima_kernel_runtime_state_py" in forbidden


def test_runtime_slice_constraints_preserve_read_only_boundary() -> None:
    constraints = _load_json(PHASE_FIXTURE_PATH)["runtime_slice_constraints"]
    assert constraints["deterministic"] is True
    assert constraints["local_only"] is True
    assert constraints["pure_read_only"] is True
    assert constraints["non_authoritative"] is True
    assert constraints["non_executing"] is True
    assert constraints["side_effect_free"] is True
    assert constraints["safe_under_malformed_input"] is True
    assert constraints["safe_under_unknown_values"] is True
    assert constraints["safe_under_bypass_wording"] is True
    assert constraints["phase_5_runtime_bridge_remains_gated"] is True


def test_no_phase_30_0_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_30_0*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_30_0*"))
