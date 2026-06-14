"""Static checks for the V1-G7 first-shell integration proof request gate."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = REPO_ROOT / "tests" / "fixtures" / "runtime_extraction"
SUMMARY_PATH = FIXTURE_DIR / "v1_g7_first_shell_integration_proof_request.json"
DOCS = {
    "request": REPO_ROOT / "docs" / "V1_G7_FIRST_SHELL_INTEGRATION_PROOF_REQUEST.md",
    "audit_criteria": REPO_ROOT
    / "docs"
    / "V1_G7_FIRST_SHELL_INTEGRATION_PROOF_AUDIT_CRITERIA.md",
    "closeout": REPO_ROOT
    / "docs"
    / "V1_G7_FIRST_SHELL_INTEGRATION_PROOF_REQUEST_CLOSEOUT.md",
}


def _load_json(path: Path) -> dict[str, Any]:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g7_request_summary_and_docs_exist() -> None:
    summary = _load_json(SUMMARY_PATH)
    assert SUMMARY_PATH.exists()
    for doc_path in DOCS.values():
        assert doc_path.exists()
    assert summary["gap_id"] == "V1-G7"
    assert summary["api_status"] == "CANDIDATE_ONLY"
    assert summary["request_gate_completed"] is True
    assert summary["v1_g7_completed"] is False
    assert summary["proof_packets_received"] is False
    assert summary["proof_accepted_as_static_shell_evidence"] is False
    assert summary["proof_accepted_as_live_runtime_parity"] is False
    assert summary["v1_product_ready"] is False


def test_v1_g7_request_names_all_first_shells_and_branches() -> None:
    shells = {shell["shell_repo"]: shell for shell in _load_json(SUMMARY_PATH)["requested_shells"]}
    assert set(shells) == {"Sparkbot_shell", "Sparkbot", "Arc-Bot-shell"}
    assert (
        shells["Sparkbot_shell"]["requested_branch"]
        == "v1-g7-sparkbot-shell-integration-proof-packet"
    )
    assert shells["Sparkbot"]["requested_branch"] == "v1-g7-sparkbot-integration-proof-packet"
    assert (
        shells["Arc-Bot-shell"]["requested_branch"]
        == "v1-g7-arc-bot-shell-integration-proof-packet"
    )
    for shell in shells.values():
        assert shell["local_path_present"] is True
        assert shell["proof_packet_received_for_v1_g7"] is False
        assert shell["known_partial_evidence"]


def test_v1_g7_required_state_and_status_coverage_is_defined() -> None:
    summary = _load_json(SUMMARY_PATH)
    assert set(summary["required_response_states"]) == {
        "received",
        "thinking",
        "preview_ready",
        "blocked",
        "needs_approval",
        "completed",
        "failed_safe",
        "deferred",
    }
    assert summary["required_kernel_status_mappings"] == {
        "proposed": "preview_only",
        "needs_review": "explain_plan",
        "blocked": "blocked",
    }
    assert {
        "preview_only",
        "explain_plan",
        "blocked",
        "completed",
        "deferred",
    }.issubset(set(summary["required_packet_statuses"]))


def test_v1_g7_required_machine_readable_fields_cover_integration_boundaries() -> None:
    fields = set(_load_json(SUMMARY_PATH)["required_machine_readable_fields"])
    assert "proof_gap_id" in fields
    assert "shell_repo" in fields
    assert "proof_branch" in fields
    assert "validation_commands" in fields
    assert "can_consume_lima_contract_outputs_as_static_evidence" in fields
    assert "can_consume_lima_runtime_outputs_live" in fields
    assert "lima_runtime_wiring_added" in fields
    assert "runtime_exports_required_from_lima" in fields
    assert "shell_response_states_evaluated" in fields
    assert "haptic_intent_metadata_supported" in fields
    assert "shell_owns_haptics" in fields
    assert "lima_owns_haptic_device_behavior" in fields
    assert "destructive_edit_delete_requires_operator_approval" in fields
    assert "approval_enforcement_status" in fields
    assert "guardian_decision_status" in fields
    assert "provider_model_routing_status" in fields
    assert "audit_evidence_status" in fields
    assert "tool_pack_scope_status" in fields
    assert "connector_file_browser_network_device_robotics_status" in fields
    assert "raw_natural_language_to_tool_execution_allowed" in fields
    assert "production_readiness_claimed" in fields
    assert "v1_product_readiness_claimed" in fields


def test_v1_g7_request_boundaries_add_no_runtime_or_shell_changes() -> None:
    summary = _load_json(SUMMARY_PATH)
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
        "physical_world_behavior_added",
        "runtime_export_cleanup_approved",
        "final_freeze_approved",
    ):
        assert summary[key] is False


def test_v1_g7_rejection_criteria_fail_closed_for_unsafe_claims() -> None:
    criteria = set(_load_json(SUMMARY_PATH)["rejection_criteria"])
    assert "missing_required_response_state" in criteria
    assert "missing_kernel_status_mapping" in criteria
    assert "lima_owned_haptic_device_behavior_claim" in criteria
    assert "destructive_edit_delete_operator_approval_bypass" in criteria
    assert "unsupported_real_approval_enforcement_claim" in criteria
    assert "unsupported_real_guardian_decision_authority_claim" in criteria
    assert "unconstrained_provider_model_routing_claim" in criteria
    assert "raw_natural_language_to_tool_execution_shortcut" in criteria
    assert "unsafe_connector_file_browser_network_device_robotics_claim" in criteria
    assert "production_or_v1_readiness_claim_from_static_evidence" in criteria
    assert "requires_unapproved_lima_runtime_wiring_or_final_freeze" in criteria


def test_v1_g7_docs_state_request_only_and_parallel_shell_recommendation() -> None:
    request_text = DOCS["request"].read_text(encoding="utf-8")
    audit_text = DOCS["audit_criteria"].read_text(encoding="utf-8")
    closeout_text = DOCS["closeout"].read_text(encoding="utf-8")
    assert "This document requests first-shell integration proof packets" in request_text
    assert "`Sparkbot_shell`" in request_text
    assert "`Sparkbot`" in request_text
    assert "`Arc-Bot-shell`" in request_text
    assert "Static acceptance is not live runtime parity." in audit_text
    assert "`V1-G7` request gate is complete." in closeout_text
    assert "Recommended: `V1-G7D`." in closeout_text
