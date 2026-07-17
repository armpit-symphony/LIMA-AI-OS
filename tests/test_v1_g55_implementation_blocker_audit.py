"""Static checks for the V1-G55 implementation blocker audit."""

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
    / "v1_g55_implementation_blocker_audit.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g55_blocker_audit_docs_and_fixture_exist() -> None:
    fixture = _load_fixture()

    assert fixture["audit_id"] == "v1_g55_implementation_blocker_audit"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["audit_branch"] == "audit-v1-g55-implementation-blocker"
    assert fixture["audited_request_branch"] == (
        "prepare-v1-g55-real-provider-sdk-network-egress-approval-request"
    )
    assert fixture["source_commit_before_audit"] == (
        "c14cae6cc814f62e784affe22e8ab37199687f95"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g55_blocker_is_missing_operator_decision() -> None:
    fixture = _load_fixture()
    decision = fixture["decision_record"]

    assert fixture["audit_verdict"] == "BLOCKED_PENDING_OPERATOR_DECISION"
    assert fixture["blocker"] == "missing_valid_approve_v1_g55_decision_record"
    assert fixture["required_unblock_choice"] == "Approve-V1-G55"
    assert fixture["required_approved_branch"] == (
        "v1-g55-real-provider-sdk-network-egress"
    )
    assert fixture["valid_operator_choices"] == [
        "Approve-V1-G55",
        "Revise-V1-G55",
        "Pause",
    ]
    assert decision["recorded_choice"] == "none"
    assert decision["recorded_approval_wording"] == "none"
    assert decision["approved_implementation_branch"] == "none"
    assert decision["implementation_approved"] is False


def test_v1_g55_broad_goal_and_request_are_not_approval() -> None:
    not_approval = set(_load_fixture()["inputs_that_are_not_approval"])

    assert "persistent_broad_goal" in not_approval
    assert "v1_g54_implementation" in not_approval
    assert "v1_g54_audit" in not_approval
    assert "v1_runtime_authority_chain_through_g54_audit" in not_approval
    assert "v1_readiness_rollup_through_g54" in not_approval
    assert "v1_post_g54_next_lane_decision_matrix" in not_approval
    assert "v1_g55_approval_request" in not_approval
    assert "v1_g55_work_order" in not_approval
    assert "v1_g55_preflight_audit" in not_approval
    assert "v1_g55_operator_decision_packet_with_recorded_choice_none" in not_approval
    assert "successful_validation_on_request_branch" in not_approval


def test_v1_g55_only_docs_work_can_continue_without_approval() -> None:
    can_continue = set(_load_fixture()["can_continue_without_approval"])
    cannot_continue = set(_load_fixture()["cannot_continue_without_approval"])

    assert can_continue == {
        "docs_tests_fixtures_review",
        "guard_docs",
        "audit_docs",
        "request_revision_work",
        "decision_recording_work",
    }
    assert "v1_g55_runtime_implementation" in cannot_continue
    assert "lima_runtime_file_changes_for_v1_g55" in cannot_continue
    assert "public_api_export_changes_for_v1_g55" in cannot_continue
    assert "bounded_real_provider_sdk_network_egress_wrapper" in cannot_continue
    assert "caller_injected_provider_sdk_network_executor_invocation" in cannot_continue
    assert "provider_sdk_network_egress_invocation" in cannot_continue
    assert "built_in_provider_sdk_clients" in cannot_continue
    assert "sdk_dependencies" in cannot_continue
    assert "vendor_sdk_imports" in cannot_continue
    assert "direct_provider_sdk_implementation" in cannot_continue
    assert "endpoint_resolution_by_lima" in cannot_continue
    assert "dns_http_socket_network_calls_by_lima" in cannot_continue
    assert "direct_provider_egress_by_lima" in cannot_continue
    assert "secret_lookup_or_credential_value_access" in cannot_continue
    assert "provider_token_or_api_key_access" in cannot_continue
    assert "provider_configuration_changes" in cannot_continue
    assert "fallback_execution" in cannot_continue
    assert "consumer_production_runtime_integration" in cannot_continue
    assert (
        "connector_browser_network_file_device_robotics_physical_world_behavior"
        in cannot_continue
    )
    assert "product_readiness" in cannot_continue
    assert "production_readiness" in cannot_continue


def test_v1_g55_blocker_audit_preserves_boundaries() -> None:
    boundaries = _load_fixture()["boundaries"]

    assert boundaries["runtime_behavior_added"] is False
    assert boundaries["bounded_real_provider_sdk_network_egress_wrapper_added"] is False
    assert boundaries["provider_sdk_network_egress_invocation_added"] is False
    assert boundaries["caller_injected_provider_sdk_network_executor_added"] is False
    assert boundaries["caller_injected_provider_sdk_network_executor_invoked"] is False
    assert boundaries["built_in_provider_sdk_client_added"] is False
    assert boundaries["real_provider_sdk_client_added_by_lima"] is False
    assert boundaries["sdk_dependency_added"] is False
    assert boundaries["vendor_provider_sdk_import_added"] is False
    assert boundaries["direct_provider_sdk_added"] is False
    assert boundaries["provider_endpoint_resolution_added"] is False
    assert boundaries["provider_endpoint_resolution_performed"] is False
    assert boundaries["direct_network_code_added"] is False
    assert boundaries["dns_lookup_added"] is False
    assert boundaries["http_client_added"] is False
    assert boundaries["socket_client_added"] is False
    assert boundaries["network_call_performed_by_lima"] is False
    assert boundaries["direct_provider_egress_performed_by_lima"] is False
    assert boundaries["secret_lookup_added"] is False
    assert boundaries["secret_lookup_performed"] is False
    assert boundaries["credential_value_access_added"] is False
    assert boundaries["credential_value_accessed"] is False
    assert boundaries["provider_token_or_api_key_access_added"] is False
    assert boundaries["provider_token_or_api_key_accessed"] is False
    assert boundaries["provider_configuration_changes_added"] is False
    assert boundaries["fallback_execution_added"] is False
    assert boundaries["lima_runtime_files_changed"] is False
    assert boundaries["lima_public_api_changed"] is False
    assert boundaries["sparkbot_touched"] is False
    assert boundaries["sparkbot_shell_touched"] is False
    assert boundaries["arc_bot_shell_touched"] is False
    assert boundaries["consumer_repos_touched"] is False
    assert boundaries["consumer_production_runtime_integration_added"] is False
    assert boundaries["connector_behavior_added"] is False
    assert boundaries["browser_file_network_device_robotics_physical_world_behavior_added"] is False
    assert boundaries["raw_prompt_persisted"] is False
    assert boundaries["raw_model_response_persisted"] is False
    assert boundaries["raw_customer_data_persisted"] is False
    assert boundaries["raw_secret_or_credential_persisted"] is False
    assert boundaries["raw_provider_token_or_api_key_persisted"] is False
    assert boundaries["raw_diff_or_patch_persisted"] is False
    assert boundaries["raw_file_content_persisted"] is False
    assert boundaries["product_ready"] is False
    assert boundaries["production_ready"] is False


def test_v1_g55_blocker_docs_match_fixture() -> None:
    fixture = _load_fixture()
    audit_text = (
        REPO_ROOT / fixture["documents"]["implementation_blocker_audit"]
    ).read_text(encoding="utf-8")
    approval_text = (REPO_ROOT / fixture["documents"]["approval_request"]).read_text(
        encoding="utf-8"
    )
    decision_text = (
        REPO_ROOT / fixture["documents"]["operator_decision_packet"]
    ).read_text(encoding="utf-8")

    assert "V1-G55 runtime implementation is blocked pending an explicit operator decision" in audit_text
    assert "Recorded choice: `none`" in audit_text
    assert "Approve-V1-G55" in audit_text
    assert "Implementation may start only from the valid `Approve-V1-G55` state" in decision_text
    assert "Approval request packet only: yes" in approval_text
    assert "Bounded real provider SDK/network egress authority approved: no" in approval_text
