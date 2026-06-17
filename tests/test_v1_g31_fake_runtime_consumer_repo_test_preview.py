"""Tests for the approved V1-G31 fake-runtime consumer repo test preview slice."""

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
    / "v1_g31_fake_runtime_consumer_repo_test_preview.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _records() -> list[dict[str, Any]]:
    records = _load_fixture()["consumer_repo_test_preview_records"]
    assert isinstance(records, list)
    return records


def test_v1_g31_fixture_records_approved_scope_and_boundaries() -> None:
    fixture = _load_fixture()

    assert fixture["packet_set_id"] == "v1_g31_fake_runtime_consumer_repo_test_preview"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g31-fake-runtime-consumer-repo-test-preview"
    assert fixture["operator_decision"] == "Approve-V1-G31"
    assert fixture["approved_scope"] == (
        "fake_runtime_consumer_repo_test_preview_metadata_slice"
    )
    assert fixture["fake_runtime_consumer_repo_test_preview_added"] is True
    assert fixture["future_consumer_test_files_previewed"] is True
    assert fixture["consumer_test_files_created"] is False
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["consumer_repo_mutation_added"] is False
    assert fixture["planned_adapter_symbols_called"] is False
    assert fixture["fake_call_envelopes_executed"] is False
    assert fixture["consumer_runtime_calls_added"] is False
    assert fixture["live_consumer_import_calls_added"] is False
    assert fixture["product_ready"] is False


def test_v1_g31_file_scope_is_docs_tests_fixtures_only() -> None:
    fixture = _load_fixture()

    assert fixture["approved_lima_files_changed"] == [
        "docs/V1_G31_FAKE_RUNTIME_CONSUMER_REPO_TEST_PREVIEW.md",
        "docs/V1_G31_FAKE_RUNTIME_CONSUMER_REPO_TEST_PREVIEW_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g31_fake_runtime_consumer_repo_test_preview.json",
        "tests/test_v1_g31_fake_runtime_consumer_repo_test_preview.py",
    ]
    assert all(not path.startswith("lima/") for path in fixture["approved_lima_files_changed"])
    assert fixture["approved_consumer_files_changed"] == []


def test_v1_g31_contains_exactly_first_two_consumer_preview_records() -> None:
    records = _records()

    assert [record["consumer_packet_family"] for record in records] == [
        "sparkbot",
        "arc_bot",
    ]
    assert [record["consumer_name"] for record in records] == [
        "Sparkbot",
        "Arc-Bot-shell",
    ]


def test_v1_g31_records_saved_consumer_evidence_commits_and_source_refs() -> None:
    expected = {
        "sparkbot": (
            "e169fa91ff9ccf35bf24d6f1ff9f57f5dae8402f",
            "live-consumer-import-call-plan:v1-g29:sparkbot:001",
            "fake-runtime-consumer-call-evidence:v1-g30:sparkbot:001",
        ),
        "arc_bot": (
            "e619e51d2dca81b272173dffcbc60bf9c3f0d659",
            "live-consumer-import-call-plan:v1-g29:arc-bot-shell:001",
            "fake-runtime-consumer-call-evidence:v1-g30:arc-bot-shell:001",
        ),
    }

    for record in _records():
        commit_sha, planning_ref, fake_runtime_ref = expected[
            record["consumer_packet_family"]
        ]
        assert record["consumer_evidence_commit_sha"] == commit_sha
        assert len(record["consumer_evidence_commit_sha"]) == 40
        assert record["consumer_evidence_branch"] == (
            "v1-g27-first-consumer-frozen-api-import-smoke"
        )
        assert record["planning_record_ref"] == planning_ref
        assert record["source_fake_runtime_evidence_record_ref"] == fake_runtime_ref


