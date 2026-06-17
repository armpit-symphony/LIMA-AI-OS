"""Runtime tests for the approved V1-G23 consumer import dry-run slice."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from lima.adapters import (
    V1ConsumerImportDryRunError,
    validate_v1_consumer_integration_proof_to_import_dry_run,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g23_consumer_integration_proof_to_import_dry_run.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _import_plan_metadata(**overrides: Any) -> dict[str, Any]:
    record = {
        "import_plan_id": "import-plan:v1-g23:sparkbot:001",
        "consumer_packet_family": "sparkbot",
        "consumer_name": "Sparkbot",
        "consumer_repository": "armpit-symphony/Sparkbot",
        "consumer_branch_ref": "origin/main",
        "consumer_commit_sha": "abcdef1234567890",
        "proof_packet_ref": "proof-packet:v1-g18:sparkbot",
        "compatibility_packet_ref": "compatibility:v1-g21:sparkbot",
        "frozen_api_packet_ref": "api-freeze:v1-g22",
        "proposed_import_metadata": {
            "import_refs": [
                "from lima.adapters import validate_v1_consumer_integration_proof_to_import_dry_run"
            ],
            "import_target_refs": [
                "lima.adapters.validate_v1_consumer_integration_proof_to_import_dry_run"
            ],
            "metadata_only": True,
            "consumer_code_imported": False,
            "live_import_performed": False,
            "consumer_repo_mutation_added": False,
            "grants_runtime_authority": False,
        },
        "proposed_call_site_metadata": {
            "call_site_refs": ["sparkbot.integration.plan.consumer_import_dry_run"],
            "call_shape_refs": [
                "validate_v1_consumer_integration_proof_to_import_dry_run(metadata)"
            ],
            "metadata_only": True,
            "live_call_performed": False,
            "consumer_runtime_calls_added": False,
            "consumer_runtime_invoked": False,
            "grants_runtime_authority": False,
        },
        "adapter_boundary_mapping": {
            "boundary_ref": "adapter-boundary:v1-g23",
            "mapped_refs": ["lima.adapters"],
            "compatible": True,
            "metadata_only": True,
            "proof_not_authority": True,
            "grants_execution_authority": False,
            "future_integration_requires_approval": True,
        },
        "guardian_boundary_mapping": {
            "boundary_ref": "guardian-boundary:v1-g23",
            "mapped_refs": ["guardian.syscall-gate"],
            "compatible": True,
            "metadata_only": True,
            "proof_not_authority": True,
            "grants_execution_authority": False,
            "future_integration_requires_approval": True,
        },
        "approval_boundary_mapping": {
            "boundary_ref": "approval-boundary:v1-g23",
            "mapped_refs": ["approval.evidence"],
            "compatible": True,
            "metadata_only": True,
            "proof_not_authority": True,
            "grants_execution_authority": False,
            "future_integration_requires_approval": True,
        },
        "provider_model_route_boundary_mapping": {
            "boundary_ref": "provider-model-boundary:v1-g23",
            "mapped_refs": ["model.route.metadata"],
            "compatible": True,
            "metadata_only": True,
            "proof_not_authority": True,
            "grants_execution_authority": False,
            "future_integration_requires_approval": True,
        },
        "expected_test_command_metadata": {
            "command_refs": ["python -m pytest tests/test_import_plan_static.py"],
            "expected_result_refs": ["dry-run import plan can be inspected"],
            "metadata_only": True,
            "dry_run_only": True,
            "consumer_runtime_invoked": False,
            "external_services_required": False,
        },
        "rollback_metadata": {
            "rollback_ref": "rollback:v1-g23:sparkbot-import-plan",
            "rollback_step_refs": ["remove import-plan fixture metadata"],
            "consumer_repo_changes_required": False,
            "runtime_export_cleanup_required": False,
            "external_service_changes_required": False,
        },
        "no_consumer_repo_mutation_confirmation": True,
        "no_live_import_call_confirmation": True,
        "no_runtime_export_cleanup_confirmation": True,
        "no_raw_content_secret_credential_customer_data_confirmation": True,
        "proof_not_authority_confirmation": True,
        "audit_evidence_linkage": {
            "audit_record_ref": "audit:v1-g23:consumer-import-plan",
            "evidence_refs": [
                "proof-packet:v1-g18:sparkbot",
                "compatibility:v1-g21:sparkbot",
                "api-freeze:v1-g22",
            ],
            "required": True,
            "proof_not_authority": True,
        },
    }
    record.update(overrides)
    return record


def test_v1_g23_fixture_records_approved_scope_and_boundaries() -> None:
    fixture = _load_fixture()

    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g23-consumer-integration-proof-to-import-dry-run"
    assert fixture["operator_decision"] == "Approve-V1-G23"
    assert fixture["approved_scope"] == (
        "consumer_integration_proof_to_import_dry_run_metadata_slice"
    )
    assert set(fixture["runtime_symbols"]) == {
        "V1ConsumerImportDryRunError",
        "validate_v1_consumer_integration_proof_to_import_dry_run",
    }
    assert fixture["consumer_import_dry_run_runtime_behavior_added"] is True
    assert all(value is False for value in fixture["forbidden_behavior"].values())


def test_v1_g23_valid_import_plan_metadata_normalizes_record() -> None:
    record = validate_v1_consumer_integration_proof_to_import_dry_run(
        _import_plan_metadata()
    )

    assert record["record_type"] == "v1_consumer_integration_proof_to_import_dry_run"
    assert record["schema_version"] == "v1-g23-candidate"
    assert record["import_plan_id"] == "import-plan:v1-g23:sparkbot:001"
    assert record["consumer_packet_family"] == "sparkbot"
    assert record["consumer_commit_sha"] == "abcdef1234567890"
    assert record["consumer_import_dry_run_runtime_behavior"] is True
    assert record["import_plan_metadata_only"] is True
    assert record["proof_not_authority"] is True
    assert record["non_executing"] is True
    assert record["consumer_repo_mutation_added"] is False
    assert record["consumer_code_imported"] is False
    assert record["consumer_runtime_calls_added"] is False
    assert record["consumer_integration_added"] is False
    assert record["runtime_export_cleanup_approved"] is False
    assert record["runtime_export_cleanup_performed"] is False
    assert record["provider_model_calls_added"] is False
    assert record["tool_executed"] is False
    assert record["product_ready"] is False


def test_v1_g23_records_are_deterministic_for_sanitized_metadata() -> None:
    first = validate_v1_consumer_integration_proof_to_import_dry_run(
        _import_plan_metadata()
    )
    second = validate_v1_consumer_integration_proof_to_import_dry_run(
        _import_plan_metadata()
    )

    assert first == second
    assert first["record_hash"] == second["record_hash"]


@pytest.mark.parametrize(
    "field",
    [
        "import_plan_id",
        "consumer_packet_family",
        "consumer_name",
        "consumer_repository",
        "consumer_branch_ref",
        "consumer_commit_sha",
        "proof_packet_ref",
        "compatibility_packet_ref",
        "frozen_api_packet_ref",
        "proposed_import_metadata",
        "proposed_call_site_metadata",
        "adapter_boundary_mapping",
        "guardian_boundary_mapping",
        "approval_boundary_mapping",
        "provider_model_route_boundary_mapping",
        "expected_test_command_metadata",
        "rollback_metadata",
        "no_consumer_repo_mutation_confirmation",
        "no_live_import_call_confirmation",
        "no_runtime_export_cleanup_confirmation",
        "no_raw_content_secret_credential_customer_data_confirmation",
        "proof_not_authority_confirmation",
        "audit_evidence_linkage",
    ],
)
def test_v1_g23_required_import_plan_fields_fail_closed(field: str) -> None:
    metadata = _import_plan_metadata()
    del metadata[field]

    with pytest.raises(V1ConsumerImportDryRunError, match=field):
        validate_v1_consumer_integration_proof_to_import_dry_run(metadata)


@pytest.mark.parametrize(
    "family",
    ["sparkbot", "arc_bot", "lima_robo_os", "lima_office", "future_shell"],
)
def test_v1_g23_supported_consumer_packet_families_normalize(family: str) -> None:
    record = validate_v1_consumer_integration_proof_to_import_dry_run(
        _import_plan_metadata(consumer_packet_family=family.replace("_", "-"))
    )

    assert record["consumer_packet_family"] == family


@pytest.mark.parametrize("commit", ["bad", "not-a-sha", "gabcdef", "a" * 65])
def test_v1_g23_consumer_commit_sha_metadata_is_validated(commit: str) -> None:
    with pytest.raises(V1ConsumerImportDryRunError, match="commit SHA"):
        validate_v1_consumer_integration_proof_to_import_dry_run(
            _import_plan_metadata(consumer_commit_sha=commit)
        )


def test_v1_g23_unknown_consumer_packet_family_fails_closed() -> None:
    with pytest.raises(V1ConsumerImportDryRunError, match="consumer packet family"):
        validate_v1_consumer_integration_proof_to_import_dry_run(
            _import_plan_metadata(consumer_packet_family="unknown")
        )


@pytest.mark.parametrize(
    "field",
    ["proof_packet_ref", "compatibility_packet_ref", "frozen_api_packet_ref"],
)
def test_v1_g23_required_packet_refs_fail_closed(field: str) -> None:
    with pytest.raises(V1ConsumerImportDryRunError, match=field):
        validate_v1_consumer_integration_proof_to_import_dry_run(
            _import_plan_metadata(**{field: ""})
        )


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("import_refs", [], "import_refs"),
        ("import_target_refs", [], "import_target_refs"),
        ("metadata_only", False, "metadata only"),
        ("consumer_code_imported", True, "runtime authority|imports"),
        ("live_import_performed", True, "runtime authority|imports"),
        ("consumer_repo_mutation_added", True, "runtime authority|repo mutation"),
        ("grants_runtime_authority", True, "runtime authority"),
    ],
)
def test_v1_g23_proposed_import_metadata_fail_closed(
    field: str,
    value: Any,
    match: str,
) -> None:
    proposed_import = dict(_import_plan_metadata()["proposed_import_metadata"])
    proposed_import[field] = value

    with pytest.raises(V1ConsumerImportDryRunError, match=match):
        validate_v1_consumer_integration_proof_to_import_dry_run(
            _import_plan_metadata(proposed_import_metadata=proposed_import)
        )


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("call_site_refs", [], "call_site_refs"),
        ("call_shape_refs", [], "call_shape_refs"),
        ("metadata_only", False, "metadata only"),
        ("live_call_performed", True, "runtime authority|runtime calls"),
        ("consumer_runtime_calls_added", True, "runtime authority|runtime calls"),
        ("consumer_runtime_invoked", True, "runtime authority|runtime calls"),
        ("grants_runtime_authority", True, "runtime authority"),
    ],
)
def test_v1_g23_proposed_call_site_metadata_fail_closed(
    field: str,
    value: Any,
    match: str,
) -> None:
    call_site = dict(_import_plan_metadata()["proposed_call_site_metadata"])
    call_site[field] = value

    with pytest.raises(V1ConsumerImportDryRunError, match=match):
        validate_v1_consumer_integration_proof_to_import_dry_run(
            _import_plan_metadata(proposed_call_site_metadata=call_site)
        )


@pytest.mark.parametrize(
    "field_name",
    [
        "adapter_boundary_mapping",
        "guardian_boundary_mapping",
        "approval_boundary_mapping",
        "provider_model_route_boundary_mapping",
    ],
)
@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("mapped_refs", [], "mapped_refs"),
        ("compatible", False, "compatibility"),
        ("metadata_only", False, "metadata only"),
        ("proof_not_authority", False, "authority"),
        ("grants_execution_authority", True, "grant execution"),
        ("future_integration_requires_approval", False, "future integration"),
    ],
)
def test_v1_g23_boundary_mapping_metadata_fail_closed(
    field_name: str,
    field: str,
    value: Any,
    match: str,
) -> None:
    boundary = dict(_import_plan_metadata()[field_name])
    boundary[field] = value

    with pytest.raises(V1ConsumerImportDryRunError, match=match):
        validate_v1_consumer_integration_proof_to_import_dry_run(
            _import_plan_metadata(**{field_name: boundary})
        )


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("command_refs", [], "command_refs"),
        ("expected_result_refs", [], "expected_result_refs"),
        ("metadata_only", False, "metadata only"),
        ("dry_run_only", False, "dry-run"),
        ("consumer_runtime_invoked", True, "runtime authority|runtime calls"),
        ("external_services_required", True, "external services"),
    ],
)
def test_v1_g23_expected_test_command_metadata_fail_closed(
    field: str,
    value: Any,
    match: str,
) -> None:
    tests = dict(_import_plan_metadata()["expected_test_command_metadata"])
    tests[field] = value

    with pytest.raises(V1ConsumerImportDryRunError, match=match):
        validate_v1_consumer_integration_proof_to_import_dry_run(
            _import_plan_metadata(expected_test_command_metadata=tests)
        )


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("rollback_step_refs", [], "rollback_step_refs"),
        ("consumer_repo_changes_required", True, "runtime authority|repo mutation"),
        ("runtime_export_cleanup_required", True, "runtime authority|export cleanup"),
        ("external_service_changes_required", True, "external services"),
    ],
)
def test_v1_g23_rollback_metadata_fail_closed(
    field: str,
    value: Any,
    match: str,
) -> None:
    rollback = dict(_import_plan_metadata()["rollback_metadata"])
    rollback[field] = value

    with pytest.raises(V1ConsumerImportDryRunError, match=match):
        validate_v1_consumer_integration_proof_to_import_dry_run(
            _import_plan_metadata(rollback_metadata=rollback)
        )


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("required", False, "audit/evidence"),
        ("proof_not_authority", False, "authority"),
        ("evidence_refs", [], "evidence_refs"),
    ],
)
def test_v1_g23_audit_evidence_linkage_fail_closed(
    field: str,
    value: Any,
    match: str,
) -> None:
    audit = dict(_import_plan_metadata()["audit_evidence_linkage"])
    audit[field] = value

    with pytest.raises(V1ConsumerImportDryRunError, match=match):
        validate_v1_consumer_integration_proof_to_import_dry_run(
            _import_plan_metadata(audit_evidence_linkage=audit)
        )


@pytest.mark.parametrize(
    "field",
    [
        "no_consumer_repo_mutation_confirmation",
        "no_live_import_call_confirmation",
        "no_runtime_export_cleanup_confirmation",
        "no_raw_content_secret_credential_customer_data_confirmation",
        "proof_not_authority_confirmation",
    ],
)
def test_v1_g23_required_confirmations_fail_closed(field: str) -> None:
    with pytest.raises(V1ConsumerImportDryRunError, match=field):
        validate_v1_consumer_integration_proof_to_import_dry_run(
            _import_plan_metadata(**{field: False})
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
def test_v1_g23_runtime_authority_claims_fail_closed(field: str) -> None:
    with pytest.raises(V1ConsumerImportDryRunError, match="runtime authority"):
        validate_v1_consumer_integration_proof_to_import_dry_run(
            _import_plan_metadata(**{field: True})
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
def test_v1_g23_raw_sensitive_content_fails_closed(field: str, value: str) -> None:
    with pytest.raises(V1ConsumerImportDryRunError, match="raw sensitive"):
        validate_v1_consumer_integration_proof_to_import_dry_run(
            _import_plan_metadata(**{field: value})
        )


def test_v1_g23_output_does_not_emit_sensitive_values() -> None:
    record = validate_v1_consumer_integration_proof_to_import_dry_run(
        _import_plan_metadata()
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
