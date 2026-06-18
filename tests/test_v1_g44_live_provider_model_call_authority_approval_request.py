"""Static checks for the V1-G44 live provider/model call authority request."""

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
    / "v1_g44_live_provider_model_call_authority_approval_request.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g44_request_docs_and_fixture_exist() -> None:
    fixture = _load_fixture()

    assert fixture["gate_id"] == "v1_g44_live_provider_model_call_authority_approval_request"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == (
        "prepare-v1-g44-live-provider-model-call-authority-approval-request"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g44_has_no_implementation_approval_yet() -> None:
    fixture = _load_fixture()
    decision = fixture["decision_record"]

    assert fixture["implementation_approved"] is False
    assert fixture["operator_approval_recorded"] is False
    assert fixture["live_provider_model_call_authority_approved"] is False
    assert fixture["live_provider_model_call_authority_added"] is False
    assert fixture["non_network_authority_validator_added"] is False
    assert fixture["live_provider_model_call_execution_added"] is False
    assert decision["recorded_choice"] == "none"
    assert decision["approved_implementation_branch"] == "none"
    assert decision["implementation_approved"] is False


def test_v1_g44_exact_decision_options_are_locked() -> None:
    fixture = _load_fixture()

    assert fixture["valid_operator_choices"] == [
        "Approve-V1-G44",
        "Revise-V1-G44",
        "Pause",
    ]
    assert fixture["required_approval_wording"].startswith(
        "I explicitly approve V1-G44 implementation"
    )
    assert fixture["proposed_implementation_branch"] == (
        "v1-g44-live-provider-model-call-authority"
    )


def test_v1_g44_edit_scope_is_non_network_and_non_executing() -> None:
    scope = _load_fixture()["edit_scope_if_operator_says_yes"]

    assert scope["lima_candidate_runtime_validator_docs_tests_fixtures_only"] is True
    assert scope["approved_consumer_files_empty"] is True
    assert scope["non_network_live_call_authority_validator_allowed"] is True
    assert scope["credential_reference_metadata_allowed"] is True
    assert scope["network_policy_reference_metadata_allowed"] is True
    assert scope["approval_evidence_metadata_required"] is True
    assert scope["audit_evidence_metadata_required"] is True
    assert scope["live_provider_model_call_execution_allowed"] is False
    assert scope["actual_model_request_dispatch_execution_allowed"] is False
    assert scope["network_calls_allowed"] is False
    assert scope["provider_readiness_network_check_allowed"] is False
    assert scope["token_guardian_live_routing_allowed"] is False
    assert scope["fallback_execution_allowed"] is False
    assert scope["secret_lookup_allowed"] is False
    assert scope["credential_value_access_allowed"] is False
    assert scope["tool_execution_allowed"] is False
    assert scope["consumer_repo_edits_allowed"] is False
    assert scope["consumer_runtime_source_edits_allowed"] is False
    assert scope["runtime_shell_wiring_execution_allowed"] is False
    assert scope["raw_prompt_or_model_response_persistence_allowed"] is False
    assert scope["raw_secret_or_credential_persistence_allowed"] is False
    assert scope["connector_browser_network_behavior_allowed"] is False
    assert scope["physical_world_behavior_allowed"] is False
    assert scope["product_readiness_claim_allowed"] is False


def test_v1_g44_approved_lima_file_scope_is_exact() -> None:
    fixture = _load_fixture()

    assert fixture["approved_lima_files_if_operator_says_yes"] == [
        "lima/harness/v1_live_provider_model_call_authority.py",
        "lima/harness/__init__.py",
        "docs/V1_G44_LIVE_PROVIDER_MODEL_CALL_AUTHORITY.md",
        "docs/V1_G44_LIVE_PROVIDER_MODEL_CALL_AUTHORITY_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g44_live_provider_model_call_authority.json",
        "tests/test_v1_g44_live_provider_model_call_authority.py",
    ]


def test_v1_g44_has_no_consumer_file_scope() -> None:
    fixture = _load_fixture()

    assert fixture["target_consumers"] == []
    assert fixture["approved_consumer_files_if_operator_says_yes"] == {}


def test_v1_g44_prior_evidence_refs_exist() -> None:
    fixture = _load_fixture()

    for relative_path in fixture["required_prior_evidence_refs"]:
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g44_forbidden_runtime_and_external_boundaries_remain_false() -> None:
    fixture = _load_fixture()

    for key in (
        "lima_runtime_files_changed_by_request",
        "consumer_repo_mutation_added_by_request",
        "sparkbot_files_changed_by_request",
        "arc_bot_shell_files_changed_by_request",
        "consumer_runtime_source_files_changed_by_request",
        "raw_prompt_persisted",
        "raw_model_response_persisted",
        "raw_customer_data_persisted",
        "raw_secret_or_credential_persisted",
        "raw_patch_bodies_persisted",
        "patches_applied",
        "adapter_symbols_called",
        "consumer_runtime_modules_imported",
        "runtime_shell_wiring_execution_added",
        "actual_model_request_dispatch_execution_added",
        "network_call_added",
        "provider_readiness_network_check_added",
        "token_guardian_live_routing_added",
        "fallback_execution_added",
        "secret_lookup_added",
        "credential_value_access_added",
        "tool_execution_added",
        "file_mutation_execution_added",
        "external_sends_added",
        "connector_browser_network_file_device_robotics_physical_world_behavior_added",
        "raw_sensitive_content_persisted_in_lima_evidence",
        "product_ready",
    ):
        assert fixture[key] is False


def test_v1_g44_docs_contain_live_call_authority_boundary_language() -> None:
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

    assert "live provider/model call authority metadata/preflight" in approval_text
    assert "non-executing" in approval_text
    assert "Live provider/model call execution added: no" in approval_text
    assert "Network call added: no" in approval_text
    assert "Credential value access added: no" in approval_text
    assert "Recorded choice: none" in decision_text
    assert "Recorded choice: Approve-V1-G44" in decision_text
    assert "Implementation must not start until `Approve-V1-G44`" in preflight_text
