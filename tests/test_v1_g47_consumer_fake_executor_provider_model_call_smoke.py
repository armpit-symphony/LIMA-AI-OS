"""Tests for the approved V1-G47 consumer fake-executor smoke slice."""

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
    / "v1_g47_consumer_fake_executor_provider_model_call_smoke.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _load_consumer_fixture(consumer_key: str) -> dict[str, Any]:
    consumer = _load_fixture()["consumer_repositories"][consumer_key]
    consumer_root = (REPO_ROOT / consumer["local_path"]).resolve()
    fixture = json.loads((consumer_root / consumer["fixture_ref"]).read_text())
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g47_fixture_records_approved_scope_and_status() -> None:
    fixture = _load_fixture()

    assert fixture["packet_set_id"] == (
        "v1_g47_consumer_fake_executor_provider_model_call_smoke"
    )
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == (
        "v1-g47-consumer-fake-executor-provider-model-call-smoke"
    )
    assert fixture["operator_decision"] == "Approve-V1-G47"
    assert fixture["approved_scope"] == (
        "consumer_fake_executor_provider_model_call_smoke_slice"
    )
    assert fixture["consumer_fake_executor_provider_model_call_smoke_approved"] is True
    assert fixture["consumer_fake_executor_provider_model_call_smoke_added"] is True
    assert fixture["product_ready"] is False


def test_v1_g47_lima_file_scope_is_exact_and_runtime_unchanged() -> None:
    fixture = _load_fixture()

    assert fixture["approved_lima_runtime_files_changed"] == []
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["approved_lima_docs_tests_fixtures_changed"] == [
        "docs/V1_G47_CONSUMER_FAKE_EXECUTOR_PROVIDER_MODEL_CALL_SMOKE.md",
        "docs/V1_G47_CONSUMER_FAKE_EXECUTOR_PROVIDER_MODEL_CALL_SMOKE_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g47_consumer_fake_executor_provider_model_call_smoke.json",
        "tests/test_v1_g47_consumer_fake_executor_provider_model_call_smoke.py",
    ]
    for relative_path in fixture["approved_lima_docs_tests_fixtures_changed"]:
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g47_consumer_file_scope_and_commits_are_recorded() -> None:
    fixture = _load_fixture()

    assert fixture["consumer_repositories"]["sparkbot"] == {
        "repository": "sparkpit-labs/Sparkbot",
        "local_path": "../Sparkbot",
        "branch": "v1-g47-consumer-fake-executor-provider-model-call-smoke",
        "commit": "83918032f52f069d16796865066ea78dfd182d58",
        "approved_files_changed": [
            "tests/fixtures/sparkbot_lima_v1_g47_fake_executor_provider_model_call_smoke.json",
            "tests/test_sparkbot_lima_v1_g47_fake_executor_provider_model_call_smoke.py",
        ],
        "fixture_ref": (
            "tests/fixtures/"
            "sparkbot_lima_v1_g47_fake_executor_provider_model_call_smoke.json"
        ),
        "test_ref": (
            "tests/test_sparkbot_lima_v1_g47_fake_executor_provider_model_call_smoke.py"
        ),
        "focused_v1_g47_validation": {
            "command": (
                "python -B -m pytest -q "
                "tests\\test_sparkbot_lima_v1_g47_fake_executor_provider_model_call_smoke.py "
                "-p no:cacheprovider"
            ),
            "passed": True,
            "tests_passed": 8,
        },
        "focused_v1_g42_validation": {
            "command": (
                "python -B -m pytest -q "
                "tests\\test_sparkbot_lima_v1_g42_shell_wiring_implementation.py "
                "-p no:cacheprovider"
            ),
            "passed": True,
            "tests_passed": 9,
        },
    }
    assert fixture["consumer_repositories"]["arc_bot_shell"] == {
        "repository": "armpit-symphony/Arc-Bot-shell",
        "local_path": "../Arc-Bot-shell",
        "branch": "v1-g47-consumer-fake-executor-provider-model-call-smoke",
        "commit": "3edf31f2ee3143756db8d9410009cd87e98bba71",
        "approved_files_changed": [
            "tests/fixtures/arc_bot_shell_lima_v1_g47_fake_executor_provider_model_call_smoke.json",
            "tests/test_arc_bot_shell_lima_v1_g47_fake_executor_provider_model_call_smoke.py",
        ],
        "fixture_ref": (
            "tests/fixtures/"
            "arc_bot_shell_lima_v1_g47_fake_executor_provider_model_call_smoke.json"
        ),
        "test_ref": (
            "tests/test_arc_bot_shell_lima_v1_g47_fake_executor_provider_model_call_smoke.py"
        ),
        "focused_v1_g47_validation": {
            "command": (
                "python -B -m pytest -q "
                "tests\\test_arc_bot_shell_lima_v1_g47_fake_executor_provider_model_call_smoke.py "
                "-p no:cacheprovider"
            ),
            "passed": True,
            "tests_passed": 8,
        },
        "focused_v1_g42_validation": {
            "command": (
                "python -B -m pytest -q "
                "tests\\test_arc_bot_shell_lima_v1_g42_shell_wiring_implementation.py "
                "-p no:cacheprovider"
            ),
            "passed": True,
            "tests_passed": 9,
        },
    }


