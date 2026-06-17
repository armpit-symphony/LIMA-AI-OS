"""Tests for the approved V1-G33 consumer fake-runtime smoke slice."""

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
    / "v1_g33_consumer_fake_runtime_import_call_smoke.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _records() -> list[dict[str, Any]]:
    records = _load_fixture()["consumer_smoke_records"]
    assert isinstance(records, list)
    return records


def test_v1_g33_fixture_records_approved_scope_and_candidate_status() -> None:
    fixture = _load_fixture()

    assert fixture["packet_set_id"] == "v1_g33_consumer_fake_runtime_import_call_smoke"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g33-consumer-fake-runtime-import-call-smoke"
    assert fixture["operator_decision"] == "Approve-V1-G33"
    assert fixture["approved_scope"] == (
        "consumer_fake_runtime_import_call_smoke_evidence_slice"
    )
    assert fixture["consumer_fake_runtime_import_call_smoke_added"] is True
    assert fixture["metadata_only"] is True
    assert fixture["fake_runtime_only"] is True
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["consumer_repo_mutation_added"] is False
    assert fixture["consumer_test_files_created"] is False
    assert fixture["product_ready"] is False


def test_v1_g33_file_scope_is_exact_lima_docs_tests_fixtures_only() -> None:
    fixture = _load_fixture()

    assert fixture["approved_lima_files_changed"] == [
        "docs/V1_G33_CONSUMER_FAKE_RUNTIME_IMPORT_CALL_SMOKE.md",
        "docs/V1_G33_CONSUMER_FAKE_RUNTIME_IMPORT_CALL_SMOKE_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g33_consumer_fake_runtime_import_call_smoke.json",
        "tests/test_v1_g33_consumer_fake_runtime_import_call_smoke.py",
    ]
    assert all(not path.startswith("lima/") for path in fixture["approved_lima_files_changed"])
    assert fixture["approved_consumer_files_changed"] == []
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["arc_bot_shell_files_changed"] is False


def test_v1_g33_contains_exactly_first_two_consumer_smoke_records() -> None:
    records = _records()

    assert [record["consumer_packet_family"] for record in records] == [
        "sparkbot",
        "arc_bot",
    ]
    assert [record["consumer_name"] for record in records] == [
        "Sparkbot",
        "Arc-Bot-shell",
    ]


def test_v1_g33_records_saved_g32_consumer_commits_and_refs() -> None:
    expected = {
        "sparkbot": (
            "ebef6ae816f9ae4e43cc1ac57c13ce04a20a04f1",
            "consumer-repository-test-edit:v1-g32:sparkbot:001",
            "fake-runtime-consumer-call-evidence:v1-g30:sparkbot:001",
            "fake-runtime-consumer-repo-test-preview:v1-g31:sparkbot:001",
            "live-consumer-import-call-plan:v1-g29:sparkbot:001",
        ),
        "arc_bot": (
            "2dfb3673ffbd5c044e586a9fe2f714d941318be8",
            "consumer-repository-test-edit:v1-g32:arc-bot-shell:001",
            "fake-runtime-consumer-call-evidence:v1-g30:arc-bot-shell:001",
            "fake-runtime-consumer-repo-test-preview:v1-g31:arc-bot-shell:001",
            "live-consumer-import-call-plan:v1-g29:arc-bot-shell:001",
        ),
    }

    for record in _records():
        commit_sha, edit_ref, fake_runtime_ref, preview_ref, planning_ref = expected[
            record["consumer_packet_family"]
        ]
        assert record["consumer_test_branch"] == "v1-g32-consumer-repository-test-edit"
        assert record["consumer_test_commit_sha"] == commit_sha
        assert len(record["consumer_test_commit_sha"]) == 40
        assert record["source_consumer_test_edit_record_ref"] == edit_ref
        assert record["source_fake_runtime_evidence_record_ref"] == fake_runtime_ref
        assert record["source_preview_record_ref"] == preview_ref
        assert record["planning_record_ref"] == planning_ref


def test_v1_g33_smoke_records_are_metadata_only() -> None:
    for record in _records():
        smoke = record["smoke_import_call_metadata"]

        assert smoke["metadata_only"] is True
        assert smoke["fake_runtime_only"] is True
        assert smoke["metadata_payload_ref"].startswith("fixture://runtime_extraction/")
        assert smoke["consumer_runtime_invoked"] is False
        assert smoke["live_import_call_invoked"] is False
        assert smoke["external_services_required"] is False
        assert smoke["network_required"] is False
        assert smoke["secrets_required"] is False
        assert smoke["provider_model_required"] is False


def test_v1_g33_adapter_symbols_are_exact_and_not_called() -> None:
    expected = [
        "lima.adapters.validate_v1_consumer_integration_compatibility_freeze",
        "lima.adapters.validate_v1_consumer_integration_proof_to_import_dry_run",
    ]

    assert _load_fixture()["approved_candidate_adapter_symbols"] == expected
    for record in _records():
        smoke = record["smoke_import_call_metadata"]

        assert smoke["adapter_symbol_refs"] == expected
        assert smoke["call_shape_refs"] == [
            "validate_v1_consumer_integration_compatibility_freeze(metadata)",
            "validate_v1_consumer_integration_proof_to_import_dry_run(metadata)",
        ]
        assert smoke["planned_adapter_symbols_called"] is False
        assert smoke["adapter_symbol_calls_executed"] is False
        assert record["consumer_repo_edits_allowed"] is False
        assert record["consumer_test_file_creation_allowed"] is False


