"""Tests for the approved V1-G56 consumer fake-executor SDK/network smoke."""

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
    / "v1_g56_consumer_fake_executor_provider_sdk_network_egress_smoke.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _load_consumer_fixture(consumer_key: str) -> dict[str, Any]:
    consumer = _load_fixture()["consumer_repositories"][consumer_key]
    consumer_root = (REPO_ROOT / consumer["local_path"]).resolve()
    fixture = json.loads(
        (consumer_root / consumer["fixture_ref"]).read_text(encoding="utf-8")
    )
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g56_fixture_records_approved_scope_and_status() -> None:
    fixture = _load_fixture()

    assert fixture["packet_set_id"] == (
        "v1_g56_consumer_fake_executor_provider_sdk_network_egress_smoke"
    )
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == (
        "v1-g56-consumer-fake-executor-provider-sdk-network-egress-smoke"
    )
    assert fixture["operator_decision"] == "Approve-V1-G56"
    assert fixture["approved_scope"] == (
        "consumer_fake_executor_provider_sdk_network_egress_smoke_slice"
    )
    assert (
        fixture["consumer_fake_executor_provider_sdk_network_egress_smoke_approved"]
        is True
    )
    assert (
        fixture["consumer_fake_executor_provider_sdk_network_egress_smoke_added"]
        is True
    )
    assert fixture["v1_g48_g50_g51_g53_g54_g55_authority_metadata_used"] is True
    assert (
        fixture["fake_in_process_provider_sdk_network_executor_invoked_by_consumer_tests"]
        is True
    )
    assert fixture["g55_public_wrapper_invoked_by_consumer_tests"] is True
    assert fixture["product_ready"] is False


def test_v1_g56_lima_file_scope_is_exact_and_runtime_unchanged() -> None:
    fixture = _load_fixture()

    assert fixture["approved_lima_runtime_files_changed"] == []
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["lima_public_api_changed"] is False
    assert fixture["lima_runtime_behavior_added_by_v1_g56"] is False
    assert fixture["approved_lima_docs_tests_fixtures_changed"] == [
        "docs/V1_G56_CONSUMER_FAKE_EXECUTOR_PROVIDER_SDK_NETWORK_EGRESS_SMOKE.md",
        "docs/V1_G56_CONSUMER_FAKE_EXECUTOR_PROVIDER_SDK_NETWORK_EGRESS_SMOKE_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g56_consumer_fake_executor_provider_sdk_network_egress_smoke.json",
        "tests/test_v1_g56_consumer_fake_executor_provider_sdk_network_egress_smoke.py",
    ]
    for relative_path in fixture["approved_lima_docs_tests_fixtures_changed"]:
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g56_consumer_file_scope_and_commits_are_recorded() -> None:
    fixture = _load_fixture()

    assert fixture["consumer_repositories"]["sparkbot"] == {
        "repository": "sparkpit-labs/Sparkbot",
        "local_path": "../Sparkbot-public",
        "branch": "v1-g56-consumer-fake-executor-provider-sdk-network-egress-smoke",
        "commit": "ae5cc9c563ea2b0f08c91af03164a78b4b20e3e2",
        "push_status": "blocked_github_403_current_credential",
        "approved_files_changed": [
            "tests/test_sparkbot_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.py",
            "tests/fixtures/sparkbot_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.json",
        ],
        "fixture_ref": (
            "tests/fixtures/"
            "sparkbot_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.json"
        ),
        "test_ref": (
            "tests/test_sparkbot_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.py"
        ),
        "focused_v1_g56_validation": {
            "command": (
                "python -B -m pytest -q "
                "tests\\test_sparkbot_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.py "
                "-p no:cacheprovider"
            ),
            "passed": True,
            "tests_passed": 8,
        },
        "remote_push_validation": {
            "command": (
                "git push -u origin "
                "v1-g56-consumer-fake-executor-provider-sdk-network-egress-smoke"
            ),
            "passed": False,
            "blocked_reason": "github_403_permission_denied_to_current_credential",
        },
    }
    assert fixture["consumer_repositories"]["arc_bot_shell"] == {
        "repository": "armpit-symphony/Arc-Bot-shell",
        "local_path": "../Arc-Bot-shell",
        "branch": "v1-g56-consumer-fake-executor-provider-sdk-network-egress-smoke",
        "commit": "ec06e7670f18eeae192fc0f995b6ffd07481d8c9",
        "push_status": "pushed_to_origin",
        "approved_files_changed": [
            "tests/test_arc_bot_shell_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.py",
            "tests/fixtures/arc_bot_shell_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.json",
        ],
        "fixture_ref": (
            "tests/fixtures/"
            "arc_bot_shell_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.json"
        ),
        "test_ref": (
            "tests/test_arc_bot_shell_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.py"
        ),
        "focused_v1_g56_validation": {
            "command": (
                "python -B -m pytest -q "
                "tests\\test_arc_bot_shell_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.py "
                "-p no:cacheprovider"
            ),
            "passed": True,
            "tests_passed": 8,
        },
        "focused_v1_g52_validation": {
            "command": (
                "python -B -m pytest -q "
                "tests\\test_arc_bot_shell_lima_v1_g52_fake_executor_provider_invocation_smoke.py "
                "-p no:cacheprovider"
            ),
            "passed": True,
            "tests_passed": 8,
        },
    }