def test_v1_g47_consumer_files_exist_and_match_fixture_scope() -> None:
    fixture = _load_fixture()

    for consumer_key, consumer in fixture["consumer_repositories"].items():
        consumer_root = (REPO_ROOT / consumer["local_path"]).resolve()
        assert consumer_root.exists(), consumer_key
        consumer_fixture = _load_consumer_fixture(consumer_key)

        assert consumer_fixture["api_status"] == "CANDIDATE_ONLY"
        assert consumer_fixture["proof_gap_id"] == "V1-G47"
        assert consumer_fixture["proof_branch"] == consumer["branch"]
        assert consumer_fixture["approved_file_scope"] == consumer[
            "approved_files_changed"
        ]
        for relative_path in consumer["approved_files_changed"]:
            assert (consumer_root / relative_path).exists(), relative_path


def test_v1_g47_consumers_import_only_approved_public_symbols() -> None:
    fixture = _load_fixture()

    expected = [
        "V1LiveProviderModelCallExecutionError",
        "execute_v1_live_provider_model_call",
        "validate_v1_live_provider_model_call_authority",
    ]
    assert fixture["public_lima_harness_symbols_imported_by_consumers"] == expected
    assert _load_consumer_fixture("sparkbot")["expected_lima_public_symbols"] == expected
    assert _load_consumer_fixture("arc_bot_shell")[
        "expected_lima_public_symbols"
    ] == expected


def test_v1_g47_consumer_fake_executor_records_are_sanitized() -> None:
    sparkbot = _load_consumer_fixture("sparkbot")
    arc = _load_consumer_fixture("arc_bot_shell")

    assert sparkbot["expected_execution_record"]["record_type"] == (
        "v1_live_provider_model_call_execution"
    )
    assert sparkbot["expected_execution_record"]["schema_version"] == "v1-g46-candidate"
    assert arc["expected_execution_record"]["record_type"] == (
        "v1_live_provider_model_call_execution"
    )
    assert arc["expected_execution_record"]["schema_version"] == "v1-g46-candidate"

    for consumer_fixture in (sparkbot, arc):
        assert consumer_fixture["fake_provider_executor_injected"] is True
        assert consumer_fixture["fake_provider_executor_invoked"] is True
        assert consumer_fixture["real_provider_executor_invoked"] is False
        assert consumer_fixture["network_calls_performed"] is False
        assert consumer_fixture["credential_value_accessed"] is False
        assert consumer_fixture["product_ready"] is False


def test_v1_g47_forbidden_boundaries_remain_false() -> None:
    fixture = _load_fixture()

    for key in (
        "consumer_production_runtime_source_files_changed",
        "consumer_runtime_calls_added",
        "consumer_integration_added",
        "shell_runtime_wiring_added",
        "lima_public_api_expanded",
        "lima_runtime_behavior_added_by_v1_g47",
        "real_provider_executor_invocation_added",
        "real_provider_executor_invoked",
        "live_provider_model_call_execution_added_by_v1_g47",
        "live_provider_credentials_used",
        "direct_provider_sdk_added",
        "direct_provider_sdk_used",
        "direct_network_code_added",
        "direct_network_code_used",
        "network_call_performed",
        "provider_readiness_network_check_added",
        "token_guardian_live_routing_added",
        "ambient_environment_secret_lookup_added",
        "secret_lookup_added",
        "credential_access_added",
        "credential_value_access_added",
        "credential_value_accessed",
        "fallback_execution_added",
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


def test_v1_g47_required_confirmations_and_future_gates_are_locked() -> None:
    fixture = _load_fixture()

    assert fixture["future_required_gates"] == [
        "provider_credential_network_hardening_approval_request",
        "real_provider_executor_approval_request",
        "connector_browser_network_authority_approval_request",
        "physical_world_authority_approval_request",
        "product_readiness_approval_request",
    ]
    assert all(fixture["required_confirmations"].values())
    assert fixture["blocked_future_authorities"] == {
        "real_provider_executor_approved": False,
        "provider_secret_lookup_approved": False,
        "provider_network_egress_approved": False,
        "built_in_provider_sdk_approved": False,
        "fallback_execution_approved": False,
        "connector_browser_network_authority_approved": False,
        "physical_world_authority_approved": False,
        "product_readiness_approved": False,
    }


def test_v1_g47_optional_consumer_full_suite_note_is_bounded() -> None:
    audit = _load_fixture()["optional_consumer_full_suite_self_audit"]

    assert audit["attempted"] is True
    assert audit["required_by_v1_g47_approval_request"] is False
    assert audit["sparkbot_v1_g47_deselected_result"] == "same_failure_reproduced"
    assert audit["arc_bot_shell_v1_g47_deselected_result"] == "same_failure_reproduced"
    assert audit["older_consumer_tests_changed"] is False
    assert audit["not_treated_as_v1_g47_required_validation_failure"] is True


def test_v1_g47_lima_validation_results_are_recorded() -> None:
    validation = _load_fixture()["lima_validation_results"]

    assert validation["focused_v1_g47_g46_g22_validation"]["passed"] is True
    assert validation["focused_v1_g47_g46_g22_validation"]["tests_passed"] == 77
    assert validation["compileall_lima"] == {
        "command": "python -m compileall lima",
        "passed": True,
    }
    assert validation["full_lima_suite"]["passed"] is True
    assert validation["full_lima_suite"]["tests_passed"] == 4291


def test_v1_g47_fixture_and_docs_do_not_include_sensitive_markers() -> None:
    fixture = _load_fixture()
    output = json.dumps(fixture, sort_keys=True)
    output += (
        REPO_ROOT / "docs" / "V1_G47_CONSUMER_FAKE_EXECUTOR_PROVIDER_MODEL_CALL_SMOKE.md"
    ).read_text(encoding="utf-8")
    output += (
        REPO_ROOT
        / "docs"
        / "V1_G47_CONSUMER_FAKE_EXECUTOR_PROVIDER_MODEL_CALL_SMOKE_CLOSEOUT.md"
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
