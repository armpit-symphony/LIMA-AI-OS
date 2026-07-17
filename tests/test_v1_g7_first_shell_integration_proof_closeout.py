"""Static checks for the V1-G7 first-shell integration proof closeout."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = REPO_ROOT / "docs" / "V1_G7_FIRST_SHELL_INTEGRATION_PROOF_CLOSEOUT.md"
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g7_first_shell_integration_proof_closeout.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g7_closeout_exists_and_accepts_all_three_shells_static_only() -> None:
    fixture = _load_fixture()
    assert DOC_PATH.exists()
    assert fixture["gap_id"] == "V1-G7"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g7-first-shell-integration-proof-closeout"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["v1_g7_completed_as_static_evidence"] is True
    assert fixture["v1_g7_completed_as_runtime_parity"] is False
    assert fixture["v1_product_ready"] is False
    assert fixture["sparkbot_shell_packet_accepted"] is True
    assert fixture["sparkbot_packet_accepted"] is True
    assert fixture["arc_bot_shell_packet_accepted"] is True
    assert fixture["all_requested_shell_packets_intaken"] is True
    assert fixture["consolidated_v1_g7_closeout_complete"] is True


def test_v1_g7_closeout_records_expected_shell_commits() -> None:
    packets = {packet["shell_repo"]: packet for packet in _load_fixture()["shell_packets"]}
    assert packets["Sparkbot_shell"]["proof_commit"] == "54057a6222dadb898da9389e4b2242554f4c0bf1"
    assert packets["Sparkbot"]["proof_commit"] == "0bb99352a9b62cf1dc35e075c9f3a08054b6bef1"
    assert packets["Arc-Bot-shell"]["proof_commit"] == "67653b2f43095b3807e8b3f7feaf98afda2bb774"
    assert packets["Sparkbot_shell"]["intake_verdict"] == "accept_static_shell_integration_evidence_only"
    assert packets["Sparkbot"]["intake_verdict"] == "accept_static_behavior_reference_evidence_only"
    assert packets["Arc-Bot-shell"]["intake_verdict"] == "accept_static_docs_fixture_evidence_only"


def test_v1_g7_closeout_state_and_mapping_coverage() -> None:
    fixture = _load_fixture()
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
    assert set(fixture["shell_response_states_evaluated_by_all_shells"]) == required_states
    assert set(fixture["runtime_source_backed_shell_states_present_somewhere"]) == required_states
    assert set(fixture["docs_fixture_only_states_present_somewhere"]) == required_states
    assert set(fixture["missing_lima_runtime_behavior_states"]) == required_states

    assert {"preview_only", "explain_plan", "blocked", "completed", "deferred"}.issubset(
        set(fixture["packet_statuses"])
    )
    assert fixture["kernel_status_mappings"]["proposed"] == "preview_only"
    assert fixture["kernel_status_mappings"]["needs_review"] == "explain_plan"
    assert fixture["kernel_status_mappings"]["blocked"] == "blocked"


def test_v1_g7_closeout_preserves_runtime_boundaries() -> None:
    fixture = _load_fixture()
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
        "physical_world_behavior_added",
        "runtime_export_cleanup_approved",
        "final_freeze_approved",
    ):
        assert fixture[key] is False

    assert fixture["shell_owns_haptics"] is True
    assert fixture["lima_owns_haptic_device_behavior"] is False
    assert fixture["destructive_edit_delete_requires_operator_approval_or_block"] is True
    assert fixture["raw_natural_language_to_tool_execution_allowed"] is False


def test_v1_g7_closeout_rejects_live_claims_and_recommends_v1_g8() -> None:
    fixture = _load_fixture()
    rejected = set(fixture["rejected_claims"])
    assert "live_lima_runtime_parity" in rejected
    assert "lima_guardian_decision_authority" in rejected
    assert "lima_approval_enforcement" in rejected
    assert "lima_provider_model_routing" in rejected
    assert "runtime_export_cleanup_approval" in rejected
    assert "final_api_freeze" in rejected
    assert "v1_product_readiness" in rejected

    blockers = set(fixture["remaining_v1_blockers"])
    assert "v1_g8_audit_evidence_persistence_not_complete" in blockers
    assert "durable_lima_audit_persistence_missing" in blockers
    assert "live_lima_runtime_parity_missing" in blockers
    assert fixture["recommended_next_gap_id"] == "V1-G8"

    text = DOC_PATH.read_text(encoding="utf-8")
    assert "complete_static_first_shell_integration_evidence_only" in text
    assert "API status remains: `CANDIDATE_ONLY`." in text
    assert "Recommended: `V1-G8`." in text
