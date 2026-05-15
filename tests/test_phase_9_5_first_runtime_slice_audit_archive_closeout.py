"""Archive checks for Phase 9.5 first runtime slice closeout."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from lima.kernel.intake_candidate import IntakeCandidateError, build_intake_candidate


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_9_5_FIRST_RUNTIME_SLICE_AUDIT_ARCHIVE_CLOSEOUT.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_9_5_first_runtime_slice_audit_archive_closeout.json"
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
        "intake_id": "phase-9-5-intake",
        "source": "archive_shell",
        "source_channel": "archive_channel",
        "operator_intent": "archive Phase 9",
        "normalized_request": "archive_phase_9",
        "requested_action": "archive_metadata",
        "action_category": "informational",
        "freshness": "fresh",
        "replay_status": "not_replayed",
        "provenance": {"lineage_seed": "phase-9-5-lineage"},
    }
    intake.update(overrides)
    return intake


def test_phase_declares_docs_tests_fixtures_only_closeout() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "9.5"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False
    assert fixture["phase_10_requires_explicit_phil_approval"] is True


def test_phase_nine_zero_through_nine_four_are_listed_complete() -> None:
    assert _load_json(PHASE_FIXTURE_PATH)["completed_phase_9_scope"] == [
        "phase_9_0_runtime_slice_preflight_audit_eligible_file_confirmation",
        "phase_9_1_runtime_slice_acceptance_test_scaffolding",
        "phase_9_2_non_executing_kernel_intake_to_candidate_coordinator_implementation",
        "phase_9_3_runtime_slice_readiness_review",
        "phase_9_4_phase_9_runtime_slice_audit_archive_closeout",
    ]


def test_only_approved_phase_eight_one_runtime_files_were_touched() -> None:
    assert _load_json(PHASE_FIXTURE_PATH)["approved_runtime_files_touched"] == [
        "lima/kernel/__init__.py",
        "lima/kernel/intake_candidate.py",
    ]


def test_phase_nine_added_expected_artifacts_only() -> None:
    added = set(_load_json(PHASE_FIXTURE_PATH)["phase_9_added"])
    assert added == {
        "first_non_executing_kernel_intake_to_candidate_coordinator",
        "acceptance_tests",
        "docs",
        "fixtures",
        "static_tests",
        "roadmap_state_updates",
    }


def test_phase_nine_did_not_add_forbidden_surfaces() -> None:
    not_added = set(_load_json(PHASE_FIXTURE_PATH)["phase_9_not_added"])
    assert "humaninput_runtime_bridge" in not_added
    assert "sparkbot_wiring_or_imports" in not_added
    assert "live_adapter" in not_added
    assert "intentcompiler_behavior_change" in not_added
    assert "guardiandecision_behavior_change" in not_added
    assert "approval_enforcement" in not_added
    assert "execution" in not_added
    assert "audit_persistence" in not_added
    assert "dispatch" in not_added
    assert "shell_browser_network_file_mutation_robotics_physical_world_behavior" in not_added
    assert "tests_support_changes" in not_added


def test_candidate_safety_guarantees_are_preserved() -> None:
    guarantees = _load_json(PHASE_FIXTURE_PATH)["candidate_safety_guarantees"]
    assert guarantees["execution_allowed_always_false"] is True
    assert guarantees["side_effects_allowed_always_false"] is True
    assert guarantees["approval_state_never_approved"] is True
    assert guarantees["unknown_input_blocked"] is True
    assert guarantees["malformed_input_rejected_or_blocked_safely"] is True
    assert guarantees["stale_or_replayed_input_blocked"] is True
    assert guarantees["provenance_preserved"] is True
    assert guarantees["operator_admin_phil_trusted_wording_bypasses_safety"] is False
    assert guarantees["phase_5_runtime_bridge_remains_gated"] is True


def test_runtime_candidate_still_has_non_executing_flags() -> None:
    candidate = build_intake_candidate(_intake())
    assert candidate["execution_allowed"] is False
    assert candidate["side_effects_allowed"] is False
    assert candidate["approval_state"] != "approved"
    assert candidate["approved"] is False
    assert candidate["phase_5_humaninput_runtime_bridge_gated"] is True


def test_runtime_candidate_still_blocks_unknown_and_malformed_inputs() -> None:
    unknown = build_intake_candidate(_intake(action_category="unknown_kind"))
    assert unknown["approval_state"] == "blocked"
    assert unknown["execution_allowed"] is False
    with pytest.raises(IntakeCandidateError):
        build_intake_candidate(_intake(normalized_request=""))


def test_phase_eight_one_warning_is_preserved_and_explained() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert (
        fixture["preserved_warning"]
        == "phase_8_1_future_files_do_not_exist_test_updated_after_approved_phase_9_2_kernel_file_creation"
    )
    assert fixture["warning_is_acceptable"] is True
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "PASS WITH WARNINGS" in phase_doc
    assert "Phase 8.1's original" in phase_doc
    assert "explicitly listed as Phase 8.1 eligible runtime files" in phase_doc


def test_boundary_results_show_no_phase_nine_five_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["new_lima_changes_in_phase_9_5"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_remains_non_executing"] is True
    assert boundary["humaninput_runtime_bridge_added"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["live_adapter_added"] is False
    assert boundary["intentcompiler_runtime_changed"] is False
    assert boundary["guardiandecision_runtime_changed"] is False
    assert boundary["approval_enforcement_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["shell_browser_network_file_mutation_robotics_physical_world_side_effects_added"] is False


def test_phase_doc_gates_phase_ten_and_runtime_expansion() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "Phase 10 remains gated" in phase_doc
    assert "must not begin without explicit Phil approval" in phase_doc
    assert "No Phase 10, runtime expansion" in phase_doc


def test_no_phase_nine_five_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_9_5*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_9_5*"))
