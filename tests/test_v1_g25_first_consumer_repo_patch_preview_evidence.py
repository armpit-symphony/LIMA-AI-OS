"""Tests for V1-G25 first consumer repo patch-preview evidence."""

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
    / "v1_g25_first_consumer_repo_patch_preview_evidence.json"
)
G24_FIXTURE_PATH = (
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


def _load_g24_fixture() -> dict[str, Any]:
    fixture = json.loads(G24_FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _packets() -> list[dict[str, Any]]:
    packets = _load_fixture()["patch_preview_packets"]
    assert isinstance(packets, list)
    return packets


def test_v1_g25_fixture_records_approved_scope_and_boundaries() -> None:
    fixture = _load_fixture()

    assert fixture["packet_set_id"] == "v1_g25_first_consumer_repo_patch_preview_evidence"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g25-first-consumer-repo-patch-preview-evidence"
    assert fixture["operator_decision"] == "Approve-V1-G25"
    assert fixture["approved_scope"] == (
        "first_consumer_repo_patch_preview_evidence_docs_tests_fixtures_slice"
    )
    assert fixture["first_consumer_repo_patch_preview_evidence_added"] is True
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["sparkbot_repo_mutation_added"] is False
    assert fixture["arc_bot_shell_repo_mutation_added"] is False
    assert fixture["consumer_repo_mutation_added"] is False
    assert fixture["consumer_repo_file_writes_added"] is False
    assert fixture["patch_files_generated"] is False
    assert fixture["diff_body_included"] is False
    assert fixture["full_patch_body_included"] is False
    assert fixture["raw_file_contents_included"] is False
    assert fixture["product_ready"] is False


def test_v1_g25_contains_exactly_first_two_consumer_patch_previews() -> None:
    packets = _packets()

    assert [packet["consumer_packet_family"] for packet in packets] == [
        "sparkbot",
        "arc_bot",
    ]
    assert [packet["consumer_name"] for packet in packets] == [
        "Sparkbot",
        "Arc-Bot-shell",
    ]


def test_v1_g25_each_packet_links_to_v1_g24_import_plan_evidence() -> None:
    g24_ids = {
        packet["import_plan_id"] for packet in _load_g24_fixture()["evidence_packets"]
    }

    for packet in _packets():
        assert packet["v1_g24_import_plan_id"] in g24_ids
        assert packet["v1_g24_import_plan_id"] in packet["audit_evidence_linkage"][
            "evidence_refs"
        ]


def test_v1_g25_packet_refs_link_required_evidence() -> None:
    for packet in _packets():
        assert packet["proof_packet_ref"].startswith("proof-packet:v1-g18:")
        assert packet["compatibility_packet_ref"].startswith("compatibility:v1-g21:")
        assert packet["frozen_api_packet_ref"] == "api-freeze:v1-g22"
        assert packet["v1_g23_import_plan_ref"] == "import-plan:v1-g23"
        assert "api-freeze:v1-g22" in packet["audit_evidence_linkage"]["evidence_refs"]
        assert "import-plan:v1-g23" in packet["audit_evidence_linkage"]["evidence_refs"]


def test_v1_g25_file_targets_are_sanitized_metadata_only() -> None:
    for packet in _packets():
        targets = packet["sanitized_file_target_metadata"]

        assert targets["metadata_only"] is True
        assert targets["consumer_repo_file_writes_added"] is False
        assert len(targets["file_targets"]) == 2
        for target in targets["file_targets"]:
            assert target["path_ref"]
            assert target["target_kind"]
            assert target["operation_intent"]
            assert target["raw_file_contents_included"] is False
            assert target["diff_body_included"] is False
            assert target["full_patch_body_included"] is False


def test_v1_g25_edit_intent_metadata_is_non_authorizing() -> None:
    for packet in _packets():
        edit_intent = packet["edit_intent_metadata"]

        assert edit_intent["metadata_only"] is True
        assert edit_intent["intent_refs"]
        assert edit_intent["proposed_import_refs"]
        assert edit_intent["proposed_call_site_refs"]
        assert edit_intent["consumer_code_imported"] is False
        assert edit_intent["live_import_performed"] is False
        assert edit_intent["consumer_runtime_calls_added"] is False
        assert edit_intent["consumer_integration_added"] is False
        assert edit_intent["grants_edit_authority"] is False
        assert edit_intent["grants_runtime_authority"] is False


def test_v1_g25_approval_validation_and_rollback_metadata_are_present() -> None:
    for packet in _packets():
        approval = packet["approval_requirement_metadata"]
        validation = packet["validation_metadata"]
        rollback = packet["rollback_metadata"]

        assert approval["approval_required_before_repo_edit"] is True
        assert approval["required_future_gate"] == "consumer_repository_edit_approval"
        assert approval["requires_exact_file_scope"] is True
        assert approval["requires_rollback_plan"] is True
        assert approval["requires_consumer_ci_plan"] is True
        assert approval["metadata_only"] is True
        assert approval["proof_not_authority"] is True
        assert validation["command_refs"]
        assert validation["expected_result_refs"]
        assert validation["metadata_only"] is True
        assert validation["dry_run_only"] is True
        assert validation["consumer_runtime_invoked"] is False
        assert validation["external_services_required"] is False
        assert rollback["rollback_ref"]
        assert rollback["rollback_step_refs"]
        assert rollback["consumer_repo_changes_required_now"] is False
        assert rollback["runtime_export_cleanup_required"] is False
        assert rollback["external_service_changes_required"] is False


def test_v1_g25_required_confirmations_are_true() -> None:
    for packet in _packets():
        assert packet["no_consumer_repo_mutation_confirmation"] is True
        assert packet["no_consumer_repo_file_write_confirmation"] is True
        assert packet["no_patch_file_generated_confirmation"] is True
        assert packet["no_live_import_call_confirmation"] is True
        assert packet["no_runtime_export_cleanup_confirmation"] is True
        assert (
            packet[
                "no_raw_content_secret_credential_customer_data_diff_patch_confirmation"
            ]
            is True
        )
        assert packet["proof_not_authority_confirmation"] is True
        assert packet["audit_evidence_linkage"]["required"] is True
        assert packet["audit_evidence_linkage"]["proof_not_authority"] is True


def test_v1_g25_accepted_evidence_refs_exist() -> None:
    fixture = _load_fixture()

    for relative_path in fixture["accepted_evidence_refs"]:
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g25_output_does_not_include_patch_bodies_or_sensitive_markers() -> None:
    output = json.dumps(_load_fixture(), sort_keys=True)

    for forbidden in (
        "diff --git",
        "@@",
        "BEGIN PATCH",
        "raw prompt value",
        "raw customer data value",
        "provider credential value",
        "provider token value",
        "api key value",
        "raw-secret-123",
    ):
        assert forbidden not in output


def test_v1_g25_docs_contain_boundary_language() -> None:
    implementation_text = (
        REPO_ROOT / "docs" / "V1_G25_FIRST_CONSUMER_REPO_PATCH_PREVIEW_EVIDENCE.md"
    ).read_text(encoding="utf-8")
    closeout_text = (
        REPO_ROOT
        / "docs"
        / "V1_G25_FIRST_CONSUMER_REPO_PATCH_PREVIEW_EVIDENCE_CLOSEOUT.md"
    ).read_text(encoding="utf-8")

    assert "No `lima/` runtime file" in implementation_text
    assert "Sparkbot patch-preview evidence packet" in implementation_text
    assert "Arc-Bot-shell patch-preview evidence packet" in implementation_text
    assert "raw diffs and full patch bodies: not approved" in implementation_text
    assert "V1-G25 is complete" in closeout_text
    assert "No Sparkbot, Arc-Bot-shell, or other consumer repository files were changed" in closeout_text
