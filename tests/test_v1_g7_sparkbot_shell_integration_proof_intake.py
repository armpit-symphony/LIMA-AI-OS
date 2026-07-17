"""Static checks for the V1-G7 Sparkbot_shell integration proof intake."""

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
    / "v1_g7_sparkbot_shell_integration_proof_intake.json"
)
DOCS = {
    "intake": REPO_ROOT / "docs" / "V1_G7_SPARKBOT_SHELL_INTEGRATION_PROOF_INTAKE.md",
    "audit": REPO_ROOT
    / "docs"
    / "V1_G7_SPARKBOT_SHELL_INTEGRATION_PROOF_INTAKE_AUDIT.md",
    "closeout": REPO_ROOT
    / "docs"
    / "V1_G7_SPARKBOT_SHELL_INTEGRATION_PROOF_INTAKE_CLOSEOUT.md",
}


def _load_json(path: Path) -> dict[str, Any]:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_sparkbot_shell_intake_summary_and_docs_exist() -> None:
    summary = _load_json(FIXTURE_PATH)
    assert FIXTURE_PATH.exists()
    for doc_path in DOCS.values():
        assert doc_path.exists()

    assert summary["gap_id"] == "V1-G7"
    assert summary["shell_repo"] == "Sparkbot_shell"
    assert summary["api_status"] == "CANDIDATE_ONLY"
    assert summary["branch"] == "intake-v1-g7-sparkbot-shell-integration-proof-packet"
    assert summary["source_branch"] == "v1-g7-first-shell-integration-proof-request-gate"
    assert summary["sparkbot_shell_branch"] == "v1-g7-sparkbot-shell-integration-proof-packet"
    assert summary["sparkbot_shell_commit"] == "54057a6222dadb898da9389e4b2242554f4c0bf1"
    assert summary["proof_packet_received"] is True
    assert summary["proof_packet_received_for"] == "Sparkbot_shell"
    assert summary["sparkbot_packet_received"] is False
    assert summary["arc_bot_shell_packet_received"] is False
    assert summary["proof_accepted_as_static_shell_evidence"] is True
    assert summary["proof_accepted_as_live_runtime_parity"] is False
    assert summary["v1_g7_completed"] is False
    assert summary["v1_product_ready"] is False


def test_sparkbot_shell_intake_preserves_boundaries() -> None:
    summary = _load_json(FIXTURE_PATH)
    for key in (
        "runtime_behavior_added",
        "lima_runtime_files_changed",
        "tests_support_changed",
        "runtime_exports_changed",
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
        "physical_world_behavior_added",
        "runtime_export_cleanup_approved",
        "final_freeze_approved",
    ):
        assert summary[key] is False


def test_sparkbot_shell_intake_state_status_and_haptics() -> None:
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
    assert required_states == set(summary["shell_response_states_evaluated"])
    assert {
        "received",
        "thinking",
        "preview_ready",
        "blocked",
        "completed",
        "failed_safe",
        "deferred",
    }.issubset(set(summary["source_backed_shell_response_states"]))
    assert summary["docs_fixture_only_shell_response_states"] == ["needs_approval"]
    assert summary["missing_shell_response_states"] == []

    assert {"preview_only", "explain_plan", "blocked", "completed", "deferred"}.issubset(
        set(summary["packet_statuses"])
    )
    assert summary["kernel_status_mappings"]["proposed"] == "preview_only"
    assert summary["kernel_status_mappings"]["needs_review"] == "explain_plan"
    assert summary["kernel_status_mappings"]["blocked"] == "blocked"

    assert summary["haptic_intent_metadata_supported"] is True
    assert summary["shell_owns_haptics"] is True
    assert summary["lima_owns_haptic_device_behavior"] is False
    assert summary["destructive_edit_delete_requires_operator_approval"] is True
    assert summary["destructive_edit_delete_runtime_present"] is False


def test_sparkbot_shell_intake_accepts_and_rejects_correct_claims() -> None:
    summary = _load_json(FIXTURE_PATH)

    accepted = set(summary["accepted_evidence"])
    assert "Sparkbot_shell proof packet delivered" in accepted
    assert "required response states evaluated" in accepted
    assert "required packet statuses evaluated" in accepted
    assert "haptics remain shell-owned" in accepted

    rejected = set(summary["rejected_claims"])
    assert "live_lima_runtime_parity" in rejected
    assert "real_approval_enforcement" in rejected
    assert "real_guardian_decision_authority" in rejected
    assert "provider_model_runtime_routing" in rejected
    assert "runtime_export_cleanup_approval" in rejected
    assert "final_api_freeze" in rejected

    blockers = set(summary["blockers"])
    assert "sparkbot_v1_g7_packet_not_delivered" in blockers
    assert "arc_bot_shell_v1_g7_packet_not_delivered" in blockers
    assert "consolidated_v1_g7_closeout_not_complete" in blockers


def test_sparkbot_shell_intake_docs_state_static_only_verdict() -> None:
    intake_text = DOCS["intake"].read_text(encoding="utf-8")
    audit_text = DOCS["audit"].read_text(encoding="utf-8")
    closeout_text = DOCS["closeout"].read_text(encoding="utf-8")

    assert "LIMA can accept this Sparkbot_shell packet as static V1-G7 shell integration evidence." in intake_text
    assert "LIMA cannot treat it as live runtime parity." in intake_text
    assert "API status remains `CANDIDATE_ONLY`" in intake_text
    assert "accept_static_shell_integration_evidence_only" in audit_text
    assert "Sparkbot: not yet delivered or audited for V1-G7." in audit_text
    assert "API status remains: `CANDIDATE_ONLY`." in closeout_text
    assert "Recommended: `V1-G7S`." in closeout_text
