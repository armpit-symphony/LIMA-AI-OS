"""Phase 42.0 LIMA universal runtime contract reframe tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_42_0_LIMA_UNIVERSAL_RUNTIME_CONTRACT_REFRAMING_AUDIT.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_42_0_lima_universal_runtime_contract_reframing_audit.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_42_0_reframes_lima_as_universal_os_target() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "42.0"
    assert fixture["phase_42_reframed_from_arc_centered_to_universal_lima_ai_os"] is True
    assert fixture["primary_target"] == "lima_ai_os_runtime"
    assert fixture["model_agnostic"] is True
    assert fixture["consumer_agnostic"] is True
    assert fixture["embodiment_agnostic"] is True
    text = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "Arc Bot is one consumer profile" in text
    assert "LIMA AI OS is the universal runtime contract target" in text


def test_phase_42_0_records_product_split() -> None:
    split = _load_json(PHASE_FIXTURE_PATH)["product_split"]
    assert split["lima_ai_os_runtime"] == "public_universal_runtime_contract_and_safety_substrate"
    assert split["sparkbot_public"] == "open_source_showcase_shell"
    assert split["arc_bot_lima_office"] == "proprietary_guarded_worker_bot_shell"
    assert split["paid_lima_robotics_iot_unlock"] == "proprietary_paid_robotics_iot_embodiment_path"


def test_phase_42_0_demotes_arc_bot_and_keeps_sparkbot_reference_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["arc_bot_role"] == "example_guarded_office_agent_consumer_profile"
    assert fixture["sparkbot_role"] == "reference_evidence_and_public_showcase_shell"
    assert "arc_bot_product_shell" in fixture["private_boundary"]
    assert "model_agnostic_contracts" in fixture["public_boundary"]


def test_phase_42_0_records_repo_sanitization_checklist() -> None:
    checklist = set(_load_json(PHASE_FIXTURE_PATH)["repo_sanitization_checklist"])
    assert "no_secrets_tokens_keys_customer_data" in checklist
    assert "no_proprietary_arc_bot_implementation" in checklist
    assert "no_paid_robotics_iot_unlock_code" in checklist
    assert "no_sparkbot_private_workstation_code_copied_into_lima" in checklist
    assert "no_guardian_bypass_or_runtime_authority_from_profile_vocabulary" in checklist


def test_phase_42_0_preserves_hard_invariants_and_scope() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    invariants = fixture["hard_invariants"]
    assert invariants["preview_only"] is True
    assert invariants["non_authoritative"] is True
    assert invariants["safe_by_default"] is True
    for key in (
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
        "lima_grants_approval",
    ):
        assert invariants[key] is False
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["runtime_behavior_changed"] is False
    assert not list((REPO_ROOT / "lima").rglob("*phase_42_0*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_42_0*"))
