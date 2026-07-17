"""Tests for the approved V1-G34 live consumer import/call slice."""

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
    / "v1_g34_live_consumer_import_call.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _records() -> list[dict[str, Any]]:
    records = _load_fixture()["consumer_live_import_call_records"]
    assert isinstance(records, list)
    return records


def test_v1_g34_fixture_records_approved_scope_and_candidate_status() -> None:
    fixture = _load_fixture()

    assert fixture["packet_set_id"] == "v1_g34_live_consumer_import_call"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g34-live-consumer-import-call"
    assert fixture["operator_decision"] == "Approve-V1-G34"
    assert fixture["approved_scope"] == "live_consumer_import_call_test_slice"
    assert fixture["live_consumer_import_call_test_added"] is True
    assert fixture["approved_consumer_test_fixture_files_added"] is True
    assert fixture["consumer_test_files_created"] is True
    assert fixture["unapproved_consumer_repo_mutation_added"] is False
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["product_ready"] is False


def test_v1_g34_lima_file_scope_is_docs_tests_fixtures_only() -> None:
    fixture = _load_fixture()

    assert fixture["approved_lima_files_changed"] == [
        "docs/V1_G34_LIVE_CONSUMER_IMPORT_CALL.md",
        "docs/V1_G34_LIVE_CONSUMER_IMPORT_CALL_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g34_live_consumer_import_call.json",
        "tests/test_v1_g34_live_consumer_import_call.py",
    ]
    assert all(not path.startswith("lima/") for path in fixture["approved_lima_files_changed"])


def test_v1_g34_consumer_file_scope_is_exact() -> None:
    fixture = _load_fixture()

    assert fixture["approved_consumer_files_changed"] == {
        "sparkbot": [
            "tests/fixtures/sparkbot_lima_v1_g34_live_consumer_import_call.json",
            "tests/test_sparkbot_lima_v1_g34_live_consumer_import_call.py",
        ],
        "arc_bot": [
            "tests/fixtures/arc_bot_shell_lima_v1_g34_live_consumer_import_call.json",
            "tests/test_arc_bot_shell_lima_v1_g34_live_consumer_import_call.py",
        ],
    }

    for record in _records():
        assert record["approved_consumer_files_changed"] == (
            fixture["approved_consumer_files_changed"][record["consumer_packet_family"]]
        )
        assert record["consumer_runtime_source_files_changed"] is False
        assert record["consumer_runtime_modules_imported"] is False


def test_v1_g34_contains_exactly_first_two_consumer_live_call_records() -> None:
    records = _records()

    assert [record["consumer_packet_family"] for record in records] == [
        "sparkbot",
        "arc_bot",
    ]
    assert [record["consumer_name"] for record in records] == [
        "Sparkbot",
        "Arc-Bot-shell",
    ]


def test_v1_g34_records_saved_consumer_commits_and_source_refs() -> None:
    expected = {
        "sparkbot": (
            "cee164655e1603f5e68b6df9773dc5b08dd27ca0",
            "ebef6ae816f9ae4e43cc1ac57c13ce04a20a04f1",
            "consumer-repository-test-edit:v1-g32:sparkbot:001",
            "consumer-fake-runtime-import-call-smoke:v1-g33:sparkbot:001",
        ),
        "arc_bot": (
            "61404a3bf7d95a45138ebd97992bcebe61651d79",
            "2dfb3673ffbd5c044e586a9fe2f714d941318be8",
            "consumer-repository-test-edit:v1-g32:arc-bot-shell:001",
            "consumer-fake-runtime-import-call-smoke:v1-g33:arc-bot-shell:001",
        ),
    }

    for record in _records():
        commit_sha, source_sha, edit_ref, smoke_ref = expected[
            record["consumer_packet_family"]
        ]
        assert record["consumer_branch"] == "v1-g34-live-consumer-import-call"
        assert record["consumer_commit_sha"] == commit_sha
        assert len(record["consumer_commit_sha"]) == 40
        assert record["source_g32_consumer_commit_sha"] == source_sha
        assert len(record["source_g32_consumer_commit_sha"]) == 40
        assert record["source_consumer_test_edit_record_ref"] == edit_ref
        assert record["source_smoke_record_ref"] == smoke_ref


def test_v1_g34_approved_adapter_validator_calls_are_exact() -> None:
    expected = [
        "lima.adapters.validate_v1_consumer_integration_compatibility_freeze",
        "lima.adapters.validate_v1_consumer_integration_proof_to_import_dry_run",
    ]

    fixture = _load_fixture()
    assert fixture["approved_adapter_validator_symbols"] == expected
    assert fixture["approved_adapter_validator_calls_executed"] is True
    assert fixture["approved_adapter_validator_calls_limited_to_consumer_tests"] is True
    assert fixture["unapproved_adapter_symbol_calls_executed"] is False

    for record in _records():
        assert record["approved_adapter_validator_symbols"] == expected
        assert record["approved_adapter_validator_calls_executed"] is True
        assert record["approved_adapter_validator_calls_limited_to_consumer_tests"] is True
        assert record["unapproved_adapter_symbol_calls_executed"] is False
        assert record["expected_validator_record_types"] == [
            "v1_consumer_integration_compatibility_freeze",
            "v1_consumer_integration_proof_to_import_dry_run",
        ]


