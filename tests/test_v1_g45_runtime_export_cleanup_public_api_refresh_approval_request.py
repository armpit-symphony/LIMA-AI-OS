"""Static checks for the V1-G45 runtime export cleanup/public API refresh request."""

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
    / "v1_g45_runtime_export_cleanup_public_api_refresh_approval_request.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g45_request_docs_and_fixture_exist() -> None:
    fixture = _load_fixture()

    assert fixture["gate_id"] == (
        "v1_g45_runtime_export_cleanup_public_api_refresh_approval_request"
    )
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == (
        "prepare-v1-g45-runtime-export-cleanup-public-api-refresh-approval-request"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g45_has_no_implementation_approval_yet() -> None:
    fixture = _load_fixture()
    decision = fixture["decision_record"]

    assert fixture["implementation_approved"] is False
    assert fixture["operator_approval_recorded"] is False
    assert fixture["runtime_export_cleanup_public_api_refresh_approved"] is False
    assert fixture["runtime_export_cleanup_public_api_refresh_added"] is False
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["public_api_fixture_refreshed"] is False
    assert fixture["validator_behavior_changed"] is False
    assert decision["recorded_choice"] == "none"
    assert decision["approved_implementation_branch"] == "none"
    assert decision["implementation_approved"] is False


def test_v1_g45_exact_decision_options_are_locked() -> None:
    fixture = _load_fixture()

    assert fixture["valid_operator_choices"] == [
        "Approve-V1-G45",
        "Revise-V1-G45",
        "Pause",
    ]
    assert fixture["required_approval_wording"].startswith(
        "I explicitly approve V1-G45 implementation"
    )
    assert fixture["proposed_implementation_branch"] == (
        "v1-g45-runtime-export-cleanup-public-api-refresh"
    )


def test_v1_g45_cleanup_target_is_exact() -> None:
    target = _load_fixture()["cleanup_target_if_operator_says_yes"]

    assert target["package"] == "lima.harness"
    assert target["runtime_file"] == "lima/harness/__init__.py"
    assert target["export_surface"] == "lima.harness.__all__"
    assert target["symbols_to_add_to_all"] == [
        "V1LiveProviderModelCallAuthorityError",
        "validate_v1_live_provider_model_call_authority",
    ]
    assert target["symbol_removal_allowed"] is False
    assert target["symbol_rename_allowed"] is False
    assert target["validator_behavior_change_allowed"] is False
    assert target["consumer_repo_edits_allowed"] is False
    assert target["live_runtime_calls_allowed"] is False


def test_v1_g45_existing_frozen_exports_must_be_preserved() -> None:
    target = _load_fixture()["cleanup_target_if_operator_says_yes"]

    assert target["required_existing_symbols_to_preserve"] == [
        "V1ProviderModelRoutingAuthorityError",
        "validate_v1_provider_model_routing_authority",
    ]


def test_v1_g45_approved_file_scope_is_exact() -> None:
    fixture = _load_fixture()

    assert fixture["approved_lima_runtime_files_if_operator_says_yes"] == [
        "lima/harness/__init__.py"
    ]
    assert set(fixture["approved_lima_docs_tests_fixtures_if_operator_says_yes"]) == {
        "docs/V1_G45_RUNTIME_EXPORT_CLEANUP_PUBLIC_API_REFRESH.md",
        "docs/V1_G45_RUNTIME_EXPORT_CLEANUP_PUBLIC_API_REFRESH_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g45_runtime_export_cleanup_public_api_refresh.json",
        "tests/test_v1_g45_runtime_export_cleanup_public_api_refresh.py",
        "tests/fixtures/runtime_extraction/v1_g22_final_public_api_freeze.json",
    }
    assert fixture["approved_consumer_files_if_operator_says_yes"] == []


def test_v1_g45_prior_evidence_refs_exist() -> None:
    fixture = _load_fixture()

    for relative_path in fixture["required_prior_evidence_refs"]:
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g45_forbidden_runtime_and_external_boundaries_remain_false() -> None:
    fixture = _load_fixture()

    for key in (
        "validator_behavior_changed",
        "consumer_repo_mutation_added",
        "consumer_runtime_calls_added",
        "consumer_integration_added",
        "live_provider_model_call_execution_added",
        "actual_model_request_dispatch_execution_added",
        "network_call_added",
        "secret_lookup_added",
        "credential_value_access_added",
        "fallback_execution_added",
        "tool_execution_added",
        "connector_browser_network_file_device_robotics_physical_world_behavior_added",
        "raw_diff_or_patch_persisted",
        "raw_file_content_persisted",
        "product_ready",
    ):
        assert fixture[key] is False


def test_v1_g45_docs_contain_cleanup_boundary_language() -> None:
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
    assert "must not change validator behavior" in approval_text
    assert "No Sparkbot or Arc-Bot-shell files" in approval_text
    assert "Runtime export cleanup/public API refresh approved: no" in approval_text
    assert "Recorded choice: none" in decision_text
    assert "Recorded choice: Approve-V1-G45" in decision_text
    assert "Implementation must not start until `Approve-V1-G45`" in preflight_text
