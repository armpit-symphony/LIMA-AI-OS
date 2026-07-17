"""Static checks for the V1-G8 audit/evidence persistence request gate."""

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
    / "v1_g8_audit_evidence_persistence_request_gate.json"
)
DOCS = {
    "request": REPO_ROOT / "docs" / "V1_G8_AUDIT_EVIDENCE_PERSISTENCE_REQUEST_GATE.md",
    "audit_criteria": REPO_ROOT
    / "docs"
    / "V1_G8_AUDIT_EVIDENCE_PERSISTENCE_AUDIT_CRITERIA.md",
    "closeout": REPO_ROOT
    / "docs"
    / "V1_G8_AUDIT_EVIDENCE_PERSISTENCE_REQUEST_CLOSEOUT.md",
}


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g8_request_gate_documents_exist_and_status_is_candidate_only() -> None:
    fixture = _load_fixture()
    assert FIXTURE_PATH.exists()
    for path in DOCS.values():
        assert path.exists()

    assert fixture["gap_id"] == "V1-G8"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g8-audit-evidence-persistence-request-gate"
    assert fixture["source_branch"] == "v1-g7-first-shell-integration-proof-closeout"
    assert fixture["request_gate_completed"] is True
    assert fixture["v1_g8_completed"] is False
    assert fixture["v1_product_ready"] is False


def test_v1_g8_request_gate_preserves_no_runtime_boundaries() -> None:
    fixture = _load_fixture()
    for key in (
        "durable_audit_persistence_implemented",
        "runtime_behavior_added",
        "lima_runtime_files_changed",
        "tests_support_changed",
        "runtime_exports_changed",
        "storage_adapter_added",
        "external_database_writes_added",
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


def test_v1_g8_request_gate_defines_record_families_and_lineage_chain() -> None:
    fixture = _load_fixture()
    families = set(fixture["required_future_record_families"])
    assert "AuditEventRecord" in families
    assert "AuditLineageRecord" in families
    assert "EvidenceArtifactRef" in families
    assert "GuardianDecisionEvidenceRef" in families
    assert "ApprovalEvidenceRef" in families
    assert "ProviderModelRouteEvidenceRef" in families
    assert "ExportReviewRef" in families
    assert "DeletionReviewRef" in families

    chain = fixture["required_lineage_chain"]
    assert chain[0] == "HumanInput"
    assert "IntentEnvelope" in chain
    assert "GuardianDecision" in chain
    assert "ApprovalMetadata_when_required" in chain
    assert chain[-1] == "EvidenceArtifactRef"


def test_v1_g8_request_gate_requires_safe_durable_fields_and_queries() -> None:
    fixture = _load_fixture()
    fields = set(fixture["minimum_durable_fields"])
    assert "lineage_id" in fields
    assert "decision_id" in fields
    assert "approval_id_when_required" in fields
    assert "tenant_or_customer_context_ref" in fields
    assert "actor_or_operator_ref" in fields
    assert "shell_id" in fields
    assert "privacy_class" in fields
    assert "redaction_class" in fields
    assert "retention_class" in fields
    assert "visibility_class" in fields
    assert "content_or_evidence_hash" in fields

    queries = set(fixture["required_query_capabilities"])
    assert "lineage_id" in queries
    assert "decision_id" in queries
    assert "approval_id" in queries
    assert "tenant_or_customer_context_ref" in queries
    assert "provider_model_route_ref" in queries
    assert "evidence_ref" in queries


def test_v1_g8_request_gate_negative_cases_cover_v1_risks() -> None:
    fixture = _load_fixture()
    cases = set(fixture["required_negative_cases"])
    assert "consequential_event_without_decision_id" in cases
    assert "destructive_edit_delete_without_approval_metadata" in cases
    assert "raw_secret_inline" in cases
    assert "raw_approval_token_or_pin_inline" in cases
    assert "provider_model_route_without_evidence_ref" in cases
    assert "cross_tenant_query_leakage" in cases
    assert "unknown_privacy_class_treated_as_safe" in cases
    assert (
        "connector_file_browser_network_device_robotics_execution_without_guardian_decision"
        in cases
    )


def test_v1_g8_request_gate_shell_relevance_and_next_step() -> None:
    fixture = _load_fixture()
    shell_relevance = fixture["shell_relevance"]
    assert set(shell_relevance) == {"Sparkbot_shell", "Sparkbot", "Arc-Bot-shell"}
    assert "haptic_intent_evidence_refs" in shell_relevance["Sparkbot_shell"]
    assert "provider_model_route_refs" in shell_relevance["Sparkbot"]
    assert "connector_readiness_refs" in shell_relevance["Arc-Bot-shell"]

    assert fixture["recommended_next_option"] == "V1-G8A"
    assert "static audit/evidence persistence contract" in fixture["recommended_next_step"]


def test_v1_g8_request_gate_docs_state_request_only_boundary() -> None:
    request_text = DOCS["request"].read_text(encoding="utf-8")
    audit_text = DOCS["audit_criteria"].read_text(encoding="utf-8")
    closeout_text = DOCS["closeout"].read_text(encoding="utf-8")

    assert "This document opens the V1-G8 request gate" in request_text
    assert "It is a request/design gate only." in request_text
    assert "Runtime behavior added: no." in request_text
    assert "Static acceptance is not durable runtime persistence." in audit_text
    assert "`V1-G8` request gate is complete." in closeout_text
    assert "Recommended: `V1-G8A`." in closeout_text
