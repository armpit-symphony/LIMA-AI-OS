"""Static checks for Phase 6.2 IntentEnvelope and GuardianDecision lifecycle boundary mapping."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_6_2_INTENTENVELOPE_GUARDIANDECISION_LIFECYCLE_BOUNDARY_MAP.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_6_2_intentenvelope_guardiandecision_lifecycle_boundary_map.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_declares_lifecycle_boundary_map_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "6.2"
    assert fixture["non_runtime"] is True
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["lifecycle_boundary_map_only"] is True


def test_intentenvelope_candidate_lifecycle_blocks_runtime_paths() -> None:
    lifecycle = _load_json(PHASE_FIXTURE_PATH)["intentenvelope_candidate_lifecycle"]
    assert lifecycle == [
        "humaninput_context_referenced",
        "candidate_metadata_drafted",
        "provenance_lineage_attached",
        "risk_confidence_metadata_proposed",
        "approval_state_described",
        "guardian_review_readiness_recorded",
        "compile_dispatch_execution_persistence_blocked",
    ]


def test_guardiandecision_lifecycle_remains_future_authority_only() -> None:
    lifecycle = _load_json(PHASE_FIXTURE_PATH)["guardiandecision_lifecycle"]
    assert "review_request_metadata_prepared" in lifecycle
    assert "policy_risk_trust_context_referenced" in lifecycle
    assert "decision_states_described" in lifecycle
    assert "approval_semantics_reserved_for_future_authority" in lifecycle
    assert "enforcement_execution_driver_handoff_audit_persistence_blocked" in lifecycle


def test_boundary_rules_prevent_candidates_from_becoming_permission() -> None:
    rules = _load_json(PHASE_FIXTURE_PATH)["boundary_rules"]
    assert rules["humaninput_is_intent_context_not_execution_permission"] is True
    assert rules["intentenvelope_candidate_not_command"] is True
    assert rules["intentenvelope_candidate_not_authorization"] is True
    assert rules["intentenvelope_candidate_not_approval"] is True
    assert rules["intentenvelope_candidate_not_execution"] is True
    assert rules["operator_admin_phil_trusted_wording_never_bypasses_approval"] is True


def test_guardian_and_audit_boundaries_are_descriptive_only() -> None:
    rules = _load_json(PHASE_FIXTURE_PATH)["boundary_rules"]
    assert rules["guardiandecision_future_authority_not_implemented"] is True
    assert rules["approval_state_metadata_descriptive_only"] is True
    assert rules["audit_spine_memory_refs_lineage_planning_only"] is True
    assert rules["driver_tool_handoff_blocked_until_future_guardian_decision"] is True


def test_ready_only_for_phase_six_three_boundary_planning() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["ready_for"] == [
        "phase_6_3_docs_tests_fixtures_only_approval_audit_memory_boundary_planning"
    ]
    assert "runtime_behavior" in fixture["not_ready_for"]
    assert "real_intentcompiler" in fixture["not_ready_for"]
    assert "real_guardiandecision" in fixture["not_ready_for"]
    assert "audit_persistence" in fixture["not_ready_for"]


def test_doc_keeps_runtime_behavior_and_decisions_blocked() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "does not implement runtime behavior" in phase_doc
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "IntentEnvelope candidate metadata is not a command" in phase_doc
    assert "does not create, evaluate, enforce, persist, or execute GuardianDecision behavior" in phase_doc
    assert "Runtime implementation remains blocked" in phase_doc


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["runtime_behavior_added"] is False
    assert boundary["files_under_lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["helper_behavior_changed"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["intentcompiler_runtime_changed"] is False
    assert boundary["guardiandecision_runtime_changed"] is False
    assert boundary["execution_added"] is False
    assert boundary["physical_world_action_added"] is False


def test_no_phase_six_two_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_6_2*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_6_2*"))
