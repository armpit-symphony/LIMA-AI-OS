"""Static checks for Phase 8.4 runtime implementation approval gate closeout."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_8_4_RUNTIME_IMPLEMENTATION_APPROVAL_GATE_CLOSEOUT.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_8_4_runtime_implementation_approval_gate_closeout.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_docs_tests_fixtures_only_approval_gate_closeout() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "8.4"
    assert fixture["non_runtime"] is True
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_implementation_approved"] is False


def test_completed_phase_eight_scope_lists_design_lane() -> None:
    completed = _load_json(PHASE_FIXTURE_PATH)["completed_phase_8_scope"]
    assert completed == [
        "phase_8_0_implementation_design_review_charter",
        "phase_8_1_exact_runtime_file_touch_map",
        "phase_8_2_runtime_acceptance_test_design",
        "phase_8_3_rollback_audit_proof_plan",
    ]


def test_designed_future_runtime_slice_remains_non_executing() -> None:
    future_slice = _load_json(PHASE_FIXTURE_PATH)["designed_future_runtime_slice"]
    assert future_slice["name"] == "non_executing_kernel_intake_to_candidate_coordinator"
    assert future_slice["typed_explicit_input_metadata_only"] is True
    assert future_slice["non_executable_candidate_metadata_output_only"] is True
    assert future_slice["parses_natural_language"] is False
    assert future_slice["creates_real_intentenvelope_behavior"] is False
    assert future_slice["creates_real_guardiandecision_behavior"] is False
    assert future_slice["enforces_approval"] is False
    assert future_slice["executes"] is False
    assert future_slice["persists_audit"] is False
    assert future_slice["calls_models"] is False
    assert future_slice["calls_tools"] is False
    assert future_slice["wires_sparkbot"] is False
    assert future_slice["touches_robotics_or_physical_world"] is False


def test_future_eligible_file_scope_matches_phase_eight_one_map() -> None:
    files = _load_json(PHASE_FIXTURE_PATH)["future_eligible_file_scope"]
    assert files == [
        "lima/contracts/boundary.py",
        "lima/contracts/intent.py",
        "lima/contracts/guardian.py",
        "lima/contracts/events.py",
        "lima/contracts/privacy.py",
        "lima/__init__.py",
        "lima/kernel/__init__.py",
        "lima/kernel/intake_candidate.py",
    ]


def test_future_runtime_preconditions_include_tests_rollback_and_audit_proof() -> None:
    preconditions = set(_load_json(PHASE_FIXTURE_PATH)["future_runtime_preconditions"])
    assert "targeted_tests_for_every_touched_file" in preconditions
    assert "all_phase_8_gate_tests" in preconditions
    assert "python -m pytest -q" in preconditions
    assert "python -m compileall lima" in preconditions
    assert "git diff --check" in preconditions
    assert "explicit_forbidden_path_review" in preconditions
    assert "rollback_path_documentation" in preconditions
    assert "audit_proof_as_test_evidence_only" in preconditions
    assert "non_executable_output_markers" in preconditions


def test_still_out_of_scope_blocks_runtime_escape_paths() -> None:
    blocked = set(_load_json(PHASE_FIXTURE_PATH)["still_out_of_scope"])
    assert "phase_5_humaninput_runtime_bridge" in blocked
    assert "runtime_humaninput_to_intentenvelope_bridge" in blocked
    assert "live_adapter_code" in blocked
    assert "sparkbot_import_or_wiring" in blocked
    assert "real_intentcompiler_behavior" in blocked
    assert "real_guardiandecision_behavior" in blocked
    assert "approval_enforcement" in blocked
    assert "execution" in blocked
    assert "audit_persistence" in blocked
    assert "shell_browser_network_file_mutation_robotics_physical_world_side_effects" in blocked


def test_approval_question_is_explicit_and_runtime_remains_blocked() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    question = fixture["exact_future_runtime_implementation_approval_question"]
    assert "Do you approve a narrow Phase 9 runtime implementation slice" in question
    assert "non-executing kernel intake-to-candidate coordinator" in question
    assert "touching only the Phase 8.1 eligible files" in question
    assert "still forbidding HumanInput runtime bridge behavior" in question
    assert fixture["phase_5_runtime_bridge_remains_gated"] is True
    assert fixture["requires_explicit_phil_approval_before_runtime_code"] is True


def test_recommended_next_options_require_operator_choice() -> None:
    options = set(_load_json(PHASE_FIXTURE_PATH)["recommended_next_options"])
    assert "approve_phase_9_narrow_runtime_implementation_slice_exactly_as_scoped" in options
    assert "request_another_no_code_review_of_phase_8_design_package" in options
    assert "sparkbot_integration_boundary_planning" in options
    assert "robo_os_physical_world_boundary_planning" in options
    assert "pause_and_preserve_current_state" in options


def test_doc_closes_phase_eight_without_runtime_implementation() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "closes the no-code Phase 8 implementation design review lane" in phase_doc
    assert "does not implement runtime behavior" in phase_doc
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "Until Phil explicitly answers yes to that narrow question, runtime implementation remains blocked" in phase_doc


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["runtime_behavior_added"] is False
    assert boundary["files_under_lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["helper_behavior_changed"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["execution_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False


def test_no_phase_eight_four_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_8_4*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_8_4*"))
