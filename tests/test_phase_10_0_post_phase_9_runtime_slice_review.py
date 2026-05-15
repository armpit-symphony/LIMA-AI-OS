"""Static checks for Phase 10.0 post-Phase-9 runtime slice review."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_10_0_POST_PHASE_9_RUNTIME_SLICE_REVIEW.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_10_0_post_phase_9_runtime_slice_review.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_no_code_design_review_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "10.0"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False
    assert fixture["phase_11_runtime_implementation_approved"] is False


def test_phase_reviews_all_phase_nine_scope() -> None:
    reviewed = _load_json(PHASE_FIXTURE_PATH)["reviewed_phase_9_scope"]
    assert reviewed == [
        "phase_9_0_runtime_slice_preflight_audit_eligible_file_confirmation",
        "phase_9_1_runtime_slice_acceptance_test_scaffolding",
        "phase_9_2_non_executing_kernel_intake_to_candidate_coordinator_implementation",
        "phase_9_3_runtime_slice_readiness_review",
        "phase_9_4_phase_9_runtime_slice_audit_archive_closeout",
        "phase_9_5_first_runtime_slice_audit_archive_closeout",
    ]


def test_phase_nine_runtime_files_are_exact() -> None:
    assert _load_json(PHASE_FIXTURE_PATH)["phase_9_runtime_files"] == [
        "lima/kernel/__init__.py",
        "lima/kernel/intake_candidate.py",
    ]


def test_phase_nine_proof_and_gap_lists_are_boundary_safe() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    proved = set(fixture["phase_9_proved"])
    gaps = set(fixture["phase_9_did_not_prove"])
    assert "candidate_metadata_without_execution_authority" in proved
    assert "execution_allowed_false" in proved
    assert "side_effects_allowed_false" in proved
    assert "approval_state_never_approved" in proved
    assert "phase_5_runtime_bridge_remains_gated" in proved
    assert "humaninput_runtime_bridge_safety" in gaps
    assert "intentcompiler_behavior" in gaps
    assert "guardiandecision_behavior" in gaps
    assert "approval_enforcement" in gaps
    assert "execution" in gaps
    assert "dispatch" in gaps
    assert "audit_persistence" in gaps


def test_phase_ten_direction_is_no_code_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase_10_direction"] == "no_code_design_for_next_possible_runtime_slice"
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "does not implement runtime behavior" in phase_doc
    assert "No Phase 11 runtime implementation is approved" in phase_doc


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["live_adapter_added"] is False
    assert boundary["approval_enforcement_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False


def test_no_phase_ten_zero_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_10_0*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_10_0*"))
