"""Static checks for the V1 consumer Work/Settings readiness audit."""

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
    / "v1_consumer_work_settings_readiness_audit.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_consumer_work_settings_audit_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["audit_id"] == "v1_consumer_work_settings_readiness_audit"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["audit_branch"] == "audit-v1-consumer-work-settings-readiness"
    assert fixture["source_lima_commit_before_audit"] == (
        "21a489c6498d46efeb0ce5e44b27f11061445af6"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_consumer_work_settings_audit_records_all_three_consumer_branches() -> None:
    evidence = _load_fixture()["consumer_evidence"]

    assert evidence["public_sparkbot"]["repository"] == "sparkpit-labs/Sparkbot"
    assert evidence["public_sparkbot"]["fork_repository"] == "armpit-symphony/Sparkbot"
    assert evidence["public_sparkbot"]["branch"] == "public-work-settings-preview"
    assert evidence["public_sparkbot"]["commit"] == (
        "81eed8c4067b1a73885bbc79003ea5870b1604a2"
    )
    assert evidence["public_sparkbot"]["target_pr_created"] is False

    assert evidence["sparkbot_shell"]["repository"] == "armpit-symphony/Sparkbot_shell"
    assert evidence["sparkbot_shell"]["branch"] == (
        "sparkbot-shell-work-settings-runtime-preview"
    )
    assert evidence["sparkbot_shell"]["commit"] == (
        "548b6d6aa6cde98b261e867c0c2db86ddbfa83dc"
    )

    assert evidence["arc_bot_shell"]["repository"] == "armpit-symphony/Arc-Bot-shell"
    assert evidence["arc_bot_shell"]["branch"] == (
        "arc-work-queue-runtime-settings-docs"
    )
    assert evidence["arc_bot_shell"]["commit"] == (
        "a05faea14ab24341b4b4567967911e33e51ce88a"
    )


def test_consumer_work_settings_audit_accepts_only_bounded_capabilities() -> None:
    evidence = _load_fixture()["consumer_evidence"]

    assert set(evidence["public_sparkbot"]["accepted_capabilities"]) == {
        "static_work_page_preview",
        "static_local_ai_settings_preview",
        "public_capability_contract_updates",
        "frontend_backend_tests",
    }
    assert set(evidence["sparkbot_shell"]["accepted_capabilities"]) == {
        "work_route",
        "settings_route",
        "user_selected_file_reads_into_browser_react_state",
        "in_memory_document_editing",
        "simulated_network_index_search",
        "localhost_loopback_endpoint_reachability_checks",
    }
    assert set(evidence["arc_bot_shell"]["accepted_capabilities"]) == {
        "work_queue_operator_console_docs",
        "runtime_settings_operator_console_docs",
        "work_program_state_contract",
        "fail_closed_boundary_tests",
    }


def test_consumer_work_settings_audit_keeps_blockers_explicit() -> None:
    blockers = _load_fixture()["blocked_or_not_proven"]

    for key in (
        "public_sparkbot_target_pr_created",
        "v1_g55_implementation_approved",
        "lima_provider_sdk_network_egress_runtime_added",
        "built_in_provider_sdk_client_added",
        "provider_model_generation_calls_through_lima_added",
        "credential_lookup_or_value_access_added",
        "provider_token_or_api_key_access_added",
        "non_local_endpoint_checks_allowed",
        "connector_browser_network_file_device_robotics_physical_world_authority_added",
        "consumer_production_runtime_integration_added",
        "product_ready",
        "production_ready",
        "v1_0_complete",
    ):
        assert blockers[key] is False


def test_consumer_work_settings_audit_preserves_lima_runtime_boundaries() -> None:
    boundaries = _load_fixture()["lima_boundaries"]

    for key in (
        "runtime_behavior_added",
        "lima_runtime_files_changed",
        "lima_public_api_changed",
        "provider_sdk_network_egress_invocation_added",
        "built_in_provider_sdk_client_added",
        "sdk_dependency_added",
        "vendor_provider_sdk_import_added",
        "dns_http_socket_network_call_added",
        "direct_provider_egress_added",
        "secret_lookup_added",
        "credential_value_access_added",
        "provider_token_or_api_key_access_added",
        "provider_configuration_change_added",
        "fallback_execution_added",
        "consumer_production_runtime_integration_added",
        "browser_file_network_device_robotics_physical_world_behavior_added_by_lima",
        "product_readiness_claim_added",
        "production_readiness_claim_added",
    ):
        assert boundaries[key] is False


def test_consumer_work_settings_audit_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (
        REPO_ROOT / fixture["documents"]["consumer_work_settings_readiness_audit"]
    ).read_text(encoding="utf-8")

    assert "# V1 Consumer Work/Settings Readiness Audit" in text
    assert "`audit-v1-consumer-work-settings-readiness`" in text
    assert "public `sparkpit-labs/Sparkbot` preview content" in text
    assert "`public-work-settings-preview`" in text
    assert "81eed8c4067b1a73885bbc79003ea5870b1604a2" in text
    assert "`sparkbot-shell-work-settings-runtime-preview`" in text
    assert "548b6d6aa6cde98b261e867c0c2db86ddbfa83dc" in text
    assert "`arc-work-queue-runtime-settings-docs`" in text
    assert "a05faea14ab24341b4b4567967911e33e51ce88a" in text
    assert "not live LIMA runtime parity and not V1.0 readiness" in text
    assert "Public Sparkbot target PR creation" in text
    assert "LIMA V1-G55 implementation approval" in text
    assert "`lima/` runtime files changed by this audit: no." in text
    assert "Keep the consumer branches separate and testable" in text
