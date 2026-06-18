"""Tests for the approved V1-G35 consumer compatibility review slice."""

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
    / "v1_g35_consumer_integration_compatibility_review.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _records() -> list[dict[str, Any]]:
    records = _load_fixture()["compatibility_review_records"]
    assert isinstance(records, list)
    return records


def test_v1_g35_fixture_records_approved_scope_and_candidate_status() -> None:
    fixture = _load_fixture()

    assert fixture["packet_set_id"] == (
        "v1_g35_consumer_integration_compatibility_review"
    )
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g35-consumer-integration-compatibility-review"
    assert fixture["operator_decision"] == "Approve-V1-G35"
    assert fixture["approved_scope"] == "consumer_integration_compatibility_review_slice"
    assert fixture["consumer_integration_compatibility_review_added"] is True
    assert fixture["metadata_review_only"] is True
    assert fixture["bounded_consumer_integration_lane_proposed"] is True
    assert fixture["future_bounded_consumer_integration_design_gate_required"] is True
    assert fixture["consumer_integration_approved"] is False
    assert fixture["product_ready"] is False


def test_v1_g35_lima_file_scope_is_exact_and_runtime_free() -> None:
    fixture = _load_fixture()

    assert fixture["approved_lima_files_changed"] == [
        "docs/V1_G35_CONSUMER_INTEGRATION_COMPATIBILITY_REVIEW.md",
        "docs/V1_G35_CONSUMER_INTEGRATION_COMPATIBILITY_REVIEW_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g35_consumer_integration_compatibility_review.json",
        "tests/test_v1_g35_consumer_integration_compatibility_review.py",
    ]
    assert all(not path.startswith("lima/") for path in fixture["approved_lima_files_changed"])
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["lima_docs_tests_fixtures_only"] is True


def test_v1_g35_consumer_repo_scope_is_empty() -> None:
    fixture = _load_fixture()

    assert fixture["approved_consumer_files_changed"] == []
    assert fixture["consumer_repo_mutation_added"] is False
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["arc_bot_shell_files_changed"] is False

    for record in _records():
        assert record["consumer_repo_mutation_added"] is False
        assert record["consumer_runtime_source_files_changed"] is False
        assert record["rollback_metadata"]["rollback_consumer_file_refs"] == []


def test_v1_g35_contains_exactly_two_consumer_review_records() -> None:
    records = _records()

    assert [record["consumer_packet_family"] for record in records] == [
        "sparkbot",
        "arc_bot",
    ]
    assert [record["consumer_name"] for record in records] == [
        "Sparkbot",
        "Arc-Bot-shell",
    ]


def test_v1_g35_records_commits_and_source_refs() -> None:
    expected = {
        "sparkbot": (
            "sparkpit-labs/Sparkbot",
            "cee164655e1603f5e68b6df9773dc5b08dd27ca0",
            [
                "frozen-api-import-smoke:v1-g27:sparkbot:001",
                "runtime-export-cleanup:v1-g28",
                "live-consumer-import-call-plan:v1-g29:sparkbot:001",
                "fake-runtime-consumer-call-evidence:v1-g30:sparkbot:001",
                "fake-runtime-consumer-repo-test-preview:v1-g31:sparkbot:001",
                "consumer-repository-test-edit:v1-g32:sparkbot:001",
                "consumer-fake-runtime-import-call-smoke:v1-g33:sparkbot:001",
                "live-consumer-import-call:v1-g34:sparkbot:001",
            ],
        ),
        "arc_bot": (
            "armpit-symphony/Arc-Bot-shell",
            "61404a3bf7d95a45138ebd97992bcebe61651d79",
            [
                "frozen-api-import-smoke:v1-g27:arc-bot-shell:001",
                "runtime-export-cleanup:v1-g28",
                "live-consumer-import-call-plan:v1-g29:arc-bot-shell:001",
                "fake-runtime-consumer-call-evidence:v1-g30:arc-bot-shell:001",
                "fake-runtime-consumer-repo-test-preview:v1-g31:arc-bot-shell:001",
                "consumer-repository-test-edit:v1-g32:arc-bot-shell:001",
                "consumer-fake-runtime-import-call-smoke:v1-g33:arc-bot-shell:001",
                "live-consumer-import-call:v1-g34:arc-bot-shell:001",
            ],
        ),
    }

    for record in _records():
        repository, commit_sha, refs = expected[record["consumer_packet_family"]]

        assert record["compatibility_review_record_id"].startswith(
            "consumer-integration-compatibility-review:v1-g35:"
        )
        assert record["consumer_repository"] == repository
        assert record["reviewed_consumer_branch"] == "v1-g34-live-consumer-import-call"
        assert record["reviewed_consumer_commit_sha"] == commit_sha
        assert len(record["reviewed_consumer_commit_sha"]) == 40
        assert record["source_evidence_refs"] == refs


def test_v1_g35_review_result_and_remaining_gaps_are_locked() -> None:
    expected_gaps = [
        "consumer_integration_not_approved",
        "bounded_consumer_integration_design_not_approved",
        "shell_wiring_not_approved",
        "provider_model_dispatch_not_approved",
        "secret_credential_access_not_approved",
        "connector_browser_network_authority_not_approved",
        "physical_world_authority_not_approved",
        "product_readiness_not_approved",
    ]

    for record in _records():
        assert record["compatibility_review_result"] == (
            "candidate_ready_for_bounded_integration_design_gate"
        )
        assert record["bounded_consumer_integration_lane_proposed"] is True
        assert record["future_bounded_consumer_integration_design_gate_required"] is True
        assert record["remaining_gaps"] == expected_gaps
        assert record["consumer_integration_approved"] is False
        assert record["proof_not_integration_authority"] is True
        assert record["proof_not_product_readiness"] is True


