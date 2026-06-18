"""Static checks for the V1-G52 consumer fake-executor smoke request."""

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
    / "v1_g52_consumer_fake_executor_provider_invocation_smoke_approval_request.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g52_request_docs_and_fixture_exist() -> None:
    fixture = _load_fixture()

    assert fixture["gate_id"] == (
        "v1_g52_consumer_fake_executor_provider_invocation_smoke_approval_request"
    )
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == (
        "prepare-v1-g52-consumer-fake-executor-provider-invocation-smoke-approval-request"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g52_has_no_implementation_approval_yet() -> None:
    fixture = _load_fixture()
    decision = fixture["decision_record"]

    assert fixture["implementation_approved"] is False
    assert fixture["operator_approval_recorded"] is False
    assert fixture["consumer_fake_executor_provider_invocation_smoke_approved"] is False
    assert fixture["consumer_fake_executor_provider_invocation_smoke_added"] is False
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["arc_bot_shell_files_changed"] is False
    assert fixture["fake_provider_executor_invocation_added"] is False
    assert decision["recorded_choice"] == "none"
    assert decision["approved_implementation_branch"] == "none"
    assert decision["implementation_approved"] is False


def test_v1_g52_exact_decision_options_are_locked() -> None:
    fixture = _load_fixture()

    assert fixture["valid_operator_choices"] == [
        "Approve-V1-G52",
        "Revise-V1-G52",
        "Pause",
    ]
    assert fixture["required_approval_wording"].startswith(
        "I explicitly approve V1-G52 implementation"
    )
    assert fixture["proposed_implementation_branch"] == (
        "v1-g52-consumer-fake-executor-provider-invocation-smoke"
    )


def test_v1_g52_consumer_smoke_target_is_exact() -> None:
    target = _load_fixture()["consumer_smoke_target_if_operator_says_yes"]

    assert target["public_lima_package"] == "lima.harness"
    assert target["symbols_to_import"] == [
        "V1ExecutableRealProviderExecutorInvocationError",
        "execute_v1_executable_real_provider_executor_invocation",
    ]
    assert target["provider_executor_type"] == "fake_in_process_executor_only"
    assert target["uses_v1_g50_envelope_metadata"] is True
    assert target["live_provider_credentials_allowed"] is False
    assert target["network_calls_allowed"] is False
    assert target["provider_endpoint_resolution_allowed"] is False
    assert target["fallback_execution_allowed"] is False
    assert target["connector_browser_network_physical_world_allowed"] is False
    assert target["product_readiness_claim_allowed"] is False


def test_v1_g52_approved_file_scope_if_approved_is_exact() -> None:
    fixture = _load_fixture()

    assert fixture["approved_lima_runtime_files_if_operator_says_yes"] == []
    assert set(fixture["approved_lima_docs_tests_fixtures_if_operator_says_yes"]) == {
        "docs/V1_G52_CONSUMER_FAKE_EXECUTOR_PROVIDER_INVOCATION_SMOKE.md",
        "docs/V1_G52_CONSUMER_FAKE_EXECUTOR_PROVIDER_INVOCATION_SMOKE_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g52_consumer_fake_executor_provider_invocation_smoke.json",
        "tests/test_v1_g52_consumer_fake_executor_provider_invocation_smoke.py",
    }
    assert fixture["approved_sparkbot_files_if_operator_says_yes"] == [
        "tests/test_sparkbot_lima_v1_g52_fake_executor_provider_invocation_smoke.py",
        "tests/fixtures/sparkbot_lima_v1_g52_fake_executor_provider_invocation_smoke.json",
    ]
    assert fixture["approved_arc_bot_shell_files_if_operator_says_yes"] == [
        "tests/test_arc_bot_shell_lima_v1_g52_fake_executor_provider_invocation_smoke.py",
        "tests/fixtures/arc_bot_shell_lima_v1_g52_fake_executor_provider_invocation_smoke.json",
    ]


def test_v1_g52_prior_evidence_refs_exist() -> None:
    fixture = _load_fixture()

    for relative_path in fixture["required_prior_evidence_refs"]:
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g52_forbidden_boundaries_remain_false_in_request() -> None:
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
        "secret_lookup_added",
        "credential_value_access_added",
        "provider_token_or_api_key_access_added",
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


def test_v1_g52_docs_contain_consumer_boundary_language() -> None:
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
    assert "fake in-process provider executor only" in approval_text
    assert "Consumer repository edits approved: no" in approval_text
    assert "No live provider credentials" in approval_text
    assert "Recorded choice: none" in decision_text
    assert "Recorded choice: Approve-V1-G52" in decision_text
    assert "Implementation must not start until `Approve-V1-G52`" in preflight_text
