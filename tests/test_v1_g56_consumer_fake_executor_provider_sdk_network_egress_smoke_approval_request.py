"""Static checks for the V1-G56 consumer fake-executor SDK/network egress request."""

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
    / "v1_g56_consumer_fake_executor_provider_sdk_network_egress_smoke_approval_request.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g56_request_docs_and_fixture_exist() -> None:
    fixture = _load_fixture()

    assert fixture["gate_id"] == (
        "v1_g56_consumer_fake_executor_provider_sdk_network_egress_smoke_approval_request"
    )
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == (
        "prepare-v1-g56-consumer-fake-executor-provider-sdk-network-egress-smoke-approval-request"
    )
    assert fixture["docs_tests_fixtures_only_request"] is True

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g56_records_approval_without_implementation_yet() -> None:
    fixture = _load_fixture()
    decision = fixture["decision_record"]

    assert fixture["implementation_approved"] is True
    assert fixture["operator_approval_recorded"] is True
    assert (
        fixture["consumer_fake_executor_provider_sdk_network_egress_smoke_approved"]
        is True
    )
    assert (
        fixture["consumer_fake_executor_provider_sdk_network_egress_smoke_added"]
        is False
    )
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["lima_public_api_changed"] is False
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["arc_bot_shell_files_changed"] is False
    assert fixture["v1_g55_wrapper_invoked"] is False
    assert fixture["fake_provider_sdk_network_executor_invoked"] is False
    assert decision["recorded_choice"] == "Approve-V1-G56"
    assert decision["recorded_approval_wording"] == fixture["required_approval_wording"]
    assert decision["approved_implementation_branch"] == (
        "v1-g56-consumer-fake-executor-provider-sdk-network-egress-smoke"
    )
    assert decision["implementation_approved"] is True


def test_v1_g56_exact_decision_options_are_locked() -> None:
    fixture = _load_fixture()

    assert fixture["valid_operator_choices"] == [
        "Approve-V1-G56",
        "Revise-V1-G56",
        "Pause",
    ]
    assert fixture["required_approval_wording"] == (
        "I explicitly approve V1-G56 implementation of the consumer "
        "fake-executor provider SDK/network egress smoke slice, limited to the "
        "file scope, behavior scope, tests, rollback plan, and stop conditions "
        "in docs/V1_G56_CONSUMER_FAKE_EXECUTOR_PROVIDER_SDK_NETWORK_EGRESS_SMOKE_APPROVAL_REQUEST.md."
    )
    assert fixture["proposed_implementation_branch"] == (
        "v1-g56-consumer-fake-executor-provider-sdk-network-egress-smoke"
    )


def test_v1_g56_target_is_consumer_fake_executor_only() -> None:
    target = _load_fixture()["consumer_fake_executor_target_if_operator_says_yes"]

    assert target["consumer_fake_executor_smoke_allowed"] is True
    assert target["import_v1_g55_public_harness_symbols_allowed"] is True
    assert target["call_v1_g55_wrapper_allowed"] is True
    assert target["fake_in_process_provider_sdk_network_executor_only"] is True
    assert (
        target[
            "sanitized_v1_g48_v1_g50_v1_g51_v1_g53_v1_g54_v1_g55_metadata_required"
        ]
        is True
    )
    assert target["sanitized_evidence_only_required"] is True
    assert target["sparkbot_test_fixture_scope_allowed"] is True
    assert target["arc_bot_shell_test_fixture_scope_allowed"] is True

    for key in (
        "lima_runtime_file_change_allowed",
        "consumer_production_runtime_code_edit_allowed",
        "built_in_provider_sdk_client_allowed",
        "sdk_dependency_addition_allowed",
        "vendor_provider_sdk_import_allowed",
        "direct_provider_sdk_implementation_allowed",
        "provider_endpoint_resolution_by_lima_allowed",
        "dns_lookup_by_lima_allowed",
        "http_client_by_lima_allowed",
        "socket_client_by_lima_allowed",
        "network_calls_by_lima_allowed",
        "direct_provider_egress_by_lima_allowed",
        "credential_value_access_allowed",
        "secret_lookup_allowed",
        "provider_token_or_api_key_access_allowed",
        "provider_configuration_changes_allowed",
        "fallback_execution_allowed",
        "connector_browser_network_physical_world_allowed",
        "consumer_production_runtime_integration_allowed",
        "product_readiness_claim_allowed",
    ):
        assert target[key] is False, key


