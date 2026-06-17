"""Tests for V1-G27 first consumer frozen API import-smoke evidence."""

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
    / "v1_g27_first_consumer_frozen_api_import_smoke.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _records() -> list[dict[str, Any]]:
    records = _load_fixture()["consumer_records"]
    assert isinstance(records, list)
    return records


def test_v1_g27_fixture_records_approved_scope_and_boundaries() -> None:
    fixture = _load_fixture()

    assert fixture["packet_set_id"] == "v1_g27_first_consumer_frozen_api_import_smoke"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g27-first-consumer-frozen-api-import-smoke"
    assert fixture["operator_decision"] == "Approve-V1-G27"
    assert fixture["approved_scope"] == (
        "first_consumer_frozen_api_import_smoke_tests_fixtures_slice"
    )
    assert fixture["consumer_frozen_api_import_smoke_added"] is True
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["sparkbot_runtime_source_mutation_added"] is False
    assert fixture["arc_bot_shell_runtime_source_mutation_added"] is False
    assert fixture["imported_symbols_called"] is False
    assert fixture["consumer_runtime_calls_added"] is False
    assert fixture["product_ready"] is False


def test_v1_g27_contains_exactly_first_two_consumer_records() -> None:
    records = _records()

    assert [record["consumer_packet_family"] for record in records] == [
        "sparkbot",
        "arc_bot",
    ]
    assert [record["consumer_name"] for record in records] == [
        "Sparkbot",
        "Arc-Bot-shell",
    ]


def test_v1_g27_records_saved_consumer_commit_hashes() -> None:
    expected = {
        "sparkbot": "e169fa91ff9ccf35bf24d6f1ff9f57f5dae8402f",
        "arc_bot": "e619e51d2dca81b272173dffcbc60bf9c3f0d659",
    }

    for record in _records():
        assert record["consumer_commit_sha"] == expected[record["consumer_packet_family"]]
        assert len(record["consumer_commit_sha"]) == 40
        assert record["consumer_branch"] == "v1-g27-first-consumer-frozen-api-import-smoke"


def test_v1_g27_approved_import_symbols_are_frozen_surface() -> None:
    expected = [
        "lima.adapters.validate_v1_consumer_integration_compatibility_freeze",
        "lima.adapters.V1ConsumerIntegrationCompatibilityError",
    ]

    assert _load_fixture()["approved_import_smoke_symbols"] == expected
    for record in _records():
        assert record["approved_import_smoke_symbols"] == expected
        assert record["imported_symbols_called"] is False
        assert record["lima_runtime_behavior_invoked"] is False


def test_v1_g27_consumer_files_are_approved_tests_fixtures_only() -> None:
    expected_files = {
        "sparkbot": [
            "tests/fixtures/sparkbot_lima_v1_g27_frozen_api_import_smoke.json",
            "tests/test_sparkbot_lima_v1_g27_frozen_api_import_smoke.py",
        ],
        "arc_bot": [
            "tests/fixtures/arc_bot_shell_lima_v1_g27_frozen_api_import_smoke.json",
            "tests/test_arc_bot_shell_lima_v1_g27_frozen_api_import_smoke.py",
        ],
    }

    for record in _records():
        family = record["consumer_packet_family"]
        assert record["consumer_files_added"] == expected_files[family]
        assert record["test_only_import_smoke_added"] is True
        assert record["runtime_source_files_changed"] is False


def test_v1_g27_records_link_required_lima_evidence() -> None:
    for record in _records():
        assert record["frozen_api_packet_ref"] == "api-freeze:v1-g22"
        assert record["v1_g24_import_plan_id"].startswith("import-plan:v1-g24:")
        assert record["v1_g25_patch_preview_id"].startswith("patch-preview:v1-g25:")
        assert record["v1_g26_static_consumer_edit_id"].startswith(
            "static-consumer-edit:v1-g26:"
        )


def test_v1_g27_runtime_and_external_boundaries_remain_false() -> None:
    fixture = _load_fixture()

    for key in (
        "consumer_integration_added",
        "shell_runtime_wiring_added",
        "runtime_export_cleanup_approved",
        "runtime_export_cleanup_added",
        "provider_model_calls_added",
        "secret_lookup_added",
        "credential_access_added",
        "tool_execution_added",
        "connector_browser_network_file_device_robotics_physical_world_behavior_added",
        "raw_diff_or_patch_persisted",
        "raw_file_content_persisted",
    ):
        assert fixture[key] is False

    for record in _records():
        for key in (
            "consumer_runtime_calls_added",
            "consumer_integration_added",
            "shell_runtime_wiring_added",
            "runtime_export_cleanup_approved",
            "provider_model_calls_added",
            "secret_lookup_added",
            "credential_access_added",
            "tool_execution_added",
            "connector_browser_network_file_device_robotics_physical_world_behavior_added",
            "raw_diff_or_patch_persisted",
            "raw_file_content_persisted",
        ):
            assert record[key] is False
        assert record["proof_not_authority"] is True


def test_v1_g27_validation_and_rollback_metadata_are_present() -> None:
    for record in _records():
        validation = record["validation_metadata"]
        rollback = record["rollback_metadata"]

        assert validation["command_ref"]
        assert validation["passed"] is True
        assert validation["result"] == "7 passed"
        assert validation["live_runtime_required"] is False
        assert validation["external_services_required"] is False
        assert rollback["rollback_ref"]
        assert rollback["rollback_file_refs"] == record["consumer_files_added"]
        assert rollback["runtime_source_repair_required"] is False
        assert rollback["external_service_changes_required"] is False


def test_v1_g27_required_confirmations_are_true() -> None:
    for record in _records():
        confirmations = record["required_confirmations"]

        assert confirmations["no_live_import_call_confirmation"] is True
        assert confirmations["no_runtime_wiring_confirmation"] is True
        assert confirmations["no_runtime_export_cleanup_confirmation"] is True
        assert (
            confirmations[
                "no_raw_content_secret_credential_customer_data_diff_patch_confirmation"
            ]
            is True
        )
        assert confirmations["proof_not_authority_confirmation"] is True


def test_v1_g27_accepted_evidence_refs_exist() -> None:
    fixture = _load_fixture()

    for relative_path in fixture["accepted_evidence_refs"]:
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g27_output_does_not_include_patch_bodies_or_sensitive_markers() -> None:
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


def test_v1_g27_docs_contain_boundary_language() -> None:
    implementation_text = (
        REPO_ROOT / "docs" / "V1_G27_FIRST_CONSUMER_FROZEN_API_IMPORT_SMOKE.md"
    ).read_text(encoding="utf-8")
    closeout_text = (
        REPO_ROOT / "docs" / "V1_G27_FIRST_CONSUMER_FROZEN_API_IMPORT_SMOKE_CLOSEOUT.md"
    ).read_text(encoding="utf-8")

    assert "No `lima/` runtime file" in implementation_text
    assert "Imported LIMA symbols called: no" in implementation_text
    assert "Sparkbot runtime/source files changed: no" in implementation_text
    assert "Arc-Bot-shell runtime/source files changed: no" in implementation_text
    assert "V1-G27 is complete" in closeout_text
