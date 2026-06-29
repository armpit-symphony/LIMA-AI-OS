"""Audit checks for the V1-G57 provider execution hardening request."""

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
    / "v1_g57_provider_execution_hardening_authorization_request_audit.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g57_request_audit_docs_and_fixture_exist() -> None:
    fixture = _load_fixture()

    assert fixture["audit_id"] == (
        "v1_g57_provider_execution_hardening_authorization_request_audit"
    )
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == (
        "audit-v1-g57-provider-execution-hardening-authorization-request"
    )
    assert fixture["source_branch"] == (
        "prepare-v1-g57-provider-execution-hardening-authorization-approval-request"
    )
    assert fixture["source_commit_before_audit"] == (
        "fb51718d6e778aa3d826f6de35b0cf529e933005"
    )
    assert fixture["audit_verdict"] == "PASS_REQUEST_ONLY_NOT_APPROVED"
    assert fixture["docs_tests_fixtures_only"] is True

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_g57_request_audit_preserves_unapproved_state() -> None:
    fixture = _load_fixture()

    assert fixture["implementation_approved"] is False
    assert fixture["operator_approval_recorded"] is False
    assert fixture["g56_latest_completed_gate"] is True
    assert fixture["g56_runtime_authority_chain_audit_complete"] is True
    assert fixture["g56_readiness_rollup_complete"] is True
    assert fixture["g57_active_request_gate"] is True
    assert fixture["g57_request_packet_prepared"] is True
    assert fixture["g57_operator_approval_recorded"] is False
    assert fixture["g57_runtime_implementation_approved"] is False
    assert fixture["g57_provider_execution_hardening_authorization_added"] is False
    assert fixture["valid_operator_choices"] == [
        "Approve-V1-G57",
        "Revise-V1-G57",
        "Pause",
    ]


def test_v1_g57_request_audit_forbidden_boundaries_remain_false() -> None:
    fixture = _load_fixture()

    for key in (
        "lima_runtime_files_changed_by_audit",
        "lima_public_api_changed_by_audit",
        "sparkbot_files_changed_by_audit",
        "arc_bot_shell_files_changed_by_audit",
        "provider_execution_expansion_added",
        "live_provider_model_call_execution_added",
        "provider_sdk_client_added",
        "built_in_provider_sdk_client_added",
        "sdk_dependency_added",
        "vendor_provider_sdk_import_added",
        "direct_provider_sdk_added",
        "provider_endpoint_resolution_added",
        "provider_endpoint_resolution_performed",
        "direct_network_code_added",
        "dns_lookup_added",
        "http_client_added",
        "socket_client_added",
        "network_call_performed_by_lima",
        "direct_provider_egress_performed_by_lima",
        "provider_readiness_network_check_added",
        "secret_lookup_added",
        "secret_lookup_performed",
        "credential_value_access_added",
        "credential_value_accessed",
        "provider_token_or_api_key_access_added",
        "provider_token_or_api_key_accessed",
        "credential_storage_rotation_migration_or_provisioning_added",
        "provider_configuration_changes_added",
        "fallback_execution_added",
        "tool_execution_added",
        "consumer_production_runtime_integration_added",
        "connector_browser_network_file_device_robotics_physical_world_behavior_added",
        "raw_prompt_persisted",
        "raw_model_response_persisted",
        "raw_customer_data_persisted",
        "raw_secret_or_credential_persisted",
        "raw_provider_token_or_api_key_persisted",
        "raw_diff_or_patch_persisted",
        "raw_file_content_persisted",
        "product_ready",
    ):
        assert fixture[key] is False, key

    assert fixture["credential_reference_metadata_only"] is True
    assert fixture["network_policy_metadata_only"] is True


def test_v1_g57_request_audit_doc_records_boundary_and_validation() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["audit"]).read_text(encoding="utf-8")

    assert "Audit verdict: `PASS_REQUEST_ONLY_NOT_APPROVED`" in text
    assert "does not approve V1-G57 implementation" in text
    assert "G57 implementation approval recorded: no" in text
    assert "Provider execution hardening authorization implementation added: no" in text
    assert "Provider SDK clients added: no" in text
    assert "Network calls by LIMA added: no" in text
    assert "Credential value access added: no" in text
    assert "Product readiness claimed: no" in text
    assert "4972 tests" in text
    assert "write access to `sparkpit-labs/Sparkbot` is still required" in text
    assert "The next step is an explicit operator decision" in text


def test_v1_g57_request_audit_status_docs_match_current_gate() -> None:
    fixture = _load_fixture()
    readme = (REPO_ROOT / fixture["documents"]["readme"]).read_text(encoding="utf-8")
    state = (
        REPO_ROOT / fixture["documents"]["current_project_state"]
    ).read_text(encoding="utf-8")
    target = (
        REPO_ROOT / fixture["documents"]["product_readiness_target"]
    ).read_text(encoding="utf-8")
    gap = (REPO_ROOT / fixture["documents"]["readiness_gap_matrix"]).read_text(
        encoding="utf-8"
    )

    for text in (readme, state, target, gap):
        assert "V1-G56" in text
        assert "V1-G57" in text
        assert "CANDIDATE_ONLY" in text
        assert "product readiness" in text

    assert "audited through `V1-G56`" in readme
    assert "V1-G57 provider execution hardening authorization approval request" in readme
    assert "V1 runtime authority chain audit through G56: complete." in state
    assert "V1-G57 provider execution hardening authorization evidence: complete and audited" in state
    assert "No additional V1-G61 implementation is approved" in target
    assert "Current active gate: `V1-RC-CUTOVER`" in gap


def test_v1_g57_request_audit_outputs_do_not_include_sensitive_markers() -> None:
    fixture = _load_fixture()
    output = json.dumps(fixture, sort_keys=True)
    output += (REPO_ROOT / fixture["documents"]["audit"]).read_text(
        encoding="utf-8"
    )

    for forbidden in (
        "diff --git",
        "@@",
        "BEGIN PATCH",
        "raw patch body",
        "raw prompt value",
        "raw model response value",
        "raw customer data value",
        "provider credential value",
        "provider token value",
        "api key value",
        "raw-secret-123",
    ):
        assert forbidden not in output
