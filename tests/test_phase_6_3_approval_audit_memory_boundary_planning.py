"""Static checks for Phase 6.3 approval, audit, and memory boundary planning."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_6_3_APPROVAL_AUDIT_MEMORY_BOUNDARY_PLANNING.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_6_3_approval_audit_memory_boundary_planning.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_declares_approval_audit_memory_boundary_planning_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "6.3"
    assert fixture["non_runtime"] is True
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["approval_audit_memory_boundary_planning_only"] is True


def test_approval_boundary_is_descriptive_and_non_authorizing() -> None:
    approval = _load_json(PHASE_FIXTURE_PATH)["approval_boundary"]
    assert approval["descriptive_states_only"] == [
        "proposed",
        "approval_required",
        "denied",
        "blocked",
        "ready_for_review",
    ]
    assert approval["approval_enforcement_implemented"] is False
    assert approval["authorization_created"] is False
    assert approval["breakglass_opened"] is False
    assert approval["execution_approved"] is False
    assert approval["guardian_decision_future_authority"] is True


def test_audit_and_spine_boundaries_do_not_persist_or_append() -> None:
    audit_spine = _load_json(PHASE_FIXTURE_PATH)["audit_spine_boundary"]
    assert audit_spine["lineage_planning_only"] is True
    assert audit_spine["event_ids_reference_only"] is True
    assert audit_spine["provenance_links_reference_only"] is True
    assert audit_spine["retention_policy_reference_only"] is True
    assert audit_spine["review_evidence_reference_only"] is True
    assert audit_spine["audit_events_created"] is False
    assert audit_spine["ledger_appended"] is False
    assert audit_spine["audit_persistence_added"] is False


def test_memory_boundary_is_reference_only_without_io() -> None:
    memory = _load_json(PHASE_FIXTURE_PATH)["memory_boundary"]
    assert memory["memory_refs_reference_only"] is True
    assert memory["context_refs_reference_only"] is True
    assert memory["recall_constraints_reference_only"] is True
    assert memory["privacy_markings_reference_only"] is True
    assert memory["memory_read_added"] is False
    assert memory["memory_write_added"] is False
    assert memory["embedding_update_added"] is False
    assert memory["summary_storage_added"] is False


def test_boundary_rules_prevent_references_from_becoming_behavior() -> None:
    rules = _load_json(PHASE_FIXTURE_PATH)["boundary_rules"]
    assert rules["approval_refs_are_not_enforcement"] is True
    assert rules["audit_refs_are_not_persistence"] is True
    assert rules["memory_refs_are_not_memory_io"] is True
    assert rules["spine_refs_are_not_ledger_writes"] is True
    assert rules["intentenvelope_candidates_non_executable"] is True
    assert rules["side_effecting_actions_blocked"] is True


def test_ready_only_for_phase_six_four_closeout() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["ready_for"] == [
        "phase_6_4_docs_tests_fixtures_only_roadmap_gate_next_lane_closeout"
    ]
    assert "approval_enforcement" in fixture["not_ready_for"]
    assert "audit_persistence" in fixture["not_ready_for"]
    assert "memory_io" in fixture["not_ready_for"]
    assert "spine_ledger_write" in fixture["not_ready_for"]


def test_doc_keeps_approval_audit_memory_behavior_blocked() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "does not implement runtime behavior" in phase_doc
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "Approval state remains descriptive metadata" in phase_doc
    assert "does not create audit events" in phase_doc
    assert "does not read memory, write memory" in phase_doc
    assert "Runtime implementation remains blocked" in phase_doc


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["runtime_behavior_added"] is False
    assert boundary["files_under_lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["helper_behavior_changed"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["approval_enforcement_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["memory_io_added"] is False
    assert boundary["spine_ledger_write_added"] is False
    assert boundary["physical_world_action_added"] is False


def test_no_phase_six_three_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_6_3*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_6_3*"))
