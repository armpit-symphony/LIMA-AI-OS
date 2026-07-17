"""Static checks for the V1-G19 live approval evidence/capture request."""

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
    / "v1_g19_live_approval_evidence_capture_approval_request.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g19_request_docs_and_fixture_exist() -> None:
    fixture = _load_fixture()

    assert fixture["gate_id"] == "v1_g19_live_approval_evidence_capture_approval_request"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "prepare-v1-g19-live-approval-evidence-capture-approval-request"

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g19_has_no_implementation_approval_yet() -> None:
    fixture = _load_fixture()
    decision = fixture["decision_record"]

    assert fixture["implementation_approved"] is False
    assert fixture["operator_approval_recorded"] is False
    assert fixture["live_approval_evidence_capture_behavior_added"] is False
    assert fixture["raw_pin_verification_added"] is False
    assert fixture["raw_pin_persistence_added"] is False
    assert fixture["approval_token_issuance_added"] is False
    assert fixture["execution_authority_added"] is False
    assert decision["recorded_choice"] == "none"
    assert decision["approved_implementation_branch"] == "none"
    assert decision["implementation_approved"] is False


def test_v1_g19_exact_decision_options_are_locked() -> None:
    fixture = _load_fixture()

    assert fixture["valid_operator_choices"] == [
        "Approve-V1-G19",
        "Revise-V1-G19",
        "Pause",
    ]
    assert fixture["required_approval_wording"].startswith(
        "I explicitly approve V1-G19 implementation"
    )
    assert fixture["proposed_implementation_branch"] == (
        "v1-g19-live-approval-evidence-capture"
    )


def test_v1_g19_approval_evidence_families_are_represented() -> None:
    families = set(_load_fixture()["approval_evidence_families"])

    assert "approval_challenge_metadata" in families
    assert "approver_actor_session_tenant_shell_scope_metadata" in families
    assert "approval_intent_action_scope_metadata" in families
    assert "approval_factor_result_metadata_without_raw_factors" in families
    assert "approval_freshness_expiration_metadata" in families
    assert "replay_prevention_metadata" in families
    assert "denied_revoked_stale_expired_superseded_blocked_outcomes" in families
    assert "approval_to_audit_evidence_linkage_metadata" in families
    assert "destructive_file_mutation_approval_evidence_metadata" in families


def test_v1_g19_required_artifact_fields_are_present() -> None:
    fields = set(_load_fixture()["required_artifact_fields"])

    assert "approval_evidence_id" in fields
    assert "approval_challenge_id" in fields
    assert "request_or_guardian_decision_linkage" in fields
    assert "tenant_scope" in fields
    assert "shell_scope" in fields
    assert "actor_scope" in fields
    assert "session_scope" in fields
    assert "approver_actor_ref" in fields
    assert "approval_intent_scope" in fields
    assert "action_risk_class" in fields
    assert "action_family" in fields
    assert "approval_outcome" in fields
    assert "approval_freshness_status" in fields
    assert "approval_expiration_metadata" in fields
    assert "replay_prevention_metadata" in fields
    assert "factor_evidence_summary" in fields
    assert "capture_source_metadata" in fields
    assert "audit_evidence_linkage" in fields
    assert "proof_not_authority_confirmation" in fields
    assert "no_raw_pin_token_secret_customer_data_confirmation" in fields
    assert "no_approval_token_issuance_confirmation" in fields
    assert "no_execution_authority_confirmation" in fields


def test_v1_g19_outcome_values_are_locked() -> None:
    assert _load_fixture()["normalized_approval_outcomes"] == [
        "approved",
        "denied",
        "revoked",
        "stale",
        "expired",
        "superseded",
        "blocked",
    ]


def test_v1_g19_forbidden_boundaries_remain_false() -> None:
    fixture = _load_fixture()

    assert fixture["raw_pin_verification_added"] is False
    assert fixture["raw_pin_persistence_added"] is False
    assert fixture["approval_token_issuance_added"] is False
    assert fixture["execution_authority_added"] is False
    assert fixture["consumer_repo_mutation_added"] is False
    assert fixture["consumer_integration_added"] is False
    assert fixture["consumer_runtime_calls_added"] is False
    assert fixture["provider_model_routing_added"] is False
    assert fixture["connector_browser_network_file_device_robotics_physical_world_behavior_added"] is False
    assert fixture["final_api_freeze_approved"] is False
    assert fixture["product_ready"] is False


def test_v1_g19_docs_contain_approval_boundary_language() -> None:
    fixture = _load_fixture()
    approval_text = (REPO_ROOT / fixture["documents"]["approval_request"]).read_text(
        encoding="utf-8"
    )
    decision_text = (REPO_ROOT / fixture["documents"]["operator_decision_packet"]).read_text(
        encoding="utf-8"
    )

    assert "raw PIN verification" in approval_text
    assert "approval-token issuance" in approval_text
    assert "proof-not-authority confirmation" in approval_text
    assert "Do not verify raw PINs" in decision_text
    assert "Recorded choice: none" in decision_text
    assert "Recorded choice: Approve-V1-G19" in decision_text
