"""Static checks for the V1-G8 audit/evidence persistence contract."""

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
    / "v1_g8_audit_evidence_persistence_contract.json"
)
DOCS = {
    "contract": REPO_ROOT / "docs" / "V1_G8_AUDIT_EVIDENCE_PERSISTENCE_CONTRACT.md",
    "threat_model": REPO_ROOT
    / "docs"
    / "V1_G8_AUDIT_EVIDENCE_PERSISTENCE_THREAT_MODEL.md",
    "closeout": REPO_ROOT / "docs" / "V1_G8_AUDIT_EVIDENCE_PERSISTENCE_CLOSEOUT.md",
}


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g8_contract_documents_exist_and_stay_candidate_only() -> None:
    fixture = _load_fixture()
    assert FIXTURE_PATH.exists()
    for path in DOCS.values():
        assert path.exists()

    assert fixture["gap_id"] == "V1-G8"
    assert fixture["lane_id"] == "V1-G8A"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g8a-audit-evidence-persistence-contract-threat-model"
    assert fixture["static_contract_completed"] is True
    assert fixture["static_threat_model_completed"] is True
    assert fixture["v1_g8_completed_as_static_contract"] is True
    assert fixture["v1_g8_completed_as_runtime_persistence"] is False
    assert fixture["v1_product_ready"] is False


def test_v1_g8_contract_preserves_no_runtime_boundaries() -> None:
    fixture = _load_fixture()
    for key in (
        "durable_audit_persistence_implemented",
        "storage_adapter_added",
        "query_api_added",
        "external_database_writes_added",
        "runtime_behavior_added",
        "lima_runtime_files_changed",
        "tests_support_changed",
        "runtime_exports_changed",
        "shell_wiring_added",
        "provider_model_routing_added",
        "provider_model_calls_added",
        "guardian_decision_runtime_added",
        "approval_enforcement_added",
        "execution_dispatch_persistence_added",
        "browser_file_network_device_robotics_behavior_added",
        "haptic_device_behavior_added",
        "physical_world_behavior_added",
        "runtime_export_cleanup_approved",
        "final_freeze_approved",
    ):
        assert fixture[key] is False


def test_v1_g8_contract_record_families_queries_and_envelopes() -> None:
    fixture = _load_fixture()
    families = set(fixture["record_families"])
    assert "AuditEventRecord" in families
    assert "AuditLineageRecord" in families
    assert "EvidenceArtifactRef" in families
    assert "GuardianDecisionEvidenceRef" in families
    assert "ApprovalEvidenceRef" in families
    assert "ProviderModelRouteEvidenceRef" in families
    assert "ExportReviewRef" in families
    assert "DeletionReviewRef" in families

    envelopes = set(fixture["required_envelopes"])
    assert "privacy_class" in envelopes
    assert "redaction_class" in envelopes
    assert "retention_class" in envelopes
    assert "visibility_class" in envelopes
    assert "contains_secret" in envelopes

    queries = set(fixture["query_keys"])
    assert "lineage_id" in queries
    assert "decision_id" in queries
    assert "approval_id" in queries
    assert "tenant_ref" in queries
    assert "shell_id" in queries
    assert "provider_model_route_ref" in queries
    assert "evidence_ref" in queries


def test_v1_g8_contract_positive_and_negative_cases_cover_v1_risks() -> None:
    fixture = _load_fixture()
    positives = set(fixture["positive_static_cases"])
    assert "low_risk_preview_lineage_reference_only_content" in positives
    assert "model_route_planning_lineage_with_route_evidence_ref" in positives
    assert "destructive_edit_delete_blocked_without_approval_evidence" in positives
    assert "export_delete_request_requires_review_ref" in positives

    negatives = set(fixture["negative_static_cases"])
    assert "consequential_event_without_decision_id" in negatives
    assert "destructive_edit_delete_without_approval_id" in negatives
    assert "raw_secret_inline" in negatives
    assert "raw_pin_token_inline" in negatives
    assert "cross_tenant_query_leakage" in negatives
    assert (
        "connector_file_browser_network_device_robotics_claim_without_guardian_audit_linkage"
        in negatives
    )


def test_v1_g8_threat_model_covers_expected_threats() -> None:
    fixture = _load_fixture()
    threats = set(fixture["threats"])
    assert "audit_record_as_authorization" in threats
    assert "missing_decision_linkage" in threats
    assert "destructive_edit_delete_approval_bypass" in threats
    assert "raw_secret_leakage" in threats
    assert "cross_tenant_query_leakage" in threats
    assert "provider_model_route_evidence_loss" in threats
    assert "shell_over_trust" in threats


def test_v1_g8_contract_accepts_static_only_and_recommends_v1_g9() -> None:
    fixture = _load_fixture()
    accepted = set(fixture["accepted_evidence"])
    assert "static_contract_present" in accepted
    assert "static_threat_model_present" in accepted
    assert "negative_cases_defined_and_statically_tested" in accepted

    rejected = set(fixture["rejected_claims"])
    assert "durable_runtime_audit_persistence" in rejected
    assert "storage_adapter_implementation" in rejected
    assert "live_approval_enforcement" in rejected
    assert "real_guardian_decision_runtime_authority" in rejected
    assert "runtime_export_cleanup_approval" in rejected
    assert "final_api_freeze" in rejected

    blockers = set(fixture["remaining_v1_blockers"])
    assert "durable_lima_audit_persistence_not_implemented" in blockers
    assert "live_query_read_authorization_not_implemented" in blockers
    assert "final_api_freeze_unapproved" in blockers
    assert fixture["recommended_next_gap_id"] == "V1-G9"


def test_v1_g8_contract_docs_state_static_only_verdict() -> None:
    contract_text = DOCS["contract"].read_text(encoding="utf-8")
    threat_text = DOCS["threat_model"].read_text(encoding="utf-8")
    closeout_text = DOCS["closeout"].read_text(encoding="utf-8")

    assert "Audit evidence is proof, not authority." in contract_text
    assert "Durable persistence implemented: no." in contract_text
    assert "T3: Destructive Edit/Delete Approval Bypass" in threat_text
    assert "Verdict: `complete_static_contract_and_threat_model_only`" in closeout_text
    assert "Recommended: `V1-G9`." in closeout_text