def test_v1_g34_consumer_test_results_are_recorded() -> None:
    for record in _records():
        assert record["focused_consumer_test_result"] == "9 passed"
        assert record["focused_g32_consumer_test_result"] == "8 passed"
        assert record["focused_g27_import_smoke_result"] == "7 passed"
        assert record["sanitized_metadata_only"] is True


def test_v1_g34_runtime_and_external_boundaries_remain_false() -> None:
    fixture = _load_fixture()

    for key in (
        "consumer_runtime_source_files_changed",
        "consumer_runtime_modules_imported",
        "shell_runtime_wiring_added",
        "fake_call_envelopes_executed",
        "consumer_integration_added",
        "provider_model_calls_added",
        "model_request_dispatch_added",
        "fallback_execution_added",
        "secret_lookup_added",
        "credential_access_added",
        "tool_execution_outside_local_tests_added",
        "action_execution_added",
        "connector_browser_network_file_device_robotics_physical_world_behavior_added",
        "raw_sensitive_content_persisted_in_lima_evidence",
    ):
        assert fixture[key] is False

    for record in _records():
        for key in (
            "consumer_runtime_modules_imported",
            "consumer_runtime_source_files_changed",
            "shell_runtime_wiring_added",
            "fake_call_envelopes_executed",
            "provider_model_calls_added",
            "model_request_dispatch_added",
            "fallback_execution_added",
            "secret_lookup_added",
            "credential_access_added",
            "tool_execution_outside_local_tests_added",
            "action_execution_added",
            "connector_browser_network_file_device_robotics_physical_world_behavior_added",
            "raw_sensitive_content_persisted_in_lima_evidence",
        ):
            assert record[key] is False
        assert record["proof_not_product_readiness"] is True
        assert record["product_ready"] is False


def test_v1_g34_links_required_prior_evidence() -> None:
    fixture = _load_fixture()

    for relative_path in fixture["accepted_evidence_refs"]:
        assert (REPO_ROOT / relative_path).exists()

    for record in _records():
        assert record["g27_import_smoke_ref"] in record["evidence_refs"]
        assert "runtime-export-cleanup:v1-g28" in record["evidence_refs"]
        assert record["planning_record_ref"] in record["evidence_refs"]
        assert record["source_fake_runtime_evidence_record_ref"] in record["evidence_refs"]
        assert record["source_preview_record_ref"] in record["evidence_refs"]
        assert record["source_consumer_test_edit_record_ref"] in record["evidence_refs"]
        assert record["source_smoke_record_ref"] in record["evidence_refs"]


def test_v1_g34_rollback_metadata_is_local_and_reversible() -> None:
    expected_lima_files = _load_fixture()["approved_lima_files_changed"]

    for record in _records():
        rollback = record["rollback_metadata"]

        assert rollback["rollback_ref"].startswith("rollback:v1-g34:")
        assert rollback["rollback_lima_file_refs"] == expected_lima_files
        assert rollback["rollback_consumer_file_refs"] == record[
            "approved_consumer_files_changed"
        ]
        assert rollback["runtime_source_repair_required"] is False
        assert rollback["external_service_changes_required"] is False


def test_v1_g34_required_confirmations_are_true() -> None:
    for record in _records():
        confirmations = record["required_confirmations"]

        assert confirmations["no_lima_runtime_file_change_confirmation"] is True
        assert confirmations["no_consumer_runtime_source_change_confirmation"] is True
        assert confirmations["no_consumer_runtime_module_import_confirmation"] is True
        assert confirmations["no_shell_wiring_confirmation"] is True
        assert confirmations["only_approved_adapter_validator_calls_confirmation"] is True
        assert (
            confirmations[
                "no_provider_model_secret_credential_connector_browser_network_physical_world_confirmation"
            ]
            is True
        )
        assert (
            confirmations["no_raw_sensitive_content_in_lima_evidence_confirmation"]
            is True
        )
        assert confirmations["proof_not_product_readiness_confirmation"] is True


def test_v1_g34_output_does_not_include_patch_bodies_or_sensitive_markers() -> None:
    output = json.dumps(_load_fixture(), sort_keys=True)

    for forbidden in (
        "diff --git",
        "@@",
        "BEGIN PATCH",
        "raw prompt value",
        "raw customer data value",
        "provider token value",
        "api key value",
        "raw-secret-123",
        "def test_",
        "import lima",
    ):
        assert forbidden not in output


def test_v1_g34_docs_contain_boundary_language() -> None:
    implementation_text = (
        REPO_ROOT / "docs" / "V1_G34_LIVE_CONSUMER_IMPORT_CALL.md"
    ).read_text(encoding="utf-8")
    closeout_text = (
        REPO_ROOT / "docs" / "V1_G34_LIVE_CONSUMER_IMPORT_CALL_CLOSEOUT.md"
    ).read_text(encoding="utf-8")

    assert "No `lima/` runtime file" in implementation_text
    assert "Approved adapter validator calls executed: yes" in implementation_text
    assert "No Sparkbot or Arc-Bot-shell runtime/source file" in implementation_text
    assert "No product-readiness or production-readiness claim" in closeout_text
    assert "V1-G34 is complete" in closeout_text
