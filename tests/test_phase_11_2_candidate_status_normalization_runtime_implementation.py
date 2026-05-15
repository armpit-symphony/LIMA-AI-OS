"""Runtime and static checks for Phase 11.2 candidate status normalization."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from lima.kernel import ALLOWED_CANDIDATE_STATUSES, normalize_candidate_status
from lima.kernel.intake_candidate import build_intake_candidate


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_11_2_CANDIDATE_STATUS_NORMALIZATION_RUNTIME_IMPLEMENTATION.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_11_2_candidate_status_normalization_runtime_implementation.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def _intake(**overrides: Any) -> dict[str, Any]:
    intake = {
        "synthetic": True,
        "test_only": True,
        "intake_id": "intake-11-2",
        "source": "test_shell",
        "source_channel": "test_room",
        "operator_intent": "summarize a harmless status note",
        "normalized_request": "summarize status note",
        "requested_action": "summarize",
        "action_category": "informational",
        "provenance": {"fixture": "phase_11_2", "lineage_seed": "seed-11-2"},
    }
    intake.update(overrides)
    return intake


def test_phase_fixture_lists_only_eligible_runtime_files() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "11.2"
    assert fixture["runtime_code_modified"] is True
    assert fixture["runtime_files_touched"] == [
        "lima/kernel/candidate_status.py",
        "lima/kernel/__init__.py",
    ]
    assert set(fixture["runtime_files_touched"]).issubset(set(fixture["eligible_runtime_files"]))


def test_valid_candidate_normalizes_to_safe_proposed_status() -> None:
    candidate = build_intake_candidate(_intake())
    normalized = normalize_candidate_status(candidate)
    assert normalized["candidate_status"] == "proposed"
    assert normalized["approval_state"] == "proposed"
    assert normalized["executable"] is False
    assert normalized["execution_allowed"] is False
    assert normalized["side_effects_allowed"] is False
    assert normalized["approved"] is False
    assert normalized["provenance"] == candidate["provenance"]


def test_risky_candidate_normalizes_to_needs_review_without_authority() -> None:
    candidate = build_intake_candidate(_intake(action_category="shell", requested_action="run_shell"))
    normalized = normalize_candidate_status(candidate)
    assert normalized["candidate_status"] == "needs_review"
    assert normalized["approval_state"] == "approval_required"
    assert normalized["execution_allowed"] is False
    assert normalized["side_effects_allowed"] is False
    assert normalized["approved"] is False


def test_unknown_candidate_status_blocks_safely() -> None:
    candidate = build_intake_candidate(_intake())
    candidate["candidate_status"] = "trusted_admin_ready"
    normalized = normalize_candidate_status(candidate)
    assert normalized["candidate_status"] == "blocked"
    assert normalized["approval_state"] == "blocked"
    assert normalized["blocked_reason"] == "unknown_candidate_status_not_execution_ready"


def test_approved_status_never_survives_normalization() -> None:
    candidate = build_intake_candidate(_intake())
    candidate["approval_state"] = "approved"
    candidate["approved"] = True
    normalized = normalize_candidate_status(candidate)
    assert normalized["candidate_status"] == "blocked"
    assert normalized["approval_state"] == "blocked"
    assert normalized["approved"] is False
    assert normalized["execution_allowed"] is False
    assert normalized["side_effects_allowed"] is False


def test_execution_or_side_effect_flags_are_forced_blocked_and_false() -> None:
    executable_candidate = build_intake_candidate(_intake())
    executable_candidate["execution_allowed"] = True
    normalized_execution = normalize_candidate_status(executable_candidate)
    assert normalized_execution["candidate_status"] == "blocked"
    assert normalized_execution["execution_allowed"] is False
    assert normalized_execution["blocked_reason"] == "execution_not_allowed_for_candidate"

    side_effect_candidate = build_intake_candidate(_intake())
    side_effect_candidate["side_effects_allowed"] = True
    normalized_side_effect = normalize_candidate_status(side_effect_candidate)
    assert normalized_side_effect["candidate_status"] == "blocked"
    assert normalized_side_effect["side_effects_allowed"] is False
    assert normalized_side_effect["blocked_reason"] == "side_effects_not_allowed_for_candidate"


def test_stale_and_replayed_candidates_block_safely() -> None:
    candidate = build_intake_candidate(_intake())
    candidate["freshness"] = "stale"
    stale = normalize_candidate_status(candidate)
    assert stale["candidate_status"] == "blocked"
    assert stale["blocked_reason"] == "stale_candidate_not_execution_ready"

    candidate = build_intake_candidate(_intake())
    candidate["replay_status"] = "replayed"
    replayed = normalize_candidate_status(candidate)
    assert replayed["candidate_status"] == "blocked"
    assert replayed["blocked_reason"] == "replayed_candidate_not_execution_ready"


def test_allowed_statuses_are_limited_to_non_authoritative_values() -> None:
    assert ALLOWED_CANDIDATE_STATUSES == frozenset({"proposed", "needs_review", "blocked"})
    assert "approved" not in ALLOWED_CANDIDATE_STATUSES


def test_no_forbidden_runtime_language_or_imports_are_added() -> None:
    source = (REPO_ROOT / "lima" / "kernel" / "candidate_status.py").read_text(encoding="utf-8")
    forbidden_terms = [
        "subprocess",
        "requests",
        "socket",
        "webbrowser",
        "open(",
        "Sparkbot",
        "IntentCompiler",
        "GuardianDecision",
        "dispatch(",
        "approve(",
        "persist(",
    ]
    for term in forbidden_terms:
        assert term not in source


def test_phase_document_records_static_absence_test_adjustment() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert "Static Test Adjustment" in phase_doc
    assert fixture["static_test_adjustment"]["phase_10_5_absence_assertion_updated"] is True
    assert fixture["static_test_adjustment"]["phase_11_0_absence_assertion_updated"] is True


def test_boundary_results_show_no_forbidden_behavior() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["files_outside_phase_10_2_runtime_list_changed"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_remains_non_executing"] is True
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
