"""Static checks for Phase 10.4 runtime expansion approval gate closeout."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_10_4_PHASE_10_RUNTIME_EXPANSION_APPROVAL_GATE_CLOSEOUT.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_10_4_phase_10_runtime_expansion_approval_gate_closeout.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_no_code_approval_gate_closeout_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "10.4"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False
    assert fixture["phase_11_runtime_implementation_approved_now"] is False
    assert fixture["phase_11_requires_explicit_phil_approval"] is True


def test_completed_phase_ten_scope_is_listed() -> None:
    completed = _load_json(PHASE_FIXTURE_PATH)["completed_phase_10_scope"]
    assert completed == [
        "phase_10_0_post_phase_9_runtime_slice_review",
        "phase_10_1_next_runtime_slice_design_options",
        "phase_10_2_exact_file_touch_map_for_next_runtime_slice",
        "phase_10_3_acceptance_test_and_rollback_plan",
    ]


def test_future_phase_eleven_eligible_files_are_exact_if_approved() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["future_phase_11_eligible_files_if_approved"] == [
        "lima/kernel/intake_candidate.py",
        "lima/kernel/__init__.py",
        "lima/kernel/candidate_status.py",
    ]


def test_phase_eleven_approval_question_preserves_all_boundaries() -> None:
    question = _load_json(PHASE_FIXTURE_PATH)["exact_phase_11_approval_question"]
    assert "candidate validation and candidate status normalization" in question
    assert "lima/kernel/intake_candidate.py" in question
    assert "lima/kernel/__init__.py" in question
    assert "lima/kernel/candidate_status.py" in question
    assert "HumanInput runtime bridge behavior" in question
    assert "Sparkbot wiring" in question
    assert "live adapters" in question
    assert "IntentCompiler runtime behavior" in question
    assert "GuardianDecision runtime behavior" in question
    assert "approval enforcement" in question
    assert "execution" in question
    assert "dispatch" in question
    assert "audit persistence" in question
    assert "physical-world action" in question


def test_not_implemented_list_blocks_runtime_expansion_claims() -> None:
    not_implemented = set(_load_json(PHASE_FIXTURE_PATH)["not_implemented"])
    assert "runtime_candidate_validation" in not_implemented
    assert "runtime_candidate_status_normalization" in not_implemented
    assert "lima/kernel/candidate_status.py" in not_implemented
    assert "humaninput_runtime_bridge" in not_implemented
    assert "sparkbot_wiring" in not_implemented
    assert "live_adapter" in not_implemented
    assert "intentcompiler_runtime_behavior" in not_implemented
    assert "guardiandecision_runtime_behavior" in not_implemented
    assert "approval_enforcement" in not_implemented
    assert "execution" in not_implemented
    assert "dispatch" in not_implemented
    assert "audit_persistence" in not_implemented
    assert "shell_browser_network_file_mutation_robotics_physical_world_behavior" in not_implemented


def test_phase_document_closes_lane_and_stops_for_phil_decision() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "closes the Phase 10 no-code design lane" in phase_doc
    assert "Until Phil explicitly approves" in phase_doc
    assert "Phase 11 runtime implementation is blocked" in phase_doc
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc


def test_recommended_next_action_is_stop_for_explicit_decision() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["recommended_next_action"] == "stop_for_explicit_phil_phase_11_decision"


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["helper_behavior_changed"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["live_adapter_added"] is False
    assert boundary["approval_enforcement_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False


def test_no_phase_ten_four_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_10_4*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_10_4*"))
