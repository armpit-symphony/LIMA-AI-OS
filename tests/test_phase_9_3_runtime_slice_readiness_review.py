"""Readiness checks for the Phase 9.2 non-executing runtime slice."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from lima.kernel.intake_candidate import IntakeCandidateError, build_intake_candidate


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_9_3_RUNTIME_SLICE_READINESS_REVIEW.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_9_3_runtime_slice_readiness_review.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def _intake(**overrides: Any) -> dict[str, Any]:
    intake: dict[str, Any] = {
        "synthetic": True,
        "test_only": True,
        "intake_id": "phase-9-3-intake",
        "source": "readiness_shell",
        "source_channel": "readiness_channel",
        "operator_intent": "review the candidate coordinator",
        "normalized_request": "review_candidate_coordinator",
        "requested_action": "review_metadata",
        "action_category": "informational",
        "freshness": "fresh",
        "replay_status": "not_replayed",
        "provenance": {"lineage_seed": "phase-9-3-lineage"},
    }
    intake.update(overrides)
    return intake


def test_phase_declares_readiness_review_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "9.3"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False
    assert fixture["readiness_finding"] == "ready_for_phase_9_4_audit_archive_closeout_only"


def test_reviewed_artifacts_include_phase_nine_runtime_slice() -> None:
    artifacts = set(_load_json(PHASE_FIXTURE_PATH)["reviewed_artifacts"])
    assert "lima/kernel/__init__.py" in artifacts
    assert "lima/kernel/intake_candidate.py" in artifacts
    assert "tests/test_phase_9_2_non_executing_kernel_intake_to_candidate_coordinator_implementation.py" in artifacts


def test_readiness_scope_is_closeout_only_not_runtime_expansion() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert set(fixture["ready_for"]) == {
        "phase_9_4_runtime_slice_audit_archive_closeout",
        "further_non_runtime_review",
    }
    not_ready = set(fixture["not_ready_for"])
    assert "runtime_expansion" in not_ready
    assert "humaninput_runtime_bridge_behavior" in not_ready
    assert "intentcompiler_runtime_behavior" in not_ready
    assert "guardiandecision_runtime_behavior" in not_ready
    assert "approval_enforcement" in not_ready
    assert "execution" in not_ready
    assert "audit_persistence" in not_ready
    assert "sparkbot_wiring" in not_ready
    assert "shell_browser_network_file_mutation_robotics_physical_world_side_effects" in not_ready


def test_confirmed_properties_match_runtime_slice_behavior() -> None:
    properties = _load_json(PHASE_FIXTURE_PATH)["confirmed_properties"]
    assert properties["accepts_only_synthetic_already_normalized_intake_metadata"] is True
    assert properties["rejects_raw_humaninput_like_payloads"] is True
    assert properties["returns_candidate_metadata_only"] is True
    assert properties["candidate_always_non_executable"] is True
    assert properties["execution_allowed_always_false"] is True
    assert properties["side_effects_allowed_always_false"] is True
    assert properties["approval_state_never_approved"] is True
    assert properties["provenance_preserved"] is True
    assert properties["stale_replayed_malformed_unknown_intake_fails_closed"] is True
    assert properties["intent_envelope_created"] is False
    assert properties["guardian_decision_created"] is False
    assert properties["phase_5_humaninput_runtime_bridge_remains_gated"] is True


def test_runtime_slice_still_returns_non_executing_candidate() -> None:
    candidate = build_intake_candidate(_intake())
    assert candidate["executable"] is False
    assert candidate["execution_allowed"] is False
    assert candidate["side_effects_allowed"] is False
    assert candidate["approved"] is False
    assert candidate["approval_state"] == "proposed"
    assert candidate["intent_envelope_created"] is False
    assert candidate["guardian_decision_created"] is False


def test_runtime_slice_still_fails_closed_for_raw_and_risky_input() -> None:
    with pytest.raises(IntakeCandidateError):
        build_intake_candidate(_intake(raw_text="run this now"))
    risky = build_intake_candidate(_intake(action_category="shell", requested_action="run_shell"))
    assert risky["approval_state"] == "approval_required"
    assert risky["execution_allowed"] is False
    assert risky["approved"] is False


def test_phase_doc_says_no_runtime_expansion_is_approved() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "does not modify runtime code" in phase_doc
    assert "ready for Phase 9.4 audit/archive closeout" in phase_doc
    assert "not ready for runtime expansion" in phase_doc
    assert "No Phase 10 or broader runtime expansion is approved" in phase_doc


def test_boundary_results_show_no_new_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["files_under_lima_modified_by_phase_9_3"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_added_by_phase_9_3"] is False
    assert boundary["runtime_behavior_remains_non_executing"] is True
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["live_adapter_added"] is False
    assert boundary["humaninput_runtime_bridge_added"] is False
    assert boundary["intentcompiler_runtime_changed"] is False
    assert boundary["guardiandecision_runtime_changed"] is False
    assert boundary["approval_enforcement_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False


def test_no_phase_nine_three_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_9_3*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_9_3*"))
