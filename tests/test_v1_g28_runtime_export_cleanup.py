"""Tests for the approved V1-G28 runtime export cleanup slice."""

from __future__ import annotations

import importlib
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g28_runtime_export_cleanup.json"
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


def test_v1_g28_fixture_records_approved_scope_and_boundaries() -> None:
    fixture = _load_fixture()

    assert fixture["packet_set_id"] == "v1_g28_runtime_export_cleanup"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g28-runtime-export-cleanup"
    assert fixture["operator_decision"] == "Approve-V1-G28"
    assert fixture["approved_scope"] == "runtime_export_cleanup_slice"
    assert fixture["runtime_export_cleanup_approved"] is True
    assert fixture["runtime_export_cleanup_added"] is True
    assert fixture["lima_runtime_files_changed"] is True
    assert fixture["product_ready"] is False


def test_v1_g28_file_scope_is_exact() -> None:
    fixture = _load_fixture()

    assert fixture["approved_runtime_files_changed"] == ["lima/adapters/__init__.py"]
    assert set(fixture["approved_docs_tests_fixtures_changed"]) == {
        "docs/V1_G28_RUNTIME_EXPORT_CLEANUP.md",
        "docs/V1_G28_RUNTIME_EXPORT_CLEANUP_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g28_runtime_export_cleanup.json",
        "tests/test_v1_g28_runtime_export_cleanup.py",
        "tests/fixtures/runtime_extraction/v1_g22_final_public_api_freeze.json",
    }


def test_v1_g28_adapter_all_exports_match_cleanup_fixture() -> None:
    fixture = _load_fixture()
    adapters = importlib.import_module("lima.adapters")

    assert list(getattr(adapters, "__all__")) == fixture["post_cleanup_adapter_all_exports"]


def test_v1_g28_existing_frozen_adapter_exports_are_preserved() -> None:
    fixture = _load_fixture()
    adapters = importlib.import_module("lima.adapters")
    exports = set(getattr(adapters, "__all__"))

    for symbol_name in fixture["previous_frozen_adapter_exports"]:
        assert symbol_name in exports
        assert hasattr(adapters, symbol_name), symbol_name

    assert fixture["existing_frozen_adapter_exports_preserved"] is True
    assert fixture["existing_frozen_adapter_exports_removed"] is False
    assert fixture["existing_frozen_adapter_exports_renamed"] is False


def test_v1_g28_dry_run_symbols_are_now_explicit_adapter_exports() -> None:
    fixture = _load_fixture()
    adapters = importlib.import_module("lima.adapters")
    exports = set(getattr(adapters, "__all__"))

    for symbol_name in fixture["added_adapter_exports"]:
        assert symbol_name in exports
        assert hasattr(adapters, symbol_name), symbol_name


def test_v1_g28_g22_freeze_fixture_reflects_cleanup_exports() -> None:
    fixture = _load_fixture()
    g22 = _load_g22_fixture()

    assert (
        g22["public_subpackage_export_surfaces"]["lima.adapters"]
        == fixture["post_cleanup_adapter_all_exports"]
    )
    assert fixture["g22_final_public_api_freeze_fixture_refreshed"] is True


def test_v1_g28_no_unapproved_runtime_behavior_or_consumer_changes() -> None:
    fixture = _load_fixture()

    for key in (
        "validator_behavior_changed",
        "new_validator_added",
        "consumer_repo_mutation_added",
        "sparkbot_files_changed",
        "arc_bot_shell_files_changed",
        "consumer_runtime_calls_added",
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
    ):
        assert fixture[key] is False


def test_v1_g28_evidence_refs_exist() -> None:
    fixture = _load_fixture()

    for relative_path in fixture["accepted_evidence_refs"]:
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g28_consumer_validation_metadata_is_test_only() -> None:
    metadata = _load_fixture()["consumer_validation_metadata"]

    assert metadata["sparkbot_result"] == "7 passed"
    assert metadata["arc_bot_shell_result"] == "7 passed"
    assert metadata["consumer_repo_edits_required"] is False
    assert metadata["live_runtime_required"] is False
    assert metadata["external_services_required"] is False


def test_v1_g28_rollback_metadata_is_local_and_reversible() -> None:
    rollback = _load_fixture()["rollback_metadata"]

    assert rollback["rollback_ref"] == "rollback:v1-g28:runtime-export-cleanup"
    assert rollback["rollback_runtime_file_refs"] == ["lima/adapters/__init__.py"]
    assert rollback["rollback_fixture_refs"] == [
        "tests/fixtures/runtime_extraction/v1_g22_final_public_api_freeze.json"
    ]
    assert rollback["consumer_repo_changes_required"] is False
    assert rollback["external_service_changes_required"] is False


def test_v1_g28_required_confirmations_are_true() -> None:
    confirmations = _load_fixture()["required_confirmations"]

    assert confirmations["no_validator_behavior_change_confirmation"] is True
    assert confirmations["no_consumer_repo_mutation_confirmation"] is True
    assert confirmations["no_live_import_call_confirmation"] is True
    assert (
        confirmations[
            "no_provider_model_secret_credential_connector_browser_network_physical_world_confirmation"
        ]
        is True
    )
    assert confirmations["proof_not_authority_confirmation"] is True


def test_v1_g28_output_does_not_include_patch_bodies_or_sensitive_markers() -> None:
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


def test_v1_g28_docs_contain_boundary_language() -> None:
    implementation_text = (
        REPO_ROOT / "docs" / "V1_G28_RUNTIME_EXPORT_CLEANUP.md"
    ).read_text(encoding="utf-8")
    closeout_text = (
        REPO_ROOT / "docs" / "V1_G28_RUNTIME_EXPORT_CLEANUP_CLOSEOUT.md"
    ).read_text(encoding="utf-8")

    assert "No other runtime file" in implementation_text
    assert "No Sparkbot or Arc-Bot-shell file" in implementation_text
    assert "Validator behavior changed: no" in implementation_text
    assert "V1-G28 is complete" in closeout_text