def test_v1_g33_fake_call_envelopes_are_not_executed() -> None:
    fixture = _load_fixture()

    assert fixture["fake_call_envelopes_executed"] is False
    for record in _records():
        smoke = record["smoke_import_call_metadata"]

        assert smoke["fake_call_envelope_executed"] is False
        assert record["consumer_runtime_calls_added"] is False
        assert record["live_consumer_import_calls_added"] is False


def test_v1_g33_existing_consumer_test_results_are_linked() -> None:
    expected_refs = {
        "sparkbot": [
            "tests/fixtures/sparkbot_lima_v1_g31_fake_runtime_consumer_call_preview.json",
            "tests/test_sparkbot_lima_v1_g31_fake_runtime_consumer_call_preview.py",
        ],
        "arc_bot": [
            "tests/fixtures/arc_bot_shell_lima_v1_g31_fake_runtime_consumer_call_preview.json",
            "tests/test_arc_bot_shell_lima_v1_g31_fake_runtime_consumer_call_preview.py",
        ],
    }

    for record in _records():
        results = record["existing_consumer_test_results"]

        assert record["consumer_test_refs"] == expected_refs[record["consumer_packet_family"]]
        assert results["focused_v1_g32_consumer_test_result"] == "8 passed"
        assert results["focused_v1_g27_import_smoke_result"] == "7 passed"
        assert results["live_runtime_required"] is False
        assert results["external_services_required"] is False


def test_v1_g33_links_required_prior_evidence() -> None:
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


def test_v1_g33_runtime_and_external_boundaries_remain_false() -> None:
    fixture = _load_fixture()

    for key in (
        "consumer_runtime_source_files_changed",
        "consumer_runtime_calls_added",
        "live_consumer_import_calls_added",
        "planned_adapter_symbols_called",
        "adapter_symbol_calls_executed",
        "consumer_integration_added",
        "shell_runtime_wiring_added",
        "provider_model_calls_added",
        "model_request_dispatch_added",
        "secret_lookup_added",
        "credential_access_added",
        "tool_execution_outside_local_tests_added",
        "action_execution_added",
        "connector_browser_network_file_device_robotics_physical_world_behavior_added",
        "raw_diff_or_patch_persisted_in_lima_evidence",
        "raw_file_content_persisted_in_lima_evidence",
        "customer_data_persisted_in_lima_evidence",
    ):
        assert fixture[key] is False

    for record in _records():
        for key in (
            "consumer_runtime_source_file_edits_allowed",
            "lima_runtime_file_edits_allowed",
            "consumer_runtime_calls_added",
            "live_consumer_import_calls_added",
            "consumer_integration_added",
            "shell_runtime_wiring_added",
            "provider_model_calls_allowed",
            "model_request_dispatch_allowed",
            "secret_lookup_allowed",
            "credential_access_allowed",
            "tool_execution_allowed",
            "action_execution_allowed",
            "connector_browser_network_file_device_robotics_physical_world_behavior_allowed",
            "raw_diff_or_patch_persisted_in_lima_evidence",
            "raw_file_content_persisted_in_lima_evidence",
            "customer_data_persisted_in_lima_evidence",
        ):
            assert record[key] is False
        assert record["proof_not_authority"] is True


def test_v1_g33_rollback_metadata_is_local_and_reversible() -> None:
    expected_files = _load_fixture()["approved_lima_files_changed"]

    for record in _records():
        rollback = record["rollback_metadata"]

        assert rollback["rollback_ref"].startswith("rollback:v1-g33:")
        assert rollback["rollback_lima_file_refs"] == expected_files
        assert rollback["consumer_repo_changes_required"] is False
        assert rollback["runtime_source_repair_required"] is False
        assert rollback["external_service_changes_required"] is False


def test_v1_g33_required_confirmations_are_true() -> None:
    for record in _records():
        confirmations = record["required_confirmations"]

        assert confirmations["no_runtime_file_change_confirmation"] is True
        assert confirmations["no_consumer_repo_mutation_confirmation"] is True
        assert confirmations["no_consumer_test_file_creation_confirmation"] is True
        assert confirmations["no_live_runtime_call_confirmation"] is True
        assert confirmations["no_adapter_symbol_call_confirmation"] is True
        assert confirmations["no_fake_call_envelope_execution_confirmation"] is True
        assert (
            confirmations[
                "no_provider_model_secret_credential_connector_browser_network_physical_world_confirmation"
            ]
            is True
        )
        assert (
            confirmations[
                "no_raw_diff_patch_file_content_in_lima_evidence_confirmation"
            ]
            is True
        )
        assert confirmations["proof_not_authority_confirmation"] is True


def test_v1_g33_output_does_not_include_patch_bodies_or_sensitive_markers() -> None:
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


def test_v1_g33_docs_contain_boundary_language() -> None:
    implementation_text = (
        REPO_ROOT / "docs" / "V1_G33_CONSUMER_FAKE_RUNTIME_IMPORT_CALL_SMOKE.md"
    ).read_text(encoding="utf-8")
    closeout_text = (
        REPO_ROOT / "docs" / "V1_G33_CONSUMER_FAKE_RUNTIME_IMPORT_CALL_SMOKE_CLOSEOUT.md"
    ).read_text(encoding="utf-8")

    assert "No `lima/` runtime file" in implementation_text
    assert "V1-G33 changed no Sparkbot files" in implementation_text
    assert "Planned adapter symbols called: no" in implementation_text
    assert "Fake call envelopes were not executed" in closeout_text
    assert "V1-G33 is complete" in closeout_text
