"""Runtime tests for the approved V1-G19 approval evidence slice."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from lima.guardian import (
    V1LiveApprovalEvidenceError,
    validate_v1_live_approval_evidence_capture,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g19_live_approval_evidence_capture.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _approval_metadata(**overrides: Any) -> dict[str, Any]:
    record = {
        "approval_evidence_id": "approval-evidence:v1-g19:001",
        "approval_challenge_id": "approval-challenge:v1-g19:001",
        "request_or_guardian_decision_linkage": {
            "request_id": "v1-request:file-mutation:001",
            "guardian_decision_id": "v1-decision:file-mutation:001",
            "linkage_required": True,
            "proof_not_authority": True,
        },
        "tenant_scope": "tenant:alpha",
        "shell_scope": "shell:sparkbot-shell",
        "actor_scope": "actor:user-123",
        "session_scope": "session:local",
        "approver_actor_ref": "operator:phil-lima",
        "approval_intent_scope": {
            "intent_ref": "intent:v1-g19:file-mutation",
            "requested_action_ref": "action:v1-g19:delete-file",
            "action_scope_ref": "scope:v1-g19:docs",
            "scope_bound": True,
            "grants_execution_authority": False,
        },
        "action_risk_class": "high",
        "action_family": "destructive_file_mutation",
        "approval_outcome": "approved",
        "approval_freshness_status": "fresh",
        "approval_expiration_metadata": {
            "expires_at_ref": "time-ref:v1-g19:approval-expires",
            "expiration_status": "not_expired",
            "expiration_checked": True,
        },
        "replay_prevention_metadata": {
            "replay_nonce_ref": "nonce:v1-g19:001",
            "replay_status": "not_replayed",
            "replay_checked": True,
        },
        "factor_evidence_summary": {
            "factor_family": "operator_confirmation",
            "factor_result": "passed",
            "raw_factor_value_present": False,
            "redacted_summary_only": True,
        },
        "capture_source_metadata": {
            "capture_source_ref": "shell:sparkbot-shell:approval-modal",
            "capture_channel": "shell_confirmation",
            "source_trusted_by_policy": True,
            "consumer_runtime_invoked": False,
        },
        "audit_evidence_linkage": {
            "audit_record_ref": "audit:v1-g19:approval-evidence",
            "evidence_refs": ["approval-evidence:v1-g19:001", "fixture:v1-g19"],
            "required": True,
            "proof_not_authority": True,
        },
        "proof_not_authority_confirmation": True,
        "no_raw_pin_token_secret_customer_data_confirmation": True,
        "no_approval_token_issuance_confirmation": True,
        "no_execution_authority_confirmation": True,
    }
    record.update(overrides)
    return record


def test_v1_g19_fixture_records_approved_scope_and_boundaries() -> None:
    fixture = _load_fixture()

    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g19-live-approval-evidence-capture"
    assert fixture["operator_decision"] == "Approve-V1-G19"
    assert fixture["approved_scope"] == "live_approval_evidence_capture_metadata_slice"
    assert set(fixture["runtime_symbols"]) == {
        "V1LiveApprovalEvidenceError",
        "validate_v1_live_approval_evidence_capture",
    }
    assert fixture["live_approval_evidence_capture_runtime_behavior_added"] is True
    assert all(value is False for value in fixture["forbidden_behavior"].values())


def test_v1_g19_valid_approval_metadata_normalizes_record() -> None:
    record = validate_v1_live_approval_evidence_capture(_approval_metadata())

    assert record["record_type"] == "v1_live_approval_evidence_capture"
    assert record["schema_version"] == "v1-g19-candidate"
    assert record["approval_evidence_id"] == "approval-evidence:v1-g19:001"
    assert record["approval_challenge_id"] == "approval-challenge:v1-g19:001"
    assert record["approval_outcome"] == "approved"
    assert record["approval_freshness_status"] == "fresh"
    assert record["evidence_is_current"] is True
    assert record["live_approval_evidence_capture_runtime_behavior"] is True
    assert record["proof_not_authority"] is True
    assert record["non_executing"] is True
    assert record["execution_allowed"] is False
    assert record["side_effects_allowed"] is False
    assert record["approval_token_issued"] is False
    assert record["raw_pin_verified"] is False
    assert record["action_executed"] is False
    assert record["file_mutation_executed"] is False
    assert record["consumer_integration_added"] is False
    assert record["provider_model_routed"] is False
    assert record["physical_world_invoked"] is False


def test_v1_g19_records_are_deterministic_for_sanitized_metadata() -> None:
    first = validate_v1_live_approval_evidence_capture(_approval_metadata())
    second = validate_v1_live_approval_evidence_capture(_approval_metadata())

    assert first == second
    assert first["record_hash"] == second["record_hash"]


@pytest.mark.parametrize(
    "field",
    [
        "approval_evidence_id",
        "approval_challenge_id",
        "request_or_guardian_decision_linkage",
        "tenant_scope",
        "shell_scope",
        "actor_scope",
        "session_scope",
        "approver_actor_ref",
        "approval_intent_scope",
        "action_risk_class",
        "action_family",
        "approval_outcome",
        "approval_freshness_status",
        "approval_expiration_metadata",
        "replay_prevention_metadata",
        "factor_evidence_summary",
        "capture_source_metadata",
        "audit_evidence_linkage",
        "proof_not_authority_confirmation",
        "no_raw_pin_token_secret_customer_data_confirmation",
        "no_approval_token_issuance_confirmation",
        "no_execution_authority_confirmation",
    ],
)
def test_v1_g19_required_approval_fields_fail_closed(field: str) -> None:
    metadata = _approval_metadata()
    del metadata[field]

    with pytest.raises(V1LiveApprovalEvidenceError, match=field):
        validate_v1_live_approval_evidence_capture(metadata)


def test_v1_g19_request_or_decision_linkage_is_required() -> None:
    linkage = dict(_approval_metadata()["request_or_guardian_decision_linkage"])
    linkage["request_id"] = None
    linkage["guardian_decision_id"] = None

    with pytest.raises(V1LiveApprovalEvidenceError, match="request_id|guardian_decision_id"):
        validate_v1_live_approval_evidence_capture(
            _approval_metadata(request_or_guardian_decision_linkage=linkage)
        )


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("linkage_required", False, "linkage"),
        ("proof_not_authority", False, "authority"),
    ],
)
def test_v1_g19_linkage_metadata_cannot_be_authority(
    field: str,
    value: Any,
    match: str,
) -> None:
    linkage = dict(_approval_metadata()["request_or_guardian_decision_linkage"])
    linkage[field] = value

    with pytest.raises(V1LiveApprovalEvidenceError, match=match):
        validate_v1_live_approval_evidence_capture(
            _approval_metadata(request_or_guardian_decision_linkage=linkage)
        )


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("scope_bound", False, "scope"),
        ("grants_execution_authority", True, "grant execution"),
    ],
)
def test_v1_g19_approval_intent_scope_fail_closed(
    field: str,
    value: Any,
    match: str,
) -> None:
    intent = dict(_approval_metadata()["approval_intent_scope"])
    intent[field] = value

    with pytest.raises(V1LiveApprovalEvidenceError, match=match):
        validate_v1_live_approval_evidence_capture(
            _approval_metadata(approval_intent_scope=intent)
        )


@pytest.mark.parametrize(
    ("outcome", "expected"),
    [
        ("approved", "approved"),
        ("denied", "denied"),
        ("revoked", "revoked"),
        ("stale", "stale"),
        ("expired", "expired"),
        ("superseded", "superseded"),
        ("blocked", "blocked"),
    ],
)
def test_v1_g19_approval_outcomes_are_normalized(
    outcome: str,
    expected: str,
) -> None:
    record = validate_v1_live_approval_evidence_capture(
        _approval_metadata(approval_outcome=outcome)
    )

    assert record["approval_outcome"] == expected
    assert record["evidence_is_current"] is (expected == "approved")


@pytest.mark.parametrize(
    ("field_name", "field", "value", "match"),
    [
        ("approval_expiration_metadata", "expiration_checked", False, "expiration"),
        ("approval_expiration_metadata", "expiration_status", "bad", "expiration status"),
        ("replay_prevention_metadata", "replay_checked", False, "replay"),
        ("replay_prevention_metadata", "replay_status", "bad", "replay status"),
        ("factor_evidence_summary", "factor_result", "bad", "factor result"),
        ("factor_evidence_summary", "raw_factor_value_present", True, "raw factor"),
        ("factor_evidence_summary", "redacted_summary_only", False, "redacted"),
        ("capture_source_metadata", "source_trusted_by_policy", False, "policy trust"),
        ("capture_source_metadata", "consumer_runtime_invoked", True, "runtime authority"),
        ("audit_evidence_linkage", "required", False, "audit/evidence"),
        ("audit_evidence_linkage", "proof_not_authority", False, "authority"),
        ("audit_evidence_linkage", "evidence_refs", [], "evidence refs"),
    ],
)
def test_v1_g19_required_nested_metadata_fail_closed(
    field_name: str,
    field: str,
    value: Any,
    match: str,
) -> None:
    nested = dict(_approval_metadata()[field_name])
    nested[field] = value

    with pytest.raises(V1LiveApprovalEvidenceError, match=match):
        validate_v1_live_approval_evidence_capture(_approval_metadata(**{field_name: nested}))


@pytest.mark.parametrize(
    "field",
    [
        "proof_not_authority_confirmation",
        "no_raw_pin_token_secret_customer_data_confirmation",
        "no_approval_token_issuance_confirmation",
        "no_execution_authority_confirmation",
    ],
)
def test_v1_g19_required_confirmations_fail_closed(field: str) -> None:
    with pytest.raises(V1LiveApprovalEvidenceError, match=field):
        validate_v1_live_approval_evidence_capture(_approval_metadata(**{field: False}))


@pytest.mark.parametrize(
    "field",
    [
        "approval_token_issued",
        "execution_allowed",
        "side_effects_allowed",
        "action_executed",
        "file_mutation_executed",
        "consumer_repo_mutation_added",
        "consumer_code_imported",
        "consumer_runtime_calls_added",
        "consumer_integration_added",
        "provider_model_routed",
        "tool_executed",
        "connector_invoked",
        "browser_action_executed",
        "network_action_executed",
        "scheduled_task_executed",
        "external_send_added",
        "device_command_invoked",
        "robot_control_invoked",
        "drone_control_invoked",
        "iot_control_invoked",
        "physical_world_invoked",
        "raw_pin_verified",
        "raw_pin_persisted",
        "final_api_freeze_approved",
        "product_ready",
    ],
)
def test_v1_g19_runtime_authority_claims_fail_closed(field: str) -> None:
    with pytest.raises(V1LiveApprovalEvidenceError, match="runtime authority"):
        validate_v1_live_approval_evidence_capture(_approval_metadata(**{field: True}))


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("raw_pin", "raw pin 123456"),
        ("raw_approval_pin", "approval-pin-123456"),
        ("raw_approval_token", "approval token value"),
        ("raw_factor_value", "raw factor value"),
        ("raw_secret", "raw-secret-123"),
        ("raw_prompt", "raw prompt text"),
        ("raw_file_contents", "raw file contents"),
        ("raw_customer_data", "raw customer data"),
        ("credentials", "provider credential value"),
    ],
)
def test_v1_g19_raw_sensitive_content_fails_closed(field: str, value: str) -> None:
    with pytest.raises(V1LiveApprovalEvidenceError, match="raw sensitive"):
        validate_v1_live_approval_evidence_capture(_approval_metadata(**{field: value}))


def test_v1_g19_output_does_not_emit_sensitive_values() -> None:
    record = validate_v1_live_approval_evidence_capture(_approval_metadata())
    output = json.dumps(record, sort_keys=True, default=str)

    for forbidden in (
        "approval-pin",
        "approval token",
        "raw factor",
        "raw-secret-123",
        "raw prompt",
        "raw file contents",
        "raw customer data",
        "provider credential",
    ):
        assert forbidden not in output
