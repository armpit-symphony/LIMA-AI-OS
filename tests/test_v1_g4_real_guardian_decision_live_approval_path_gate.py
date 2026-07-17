"""Static checks for the V1-G4 GuardianDecision/live approval design gate."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = REPO_ROOT / "tests" / "fixtures" / "runtime_extraction"
SUMMARY_PATH = FIXTURE_DIR / "v1_g4_real_guardian_decision_live_approval_path_gate.json"
DOCS = {
    "gate": REPO_ROOT / "docs" / "V1_G4_REAL_GUARDIAN_DECISION_LIVE_APPROVAL_PATH_GATE.md",
    "audit": REPO_ROOT / "docs" / "V1_G4_REAL_GUARDIAN_DECISION_LIVE_APPROVAL_PATH_AUDIT.md",
    "closeout": REPO_ROOT
    / "docs"
    / "V1_G4_REAL_GUARDIAN_DECISION_LIVE_APPROVAL_PATH_CLOSEOUT.md",
}


def _load_json(path: Path) -> dict[str, Any]:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g4_summary_and_docs_exist_and_accept_static_gate_only() -> None:
    summary = _load_json(SUMMARY_PATH)
    assert SUMMARY_PATH.exists()
    for doc_path in DOCS.values():
        assert doc_path.exists()
    assert summary["gap_id"] == "V1-G4"
    assert summary["api_status"] == "CANDIDATE_ONLY"
    assert summary["design_gate_completed"] is True
    assert summary["design_gate_accepted_as_static_evidence"] is True
    assert summary["design_gate_accepted_as_runtime_authority"] is False
    assert summary["v1_product_ready"] is False


def test_v1_g4_summary_tracks_expected_case_fixtures() -> None:
    summary = _load_json(SUMMARY_PATH)
    expected = {
        "tests/fixtures/runtime_extraction/v1_g4_allow_readonly_decision_shape.json",
        "tests/fixtures/runtime_extraction/v1_g4_confirm_destructive_edit_requires_approval.json",
        "tests/fixtures/runtime_extraction/v1_g4_deny_unknown_tool_pack.json",
        "tests/fixtures/runtime_extraction/v1_g4_privileged_breakglass_requires_scope.json",
        "tests/fixtures/runtime_extraction/v1_g4_expired_decision_rejected.json",
        "tests/fixtures/runtime_extraction/v1_g4_revoked_approval_rejected.json",
        "tests/fixtures/runtime_extraction/v1_g4_block_missing_decision_id.json",
        "tests/fixtures/runtime_extraction/v1_g4_forged_decision_id_fail_closed.json",
    }
    assert set(summary["case_fixture_files"]) == expected
    for relative_path in expected:
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g4_defines_required_outcome_families_and_status_mappings() -> None:
    summary = _load_json(SUMMARY_PATH)
    assert set(summary["future_decision_outcome_families"]) == {
        "allow",
        "confirm",
        "deny",
        "privileged",
        "expired",
        "revoked",
        "blocked",
    }
    mappings = {
        entry["guardian_status"]: entry["v1_outcome_family"]
        for entry in summary["existing_guardian_status_mapping"]
    }
    assert mappings["approved"] == "allow"
    assert mappings["needs_human_confirmation"] == "confirm"
    assert mappings["needs_operator_pin"] == "privileged"
    assert mappings["needs_breakglass"] == "privileged"
    assert mappings["denied"] == "deny"
    assert mappings["expired"] == "expired"
    assert mappings["revoked"] == "revoked"
    assert mappings["superseded"] == "blocked"
    assert mappings["needs_clarification"] == "blocked"
    assert mappings["escalated"] == "blocked"


def test_v1_g4_records_required_future_decision_scope_and_runtime_rules() -> None:
    summary = _load_json(SUMMARY_PATH)
    scope_fields = set(summary["required_future_decision_scope_fields"])
    assert {
        "decision_id",
        "actor_id",
        "shell_id",
        "input_id",
        "intent_id",
        "action_type",
        "target_ref",
        "allowed_tool_packs",
        "risk_class",
        "approval_level",
        "expires_at",
        "constraints",
        "policy_version",
    }.issubset(scope_fields)
    runtime_rules = set(summary["required_future_runtime_rules"])
    assert "decision_id_required_before_consequential_execution" in runtime_rules
    assert "approval_metadata_required_for_high_critical_or_destructive_actions" in runtime_rules
    assert "approval_metadata_never_replaces_guardian_decision" in runtime_rules
    assert "decision_scope_must_match_action_scope" in runtime_rules
    assert "expired_revoked_superseded_or_denied_decisions_do_not_execute" in runtime_rules
    assert "missing_forged_reused_or_scope_mismatched_decision_ids_fail_closed" in runtime_rules
    assert "downstream_events_must_carry_decision_id_when_runtime_exists" in runtime_rules


def test_v1_g4_packet_mapping_adds_no_execute_ready_state() -> None:
    summary = _load_json(SUMMARY_PATH)
    mappings = {
        entry["v1_outcome_family"]: entry
        for entry in summary["v1_outcome_to_packet_status"]
    }
    assert mappings["allow"]["packet_status"] == "preview_only"
    assert mappings["confirm"]["packet_status"] == "explain_plan"
    for outcome in ("privileged", "deny", "expired", "revoked", "blocked"):
        assert mappings[outcome]["packet_status"] == "blocked"
    for entry in mappings.values():
        assert entry["runtime_execute_ready_packet_added"] is False


def test_v1_g4_summary_boundary_results_add_no_runtime_behavior() -> None:
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
        "guardian_decision_runtime_added",
        "approval_enforcement_added",
        "approval_token_issuance_added",
        "approval_granted_by_gate",
        "execution_dispatch_persistence_added",
        "browser_file_network_device_robotics_behavior_added",
        "haptic_device_behavior_added",
        "runtime_export_cleanup_approved",
        "final_freeze_approved",
    ):
        assert summary[key] is False


def test_v1_g4_docs_state_static_only_verdict_and_next_gap() -> None:
    gate_text = DOCS["gate"].read_text(encoding="utf-8")
    audit_text = DOCS["audit"].read_text(encoding="utf-8")
    closeout_text = DOCS["closeout"].read_text(encoding="utf-8")
    assert "`V1-G4` is complete as a static design gate" in gate_text
    assert "no real `decision_id` is issued" in gate_text
    assert "Verdict: `accept_static_guardian_decision_live_approval_path_gate_only`." in audit_text
    assert "Recommended: `V1-G5`." in closeout_text