def test_v1_g56_approved_file_scope_if_approved_is_exact() -> None:
    fixture = _load_fixture()

    assert fixture["approved_lima_runtime_files_if_operator_says_yes"] == []
    assert fixture["approved_lima_docs_tests_fixtures_if_operator_says_yes"] == [
        "docs/V1_G56_CONSUMER_FAKE_EXECUTOR_PROVIDER_SDK_NETWORK_EGRESS_SMOKE.md",
        "docs/V1_G56_CONSUMER_FAKE_EXECUTOR_PROVIDER_SDK_NETWORK_EGRESS_SMOKE_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g56_consumer_fake_executor_provider_sdk_network_egress_smoke.json",
        "tests/test_v1_g56_consumer_fake_executor_provider_sdk_network_egress_smoke.py",
    ]
    assert fixture["approved_sparkbot_files_if_operator_says_yes"] == [
        "tests/test_sparkbot_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.py",
        "tests/fixtures/sparkbot_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.json",
    ]
    assert fixture["approved_arc_bot_shell_files_if_operator_says_yes"] == [
        "tests/test_arc_bot_shell_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.py",
        "tests/fixtures/arc_bot_shell_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.json",
    ]


def test_v1_g56_prior_evidence_refs_exist() -> None:
    for relative_path in _load_fixture()["required_prior_evidence_refs"]:
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g56_forbidden_boundaries_remain_false_in_request() -> None:
    fixture = _load_fixture()

    for key in (
        "consumer_repo_mutation_added",
        "consumer_runtime_calls_added",
        "consumer_production_runtime_integration_added",
        "live_provider_model_call_execution_added",
        "v1_g55_wrapper_invoked",
        "fake_provider_sdk_network_executor_invoked",
        "provider_sdk_network_egress_invocation_added",
        "real_provider_sdk_client_added_by_lima",
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


def test_v1_g56_docs_contain_request_only_boundary_language() -> None:
    fixture = _load_fixture()
    approval_text = (REPO_ROOT / fixture["documents"]["approval_request"]).read_text(
        encoding="utf-8"
    )
    decision_text = (
        REPO_ROOT / fixture["documents"]["operator_decision_packet"]
    ).read_text(encoding="utf-8")
    preflight_text = (REPO_ROOT / fixture["documents"]["preflight_audit"]).read_text(
        encoding="utf-8"
    )
    work_order_text = (REPO_ROOT / fixture["documents"]["work_order"]).read_text(
        encoding="utf-8"
    )

    assert "Approval request packet only: yes" in approval_text
    assert "Implementation approved by this request: no" in approval_text
    assert "V1-G55 wrapper invoked by this request: no" in approval_text
    assert "Fake provider SDK/network executor invoked by this request: no" in approval_text
    assert "Built-in provider SDK client added: no" in approval_text
    assert "Network calls performed by LIMA: no" in approval_text
    assert "Direct provider egress performed by LIMA: no" in approval_text
    assert "Recorded choice: `Approve-V1-G56`" in decision_text
    assert "Implementation approved: yes" in decision_text
    assert "Template for `Approve-V1-G56`" in decision_text
    assert "Implementation must not start until `Approve-V1-G56`" in preflight_text
    assert "No `lima/` runtime files may be changed." in work_order_text


def test_v1_g56_docs_and_fixture_do_not_include_sensitive_markers() -> None:
    fixture = _load_fixture()
    output = json.dumps(fixture, sort_keys=True)
    for relative_path in fixture["documents"].values():
        output += (REPO_ROOT / relative_path).read_text(encoding="utf-8")

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
