"""Static checks for Phase 20.3 acceptance test and rollback plan."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_20_3_ACCEPTANCE_TEST_AND_ROLLBACK_PLAN.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_20_3_acceptance_test_and_rollback_plan.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_docs_tests_fixtures_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "20.3"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False


def test_future_acceptance_tests_cover_provenance_and_invariants() -> None:
    tests = set(_load_json(PHASE_FIXTURE_PATH)["future_acceptance_tests"])
    assert "candidate_construction_rejects_missing_provenance" in tests
    assert "candidate_construction_rejects_empty_provenance" in tests
    assert "candidate_validation_marks_missing_provenance_invalid" in tests
    assert "status_normalization_preserves_valid_provenance" in tests
    assert "provenance_hardening_preserves_non_executing_invariants" in tests
    assert "provenance_hardening_never_sets_approval_state_approved" in tests


def test_future_acceptance_tests_cover_boundary_regressions() -> None:
    tests = set(_load_json(PHASE_FIXTURE_PATH)["future_acceptance_tests"])
    assert "stale_or_replayed_candidates_remain_blocked_or_invalid" in tests
    assert (
        "operator_admin_phil_trusted_urgent_override_approve_wording_does_not_bypass_safety"
        in tests
    )
    assert "forbidden_integrations_and_side_effects_are_unreachable" in tests
    assert "only_phase_20_2_eligible_runtime_files_changed" in tests


def test_rollback_audit_proof_requires_no_side_effect_systems() -> None:
    proof = set(_load_json(PHASE_FIXTURE_PATH)["rollback_audit_proof"])
    assert "no_database_migration_queue_worker_daemon_subprocess_thread_external_call_or_persistence" in proof
    assert "rollback_is_clean_revert_of_eligible_runtime_files_and_phase_21_artifacts" in proof
    assert "no_runtime_files_outside_phase_20_2_eligible_list" in proof
    assert "phase_5_humaninput_runtime_bridge_remains_gated" in proof


def test_phase_document_does_not_approve_phase_twenty_one() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "Phase 20.3 does not approve Phase 21" in phase_doc
    assert "only `lima/kernel/intake_candidate.py` and `lima/kernel/candidate_status.py`" in phase_doc
    assert "no database migration, queue, worker, daemon, subprocess, thread" in phase_doc


def test_boundary_results_show_no_forbidden_changes() -> None:
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
    assert boundary["physical_world_action_added"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True


def test_no_phase_twenty_three_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_20_3*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_20_3*"))
