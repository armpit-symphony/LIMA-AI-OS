"""Phase 47.1 static acceptance-test implementation checklist tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_47_1_STATIC_ACCEPTANCE_TEST_IMPLEMENTATION_CHECKLIST.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_47_1_static_acceptance_test_implementation_checklist.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_phase_47_1_fixture_exists_and_is_docs_only_checklist_lane() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "47.1"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["checklist_only"] is True
    assert fixture["runtime_test_harness_created"] is False
    assert fixture["actual_acceptance_tests_created"] is False
    assert fixture["executable_acceptance_tests_created"] is False


def test_phase_47_1_required_shared_sequence_is_explicit_and_ordered() -> None:
    sequence = _load_json(PHASE_FIXTURE_PATH)["required_shared_sequence"]
    assert sequence == [
        "ConsumerRequest",
        "TypedIntentEnvelope_or_TaskIntent",
        "CandidatePreview",
        "RuntimeStateSnapshot",
    ]


def test_phase_47_1_required_refs_and_profile_fields_are_explicit() -> None:
    refs = set(_load_json(PHASE_FIXTURE_PATH)["required_sequence_refs"])
    assert "consumer_profile" in refs
    assert "embodiment_profile" in refs
    assert "approval_posture" in refs
    assert "evidence_ref" in refs

    requirements = _load_json(PHASE_FIXTURE_PATH)["future_fixture_requirements"]
    assert requirements["consumer_profile_structured_required"] is True
    assert requirements["embodiment_profile_required_on_every_candidate_preview"] is True


def test_phase_47_1_invariant_names_and_values_match_alignment_brief() -> None:
    invariants = _load_json(PHASE_FIXTURE_PATH)["required_invariants"]
    assert invariants["preview_only"] is True
    assert invariants["non_authoritative"] is True
    assert invariants["safe_by_default"] is True
    assert invariants["execution_allowed"] is False
    assert invariants["side_effects_permitted"] is False
    assert invariants["approval_granted"] is False
    assert invariants["dispatch_allowed"] is False
    assert invariants["persistence_allowed"] is False
    assert invariants["model_provider_calls_allowed"] is False
    assert invariants["connector_calls_allowed"] is False
    assert invariants["runtime_active"] is False
    assert invariants["human_input_bridge_active"] is False
    assert invariants["live_adapter_active"] is False
    assert invariants["robotics_allowed"] is False
    assert invariants["physical_world_allowed"] is False
    assert invariants["runtime_test_harness_active"] is False
    assert invariants["guardian_decision_created"] is False
    assert invariants["adapter_calls_allowed"] is False
    assert invariants["tool_calls_allowed"] is False
    assert invariants["driver_calls_allowed"] is False
    assert invariants["audit_storage_written"] is False


def test_phase_47_1_runtime_ladder_and_mock_safe_states_are_explicit() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    ladder = fixture["runtime_ladder_vocabulary"]
    assert "preview_only" in ladder
    assert "explain_plan" in ladder
    assert "approval_required" in ladder
    assert "audited" in ladder
    assert "blocked" in ladder
    assert "deferred" in ladder

    safe_states = set(fixture["mock_safe_active_states"])
    assert safe_states == {"preview_only", "explain_plan", "blocked", "deferred"}


def test_phase_47_1_guardian_ownership_boundary_is_explicit() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["guardian_ownership_boundary"]
    assert boundary["lima_describes_approval_posture_only"] is True
    assert boundary["guardian_owns_real_approval_state"] is True
    assert boundary["consumer_displays_posture_only"] is True
    assert boundary["adapter_execution_requires_future_explicit_handoff_approval"] is True


def test_phase_47_1_forbidden_scope_keeps_runtime_and_action_surfaces_blocked() -> None:
    forbidden = set(_load_json(PHASE_FIXTURE_PATH)["forbidden_scope"])
    assert "runtime_implementation" in forbidden
    assert "lima_changes" in forbidden
    assert "tests_support_changes" in forbidden
    assert "runtime_test_harness_creation_or_activation" in forbidden
    assert "guardian_decision_creation" in forbidden
    assert "execution_dispatch_persistence" in forbidden
    assert "model_tool_driver_adapter_calls" in forbidden
    assert "robotics_physical_world_behavior" in forbidden


def test_phase_47_1_stays_out_of_runtime_and_tests_support_paths() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["runtime_behavior_changed"] is False
    assert not list((REPO_ROOT / "lima").rglob("*phase_47_1*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_47_1*"))


def test_phase_47_1_doc_declares_docs_only_checklist_and_runtime_block() -> None:
    text = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "docs/tests/fixtures-only static checklist lane" in text
    assert "does not create or activate a runtime test harness" in text
    assert "does not implement runtime bridge behavior" in text
