"""Tests for the approved V1-G40 shell wiring design slice."""

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
    / "v1_g40_shell_wiring_design.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _records() -> list[dict[str, Any]]:
    records = _load_fixture()["shell_boundary_records"]
    assert isinstance(records, list)
    return records


def test_v1_g40_fixture_records_approved_scope_and_candidate_status() -> None:
    fixture = _load_fixture()

    assert fixture["packet_set_id"] == "v1_g40_shell_wiring_design"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g40-shell-wiring-design"
    assert fixture["operator_decision"] == "Approve-V1-G40"
    assert fixture["approved_scope"] == "shell_wiring_design_slice"
    assert fixture["shell_wiring_design_approved"] is True
    assert fixture["shell_wiring_design_added"] is True
    assert fixture["metadata_only_shell_boundary_maps_added"] is True
    assert fixture["shell_wiring_implementation_approved"] is False
    assert fixture["shell_runtime_wiring_implementation_added"] is False
    assert fixture["consumer_integration_implementation_approved"] is False
    assert fixture["consumer_integration_implementation_added"] is False
    assert fixture["product_ready"] is False


def test_v1_g40_lima_file_scope_is_exact_and_runtime_free() -> None:
    fixture = _load_fixture()

    assert fixture["approved_lima_files_changed"] == [
        "docs/V1_G40_SHELL_WIRING_DESIGN.md",
        "docs/V1_G40_SHELL_WIRING_DESIGN_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g40_shell_wiring_design.json",
        "tests/test_v1_g40_shell_wiring_design.py",
    ]
    assert all(not path.startswith("lima/") for path in fixture["approved_lima_files_changed"])
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["lima_docs_tests_fixtures_only"] is True


def test_v1_g40_consumer_file_scope_is_empty() -> None:
    fixture = _load_fixture()

    assert fixture["approved_consumer_files_changed"] == {
        "sparkbot": [],
        "arc_bot": [],
    }
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["arc_bot_shell_files_changed"] is False
    assert fixture["consumer_repo_mutation_added"] is False
    assert fixture["consumer_runtime_source_files_changed"] is False

    for record in _records():
        assert record["rollback_metadata"]["rollback_consumer_file_refs"] == []
        assert record["consumer_runtime_source_files_changed"] is False


def test_v1_g40_contains_exactly_two_shell_boundary_records() -> None:
    records = _records()

    assert [record["consumer_packet_family"] for record in records] == [
        "sparkbot",
        "arc_bot",
    ]
    assert [record["consumer_name"] for record in records] == [
        "Sparkbot",
        "Arc-Bot-shell",
    ]


def test_v1_g40_records_shell_boundary_maps_and_source_refs() -> None:
    expected = {
        "sparkbot": (
            "sparkpit-labs/Sparkbot",
            "sparkbot_product_shell_boundary",
            "consumer-integration-import-smoke:v1-g39:sparkbot:001",
            "consumer-repository-edit:v1-g38:sparkbot:001",
            "shell-boundary-map:v1-g40:sparkbot",
        ),
        "arc_bot": (
            "armpit-symphony/Arc-Bot-shell",
            "arc_office_shell_boundary",
            "consumer-integration-import-smoke:v1-g39:arc-bot-shell:001",
            "consumer-repository-edit:v1-g38:arc-bot-shell:001",
            "shell-boundary-map:v1-g40:arc-bot-shell",
        ),
    }

    for record in _records():
        repository, role, import_ref, edit_ref, map_ref = expected[
            record["consumer_packet_family"]
        ]
        boundary_map = record["proposed_shell_boundary_map"]

        assert record["shell_boundary_record_id"].startswith(
            "shell-wiring-design:v1-g40:"
        )
        assert record["consumer_repository"] == repository
        assert record["shell_boundary_role"] == role
        assert record["source_import_smoke_record_ref"] == import_ref
        assert record["source_repository_edit_record_ref"] == edit_ref
        assert record["shell_wiring_design_result"] == (
            "metadata_only_shell_boundary_map_created"
        )
        assert boundary_map["boundary_map_ref"] == map_ref
        assert boundary_map["metadata_only"] is True
        assert boundary_map["runtime_wiring_added"] is False
        assert boundary_map["grants_execution_authority"] is False


def test_v1_g40_boundary_maps_require_guardian_and_block_direct_paths() -> None:
    expected_contract_refs = [
        "guardian.syscall_gate",
        "harness.model_route_request",
        "spine.audit_evidence",
        "approval.evidence_capture",
    ]
    expected_decision_points = [
        "request_intake_classification",
        "tool_pack_scope_check",
        "approval_requirement_check",
        "audit_evidence_write",
    ]
    expected_blocked_paths = [
        "direct_provider_dispatch",
        "direct_tool_execution",
        "direct_file_mutation",
        "direct_connector_call",
        "direct_browser_network_action",
        "direct_physical_world_action",
    ]

    for record in _records():
        boundary_map = record["proposed_shell_boundary_map"]

        assert boundary_map["future_lima_contract_refs"] == expected_contract_refs
        assert boundary_map["required_guardian_decision_points"] == expected_decision_points
        assert boundary_map["blocked_runtime_paths"] == expected_blocked_paths
        assert len(boundary_map["shell_surface_refs"]) == 4