def test_v1_g31_future_consumer_test_paths_are_preview_only() -> None:
    expected_paths = {
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
        family = record["consumer_packet_family"]

        assert record["future_consumer_test_file_paths"] == expected_paths[family]
        assert record["preview_metadata_only"] is True
        assert record["future_consumer_test_paths_previewed"] is True
        assert record["consumer_test_files_created"] is False
        assert record["consumer_repo_edits_allowed"] is False


def test_v1_g31_expected_assertion_categories_are_sanitized() -> None:
    expected = [
        "fixture_records_candidate_only_status",
        "imports_approved_candidate_adapter_symbols_without_calling",
        "asserts_fake_runtime_metadata_only",
        "asserts_no_network_secret_provider_model_or_external_service",
        "asserts_no_consumer_runtime_invocation",
        "asserts_no_raw_content_or_patch_persistence",
        "asserts_proof_not_authority",
    ]

    for record in _records():
        assert record["sanitized_assertion_categories"] == expected
        assert record["raw_test_content_persisted"] is False
        assert record["raw_patch_content_persisted"] is False
        assert record["raw_diff_content_persisted"] is False


def test_v1_g31_fake_call_surfaces_are_exact_and_not_called() -> None:
    expected = [
        "lima.adapters.validate_v1_consumer_integration_compatibility_freeze",
        "lima.adapters.validate_v1_consumer_integration_proof_to_import_dry_run",
    ]

    assert _load_fixture()["fake_runtime_candidate_adapter_symbols"] == expected
    for record in _records():
        assert record["fake_call_surface_refs"] == expected
        assert record["planned_adapter_symbols_called"] is False
        assert record["fake_call_envelope_executed"] is False
        assert record["fake_call_envelope_ref"].startswith("fake-call-envelope:v1-g30:")


def test_v1_g31_runtime_and_external_boundaries_remain_false() -> None:
    fixture = _load_fixture()

    for key in (
        "sparkbot_files_changed",
        "arc_bot_shell_files_changed",
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
        "raw_test_content_persisted",
    ):
        assert fixture[key] is False

    for record in _records():
        for key in (
            "consumer_runtime_calls_added",
            "live_consumer_import_calls_added",
            "planned_adapter_symbols_called",
            "fake_call_envelope_executed",
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
        ):
            assert record[key] is False
        assert record["proof_not_authority"] is True


def test_v1_g31_links_required_prior_evidence() -> None:
    fixture = _load_fixture()

    for relative_path in fixture["accepted_evidence_refs"]:
        assert (REPO_ROOT / relative_path).exists()

    for record in _records():
        assert any(ref.startswith("frozen-api-import-smoke:v1-g27:") for ref in record["evidence_refs"])
        assert "runtime-export-cleanup:v1-g28" in record["evidence_refs"]
        assert record["planning_record_ref"] in record["evidence_refs"]
        assert record["source_fake_runtime_evidence_record_ref"] in record["evidence_refs"]


def test_v1_g31_rollback_metadata_is_local_and_reversible() -> None:
    expected_files = _load_fixture()["approved_lima_files_changed"]

    for record in _records():
        rollback = record["rollback_metadata"]

        assert rollback["rollback_ref"].startswith("rollback:v1-g31:")
        assert rollback["rollback_file_refs"] == expected_files
        assert rollback["consumer_repo_changes_required"] is False
        assert rollback["runtime_source_repair_required"] is False
        assert rollback["external_service_changes_required"] is False


def test_v1_g31_required_confirmations_are_true() -> None:
    for record in _records():
        confirmations = record["required_confirmations"]

        assert confirmations["no_runtime_file_change_confirmation"] is True
        assert confirmations["no_consumer_repo_mutation_confirmation"] is True
        assert confirmations["no_consumer_test_file_creation_confirmation"] is True
        assert confirmations["no_live_import_call_confirmation"] is True
        assert confirmations["no_adapter_symbol_call_confirmation"] is True
        assert (
            confirmations[
                "no_provider_model_secret_credential_connector_browser_network_physical_world_confirmation"
            ]
            is True
        )
        assert confirmations["no_raw_diff_patch_test_file_content_confirmation"] is True
        assert confirmations["proof_not_authority_confirmation"] is True


def test_v1_g31_output_does_not_include_patch_bodies_or_sensitive_markers() -> None:
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


def test_v1_g31_docs_contain_boundary_language() -> None:
    implementation_text = (
        REPO_ROOT / "docs" / "V1_G31_FAKE_RUNTIME_CONSUMER_REPO_TEST_PREVIEW.md"
    ).read_text(encoding="utf-8")
    closeout_text = (
        REPO_ROOT / "docs" / "V1_G31_FAKE_RUNTIME_CONSUMER_REPO_TEST_PREVIEW_CLOSEOUT.md"
    ).read_text(encoding="utf-8")

    assert "No `lima/` runtime file" in implementation_text
    assert "No Sparkbot or Arc-Bot-shell file" in implementation_text
    assert "Consumer test files created: no" in implementation_text
    assert "No consumer test file was created" in closeout_text
    assert "V1-G31 is complete" in closeout_text
