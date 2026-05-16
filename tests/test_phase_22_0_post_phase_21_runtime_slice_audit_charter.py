"""Static checks for the Phase 22.0 post-Phase-21 audit charter."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_22_0_POST_PHASE_21_RUNTIME_SLICE_AUDIT_CHARTER.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_22_0_post_phase_21_runtime_slice_audit_charter.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_22_0_is_no_code_design_charter() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "22.0"
    assert fixture["runtime_code_modified"] is False
    assert fixture["phase_21_audit_result"] == "pass_with_approved_narrow_runtime_slice"
    assert fixture["phase_23_gate"]["requires_explicit_phil_approval"] is True


def test_phase_21_audit_scope_is_exact() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase_21_runtime_files_touched"] == [
        "lima/kernel/intake_candidate.py",
        "lima/kernel/candidate_status.py",
    ]
    assert "lima/kernel/__init__.py" in fixture["phase_21_runtime_files_not_touched"]
    assert "tests/support" in fixture["phase_21_runtime_files_not_touched"]


def test_phase_22_options_are_documented() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert "test_only_hardening_for_provenance_candidate_invariants" in fixture["phase_22_options"]
    assert "sparkbot_integration_boundary_planning" in fixture["phase_22_options"]
    assert "robo_os_physical_world_boundary_planning" in fixture["phase_22_options"]
    assert "pause_and_preserve_current_runtime_state" in fixture["phase_22_options"]


def test_phase_document_preserves_boundaries() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "docs/tests/fixtures-only no-code design lane" in phase_doc
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "Phase 23 must remain gated" in phase_doc


def test_boundary_results_show_no_forbidden_phase_22_0_changes() -> None:
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
    assert boundary["physical_world_behavior_added"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True


def test_no_phase_22_0_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_22_0*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_22_0*"))
