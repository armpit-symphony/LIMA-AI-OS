"""Static checks for the V1-G28 runtime export cleanup request."""

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
    / "v1_g28_runtime_export_cleanup_approval_request.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g28_request_docs_and_fixture_exist() -> None:
    fixture = _load_fixture()

    assert fixture["gate_id"] == "v1_g28_runtime_export_cleanup_approval_request"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "prepare-v1-g28-runtime-export-cleanup-approval-request"

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g28_has_no_implementation_approval_yet() -> None:
    fixture = _load_fixture()
    decision = fixture["decision_record"]

    assert fixture["implementation_approved"] is False
    assert fixture["operator_approval_recorded"] is False
    assert fixture["runtime_export_cleanup_approved"] is False
    assert fixture["runtime_export_cleanup_added"] is False
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["consumer_repo_mutation_added"] is False
    assert decision["recorded_choice"] == "none"
    assert decision["approved_implementation_branch"] == "none"
    assert decision["implementation_approved"] is False


def test_v1_g28_exact_decision_options_are_locked() -> None:
    fixture = _load_fixture()

    assert fixture["valid_operator_choices"] == [
        "Approve-V1-G28",
        "Revise-V1-G28",
        "Pause",
    ]
    assert fixture["required_approval_wording"].startswith(
        "I explicitly approve V1-G28 implementation"
    )
    assert fixture["proposed_implementation_branch"] == "v1-g28-runtime-export-cleanup"


def test_v1_g28_cleanup_target_is_exact() -> None:
    target = _load_fixture()["cleanup_target_if_operator_says_yes"]

    assert target["package"] == "lima.adapters"
    assert target["runtime_file"] == "lima/adapters/__init__.py"
    assert target["export_surface"] == "lima.adapters.__all__"
    assert target["symbols_to_add_to_all"] == [
        "V1ConsumerImportDryRunError",
        "validate_v1_consumer_integration_proof_to_import_dry_run",
    ]
    assert target["symbol_removal_allowed"] is False
    assert target["symbol_rename_allowed"] is False
    assert target["validator_behavior_change_allowed"] is False
    assert target["consumer_repo_edits_allowed"] is False
    assert target["live_runtime_calls_allowed"] is False


def test_v1_g28_existing_frozen_exports_must_be_preserved() -> None:
    target = _load_fixture()["cleanup_target_if_operator_says_yes"]

    assert target["required_existing_symbols_to_preserve"] == [
        "SparkbotChatInputPayload",
        "SparkbotHumanInputAdapter",
        "SparkbotMeetingInputPayload",
        "SparkbotOperatorInputPayload",
        "SparkbotVoiceInputPayload",
        "V1ConsumerIntegrationCompatibilityError",
        "validate_v1_consumer_integration_compatibility_freeze",
    ]


def test_v1_g28_approved_file_scope_is_exact() -> None:
    fixture = _load_fixture()

    assert fixture["approved_lima_runtime_files_if_operator_says_yes"] == [
        "lima/adapters/__init__.py"
    ]
    assert set(fixture["approved_lima_docs_tests_fixtures_if_operator_says_yes"]) == {
        "docs/V1_G28_RUNTIME_EXPORT_CLEANUP.md",
        "docs/V1_G28_RUNTIME_EXPORT_CLEANUP_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g28_runtime_export_cleanup.json",
        "tests/test_v1_g28_runtime_export_cleanup.py",
        "tests/fixtures/runtime_extraction/v1_g22_final_public_api_freeze.json",
    }
    assert fixture["approved_consumer_files_if_operator_says_yes"] == []


def test_v1_g28_prior_evidence_refs_exist() -> None:
    fixture = _load_fixture()

    for relative_path in fixture["required_prior_evidence_refs"]:
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g28_forbidden_runtime_and_external_boundaries_remain_false() -> None:
    fixture = _load_fixture()

    assert fixture["consumer_runtime_calls_added"] is False
    assert fixture["consumer_integration_added"] is False
    assert fixture["shell_runtime_wiring_added"] is False
    assert fixture["provider_model_calls_added"] is False
    assert fixture["secret_lookup_added"] is False
    assert fixture["credential_access_added"] is False
    assert fixture["tool_execution_added"] is False
    assert fixture[
        "connector_browser_network_file_device_robotics_physical_world_behavior_added"
    ] is False
    assert fixture["raw_diff_or_patch_persisted"] is False
    assert fixture["raw_file_content_persisted"] is False
    assert fixture["product_ready"] is False


def test_v1_g28_docs_contain_cleanup_boundary_language() -> None:
    fixture = _load_fixture()
    approval_text = (REPO_ROOT / fixture["documents"]["approval_request"]).read_text(
        encoding="utf-8"
    )
    decision_text = (REPO_ROOT / fixture["documents"]["operator_decision_packet"]).read_text(
        encoding="utf-8"
    )
    preflight_text = (REPO_ROOT / fixture["documents"]["preflight_audit"]).read_text(
        encoding="utf-8"
    )

    assert "Approved cleanup target" in approval_text
    assert "must not add a new validator" in approval_text
    assert "No Sparkbot or Arc-Bot-shell files" in approval_text
    assert "Runtime export cleanup approved: no" in approval_text
    assert "Recorded choice: none" in decision_text
    assert "Recorded choice: Approve-V1-G28" in decision_text
    assert "Implementation must not start until `Approve-V1-G28`" in preflight_text
