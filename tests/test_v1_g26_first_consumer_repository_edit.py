"""Tests for V1-G26 first consumer repository edit intake evidence."""

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
    / "v1_g26_first_consumer_repository_edit.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _records() -> list[dict[str, Any]]:
    records = _load_fixture()["consumer_records"]
    assert isinstance(records, list)
    return records


def test_v1_g26_fixture_records_approved_scope_and_boundaries() -> None:
    fixture = _load_fixture()

    assert fixture["packet_set_id"] == "v1_g26_first_consumer_repository_edit"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g26-first-consumer-repository-edit"
    assert fixture["operator_decision"] == "Approve-V1-G26"
    assert fixture["approved_scope"] == (
        "first_consumer_repository_edit_static_docs_tests_fixtures_slice"
    )
    assert fixture["consumer_repository_edit_implementation_added"] is True
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["sparkbot_runtime_source_mutation_added"] is False
    assert fixture["arc_bot_shell_runtime_source_mutation_added"] is False
    assert fixture["consumer_runtime_calls_added"] is False
    assert fixture["consumer_code_imports_added"] is False
    assert fixture["product_ready"] is False


def test_v1_g26_contains_exactly_first_two_consumer_records() -> None:
    records = _records()

    assert [record["consumer_packet_family"] for record in records] == [
        "sparkbot",
        "arc_bot",
    ]
    assert [record["consumer_name"] for record in records] == [
        "Sparkbot",
        "Arc-Bot-shell",
    ]


def test_v1_g26_records_saved_consumer_commit_hashes() -> None:
    expected = {
        "sparkbot": "a3fa3af26bf3346a2dddd0051cab4b0fe00cd84f",
        "arc_bot": "f2a0a2c96829c83bc6dc24c201df6d18476a21d3",
    }

    for record in _records():
        assert record["consumer_commit_sha"] == expected[record["consumer_packet_family"]]
        assert len(record["consumer_commit_sha"]) == 40
        assert record["consumer_branch"] == "v1-g26-first-consumer-repository-edit"


def test_v1_g26_consumer_files_are_approved_static_files_only() -> None:
    expected_files = {
        "sparkbot": [
            "docs/proof_packets/SPARKBOT_LIMA_V1_G26_STATIC_CONSUMER_EDIT_PACKET.md",
            "tests/fixtures/sparkbot_lima_v1_g26_static_consumer_edit_packet.json",
            "tests/test_sparkbot_lima_v1_g26_static_consumer_edit_packet.py",
        ],
        "arc_bot": [
            "docs/proof_packets/ARC_BOT_SHELL_LIMA_V1_G26_STATIC_CONSUMER_EDIT_PACKET.md",
            "tests/fixtures/arc_bot_shell_lima_v1_g26_static_consumer_edit_packet.json",
            "tests/test_arc_bot_shell_lima_v1_g26_static_consumer_edit_packet.py",
        ],
    }

    for record in _records():
        family = record["consumer_packet_family"]
        assert record["consumer_files_added"] == expected_files[family]
        assert record["docs_tests_fixtures_only"] is True
        assert record["runtime_source_files_changed"] is False


def test_v1_g26_records_link_required_lima_evidence() -> None:
    for record in _records():
        family = record["consumer_packet_family"]
        suffix = "sparkbot" if family == "sparkbot" else "arc-bot-shell"

        assert record["proof_packet_ref"] == f"proof-packet:v1-g18:{suffix}"
        assert record["compatibility_packet_ref"] == f"compatibility:v1-g21:{suffix}"
        assert record["frozen_api_packet_ref"] == "api-freeze:v1-g22"
        assert record["v1_g23_import_plan_ref"] == "import-plan:v1-g23"
        assert record["v1_g24_import_plan_id"].startswith("import-plan:v1-g24:")
        assert record["v1_g25_patch_preview_id"].startswith("patch-preview:v1-g25:")


def test_v1_g26_runtime_and_external_boundaries_remain_false() -> None:
    fixture = _load_fixture()

    for key in (
        "live_lima_imports_from_consumers_added",
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
            "consumer_code_imports_added",
            "live_lima_imports_added",
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


def test_v1_g26_validation_and_rollback_metadata_are_present() -> None:
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


def test_v1_g26_required_confirmations_are_true() -> None:
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


def test_v1_g26_accepted_evidence_refs_exist() -> None:
    fixture = _load_fixture()

    for relative_path in fixture["accepted_evidence_refs"]:
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g26_output_does_not_include_patch_bodies_or_sensitive_markers() -> None:
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


def test_v1_g26_docs_contain_boundary_language() -> None:
    implementation_text = (
        REPO_ROOT / "docs" / "V1_G26_FIRST_CONSUMER_REPOSITORY_EDIT.md"
    ).read_text(encoding="utf-8")
    closeout_text = (
        REPO_ROOT / "docs" / "V1_G26_FIRST_CONSUMER_REPOSITORY_EDIT_CLOSEOUT.md"
    ).read_text(encoding="utf-8")

    assert "No `lima/` runtime file" in implementation_text
    assert "Sparkbot runtime/source files changed: no" in implementation_text
    assert "Arc-Bot-shell runtime/source files changed: no" in implementation_text
    assert "V1-G26 is complete" in closeout_text
    assert "No consumer code was imported" in closeout_text