def test_v1_g40_design_result_and_remaining_gaps_are_locked() -> None:
    expected_gaps = [
        "consumer_integration_implementation_not_approved",
        "shell_wiring_implementation_not_approved",
        "provider_model_dispatch_not_approved",
        "secret_credential_access_not_approved",
        "connector_browser_network_authority_not_approved",
        "physical_world_authority_not_approved",
        "product_readiness_not_approved",
    ]

    assert _load_fixture()["remaining_gaps"] == expected_gaps
    for record in _records():
        assert record["shell_wiring_design_approved"] is True
        assert record["shell_wiring_design_added"] is True
        assert record["metadata_only_shell_boundary_map_added"] is True
        assert record["remaining_gaps"] == expected_gaps
        assert record["shell_wiring_implementation_approved"] is False
        assert record["shell_runtime_wiring_implementation_added"] is False
        assert record["consumer_integration_implementation_approved"] is False
        assert record["consumer_integration_implementation_added"] is False
        assert record["consumer_integration_added"] is False
        assert record["proof_not_shell_wiring_implementation"] is True
        assert record["proof_not_integration_authority"] is True
        assert record["proof_not_product_readiness"] is True
        assert record["product_ready"] is False


def test_v1_g40_future_gates_remain_blocked() -> None:
    expected_gates = [
        "consumer_integration_implementation_approval_request",
        "shell_wiring_implementation_approval_request",
        "provider_model_dispatch_approval_request",
        "connector_browser_network_authority_approval_request",
        "physical_world_authority_approval_request",
        "product_readiness_approval_request",
    ]
    expected_blocked_authorities = {
        "consumer_integration_implementation_approved": False,
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


def test_v1_g40_links_required_prior_evidence_documents() -> None:
    fixture = _load_fixture()

    assert fixture["reviewed_evidence_refs"] == [
        "docs/V1_G39_CONSUMER_INTEGRATION_IMPORT_SMOKE.md",
        "docs/V1_G39_CONSUMER_INTEGRATION_IMPORT_SMOKE_CLOSEOUT.md",
        "docs/audits/V1_G39_CONSUMER_INTEGRATION_IMPORT_SMOKE_AUDIT.md",
        "docs/audits/V1_RUNTIME_AUTHORITY_CHAIN_THROUGH_G39_AUDIT.md",
        "docs/readiness/V1_RUNTIME_READINESS_ROLLUP_THROUGH_G39.md",
        "docs/readiness/V1_POST_G39_NEXT_LANE_DECISION_MATRIX.md",
    ]

    for relative_path in fixture["reviewed_evidence_refs"]:
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g40_runtime_patch_and_external_boundaries_remain_false() -> None:
    fixture = _load_fixture()

    forbidden_keys = (
        "lima_runtime_files_changed",
        "sparkbot_files_changed",
        "arc_bot_shell_files_changed",
        "consumer_repo_mutation_added",
        "consumer_runtime_source_files_changed",
        "raw_patch_bodies_persisted",
        "raw_patch_bodies_persisted_in_lima_evidence",
        "unapproved_patches_applied",
        "adapter_symbols_called",
        "consumer_runtime_modules_imported",
        "consumer_integration_added",
        "consumer_integration_implementation_added",
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
        assert record["product_ready"] is False


def test_v1_g40_rollback_metadata_is_exact_and_reversible() -> None:
    fixture = _load_fixture()
    expected_lima_files = fixture["approved_lima_files_changed"]

    for record in _records():
        rollback = record["rollback_metadata"]

        assert rollback["rollback_ref"].startswith("rollback:v1-g40:")
        assert rollback["rollback_lima_file_refs"] == expected_lima_files
        assert rollback["rollback_consumer_file_refs"] == []
        assert rollback["runtime_source_repair_required"] is False
        assert rollback["consumer_repository_repair_required"] is False
        assert rollback["consumer_runtime_source_repair_required"] is False
        assert rollback["shell_runtime_repair_required"] is False
        assert rollback["external_service_changes_required"] is False


def test_v1_g40_required_confirmations_are_true() -> None:
    for record in _records():
        confirmations = record["required_confirmations"]

        assert confirmations["shell_wiring_design_approval_recorded_confirmation"] is True
        assert confirmations["no_lima_runtime_file_change_confirmation"] is True
        assert confirmations["no_consumer_repo_mutation_confirmation"] is True
        assert confirmations["no_consumer_runtime_source_change_confirmation"] is True
        assert confirmations["no_raw_patch_body_persistence_confirmation"] is True
        assert confirmations["no_unapproved_patch_application_confirmation"] is True
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
        assert confirmations["proof_not_shell_wiring_implementation_confirmation"] is True
        assert confirmations["proof_not_integration_authority_confirmation"] is True
        assert confirmations["proof_not_product_readiness_confirmation"] is True


def test_v1_g40_output_does_not_include_patch_bodies_imports_or_sensitive_markers() -> None:
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


def test_v1_g40_docs_contain_boundary_language() -> None:
    implementation_text = (
        REPO_ROOT / "docs" / "V1_G40_SHELL_WIRING_DESIGN.md"
    ).read_text(encoding="utf-8")
    closeout_text = (
        REPO_ROOT / "docs" / "V1_G40_SHELL_WIRING_DESIGN_CLOSEOUT.md"
    ).read_text(encoding="utf-8")

    assert "approved LIMA-side shell wiring design slice" in implementation_text
    assert "No `lima/` runtime file" in implementation_text
    assert "does not approve shell runtime wiring implementation" in implementation_text
    assert "proof-not-shell-wiring-implementation" in closeout_text
    assert "proof-not-integration-authority" in closeout_text
    assert "No product-readiness or production-readiness claim" in closeout_text
    assert "V1-G40 is complete" in closeout_text