def test_v1_g56_consumer_files_exist_and_match_fixture_scope() -> None:
    fixture = _load_fixture()

    for consumer_key, consumer in fixture["consumer_repositories"].items():
        consumer_root = (REPO_ROOT / consumer["local_path"]).resolve()
        assert consumer_root.exists(), consumer_key
        consumer_fixture = _load_consumer_fixture(consumer_key)

        assert consumer_fixture["api_status"] == "CANDIDATE_ONLY"
        assert consumer_fixture["proof_gap_id"] == "V1-G56"
        assert consumer_fixture["proof_branch"] == consumer["branch"]
        assert consumer_fixture["approved_file_scope"] == consumer[
            "approved_files_changed"
        ]
        for relative_path in consumer["approved_files_changed"]:
            assert (consumer_root / relative_path).exists(), relative_path


def test_v1_g56_consumers_import_only_approved_public_symbols() -> None:
    fixture = _load_fixture()

    expected = [
        "V1RealProviderSdkNetworkEgressError",
        "execute_v1_real_provider_sdk_network_egress",
    ]
    assert fixture["public_lima_harness_symbols_imported_by_consumers"] == expected
    assert _load_consumer_fixture("sparkbot")["expected_lima_public_symbols"] == expected
    assert _load_consumer_fixture("arc_bot_shell")[
        "expected_lima_public_symbols"
    ] == expected


def test_v1_g56_consumer_fake_executor_records_are_sanitized() -> None:
    sparkbot = _load_consumer_fixture("sparkbot")
    arc = _load_consumer_fixture("arc_bot_shell")

    assert sparkbot["expected_execution_record"]["record_type"] == (
        "v1_real_provider_sdk_network_egress"
    )
    assert sparkbot["expected_execution_record"]["schema_version"] == (
        "v1-g55-candidate"
    )
    assert arc["expected_execution_record"]["record_type"] == (
        "v1_real_provider_sdk_network_egress"
    )
    assert arc["expected_execution_record"]["schema_version"] == "v1-g55-candidate"

    for consumer_fixture in (sparkbot, arc):
        assert (
            consumer_fixture["v1_g48_g50_g51_g53_g54_g55_authority_metadata_built"]
            is True
        )
        assert (
            consumer_fixture[
                "fake_in_process_provider_sdk_network_executor_injected"
            ]
            is True
        )
        assert (
            consumer_fixture[
                "fake_in_process_provider_sdk_network_executor_invoked"
            ]
            is True
        )
        assert consumer_fixture["actual_external_provider_invoked"] is False
        assert consumer_fixture["network_calls_performed"] is False
        assert consumer_fixture["credential_value_accessed"] is False
        assert consumer_fixture["product_ready"] is False


def test_v1_g56_forbidden_boundaries_remain_false() -> None:
    fixture = _load_fixture()

    for key in (
        "consumer_production_runtime_source_files_changed",
        "consumer_runtime_calls_added",
        "consumer_integration_added",
        "shell_runtime_wiring_added",
        "lima_runtime_behavior_added_by_v1_g56",
        "lima_public_api_expanded",
        "actual_external_provider_invoked",
        "live_provider_credentials_used",
        "built_in_provider_sdk_client_added",
        "built_in_provider_sdk_client_used",
        "sdk_dependency_added",
        "vendor_provider_sdk_import_added",
        "direct_provider_sdk_added",
        "direct_provider_sdk_used",
        "direct_network_code_added",
        "direct_network_code_used",
        "provider_endpoint_resolution_added",
        "provider_endpoint_resolution_performed",
        "network_call_performed_by_lima",
        "direct_provider_egress_performed_by_lima",
        "provider_readiness_network_check_added",
        "token_guardian_live_routing_added",
        "ambient_environment_secret_lookup_added",
        "secret_lookup_added",
        "credential_access_added",
        "credential_value_access_added",
        "credential_value_accessed",
        "provider_token_or_api_key_access_added",
        "provider_token_or_api_key_accessed",
        "provider_configuration_changes_added",
        "fallback_execution_added",
        "fallback_executed",
        "tool_execution_added",
        "action_execution_added",
        "connector_browser_network_file_device_robotics_physical_world_behavior_added",
        "scheduled_task_execution_added",
        "external_send_added",
        "raw_prompt_persisted",
        "raw_model_response_persisted",
        "raw_customer_data_persisted",
        "raw_secret_or_credential_persisted",
        "provider_token_or_api_key_persisted",
        "raw_diff_or_patch_persisted",
        "raw_file_content_persisted",
        "raw_sensitive_content_persisted",
        "product_ready",
    ):
        assert fixture[key] is False


