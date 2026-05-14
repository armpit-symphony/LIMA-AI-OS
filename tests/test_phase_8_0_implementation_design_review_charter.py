"""Static checks for Phase 8.0 implementation design review charter."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_8_0_IMPLEMENTATION_DESIGN_REVIEW_CHARTER.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_8_0_implementation_design_review_charter.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_no_code_design_review_charter() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "8.0"
    assert fixture["non_runtime"] is True
    assert fixture["docs_tests_fixtures_only"] is True


def test_phase_eight_reviews_phase_seven_source_context() -> None:
    context = _load_json(PHASE_FIXTURE_PATH)["source_context"]
    assert context == [
        "phase_7_0_kernel_runtime_implementation_charter",
        "phase_7_1_first_runtime_slice_eligibility_map",
        "phase_7_2_kernel_runtime_safety_preconditions",
        "phase_7_3_runtime_implementation_test_plan",
        "phase_7_4_phase_7_implementation_decision_gate_closeout",
        "phase_7_5_phase_7_no_code_kernel_runtime_charter_audit_archive_closeout",
    ]


def test_design_review_package_requires_exact_future_artifacts() -> None:
    required = set(_load_json(PHASE_FIXTURE_PATH)["design_review_package_required"])
    assert "narrowest_future_runtime_slice_definition" in required
    assert "exact_future_file_touch_map" in required
    assert "future_runtime_acceptance_tests" in required
    assert "rollback_expectations" in required
    assert "audit_proof_requirements" in required
    assert "implementation_success_and_failure_criteria" in required
    assert "final_approval_question" in required


def test_narrowest_future_slice_is_non_executing_candidate_metadata_only() -> None:
    future_slice = _load_json(PHASE_FIXTURE_PATH)["narrowest_future_runtime_slice"]
    assert future_slice["name"] == "non_executing_kernel_intake_to_candidate_coordinator"
    assert future_slice["accepts_only_already_typed_explicit_input_metadata"] is True
    assert future_slice["produces_non_executable_candidate_metadata"] is True
    assert future_slice["guardian_review_boundary_future_only"] is True
    assert future_slice["parses_natural_language"] is False
    assert future_slice["calls_models"] is False
    assert future_slice["calls_tools"] is False
    assert future_slice["executes_commands"] is False
    assert future_slice["mutates_files"] is False
    assert future_slice["persists_audit"] is False
    assert future_slice["enforces_approval"] is False
    assert future_slice["creates_real_intentenvelope"] is False
    assert future_slice["creates_real_guardiandecision"] is False


def test_phase_five_runtime_bridge_remains_gated() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase_5_runtime_bridge_remains_gated"] is True
    assert fixture["next_phase"] == "phase_8_1_exact_runtime_file_touch_map"


def test_not_ready_for_blocks_runtime_and_side_effect_surfaces() -> None:
    blocked = set(_load_json(PHASE_FIXTURE_PATH)["not_ready_for"])
    assert "runtime_implementation" in blocked
    assert "lima_changes" in blocked
    assert "tests_support_changes" in blocked
    assert "sparkbot_import_or_wiring" in blocked
    assert "live_adapter_code" in blocked
    assert "runtime_humaninput_to_intentenvelope_bridge" in blocked
    assert "approval_enforcement" in blocked
    assert "execution" in blocked
    assert "audit_persistence" in blocked
    assert "shell_browser_network_file_mutation_robotics_physical_world_side_effects" in blocked


def test_doc_keeps_phase_eight_no_code() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "opens Phase 8 as a no-code implementation design review lane" in phase_doc
    assert "without modifying runtime code" in phase_doc
    assert "does not implement runtime behavior" in phase_doc
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "Phase 5 HumanInput runtime bridge remains gated" in phase_doc


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["runtime_behavior_added"] is False
    assert boundary["files_under_lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["helper_behavior_changed"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["live_adapter_added"] is False
    assert boundary["runtime_bridge_added"] is False
    assert boundary["intentcompiler_runtime_changed"] is False
    assert boundary["guardiandecision_runtime_changed"] is False
    assert boundary["approval_enforcement_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False


def test_no_phase_eight_zero_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_8_0*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_8_0*"))
