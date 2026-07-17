"""Tests for the approved V1-G37 consumer integration patch-preview slice."""

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
    / "v1_g37_consumer_integration_patch_preview.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _records() -> list[dict[str, Any]]:
    records = _load_fixture()["patch_preview_records"]
    assert isinstance(records, list)
    return records


def test_v1_g37_fixture_records_approved_scope_and_candidate_status() -> None:
    fixture = _load_fixture()

    assert fixture["packet_set_id"] == "v1_g37_consumer_integration_patch_preview"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g37-consumer-integration-patch-preview"
    assert fixture["operator_decision"] == "Approve-V1-G37"
    assert fixture["approved_scope"] == "consumer_integration_patch_preview_evidence_slice"
    assert fixture["consumer_integration_patch_preview_added"] is True
    assert fixture["metadata_preview_only"] is True
    assert fixture["sanitized_patch_preview_only"] is True
    assert fixture["future_consumer_repository_edit_gate_required"] is True
    assert fixture["future_consumer_integration_import_smoke_gate_required"] is True
    assert fixture["consumer_repository_edit_approved"] is False
    assert fixture["consumer_integration_approved"] is False
    assert fixture["consumer_integration_added"] is False
    assert fixture["product_ready"] is False


def test_v1_g37_lima_file_scope_is_exact_and_runtime_free() -> None:
    fixture = _load_fixture()

    assert fixture["approved_lima_files_changed"] == [
        "docs/V1_G37_CONSUMER_INTEGRATION_PATCH_PREVIEW.md",
        "docs/V1_G37_CONSUMER_INTEGRATION_PATCH_PREVIEW_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g37_consumer_integration_patch_preview.json",
        "tests/test_v1_g37_consumer_integration_patch_preview.py",
    ]
    assert all(not path.startswith("lima/") for path in fixture["approved_lima_files_changed"])
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["lima_docs_tests_fixtures_only"] is True


def test_v1_g37_consumer_repo_scope_is_empty() -> None:
    fixture = _load_fixture()

    assert fixture["approved_consumer_files_changed"] == []
    assert fixture["consumer_repo_mutation_added"] is False
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["arc_bot_shell_files_changed"] is False

    for record in _records():
        assert record["consumer_repo_mutation_added"] is False
        assert record["consumer_runtime_source_files_changed"] is False
        assert record["rollback_metadata"]["rollback_consumer_file_refs"] == []


def test_v1_g37_contains_exactly_two_consumer_preview_records() -> None:
    records = _records()

    assert [record["consumer_packet_family"] for record in records] == [
        "sparkbot",
        "arc_bot",
    ]
    assert [record["consumer_name"] for record in records] == [
        "Sparkbot",
        "Arc-Bot-shell",
    ]


def test_v1_g37_records_commits_and_bounded_design_refs() -> None:
    expected = {
        "sparkbot": (
            "sparkpit-labs/Sparkbot",
            "cee164655e1603f5e68b6df9773dc5b08dd27ca0",
            "bounded-consumer-integration-design:v1-g36:sparkbot:001",
        ),
        "arc_bot": (
            "armpit-symphony/Arc-Bot-shell",
            "61404a3bf7d95a45138ebd97992bcebe61651d79",
            "bounded-consumer-integration-design:v1-g36:arc-bot-shell:001",
        ),
    }

    for record in _records():
        repository, commit_sha, design_ref = expected[record["consumer_packet_family"]]

        assert record["patch_preview_record_id"].startswith(
            "consumer-integration-patch-preview:v1-g37:"
        )
        assert record["consumer_repository"] == repository
        assert record["reviewed_consumer_branch"] == "v1-g34-live-consumer-import-call"
        assert record["reviewed_consumer_commit_sha"] == commit_sha
        assert len(record["reviewed_consumer_commit_sha"]) == 40
        assert record["source_bounded_design_record_ref"] == design_ref