def test_v1_g35_reviewed_evidence_status_is_complete() -> None:
    expected_status_keys = {
        "g27_import_smoke",
        "g28_runtime_export_cleanup",
        "g29_live_consumer_import_call_planning",
        "g30_fake_runtime_consumer_call_evidence",
        "g31_fake_runtime_consumer_repo_test_preview",
        "g32_consumer_repository_test_edit",
        "g33_consumer_fake_runtime_import_call_smoke",
        "g34_live_consumer_import_call_test",
        "g34_audit",
        "authority_chain_through_g34",
        "readiness_rollup_through_g34",
    }

    for record in _records():
        status = record["reviewed_evidence_status"]
        assert set(status) == expected_status_keys
        assert set(status.values()) == {"pass"}


def test_v1_g35_links_required_prior_evidence_documents() -> None:
    fixture = _load_fixture()

    assert fixture["reviewed_evidence_refs"] == [
        "docs/V1_G27_FIRST_CONSUMER_FROZEN_API_IMPORT_SMOKE.md",
        "docs/V1_G28_RUNTIME_EXPORT_CLEANUP.md",
        "docs/V1_G29_LIVE_CONSUMER_IMPORT_CALL_PLANNING.md",
        "docs/V1_G30_FAKE_RUNTIME_CONSUMER_CALL_EVIDENCE.md",
        "docs/V1_G31_FAKE_RUNTIME_CONSUMER_REPO_TEST_PREVIEW.md",
        "docs/V1_G32_CONSUMER_REPOSITORY_TEST_EDIT.md",
        "docs/V1_G33_CONSUMER_FAKE_RUNTIME_IMPORT_CALL_SMOKE.md",
        "docs/V1_G34_LIVE_CONSUMER_IMPORT_CALL.md",
        "docs/audits/V1_G34_LIVE_CONSUMER_IMPORT_CALL_AUDIT.md",
        "docs/audits/V1_RUNTIME_AUTHORITY_CHAIN_THROUGH_G34_AUDIT.md",
        "docs/readiness/V1_RUNTIME_READINESS_ROLLUP_THROUGH_G34.md",
        "docs/readiness/V1_POST_G34_NEXT_LANE_DECISION_MATRIX.md",
    ]

    for relative_path in fixture["reviewed_evidence_refs"]:
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g35_runtime_and_external_boundaries_remain_false() -> None:
    fixture = _load_fixture()

    forbidden_keys = (
        "consumer_runtime_source_files_changed",
        "lima_runtime_files_changed",
        "consumer_repo_mutation_added",
        "adapter_symbols_called",
        "consumer_runtime_modules_imported",
        "shell_runtime_wiring_added",
        "provider_model_calls_added",
        "model_request_dispatch_added",
        "fallback_execution_added",
        "secret_lookup_added",
        "credential_access_added",
        "tool_execution_outside_local_tests_added",
        "action_execution_added",
        "connector_browser_network_file_device_robotics_physical_world_behavior_added",
        "human_input_bridge_activated",
        "scheduled_task_execution_added",
        "external_sends_added",
        "external_database_writes_added",
        "raw_sensitive_content_persisted_in_lima_evidence",
    )

    for key in forbidden_keys:
        assert fixture[key] is False

    for record in _records():
        for key in forbidden_keys:
            if key in record:
                assert record[key] is False
        assert record["metadata_review_only"] is True
        assert record["product_ready"] is False


def test_v1_g35_rollback_metadata_is_local_and_reversible() -> None:
    expected_lima_files = _load_fixture()["approved_lima_files_changed"]

    for record in _records():
        rollback = record["rollback_metadata"]

        assert rollback["rollback_ref"].startswith("rollback:v1-g35:")
        assert rollback["rollback_lima_file_refs"] == expected_lima_files
        assert rollback["rollback_consumer_file_refs"] == []
        assert rollback["runtime_source_repair_required"] is False
        assert rollback["consumer_repository_repair_required"] is False
        assert rollback["shell_runtime_repair_required"] is False
        assert rollback["external_service_changes_required"] is False


def test_v1_g35_required_confirmations_are_true() -> None:
    for record in _records():
        confirmations = record["required_confirmations"]

        assert confirmations["no_lima_runtime_file_change_confirmation"] is True
        assert confirmations["no_consumer_repo_mutation_confirmation"] is True
        assert confirmations["no_consumer_runtime_source_change_confirmation"] is True
        assert confirmations["no_adapter_symbol_call_confirmation"] is True
        assert confirmations["no_consumer_runtime_module_import_confirmation"] is True
        assert confirmations["no_shell_wiring_confirmation"] is True
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
        assert confirmations["proof_not_integration_authority_confirmation"] is True
        assert confirmations["proof_not_product_readiness_confirmation"] is True


def test_v1_g35_output_does_not_include_patch_bodies_imports_or_sensitive_markers() -> None:
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
        "from lima",
    ):
        assert forbidden not in output


def test_v1_g35_docs_contain_boundary_language() -> None:
    implementation_text = (
        REPO_ROOT / "docs" / "V1_G35_CONSUMER_INTEGRATION_COMPATIBILITY_REVIEW.md"
    ).read_text(encoding="utf-8")
    closeout_text = (
        REPO_ROOT / "docs" / "V1_G35_CONSUMER_INTEGRATION_COMPATIBILITY_REVIEW_CLOSEOUT.md"
    ).read_text(encoding="utf-8")

    assert "metadata-only compatibility review" in implementation_text
    assert "No Sparkbot or Arc-Bot-shell file" in implementation_text
    assert "No adapter symbol was called" in closeout_text
    assert "proof-not-integration-authority" in closeout_text
    assert "No product-readiness or production-readiness claim" in closeout_text
    assert "V1-G35 is complete" in closeout_text
