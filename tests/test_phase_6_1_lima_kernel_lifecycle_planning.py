"""Static checks for Phase 6.1 LIMA kernel lifecycle planning."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_6_1_LIMA_KERNEL_LIFECYCLE_PLANNING.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT / "tests" / "fixtures" / "runtime_extraction" / "phase_6_1_lima_kernel_lifecycle_planning.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_declares_kernel_lifecycle_planning_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "6.1"
    assert fixture["non_runtime"] is True
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["kernel_lifecycle_planning_only"] is True


def test_kernel_lifecycle_stages_are_explicit() -> None:
    stages = _load_json(PHASE_FIXTURE_PATH)["kernel_lifecycle_stages"]
    assert stages == [
        "shell_intake",
        "boundary_normalization",
        "intent_candidate_formation",
        "guardian_review",
        "guardiandecision_record",
        "spine_audit_memory_handoff",
        "driver_tool_handoff_blocked_until_approved",
    ]


def test_lifecycle_rules_keep_candidates_non_executable_and_guardian_gated() -> None:
    rules = _load_json(PHASE_FIXTURE_PATH)["lifecycle_rules"]
    assert rules["humaninput_is_intent_context_not_execution_permission"] is True
    assert rules["intentenvelope_candidates_non_executable"] is True
    assert rules["guardiandecision_is_future_authority_boundary"] is True
    assert rules["audit_spine_memory_designed_before_persistence"] is True


def test_sparkbot_and_robo_os_remain_boundaries_not_runtime_integrations() -> None:
    rules = _load_json(PHASE_FIXTURE_PATH)["lifecycle_rules"]
    assert rules["sparkbot_reference_shell_not_kernel"] is True
    assert rules["robo_os_physical_world_surfaces_remain_gated"] is True


def test_runtime_bridge_prerequisites_include_core_lifecycle_boundaries() -> None:
    prerequisites = set(_load_json(PHASE_FIXTURE_PATH)["runtime_prerequisites_before_bridge_implementation"])
    assert "kernel_lifecycle_review" in prerequisites
    assert "intentenvelope_lifecycle_boundary_map" in prerequisites
    assert "guardiandecision_lifecycle_boundary_map" in prerequisites
    assert "approval_boundary_model" in prerequisites
    assert "explicit_operator_runtime_approval" in prerequisites


def test_ready_only_for_phase_six_two_boundary_map() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["ready_for"] == [
        "phase_6_2_docs_tests_fixtures_only_intentenvelope_guardiandecision_lifecycle_boundary_map"
    ]
    assert "runtime_behavior" in fixture["not_ready_for"]
    assert "real_intentcompiler" in fixture["not_ready_for"]
    assert "real_guardiandecision" in fixture["not_ready_for"]


def test_doc_keeps_runtime_behavior_blocked() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "does not implement runtime behavior" in phase_doc
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "Runtime implementation remains blocked" in phase_doc


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["runtime_behavior_added"] is False
    assert boundary["files_under_lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["execution_added"] is False
    assert boundary["physical_world_action_added"] is False


def test_no_phase_six_one_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_6_1*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_6_1*"))
