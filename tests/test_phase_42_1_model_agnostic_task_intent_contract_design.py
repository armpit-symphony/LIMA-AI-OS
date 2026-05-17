"""Phase 42.1 model-agnostic task/intent contract design tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_42_1_MODEL_AGNOSTIC_TASK_INTENT_CONTRACT_DESIGN.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_42_1_model_agnostic_task_intent_contract_design.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_42_1_defines_model_agnostic_input_contract() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    input_fields = set(fixture["universal_input_contract"])
    assert fixture["phase"] == "42.1"
    assert "model_provider_hint" in input_fields
    assert "model_identity_hint" in input_fields
    assert "trust_context" in input_fields
    assert "redaction_posture" in input_fields
    assert "Unknown models and providers must remain safe." in PHASE_DOC_PATH.read_text(encoding="utf-8")


def test_phase_42_1_defines_task_intent_and_preview_contracts() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    task_fields = set(fixture["universal_task_intent_contract"])
    preview_fields = set(fixture["candidate_action_preview_contract"])
    assert "consumer_profile" in task_fields
    assert "embodiment_profile" in task_fields
    assert "action_class" in task_fields
    assert "risk_tier" in task_fields
    assert "approval_posture" in preview_fields
    assert "dry_run_posture" in preview_fields
    assert "blocked_reasons" in preview_fields
    assert "rollback_notes" in preview_fields


def test_phase_42_1_keeps_approval_as_description_not_grant() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    posture = set(fixture["approval_posture_values"])
    assert "confirmation_required" in posture
    assert "pin_required" in posture
    assert "breakglass_required" in posture
    assert "policy_membrane_required" in posture
    assert fixture["hard_invariants"]["approval_granted"] is False
    assert fixture["hard_invariants"]["lima_grants_approval"] is False
    assert "LIMA cannot grant approval in this phase." in PHASE_DOC_PATH.read_text(encoding="utf-8")


def test_phase_42_1_records_telemetry_and_embodiment_vocabulary_without_persistence() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    telemetry = set(fixture["telemetry_evidence_vocabulary"])
    embodiment = set(fixture["embodiment_profile_contract"])
    assert "policy_decision_ref" in telemetry
    assert "audit_hash_ref" in telemetry
    assert "simulation_ref" in telemetry
    assert "profile_kind" in embodiment
    assert "adapter_boundary" in embodiment
    assert "emergency_stop_posture" in embodiment
    assert "No audit persistence is implemented." in PHASE_DOC_PATH.read_text(encoding="utf-8")


def test_phase_42_1_stays_docs_tests_fixtures_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_schema_added"] is False
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["runtime_behavior_changed"] is False
    assert not list((REPO_ROOT / "lima").rglob("*phase_42_1*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_42_1*"))