def test_v1_g37_preview_result_and_remaining_gaps_are_locked() -> None:
    expected_gaps = [
        "consumer_repository_edit_not_approved",
        "consumer_integration_import_smoke_not_approved",
        "consumer_integration_not_approved",
        "shell_wiring_implementation_not_approved",
        "provider_model_dispatch_not_approved",
        "secret_credential_access_not_approved",
        "connector_browser_network_authority_not_approved",
        "physical_world_authority_not_approved",
        "product_readiness_not_approved",
    ]

    for record in _records():
        assert record["patch_preview_result"] == (
            "candidate_patch_preview_defined_for_future_consumer_repository_edit_gate"
        )
        assert record["future_consumer_repository_edit_gate_required"] is True
        assert record["future_consumer_integration_import_smoke_gate_required"] is True
        assert record["remaining_gaps"] == expected_gaps
        assert record["consumer_repository_edit_approved"] is False
        assert record["consumer_integration_approved"] is False
        assert record["proof_not_edit_authority"] is True
        assert record["proof_not_integration_authority"] is True
        assert record["proof_not_product_readiness"] is True


def test_v1_g37_future_gates_remain_blocked() -> None:
    expected_gates = [
        "consumer_repository_edit_approval_request",
        "consumer_integration_import_smoke_approval_request",
        "shell_wiring_design_approval_request",
        "provider_model_dispatch_approval_request",
        "connector_browser_network_authority_approval_request",
        "physical_world_authority_approval_request",
        "product_readiness_approval_request",
    ]
    expected_blocked_authorities = {
        "consumer_repository_edit_approved": False,
        "consumer_integration_import_smoke_approved": False,
        "shell_wiring_implementation_approved": False,
        "provider_model_dispatch_approved": False,
        "connector_browser_network_authority_approved": False,
        "physical_world_authority_approved": False,
        "product_readiness_approved": False,
    }
    fixture = _load_fixture()

    assert fixture["future_required_gates"] == expected_gates
    assert fixture["blocked_future_authorities"] == expected_blocked_authorities

    for record in _records():
        assert record["future_required_gates"] == expected_gates
        assert record["blocked_future_authorities"] == expected_blocked_authorities


def test_v1_g37_future_candidate_file_refs_are_sanitized_and_not_applied() -> None:
    expected_paths = {
        "sparkbot": [
            "tests/fixtures/sparkbot_lima_v1_g38_consumer_integration_candidate.json",
            "tests/test_sparkbot_lima_v1_g38_consumer_integration_candidate.py",
        ],
        "arc_bot": [
            "tests/fixtures/arc_bot_shell_lima_v1_g38_consumer_integration_candidate.json",
            "tests/test_arc_bot_shell_lima_v1_g38_consumer_integration_candidate.py",
        ],
    }

    for record in _records():
        refs = record["future_candidate_consumer_file_refs"]
        assert [ref["path"] for ref in refs] == expected_paths[record["consumer_packet_family"]]
        for ref in refs:
            assert ref["operation"] == "future_create_if_approved"
            assert "sanitized static candidate integration" in ref["content_summary"]
            assert ref["raw_content_persisted"] is False
            assert ref["requires_future_consumer_repository_edit_gate"] is True


def test_v1_g37_sanitized_edit_intent_categories_are_locked() -> None:
    expected_categories = [
        "future_static_integration_fixture",
        "future_static_integration_test",
        "future_guardian_boundary_assertions",
        "future_no_live_provider_model_assertions",
        "future_no_secret_connector_network_physical_world_assertions",
        "future_rollback_metadata_assertions",
    ]
    fixture = _load_fixture()

    assert fixture["sanitized_edit_intent_categories"] == expected_categories

    for record in _records():
        assert record["sanitized_edit_intent_categories"] == expected_categories
        assert record["metadata_preview_only"] is True
        assert record["sanitized_patch_preview_only"] is True


