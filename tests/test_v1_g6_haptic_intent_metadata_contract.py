"""Static checks for the V1-G6 haptic intent metadata contract."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = REPO_ROOT / "tests" / "fixtures" / "runtime_extraction"
SUMMARY_PATH = FIXTURE_DIR / "v1_g6_haptic_intent_metadata_contract.json"
DOCS = {
    "contract": REPO_ROOT / "docs" / "V1_G6_HAPTIC_INTENT_METADATA_CONTRACT.md",
    "audit": REPO_ROOT / "docs" / "V1_G6_HAPTIC_INTENT_METADATA_AUDIT.md",
    "closeout": REPO_ROOT / "docs" / "V1_G6_HAPTIC_INTENT_METADATA_CLOSEOUT.md",
}


def _load_json(path: Path) -> dict[str, Any]:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g6_summary_and_docs_exist_and_accept_static_contract_only() -> None:
    summary = _load_json(SUMMARY_PATH)
    assert SUMMARY_PATH.exists()
    for doc_path in DOCS.values():
        assert doc_path.exists()
    assert summary["gap_id"] == "V1-G6"
    assert summary["api_status"] == "CANDIDATE_ONLY"
    assert summary["contract_completed"] is True
    assert summary["contract_accepted_as_static_evidence"] is True
    assert summary["contract_accepted_as_device_behavior"] is False
    assert summary["v1_product_ready"] is False


def test_v1_g6_summary_tracks_expected_case_fixtures() -> None:
    summary = _load_json(SUMMARY_PATH)
    expected = {
        "tests/fixtures/runtime_extraction/v1_g6_received_soft_ack_intent.json",
        "tests/fixtures/runtime_extraction/v1_g6_thinking_progress_pulse_intent.json",
        "tests/fixtures/runtime_extraction/v1_g6_preview_ready_light_tap_intent.json",
        "tests/fixtures/runtime_extraction/v1_g6_blocked_warning_intent.json",
        "tests/fixtures/runtime_extraction/v1_g6_needs_approval_attention_intent.json",
        "tests/fixtures/runtime_extraction/v1_g6_completed_success_intent.json",
        "tests/fixtures/runtime_extraction/v1_g6_failed_safe_error_intent.json",
        "tests/fixtures/runtime_extraction/v1_g6_deferred_neutral_hold_intent.json",
        "tests/fixtures/runtime_extraction/v1_g6_forged_device_haptic_claim_fail_closed.json",
    }
    assert set(summary["case_fixture_files"]) == expected
    for relative_path in expected:
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g6_state_mapping_covers_required_shell_response_states() -> None:
    summary = _load_json(SUMMARY_PATH)
    assert set(summary["shell_response_states"]) == {
        "received",
        "thinking",
        "preview_ready",
        "blocked",
        "needs_approval",
        "completed",
        "failed_safe",
        "deferred",
    }
    assert summary["state_to_haptic_intent_family"] == {
        "received": "soft_ack",
        "thinking": "progress_pulse",
        "preview_ready": "light_tap",
        "blocked": "warning",
        "needs_approval": "attention",
        "completed": "success",
        "failed_safe": "error_alert",
        "deferred": "neutral_hold",
    }


def test_v1_g6_required_metadata_and_forbidden_device_fields_are_defined() -> None:
    summary = _load_json(SUMMARY_PATH)
    metadata = set(summary["required_haptic_intent_metadata"])
    assert {
        "intent_id",
        "source_shell",
        "response_state",
        "packet_status",
        "kernel_status",
        "haptic_intent_family",
        "urgency",
        "intensity_hint",
        "duration_hint_ms",
        "accessibility_respect",
        "fallback_visual_state",
        "fallback_auditory_state",
        "reason_code",
        "audit_evidence_ref",
        "policy_version",
    }.issubset(metadata)
    forbidden = set(summary["forbidden_haptic_device_fields"])
    assert {
        "actuator_id",
        "device_id",
        "vibration_command",
        "motor_pattern",
        "os_haptic_api",
        "execute_haptic_now",
        "hardware_target",
        "physical_feedback_command",
    }.issubset(forbidden)


def test_v1_g6_shell_ownership_and_boundary_results_add_no_device_behavior() -> None:
    summary = _load_json(SUMMARY_PATH)
    assert summary["shell_owns_haptics"] is True
    assert summary["lima_owns_haptic_device_implementation"] is False
    assert summary["haptic_intent_metadata_contract_added"] is True
    for key in (
        "runtime_behavior_added",
        "lima_runtime_files_changed",
        "tests_support_changed",
        "runtime_exports_changed",
        "shell_repos_changed",
        "sparkbot_shell_wiring_added",
        "sparkbot_import_added",
        "sparkbot_code_copied",
        "arc_bot_shell_wiring_added",
        "provider_model_routing_added",
        "provider_model_calls_added",
        "guardian_decision_runtime_added",
        "approval_enforcement_added",
        "execution_dispatch_persistence_added",
        "browser_file_network_device_robotics_behavior_added",
        "haptic_device_behavior_added",
        "device_haptic_command_added",
        "shell_rendering_invoked",
        "physical_world_behavior_added",
        "runtime_export_cleanup_approved",
        "final_freeze_approved",
    ):
        assert summary[key] is False


def test_v1_g6_docs_state_static_only_verdict_and_next_gap() -> None:
    contract_text = DOCS["contract"].read_text(encoding="utf-8")
    audit_text = DOCS["audit"].read_text(encoding="utf-8")
    closeout_text = DOCS["closeout"].read_text(encoding="utf-8")
    assert "`V1-G6` is complete as a static haptic intent metadata contract" in contract_text
    assert "Haptics are part of shell experience, not LIMA device authority." in contract_text
    assert "Verdict: `accept_static_haptic_intent_metadata_contract_only`." in audit_text
    assert "Recommended: `V1-G7`." in closeout_text
