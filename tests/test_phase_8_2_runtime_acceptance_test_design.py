"""Static checks for Phase 8.2 runtime acceptance test design."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_8_2_RUNTIME_ACCEPTANCE_TEST_DESIGN.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_8_2_runtime_acceptance_test_design.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_docs_tests_fixtures_only_acceptance_test_design() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "8.2"
    assert fixture["non_runtime"] is True
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_approved"] is False


def test_required_future_test_families_cover_boundary_and_side_effect_risks() -> None:
    families = set(_load_json(PHASE_FIXTURE_PATH)["required_future_test_families"])
    assert "import_boundary_tests_for_exact_phase_8_1_file_touch_map" in families
    assert "typed_input_acceptance_tests" in families
    assert "natural_language_raw_chat_rejection_tests" in families
    assert "non_executable_candidate_output_tests" in families
    assert "authority_free_output_tests" in families
    assert "approval_bypass_wording_rejection_tests" in families
    assert "guardiandecision_non_creation_tests" in families
    assert "intentenvelope_non_creation_tests" in families
    assert "sparkbot_coupling_rejection_tests" in families
    assert "side_effect_rejection_tests" in families


def test_required_negative_cases_block_runtime_escape_paths() -> None:
    negative = set(_load_json(PHASE_FIXTURE_PATH)["required_negative_cases"])
    assert "raw_natural_language_prompts" in negative
    assert "shell_command_requests" in negative
    assert "browser_or_network_requests" in negative
    assert "file_mutation_requests" in negative
    assert "model_call_requests" in negative
    assert "tool_call_requests" in negative
    assert "sparkbot_import_or_runtime_coupling" in negative
    assert "real_intentenvelope_creation" in negative
    assert "real_guardiandecision_creation" in negative
    assert "approval_enforcement" in negative
    assert "execution" in negative
    assert "audit_persistence" in negative
    assert "robotics_or_physical_world_requests" in negative
    assert "operator_admin_phil_trusted_bypass_wording" in negative


def test_limited_positive_cases_are_non_executable_candidate_metadata_only() -> None:
    positive = set(_load_json(PHASE_FIXTURE_PATH)["limited_positive_cases"])
    assert "typed_synthetic_metadata_input_accepted" in positive
    assert "candidate_metadata_returned" in positive
    assert "candidate_provenance_retained" in positive
    assert "candidate_output_marked_non_executable" in positive
    assert "candidate_output_marked_not_approved_and_not_execution_ready" in positive
    assert "future_guardian_review_boundary_refs_retained" in positive


def test_future_validation_commands_include_full_and_forbidden_path_checks() -> None:
    commands = set(_load_json(PHASE_FIXTURE_PATH)["future_validation_commands"])
    assert "targeted_tests_for_every_touched_file" in commands
    assert "all_phase_8_gate_tests" in commands
    assert "python -m pytest -q" in commands
    assert "python -m compileall lima" in commands
    assert "git diff --check" in commands
    assert "explicit_forbidden_path_review" in commands


def test_doc_says_runtime_tests_are_not_implemented_yet() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "does not implement those runtime tests yet" in phase_doc
    assert "does not implement runtime behavior" in phase_doc
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "Runtime implementation remains blocked" in phase_doc


def test_phase_five_runtime_bridge_remains_gated() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase_5_runtime_bridge_remains_gated"] is True
    assert fixture["next_phase"] == "phase_8_3_rollback_audit_proof_plan"


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


def test_no_phase_eight_two_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_8_2*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_8_2*"))
