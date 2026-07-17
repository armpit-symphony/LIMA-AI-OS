"""Runtime tests for the approved V1-G21 consumer compatibility slice."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from lima.adapters import (
    V1ConsumerIntegrationCompatibilityError,
    validate_v1_consumer_integration_compatibility_freeze,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g21_consumer_integration_compatibility_freeze.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _compatibility_metadata(**overrides: Any) -> dict[str, Any]:
    record = {
        "compatibility_packet_id": "compat:v1-g21:sparkbot:001",
        "consumer_packet_family": "sparkbot",
        "consumer_name": "Sparkbot",
        "consumer_repository": "armpit-symphony/Sparkbot",
        "consumer_branch_ref": "origin/main",
        "consumer_commit_sha": "abcdef1234567890",
        "candidate_export_surface_refs": [
            "lima.adapters.validate_v1_consumer_integration_compatibility_freeze"
        ],
        "runtime_symbol_refs": [
            "V1ConsumerIntegrationCompatibilityError",
            "validate_v1_consumer_integration_compatibility_freeze",
        ],
        "import_surface_expectations": {
            "expected_import_refs": [
                "from lima.adapters import validate_v1_consumer_integration_compatibility_freeze"
            ],
            "expected_call_shape_refs": [
                "validate_v1_consumer_integration_compatibility_freeze(metadata)"
            ],
            "metadata_only": True,
            "live_import_performed": False,
            "live_call_performed": False,
            "consumer_code_imported": False,
            "grants_runtime_authority": False,
        },
        "fixture_compatibility_matrix": {
            "matrix_ref": "fixture-matrix:v1-g21:sparkbot",
            "fixture_refs": ["fixture:v1-g18:sparkbot", "fixture:v1-g20:model-route"],
            "compatibility_status": "candidate_compatible",
            "raw_fixture_content_included": False,
            "consumer_runtime_invoked": False,
        },
        "version_compatibility_metadata": {
            "compatibility_version_ref": "compat-version:v1-g21",
            "lima_candidate_version_ref": "lima:v1-candidate",
            "consumer_version_ref": "sparkbot:metadata-ref",
            "compatibility_status": "candidate_compatible",
            "final_api_freeze_claimed": False,
        },
        "guardian_boundary_compatibility": {
            "boundary_ref": "guardian-boundary:v1-g21",
            "compatible": True,
            "proof_not_authority": True,
            "grants_execution_authority": False,
            "future_integration_requires_approval": True,
        },
        "approval_boundary_compatibility": {
            "boundary_ref": "approval-boundary:v1-g21",
            "compatible": True,
            "proof_not_authority": True,
            "grants_execution_authority": False,
            "future_integration_requires_approval": True,
        },
        "provider_model_route_boundary_compatibility": {
            "boundary_ref": "provider-model-boundary:v1-g21",
            "compatible": True,
            "proof_not_authority": True,
            "grants_execution_authority": False,
            "future_integration_requires_approval": True,
        },
        "consumer_runtime_call_prohibition": {
            "prohibition_ref": "runtime-prohibition:v1-g21",
            "non_execution_confirmed": True,
            "consumer_runtime_calls_added": False,
            "live_import_performed": False,
            "live_call_performed": False,
        },
        "no_consumer_repo_mutation_confirmation": True,
        "no_live_import_call_confirmation": True,
        "final_public_api_freeze_not_claimed_confirmation": True,
        "audit_evidence_linkage": {
            "audit_record_ref": "audit:v1-g21:compatibility",
            "evidence_refs": ["compat:v1-g21:sparkbot:001", "fixture:v1-g21"],
            "required": True,
            "proof_not_authority": True,
        },
        "proof_not_authority_confirmation": True,
        "no_raw_content_secret_credential_customer_data_confirmation": True,
        "no_execution_authority_confirmation": True,
    }
    record.update(overrides)
    return record


def test_v1_g21_fixture_records_approved_scope_and_boundaries() -> None:
    fixture = _load_fixture()

    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g21-consumer-integration-compatibility-freeze"
    assert fixture["operator_decision"] == "Approve-V1-G21"
    assert fixture["approved_scope"] == "consumer_integration_compatibility_freeze_metadata_slice"
    assert set(fixture["runtime_symbols"]) == {
        "V1ConsumerIntegrationCompatibilityError",
        "validate_v1_consumer_integration_compatibility_freeze",
    }
    assert fixture["consumer_integration_compatibility_freeze_runtime_behavior_added"] is True
    assert all(value is False for value in fixture["forbidden_behavior"].values())


def test_v1_g21_valid_compatibility_metadata_normalizes_record() -> None:
    record = validate_v1_consumer_integration_compatibility_freeze(
        _compatibility_metadata()
    )

    assert record["record_type"] == "v1_consumer_integration_compatibility_freeze"
    assert record["schema_version"] == "v1-g21-candidate"
    assert record["compatibility_packet_id"] == "compat:v1-g21:sparkbot:001"
    assert record["consumer_packet_family"] == "sparkbot"
    assert record["consumer_commit_sha"] == "abcdef1234567890"
    assert record["consumer_integration_compatibility_freeze_runtime_behavior"] is True
    assert record["compatibility_metadata_only"] is True
    assert record["proof_not_authority"] is True
    assert record["non_executing"] is True
    assert record["consumer_repo_mutation_added"] is False
    assert record["consumer_code_imported"] is False
    assert record["consumer_runtime_calls_added"] is False
    assert record["consumer_integration_added"] is False
    assert record["final_api_freeze_approved"] is False
    assert record["runtime_export_cleanup_approved"] is False
    assert record["provider_model_calls_added"] is False
    assert record["tool_executed"] is False
    assert record["product_ready"] is False


def test_v1_g21_records_are_deterministic_for_sanitized_metadata() -> None:
    first = validate_v1_consumer_integration_compatibility_freeze(
        _compatibility_metadata()
    )
    second = validate_v1_consumer_integration_compatibility_freeze(
        _compatibility_metadata()
    )

    assert first == second
    assert first["record_hash"] == second["record_hash"]


@pytest.mark.parametrize(
    "field",
    [
        "compatibility_packet_id",
        "consumer_packet_family",
        "consumer_name",
        "consumer_repository",
        "consumer_branch_ref",
        "consumer_commit_sha",
        "candidate_export_surface_refs",
        "runtime_symbol_refs",
        "import_surface_expectations",
        "fixture_compatibility_matrix",
        "version_compatibility_metadata",
        "guardian_boundary_compatibility",
        "approval_boundary_compatibility",
        "provider_model_route_boundary_compatibility",
        "consumer_runtime_call_prohibition",
        "no_consumer_repo_mutation_confirmation",
        "no_live_import_call_confirmation",
        "final_public_api_freeze_not_claimed_confirmation",
        "audit_evidence_linkage",
        "proof_not_authority_confirmation",
        "no_raw_content_secret_credential_customer_data_confirmation",
        "no_execution_authority_confirmation",
    ],
)
def test_v1_g21_required_compatibility_fields_fail_closed(field: str) -> None:
    metadata = _compatibility_metadata()
    del metadata[field]

    with pytest.raises(V1ConsumerIntegrationCompatibilityError, match=field):
        validate_v1_consumer_integration_compatibility_freeze(metadata)


@pytest.mark.parametrize(
    "family",
    ["sparkbot", "arc_bot", "lima_robo_os", "lima_office", "future_shell"],
)
def test_v1_g21_supported_consumer_packet_families_normalize(family: str) -> None:
    record = validate_v1_consumer_integration_compatibility_freeze(
        _compatibility_metadata(consumer_packet_family=family.replace("_", "-"))
    )

    assert record["consumer_packet_family"] == family


@pytest.mark.parametrize("commit", ["bad", "not-a-sha", "gabcdef", "a" * 65])
def test_v1_g21_consumer_commit_sha_metadata_is_validated(commit: str) -> None:
    with pytest.raises(V1ConsumerIntegrationCompatibilityError, match="commit SHA"):
        validate_v1_consumer_integration_compatibility_freeze(
            _compatibility_metadata(consumer_commit_sha=commit)
        )


def test_v1_g21_unknown_consumer_packet_family_fails_closed() -> None:
    with pytest.raises(V1ConsumerIntegrationCompatibilityError, match="consumer packet family"):
        validate_v1_consumer_integration_compatibility_freeze(
            _compatibility_metadata(consumer_packet_family="unknown")
        )


@pytest.mark.parametrize(
    "field",
    ["candidate_export_surface_refs", "runtime_symbol_refs"],
)
def test_v1_g21_required_ref_sequences_fail_closed(field: str) -> None:
    with pytest.raises(V1ConsumerIntegrationCompatibilityError, match=field):
        validate_v1_consumer_integration_compatibility_freeze(
            _compatibility_metadata(**{field: []})
        )


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("expected_import_refs", [], "expected_import_refs"),
        ("expected_call_shape_refs", [], "expected_call_shape_refs"),
        ("metadata_only", False, "metadata only"),
        ("live_import_performed", True, "runtime authority|imports"),
        ("live_call_performed", True, "runtime authority|runtime calls"),
        ("consumer_code_imported", True, "runtime authority|imports"),
        ("grants_runtime_authority", True, "runtime authority"),
    ],
)
def test_v1_g21_import_surface_expectations_fail_closed(
    field: str,
    value: Any,
    match: str,
) -> None:
    surface = dict(_compatibility_metadata()["import_surface_expectations"])
    surface[field] = value

    with pytest.raises(V1ConsumerIntegrationCompatibilityError, match=match):
        validate_v1_consumer_integration_compatibility_freeze(
            _compatibility_metadata(import_surface_expectations=surface)
        )


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("fixture_refs", [], "fixture_refs"),
        ("compatibility_status", "bad", "compatibility status"),
        ("raw_fixture_content_included", True, "raw fixture|runtime authority"),
        ("consumer_runtime_invoked", True, "runtime authority|runtime calls"),
    ],
)
def test_v1_g21_fixture_compatibility_matrix_fail_closed(
    field: str,
    value: Any,
    match: str,
) -> None:
    matrix = dict(_compatibility_metadata()["fixture_compatibility_matrix"])
    matrix[field] = value

    with pytest.raises(V1ConsumerIntegrationCompatibilityError, match=match):
        validate_v1_consumer_integration_compatibility_freeze(
            _compatibility_metadata(fixture_compatibility_matrix=matrix)
        )


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("compatibility_status", "bad", "compatibility status"),
        ("final_api_freeze_claimed", True, "final public API freeze"),
    ],
)
def test_v1_g21_version_compatibility_metadata_fail_closed(
    field: str,
    value: Any,
    match: str,
) -> None:
    version = dict(_compatibility_metadata()["version_compatibility_metadata"])
    version[field] = value

    with pytest.raises(V1ConsumerIntegrationCompatibilityError, match=match):
        validate_v1_consumer_integration_compatibility_freeze(
            _compatibility_metadata(version_compatibility_metadata=version)
        )


@pytest.mark.parametrize(
    "field_name",
    [
        "guardian_boundary_compatibility",
        "approval_boundary_compatibility",
        "provider_model_route_boundary_compatibility",
    ],
)
@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("compatible", False, "compatibility"),
        ("proof_not_authority", False, "authority"),
        ("grants_execution_authority", True, "grant execution"),
        ("future_integration_requires_approval", False, "future integration"),
    ],
)
def test_v1_g21_boundary_compatibility_metadata_fail_closed(
    field_name: str,
    field: str,
    value: Any,
    match: str,
) -> None:
    boundary = dict(_compatibility_metadata()[field_name])
    boundary[field] = value

    with pytest.raises(V1ConsumerIntegrationCompatibilityError, match=match):
        validate_v1_consumer_integration_compatibility_freeze(
            _compatibility_metadata(**{field_name: boundary})
        )


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("non_execution_confirmed", False, "non-execution"),
        ("consumer_runtime_calls_added", True, "runtime authority|runtime calls"),
        ("live_import_performed", True, "runtime authority|imports"),
        ("live_call_performed", True, "runtime authority|runtime calls"),
    ],
)
def test_v1_g21_consumer_runtime_call_prohibition_fail_closed(
    field: str,
    value: Any,
    match: str,
) -> None:
    prohibition = dict(_compatibility_metadata()["consumer_runtime_call_prohibition"])
    prohibition[field] = value

    with pytest.raises(V1ConsumerIntegrationCompatibilityError, match=match):
        validate_v1_consumer_integration_compatibility_freeze(
            _compatibility_metadata(consumer_runtime_call_prohibition=prohibition)
        )


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("required", False, "audit/evidence"),
        ("proof_not_authority", False, "authority"),
        ("evidence_refs", [], "evidence_refs"),
    ],
)
def test_v1_g21_audit_evidence_linkage_fail_closed(
    field: str,
    value: Any,
    match: str,
) -> None:
    audit = dict(_compatibility_metadata()["audit_evidence_linkage"])
    audit[field] = value

    with pytest.raises(V1ConsumerIntegrationCompatibilityError, match=match):
        validate_v1_consumer_integration_compatibility_freeze(
            _compatibility_metadata(audit_evidence_linkage=audit)
        )


@pytest.mark.parametrize(
    "field",
    [
        "no_consumer_repo_mutation_confirmation",
        "no_live_import_call_confirmation",
        "final_public_api_freeze_not_claimed_confirmation",
        "proof_not_authority_confirmation",
        "no_raw_content_secret_credential_customer_data_confirmation",
        "no_execution_authority_confirmation",
    ],
)
def test_v1_g21_required_confirmations_fail_closed(field: str) -> None:
    with pytest.raises(V1ConsumerIntegrationCompatibilityError, match=field):
        validate_v1_consumer_integration_compatibility_freeze(
            _compatibility_metadata(**{field: False})
        )


@pytest.mark.parametrize(
    "field",
    [
        "consumer_repo_mutation_added",
        "consumer_repo_edited",
        "consumer_file_written",
        "consumer_code_imported",
        "consumer_code_imports_added",
        "consumer_runtime_calls_added",
        "consumer_runtime_called",
        "consumer_runtime_invoked",
        "consumer_integration_added",
        "shell_runtime_wired",
        "final_api_freeze_approved",
        "runtime_export_cleanup_approved",
        "runtime_export_cleanup_performed",
        "provider_model_calls_added",
        "model_request_dispatched",
        "secret_lookup_added",
        "credential_access_added",
        "tool_executed",
        "execution_allowed",
        "side_effects_allowed",
        "action_executed",
        "file_mutation_executed",
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
def test_v1_g21_runtime_authority_claims_fail_closed(field: str) -> None:
    with pytest.raises(V1ConsumerIntegrationCompatibilityError, match="runtime authority"):
        validate_v1_consumer_integration_compatibility_freeze(
            _compatibility_metadata(**{field: True})
        )


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("raw_content", "raw content text"),
        ("raw_file_contents", "raw file contents"),
        ("raw_prompt", "raw prompt text"),
        ("raw_customer_data", "raw customer data"),
        ("credentials", "provider credential value"),
        ("provider_token", "provider token value"),
        ("provider_api_key", "api key value"),
        ("raw_secret", "raw-secret-123"),
    ],
)
def test_v1_g21_raw_sensitive_content_fails_closed(field: str, value: str) -> None:
    with pytest.raises(V1ConsumerIntegrationCompatibilityError, match="raw sensitive"):
        validate_v1_consumer_integration_compatibility_freeze(
            _compatibility_metadata(**{field: value})
        )


def test_v1_g21_output_does_not_emit_sensitive_values() -> None:
    record = validate_v1_consumer_integration_compatibility_freeze(
        _compatibility_metadata()
    )
    output = json.dumps(record, sort_keys=True, default=str)

    for forbidden in (
        "raw content",
        "raw file contents",
        "raw prompt",
        "raw customer data",
        "provider credential",
        "provider token",
        "api key value",
        "raw-secret-123",
    ):
        assert forbidden not in output
