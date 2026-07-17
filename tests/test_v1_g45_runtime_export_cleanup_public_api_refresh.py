"""Tests for the approved V1-G45 runtime export cleanup public API refresh."""

from __future__ import annotations

import importlib
import json
from pathlib import Path
from typing import Any

from lima.harness import validate_v1_live_provider_model_call_authority


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g45_runtime_export_cleanup_public_api_refresh.json"
)
G22_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g22_final_public_api_freeze.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _load_g22_fixture() -> dict[str, Any]:
    fixture = json.loads(G22_FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _authority_metadata(**overrides: Any) -> dict[str, Any]:
    record = {
        "authority_id": "authority:v1-g44:001",
        "request_or_guardian_decision_linkage": {
            "request_id": "request:v1-g44:001",
            "guardian_decision_id": "decision:v1-g44:001",
            "linkage_required": True,
            "proof_not_execution": True,
            "grants_execution_authority": False,
        },
        "tenant_scope": "tenant:alpha",
        "shell_scope": "shell:sparkbot-shell",
        "actor_scope": "actor:user-123",
        "session_scope": "session:local",
        "source_provider_model_route_authority_ref": "route:v1-g20:001",
        "source_provider_model_dispatch_evidence_ref": (
            "provider-model-dispatch:v1-g43:fake-provider:001"
        ),
        "provider_id": "provider:openai:metadata-ref",
        "model_id": "model:gpt-class",
        "model_role": "primary",
        "provider_boundary_metadata": {
            "provider_boundary_ref": "provider-boundary:v1-g44:openai",
            "provider_class": "hosted_api_metadata",
            "provider_configured_for_scope": True,
            "live_provider_call_authority_policy_bound": True,
            "live_provider_call_execution_allowed": False,
            "provider_readiness_network_check_allowed": False,
            "token_guardian_live_routing_allowed": False,
            "proof_not_execution": True,
        },
        "credential_reference_metadata": {
            "credential_ref": "vault-ref:metadata/openai-live-call",
            "provider_is_no_key_local": False,
            "reference_only": True,
            "secret_lookup_performed": False,
            "credential_value_accessed": False,
            "raw_secret_present": False,
            "credential_value_present": False,
            "provider_token_present": False,
        },
        "network_policy_reference_metadata": {
            "network_policy_ref": "network-policy:v1-g44:provider-egress",
            "reference_only": True,
            "network_scope_bound": True,
            "network_call_performed": False,
            "provider_endpoint_resolution_performed": False,
            "proof_not_execution": True,
        },
        "prompt_reference_metadata": {
            "prompt_ref": "prompt-ref:v1-g44:redacted-summary",
            "prompt_context_class": "redacted_summary",
            "reference_only": True,
            "redacted": True,
            "raw_prompt_present": False,
            "raw_customer_data_present": False,
        },
        "output_handling_policy": {
            "output_policy_ref": "output-policy:v1-g44:redacted",
            "audit_output_ref": "audit-output:v1-g44:redacted-summary",
            "redacted_output_required": True,
            "raw_model_response_present": False,
            "persist_raw_model_response": False,
            "proof_not_execution": True,
        },
        "data_sensitivity": "internal",
        "budget_class": "medium",
        "estimated_cost_class": "low",
        "latency_tier": "interactive",
        "approval_evidence_linkage": {
            "approval_required_by_policy": True,
            "approval_evidence_ref": "approval-evidence:v1-g44:001",
            "approval_evidence_current": True,
            "proof_not_execution": True,
            "grants_execution_authority": False,
        },
        "audit_evidence_linkage": {
            "audit_record_ref": "audit:v1-g44:live-provider-call-authority",
            "evidence_refs": [
                "route:v1-g20:001",
                "provider-model-dispatch:v1-g43:fake-provider:001",
            ],
            "required": True,
            "proof_not_execution": True,
        },
        "proof_not_execution_confirmation": True,
        "no_raw_prompt_model_response_customer_data_confirmation": True,
        "no_secret_lookup_confirmation": True,
        "no_credential_value_access_confirmation": True,
        "no_network_call_confirmation": True,
        "no_live_provider_call_execution_confirmation": True,
        "no_fallback_execution_confirmation": True,
    }
    record.update(overrides)
    return record


def test_v1_g45_fixture_records_approved_scope_and_boundaries() -> None:
    fixture = _load_fixture()

    assert fixture["packet_set_id"] == (
        "v1_g45_runtime_export_cleanup_public_api_refresh"
    )
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g45-runtime-export-cleanup-public-api-refresh"
    assert fixture["operator_decision"] == "Approve-V1-G45"
    assert fixture["approved_scope"] == (
        "runtime_export_cleanup_public_api_refresh_slice"
    )
    assert fixture["runtime_export_cleanup_public_api_refresh_approved"] is True
    assert fixture["runtime_export_cleanup_public_api_refresh_added"] is True
    assert fixture["lima_runtime_files_changed"] is True
    assert fixture["product_ready"] is False


def test_v1_g45_file_scope_is_exact() -> None:
    fixture = _load_fixture()

    assert fixture["approved_runtime_files_changed"] == ["lima/harness/__init__.py"]
    assert set(fixture["approved_docs_tests_fixtures_changed"]) == {
        "docs/V1_G45_RUNTIME_EXPORT_CLEANUP_PUBLIC_API_REFRESH.md",
        "docs/V1_G45_RUNTIME_EXPORT_CLEANUP_PUBLIC_API_REFRESH_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g45_runtime_export_cleanup_public_api_refresh.json",
        "tests/test_v1_g45_runtime_export_cleanup_public_api_refresh.py",
        "tests/fixtures/runtime_extraction/v1_g22_final_public_api_freeze.json",
    }
    assert fixture["cleanup_target"] == {
        "package": "lima.harness",
        "runtime_file": "lima/harness/__init__.py",
        "export_surface": "lima.harness.__all__",
        "source_existing_validator_module": (
            "lima/harness/v1_live_provider_model_call_authority.py"
        ),
    }


def test_v1_g45_harness_all_exports_match_refresh_fixture() -> None:
    fixture = _load_fixture()
    harness = importlib.import_module("lima.harness")
    expected_exports = fixture["post_refresh_harness_all_exports"]
    actual_exports = list(getattr(harness, "__all__"))

    assert actual_exports[: len(expected_exports)] == expected_exports


def test_v1_g45_existing_frozen_harness_exports_are_preserved() -> None:
    fixture = _load_fixture()
    harness = importlib.import_module("lima.harness")
    exports = set(getattr(harness, "__all__"))

    for symbol_name in fixture["previous_frozen_harness_exports"]:
        assert symbol_name in exports
        assert hasattr(harness, symbol_name), symbol_name

    assert fixture["existing_frozen_harness_exports_preserved"] is True
    assert fixture["existing_frozen_harness_exports_removed"] is False
    assert fixture["existing_frozen_harness_exports_renamed"] is False


def test_v1_g45_g44_symbols_are_now_explicit_harness_exports() -> None:
    fixture = _load_fixture()
    harness = importlib.import_module("lima.harness")
    exports = set(getattr(harness, "__all__"))

    assert fixture["added_harness_exports"] == [
        "V1LiveProviderModelCallAuthorityError",
        "validate_v1_live_provider_model_call_authority",
    ]
    for symbol_name in fixture["added_harness_exports"]:
        assert symbol_name in exports
        assert hasattr(harness, symbol_name), symbol_name


def test_v1_g45_g22_freeze_fixture_reflects_refresh_exports() -> None:
    fixture = _load_fixture()
    g22 = _load_g22_fixture()
    expected_exports = fixture["post_refresh_harness_all_exports"]
    actual_exports = g22["public_subpackage_export_surfaces"]["lima.harness"]

    assert actual_exports[: len(expected_exports)] == expected_exports
    assert fixture["g22_final_public_api_freeze_fixture_refreshed"] is True


def test_v1_g45_g22_runtime_symbol_inventory_is_not_expanded() -> None:
    g22 = _load_g22_fixture()

    gates = {entry["gate"] for entry in g22["v1_runtime_symbol_surfaces"]}
    assert "V1-G44" not in gates


def test_v1_g45_public_harness_import_preserves_g44_validator_behavior() -> None:
    record = validate_v1_live_provider_model_call_authority(_authority_metadata())

    assert record["record_type"] == "v1_live_provider_model_call_authority"
    assert record["schema_version"] == "v1-g44-candidate"
    assert record["authority_id"] == "authority:v1-g44:001"
    assert record["proof_not_execution"] is True
    assert record["non_executing"] is True
    assert record["authority_preflight_metadata_only"] is True
    assert record["live_provider_model_call_execution_added"] is False
    assert record["actual_model_request_dispatch_execution_added"] is False
    assert record["model_request_dispatched"] is False
    assert record["network_call_added"] is False
    assert record["secret_lookup_added"] is False
    assert record["credential_value_access_added"] is False
    assert record["fallback_execution_added"] is False
    assert record["tool_executed"] is False
    assert record["consumer_integration_added"] is False
    assert record["physical_world_invoked"] is False
    assert record["product_ready"] is False


def test_v1_g45_no_unapproved_runtime_behavior_or_consumer_changes() -> None:
    fixture = _load_fixture()

    for key in (
        "validator_behavior_changed",
        "new_validator_added",
        "g44_validator_module_changed",
        "g20_validator_module_changed",
        "consumer_repo_mutation_added",
        "sparkbot_files_changed",
        "arc_bot_shell_files_changed",
        "consumer_runtime_calls_added",
        "consumer_integration_added",
        "shell_runtime_wiring_added",
        "live_provider_model_call_execution_added",
        "actual_model_request_dispatch_execution_added",
        "network_call_added",
        "provider_readiness_network_check_added",
        "token_guardian_live_routing_added",
        "secret_lookup_added",
        "credential_value_access_added",
        "fallback_execution_added",
        "tool_execution_added",
        "action_execution_added",
        "connector_browser_network_file_device_robotics_physical_world_behavior_added",
        "raw_diff_or_patch_persisted",
        "raw_file_content_persisted",
        "raw_prompt_model_response_customer_data_persisted",
        "credential_or_secret_persisted",
    ):
        assert fixture[key] is False


def test_v1_g45_evidence_refs_exist() -> None:
    fixture = _load_fixture()

    for relative_path in fixture["accepted_evidence_refs"]:
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g45_rollback_metadata_is_local_and_reversible() -> None:
    rollback = _load_fixture()["rollback_metadata"]

    assert rollback["rollback_ref"] == (
        "rollback:v1-g45:runtime-export-cleanup-public-api-refresh"
    )
    assert rollback["rollback_runtime_file_refs"] == ["lima/harness/__init__.py"]
    assert rollback["rollback_fixture_refs"] == [
        "tests/fixtures/runtime_extraction/v1_g22_final_public_api_freeze.json"
    ]
    assert rollback["consumer_repo_changes_required"] is False
    assert rollback["external_service_changes_required"] is False
    assert rollback["provider_configuration_changes_required"] is False
    assert rollback["credential_rotation_required"] is False


def test_v1_g45_required_confirmations_are_true() -> None:
    confirmations = _load_fixture()["required_confirmations"]

    assert confirmations["no_validator_behavior_change_confirmation"] is True
    assert confirmations["no_consumer_repo_mutation_confirmation"] is True
    assert confirmations["no_live_provider_model_execution_confirmation"] is True
    assert (
        confirmations[
            "no_network_secret_credential_fallback_tool_connector_physical_world_confirmation"
        ]
        is True
    )
    assert (
        confirmations[
            "no_raw_content_secret_credential_customer_data_patch_persistence_confirmation"
        ]
        is True
    )
    assert confirmations["proof_not_authority_confirmation"] is True


def test_v1_g45_output_does_not_include_patch_bodies_or_sensitive_markers() -> None:
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


def test_v1_g45_docs_contain_boundary_language() -> None:
    implementation_text = (
        REPO_ROOT / "docs" / "V1_G45_RUNTIME_EXPORT_CLEANUP_PUBLIC_API_REFRESH.md"
    ).read_text(encoding="utf-8")
    closeout_text = (
        REPO_ROOT
        / "docs"
        / "V1_G45_RUNTIME_EXPORT_CLEANUP_PUBLIC_API_REFRESH_CLOSEOUT.md"
    ).read_text(encoding="utf-8")

    assert "No other runtime file" in implementation_text
    assert "No Sparkbot or Arc-Bot-shell file" in implementation_text
    assert "Validator behavior changed: no" in implementation_text
    assert "live provider/model call execution: not approved" in implementation_text
    assert "V1-G45 is complete" in closeout_text
    assert "No product-readiness or production-readiness claim" in closeout_text
