"""Static checks for Phase 7.3 runtime implementation test planning."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_7_3_RUNTIME_IMPLEMENTATION_TEST_PLAN.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_7_3_runtime_implementation_test_plan.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_declares_test_plan_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "7.3"
    assert fixture["non_runtime"] is True
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["test_plan_only"] is True


def test_future_test_families_cover_core_runtime_risks() -> None:
    families = set(_load_json(PHASE_FIXTURE_PATH)["future_test_families"])
    assert "import_boundary_tests" in families
    assert "typed_input_validation_tests" in families
    assert "raw_natural_language_rejection_tests" in families
    assert "non_executable_candidate_output_tests" in families
    assert "approval_bypass_rejection_tests" in families
    assert "guardiandecision_non_creation_tests" in families
    assert "sparkbot_coupling_rejection_tests" in families
    assert "side_effect_rejection_tests" in families


def test_required_negative_tests_block_runtime_side_effects() -> None:
    negative = set(_load_json(PHASE_FIXTURE_PATH)["required_negative_tests"])
    assert "missing_typed_input" in negative
    assert "raw_chat_text_without_explicit_typed_metadata" in negative
    assert "operator_admin_phil_trusted_approval_bypass_wording" in negative
    assert "shell_command_requests" in negative
    assert "browser_or_network_requests" in negative
    assert "file_mutation_requests" in negative
    assert "model_call_requests" in negative
    assert "sparkbot_import_or_runtime_coupling" in negative
    assert "real_guardiandecision_creation" in negative
    assert "approval_enforcement" in negative
    assert "audit_persistence" in negative
    assert "robotics_or_physical_world_requests" in negative


def test_positive_tests_are_limited_to_non_executable_metadata() -> None:
    positive = set(_load_json(PHASE_FIXTURE_PATH)["required_positive_tests_only"])
    assert positive == {
        "typed_explicit_metadata_is_accepted",
        "provenance_is_preserved",
        "candidate_metadata_remains_non_executable",
        "guardian_review_boundary_refs_present",
        "approval_state_remains_descriptive",
        "execution_and_side_effects_remain_disallowed",
    }


def test_future_validation_commands_include_full_and_boundary_checks() -> None:
    commands = set(_load_json(PHASE_FIXTURE_PATH)["future_validation_commands"])
    assert "targeted_tests_for_changed_files" in commands
    assert "all_phase_7_gate_tests" in commands
    assert "python -m pytest -q" in commands
    assert "python -m compileall lima" in commands
    assert "git diff --check" in commands
    assert "forbidden_path_review" in commands


def test_ready_only_for_phase_seven_four_decision_gate() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["ready_for"] == [
        "phase_7_4_docs_tests_fixtures_only_implementation_decision_gate_closeout"
    ]
    assert "runtime_behavior" in fixture["not_ready_for"]
    assert "lima_changes" in fixture["not_ready_for"]
    assert "approval_enforcement" in fixture["not_ready_for"]


def test_doc_keeps_test_plan_non_runtime() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "It is docs/tests/fixtures only" in phase_doc
    assert "does not implement runtime behavior" in phase_doc
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "Runtime implementation remains blocked" in phase_doc


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


def test_no_phase_seven_three_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_7_3*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_7_3*"))
