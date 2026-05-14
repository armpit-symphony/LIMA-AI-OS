"""Archive checks for the Phase 9 first runtime slice lane."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from lima.kernel.intake_candidate import build_intake_candidate


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_9_4_PHASE_9_RUNTIME_SLICE_AUDIT_ARCHIVE_CLOSEOUT.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_9_4_phase_9_runtime_slice_audit_archive_closeout.json"
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
        "intake_id": "phase-9-4-intake",
        "source": "archive_shell",
        "source_channel": "archive_channel",
        "operator_intent": "archive the runtime slice",
        "normalized_request": "archive_runtime_slice",
        "requested_action": "archive_metadata",
        "action_category": "informational",
        "freshness": "fresh",
        "replay_status": "not_replayed",
        "provenance": {"lineage_seed": "phase-9-4-lineage"},
    }
    intake.update(overrides)
    return intake


def test_phase_declares_archive_closeout_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "9.4"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False
    assert fixture["next_scope_requires_explicit_phil_approval"] is True


def test_completed_phase_nine_scope_lists_zero_through_three() -> None:
    completed = _load_json(PHASE_FIXTURE_PATH)["completed_phase_9_scope"]
    assert completed == [
        "phase_9_0_runtime_slice_preflight_audit_eligible_file_confirmation",
        "phase_9_1_runtime_slice_acceptance_test_scaffolding",
        "phase_9_2_non_executing_kernel_intake_to_candidate_coordinator_implementation",
        "phase_9_3_runtime_slice_readiness_review",
    ]


def test_archive_lists_added_runtime_files_and_artifact_types() -> None:
    added = set(_load_json(PHASE_FIXTURE_PATH)["added"])
    assert "docs" in added
    assert "fixtures" in added
    assert "static_tests" in added
    assert "runtime_slice_tests" in added
    assert "roadmap_state_updates" in added
    assert "lima/kernel/__init__.py" in added
    assert "lima/kernel/intake_candidate.py" in added


def test_archive_lists_forbidden_surfaces_not_added() -> None:
    not_added = set(_load_json(PHASE_FIXTURE_PATH)["not_added"])
    assert "humaninput_runtime_bridge" in not_added
    assert "live_adapter" in not_added
    assert "sparkbot_import_or_wiring" in not_added
    assert "real_intentenvelope_creation" in not_added
    assert "intentcompiler_runtime_behavior" in not_added
    assert "real_guardiandecision_creation" in not_added
    assert "guardiandecision_runtime_behavior" in not_added
    assert "approval_enforcement" in not_added
    assert "execution" in not_added
    assert "audit_persistence" in not_added
    assert "tests_support_changes" in not_added
    assert "shell_browser_network_file_mutation_robotics_physical_world_side_effects" in not_added


def test_exact_runtime_files_touched_in_phase_nine_are_eligible() -> None:
    files = _load_json(PHASE_FIXTURE_PATH)["eligible_runtime_files_touched_in_phase_9"]
    assert files == [
        "lima/kernel/__init__.py",
        "lima/kernel/intake_candidate.py",
    ]


def test_archived_coordinator_still_outputs_non_executing_candidate() -> None:
    candidate = build_intake_candidate(_intake())
    required_flags = _load_json(PHASE_FIXTURE_PATH)["candidate_output_required_flags"]
    for field_name, expected in required_flags.items():
        assert candidate[field_name] is expected
    assert candidate["provenance"]["lineage_seed"] == "phase-9-4-lineage"


def test_next_options_stop_before_phase_ten_or_runtime_expansion() -> None:
    options = set(_load_json(PHASE_FIXTURE_PATH)["recommended_next_options"])
    assert options == {
        "audit_phase_9_0_through_9_4",
        "phase_10_no_code_design_lane_for_next_runtime_slice",
        "more_tests_for_existing_phase_9_coordinator_without_runtime_expansion",
        "pause_and_preserve_current_runtime_slice",
    }


def test_phase_doc_closes_phase_nine_at_decision_gate() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "archives the Phase 9 first runtime slice lane" in phase_doc
    assert "does not modify runtime code" in phase_doc
    assert "Phase 9 is complete" in phase_doc
    assert "require a new explicit Phil approval" in phase_doc
    assert "No next option is selected by this closeout" in phase_doc


def test_boundary_results_show_no_new_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["files_under_lima_modified_by_phase_9_4"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_added_by_phase_9_4"] is False
    assert boundary["phase_9_runtime_behavior_remains_non_executing"] is True
    assert boundary["files_outside_phase_8_1_eligible_runtime_list_modified"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["live_adapter_added"] is False
    assert boundary["humaninput_runtime_bridge_added"] is False
    assert boundary["intentcompiler_runtime_changed"] is False
    assert boundary["guardiandecision_runtime_changed"] is False
    assert boundary["approval_enforcement_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False


def test_no_phase_nine_four_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_9_4*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_9_4*"))
