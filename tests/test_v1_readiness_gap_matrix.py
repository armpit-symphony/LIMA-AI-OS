"""Static checks for the V1 readiness gap matrix."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = REPO_ROOT / "docs" / "V1_READINESS_GAP_MATRIX.md"
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_readiness_gap_matrix.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_gap_matrix_exists_and_preserves_non_implementation_scope() -> None:
    fixture = _load_fixture()

    assert DOC_PATH.exists()
    assert fixture["document"] == "docs/V1_READINESS_GAP_MATRIX.md"
    assert fixture["source_target"] == "docs/V1_PRODUCT_READINESS_TARGET.md"
    assert fixture["current_branch"] == (
        "prepare-v1-g57-provider-execution-hardening-authorization-approval-request"
    )
    assert fixture["source_commit_before_matrix_refresh"] == (
        "7c7f7ee6f566cbbc1d6eac5b3bd9e6a0ad2dba16"
    )
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["implementation_approved"] is False
    assert fixture["v1_product_ready"] is False


def test_v1_gap_matrix_names_first_shell_consumers() -> None:
    assert set(_load_fixture()["first_shell_consumers"]) == {
        "Sparkbot_shell",
        "Sparkbot",
        "Arc-Bot-shell",
    }


def test_v1_gap_matrix_current_anchor_is_g57_request_prep() -> None:
    anchor = _load_fixture()["current_anchor"]

    assert anchor["latest_completed_gate"] == "V1-G56"
    assert anchor["current_gate"] == "V1-G57"
    assert anchor["g55_operator_approval_recorded"] is True
    assert anchor["g55_runtime_implementation_approved"] is True
    assert anchor["g55_independent_audit_complete"] is True
    assert anchor["g56_request_packet_prepared"] is True
    assert anchor["g56_operator_approval_recorded"] is True
    assert anchor["g56_runtime_implementation_approved"] is True
    assert anchor["g56_independent_audit_complete"] is True
    assert anchor["g57_request_packet_prepared"] is True
    assert anchor["g57_operator_approval_recorded"] is False
    assert anchor["g57_runtime_implementation_approved"] is False
    assert anchor["next_required_artifact"] == (
        "v1_g57_provider_execution_hardening_authorization_approval_request"
    )
    assert anchor["next_required_action"] == "record_v1_g57_operator_decision"
    assert anchor["valid_operator_choices"] == [
        "Approve-V1-G57",
        "Revise-V1-G57",
        "Pause",
    ]


def test_v1_gap_matrix_covers_expected_gap_groups() -> None:
    groups = {group["ids"]: group for group in _load_fixture()["gap_groups"]}

    assert set(groups) == {
        "V1-G1..V1-G10",
        "V1-G11..V1-G17",
        "V1-G18..V1-G28",
        "V1-G29..V1-G42",
        "V1-G43..V1-G56",
        "V1-G57",
    }
    assert groups["V1-G1..V1-G10"]["status"] == (
        "complete_historical_candidate_only_evidence"
    )
    assert groups["V1-G43..V1-G56"]["status"] == (
        "complete_prior_approved_provider_authority_fake_egress_g55_wrapper_and_g56_consumer_smoke_evidence"
    )
    g57 = groups["V1-G57"]
    assert g57["status"] == (
        "approval_request_prepared_awaiting_operator_decision_implementation_not_approved"
    )
    assert (
        g57["approval_request_document"]
        == "docs/V1_G57_PROVIDER_EXECUTION_HARDENING_AUTHORIZATION_APPROVAL_REQUEST.md"
    )
    assert (
        g57["operator_decision_packet_document"]
        == "docs/V1_G57_PROVIDER_EXECUTION_HARDENING_AUTHORIZATION_OPERATOR_DECISION_PACKET.md"
    )
    assert (
        g57["next_lane_matrix_document"]
        == "docs/readiness/V1_POST_G56_NEXT_LANE_DECISION_MATRIX.md"
    )
    assert (
        g57["g56_smoke_audit_document"]
        == "docs/audits/V1_G56_CONSUMER_FAKE_EXECUTOR_PROVIDER_SDK_NETWORK_EGRESS_SMOKE_AUDIT.md"
    )
    assert (
        g57["g56_chain_audit_document"]
        == "docs/audits/V1_RUNTIME_AUTHORITY_CHAIN_THROUGH_G56_AUDIT.md"
    )
    assert g57["g57_request_packet_prepared"] is True
    assert g57["g57_operator_approval_recorded"] is False
    assert g57["runtime_implementation_added"] is False
    assert g57["runtime_approval_needed"] is True


def test_v1_gap_matrix_recommends_g57_request_preparation() -> None:
    fixture = _load_fixture()

    assert fixture["next_smallest_safe_step"] == "record_v1_g57_operator_decision"
    assert fixture["next_smallest_safe_step_status"] == "pending_operator_decision"
    assert fixture["next_smallest_safe_step_reason"] == (
        "g56_consumer_smoke_is_audited_and_next_provider_execution_hardening_should_remain_metadata_only"
    )


def test_v1_gap_matrix_stop_conditions_cover_forbidden_g57_surfaces() -> None:
    stop_conditions = set(_load_fixture()["stop_conditions"])

    assert "g57_provider_execution_hardening_authorization_implementation_without_exact_approval" in stop_conditions
    assert "file_scope_outside_future_g57_request" in stop_conditions
    assert "sparkbot_or_arc_bot_shell_modification_for_g57_without_exact_approval" in stop_conditions
    assert "credential_handling_or_real_provider_sdk_network_egress_in_hardening_authorization_lane" in stop_conditions
    assert "built_in_provider_sdk_client" in stop_conditions
    assert "sdk_dependency" in stop_conditions
    assert "vendor_sdk_import" in stop_conditions
    assert "endpoint_resolution_by_lima" in stop_conditions
    assert "dns_http_socket_network_calls_by_lima" in stop_conditions
    assert "direct_provider_egress_by_lima" in stop_conditions
    assert "secret_lookup_or_credential_value_access" in stop_conditions
    assert "provider_configuration_change" in stop_conditions
    assert "fallback_execution" in stop_conditions
    assert "consumer_production_runtime_integration" in stop_conditions
    assert (
        "connector_browser_network_file_device_robotics_physical_world_behavior"
        in stop_conditions
    )
    assert "v1_product_or_production_readiness_claim" in stop_conditions


def test_v1_gap_matrix_boundary_results_add_no_new_runtime_behavior() -> None:
    boundary = _load_fixture()["boundary_results"]

    assert boundary["v1_g56_request_packet_added"] is True
    assert boundary["v1_g56_operator_approval_recorded"] is True
    assert boundary["v1_g56_runtime_implementation_added"] is True
    assert boundary["v1_g57_request_packet_added"] is True
    assert boundary["v1_g57_operator_approval_recorded"] is False
    assert boundary["v1_g57_runtime_implementation_added"] is False

    for key in (
        "runtime_behavior_added_by_refresh",
        "lima_runtime_files_changed_by_refresh",
        "tests_support_changed",
        "shell_repos_changed_by_refresh",
        "built_in_provider_sdk_client_added",
        "sdk_dependency_added",
        "vendor_sdk_import_added",
        "provider_endpoint_resolution_by_lima_added",
        "network_call_performed_by_lima",
        "secret_lookup_added",
        "credential_value_access_added",
        "provider_token_or_api_key_access_added",
        "provider_configuration_changes_added",
        "fallback_execution_added",
        "consumer_production_runtime_integration_added",
        "connector_browser_network_file_device_robotics_physical_world_behavior_added",
        "v1_release_claimed",
    ):
        assert boundary[key] is False, key


def test_v1_gap_matrix_doc_matches_g57_next_step_and_boundaries() -> None:
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "This matrix turns the V1 product target into the current implementation-readiness sequence." in text
    assert "Current active gate: `V1-G57`" in text
    assert "`V1-G43` through `V1-G56`" in text
    assert "`V1-G57`" in text
    assert "Awaiting operator decision; implementation not approved" in text
    assert "V1-G57 provider execution hardening authorization implementation without exact approval" in text
    assert "credential handling or real provider SDK/network egress in a hardening authorization lane" in text
    assert "built-in provider SDK clients" in text
    assert "LIMA-owned DNS, HTTP, socket, network calls" in text
    assert "secret lookup, credential value access" in text
    assert "V1 product readiness, production readiness" in text
    assert "The next smallest safe step is to record exactly one operator choice in the V1-G57 provider execution hardening authorization operator decision packet." in text
