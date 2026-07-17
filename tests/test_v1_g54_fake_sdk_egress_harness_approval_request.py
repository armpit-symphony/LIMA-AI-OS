"""Static checks for the V1-G54 fake SDK/fake-egress harness request."""

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
    / "v1_g54_fake_sdk_egress_harness_approval_request.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g54_request_docs_and_fixture_exist() -> None:
    fixture = _load_fixture()

    assert fixture["gate_id"] == "v1_g54_fake_sdk_egress_harness_approval_request"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "prepare-v1-g54-fake-sdk-egress-harness-approval-request"
    assert fixture["docs_tests_fixtures_only_request"] is True

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g54_has_no_implementation_approval_yet() -> None:
    fixture = _load_fixture()
    decision = fixture["decision_record"]

    assert fixture["implementation_approved"] is False
    assert fixture["operator_approval_recorded"] is False
    assert fixture["fake_sdk_egress_harness_approved"] is False
    assert fixture["fake_sdk_egress_harness_added"] is False
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["lima_public_api_changed"] is False
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["arc_bot_shell_files_changed"] is False
    assert fixture["fake_sdk_harness_added"] is False
    assert fixture["fake_egress_harness_added"] is False
    assert decision["recorded_choice"] == "none"
    assert decision["approved_implementation_branch"] == "none"
    assert decision["implementation_approved"] is False


def test_v1_g54_exact_decision_options_are_locked() -> None:
    fixture = _load_fixture()

    assert fixture["valid_operator_choices"] == [
        "Approve-V1-G54",
        "Revise-V1-G54",
        "Pause",
    ]
    assert fixture["required_approval_wording"] == (
        "I explicitly approve V1-G54 implementation of the LIMA-side fake "
        "SDK/fake-egress harness evidence slice, limited to the file scope, "
        "behavior scope, tests, rollback plan, and stop conditions in "
        "docs/V1_G54_FAKE_SDK_EGRESS_HARNESS_APPROVAL_REQUEST.md."
    )
    assert fixture["proposed_implementation_branch"] == (
        "v1-g54-fake-sdk-egress-harness"
    )


def test_v1_g54_fake_harness_target_if_approved_is_exact() -> None:
    target = _load_fixture()["fake_sdk_egress_harness_target_if_operator_says_yes"]

    assert target == {
        "fake_in_process_sdk_harness_evidence_allowed": True,
        "fake_in_process_egress_harness_evidence_allowed": True,
        "test_module_local_fake_components_only": True,
        "docs_tests_fixtures_only": True,
        "real_provider_sdk_client_allowed": False,
        "built_in_provider_sdk_client_allowed": False,
        "sdk_dependency_addition_allowed": False,
        "direct_provider_sdk_implementation_allowed": False,
        "provider_endpoint_resolution_execution_allowed": False,
        "dns_lookup_allowed": False,
        "http_client_allowed": False,
        "socket_client_allowed": False,
        "network_calls_allowed": False,
        "direct_provider_egress_allowed": False,
        "credential_value_access_allowed": False,
        "secret_lookup_allowed": False,
        "provider_token_or_api_key_access_allowed": False,
        "provider_configuration_changes_allowed": False,
        "fallback_execution_allowed": False,
        "connector_browser_network_physical_world_allowed": False,
        "consumer_production_runtime_integration_allowed": False,
        "product_readiness_claim_allowed": False,
    }


def test_v1_g54_approved_file_scope_if_approved_is_exact() -> None:
    fixture = _load_fixture()

    assert fixture["approved_lima_runtime_files_if_operator_says_yes"] == []
    assert fixture["approved_lima_docs_tests_fixtures_if_operator_says_yes"] == [
        "docs/V1_G54_FAKE_SDK_EGRESS_HARNESS.md",
        "docs/V1_G54_FAKE_SDK_EGRESS_HARNESS_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g54_fake_sdk_egress_harness.json",
        "tests/test_v1_g54_fake_sdk_egress_harness.py",
    ]
    assert fixture["approved_sparkbot_files_if_operator_says_yes"] == []
    assert fixture["approved_arc_bot_shell_files_if_operator_says_yes"] == []


def test_v1_g54_prior_evidence_refs_exist() -> None:
    fixture = _load_fixture()

    for relative_path in fixture["required_prior_evidence_refs"]:
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g54_forbidden_boundaries_remain_false_in_request() -> None:
    fixture = _load_fixture()

    for key in (
        "consumer_repo_mutation_added",
        "consumer_runtime_calls_added",
        "consumer_production_runtime_integration_added",
        "live_provider_model_call_execution_added",
        "provider_executor_invocation_added",
        "real_provider_executor_invocation_added",
        "fake_provider_executor_invocation_added",
        "fake_sdk_harness_added",
        "fake_sdk_harness_executed",
        "fake_egress_harness_added",
        "fake_egress_harness_executed",
        "real_provider_sdk_client_added",
        "built_in_provider_sdk_client_added",
        "sdk_dependency_added",
        "direct_provider_sdk_added",
        "provider_endpoint_resolution_added",
        "provider_endpoint_resolution_performed",
        "direct_network_code_added",
        "dns_lookup_added",
        "http_client_added",
        "socket_client_added",
        "network_call_performed",
        "direct_provider_egress_added",
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
        assert fixture[key] is False

    assert fixture["credential_reference_metadata_only"] is True


def test_v1_g54_docs_contain_fake_harness_boundary_language() -> None:
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

    assert "Approval request packet only: yes" in approval_text
    assert "Fake SDK/fake-egress harness evidence approved: no" in approval_text
    assert "Real provider SDK client added: no" in approval_text
    assert "Network call performed: no" in approval_text
    assert "Recorded choice: none" in decision_text
    assert "Recorded choice: Approve-V1-G54" in decision_text
    assert "Implementation must not start until `Approve-V1-G54`" in preflight_text
