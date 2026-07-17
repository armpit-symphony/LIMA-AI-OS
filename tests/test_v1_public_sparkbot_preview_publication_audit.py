"""Static checks for the public Sparkbot preview publication audit."""

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
    / "v1_public_sparkbot_preview_publication_audit.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_public_sparkbot_publication_audit_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["audit_id"] == "v1_public_sparkbot_preview_publication_audit"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["audit_branch"] == "audit-v1-public-sparkbot-preview-publication"
    assert fixture["source_lima_commit_before_audit"] == (
        "2e5d5285059ef4f18c08c6959b191332b8122e5d"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_public_sparkbot_preview_branch_is_saved_to_fork_not_target() -> None:
    fixture = _load_fixture()

    assert fixture["public_sparkbot_local_branch"] == "public-work-settings-preview"
    assert fixture["public_sparkbot_local_commit"] == (
        "81eed8c4067b1a73885bbc79003ea5870b1604a2"
    )
    assert fixture["fork_repository"] == "https://github.com/armpit-symphony/Sparkbot"
    assert fixture["fork_branch"] == "public-work-settings-preview"
    assert fixture["fork_branch_sha"] == (
        "81eed8c4067b1a73885bbc79003ea5870b1604a2"
    )
    assert fixture["target_repository"] == "https://github.com/sparkpit-labs/Sparkbot"
    assert fixture["target_branch_present"] is False
    assert fixture["target_pull_request_created"] is False
    assert fixture["manual_pull_request_compare_url"] == (
        "https://github.com/sparkpit-labs/Sparkbot/compare/"
        "main...armpit-symphony:public-work-settings-preview?expand=1"
    )


def test_public_sparkbot_publication_blockers_are_explicit() -> None:
    blockers = _load_fixture()["publication_blockers"]

    assert blockers["direct_push_blocked_by_403"] is True
    assert "denied to armpit-symphony" in blockers["direct_push_error"]
    assert blockers["github_connector_pr_create_blocked_by_tool_mismatch"] is True
    assert blockers["github_cli_pr_create_blocked_by_missing_auth"] is True
    assert "gh auth login" in blockers["github_cli_missing_auth_message"]


def test_public_sparkbot_preview_scope_is_static_and_inert() -> None:
    fixture = _load_fixture()
    scope = fixture["sparkbot_preview_scope"]
    forbidden = fixture["sparkbot_forbidden_by_preview"]

    assert scope == {
        "work_page_shell_preview": True,
        "local_ai_settings_shell_preview": True,
        "public_capability_contract_additions": True,
        "documentation_alignment": True,
        "backend_capability_tests": True,
        "frontend_static_ui_tests": True,
    }

    for key in (
        "file_reads_added",
        "file_writes_added",
        "connector_calls_added",
        "credential_fields_added",
        "credential_storage_added",
        "endpoint_checks_added",
        "provider_calls_added",
        "model_routing_added",
        "model_calls_added",
        "tool_execution_added",
        "terminal_execution_added",
        "external_sends_added",
        "live_guardian_policy_enforcement_added",
        "lima_runtime_calls_added",
        "production_readiness_claim_added",
    ):
        assert forbidden[key] is False


def test_public_sparkbot_publication_validation_is_recorded() -> None:
    validation = _load_fixture()["validation"]

    assert validation["backend_capabilities_pytest"]["result"] == (
        "4 passed, 1 Starlette/httpx deprecation warning"
    )
    assert validation["frontend_vitest"]["result"] == (
        "1 test file passed, 4 tests passed"
    )
    assert validation["frontend_build"]["result"] == "passed"
    assert validation["sparkbot_diff_check"]["result"] == "passed"


def test_public_sparkbot_publication_audit_preserves_lima_boundaries() -> None:
    boundaries = _load_fixture()["lima_boundaries"]

    for key in (
        "runtime_behavior_added",
        "lima_runtime_files_changed",
        "lima_public_api_changed",
        "v1_g55_implementation_approved",
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
        "browser_file_network_device_robotics_physical_world_behavior_added",
        "product_readiness_claim_added",
        "production_readiness_claim_added",
    ):
        assert boundaries[key] is False


def test_public_sparkbot_publication_audit_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["publication_audit"]).read_text(
        encoding="utf-8"
    )

    assert "# V1 Public Sparkbot Preview Publication Audit" in text
    assert "public `sparkpit-labs/Sparkbot` preview branch" in text
    assert "saved to an accessible fork branch" in text
    assert "Target pull request created: no" in text
    assert "Permission to sparkpit-labs/Sparkbot.git denied to armpit-symphony" in text
    assert "Tool name github.create_pull_request does not match resource uri" in text
    assert "GitHub CLI pull-request creation failed because `gh` is not authenticated" in text
    assert fixture["manual_pull_request_compare_url"] in text
    assert "Work Page shell preview." in text
    assert "Local AI Settings shell preview." in text
    assert "does not add file reads, file writes, connector calls" in text
    assert "V1-G55 runtime implementation remains separately blocked" in text
