"""Phase 47.3 static acceptance-test implementation preflight archive closeout tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_47_3_STATIC_ACCEPTANCE_TEST_IMPLEMENTATION_PREFLIGHT_ARCHIVE_CLOSEOUT.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_47_3_static_acceptance_test_implementation_preflight_archive_closeout.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_phase_47_3_fixture_exists_and_is_docs_only_archive_closeout() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "47.3"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["archive_closeout_only"] is True
    assert fixture["runtime_test_harness_created"] is False
    assert fixture["actual_acceptance_tests_created"] is False
    assert fixture["executable_acceptance_tests_created"] is False


def test_phase_47_3_completed_phases_include_47_0_through_47_3() -> None:
    phases = _load_json(PHASE_FIXTURE_PATH)["completed_phases"]
    assert phases == ["47.0", "47.1", "47.2", "47.3"]


def test_phase_47_3_evidence_summary_matches_closeout_requirements() -> None:
    evidence = _load_json(PHASE_FIXTURE_PATH)["evidence_summary"]
    assert evidence["phase_47_0_preflight_review_complete"] is True
    assert evidence["phase_47_1_static_checklist_complete"] is True
    assert evidence["phase_47_2_readiness_review_complete"] is True
    assert evidence["shared_sequence_alignment_confirmed"] is True
    assert evidence["consumer_and_embodiment_requirements_confirmed"] is True
    assert evidence["guardian_ownership_boundary_confirmed"] is True


def test_phase_47_3_gap_summary_has_no_sev_1_or_sev_2() -> None:
    gaps = _load_json(PHASE_FIXTURE_PATH)["gap_summary"]
    assert gaps["sev_1_blockers"] == []
    assert gaps["sev_2_readiness_gaps"] == []
    assert isinstance(gaps["sev_3_cleanup_notes"], list)


def test_phase_47_3_boundary_results_preserve_blocked_runtime_surfaces() -> None:
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


def test_phase_47_3_recommends_new_explicit_approval_before_implementation() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert (
        fixture["recommended_next_lane"]
        == "new_explicit_phil_approval_required_before_any_implementation_lane"
    )
    assert fixture["runtime_implementation_recommended"] is False
    assert fixture["next_runtime_implementation_approved"] is False


def test_phase_47_3_stays_out_of_runtime_and_tests_support_paths() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["runtime_behavior_changed"] is False
    assert not list((REPO_ROOT / "lima").rglob("*phase_47_3*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_47_3*"))


def test_phase_47_3_doc_declares_archive_closeout_only_and_runtime_block() -> None:
    text = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "docs/tests/fixtures-only static preflight lane" in text
    assert "does not create or activate a runtime test harness" in text
    assert "Any future implementation lane remains blocked until explicit Phil approval" in text
