"""Tests for V1-G24 first consumer import-plan evidence packets."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from lima.adapters import validate_v1_consumer_integration_proof_to_import_dry_run


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g24_first_consumer_import_plan_evidence_packets.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _packets() -> list[dict[str, Any]]:
    packets = _load_fixture()["evidence_packets"]
    assert isinstance(packets, list)
    return packets


def test_v1_g24_fixture_records_approved_scope_and_boundaries() -> None:
    fixture = _load_fixture()

    assert fixture["packet_set_id"] == "v1_g24_first_consumer_import_plan_evidence_packets"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g24-first-consumer-import-plan-evidence-packets"
    assert fixture["operator_decision"] == "Approve-V1-G24"
    assert fixture["approved_scope"] == (
        "first_consumer_import_plan_evidence_packets_docs_tests_fixtures_slice"
    )
    assert fixture["first_consumer_import_plan_evidence_packets_added"] is True
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["sparkbot_repo_mutation_added"] is False
    assert fixture["arc_bot_shell_repo_mutation_added"] is False
    assert fixture["consumer_repo_mutation_added"] is False
    assert fixture["product_ready"] is False


def test_v1_g24_contains_exactly_first_two_consumer_packets() -> None:
    packets = _packets()

    assert [packet["consumer_packet_family"] for packet in packets] == [
        "sparkbot",
        "arc_bot",
    ]
    assert [packet["consumer_name"] for packet in packets] == [
        "Sparkbot",
        "Arc-Bot-shell",
    ]


def test_v1_g24_each_packet_validates_through_v1_g23_validator() -> None:
    for packet in _packets():
        record = validate_v1_consumer_integration_proof_to_import_dry_run(packet)

        assert record["record_type"] == "v1_consumer_integration_proof_to_import_dry_run"
        assert record["schema_version"] == "v1-g23-candidate"
        assert record["import_plan_metadata_only"] is True
        assert record["non_executing"] is True
        assert record["proof_not_authority"] is True
        assert record["consumer_repo_mutation_added"] is False
        assert record["consumer_code_imported"] is False
        assert record["consumer_runtime_calls_added"] is False
        assert record["consumer_integration_added"] is False
        assert record["runtime_export_cleanup_approved"] is False
        assert record["provider_model_calls_added"] is False
        assert record["secret_lookup_added"] is False
        assert record["tool_executed"] is False
        assert record["product_ready"] is False
        assert len(record["record_hash"]) == 64


def test_v1_g24_packet_refs_link_required_evidence() -> None:
    for packet in _packets():
        assert packet["proof_packet_ref"].startswith("proof-packet:v1-g18:")
        assert packet["compatibility_packet_ref"].startswith("compatibility:v1-g21:")
        assert packet["frozen_api_packet_ref"] == "api-freeze:v1-g22"
        assert "api-freeze:v1-g22" in packet["audit_evidence_linkage"]["evidence_refs"]
        assert "import-plan:v1-g23" in packet["audit_evidence_linkage"]["evidence_refs"]


def test_v1_g24_import_and_call_site_metadata_remains_metadata_only() -> None:
    for packet in _packets():
        proposed_import = packet["proposed_import_metadata"]
        call_site = packet["proposed_call_site_metadata"]

        assert proposed_import["metadata_only"] is True
        assert proposed_import["consumer_code_imported"] is False
        assert proposed_import["live_import_performed"] is False
        assert proposed_import["consumer_repo_mutation_added"] is False
        assert proposed_import["grants_runtime_authority"] is False
        assert call_site["metadata_only"] is True
        assert call_site["live_call_performed"] is False
        assert call_site["consumer_runtime_calls_added"] is False
        assert call_site["consumer_runtime_invoked"] is False
        assert call_site["grants_runtime_authority"] is False


def test_v1_g24_boundary_mappings_are_non_authorizing() -> None:
    boundary_fields = [
        "adapter_boundary_mapping",
        "guardian_boundary_mapping",
        "approval_boundary_mapping",
        "provider_model_route_boundary_mapping",
    ]

    for packet in _packets():
        for field in boundary_fields:
            boundary = packet[field]
            assert boundary["compatible"] is True
            assert boundary["metadata_only"] is True
            assert boundary["proof_not_authority"] is True
            assert boundary["grants_execution_authority"] is False
            assert boundary["future_integration_requires_approval"] is True
            assert boundary["mapped_refs"]


def test_v1_g24_expected_tests_are_dry_run_only() -> None:
    for packet in _packets():
        expected_tests = packet["expected_test_command_metadata"]

        assert expected_tests["command_refs"]
        assert expected_tests["expected_result_refs"]
        assert expected_tests["metadata_only"] is True
        assert expected_tests["dry_run_only"] is True
        assert expected_tests["consumer_runtime_invoked"] is False
        assert expected_tests["external_services_required"] is False


def test_v1_g24_rollback_metadata_requires_no_external_changes() -> None:
    for packet in _packets():
        rollback = packet["rollback_metadata"]

        assert rollback["rollback_ref"]
        assert rollback["rollback_step_refs"]
        assert rollback["consumer_repo_changes_required"] is False
        assert rollback["runtime_export_cleanup_required"] is False
        assert rollback["external_service_changes_required"] is False


def test_v1_g24_required_confirmations_are_true() -> None:
    for packet in _packets():
        assert packet["no_consumer_repo_mutation_confirmation"] is True
        assert packet["no_live_import_call_confirmation"] is True
        assert packet["no_runtime_export_cleanup_confirmation"] is True
        assert packet["no_raw_content_secret_credential_customer_data_confirmation"] is True
        assert packet["proof_not_authority_confirmation"] is True
        assert packet["audit_evidence_linkage"]["required"] is True
        assert packet["audit_evidence_linkage"]["proof_not_authority"] is True


def test_v1_g24_accepted_evidence_refs_exist() -> None:
    fixture = _load_fixture()

    for relative_path in fixture["accepted_evidence_refs"]:
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g24_output_does_not_include_raw_sensitive_markers() -> None:
    output = json.dumps(_load_fixture(), sort_keys=True)

    for forbidden in (
        "raw content",
        "raw file contents",
        "raw prompt",
        "raw customer data",
        "provider credential",
        "provider token",
        "api key value",
        "raw-secret-123",
    ):
        assert forbidden not in output


def test_v1_g24_docs_contain_boundary_language() -> None:
    implementation_text = (
        REPO_ROOT / "docs" / "V1_G24_FIRST_CONSUMER_IMPORT_PLAN_EVIDENCE_PACKETS.md"
    ).read_text(encoding="utf-8")
    closeout_text = (
        REPO_ROOT
        / "docs"
        / "V1_G24_FIRST_CONSUMER_IMPORT_PLAN_EVIDENCE_PACKETS_CLOSEOUT.md"
    ).read_text(encoding="utf-8")

    assert "No `lima/` runtime file" in implementation_text
    assert "Sparkbot import-plan evidence packet" in implementation_text
    assert "Arc-Bot-shell import-plan evidence packet" in implementation_text
    assert "consumer repo edits: not approved" in implementation_text
    assert "V1-G24 is complete" in closeout_text
    assert "No Sparkbot, Arc-Bot-shell, or other consumer repository files were changed" in closeout_text
