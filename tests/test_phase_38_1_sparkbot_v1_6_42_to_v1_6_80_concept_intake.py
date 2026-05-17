"""Phase 38.1 Sparkbot concept intake tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_38_1_SPARKBOT_V1_6_42_TO_V1_6_80_CONCEPT_INTAKE.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_38_1_sparkbot_v1_6_42_to_v1_6_80_concept_intake.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_38_1_records_v1_6_42_baseline() -> None:
    baseline = set(_load_json(PHASE_FIXTURE_PATH)["baseline_v1_6_42"])
    assert "computer_control_checkbox_persistence" in baseline
    assert "model_stack_provider_setting_persistence" in baseline
    assert "startup_loading_saved_settings" in baseline
    assert "Sparkbot v1.6.42 focused on operational persistence" in PHASE_DOC_PATH.read_text(encoding="utf-8")


def test_phase_38_1_records_current_sparkbot_operating_concepts() -> None:
    concepts = set(_load_json(PHASE_FIXTURE_PATH)["v1_6_80_concepts_identified"])
    expected = {
        "command_center_operator_hub",
        "owner_local_posture",
        "strict_security_posture",
        "policy_simulation_explain_plan",
        "persistent_approval_inbox",
        "agent_identity_metadata",
        "memory_lifecycle_trust_metadata",
        "mcp_registry_lima_robo_os_manifests",
        "robotics_replay_simulation_default",
        "real_hardware_motion_blocked_by_default",
        "sparkbot_command_center_lima_runtime_substrate",
    }
    assert expected.issubset(concepts)


def test_phase_38_1_keeps_lima_concepts_as_planning_metadata_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["lima_inclusion_rule"] == "planning_preview_metadata_only"
    invariants = fixture["hard_invariants"]
    assert invariants["execution_allowed"] is False
    assert invariants["approval_granted"] is False
    assert invariants["dispatch_allowed"] is False
    assert invariants["persistence_allowed"] is False
    assert invariants["side_effects_allowed"] is False
    assert invariants["sparkbot_wiring_active"] is False
    assert invariants["robotics_physical_world_active"] is False


def test_phase_38_1_sets_up_vocabulary_review_groups() -> None:
    groups = set(_load_json(PHASE_FIXTURE_PATH)["concept_groups_for_vocabulary_review"])
    assert "operator_posture" in groups
    assert "approval_posture" in groups
    assert "dry_run_posture" in groups
    assert "agent_identity" in groups
    assert "memory_trust" in groups
    assert "robotics_posture" in groups
    assert "audit_surface" in groups


def test_phase_38_1_stays_docs_tests_fixtures_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert not list((REPO_ROOT / "lima").rglob("*phase_38_1*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_38_1*"))
