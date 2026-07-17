"""Static checks for the V1-G7 Arc-Bot-shell integration proof intake."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g7_arc_bot_shell_integration_proof_intake.json"
)
DOCS = {
    "intake": REPO_ROOT / "docs" / "V1_G7_ARC_BOT_SHELL_INTEGRATION_PROOF_INTAKE.md",
    "audit": REPO_ROOT / "docs" / "V1_G7_ARC_BOT_SHELL_INTEGRATION_PROOF_INTAKE_AUDIT.md",
    "closeout": REPO_ROOT / "docs" / "V1_G7_ARC_BOT_SHELL_INTEGRATION_PROOF_INTAKE_CLOSEOUT.md",
}


def _load_json(path: Path) -> dict[str, Any]:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_arc_bot_shell_intake_summary_and_docs_exist() -> None:
    summary = _load_json(FIXTURE_PATH)
    assert FIXTURE_PATH.exists()
    for doc_path in DOCS.values():
        assert doc_path.exists()

    assert summary["gap_id"] == "V1-G7"
    assert summary["shell_repo"] == "Arc-Bot-shell"
    assert summary["api_status"] == "CANDIDATE_ONLY"
    assert summary["branch"] == "intake-v1-g7-arc-bot-shell-integration-proof-packet"
    assert summary["source_branch"] == "intake-v1-g7-sparkbot-integration-proof-packet"
    assert summary["arc_bot_shell_branch"] == "v1-g7-arc-bot-shell-integration-proof-packet"
    assert summary["arc_bot_shell_commit"] == "67653b2f43095b3807e8b3f7feaf98afda2bb774"
    assert summary["sparkbot_shell_packet_accepted"] is True
    assert summary["sparkbot_packet_accepted"] is True
    assert summary["arc_bot_shell_packet_received"] is True
    assert summary["arc_bot_shell_packet_accepted"] is True
    assert summary["all_requested_shell_packets_intaken"] is True
    assert summary["consolidated_v1_g7_closeout_complete"] is False
    assert summary["v1_g7_completed"] is False
    assert summary["v1_product_ready"] is False


def test_arc_bot_shell_intake_preserves_boundaries() -> None:
    summary = _load_json(FIXTURE_PATH)
    for key in (
        "runtime_behavior_added",
        "lima_runtime_files_changed",
        "tests_support_changed",
        "runtime_exports_changed",
        "sparkbot_shell_wiring_added",
        "sparkbot_wiring_added",
        "arc_bot_shell_wiring_added",
        "sparkbot_import_added",
        "sparkbot_code_copied",
        "shell_code_copied_or_imported_into_lima",
        "provider_model_routing_added",
        "provider_model_calls_added",
        "guardian_decision_runtime_added",
        "approval_enforcement_added",
        "execution_dispatch_persistence_added",
        "browser_file_network_device_robotics_behavior_added",
        "haptic_device_behavior_added",
        "device_haptic_command_added",
        "physical_world_behavior_added",
        "runtime_export_cleanup_approved",
        "final_freeze_approved",
    ):
        assert summary[key] is False


def test_arc_bot_shell_intake_state_status_and_haptics() -> None:
    summary = _load_json(FIXTURE_PATH)
    required_states = {
        "received",
        "thinking",
        "preview_ready",
        "blocked",
        "needs_approval",
        "completed",
        "failed_safe",
        "deferred",
    }

    assert set(summary["shell_response_states_evaluated"]) == required_states
    assert summary["source_backed_shell_response_states"] == []
    assert set(summary["docs_fixture_only_shell_response_states"]) == required_states
    assert summary["missing_shell_response_states"] == []
    assert set(summary["missing_runtime_behavior_states"]) == required_states

    assert {"preview_only", "explain_plan", "blocked", "completed", "deferred"}.issubset(
        set(summary["packet_statuses"])
    )
    assert summary["currently_allowed_arc_packet_statuses"] == [
        "preview_only",
        "explain_plan",
        "blocked",
        "deferred",
    ]
    assert summary["kernel_status_mappings"]["proposed"] == "preview_only"
    assert summary["kernel_status_mappings"]["needs_review"] == "explain_plan"
    assert summary["kernel_status_mappings"]["blocked"] == "blocked"

    assert summary["haptic_intent_metadata_supported"] is False
    assert summary["shell_owns_haptics"] is True
    assert summary["lima_owns_haptic_device_behavior"] is False
    assert summary["completed_status_currently_runtime_backed"] is False


def test_arc_bot_shell_intake_accepts_and_rejects_correct_claims() -> None:
    summary = _load_json(FIXTURE_PATH)

    assert summary["proof_accepted_as_static_shell_evidence"] is True
    assert summary["proof_accepted_as_live_runtime_parity"] is False
    assert summary["destructive_edit_delete_requires_operator_approval"] is True
    assert (
        summary["destructive_edit_delete_current_behavior"]
        == "blocked_until_future_operator_approval_and_guardian_gate"
    )
    assert summary["approval_enforcement_status"] == "docs_only_blocked_no_real_enforcement"
    assert summary["guardian_decision_status"] == "docs_only_future_required_missing_real_authority"
    assert summary["provider_model_routing_status"] == (
        "absent_docs_only_blocked_no_provider_model_routing"
    )
    assert summary["audit_evidence_status"] == "static_only_reference_based_no_durable_persistence"
    assert summary["raw_natural_language_to_tool_execution_allowed"] is False

    rejected = set(summary["rejected_claims"])
    assert "live_lima_runtime_parity" in rejected
    assert "runtime_source_backed_arc_shell_behavior" in rejected
    assert "real_approval_enforcement" in rejected
    assert "real_guardian_decision_authority" in rejected
    assert "runtime_export_cleanup_approval" in rejected
    assert "final_api_freeze" in rejected

    blockers = set(summary["blockers"])
    assert "consolidated_v1_g7_closeout_not_complete" in blockers
    assert "real_lima_approval_enforcement_missing" in blockers
    assert "real_lima_guardian_decision_path_missing" in blockers
    assert summary["recommended_next_option"] == "V1-G7X"


def test_arc_bot_shell_intake_docs_state_static_only_verdict() -> None:
    intake_text = DOCS["intake"].read_text(encoding="utf-8")
    audit_text = DOCS["audit"].read_text(encoding="utf-8")
    closeout_text = DOCS["closeout"].read_text(encoding="utf-8")

    assert "LIMA can accept this Arc-Bot-shell packet as static docs/fixture V1-G7 shell evidence." in intake_text
    assert "LIMA cannot treat it as live runtime parity." in intake_text
    assert "API status remains `CANDIDATE_ONLY`" in intake_text
    assert "accept_static_docs_fixture_evidence_only" in audit_text
    assert "Arc-Bot-shell: accepted as static docs/fixture shell evidence." in audit_text
    assert "API status remains: `CANDIDATE_ONLY`." in closeout_text
    assert "Recommended: `V1-G7X`." in closeout_text
