"""Static checks for the V1-G46 live provider/model call execution request."""

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
    / "v1_g46_live_provider_model_call_execution_approval_request.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g46_request_docs_and_fixture_exist() -> None:
    fixture = _load_fixture()

    assert fixture["gate_id"] == (
        "v1_g46_live_provider_model_call_execution_approval_request"
    )
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == (
        "prepare-v1-g46-live-provider-model-call-execution-approval-request"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g46_has_no_implementation_approval_yet() -> None:
    fixture = _load_fixture()
    decision = fixture["decision_record"]

    assert fixture["implementation_approved"] is False
    assert fixture["operator_approval_recorded"] is False
    assert fixture["live_provider_model_call_execution_approved"] is False
    assert fixture["live_provider_model_call_execution_added"] is False
    assert fixture["provider_executor_invocation_added"] is False
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["public_api_fixture_refreshed"] is False
    assert decision["recorded_choice"] == "none"
    assert decision["approved_implementation_branch"] == "none"
    assert decision["implementation_approved"] is False


def test_v1_g46_exact_decision_options_are_locked() -> None:
    fixture = _load_fixture()

    assert fixture["valid_operator_choices"] == [
        "Approve-V1-G46",
        "Revise-V1-G46",
        "Pause",
    ]
    assert fixture["required_approval_wording"].startswith(
        "I explicitly approve V1-G46 implementation"
    )
    assert fixture["proposed_implementation_branch"] == (
        "v1-g46-live-provider-model-call-execution"
    )


def test_v1_g46_execution_target_is_exact() -> None:
    target = _load_fixture()["execution_target_if_operator_says_yes"]

    assert target["package"] == "lima.harness"
    assert target["new_runtime_module"] == (
        "lima/harness/v1_live_provider_model_call_execution.py"
    )
    assert target["export_surface"] == "lima.harness.__all__"
    assert target["symbols_to_add_to_all"] == [
        "V1LiveProviderModelCallExecutionError",
        "execute_v1_live_provider_model_call",
    ]
    assert target["requires_prevalidated_g44_authority"] is True
    assert target["provider_executor_must_be_injected"] is True
    assert target["direct_provider_sdk_allowed"] is False
    assert target["ambient_environment_secret_lookup_allowed"] is False
    assert target["fallback_execution_allowed"] is False
    assert target["consumer_repo_edits_allowed"] is False


def test_v1_g46_existing_harness_exports_must_be_preserved() -> None:
    target = _load_fixture()["execution_target_if_operator_says_yes"]

    assert target["required_existing_symbols_to_preserve"] == [
        "V1ProviderModelRoutingAuthorityError",
        "validate_v1_provider_model_routing_authority",
        "V1LiveProviderModelCallAuthorityError",
        "validate_v1_live_provider_model_call_authority",
    ]


def test_v1_g46_approved_file_scope_if_approved_is_exact() -> None:
    fixture = _load_fixture()

    assert fixture["approved_lima_runtime_files_if_operator_says_yes"] == [
        "lima/harness/v1_live_provider_model_call_execution.py",
        "lima/harness/__init__.py",
    ]
    assert set(fixture["approved_lima_docs_tests_fixtures_if_operator_says_yes"]) == {
        "docs/V1_G46_LIVE_PROVIDER_MODEL_CALL_EXECUTION.md",
        "docs/V1_G46_LIVE_PROVIDER_MODEL_CALL_EXECUTION_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g46_live_provider_model_call_execution.json",
        "tests/test_v1_g46_live_provider_model_call_execution.py",
        "tests/fixtures/runtime_extraction/v1_g22_final_public_api_freeze.json",
    }
    assert fixture["approved_consumer_files_if_operator_says_yes"] == []


def test_v1_g46_prior_evidence_refs_exist() -> None:
    fixture = _load_fixture()

    for relative_path in fixture["required_prior_evidence_refs"]:
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g46_forbidden_boundaries_remain_false_in_request() -> None:
    fixture = _load_fixture()

    for key in (
        "direct_provider_sdk_added",
        "direct_network_code_added",
        "consumer_repo_mutation_added",
        "sparkbot_files_changed",
        "arc_bot_shell_files_changed",
        "consumer_runtime_calls_added",
        "consumer_integration_added",
        "actual_model_request_dispatch_execution_added",
        "network_call_performed",
        "provider_readiness_network_check_added",
        "token_guardian_live_routing_added",
        "secret_lookup_added",
        "credential_value_access_added",
        "fallback_execution_added",
        "tool_execution_added",
        "connector_browser_network_file_device_robotics_physical_world_behavior_added",
        "raw_prompt_persisted",
        "raw_model_response_persisted",
        "raw_customer_data_persisted",
        "raw_diff_or_patch_persisted",
        "raw_file_content_persisted",
        "product_ready",
    ):
        assert fixture[key] is False


def test_v1_g46_docs_contain_execution_boundary_language() -> None:
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
    assert "provider executor must be injected" in approval_text
    assert "No Sparkbot or Arc-Bot-shell files" in approval_text
    assert "Live provider/model call execution approved: no" in approval_text
    assert "Recorded choice: none" in decision_text
    assert "Recorded choice: Approve-V1-G46" in decision_text
    assert "Implementation must not start until `Approve-V1-G46`" in preflight_text
