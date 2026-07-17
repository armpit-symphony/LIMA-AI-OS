"""Tests for the approved V1-G30 fake-runtime consumer call evidence slice."""

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
    / "v1_g30_fake_runtime_consumer_call_evidence.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _records() -> list[dict[str, Any]]:
    records = _load_fixture()["consumer_fake_runtime_evidence_records"]
    assert isinstance(records, list)
    return records


def test_v1_g30_fixture_records_approved_scope_and_boundaries() -> None:
    fixture = _load_fixture()

    assert fixture["packet_set_id"] == "v1_g30_fake_runtime_consumer_call_evidence"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g30-fake-runtime-consumer-call-evidence"
    assert fixture["operator_decision"] == "Approve-V1-G30"
    assert fixture["approved_scope"] == "fake_runtime_consumer_call_evidence_metadata_slice"
    assert fixture["fake_runtime_consumer_call_evidence_added"] is True
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["consumer_repo_mutation_added"] is False
    assert fixture["planned_adapter_symbols_called"] is False
    assert fixture["adapter_symbol_calls_executed"] is False
    assert fixture["consumer_runtime_calls_added"] is False
    assert fixture["live_consumer_import_calls_added"] is False
    assert fixture["product_ready"] is False


def test_v1_g30_file_scope_is_docs_tests_fixtures_only() -> None:
    fixture = _load_fixture()

    assert fixture["approved_lima_files_changed"] == [
        "docs/V1_G30_FAKE_RUNTIME_CONSUMER_CALL_EVIDENCE.md",
        "docs/V1_G30_FAKE_RUNTIME_CONSUMER_CALL_EVIDENCE_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g30_fake_runtime_consumer_call_evidence.json",
        "tests/test_v1_g30_fake_runtime_consumer_call_evidence.py",
    ]
    assert all(not path.startswith("lima/") for path in fixture["approved_lima_files_changed"])


def test_v1_g30_contains_exactly_first_two_consumer_evidence_records() -> None:
    records = _records()

    assert [record["consumer_packet_family"] for record in records] == [
        "sparkbot",
        "arc_bot",
    ]
    assert [record["consumer_name"] for record in records] == [
        "Sparkbot",
        "Arc-Bot-shell",
    ]


def test_v1_g30_records_saved_consumer_evidence_commits_and_planning_refs() -> None:
    expected = {
        "sparkbot": (
            "e169fa91ff9ccf35bf24d6f1ff9f57f5dae8402f",
            "live-consumer-import-call-plan:v1-g29:sparkbot:001",
        ),
        "arc_bot": (
            "e619e51d2dca81b272173dffcbc60bf9c3f0d659",
            "live-consumer-import-call-plan:v1-g29:arc-bot-shell:001",
        ),
    }

    for record in _records():
        commit_sha, planning_ref = expected[record["consumer_packet_family"]]
        assert record["consumer_evidence_commit_sha"] == commit_sha
        assert len(record["consumer_evidence_commit_sha"]) == 40
        assert record["consumer_evidence_branch"] == (
            "v1-g27-first-consumer-frozen-api-import-smoke"
        )
        assert record["planning_record_ref"] == planning_ref


def test_v1_g30_fake_call_surfaces_are_exact_and_not_called() -> None:
    expected = [
        "lima.adapters.validate_v1_consumer_integration_compatibility_freeze",
        "lima.adapters.validate_v1_consumer_integration_proof_to_import_dry_run",
    ]

    assert _load_fixture()["fake_runtime_candidate_adapter_symbols"] == expected
    for record in _records():
        envelope = record["fake_call_envelope"]

        assert envelope["adapter_symbol_refs"] == expected
        assert record["planned_adapter_symbols_called"] is False
        assert record["adapter_symbol_calls_executed"] is False
        assert envelope["executed"] is False


def test_v1_g30_fake_call_envelopes_are_metadata_only() -> None:
    for record in _records():
        envelope = record["fake_call_envelope"]

        assert envelope["call_shape_refs"] == [
            "validate_v1_consumer_integration_compatibility_freeze(metadata)",
            "validate_v1_consumer_integration_proof_to_import_dry_run(metadata)",
        ]
        assert envelope["metadata_payload_ref"].startswith("fixture://runtime_extraction/")
        assert record["metadata_only"] is True
        assert record["fake_runtime_only"] is True
        assert envelope["consumer_runtime_invoked"] is False
        assert envelope["external_services_required"] is False
        assert envelope["network_required"] is False
        assert envelope["secrets_required"] is False
        assert envelope["provider_model_required"] is False


