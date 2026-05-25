"""Phase 47.2 static acceptance-test implementation checklist readiness review tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_47_2_STATIC_ACCEPTANCE_TEST_IMPLEMENTATION_CHECKLIST_READINESS_REVIEW.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_47_2_static_acceptance_test_implementation_checklist_readiness_review.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_phase_47_2_fixture_exists_and_is_docs_only_readiness_review() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "47.2"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["readiness_review_only"] is True
    assert fixture["runtime_test_harness_created"] is False
    assert fixture["actual_acceptance_tests_created"] is False
    assert fixture["executable_acceptance_tests_created"] is False
    assert fixture["reviewed_phase"] == "47.1"


def test_phase_47_2_coverage_results_confirm_alignment_requirements() -> None:
    coverage = _load_json(PHASE_FIXTURE_PATH)["coverage_results"]
    assert coverage["required_shared_sequence_explicit"] is True
    assert coverage["required_sequence_refs_explicit"] is True
    assert coverage["required_invariant_naming_aligned"] is True
    assert coverage["required_invariant_values_fail_closed"] is True
    assert coverage["runtime_ladder_vocabulary_explicit"] is True
    assert coverage["mock_safe_active_states_explicit"] is True
    assert coverage["guardian_ownership_boundary_explicit"] is True
    assert coverage["consumer_profile_required"] is True
    assert coverage["embodiment_profile_required_on_every_candidate_preview"] is True
    assert coverage["forbidden_scope_explicit_and_fail_closed"] is True


def test_phase_47_2_gap_results_show_no_sev_1_or_sev_2_blockers() -> None:
    gaps = _load_json(PHASE_FIXTURE_PATH)["gap_results"]
    assert gaps["sev_1_blockers"] == []
    assert gaps["sev_2_readiness_gaps"] == []
    assert isinstance(gaps["sev_3_cleanup_notes"], list)
    assert gaps["continuation_recommended"] is True


def test_phase_47_2_boundary_results_preserve_blocked_runtime_surfaces() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    for key in (
        "runtime_bridge_behavior_added",
        "runtime_test_harness_active",
        "actual_acceptance_test_harness_behavior_added",
        "executable_acceptance_tests_created",
        "lima_changes",
        "tests_support_changes",
        "guardian_decision_created",
        "approval_enforcement_added",
        "execution_dispatch_persistence_added",
        "model_tool_driver_adapter_calls_added",
        "external_calls_added",
        "shell_browser_network_file_mutation_added",
        "robotics_physical_world_behavior_added",
        "hidden_side_effects_added",
    ):
        assert boundary[key] is False


def test_phase_47_2_recommends_non_runtime_next_lane_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["recommended_next_lane"] == (
        "phase_47_3_docs_tests_fixtures_only_static_preflight_archive_closeout"
    )
    assert fixture["runtime_implementation_recommended"] is False
    assert fixture["next_runtime_implementation_approved"] is False


def test_phase_47_2_stays_out_of_runtime_and_tests_support_paths() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["runtime_behavior_changed"] is False
    assert not list((REPO_ROOT / "lima").rglob("*phase_47_2*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_47_2*"))


def test_phase_47_2_doc_declares_readiness_only_and_runtime_block() -> None:
    text = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "docs/tests/fixtures-only readiness review" in text
    assert "does not create or activate a runtime test harness" in text
    assert "No runtime implementation is recommended by this review." in text
