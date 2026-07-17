"""Static checks for the V1-G50 real provider executor invocation request."""

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
    / "v1_g50_real_provider_executor_invocation_approval_request.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g50_request_docs_and_fixture_exist() -> None:
    fixture = _load_fixture()

    assert fixture["gate_id"] == "v1_g50_real_provider_executor_invocation_approval_request"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert (
        fixture["branch"]
        == "prepare-v1-g50-real-provider-executor-invocation-approval-request"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g50_has_no_implementation_approval_yet() -> None:
    fixture = _load_fixture()
    decision = fixture["decision_record"]

    assert fixture["implementation_approved"] is False
    assert fixture["operator_approval_recorded"] is False
    assert fixture["real_provider_executor_invocation_metadata_approved"] is False
    assert fixture["real_provider_executor_invocation_metadata_added"] is False
    assert fixture["executable_provider_invocation_approved"] is False
    assert fixture["executable_provider_invocation_added"] is False
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["lima_public_api_changed"] is False
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["arc_bot_shell_files_changed"] is False
    assert fixture["provider_executor_invocation_added"] is False
    assert decision["recorded_choice"] == "none"
    assert decision["approved_implementation_branch"] == "none"
    assert decision["implementation_approved"] is False


def test_v1_g50_exact_decision_options_are_locked() -> None:
    fixture = _load_fixture()

    assert fixture["valid_operator_choices"] == [
        "Approve-V1-G50",
        "Revise-V1-G50",
        "Pause",
    ]
    assert fixture["required_approval_wording"].startswith(
        "I explicitly approve V1-G50 implementation"
    )
    assert (
        fixture["proposed_implementation_branch"]
        == "v1-g50-real-provider-executor-invocation"
    )


def test_v1_g50_invocation_target_is_metadata_only() -> None:
    target = _load_fixture()[
        "real_provider_executor_invocation_target_if_operator_says_yes"
    ]

    assert target["invocation_metadata_only"] is True
    assert target["invocation_request_envelope_metadata_only"] is True
    assert target["invocation_response_envelope_metadata_only"] is True
    assert target["non_executing"] is True
    assert target["proof_not_execution"] is True
    assert target["provider_executor_invocation_allowed"] is False
    assert target["real_provider_executor_invocation_allowed"] is False
    assert target["fake_provider_executor_invocation_allowed"] is False
    assert target["executable_provider_invocation_allowed"] is False
    assert target["credential_reference_metadata_only"] is True
    assert target["credential_values_allowed"] is False
    assert target["secret_lookup_allowed"] is False
    assert target["network_policy_reference_metadata_only"] is True
    assert target["deny_by_default_network_required"] is True
    assert target["provider_endpoint_resolution_allowed"] is False
    assert target["network_calls_allowed"] is False
    assert target["provider_sdk_clients_allowed"] is False
    assert target["fallback_execution_allowed"] is False
    assert target["connector_browser_network_physical_world_allowed"] is False
    assert target["product_readiness_claim_allowed"] is False


def test_v1_g50_approved_file_scope_if_approved_is_exact() -> None:
    fixture = _load_fixture()

    assert fixture["approved_lima_runtime_files_if_operator_says_yes"] == []
    assert fixture["approved_lima_docs_tests_fixtures_if_operator_says_yes"] == [
        "docs/V1_G50_REAL_PROVIDER_EXECUTOR_INVOCATION.md",
        "docs/V1_G50_REAL_PROVIDER_EXECUTOR_INVOCATION_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g50_real_provider_executor_invocation.json",
        "tests/test_v1_g50_real_provider_executor_invocation.py",
    ]
    assert fixture["approved_sparkbot_files_if_operator_says_yes"] == []
    assert fixture["approved_arc_bot_shell_files_if_operator_says_yes"] == []


def test_v1_g50_prior_evidence_refs_exist() -> None:
    fixture = _load_fixture()

    for relative_path in fixture["required_prior_evidence_refs"]:
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g50_forbidden_boundaries_remain_false_in_request() -> None:
    fixture = _load_fixture()

    for key in (
        "consumer_repo_mutation_added",
        "consumer_runtime_calls_added",
        "live_provider_model_call_execution_added",
        "provider_executor_invocation_added",
        "real_provider_executor_invocation_added",
        "fake_provider_executor_invocation_added",
        "direct_provider_sdk_added",
        "direct_network_code_added",
        "provider_endpoint_resolution_added",
        "network_call_performed",
        "ambient_environment_secret_lookup_added",
        "secret_lookup_added",
        "credential_value_access_added",
        "provider_token_or_api_key_access_added",
        "credential_storage_or_rotation_added",
        "provider_configuration_changes_added",
        "fallback_execution_added",
        "provider_readiness_network_check_added",
        "token_guardian_live_routing_added",
        "tool_execution_added",
        "connector_browser_network_file_device_robotics_physical_world_behavior_added",
        "raw_prompt_persisted",
        "raw_model_response_persisted",
        "raw_customer_data_persisted",
        "raw_secret_or_credential_persisted",
        "provider_token_or_api_key_persisted",
        "raw_diff_or_patch_persisted",
        "raw_file_content_persisted",
        "product_ready",
    ):
        assert fixture[key] is False


def test_v1_g50_docs_contain_boundary_language() -> None:
    fixture = _load_fixture()
    approval_text = (REPO_ROOT / fixture["documents"]["approval_request"]).read_text(
        encoding="utf-8"
    )
    decision_text = (REPO_ROOT / fixture["documents"]["operator_decision_packet"]).read_text(
        encoding="utf-8"
    )
    preflight_text = (REPO_ROOT / fixture["documents"]["preflight_audit"]).read_text(
        encoding="utf-8"
    )

    assert "Approval request packet only: yes" in approval_text
    assert "Executable provider invocation approved: no" in approval_text
    assert "Provider executor invoked by this request: no" in approval_text
    assert "Network calls allowed: no" in approval_text
    assert "Provider SDK clients allowed: no" in approval_text
    assert "Recorded choice: none" in decision_text
    assert "Template for `Approve-V1-G50`" in decision_text
    assert "Implementation must not start until `Approve-V1-G50`" in preflight_text