def test_v1_g56_required_confirmations_and_future_gates_are_locked() -> None:
    fixture = _load_fixture()

    assert fixture["future_required_gates"] == [
        "built_in_provider_sdk_client_approval_request",
        "provider_credential_value_access_approval_request",
        "lima_owned_provider_network_egress_approval_request",
        "fallback_execution_approval_request",
        "connector_browser_network_authority_approval_request",
        "consumer_production_runtime_integration_approval_request",
        "physical_world_authority_approval_request",
        "product_readiness_approval_request",
    ]
    assert fixture["blocked_future_authorities"] == {
        "built_in_provider_sdk_client_approved": False,
        "provider_secret_lookup_approved": False,
        "provider_credential_value_access_approved": False,
        "lima_owned_provider_network_egress_approved": False,
        "fallback_execution_approved": False,
        "connector_browser_network_authority_approved": False,
        "consumer_production_runtime_integration_approved": False,
        "physical_world_authority_approved": False,
        "product_readiness_approved": False,
    }
    assert all(fixture["required_confirmations"].values())


def test_v1_g56_accepted_evidence_refs_exist() -> None:
    fixture = _load_fixture()

    for relative_path in fixture["accepted_evidence_refs"]:
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g56_validation_results_are_recorded() -> None:
    fixture = _load_fixture()
    consumer_validation = fixture["consumer_validation_results"]
    lima_validation = fixture["lima_validation_results"]

    assert consumer_validation["sparkbot_focused_v1_g56"]["passed"] is True
    assert consumer_validation["sparkbot_focused_v1_g56"]["tests_passed"] == 8
    assert consumer_validation["sparkbot_public_branch_push"]["passed"] is False
    assert (
        consumer_validation["sparkbot_public_branch_push"]["blocked_reason"]
        == "github_403_permission_denied_to_current_credential"
    )
    assert consumer_validation["sparkbot_reference_focused_v1_g52"]["passed"] is True
    assert (
        consumer_validation["sparkbot_reference_focused_v1_g52"]["tests_passed"] == 8
    )
    assert (
        consumer_validation["sparkbot_reference_focused_v1_g52"]["source_checkout"]
        == "../Sparkbot"
    )
    assert consumer_validation["arc_bot_shell_focused_v1_g56"]["passed"] is True
    assert consumer_validation["arc_bot_shell_focused_v1_g56"]["tests_passed"] == 8
    assert consumer_validation["arc_bot_shell_focused_v1_g52"]["passed"] is True
    assert consumer_validation["arc_bot_shell_focused_v1_g52"]["tests_passed"] == 8

    assert lima_validation["focused_v1_g56_validation"]["passed"] is True
    assert lima_validation["focused_v1_g56_validation"]["tests_passed"] == 12
    assert (
        lima_validation[
            "focused_v1_g56_g55_g54_g53_g52_g51_g50_g48_g22_validation"
        ]["passed"]
        is True
    )
    assert (
        lima_validation[
            "focused_v1_g56_g55_g54_g53_g52_g51_g50_g48_g22_validation"
        ]["tests_passed"]
        == 383
    )
    assert lima_validation["compileall_lima"] == {
        "command": "python -B -m compileall lima",
        "passed": True,
    }
    assert lima_validation["full_lima_suite"]["passed"] is True
    assert lima_validation["full_lima_suite"]["tests_passed"] == 4931


def test_v1_g56_fixture_and_docs_do_not_include_sensitive_markers() -> None:
    fixture = _load_fixture()
    output = json.dumps(fixture, sort_keys=True)
    output += (
        REPO_ROOT
        / "docs"
        / "V1_G56_CONSUMER_FAKE_EXECUTOR_PROVIDER_SDK_NETWORK_EGRESS_SMOKE.md"
    ).read_text(encoding="utf-8")
    output += (
        REPO_ROOT
        / "docs"
        / "V1_G56_CONSUMER_FAKE_EXECUTOR_PROVIDER_SDK_NETWORK_EGRESS_SMOKE_CLOSEOUT.md"
    ).read_text(encoding="utf-8")

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


def test_v1_g56_docs_contain_boundary_language() -> None:
    implementation_text = (
        REPO_ROOT
        / "docs"
        / "V1_G56_CONSUMER_FAKE_EXECUTOR_PROVIDER_SDK_NETWORK_EGRESS_SMOKE.md"
    ).read_text(encoding="utf-8")
    closeout_text = (
        REPO_ROOT
        / "docs"
        / "V1_G56_CONSUMER_FAKE_EXECUTOR_PROVIDER_SDK_NETWORK_EGRESS_SMOKE_CLOSEOUT.md"
    ).read_text(encoding="utf-8")

    assert "fake in-process provider SDK/network executor only" in implementation_text
    assert "No `lima/` runtime file" in implementation_text
    assert "Actual external provider invoked: no" in implementation_text
    assert "Direct provider egress performed by LIMA: no" in implementation_text
    assert "Public Sparkbot branch pushed: no, blocked by GitHub 403" in implementation_text
    assert "V1-G56 is complete" in closeout_text
    assert "Product readiness claimed: no" in closeout_text
