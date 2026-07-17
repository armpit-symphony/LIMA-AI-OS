"""Runtime tests for the approved V1-G20 provider/model routing authority slice."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from lima.harness import (
    V1ProviderModelRoutingAuthorityError,
    validate_v1_provider_model_routing_authority,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g20_provider_model_routing_authority.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _route_metadata(**overrides: Any) -> dict[str, Any]:
    record = {
        "route_id": "route:v1-g20:001",
        "route_family": "primary_model_route",
        "route_intent_scope": {
            "route_intent_ref": "intent:v1-g20:model-route",
            "requested_model_route_ref": "model-route:v1-g20:primary",
            "capability_scope_ref": "capability:model-harness:chat",
            "scope_bound": True,
            "grants_execution_authority": False,
        },
        "request_or_guardian_decision_linkage": {
            "request_id": "v1-request:model-route:001",
            "guardian_decision_id": "v1-decision:model-route:001",
            "linkage_required": True,
            "proof_not_authority": True,
        },
        "tenant_scope": "tenant:alpha",
        "shell_scope": "shell:sparkbot-shell",
        "actor_scope": "actor:user-123",
        "session_scope": "session:local",
        "provider_id": "provider:openai:metadata-ref",
        "model_id": "model:gpt-class",
        "model_role": "primary",
        "provider_boundary_metadata": {
            "provider_boundary_ref": "provider-boundary:v1-g20:openai",
            "provider_class": "hosted_api_metadata",
            "provider_configured_for_scope": True,
            "live_provider_call_allowed": False,
            "provider_readiness_network_check_allowed": False,
            "credential_lookup_allowed": False,
            "proof_not_authority": True,
        },
        "data_sensitivity": "internal",
        "prompt_context_class": "redacted_summary",
        "requested_tool_packs": ["memory"],
        "allowed_tool_packs": ["memory", "files"],
        "credential_reference_metadata": {
            "credential_ref": "vault-ref:metadata/openai-route",
            "provider_is_no_key_local": False,
            "reference_only": True,
            "secret_lookup_performed": False,
            "raw_secret_present": False,
            "credential_value_present": False,
        },
        "budget_class": "medium",
        "estimated_cost_class": "low",
        "latency_tier": "interactive",
        "fallback_chain_metadata": {
            "fallback_chain_ref": "fallback:v1-g20:001",
            "fallback_inherits_same_gates": True,
            "fallback_candidates": [
                {
                    "candidate_ref": "fallback-candidate:v1-g20:backup",
                    "provider_id": "provider:anthropic:metadata-ref",
                    "model_id": "model:backup-class",
                    "route_family": "backup_fallback_route",
                    "inherits_same_gates": True,
                    "secret_lookup_performed": False,
                    "live_provider_call_allowed": False,
                    "fallback_execution_allowed": False,
                }
            ],
        },
        "approval_evidence_linkage_when_required": {
            "approval_required_by_policy": True,
            "approval_evidence_ref": "approval-evidence:v1-g19:001",
            "approval_evidence_current": True,
            "proof_not_authority": True,
            "grants_execution_authority": False,
        },
        "provider_configuration_ref": "provider-config:v1-g20:openai-primary",
        "audit_evidence_linkage": {
            "audit_record_ref": "audit:v1-g20:provider-route",
            "evidence_refs": ["route:v1-g20:001", "fixture:v1-g20"],
            "required": True,
            "proof_not_authority": True,
        },
        "proof_not_authority_confirmation": True,
        "no_raw_prompt_secret_credential_customer_data_confirmation": True,
        "no_secret_lookup_confirmation": True,
        "no_live_provider_call_confirmation": True,
        "no_execution_authority_confirmation": True,
    }
    record.update(overrides)
    return record


def test_v1_g20_fixture_records_approved_scope_and_boundaries() -> None:
    fixture = _load_fixture()

    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g20-provider-model-routing-authority"
    assert fixture["operator_decision"] == "Approve-V1-G20"
    assert fixture["approved_scope"] == "provider_model_routing_authority_metadata_slice"
    assert set(fixture["runtime_symbols"]) == {
        "V1ProviderModelRoutingAuthorityError",
        "validate_v1_provider_model_routing_authority",
    }
    assert fixture["provider_model_routing_authority_runtime_behavior_added"] is True
    assert all(value is False for value in fixture["forbidden_behavior"].values())


def test_v1_g20_valid_route_metadata_normalizes_record() -> None:
    record = validate_v1_provider_model_routing_authority(_route_metadata())

    assert record["record_type"] == "v1_provider_model_routing_authority"
    assert record["schema_version"] == "v1-g20-candidate"
    assert record["route_id"] == "route:v1-g20:001"
    assert record["route_family"] == "primary_model_route"
    assert record["model_role"] == "primary"
    assert record["provider_model_routing_authority_runtime_behavior"] is True
    assert record["proof_not_authority"] is True
    assert record["non_executing"] is True
    assert record["route_metadata_only"] is True
    assert record["provider_model_routing_added"] is False
    assert record["provider_model_calls_added"] is False
    assert record["live_provider_call_performed"] is False
    assert record["model_request_dispatched"] is False
    assert record["fallback_executed"] is False
    assert record["secret_lookup_added"] is False
    assert record["credential_access_added"] is False
    assert record["tool_executed"] is False
    assert record["execution_allowed"] is False
    assert record["consumer_integration_added"] is False
    assert record["physical_world_invoked"] is False


def test_v1_g20_records_are_deterministic_for_sanitized_metadata() -> None:
    first = validate_v1_provider_model_routing_authority(_route_metadata())
    second = validate_v1_provider_model_routing_authority(_route_metadata())

    assert first == second
    assert first["record_hash"] == second["record_hash"]


@pytest.mark.parametrize(
    "field",
    [
        "route_id",
        "route_family",
        "route_intent_scope",
        "request_or_guardian_decision_linkage",
        "tenant_scope",
        "shell_scope",
        "actor_scope",
        "session_scope",
        "provider_id",
        "model_id",
        "model_role",
        "provider_boundary_metadata",
        "data_sensitivity",
        "prompt_context_class",
        "requested_tool_packs",
        "allowed_tool_packs",
        "credential_reference_metadata",
        "budget_class",
        "estimated_cost_class",
        "latency_tier",
        "fallback_chain_metadata",
        "approval_evidence_linkage_when_required",
        "provider_configuration_ref",
        "audit_evidence_linkage",
        "proof_not_authority_confirmation",
        "no_raw_prompt_secret_credential_customer_data_confirmation",
        "no_secret_lookup_confirmation",
        "no_live_provider_call_confirmation",
        "no_execution_authority_confirmation",
    ],
)
def test_v1_g20_required_route_fields_fail_closed(field: str) -> None:
    metadata = _route_metadata()
    del metadata[field]

    with pytest.raises(V1ProviderModelRoutingAuthorityError, match=field):
        validate_v1_provider_model_routing_authority(metadata)


def test_v1_g20_request_or_decision_linkage_is_required() -> None:
    linkage = dict(_route_metadata()["request_or_guardian_decision_linkage"])
    linkage["request_id"] = None
    linkage["guardian_decision_id"] = None

    with pytest.raises(
        V1ProviderModelRoutingAuthorityError,
        match="request_id|guardian_decision_id",
    ):
        validate_v1_provider_model_routing_authority(
            _route_metadata(request_or_guardian_decision_linkage=linkage)
        )


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("linkage_required", False, "linkage"),
        ("proof_not_authority", False, "authority"),
    ],
)
def test_v1_g20_linkage_metadata_cannot_be_authority(
    field: str,
    value: Any,
    match: str,
) -> None:
    linkage = dict(_route_metadata()["request_or_guardian_decision_linkage"])
    linkage[field] = value

    with pytest.raises(V1ProviderModelRoutingAuthorityError, match=match):
        validate_v1_provider_model_routing_authority(
            _route_metadata(request_or_guardian_decision_linkage=linkage)
        )


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("scope_bound", False, "scope"),
        ("grants_execution_authority", True, "grant execution"),
    ],
)
def test_v1_g20_route_intent_scope_fail_closed(
    field: str,
    value: Any,
    match: str,
) -> None:
    intent = dict(_route_metadata()["route_intent_scope"])
    intent[field] = value

    with pytest.raises(V1ProviderModelRoutingAuthorityError, match=match):
        validate_v1_provider_model_routing_authority(
            _route_metadata(route_intent_scope=intent)
        )


@pytest.mark.parametrize(
    "route_family",
    [
        "primary_model_route",
        "backup_fallback_route",
        "heavy_hitter_route",
        "agent_override_route",
        "workstation_model_seat_route",
        "local_endpoint_route",
        "codex_subscription_route",
        "provider_readiness_self_inspection_route",
    ],
)
def test_v1_g20_route_families_are_normalized(route_family: str) -> None:
    record = validate_v1_provider_model_routing_authority(
        _route_metadata(route_family=route_family.replace("_", "-"))
    )

    assert record["route_family"] == route_family


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("route_family", "unknown", "route family"),
        ("model_role", "unknown", "model role"),
        ("data_sensitivity", "secret", "data sensitivity"),
        ("prompt_context_class", "raw_prompt", "raw sensitive|prompt context"),
        ("budget_class", "unbounded", "budget class"),
        ("estimated_cost_class", "unbounded", "cost class"),
        ("latency_tier", "instant", "latency tier"),
    ],
)
def test_v1_g20_invalid_route_enums_fail_closed(
    field: str,
    value: str,
    match: str,
) -> None:
    with pytest.raises(V1ProviderModelRoutingAuthorityError, match=match):
        validate_v1_provider_model_routing_authority(_route_metadata(**{field: value}))


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("provider_configured_for_scope", False, "configuration"),
        ("live_provider_call_allowed", True, "runtime authority|live provider"),
        (
            "provider_readiness_network_check_allowed",
            True,
            "runtime authority|provider readiness",
        ),
        ("credential_lookup_allowed", True, "secret lookup|runtime authority"),
        ("proof_not_authority", False, "authority"),
    ],
)
def test_v1_g20_provider_boundary_metadata_fail_closed(
    field: str,
    value: Any,
    match: str,
) -> None:
    boundary = dict(_route_metadata()["provider_boundary_metadata"])
    boundary[field] = value

    with pytest.raises(V1ProviderModelRoutingAuthorityError, match=match):
        validate_v1_provider_model_routing_authority(
            _route_metadata(provider_boundary_metadata=boundary)
        )


def test_v1_g20_requested_tool_packs_cannot_exceed_allowed_scope() -> None:
    with pytest.raises(V1ProviderModelRoutingAuthorityError, match="tool packs"):
        validate_v1_provider_model_routing_authority(
            _route_metadata(requested_tool_packs=["memory", "admin"])
        )


def test_v1_g20_allowed_tool_pack_scope_is_required() -> None:
    with pytest.raises(V1ProviderModelRoutingAuthorityError, match="allowed_tool_packs"):
        validate_v1_provider_model_routing_authority(
            _route_metadata(allowed_tool_packs=[])
        )


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("credential_ref", None, "credential reference"),
        ("reference_only", False, "reference only"),
        ("secret_lookup_performed", True, "runtime authority|secret lookup"),
        ("raw_secret_present", True, "raw credential|runtime authority"),
        ("credential_value_present", True, "raw credential"),
    ],
)
def test_v1_g20_credential_reference_metadata_fail_closed(
    field: str,
    value: Any,
    match: str,
) -> None:
    credential = dict(_route_metadata()["credential_reference_metadata"])
    credential[field] = value
    if field == "credential_ref":
        credential["provider_is_no_key_local"] = False

    with pytest.raises(V1ProviderModelRoutingAuthorityError, match=match):
        validate_v1_provider_model_routing_authority(
            _route_metadata(credential_reference_metadata=credential)
        )


def test_v1_g20_no_key_local_provider_reference_is_allowed_without_secret_lookup() -> None:
    credential = dict(_route_metadata()["credential_reference_metadata"])
    credential["credential_ref"] = None
    credential["provider_is_no_key_local"] = True

    record = validate_v1_provider_model_routing_authority(
        _route_metadata(credential_reference_metadata=credential)
    )

    assert record["credential_reference_metadata"]["credential_ref"] is None
    assert record["credential_reference_metadata"]["provider_is_no_key_local"] is True
    assert record["secret_lookup_added"] is False


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("fallback_inherits_same_gates", False, "fallback"),
        ("fallback_candidates", [], "fallback_chain_metadata.fallback_candidates"),
    ],
)
def test_v1_g20_fallback_chain_metadata_fail_closed(
    field: str,
    value: Any,
    match: str,
) -> None:
    fallback = dict(_route_metadata()["fallback_chain_metadata"])
    fallback[field] = value

    with pytest.raises(V1ProviderModelRoutingAuthorityError, match=match):
        validate_v1_provider_model_routing_authority(
            _route_metadata(fallback_chain_metadata=fallback)
        )


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("inherits_same_gates", False, "fallback"),
        ("secret_lookup_performed", True, "runtime authority|secret lookup"),
        ("live_provider_call_allowed", True, "runtime authority|live provider"),
        ("fallback_execution_allowed", True, "runtime authority|fallback execution"),
    ],
)
def test_v1_g20_fallback_candidates_inherit_same_gates(
    field: str,
    value: Any,
    match: str,
) -> None:
    fallback = dict(_route_metadata()["fallback_chain_metadata"])
    candidate = dict(fallback["fallback_candidates"][0])
    candidate[field] = value
    fallback["fallback_candidates"] = [candidate]

    with pytest.raises(V1ProviderModelRoutingAuthorityError, match=match):
        validate_v1_provider_model_routing_authority(
            _route_metadata(fallback_chain_metadata=fallback)
        )


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("approval_evidence_ref", None, "approval evidence"),
        ("approval_evidence_current", False, "current"),
        ("proof_not_authority", False, "authority"),
        ("grants_execution_authority", True, "grant execution"),
    ],
)
def test_v1_g20_approval_evidence_linkage_fail_closed(
    field: str,
    value: Any,
    match: str,
) -> None:
    approval = dict(_route_metadata()["approval_evidence_linkage_when_required"])
    approval[field] = value

    with pytest.raises(V1ProviderModelRoutingAuthorityError, match=match):
        validate_v1_provider_model_routing_authority(
            _route_metadata(approval_evidence_linkage_when_required=approval)
        )


def test_v1_g20_approval_evidence_can_be_optional_when_policy_does_not_require_it() -> None:
    approval = dict(_route_metadata()["approval_evidence_linkage_when_required"])
    approval["approval_required_by_policy"] = False
    approval["approval_evidence_ref"] = None
    approval["approval_evidence_current"] = False

    record = validate_v1_provider_model_routing_authority(
        _route_metadata(approval_evidence_linkage_when_required=approval)
    )

    assert record["approval_evidence_linkage_when_required"]["approval_required_by_policy"] is False
    assert record["approval_evidence_linkage_when_required"]["approval_evidence_ref"] is None


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("required", False, "audit/evidence"),
        ("proof_not_authority", False, "authority"),
        ("evidence_refs", [], "evidence_refs"),
    ],
)
def test_v1_g20_audit_evidence_linkage_fail_closed(
    field: str,
    value: Any,
    match: str,
) -> None:
    audit = dict(_route_metadata()["audit_evidence_linkage"])
    audit[field] = value

    with pytest.raises(V1ProviderModelRoutingAuthorityError, match=match):
        validate_v1_provider_model_routing_authority(
            _route_metadata(audit_evidence_linkage=audit)
        )


@pytest.mark.parametrize(
    "field",
    [
        "proof_not_authority_confirmation",
        "no_raw_prompt_secret_credential_customer_data_confirmation",
        "no_secret_lookup_confirmation",
        "no_live_provider_call_confirmation",
        "no_execution_authority_confirmation",
    ],
)
def test_v1_g20_required_confirmations_fail_closed(field: str) -> None:
    with pytest.raises(V1ProviderModelRoutingAuthorityError, match=field):
        validate_v1_provider_model_routing_authority(_route_metadata(**{field: False}))


@pytest.mark.parametrize(
    "field",
    [
        "provider_model_routing_added",
        "provider_model_calls_added",
        "provider_model_call_allowed",
        "live_provider_call_performed",
        "model_request_dispatched",
        "fallback_executed",
        "fallback_execution_allowed",
        "provider_readiness_checks_added",
        "provider_readiness_check_performed",
        "token_guardian_live_routing_added",
        "secret_lookup_added",
        "secret_lookup_performed",
        "credential_access_added",
        "credential_accessed",
        "tool_executed",
        "execution_allowed",
        "side_effects_allowed",
        "action_executed",
        "file_mutation_executed",
        "consumer_repo_mutation_added",
        "consumer_code_imported",
        "consumer_runtime_calls_added",
        "consumer_integration_added",
        "connector_invoked",
        "browser_action_executed",
        "network_action_executed",
        "device_command_invoked",
        "robot_control_invoked",
        "drone_control_invoked",
        "iot_control_invoked",
        "physical_world_invoked",
        "final_api_freeze_approved",
        "product_ready",
    ],
)
def test_v1_g20_runtime_authority_claims_fail_closed(field: str) -> None:
    with pytest.raises(V1ProviderModelRoutingAuthorityError, match="runtime authority"):
        validate_v1_provider_model_routing_authority(_route_metadata(**{field: True}))


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("raw_prompt", "raw prompt text"),
        ("raw_customer_data", "raw customer data"),
        ("raw_customer_context", "raw customer context"),
        ("credentials", "provider credential value"),
        ("provider_token", "provider token value"),
        ("provider_api_key", "api key value"),
        ("raw_secret", "raw-secret-123"),
        ("raw_model_response", "model response text"),
    ],
)
def test_v1_g20_raw_sensitive_content_fails_closed(field: str, value: str) -> None:
    with pytest.raises(V1ProviderModelRoutingAuthorityError, match="raw sensitive"):
        validate_v1_provider_model_routing_authority(_route_metadata(**{field: value}))


def test_v1_g20_output_does_not_emit_sensitive_values() -> None:
    record = validate_v1_provider_model_routing_authority(_route_metadata())
    output = json.dumps(record, sort_keys=True, default=str)

    for forbidden in (
        "raw prompt",
        "raw customer data",
        "raw customer context",
        "provider credential",
        "provider token",
        "api key value",
        "raw-secret-123",
    ):
        assert forbidden not in output
