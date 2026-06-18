"""Tests for the approved V1-G43 provider/model dispatch evidence slice."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g43_provider_model_dispatch.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _records() -> list[dict[str, Any]]:
    records = _load_fixture()["provider_model_dispatch_records"]
    assert isinstance(records, list)
    return records


def test_v1_g43_fixture_records_approved_scope_and_candidate_status() -> None:
    fixture = _load_fixture()

    assert fixture["packet_set_id"] == "v1_g43_provider_model_dispatch"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g43-provider-model-dispatch"
    assert fixture["operator_decision"] == "Approve-V1-G43"
    assert fixture["approved_scope"] == "provider_model_dispatch_slice"
    assert fixture["provider_model_dispatch_approved"] is True
    assert fixture["provider_model_dispatch_evidence_added"] is True
    assert fixture["static_fake_provider_no_secret_dispatch_evidence_added"] is True
    assert fixture["deterministic_fake_provider_dispatch_recorded"] is True
    assert fixture["bounded_provider_model_dispatch_evidence_only"] is True
    assert fixture["provider_model_dispatch_runtime_behavior_added"] is False
    assert fixture["actual_model_request_dispatch_execution_added"] is False
    assert fixture["product_ready"] is False


def test_v1_g43_lima_file_scope_is_exact_and_runtime_free() -> None:
    fixture = _load_fixture()

    assert fixture["approved_lima_files_changed"] == [
        "docs/V1_G43_PROVIDER_MODEL_DISPATCH.md",
        "docs/V1_G43_PROVIDER_MODEL_DISPATCH_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g43_provider_model_dispatch.json",
        "tests/test_v1_g43_provider_model_dispatch.py",
    ]
    assert all(not path.startswith("lima/") for path in fixture["approved_lima_files_changed"])
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["lima_docs_tests_fixtures_only"] is True


def test_v1_g43_has_no_consumer_file_scope() -> None:
    fixture = _load_fixture()

    assert fixture["approved_consumer_files_changed"] == {}
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["arc_bot_shell_files_changed"] is False
    assert fixture["consumer_repo_mutation_added"] is False
    assert fixture["consumer_runtime_source_files_changed"] is False

    for record in _records():
        assert record["rollback_metadata"]["rollback_consumer_file_refs"] == []


def test_v1_g43_links_request_and_prior_evidence_documents() -> None:
    fixture = _load_fixture()

    assert fixture["request_evidence_refs"] == [
        "docs/V1_G43_PROVIDER_MODEL_DISPATCH_APPROVAL_REQUEST.md",
        "docs/V1_G43_PROVIDER_MODEL_DISPATCH_WORK_ORDER.md",
        "docs/V1_G43_PROVIDER_MODEL_DISPATCH_OPERATOR_DECISION_PACKET.md",
        "docs/V1_G43_PROVIDER_MODEL_DISPATCH_PREFLIGHT_AUDIT.md",
    ]
    assert fixture["reviewed_prior_evidence_refs"] == [
        "docs/V1_G42_SHELL_WIRING_IMPLEMENTATION.md",
        "docs/V1_G42_SHELL_WIRING_IMPLEMENTATION_CLOSEOUT.md",
        "docs/audits/V1_G42_SHELL_WIRING_IMPLEMENTATION_AUDIT.md",
        "docs/audits/V1_RUNTIME_AUTHORITY_CHAIN_THROUGH_G42_AUDIT.md",
        "docs/readiness/V1_RUNTIME_READINESS_ROLLUP_THROUGH_G42.md",
        "docs/readiness/V1_POST_G42_NEXT_LANE_DECISION_MATRIX.md",
        "docs/V1_G20_PROVIDER_MODEL_ROUTING_AUTHORITY.md",
        "docs/V1_G20_PROVIDER_MODEL_ROUTING_AUTHORITY_CLOSEOUT.md",
        "docs/audits/V1_G20_PROVIDER_MODEL_ROUTING_AUTHORITY_AUDIT.md",
        "docs/audits/V1_RUNTIME_AUTHORITY_CHAIN_THROUGH_G20_AUDIT.md",
    ]

    for relative_path in (
        fixture["request_evidence_refs"] + fixture["reviewed_prior_evidence_refs"]
    ):
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g43_contains_one_static_fake_provider_dispatch_record() -> None:
    records = _records()

    assert len(records) == 1
    record = records[0]
    assert record["provider_model_dispatch_record_id"] == (
        "provider-model-dispatch:v1-g43:fake-provider:001"
    )
    assert record["dispatch_result"] == (
        "static_fake_provider_no_secret_dispatch_evidence_created"
    )
    assert record["provider_id"] == "provider:fake-local:no-key"
    assert record["model_id"] == "model:fake-local:no-network"
    assert record["provider_boundary_class"] == "fake_local_no_secret_no_network"
    assert record["dispatch_mode"] == "static_evidence_only"
    assert record["input_context_class"] == "redacted_summary_ref"
    assert record["output_context_class"] == "synthetic_response_summary_ref"
    assert record["source_provider_model_routing_authority_ref"] == "route:v1-g20:001"
    assert record["source_shell_wiring_record_refs"] == [
        "shell-wiring-implementation:v1-g42:sparkbot:001",
        "shell-wiring-implementation:v1-g42:arc-bot-shell:001",
    ]


def test_v1_g43_static_dispatch_hash_is_deterministic() -> None:
    record = _records()[0]

    expected_hash = hashlib.sha256(
        record["sanitized_dispatch_hash_source"].encode("utf-8")
    ).hexdigest()
    assert record["sanitized_dispatch_hash"] == f"sha256:{expected_hash}"
    assert record["sanitized_dispatch_hash_source"] == (
        "v1-g43-provider-model-dispatch:no-secret:fake-provider"
    )


def test_v1_g43_future_gates_remain_blocked() -> None:
    expected_gates = [
        "live_provider_model_call_approval_request",
        "secret_credential_access_approval_request",
        "fallback_execution_approval_request",
        "connector_browser_network_authority_approval_request",
        "physical_world_authority_approval_request",
        "product_readiness_approval_request",
    ]
    expected_blocked_authorities = {
        "live_provider_model_calls_approved": False,
        "actual_model_request_dispatch_execution_approved": False,
        "fallback_execution_approved": False,
        "secret_credential_access_approved": False,
        "connector_browser_network_authority_approved": False,
        "physical_world_authority_approved": False,
        "product_readiness_approved": False,
    }
    expected_gaps = [
        "live_provider_model_calls_not_approved",
        "actual_model_request_dispatch_execution_not_approved",
        "fallback_execution_not_approved",
        "secret_credential_access_not_approved",
        "connector_browser_network_authority_not_approved",
        "physical_world_authority_not_approved",
        "product_readiness_not_approved",
    ]
    fixture = _load_fixture()

    assert fixture["future_required_gates"] == expected_gates
    assert fixture["blocked_future_authorities"] == expected_blocked_authorities
    assert fixture["remaining_gaps"] == expected_gaps

    for record in _records():
        assert record["future_required_gates"] == expected_gates
        assert record["blocked_future_authorities"] == expected_blocked_authorities
        assert record["remaining_gaps"] == expected_gaps


def test_v1_g43_runtime_sensitive_and_external_boundaries_remain_false() -> None:
    fixture = _load_fixture()
    forbidden_keys = (
        "provider_model_dispatch_runtime_behavior_added",
        "actual_model_request_dispatch_execution_added",
        "live_provider_model_calls_added",
        "model_request_dispatch_added",
        "fallback_execution_added",
        "provider_readiness_network_check_added",
        "token_guardian_live_routing_added",
        "secret_lookup_added",
        "credential_access_added",
        "tool_execution_added",
        "lima_runtime_files_changed",
        "sparkbot_files_changed",
        "arc_bot_shell_files_changed",
        "consumer_repo_mutation_added",
        "consumer_runtime_source_files_changed",
        "raw_prompt_persisted",
        "raw_model_response_persisted",
        "raw_customer_data_persisted",
        "raw_secret_or_credential_persisted",
        "raw_patch_bodies_persisted",
        "raw_patch_bodies_persisted_in_lima_evidence",
        "unapproved_patches_applied",
        "adapter_symbols_called",
        "consumer_runtime_modules_imported",
        "runtime_shell_wiring_execution_added",
        "action_execution_added",
        "file_mutation_execution_added",
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
        assert record["model_request_dispatched"] is False
        assert record["fallback_executed"] is False
        assert record["secret_lookup_performed"] is False
        assert record["credential_accessed"] is False
        assert record["tool_executed"] is False
        assert record["product_ready"] is False


def test_v1_g43_rollback_metadata_is_exact_and_reversible() -> None:
    fixture = _load_fixture()
    expected_lima_files = fixture["approved_lima_files_changed"]

    for record in _records():
        rollback = record["rollback_metadata"]

        assert rollback["rollback_ref"] == "rollback:v1-g43:provider-model-dispatch"
        assert rollback["rollback_lima_file_refs"] == expected_lima_files
        assert rollback["rollback_consumer_file_refs"] == []
        assert rollback["runtime_source_repair_required"] is False
        assert rollback["consumer_runtime_source_repair_required"] is False
        assert rollback["shell_runtime_repair_required"] is False
        assert rollback["provider_configuration_changes_required"] is False
        assert rollback["credential_rotation_required"] is False
        assert rollback["external_service_changes_required"] is False


def test_v1_g43_required_confirmations_are_true() -> None:
    confirmations = _records()[0]["required_confirmations"]

    assert confirmations["provider_model_dispatch_approval_recorded_confirmation"] is True
    assert confirmations["no_lima_runtime_file_change_confirmation"] is True
    assert confirmations["no_consumer_repo_change_confirmation"] is True
    assert (
        confirmations["g20_provider_model_routing_authority_reference_only_confirmation"]
        is True
    )
    assert confirmations["g42_shell_wiring_reference_only_confirmation"] is True
    assert confirmations["deterministic_fake_provider_no_secret_confirmation"] is True
    assert confirmations["no_live_provider_model_call_confirmation"] is True
    assert confirmations["no_actual_model_request_dispatch_execution_confirmation"] is True
    assert confirmations["no_fallback_execution_confirmation"] is True
    assert confirmations["no_provider_readiness_network_check_confirmation"] is True
    assert confirmations["no_token_guardian_live_routing_confirmation"] is True
    assert confirmations["no_secret_lookup_confirmation"] is True
    assert confirmations["no_credential_access_confirmation"] is True
    assert confirmations["no_tool_execution_confirmation"] is True
    assert confirmations["no_adapter_symbol_call_confirmation"] is True
    assert confirmations["no_consumer_runtime_module_import_confirmation"] is True
    assert confirmations["no_runtime_shell_wiring_execution_confirmation"] is True
    assert confirmations["no_connector_browser_network_physical_world_confirmation"] is True
    assert confirmations["no_raw_sensitive_content_in_lima_evidence_confirmation"] is True
    assert confirmations["proof_not_live_provider_authority_confirmation"] is True
    assert confirmations["proof_not_secret_authority_confirmation"] is True
    assert confirmations["proof_not_product_readiness_confirmation"] is True


def test_v1_g43_output_does_not_include_patch_imports_or_sensitive_markers() -> None:
    output = json.dumps(_load_fixture(), sort_keys=True)

    for forbidden in (
        "diff --git",
        "@@",
        "BEGIN PATCH",
        "raw patch body",
        "raw prompt value",
        "raw model response value",
        "raw customer data value",
        "provider token value",
        "api key value",
        "raw-secret-123",
        "def test_",
        "import lima",
        "from lima",
    ):
        assert forbidden not in output


def test_v1_g43_docs_contain_boundary_language() -> None:
    implementation_text = (
        REPO_ROOT / "docs" / "V1_G43_PROVIDER_MODEL_DISPATCH.md"
    ).read_text(encoding="utf-8")
    closeout_text = (
        REPO_ROOT / "docs" / "V1_G43_PROVIDER_MODEL_DISPATCH_CLOSEOUT.md"
    ).read_text(encoding="utf-8")

    assert "approved bounded provider/model dispatch evidence slice" in implementation_text
    assert "fake-provider/no-secret/no-network dispatch record" in implementation_text
    assert "does not approve live provider/model calls" in implementation_text
    assert "No `lima/` runtime file" in implementation_text
    assert "proof-not-live-provider-authority" in closeout_text
    assert "proof-not-secret-authority" in closeout_text
    assert "No product-readiness or production-readiness claim" in closeout_text
    assert "V1-G43 is complete" in closeout_text
