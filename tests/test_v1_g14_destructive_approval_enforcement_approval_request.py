"""Static checks for the V1-G14 approval-enforcement request gate."""

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
    / "v1_g14_destructive_approval_enforcement_approval_request.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g14_request_docs_and_fixture_exist() -> None:
    fixture = _load_fixture()

    assert fixture["gate_id"] == "v1_g14_destructive_approval_enforcement_approval_request"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g14-destructive-approval-enforcement-approval-request"
    assert fixture["source_branch"] == "v1-g13-readiness-gap-refresh-next-lane-decision-gate"
    assert fixture["source_commit"] == "7d2b736ef522595c23bfc6aa6a1f2787bf6fb203"

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g14_request_adds_no_runtime_or_release_approval() -> None:
    fixture = _load_fixture()
    boundaries = fixture["boundaries"]

    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_behavior_added"] is False
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["operator_approval_recorded"] is False
    assert fixture["runtime_implementation_approved"] is False
    assert fixture["approval_enforcement_added"] is False
    assert boundaries["product_ready"] is False
    assert boundaries["production_ready"] is False
    assert boundaries["runtime_export_cleanup_approved"] is False
    assert boundaries["final_api_freeze_approved"] is False
    assert boundaries["approval_tokens_issued"] is False


def test_v1_g14_operator_decision_packet_has_exact_choices() -> None:
    fixture = _load_fixture()
    decision = fixture["decision_record"]

    assert fixture["valid_operator_choices"] == [
        "Approve-V1-G14",
        "Revise-V1-G14",
        "Pause",
    ]
    assert decision == {
        "recorded_choice": "none",
        "recorded_approval_wording": "none",
        "recorded_revision_request": "none",
        "recorded_pause_reason": "none",
        "approved_implementation_branch": "none",
        "runtime_implementation_approved": False,
    }
    assert fixture["approved_implementation_branch"] == "none"
    assert fixture["proposed_implementation_branch"] == "v1-g14-destructive-approval-enforcement"
    assert fixture["required_approval_wording"].startswith(
        "I explicitly approve V1-G14 implementation"
    )


def test_v1_g14_proposed_file_map_is_narrow() -> None:
    fixture = _load_fixture()

    assert fixture["proposed_runtime_file_map"] == [
        "lima/guardian/v1_approval_enforcement.py",
        "lima/guardian/__init__.py",
    ]
    assert fixture["proposed_docs_tests_fixtures_file_map"] == [
        "docs/V1_G14_DESTRUCTIVE_APPROVAL_ENFORCEMENT.md",
        "docs/V1_G14_DESTRUCTIVE_APPROVAL_ENFORCEMENT_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g14_destructive_approval_enforcement.json",
        "tests/test_v1_g14_destructive_approval_enforcement.py",
    ]


def test_v1_g14_allowed_scope_is_non_executing_approval_enforcement() -> None:
    allowed = set(_load_fixture()["allowed_if_approved"])

    assert "deterministic_local_non_executing_approval_enforcement_gate" in allowed
    assert "v1_g11_request_decision_metadata_validation" in allowed
    assert "destructive_edit_delete_file_mutation_approval_metadata_required" in allowed
    assert "approval_id_required" in allowed
    assert "approval_evidence_ref_required" in allowed
    assert "approving_actor_ref_required" in allowed
    assert "tenant_shell_actor_request_decision_target_linkage_required" in allowed
    assert "approval_enforcement_proof_not_authority" in allowed


def test_v1_g14_forbidden_surfaces_stay_blocked() -> None:
    forbidden = set(_load_fixture()["forbidden"])

    assert "provider_model_calls_or_routing" in forbidden
    assert "tool_execution" in forbidden
    assert "file_mutation_delete_overwrite_or_external_file_action_behavior" in forbidden
    assert "browser_or_network_behavior" in forbidden
    assert "connector_behavior" in forbidden
    assert "shell_runtime_wiring" in forbidden
    assert "humaninput_bridge_activation" in forbidden
    assert "approval_token_issuance" in forbidden
    assert "raw_pin_verification_or_persistence" in forbidden
    assert "audit_metadata_as_execution_authority" in forbidden
    assert "raw_sensitive_content_persistence" in forbidden
    assert "device_robotics_iot_drone_robot_humanoid_physical_world_behavior" in forbidden
    assert "runtime_export_cleanup" in forbidden
    assert "final_api_freeze" in forbidden


def test_v1_g14_required_future_acceptance_tests_cover_fail_closed_cases() -> None:
    required = set(_load_fixture()["required_acceptance_tests_if_approved"])

    assert "destructive_requests_without_approval_metadata_fail_closed" in required
    assert "complete_sanitized_approval_evidence_returns_non_executing_record" in required
    assert "safe_requests_are_not_upgraded" in required
    assert "request_decision_identity_mismatch_fails_closed" in required
    assert "approval_scope_mismatch_fails_closed" in required
    assert "expired_revoked_denied_superseded_stale_replayed_approval_fails_closed" in required
    assert "raw_pin_token_secret_prompt_file_customer_data_fails_closed" in required
    assert "forged_approval_decision_metadata_fails_closed" in required
    assert "forbidden_surface_claims_fail_closed" in required
    assert "approval_enforcement_records_do_not_authorize_execution_or_issue_tokens" in required


def test_v1_g14_docs_match_fixture() -> None:
    fixture = _load_fixture()
    approval_text = (REPO_ROOT / fixture["documents"]["approval_request"]).read_text(
        encoding="utf-8"
    )
    decision_text = (REPO_ROOT / fixture["documents"]["operator_decision_packet"]).read_text(
        encoding="utf-8"
    )
    state_text = (REPO_ROOT / fixture["documents"]["current_state"]).read_text(
        encoding="utf-8"
    )

    assert fixture["required_approval_wording"] in decision_text
    assert "Request verdict: `ready_for_operator_decision_not_approved`" in approval_text
    assert "Recorded choice: none" in decision_text
    assert "Recorded choice: Approve-V1-G14" in decision_text
    assert "V1-G14 - Destructive Approval Enforcement Approval Request" in state_text
