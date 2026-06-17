"""Static checks for the V1-G20 provider/model routing authority request."""

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
    / "v1_g20_provider_model_routing_authority_approval_request.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g20_request_docs_and_fixture_exist() -> None:
    fixture = _load_fixture()

    assert fixture["gate_id"] == "v1_g20_provider_model_routing_authority_approval_request"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == (
        "prepare-v1-g20-provider-model-routing-authority-approval-request"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g20_has_no_implementation_approval_yet() -> None:
    fixture = _load_fixture()
    decision = fixture["decision_record"]

    assert fixture["implementation_approved"] is False
    assert fixture["operator_approval_recorded"] is False
    assert fixture["provider_model_routing_authority_behavior_added"] is False
    assert fixture["provider_model_routing_added"] is False
    assert fixture["provider_model_calls_added"] is False
    assert fixture["secret_lookup_added"] is False
    assert fixture["credential_access_added"] is False
    assert fixture["execution_authority_added"] is False
    assert decision["recorded_choice"] == "none"
    assert decision["approved_implementation_branch"] == "none"
    assert decision["implementation_approved"] is False


def test_v1_g20_exact_decision_options_are_locked() -> None:
    fixture = _load_fixture()

    assert fixture["valid_operator_choices"] == [
        "Approve-V1-G20",
        "Revise-V1-G20",
        "Pause",
    ]
    assert fixture["required_approval_wording"].startswith(
        "I explicitly approve V1-G20 implementation"
    )
    assert fixture["proposed_implementation_branch"] == (
        "v1-g20-provider-model-routing-authority"
    )


def test_v1_g20_route_families_are_represented() -> None:
    families = set(_load_fixture()["route_families"])

    assert "primary_model_route" in families
    assert "backup_fallback_route" in families
    assert "heavy_hitter_route" in families
    assert "agent_override_route" in families
    assert "workstation_model_seat_route" in families
    assert "local_endpoint_route" in families
    assert "codex_subscription_route" in families
    assert "provider_readiness_self_inspection_route" in families


def test_v1_g20_required_route_metadata_is_present() -> None:
    fields = set(_load_fixture()["required_route_metadata"])

    assert "route_id" in fields
    assert "route_family" in fields
    assert "route_intent_scope" in fields
    assert "request_or_guardian_decision_linkage" in fields
    assert "tenant_scope" in fields
    assert "shell_scope" in fields
    assert "actor_scope" in fields
    assert "session_scope" in fields
    assert "provider_id" in fields
    assert "model_id" in fields
    assert "model_role" in fields
    assert "provider_boundary_metadata" in fields
    assert "data_sensitivity" in fields
    assert "prompt_context_class" in fields
    assert "requested_tool_packs" in fields
    assert "allowed_tool_packs" in fields
    assert "credential_reference_metadata" in fields
    assert "budget_class" in fields
    assert "estimated_cost_class" in fields
    assert "latency_tier" in fields
    assert "fallback_chain_metadata" in fields
    assert "approval_evidence_linkage_when_required" in fields
    assert "provider_configuration_ref" in fields
    assert "audit_evidence_linkage" in fields
    assert "proof_not_authority_confirmation" in fields
    assert "no_raw_prompt_secret_credential_customer_data_confirmation" in fields
    assert "no_secret_lookup_confirmation" in fields
    assert "no_live_provider_call_confirmation" in fields
    assert "no_execution_authority_confirmation" in fields


def test_v1_g20_required_routing_gates_are_present() -> None:
    gates = set(_load_fixture()["required_routing_gates"])

    assert "shell_allows_model_pack" in gates
    assert "actor_session_policy_allows_model_use" in gates
    assert "guardian_decision_allows_model_routing" in gates
    assert "provider_model_configured_for_shell_room_or_agent" in gates
    assert "credential_reference_is_metadata_only" in gates
    assert "data_sensitivity_allowed_for_provider_class" in gates
    assert "budget_cost_policy_allows_model" in gates
    assert "requested_tool_packs_allowed_by_decision_and_shell_scope" in gates
    assert "fallback_candidates_satisfy_same_gates" in gates
    assert "approval_evidence_present_when_risk_policy_requires" in gates
    assert "audit_evidence_redacted_and_reference_only" in gates
    assert "no_live_provider_call_confirmation" in gates


def test_v1_g20_forbidden_boundaries_remain_false() -> None:
    fixture = _load_fixture()

    assert fixture["provider_model_routing_added"] is False
    assert fixture["provider_model_calls_added"] is False
    assert fixture["provider_readiness_checks_added"] is False
    assert fixture["token_guardian_live_routing_added"] is False
    assert fixture["secret_lookup_added"] is False
    assert fixture["credential_access_added"] is False
    assert fixture["execution_authority_added"] is False
    assert fixture["tool_execution_added"] is False
    assert fixture["consumer_repo_mutation_added"] is False
    assert fixture["consumer_integration_added"] is False
    assert fixture["consumer_runtime_calls_added"] is False
    assert fixture[
        "connector_browser_network_file_device_robotics_physical_world_behavior_added"
    ] is False
    assert fixture["final_api_freeze_approved"] is False
    assert fixture["product_ready"] is False


def test_v1_g20_docs_contain_provider_model_boundary_language() -> None:
    fixture = _load_fixture()
    approval_text = (REPO_ROOT / fixture["documents"]["approval_request"]).read_text(
        encoding="utf-8"
    )
    decision_text = (REPO_ROOT / fixture["documents"]["operator_decision_packet"]).read_text(
        encoding="utf-8"
    )

    assert "live provider/model calls" in approval_text
    assert "secret lookup" in approval_text
    assert "credential reference metadata" in approval_text
    assert "proof-not-authority confirmation" in approval_text
    assert "Do not call providers/models" in decision_text
    assert "Recorded choice: none" in decision_text
    assert "Recorded choice: Approve-V1-G20" in decision_text
