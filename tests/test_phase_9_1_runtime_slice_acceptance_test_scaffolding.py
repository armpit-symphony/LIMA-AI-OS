"""Static checks for Phase 9.1 runtime slice acceptance scaffolding."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_9_1_RUNTIME_SLICE_ACCEPTANCE_TEST_SCAFFOLDING.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_9_1_runtime_slice_acceptance_test_scaffolding.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_declares_acceptance_scaffolding_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "9.1"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_behavior_added"] is False


def test_acceptance_target_is_non_executing_coordinator_only() -> None:
    target = _load_json(PHASE_FIXTURE_PATH)["acceptance_target"]
    assert target == "pure_in_process_non_executing_kernel_intake_to_candidate_coordinator"


def test_phase_nine_two_acceptance_cases_are_machine_checkable() -> None:
    cases = set(_load_json(PHASE_FIXTURE_PATH)["phase_9_2_required_acceptance_cases"])
    assert "low_risk_synthetic_intake_creates_non_executing_candidate" in cases
    assert "unknown_intake_becomes_blocked_or_needs_review" in cases
    assert "malformed_intake_rejected_or_blocked_safely" in cases
    assert "stale_or_replayed_intake_rejected_or_blocked" in cases
    assert "candidate_always_non_executable" in cases
    assert "execution_allowed_always_false" in cases
    assert "side_effects_allowed_always_false" in cases
    assert "approval_state_never_approved" in cases
    assert "provenance_preserved" in cases
    assert "no_shell_browser_network_file_mutation_robotics_physical_world_behavior_reachable" in cases
    assert "no_sparkbot_import_or_wiring" in cases
    assert "phase_5_humaninput_runtime_bridge_remains_gated" in cases
    assert "only_phase_8_1_eligible_runtime_files_changed" in cases
    assert "phase_8_3_rollback_and_audit_proof_satisfied" in cases


def test_forbidden_runtime_interpretations_remain_blocked() -> None:
    blocked = set(_load_json(PHASE_FIXTURE_PATH)["forbidden_runtime_interpretations"])
    assert "raw_natural_language_parsing" in blocked
    assert "real_intentenvelope_creation" in blocked
    assert "real_guardiandecision_creation" in blocked
    assert "approval_enforcement" in blocked
    assert "tool_dispatch" in blocked
    assert "execution" in blocked
    assert "audit_persistence" in blocked
    assert "model_calls" in blocked
    assert "network_calls" in blocked
    assert "shell_or_browser_calls" in blocked
    assert "file_mutation" in blocked
    assert "driver_handoff" in blocked
    assert "sparkbot_wiring" in blocked
    assert "robotics_or_physical_world_action" in blocked


def test_phase_nine_two_touch_scope_is_phase_eight_one_only() -> None:
    allowed = set(_load_json(PHASE_FIXTURE_PATH)["phase_9_2_may_touch_only"])
    assert allowed == {
        "lima/contracts/boundary.py",
        "lima/contracts/intent.py",
        "lima/contracts/guardian.py",
        "lima/contracts/events.py",
        "lima/contracts/privacy.py",
        "lima/__init__.py",
        "lima/kernel/__init__.py",
        "lima/kernel/intake_candidate.py",
    }


def test_phase_doc_scaffolds_acceptance_without_runtime_code() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "Phase 9.1 converts the Phase 8.2 acceptance-test design" in phase_doc
    assert "does not modify `lima/`" in phase_doc
    assert "The Phase 9.2 target remains a pure in-process" in phase_doc
    assert "Phase 9.2 may implement the narrow coordinator only inside the Phase 8.1" in phase_doc


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


def test_no_phase_nine_one_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_9_1*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_9_1*"))