def test_v1_g30_runtime_and_external_boundaries_remain_false() -> None:
    fixture = _load_fixture()

    for key in (
        "consumer_integration_added",
        "shell_runtime_wiring_added",
        "provider_model_calls_added",
        "model_request_dispatch_added",
        "secret_lookup_added",
        "credential_access_added",
        "tool_execution_added",
        "action_execution_added",
        "connector_browser_network_file_device_robotics_physical_world_behavior_added",
        "raw_diff_or_patch_persisted",
        "raw_file_content_persisted",
    ):
        assert fixture[key] is False

    for record in _records():
        for key in (
            "consumer_runtime_calls_added",
            "live_consumer_import_calls_added",
            "planned_adapter_symbols_called",
            "adapter_symbol_calls_executed",
            "consumer_integration_added",
            "shell_runtime_wiring_added",
            "provider_model_calls_allowed",
            "model_request_dispatch_allowed",
            "consumer_repo_edits_allowed",
            "lima_runtime_file_edits_allowed",
            "secret_lookup_allowed",
            "credential_access_allowed",
            "tool_execution_allowed",
            "action_execution_allowed",
            "connector_browser_network_file_device_robotics_physical_world_behavior_allowed",
            "raw_diff_or_patch_persisted",
            "raw_file_content_persisted",
        ):
            assert record[key] is False
        assert record["proof_not_authority"] is True


def test_v1_g30_links_required_prior_evidence() -> None:
    fixture = _load_fixture()

    for relative_path in fixture["accepted_evidence_refs"]:
        assert (REPO_ROOT / relative_path).exists()

    for record in _records():
        assert any(ref.startswith("frozen-api-import-smoke:v1-g27:") for ref in record["evidence_refs"])
        assert "runtime-export-cleanup:v1-g28" in record["evidence_refs"]
        assert record["planning_record_ref"] in record["evidence_refs"]


def test_v1_g30_rollback_metadata_is_local_and_reversible() -> None:
    expected_files = _load_fixture()["approved_lima_files_changed"]

    for record in _records():
        rollback = record["rollback_metadata"]

        assert rollback["rollback_ref"].startswith("rollback:v1-g30:")
        assert rollback["rollback_file_refs"] == expected_files
        assert rollback["consumer_repo_changes_required"] is False
        assert rollback["runtime_source_repair_required"] is False
        assert rollback["external_service_changes_required"] is False


def test_v1_g30_required_confirmations_are_true() -> None:
    for record in _records():
        confirmations = record["required_confirmations"]

        assert confirmations["no_runtime_file_change_confirmation"] is True
        assert confirmations["no_consumer_repo_mutation_confirmation"] is True
        assert confirmations["no_live_import_call_confirmation"] is True
        assert confirmations["no_adapter_symbol_call_confirmation"] is True
        assert (
            confirmations[
                "no_provider_model_secret_credential_connector_browser_network_physical_world_confirmation"
            ]
            is True
        )
        assert confirmations["proof_not_authority_confirmation"] is True


def test_v1_g30_output_does_not_include_patch_bodies_or_sensitive_markers() -> None:
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
    ):
        assert forbidden not in output


def test_v1_g30_docs_contain_boundary_language() -> None:
    implementation_text = (
        REPO_ROOT / "docs" / "V1_G30_FAKE_RUNTIME_CONSUMER_CALL_EVIDENCE.md"
    ).read_text(encoding="utf-8")
    closeout_text = (
        REPO_ROOT / "docs" / "V1_G30_FAKE_RUNTIME_CONSUMER_CALL_EVIDENCE_CLOSEOUT.md"
    ).read_text(encoding="utf-8")

    assert "No `lima/` runtime file" in implementation_text
    assert "Planned adapter symbols called: no" in implementation_text
    assert "Fake call envelopes were not executed" in closeout_text
    assert "V1-G30 is complete" in closeout_text
