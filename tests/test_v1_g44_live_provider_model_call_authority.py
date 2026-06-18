"""Runtime tests for the approved V1-G44 live provider/model call authority slice."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from lima.harness.v1_live_provider_model_call_authority import (
    V1LiveProviderModelCallAuthorityError,
    validate_v1_live_provider_model_call_authority,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g44_live_provider_model_call_authority.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _authority_metadata(**overrides: Any) -> dict[str, Any]:
    record = {
        "authority_id": "authority:v1-g44:001",
        "request_or_guardian_decision_linkage": {
            "request_id": "request:v1-g44:001",
            "guardian_decision_id": "decision:v1-g44:001",
            "linkage_required": True,
            "proof_not_execution": True,
            "grants_execution_authority": False,
        },
        "tenant_scope": "tenant:alpha",
        "shell_scope": "shell:sparkbot-shell",
        "actor_scope": "actor:user-123",
        "session_scope": "session:local",
        "source_provider_model_route_authority_ref": "route:v1-g20:001",
        "source_provider_model_dispatch_evidence_ref": (
            "provider-model-dispatch:v1-g43:fake-provider:001"
        ),
        "provider_id": "provider:openai:metadata-ref",
        "model_id": "model:gpt-class",
        "model_role": "primary",
        "provider_boundary_metadata": {
            "provider_boundary_ref": "provider-boundary:v1-g44:openai",
            "provider_class": "hosted_api_metadata",
            "provider_configured_for_scope": True,
            "live_provider_call_authority_policy_bound": True,
            "live_provider_call_execution_allowed": False,
            "provider_readiness_network_check_allowed": False,
            "token_guardian_live_routing_allowed": False,
            "proof_not_execution": True,
        },
        "credential_reference_metadata": {
            "credential_ref": "vault-ref:metadata/openai-live-call",
            "provider_is_no_key_local": False,
            "reference_only": True,
            "secret_lookup_performed": False,
            "credential_value_accessed": False,
            "raw_secret_present": False,
            "credential_value_present": False,
            "provider_token_present": False,
        },
        "network_policy_reference_metadata": {
            "network_policy_ref": "network-policy:v1-g44:provider-egress",
            "reference_only": True,
            "network_scope_bound": True,
            "network_call_performed": False,
            "provider_endpoint_resolution_performed": False,
            "proof_not_execution": True,
        },
        "prompt_reference_metadata": {
            "prompt_ref": "prompt-ref:v1-g44:redacted-summary",
            "prompt_context_class": "redacted_summary",
            "reference_only": True,
            "redacted": True,
            "raw_prompt_present": False,
            "raw_customer_data_present": False,
        },
        "output_handling_policy": {
            "output_policy_ref": "output-policy:v1-g44:redacted",
            "audit_output_ref": "audit-output:v1-g44:redacted-summary",
            "redacted_output_required": True,
            "raw_model_response_present": False,
            "persist_raw_model_response": False,
            "proof_not_execution": True,
        },
        "data_sensitivity": "internal",
        "budget_class": "medium",
        "estimated_cost_class": "low",
        "latency_tier": "interactive",
        "approval_evidence_linkage": {
            "approval_required_by_policy": True,
            "approval_evidence_ref": "approval-evidence:v1-g44:001",
            "approval_evidence_current": True,
            "proof_not_execution": True,
            "grants_execution_authority": False,
        },
        "audit_evidence_linkage": {
            "audit_record_ref": "audit:v1-g44:live-provider-call-authority",
            "evidence_refs": [
                "route:v1-g20:001",
                "provider-model-dispatch:v1-g43:fake-provider:001",
            ],
            "required": True,
            "proof_not_execution": True,
        },
        "proof_not_execution_confirmation": True,
        "no_raw_prompt_model_response_customer_data_confirmation": True,
        "no_secret_lookup_confirmation": True,
        "no_credential_value_access_confirmation": True,
        "no_network_call_confirmation": True,
        "no_live_provider_call_execution_confirmation": True,
        "no_fallback_execution_confirmation": True,
    }
    record.update(overrides)
    return record


def test_v1_g44_fixture_records_approved_scope_and_boundaries() -> None:
    fixture = _load_fixture()

    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g44-live-provider-model-call-authority"
    assert fixture["operator_decision"] == "Approve-V1-G44"
    assert fixture["approved_scope"] == (
        "live_provider_model_call_authority_metadata_preflight_slice"
    )
    assert set(fixture["runtime_symbols"]) == {
        "V1LiveProviderModelCallAuthorityError",
        "validate_v1_live_provider_model_call_authority",
    }
    assert fixture["live_provider_model_call_authority_runtime_behavior_added"] is True
    assert fixture["non_executing_authority_validator_added"] is True
    assert fixture["frozen_public_api_export_surface_changed"] is False
    assert fixture["harness_all_exports_changed"] is False
    assert fixture["future_export_cleanup_required"] is True
    assert all(value is False for value in fixture["forbidden_behavior"].values())


def test_v1_g44_approved_file_scope_is_exact() -> None:
    fixture = _load_fixture()

    assert fixture["approved_lima_files_changed"] == [
        "lima/harness/v1_live_provider_model_call_authority.py",
        "docs/V1_G44_LIVE_PROVIDER_MODEL_CALL_AUTHORITY.md",
        "docs/V1_G44_LIVE_PROVIDER_MODEL_CALL_AUTHORITY_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g44_live_provider_model_call_authority.json",
        "tests/test_v1_g44_live_provider_model_call_authority.py",
    ]
    assert fixture["approved_consumer_files_changed"] == {}


def test_v1_g44_valid_authority_metadata_normalizes_record() -> None:
    record = validate_v1_live_provider_model_call_authority(_authority_metadata())

    assert record["record_type"] == "v1_live_provider_model_call_authority"
    assert record["schema_version"] == "v1-g44-candidate"
    assert record["authority_id"] == "authority:v1-g44:001"
    assert record["model_role"] == "primary"
    assert record["live_provider_model_call_authority_runtime_behavior"] is True
    assert record["proof_not_execution"] is True
    assert record["non_executing"] is True
    assert record["authority_preflight_metadata_only"] is True
    assert record["live_provider_model_call_execution_added"] is False
    assert record["actual_model_request_dispatch_execution_added"] is False
    assert record["model_request_dispatched"] is False
    assert record["network_call_added"] is False
    assert record["network_call_performed"] is False
    assert record["secret_lookup_added"] is False
    assert record["credential_value_access_added"] is False
    assert record["fallback_execution_added"] is False
    assert record["tool_executed"] is False
    assert record["consumer_integration_added"] is False
    assert record["physical_world_invoked"] is False
    assert record["product_ready"] is False


def test_v1_g44_records_are_deterministic_for_sanitized_metadata() -> None:
    first = validate_v1_live_provider_model_call_authority(_authority_metadata())
    second = validate_v1_live_provider_model_call_authority(_authority_metadata())

    assert first == second
    assert first["record_hash"] == second["record_hash"]


@pytest.mark.parametrize(
    "field",
    [
        "authority_id",
        "request_or_guardian_decision_linkage",
        "tenant_scope",
        "shell_scope",
        "actor_scope",
        "session_scope",
        "source_provider_model_route_authority_ref",
        "source_provider_model_dispatch_evidence_ref",
        "provider_id",
        "model_id",
        "model_role",
        "provider_boundary_metadata",
        "credential_reference_metadata",
        "network_policy_reference_metadata",
        "prompt_reference_metadata",
        "output_handling_policy",
        "data_sensitivity",
        "budget_class",
        "estimated_cost_class",
        "latency_tier",
        "approval_evidence_linkage",
        "audit_evidence_linkage",
        "proof_not_execution_confirmation",
        "no_raw_prompt_model_response_customer_data_confirmation",
        "no_secret_lookup_confirmation",
        "no_credential_value_access_confirmation",
        "no_network_call_confirmation",
        "no_live_provider_call_execution_confirmation",
        "no_fallback_execution_confirmation",
    ],
)
def test_v1_g44_required_authority_fields_fail_closed(field: str) -> None:
    metadata = _authority_metadata()
    del metadata[field]

    with pytest.raises(V1LiveProviderModelCallAuthorityError, match=field):
        validate_v1_live_provider_model_call_authority(metadata)


def test_v1_g44_request_or_decision_linkage_is_required() -> None:
    linkage = dict(_authority_metadata()["request_or_guardian_decision_linkage"])
    linkage["request_id"] = None
    linkage["guardian_decision_id"] = None

    with pytest.raises(
        V1LiveProviderModelCallAuthorityError,
        match="request_id|guardian_decision_id",
    ):
        validate_v1_live_provider_model_call_authority(
            _authority_metadata(request_or_guardian_decision_linkage=linkage)
        )


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("linkage_required", False, "linkage"),
        ("proof_not_execution", False, "execution authority"),
        ("grants_execution_authority", True, "grant execution"),
    ],
)
def test_v1_g44_linkage_metadata_cannot_be_execution_authority(
    field: str,
    value: Any,
    match: str,
) -> None:
    linkage = dict(_authority_metadata()["request_or_guardian_decision_linkage"])
    linkage[field] = value

    with pytest.raises(V1LiveProviderModelCallAuthorityError, match=match):
        validate_v1_live_provider_model_call_authority(
            _authority_metadata(request_or_guardian_decision_linkage=linkage)
        )


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("provider_configured_for_scope", False, "configuration"),
        ("live_provider_call_authority_policy_bound", False, "policy binding"),
        ("live_provider_call_execution_allowed", True, "execution"),
        ("provider_readiness_network_check_allowed", True, "readiness"),
        ("token_guardian_live_routing_allowed", True, "Token Guardian"),
        ("proof_not_execution", False, "execution authority"),
    ],
)
def test_v1_g44_provider_boundary_metadata_fail_closed(
    field: str,
    value: Any,
    match: str,
) -> None:
    boundary = dict(_authority_metadata()["provider_boundary_metadata"])
    boundary[field] = value

    with pytest.raises(V1LiveProviderModelCallAuthorityError, match=match):
        validate_v1_live_provider_model_call_authority(
            _authority_metadata(provider_boundary_metadata=boundary)
        )


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("credential_ref", None, "credential reference"),
        ("reference_only", False, "reference only"),
        ("secret_lookup_performed", True, "secret lookup"),
        ("credential_value_accessed", True, "credential value access"),
        ("raw_secret_present", True, "raw credential"),
        ("credential_value_present", True, "raw credential"),
        ("provider_token_present", True, "provider tokens"),
    ],
)
def test_v1_g44_credential_reference_metadata_fail_closed(
    field: str,
    value: Any,
    match: str,
) -> None:
    credential = dict(_authority_metadata()["credential_reference_metadata"])
    credential[field] = value
    if field == "credential_ref":
        credential["provider_is_no_key_local"] = False

    with pytest.raises(V1LiveProviderModelCallAuthorityError, match=match):
        validate_v1_live_provider_model_call_authority(
            _authority_metadata(credential_reference_metadata=credential)
        )


def test_v1_g44_no_key_local_provider_reference_is_allowed_without_secret_lookup() -> None:
    credential = dict(_authority_metadata()["credential_reference_metadata"])
    credential["credential_ref"] = None
    credential["provider_is_no_key_local"] = True

    record = validate_v1_live_provider_model_call_authority(
        _authority_metadata(credential_reference_metadata=credential)
    )

    assert record["credential_reference_metadata"]["credential_ref"] is None
    assert record["credential_reference_metadata"]["provider_is_no_key_local"] is True
    assert record["secret_lookup_added"] is False


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("network_policy_ref", None, "network_policy_ref"),
        ("reference_only", False, "reference only"),
        ("network_scope_bound", False, "network policy scope"),
        ("network_call_performed", True, "network calls"),
        ("provider_endpoint_resolution_performed", True, "endpoint resolution"),
        ("proof_not_execution", False, "execution authority"),
    ],
)
def test_v1_g44_network_policy_metadata_fail_closed(
    field: str,
    value: Any,
    match: str,
) -> None:
    network = dict(_authority_metadata()["network_policy_reference_metadata"])
    network[field] = value

    with pytest.raises(V1LiveProviderModelCallAuthorityError, match=match):
        validate_v1_live_provider_model_call_authority(
            _authority_metadata(network_policy_reference_metadata=network)
        )


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("prompt_ref", None, "prompt_ref"),
        ("reference_only", False, "reference only"),
        ("redacted", False, "redacted"),
        ("raw_prompt_present", True, "raw prompts"),
        ("raw_customer_data_present", True, "raw customer data"),
    ],
)
def test_v1_g44_prompt_reference_metadata_fail_closed(
    field: str,
    value: Any,
    match: str,
) -> None:
    prompt = dict(_authority_metadata()["prompt_reference_metadata"])
    prompt[field] = value

    with pytest.raises(V1LiveProviderModelCallAuthorityError, match=match):
        validate_v1_live_provider_model_call_authority(
            _authority_metadata(prompt_reference_metadata=prompt)
        )


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("output_policy_ref", None, "output_policy_ref"),
        ("audit_output_ref", None, "audit_output_ref"),
        ("redacted_output_required", False, "redacted output"),
        ("raw_model_response_present", True, "raw model responses"),
        ("persist_raw_model_response", True, "raw model responses"),
        ("proof_not_execution", False, "execution authority"),
    ],
)
def test_v1_g44_output_handling_policy_fail_closed(
    field: str,
    value: Any,
    match: str,
) -> None:
    output = dict(_authority_metadata()["output_handling_policy"])
    output[field] = value

    with pytest.raises(V1LiveProviderModelCallAuthorityError, match=match):
        validate_v1_live_provider_model_call_authority(
            _authority_metadata(output_handling_policy=output)
        )


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("approval_required_by_policy", False, "approval evidence"),
        ("approval_evidence_ref", None, "approval_evidence_ref"),
        ("approval_evidence_current", False, "current"),
        ("proof_not_execution", False, "execution authority"),
        ("grants_execution_authority", True, "grant execution"),
    ],
)
def test_v1_g44_approval_evidence_linkage_fail_closed(
    field: str,
    value: Any,
    match: str,
) -> None:
    approval = dict(_authority_metadata()["approval_evidence_linkage"])
    approval[field] = value

    with pytest.raises(V1LiveProviderModelCallAuthorityError, match=match):
        validate_v1_live_provider_model_call_authority(
            _authority_metadata(approval_evidence_linkage=approval)
        )


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("required", False, "audit/evidence"),
        ("proof_not_execution", False, "execution authority"),
        ("evidence_refs", [], "evidence_refs"),
    ],
)
def test_v1_g44_audit_evidence_linkage_fail_closed(
    field: str,
    value: Any,
    match: str,
) -> None:
    audit = dict(_authority_metadata()["audit_evidence_linkage"])
    audit[field] = value

    with pytest.raises(V1LiveProviderModelCallAuthorityError, match=match):
        validate_v1_live_provider_model_call_authority(
            _authority_metadata(audit_evidence_linkage=audit)
        )


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("model_role", "unknown", "model role"),
        ("data_sensitivity", "secret", "data sensitivity"),
        ("budget_class", "unbounded", "budget class"),
        ("estimated_cost_class", "unbounded", "cost class"),
        ("latency_tier", "instant", "latency tier"),
    ],
)
def test_v1_g44_invalid_enums_fail_closed(
    field: str,
    value: str,
    match: str,
) -> None:
    with pytest.raises(V1LiveProviderModelCallAuthorityError, match=match):
        validate_v1_live_provider_model_call_authority(
            _authority_metadata(**{field: value})
        )


@pytest.mark.parametrize(
    "field",
    [
        "proof_not_execution_confirmation",
        "no_raw_prompt_model_response_customer_data_confirmation",
        "no_secret_lookup_confirmation",
        "no_credential_value_access_confirmation",
        "no_network_call_confirmation",
        "no_live_provider_call_execution_confirmation",
        "no_fallback_execution_confirmation",
    ],
)
def test_v1_g44_required_confirmations_fail_closed(field: str) -> None:
    with pytest.raises(V1LiveProviderModelCallAuthorityError, match=field):
        validate_v1_live_provider_model_call_authority(
            _authority_metadata(**{field: False})
        )


@pytest.mark.parametrize(
    "field",
    [
        "live_provider_model_call_execution_added",
        "live_provider_call_execution_added",
        "live_provider_call_performed",
        "actual_model_request_dispatch_execution_added",
        "model_request_dispatched",
        "network_call_added",
        "network_call_performed",
        "provider_readiness_network_check_added",
        "token_guardian_live_routing_added",
        "secret_lookup_added",
        "secret_lookup_performed",
        "credential_value_access_added",
        "credential_value_accessed",
        "credential_accessed",
        "fallback_execution_added",
        "fallback_executed",
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
        "product_ready",
    ],
)
def test_v1_g44_runtime_execution_claims_fail_closed(field: str) -> None:
    with pytest.raises(V1LiveProviderModelCallAuthorityError, match="runtime execution"):
        validate_v1_live_provider_model_call_authority(
            _authority_metadata(**{field: True})
        )


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("raw_prompt", "raw prompt text"),
        ("raw_model_response", "raw model response text"),
        ("raw_customer_data", "raw customer data"),
        ("credentials", "provider credential value"),
        ("provider_token", "provider token value"),
        ("provider_api_key", "api key value"),
        ("raw_secret", "raw-secret-123"),
    ],
)
def test_v1_g44_raw_sensitive_content_fails_closed(field: str, value: str) -> None:
    with pytest.raises(V1LiveProviderModelCallAuthorityError, match="raw sensitive"):
        validate_v1_live_provider_model_call_authority(
            _authority_metadata(**{field: value})
        )


def test_v1_g44_output_does_not_emit_sensitive_values() -> None:
    record = validate_v1_live_provider_model_call_authority(_authority_metadata())
    output = json.dumps(record, sort_keys=True, default=str)

    for forbidden in (
        "raw prompt",
        "raw model response",
        "raw customer data",
        "provider credential",
        "provider token",
        "api key value",
        "raw-secret-123",
    ):
        assert forbidden not in output


def test_v1_g44_links_required_prior_evidence_documents() -> None:
    fixture = _load_fixture()

    for relative_path in fixture["reviewed_prior_evidence_refs"]:
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g44_docs_contain_boundary_language() -> None:
    implementation_text = (
        REPO_ROOT / "docs" / "V1_G44_LIVE_PROVIDER_MODEL_CALL_AUTHORITY.md"
    ).read_text(encoding="utf-8")
    closeout_text = (
        REPO_ROOT / "docs" / "V1_G44_LIVE_PROVIDER_MODEL_CALL_AUTHORITY_CLOSEOUT.md"
    ).read_text(encoding="utf-8")

    assert "approved LIMA-side live provider/model call authority" in implementation_text
    assert "does not execute live provider/model calls" in implementation_text
    assert "leaves frozen `lima.harness.__all__` unchanged" in implementation_text
    assert "network calls: not approved and not implemented" in implementation_text
    assert "V1-G44 is complete" in closeout_text
    assert "No product-readiness or production-readiness claim" in closeout_text
