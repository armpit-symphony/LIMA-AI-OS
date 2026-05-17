"""Phase 40.2 LIMA Office vocabulary matrix tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_40_2_LIMA_OFFICE_TASK_APPROVAL_AUDIT_VOCABULARY_MATRIX.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_40_2_lima_office_task_approval_audit_vocabulary_matrix.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_40_2_keeps_arc_bot_as_primary_consumer() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "40.2"
    assert fixture["primary_guarded_task_consumer"] == "arc_bot_lima_ai_office"
    assert fixture["sparkbot_reference_evidence_only"] is True
    assert fixture["direct_sparkbot_integration_recommended"] is False
    assert fixture["arc_bot_implementation_recommended"] is False
    assert fixture["humaninput_bridge_implementation_recommended"] is False


def test_phase_40_2_classifies_concepts_for_arc_bot_defaults() -> None:
    matrix = _load_json(PHASE_FIXTURE_PATH)["classification_matrix"]
    assert "task_intake" in matrix["adopt"]
    assert "audit_evidence_ref" in matrix["adopt"]
    assert "operator_approval_boundary" in matrix["adapt_for_arc_bot_stricter_defaults"]
    assert "external_write_posture" in matrix["adapt_for_arc_bot_stricter_defaults"]
    assert "broad_owner_local_execution_surface" in matrix["sparkbot_only"]
    assert "physical_world_posture" in matrix["defer"]
    assert "runtime_authority_from_planning_labels" in matrix["reject"]


def test_phase_40_2_records_office_run_and_connector_vocab() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert set(fixture["run_states"]) == {
        "planned",
        "awaiting_approval",
        "ready",
        "blocked",
        "completed",
        "failed",
    }
    assert "missing_secrets" in fixture["connector_health_values"]
    assert "bridge_needed" in fixture["connector_health_values"]
    text = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "`run_state`" in text
    assert "`connector_health`" in text
    assert "`memory_trust`" in text


def test_phase_40_2_preserves_hard_invariants() -> None:
    invariants = _load_json(PHASE_FIXTURE_PATH)["hard_invariants"]
    false_keys = [
        "execution_allowed",
        "side_effects_allowed",
        "approval_granted",
        "dispatch_allowed",
        "persistence_allowed",
        "humaninput_bridge_active",
        "sparkbot_wiring_active",
        "live_adapter_active",
        "external_calls_allowed",
        "robotics_allowed",
        "physical_world_allowed",
    ]
    for key in false_keys:
        assert invariants[key] is False
    assert invariants["non_authoritative"] is True
    assert invariants["preview_only"] is True
    assert invariants["safe_by_default"] is True


def test_phase_40_2_stays_in_approved_scope() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["runtime_behavior_changed"] is False
    assert not list((REPO_ROOT / "lima").rglob("*phase_40_2*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_40_2*"))
