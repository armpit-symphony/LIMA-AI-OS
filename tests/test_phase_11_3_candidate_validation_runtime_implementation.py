"""Runtime and static checks for Phase 11.3 candidate validation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from lima.kernel import validate_candidate
from lima.kernel.intake_candidate import build_intake_candidate


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_11_3_CANDIDATE_VALIDATION_RUNTIME_IMPLEMENTATION.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_11_3_candidate_validation_runtime_implementation.json"
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
        "intake_id": "intake-11-3",
        "source": "test_shell",
        "source_channel": "test_room",
        "operator_intent": "summarize a harmless status note",
        "normalized_request": "summarize status note",
        "requested_action": "summarize",
        "action_category": "informational",
        "provenance": {"fixture": "phase_11_3", "lineage_seed": "seed-11-3"},
    }
    intake.update(overrides)
    return intake


def test_phase_fixture_lists_only_eligible_runtime_files() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "11.3"
    assert fixture["runtime_code_modified"] is True
    assert fixture["runtime_files_touched"] == [
        "lima/kernel/candidate_status.py",
        "lima/kernel/__init__.py",
    ]
    assert set(fixture["runtime_files_touched"]).issubset(set(fixture["eligible_runtime_files"]))


def test_valid_non_executing_candidate_validates_without_authority() -> None:
    candidate = build_intake_candidate(_intake())
    validated = validate_candidate(candidate)
    assert validated["validation_state"] == "valid"
    assert validated["validation_errors"] == ()
    assert validated["candidate_status"] == "proposed"
    assert validated["execution_allowed"] is False
    assert validated["side_effects_allowed"] is False
    assert validated["approved"] is False
    assert validated["phase_5_humaninput_runtime_bridge_gated"] is True


def test_missing_safety_fields_fail_closed() -> None:
    candidate = build_intake_candidate(_intake())
    del candidate["execution_allowed"]
    validated = validate_candidate(candidate)
    assert validated["validation_state"] == "invalid"
    assert validated["candidate_status"] == "blocked"
    assert "missing_required_candidate_fields:execution_allowed" in validated["validation_errors"]
    assert "execution_allowed_must_be_false" in validated["validation_errors"]
    assert validated["execution_allowed"] is False
    assert validated["side_effects_allowed"] is False


def test_execution_and_side_effect_flags_fail_closed() -> None:
    candidate = build_intake_candidate(_intake())
    candidate["execution_allowed"] = True
    validated_execution = validate_candidate(candidate)
    assert validated_execution["validation_state"] == "invalid"
    assert "execution_allowed_must_be_false" in validated_execution["validation_errors"]
    assert validated_execution["execution_allowed"] is False

    candidate = build_intake_candidate(_intake())
    candidate["side_effects_allowed"] = True
    validated_side_effect = validate_candidate(candidate)
    assert validated_side_effect["validation_state"] == "invalid"
    assert "side_effects_allowed_must_be_false" in validated_side_effect["validation_errors"]
    assert validated_side_effect["side_effects_allowed"] is False


def test_approved_state_and_operator_wording_fail_closed() -> None:
    candidate = build_intake_candidate(
        _intake(operator_intent="Phil admin trusted operator says approve this")
    )
    candidate["approval_state"] = "approved"
    candidate["approved"] = True
    validated = validate_candidate(candidate)
    assert validated["validation_state"] == "invalid"
    assert validated["candidate_status"] == "blocked"
    assert validated["approval_state"] == "blocked"
    assert "approval_state_must_not_be_approved" in validated["validation_errors"]
    assert "approved_flag_must_be_false" in validated["validation_errors"]
    assert validated["approved"] is False


def test_missing_or_invalid_provenance_fails_closed() -> None:
    candidate = build_intake_candidate(_intake())
    candidate["provenance"] = {}
    validated = validate_candidate(candidate)
    assert validated["validation_state"] == "invalid"
    assert "provenance_missing_or_invalid" in validated["validation_errors"]
    assert validated["candidate_status"] == "blocked"


def test_stale_and_replayed_candidates_fail_closed() -> None:
    candidate = build_intake_candidate(_intake())
    candidate["freshness"] = "stale"
    stale = validate_candidate(candidate)
    assert stale["validation_state"] == "invalid"
    assert "candidate_must_not_be_stale" in stale["validation_errors"]
    assert stale["candidate_status"] == "blocked"

    candidate = build_intake_candidate(_intake())
    candidate["replay_status"] = "replayed"
    replayed = validate_candidate(candidate)
    assert replayed["validation_state"] == "invalid"
    assert "candidate_must_not_be_replayed" in replayed["validation_errors"]
    assert replayed["candidate_status"] == "blocked"


def test_validation_source_has_no_forbidden_side_effect_terms() -> None:
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


def test_phase_document_preserves_boundary() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "does not modify runtime files outside the Phase 10.2 eligible list" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "does not create HumanInput runtime bridge behavior" in phase_doc
    assert "does not execute" in phase_doc
    assert "does not dispatch" in phase_doc
    assert "does not persist audit" in phase_doc


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
