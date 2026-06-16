"""Runtime tests for the approved V1-G18 consumer proof-packet intake slice."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from lima.guardian import (
    V1ConsumerProofPacketIntakeError,
    validate_v1_consumer_proof_packet_intake,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g18_consumer_proof_packet_audit_intake.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _packet_metadata(**overrides: Any) -> dict[str, Any]:
    record = {
        "consumer_packet_family": "sparkbot",
        "consumer_name": "Sparkbot",
        "consumer_repository": "https://github.com/sparkpit-labs/Sparkbot",
        "consumer_branch_ref": "proof/v1-g18",
        "consumer_commit_sha": "a" * 40,
        "proof_packet_path": "docs/lima/v1_g18_proof_packet.md",
        "audit_packet_path": "docs/lima/v1_g18_audit_packet.md",
        "machine_readable_summary_path": "tests/fixtures/lima/v1_g18_summary.json",
        "validation_commands": [
            {
                "command_ref": "validation:sparkbot:pytest",
                "command": "python -m pytest -q tests/lima",
                "reported_result": "pass",
            }
        ],
        "proposed_import_call_shape_evidence": {
            "evidence_ref": "evidence:sparkbot:import-call-shape",
            "proposed_import_shape": "from lima.guardian import validate_v1_consumer_proof_packet_intake",
            "proposed_call_shape": "validate_v1_consumer_proof_packet_intake(packet_metadata)",
            "evidence_only": True,
            "live_import_performed": False,
            "live_call_performed": False,
            "grants_runtime_authority": False,
        },
        "normalized_metadata_examples": {
            "examples_present": True,
            "redacted": True,
            "raw_content_included": False,
            "example_refs": ["fixture:sparkbot:v1-g18"],
        },
        "capability_profile_expectations": {
            "capability_profile_ref": "capability:sparkbot:v1-g18",
            "expectations_declared": True,
            "expected_tool_packs": ["files", "memory"],
            "execution_authority_granted": False,
            "future_integration_requires_approval": True,
        },
        "guardian_approval_boundary_expectations": {
            "boundary_ref": "guardian-boundary:sparkbot:v1-g18",
            "guardian_required": True,
            "approval_boundary_declared": True,
            "proof_not_authority": True,
            "execution_authority_granted": False,
            "future_integration_requires_approval": True,
        },
        "dry_run_non_execution_confirmation": {
            "confirmation_ref": "dry-run:sparkbot:v1-g18",
            "dry_run": True,
            "non_execution_confirmed": True,
            "no_side_effects_confirmed": True,
            "consumer_runtime_invoked": False,
        },
        "no_live_consumer_runtime_path_calls_lima": True,
        "no_bypass_claims": True,
        "independent_audit_required": True,
        "packet_status": "received",
    }
    record.update(overrides)
    return record


def test_v1_g18_fixture_records_approved_scope_and_boundaries() -> None:
    fixture = _load_fixture()

    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g18-consumer-proof-packet-audit-intake"
    assert fixture["operator_decision"] == "Approve-V1-G18"
    assert fixture["approved_scope"] == "consumer_proof_packet_audit_intake_metadata_slice"
    assert set(fixture["runtime_symbols"]) == {
        "V1ConsumerProofPacketIntakeError",
        "validate_v1_consumer_proof_packet_intake",
    }
    assert fixture["consumer_proof_packet_audit_intake_runtime_behavior_added"] is True
    assert set(fixture["consumer_packet_families"]) == {
        "sparkbot",
        "arc_bot",
        "lima_robo_os",
        "lima_office",
        "future_shell",
    }
    assert all(value is False for value in fixture["forbidden_behavior"].values())


def test_v1_g18_valid_packet_metadata_normalizes_record() -> None:
    record = validate_v1_consumer_proof_packet_intake(_packet_metadata())

    assert record["record_type"] == "v1_consumer_proof_packet_audit_intake"
    assert record["schema_version"] == "v1-g18-candidate"
    assert record["consumer_packet_family"] == "sparkbot"
    assert record["consumer_name"] == "Sparkbot"
    assert record["consumer_commit_sha"] == "a" * 40
    assert record["packet_status"] == "received"
    assert record["consumer_proof_packet_audit_intake_runtime_behavior"] is True
    assert record["proof_not_authority"] is True
    assert record["non_executing"] is True
    assert record["execution_allowed"] is False
    assert record["side_effects_allowed"] is False
    assert record["consumer_repo_mutation_added"] is False
    assert record["consumer_integration_added"] is False
    assert record["consumer_runtime_calls_added"] is False
    assert record["provider_model_routed"] is False
    assert record["tool_executed"] is False
    assert record["physical_world_invoked"] is False
    assert record["status_ledger_record"]["status_recorded"] is True
    assert record["status_ledger_record"]["proof_not_authority"] is True


def test_v1_g18_records_are_deterministic_for_sanitized_metadata() -> None:
    first = validate_v1_consumer_proof_packet_intake(_packet_metadata())
    second = validate_v1_consumer_proof_packet_intake(_packet_metadata())

    assert first == second
    assert first["record_hash"] == second["record_hash"]


@pytest.mark.parametrize(
    ("family", "expected"),
    [
        ("sparkbot", "sparkbot"),
        ("arc_bot", "arc_bot"),
        ("lima_robo_os", "lima_robo_os"),
        ("lima_office", "lima_office"),
        ("future-shell", "future_shell"),
    ],
)
def test_v1_g18_consumer_packet_families_are_supported(
    family: str,
    expected: str,
) -> None:
    record = validate_v1_consumer_proof_packet_intake(
        _packet_metadata(consumer_packet_family=family)
    )

    assert record["consumer_packet_family"] == expected


@pytest.mark.parametrize(
    "field",
    [
        "consumer_packet_family",
        "consumer_name",
        "consumer_repository",
        "consumer_branch_ref",
        "consumer_commit_sha",
        "proof_packet_path",
        "audit_packet_path",
        "machine_readable_summary_path",
        "validation_commands",
        "proposed_import_call_shape_evidence",
        "normalized_metadata_examples",
        "capability_profile_expectations",
        "guardian_approval_boundary_expectations",
        "dry_run_non_execution_confirmation",
        "no_live_consumer_runtime_path_calls_lima",
        "no_bypass_claims",
        "independent_audit_required",
        "packet_status",
    ],
)
def test_v1_g18_required_artifact_fields_fail_closed(field: str) -> None:
    metadata = _packet_metadata()
    del metadata[field]

    with pytest.raises(V1ConsumerProofPacketIntakeError, match=field):
        validate_v1_consumer_proof_packet_intake(metadata)


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("consumer_commit_sha", "not-a-sha", "commit SHA"),
        ("proof_packet_path", "../proof.md", "traversal"),
        ("audit_packet_path", "C:/audit.md", "drive"),
        ("machine_readable_summary_path", "/tmp/summary.json", "absolute"),
    ],
)
def test_v1_g18_repo_ref_commit_and_path_evidence_fail_closed(
    field: str,
    value: str,
    match: str,
) -> None:
    with pytest.raises(V1ConsumerProofPacketIntakeError, match=match):
        validate_v1_consumer_proof_packet_intake(_packet_metadata(**{field: value}))


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("evidence_only", False, "evidence only"),
        ("live_import_performed", True, "runtime authority"),
        ("live_call_performed", True, "runtime authority"),
        ("grants_runtime_authority", True, "authority"),
    ],
)
def test_v1_g18_import_call_shape_is_evidence_only(
    field: str,
    value: Any,
    match: str,
) -> None:
    shape = dict(_packet_metadata()["proposed_import_call_shape_evidence"])
    shape[field] = value

    with pytest.raises(V1ConsumerProofPacketIntakeError, match=match):
        validate_v1_consumer_proof_packet_intake(
            _packet_metadata(proposed_import_call_shape_evidence=shape)
        )


@pytest.mark.parametrize(
    ("field_name", "field", "value", "match"),
    [
        ("normalized_metadata_examples", "examples_present", False, "examples"),
        ("normalized_metadata_examples", "redacted", False, "redacted"),
        ("normalized_metadata_examples", "raw_content_included", True, "raw content"),
        ("normalized_metadata_examples", "example_refs", [], "example refs"),
        ("capability_profile_expectations", "expectations_declared", False, "capability"),
        (
            "capability_profile_expectations",
            "execution_authority_granted",
            True,
            "grant execution",
        ),
        (
            "capability_profile_expectations",
            "future_integration_requires_approval",
            False,
            "future integration",
        ),
        (
            "guardian_approval_boundary_expectations",
            "guardian_required",
            False,
            "Guardian",
        ),
        (
            "guardian_approval_boundary_expectations",
            "approval_boundary_declared",
            False,
            "approval boundary",
        ),
        (
            "guardian_approval_boundary_expectations",
            "proof_not_authority",
            False,
            "cannot be authority",
        ),
        (
            "guardian_approval_boundary_expectations",
            "execution_authority_granted",
            True,
            "grant execution",
        ),
        (
            "guardian_approval_boundary_expectations",
            "future_integration_requires_approval",
            False,
            "future integration",
        ),
    ],
)
def test_v1_g18_required_examples_capability_and_guardian_metadata_fail_closed(
    field_name: str,
    field: str,
    value: Any,
    match: str,
) -> None:
    nested = dict(_packet_metadata()[field_name])
    nested[field] = value

    with pytest.raises(V1ConsumerProofPacketIntakeError, match=match):
        validate_v1_consumer_proof_packet_intake(_packet_metadata(**{field_name: nested}))


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("dry_run", False, "dry-run"),
        ("non_execution_confirmed", False, "non-execution"),
        ("no_side_effects_confirmed", False, "side-effects"),
        ("consumer_runtime_invoked", True, "runtime authority"),
    ],
)
def test_v1_g18_dry_run_non_execution_confirmation_fails_closed(
    field: str,
    value: Any,
    match: str,
) -> None:
    confirmation = dict(_packet_metadata()["dry_run_non_execution_confirmation"])
    confirmation[field] = value

    with pytest.raises(V1ConsumerProofPacketIntakeError, match=match):
        validate_v1_consumer_proof_packet_intake(
            _packet_metadata(dry_run_non_execution_confirmation=confirmation)
        )


@pytest.mark.parametrize(
    "field",
    [
        "no_live_consumer_runtime_path_calls_lima",
        "no_bypass_claims",
        "independent_audit_required",
    ],
)
def test_v1_g18_required_confirmations_fail_closed(field: str) -> None:
    with pytest.raises(V1ConsumerProofPacketIntakeError, match=field):
        validate_v1_consumer_proof_packet_intake(_packet_metadata(**{field: False}))


@pytest.mark.parametrize(
    ("status", "expected"),
    [
        ("received", "received"),
        ("missing", "missing"),
        ("blocked", "blocked"),
        ("rejected", "rejected"),
        ("accepted-static-evidence", "accepted_static_evidence"),
    ],
)
def test_v1_g18_packet_statuses_are_normalized(status: str, expected: str) -> None:
    record = validate_v1_consumer_proof_packet_intake(
        _packet_metadata(packet_status=status)
    )

    assert record["packet_status"] == expected


@pytest.mark.parametrize(
    "field",
    [
        "consumer_repo_mutation_added",
        "consumer_code_imported",
        "consumer_runtime_calls_added",
        "consumer_integration_added",
        "provider_model_routed",
        "tool_executed",
        "connector_invoked",
        "browser_action_executed",
        "network_action_executed",
        "file_mutation_executed",
        "scheduled_task_executed",
        "external_send_added",
        "device_command_invoked",
        "robot_control_invoked",
        "drone_control_invoked",
        "iot_control_invoked",
        "physical_world_invoked",
        "approval_token_issued",
        "final_api_freeze_approved",
        "product_ready",
    ],
)
def test_v1_g18_runtime_authority_and_bypass_claims_fail_closed(field: str) -> None:
    with pytest.raises(V1ConsumerProofPacketIntakeError, match="runtime authority"):
        validate_v1_consumer_proof_packet_intake(_packet_metadata(**{field: True}))


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("raw_secret", "raw-secret-123"),
        ("raw_prompt", "raw prompt text"),
        ("raw_file_contents", "raw file contents"),
        ("raw_approval_pin", "approval-pin-123456"),
        ("raw_approval_token", "approval token value"),
        ("raw_customer_data", "raw customer data"),
        ("credentials", "provider credential value"),
    ],
)
def test_v1_g18_raw_sensitive_content_fails_closed(field: str, value: str) -> None:
    with pytest.raises(V1ConsumerProofPacketIntakeError, match="raw sensitive"):
        validate_v1_consumer_proof_packet_intake(_packet_metadata(**{field: value}))


def test_v1_g18_output_does_not_emit_sensitive_values() -> None:
    record = validate_v1_consumer_proof_packet_intake(_packet_metadata())
    output = json.dumps(record, sort_keys=True, default=str)

    for forbidden in (
        "raw-secret-123",
        "approval-pin",
        "approval token",
        "raw prompt",
        "raw file contents",
        "raw customer data",
        "provider credential",
    ):
        assert forbidden not in output