def test_v1_g37_links_required_prior_evidence_documents() -> None:
    fixture = _load_fixture()

    assert fixture["reviewed_evidence_refs"] == [
        "docs/V1_G36_BOUNDED_CONSUMER_INTEGRATION_DESIGN.md",
        "docs/V1_G36_BOUNDED_CONSUMER_INTEGRATION_DESIGN_CLOSEOUT.md",
        "docs/audits/V1_G36_BOUNDED_CONSUMER_INTEGRATION_DESIGN_AUDIT.md",
        "docs/audits/V1_RUNTIME_AUTHORITY_CHAIN_THROUGH_G36_AUDIT.md",
        "docs/readiness/V1_RUNTIME_READINESS_ROLLUP_THROUGH_G36.md",
        "docs/readiness/V1_POST_G36_NEXT_LANE_DECISION_MATRIX.md",
    ]

    for relative_path in fixture["reviewed_evidence_refs"]:
        assert (REPO_ROOT / relative_path).exists()

    for record in _records():
        for relative_path in record["source_evidence_refs"]:
            assert (REPO_ROOT / relative_path).exists()


def test_v1_g37_runtime_patch_and_external_boundaries_remain_false() -> None:
    fixture = _load_fixture()

    forbidden_keys = (
        "consumer_runtime_source_files_changed",
        "lima_runtime_files_changed",
        "consumer_repo_mutation_added",
        "raw_patch_bodies_persisted",
        "patches_applied",
        "adapter_symbols_called",
        "consumer_runtime_modules_imported",
        "consumer_integration_added",
        "shell_runtime_wiring_implementation_added",
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
        assert record["metadata_preview_only"] is True
        assert record["product_ready"] is False


def test_v1_g37_rollback_metadata_is_local_and_reversible() -> None:
    expected_lima_files = _load_fixture()["approved_lima_files_changed"]

    for record in _records():
        rollback = record["rollback_metadata"]

        assert rollback["rollback_ref"].startswith("rollback:v1-g37:")
        assert rollback["rollback_lima_file_refs"] == expected_lima_files
        assert rollback["rollback_consumer_file_refs"] == []
        assert rollback["runtime_source_repair_required"] is False
        assert rollback["consumer_repository_repair_required"] is False
        assert rollback["shell_runtime_repair_required"] is False
        assert rollback["external_service_changes_required"] is False


def test_v1_g37_required_confirmations_are_true() -> None:
    for record in _records():
        confirmations = record["required_confirmations"]

        assert confirmations["no_lima_runtime_file_change_confirmation"] is True
        assert confirmations["no_consumer_repo_mutation_confirmation"] is True
        assert confirmations["no_consumer_runtime_source_change_confirmation"] is True
        assert confirmations["no_raw_patch_body_persistence_confirmation"] is True
        assert confirmations["no_patch_application_confirmation"] is True
        assert confirmations["no_adapter_symbol_call_confirmation"] is True
        assert confirmations["no_consumer_runtime_module_import_confirmation"] is True
        assert confirmations["no_consumer_integration_implementation_confirmation"] is True
        assert confirmations["no_shell_wiring_implementation_confirmation"] is True
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
        assert confirmations["proof_not_edit_authority_confirmation"] is True
        assert confirmations["proof_not_integration_authority_confirmation"] is True
        assert confirmations["proof_not_product_readiness_confirmation"] is True


def test_v1_g37_output_does_not_include_patch_bodies_imports_or_sensitive_markers() -> None:
    output = json.dumps(_load_fixture(), sort_keys=True)

    for forbidden in (
        "diff --git",
        "@@",
        "BEGIN PATCH",
        "raw patch body",
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


def test_v1_g37_docs_contain_boundary_language() -> None:
    implementation_text = (
        REPO_ROOT / "docs" / "V1_G37_CONSUMER_INTEGRATION_PATCH_PREVIEW.md"
    ).read_text(encoding="utf-8")
    closeout_text = (
        REPO_ROOT / "docs" / "V1_G37_CONSUMER_INTEGRATION_PATCH_PREVIEW_CLOSEOUT.md"
    ).read_text(encoding="utf-8")

    assert "metadata-only consumer integration patch-preview" in implementation_text
    assert "No Sparkbot or Arc-Bot-shell file" in implementation_text
    assert "No raw patch body" in implementation_text
    assert "No patch was applied" in closeout_text
    assert "proof-not-edit-authority" in closeout_text
    assert "proof-not-integration-authority" in closeout_text
    assert "No product-readiness or production-readiness claim" in closeout_text
    assert "V1-G37 is complete" in closeout_text
