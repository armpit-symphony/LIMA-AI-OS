"""Runtime tests for the approved V1-G15 guiderail contract slice."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from lima.shells.contracts import (
    V1GuiderailInputError,
    validate_v1_shell_harness_guiderail_input,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g15_shell_harness_guiderail_contract.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _guiderail_input(**overrides: Any) -> dict[str, Any]:
    record = {
        "capability_profile": {
            "profile_id": "sparkbot-shell-candidate",
            "capability_lanes": [
                "informational",
                "planning",
                "file_mutation",
                "provider_model",
                "connector",
                "browser_network",
                "physical_world",
            ],
        },
        "guardrail_mode": "approval_required",
        "approval_policy": {
            "policy_id": "policy:v1-g15",
            "default_decision": "require_approval",
        },
        "actor_scope": "actor:user-123",
        "session_scope": "session:local",
        "tenant_scope": "tenant:alpha",
        "shell_scope": "shell:sparkbot-shell",
        "allowed_capability_lanes": [
            "informational",
            "planning",
            "file_mutation",
            "provider_model",
            "connector",
            "browser_network",
            "physical_world",
        ],
        "destructive_edit_delete_policy": {
            "requires_explicit_approval": True,
            "mutation_without_approval_allowed": False,
        },
        "file_mutation_policy": {
            "requires_explicit_approval": True,
            "execution_allowed_without_future_policy": False,
        },
        "provider_model_policy": {
            "policy_metadata_only": True,
            "execution_allowed": False,
        },
        "connector_policy": {
            "policy_metadata_only": True,
            "execution_allowed": False,
        },
        "browser_network_policy": {
            "policy_metadata_only": True,
            "execution_allowed": False,
        },
        "physical_world_policy": {
            "mode": "blocked_until_dedicated_authority_lane",
            "execution_allowed": False,
        },
        "emergency_stop_expectations": {
            "represented": True,
            "required_for_physical_world": True,
        },
        "rollback_expectations": {
            "represented": True,
            "required_for_mutation": True,
        },
        "dry_run_vs_execution_authorized_posture": "dry_run",
        "operator_approval_evidence_expectations": {
            "represented": True,
            "required_for_destructive": True,
        },
        "audit_evidence_linkage_expectations": {
            "represented": True,
            "lineage_required": True,
        },
        "evidence_refs": ["fixture:v1-g15"],
    }
    record.update(overrides)
    return record


def test_v1_g15_fixture_records_approved_scope_and_boundaries() -> None:
    fixture = _load_fixture()

    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g15-shell-harness-guiderail-contract"
    assert fixture["operator_decision"] == "Approve-V1-G15"
    assert fixture["approved_scope"] == "shell_harness_guiderail_input_contract_slice"
    assert set(fixture["runtime_symbols"]) == {
        "V1GuiderailInputError",
        "validate_v1_shell_harness_guiderail_input",
    }
    assert fixture["capability_open"] is True
    assert fixture["authority_gated"] is True
    assert all(value is False for value in fixture["forbidden_behavior"].values())


def test_v1_g15_valid_guiderail_input_normalizes_contract_metadata() -> None:
    normalized = validate_v1_shell_harness_guiderail_input(_guiderail_input())

    assert normalized["record_type"] == "v1_shell_harness_guiderail_input"
    assert normalized["schema_version"] == "v1-g15-candidate"
    assert normalized["guardrail_mode"] == "approval_required"
    assert normalized["actor_scope"] == "actor:user-123"
    assert normalized["tenant_scope"] == "tenant:alpha"
    assert normalized["capability_open"] is True
    assert normalized["authority_gated"] is True
    assert normalized["execution_allowed"] is False
    assert normalized["side_effects_allowed"] is False
    assert normalized["provider_model_routed"] is False
    assert normalized["connector_invoked"] is False
    assert normalized["file_mutation_executed"] is False
    assert normalized["physical_world_invoked"] is False
    assert normalized["consumer_integration_added"] is False
    assert normalized["final_api_freeze_approved"] is False
    assert normalized["product_ready"] is False


@pytest.mark.parametrize(
    "field",
    [
        "capability_profile",
        "guardrail_mode",
        "approval_policy",
        "actor_scope",
        "session_scope",
        "tenant_scope",
        "shell_scope",
        "allowed_capability_lanes",
        "destructive_edit_delete_policy",
        "file_mutation_policy",
        "provider_model_policy",
        "connector_policy",
        "browser_network_policy",
        "physical_world_policy",
        "emergency_stop_expectations",
        "rollback_expectations",
        "dry_run_vs_execution_authorized_posture",
        "operator_approval_evidence_expectations",
        "audit_evidence_linkage_expectations",
    ],
)
def test_v1_g15_required_contract_fields_fail_closed(field: str) -> None:
    record = _guiderail_input()
    del record[field]

    with pytest.raises(V1GuiderailInputError, match=field):
        validate_v1_shell_harness_guiderail_input(record)


def test_v1_g15_capability_profile_must_match_allowed_lanes() -> None:
    record = _guiderail_input(
        capability_profile={
            "profile_id": "sparkbot-shell-candidate",
            "capability_lanes": ["file_mutation", "connector"],
        },
        allowed_capability_lanes=["file_mutation"],
    )

    with pytest.raises(V1GuiderailInputError, match="capability_profile"):
        validate_v1_shell_harness_guiderail_input(record)


def test_v1_g15_destructive_edit_delete_policy_requires_approval() -> None:
    record = _guiderail_input(
        destructive_edit_delete_policy={
            "requires_explicit_approval": False,
            "mutation_without_approval_allowed": False,
        }
    )

    with pytest.raises(V1GuiderailInputError, match="explicit approval"):
        validate_v1_shell_harness_guiderail_input(record)


def test_v1_g15_file_mutation_policy_requires_future_policy_for_execution() -> None:
    record = _guiderail_input(
        file_mutation_policy={
            "requires_explicit_approval": True,
            "execution_allowed_without_future_policy": True,
        }
    )

    with pytest.raises(V1GuiderailInputError, match="future policy"):
        validate_v1_shell_harness_guiderail_input(record)


@pytest.mark.parametrize(
    "field",
    ["provider_model_policy", "connector_policy", "browser_network_policy"],
)
def test_v1_g15_powerful_lanes_are_policy_metadata_only(field: str) -> None:
    record = _guiderail_input(**{field: {"policy_metadata_only": True, "execution_allowed": False}})
    normalized = validate_v1_shell_harness_guiderail_input(record)

    assert normalized[field]["policy_metadata_only"] is True
    assert normalized[field]["execution_allowed"] is False
    assert normalized["execution_allowed"] is False


@pytest.mark.parametrize(
    "field",
    ["provider_model_policy", "connector_policy", "browser_network_policy"],
)
def test_v1_g15_powerful_lanes_cannot_allow_execution(field: str) -> None:
    record = _guiderail_input(**{field: {"policy_metadata_only": True, "execution_allowed": True}})

    with pytest.raises(V1GuiderailInputError, match="runtime authority"):
        validate_v1_shell_harness_guiderail_input(record)


def test_v1_g15_physical_world_policy_remains_blocked_until_dedicated_lane() -> None:
    record = _guiderail_input(
        physical_world_policy={
            "mode": "blocked_until_dedicated_authority_lane",
            "execution_allowed": False,
        }
    )
    normalized = validate_v1_shell_harness_guiderail_input(record)

    assert normalized["physical_world_policy"]["mode"] == (
        "blocked_until_dedicated_authority_lane"
    )
    assert normalized["physical_world_invoked"] is False


def test_v1_g15_emergency_stop_and_rollback_are_required_for_consequential_lanes() -> None:
    record = _guiderail_input(emergency_stop_expectations={"represented": False})

    with pytest.raises(V1GuiderailInputError, match="emergency stop"):
        validate_v1_shell_harness_guiderail_input(record)

    record = _guiderail_input(rollback_expectations={"represented": False})
    with pytest.raises(V1GuiderailInputError, match="rollback"):
        validate_v1_shell_harness_guiderail_input(record)


def test_v1_g15_approval_evidence_and_audit_linkage_are_required() -> None:
    record = _guiderail_input(
        operator_approval_evidence_expectations={"represented": False}
    )
    with pytest.raises(V1GuiderailInputError, match="approval evidence"):
        validate_v1_shell_harness_guiderail_input(record)

    record = _guiderail_input(audit_evidence_linkage_expectations={"represented": False})
    with pytest.raises(V1GuiderailInputError, match="audit/evidence"):
        validate_v1_shell_harness_guiderail_input(record)


@pytest.mark.parametrize(
    "field,value",
    [
        ("raw_secret", "raw-secret-123"),
        ("raw_prompt", "raw prompt text"),
        ("raw_file_contents", "raw file contents"),
        ("raw_approval_pin", "approval-pin-123456"),
        ("raw_approval_token", "approval token value"),
        ("raw_customer_data", "raw customer data"),
    ],
)
def test_v1_g15_raw_sensitive_content_fails_closed(field: str, value: str) -> None:
    record = _guiderail_input(**{field: value})

    with pytest.raises(V1GuiderailInputError, match="raw sensitive"):
        validate_v1_shell_harness_guiderail_input(record)


@pytest.mark.parametrize(
    "field",
    [
        "execution_allowed",
        "side_effects_allowed",
        "provider_model_routed",
        "connector_invoked",
        "browser_action_executed",
        "network_action_executed",
        "file_mutation_executed",
        "physical_world_invoked",
        "humaninput_bridge_activated",
        "consumer_integration_added",
        "final_api_freeze_approved",
        "product_ready",
    ],
)
def test_v1_g15_runtime_authority_claims_fail_closed(field: str) -> None:
    record = _guiderail_input(**{field: True})

    with pytest.raises(V1GuiderailInputError, match="runtime authority"):
        validate_v1_shell_harness_guiderail_input(record)


def test_v1_g15_output_does_not_emit_sensitive_values() -> None:
    normalized = validate_v1_shell_harness_guiderail_input(_guiderail_input())
    output = json.dumps(normalized, sort_keys=True, default=str)

    for forbidden in (
        "raw-secret-123",
        "approval-pin",
        "approval token",
        "raw prompt",
        "raw file contents",
        "raw customer data",
    ):
        assert forbidden not in output
