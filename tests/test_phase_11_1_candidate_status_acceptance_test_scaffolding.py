"""Static checks for Phase 11.1 acceptance test scaffolding."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_11_1_CANDIDATE_STATUS_ACCEPTANCE_TEST_SCAFFOLDING.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_11_1_candidate_status_acceptance_test_scaffolding.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_docs_tests_fixtures_only_scaffolding() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "11.1"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False


def test_phase_eleven_two_status_tests_are_scaffolded() -> None:
    tests = set(_load_json(PHASE_FIXTURE_PATH)["phase_11_2_required_test_families"])
    assert "valid_phase_9_style_candidates_normalize_to_safe_status" in tests
    assert "allowed_statuses_limited_to_proposed_needs_review_blocked" in tests
    assert "unknown_status_normalizes_to_blocked_or_needs_review" in tests
    assert "approved_status_never_survives_normalization" in tests
    assert "execution_allowed_remains_false" in tests
    assert "side_effects_allowed_remains_false" in tests
    assert "provenance_preserved" in tests


def test_phase_eleven_three_validation_tests_are_scaffolded() -> None:
    tests = set(_load_json(PHASE_FIXTURE_PATH)["phase_11_3_required_test_families"])
    assert "malformed_candidates_rejected_or_marked_invalid_safely" in tests
    assert "missing_execution_allowed_fails_closed" in tests
    assert "missing_side_effects_allowed_fails_closed" in tests
    assert "execution_allowed_true_fails_closed" in tests
    assert "side_effects_allowed_true_fails_closed" in tests
    assert "approval_state_approved_fails_closed" in tests
    assert "stale_or_replayed_candidates_remain_blocked_or_invalid" in tests
    assert "validation_cannot_approve_execute_persist_or_dispatch" in tests


def test_shared_boundary_tests_are_scaffolded() -> None:
    tests = set(_load_json(PHASE_FIXTURE_PATH)["shared_required_test_families"])
    assert "no_sparkbot_import_or_wiring" in tests
    assert "no_humaninput_runtime_bridge" in tests
    assert "no_live_adapter" in tests
    assert "no_intentcompiler_runtime_behavior_changes" in tests
    assert "no_guardiandecision_runtime_behavior_changes" in tests
    assert "no_shell_browser_network_file_mutation_robotics_physical_world_behavior" in tests
    assert "only_phase_10_2_eligible_runtime_files_touched" in tests
    assert "phase_5_runtime_bridge_remains_gated" in tests


def test_phase_document_does_not_implement_runtime_behavior() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "does not implement candidate status normalization or candidate validation" in phase_doc
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "does not add `lima/kernel/candidate_status.py`" in phase_doc


def test_next_phase_is_candidate_status_implementation() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["next_phase"] == "phase_11_2_candidate_status_normalization_runtime_implementation"


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["helper_behavior_changed"] is False
    assert boundary["candidate_status_added"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["humaninput_runtime_bridge_added"] is False
    assert boundary["live_adapter_added"] is False
    assert boundary["intentcompiler_runtime_behavior_changed"] is False
    assert boundary["guardiandecision_runtime_behavior_changed"] is False
    assert boundary["approval_enforcement_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False


def test_no_phase_eleven_one_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_11_1*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_11_1*"))
