"""Phase 46.3 static acceptance-test dry-run archive closeout tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_46_3_STATIC_ACCEPTANCE_TEST_DRY_RUN_ARCHIVE_CLOSEOUT.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_46_3_static_acceptance_test_dry_run_archive_closeout.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_phase_46_3_fixture_exists_and_is_docs_tests_fixtures_only_archive_closeout() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "46.3"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["archive_closeout_only"] is True
    assert fixture["runtime_test_harness_created"] is False
    assert fixture["actual_acceptance_tests_created"] is False
    assert fixture["executable_acceptance_tests_created"] is False
    assert fixture["phase_46_2_anchor"] == "2191d8281b5d115f770392d3ce9d8752e1071630"
    assert (
        fixture["phase_46_2_tag"]
        == "phase-46.2-static-acceptance-test-dry-run-readiness-review"
    )


def test_phase_46_3_completed_phases_include_46_0_through_46_3() -> None:
    phases = _load_json(PHASE_FIXTURE_PATH)["completed_phases"]
    assert phases == ["46.0", "46.1", "46.2", "46.3"]


def test_phase_46_3_evidence_and_gap_summary_match_closeout_requirements() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    evidence = fixture["evidence_summary"]
    assert evidence["phase_46_0_static_template_defined"] is True
    assert evidence["phase_46_1_static_dry_run_plan_defined"] is True
    assert evidence["phase_46_2_readiness_review_no_sev_1_or_sev_2_gaps"] is True
    assert evidence["phase_46_2_only_optional_sev_3_notes"] is True

    gaps = fixture["gap_summary"]
    assert gaps["sev_1_blockers"] == []
    assert gaps["sev_2_readiness_gaps"] == []
    assert isinstance(gaps["sev_3_cleanup_notes"], list)


def test_phase_46_3_boundary_results_preserve_blocked_runtime_and_action_surfaces() -> None:
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
        "model_tool_driver_calls_added",
        "external_calls_added",
        "shell_browser_network_file_mutation_added",
        "robotics_physical_world_behavior_added",
        "hidden_side_effects_added",
    ):
        assert boundary[key] is False


def test_phase_46_3_recommends_non_runtime_next_lane_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["recommended_next_lane"].startswith(
        "phase_47_docs_tests_fixtures_only_"
    )
    assert fixture["runtime_implementation_recommended"] is False
    assert fixture["next_runtime_implementation_approved"] is False
    blocked = set(fixture["blocked_scope"])
    assert "runtime_implementation" in blocked
    assert "lima_changes" in blocked
    assert "tests_support_changes" in blocked
    assert "runtime_test_harness_creation_or_activation" in blocked
    assert "model_tool_driver_calls" in blocked
    assert "robotics_hardware_control_physical_world_behavior" in blocked


def test_phase_46_3_stays_out_of_runtime_and_tests_support_paths() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["runtime_behavior_changed"] is False
    assert not list((REPO_ROOT / "lima").rglob("*phase_46_3*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_46_3*"))


def test_phase_46_3_doc_declares_archive_closeout_only_and_runtime_block() -> None:
    text = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "docs/tests/fixtures-only" in text
    assert "This phase does not implement runtime bridge behavior." in text
    assert "No future runtime implementation is approved by this closeout." in text
    assert "Runtime implementation remains blocked" in text
