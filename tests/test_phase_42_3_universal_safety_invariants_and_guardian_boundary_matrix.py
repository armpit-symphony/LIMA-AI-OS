"""Phase 42.3 universal safety invariant and Guardian boundary tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_42_3_UNIVERSAL_SAFETY_INVARIANTS_AND_GUARDIAN_BOUNDARY_MATRIX.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_42_3_universal_safety_invariants_and_guardian_boundary_matrix.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_42_3_records_guardian_approval_boundary() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "42.3"
    assert fixture["guardian_or_future_policy_membrane_owns_real_approval_state"] is True
    assert fixture["lima_describes_approval_posture_only"] is True
    assert fixture["consumer_profile_vocabulary_can_grant_runtime_authority"] is False
    text = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "Guardian or a future policy membrane owns real approval state." in text
    assert "LIMA AI OS in Phase 42 cannot:" in text


def test_phase_42_3_preserves_hard_invariants() -> None:
    invariants = _load_json(PHASE_FIXTURE_PATH)["hard_invariants"]
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


def test_phase_42_3_boundary_matrix_blocks_high_risk_action_classes() -> None:
    matrix = _load_json(PHASE_FIXTURE_PATH)["boundary_matrix"]
    assert matrix["external_write"] == "blocked_or_approval_postured_guardian_confirmation_required"
    assert matrix["execute"] == "blocked_future_implementation_and_guardian_approval_required"
    assert matrix["admin"] == "blocked_or_breakglass_postured_guardian_pin_breakglass_required"
    assert matrix["secret_use"] == "blocked_or_redacted_guardian_vault_approval_required"
    assert matrix["scheduled_work"] == "planned_only_no_worker_queue"
    assert matrix["robot_motion"] == "blocked_deferred_guardian_hardware_adapter_emergency_stop_required"
    assert (
        matrix["physical_world_action"]
        == "blocked_deferred_guardian_embodiment_policy_emergency_stop_required"
    )
    assert matrix["emergency_stop"] == "descriptive_only_future_audited_path_requires_explicit_approval"


def test_phase_42_3_keeps_robotics_iot_as_vocabulary_only() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["robotics_iot_boundary"]
    assert boundary["profile_vocabulary_only"] is True
    assert boundary["blocked_or_deferred_action_classes"] is True
    assert boundary["hardware_calls_added"] is False
    assert boundary["mcp_calls_added"] is False
    assert boundary["adapters_added"] is False
    assert boundary["physical_world_behavior_added"] is False
    assert "No MCP calls, hardware calls, adapters, drivers, movement, actuation" in PHASE_DOC_PATH.read_text(
        encoding="utf-8"
    )


def test_phase_42_3_stays_docs_tests_fixtures_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["runtime_behavior_changed"] is False
    assert not list((REPO_ROOT / "lima").rglob("*phase_42_3*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_42_3*"))
