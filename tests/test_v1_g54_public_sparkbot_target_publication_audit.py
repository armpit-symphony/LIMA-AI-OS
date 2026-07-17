"""Static checks for the V1-G54 public Sparkbot target publication audit."""

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
    / "v1_g54_public_sparkbot_target_publication_audit.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g54_public_target_publication_audit_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["audit_id"] == "v1_g54_public_sparkbot_target_publication_audit"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["audit_branch"] == (
        "audit-v1-g54-public-sparkbot-target-publication"
    )
    assert fixture["source_lima_commit_before_audit"] == (
        "afeec9a68965702b6869748cb0f7ad86ced588c3"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g54_public_target_branch_matches_local_sparkbot_commit() -> None:
    fixture = _load_fixture()

    assert fixture["public_sparkbot_local_branch"] == "public-work-settings-preview"
    assert fixture["public_sparkbot_local_commit"] == (
        "81eed8c4067b1a73885bbc79003ea5870b1604a2"
    )
    assert fixture["target_repository"] == "https://github.com/sparkpit-labs/Sparkbot"
    assert fixture["target_branch"] == "public-work-settings-preview"
    assert fixture["target_branch_present"] is True
    assert fixture["target_branch_sha"] == fixture["public_sparkbot_local_commit"]
    assert fixture["target_branch_matches_local_commit"] is True


def test_v1_g54_public_target_push_probe_records_permission_boundary() -> None:
    fixture = _load_fixture()

    assert fixture["direct_push_with_current_credential"] == "failed_403"
    assert "denied to armpit-symphony" in fixture["direct_push_error"]
    assert fixture["target_pull_request_created_by_this_audit"] is False


def test_v1_g54_public_sparkbot_preview_scope_is_static_and_inert() -> None:
    fixture = _load_fixture()

    assert fixture["sparkbot_preview_scope"] == {
        "work_page_shell_preview": True,
        "local_ai_settings_shell_preview": True,
        "public_capability_contract_additions": True,
        "documentation_alignment": True,
        "backend_capability_status_updates": True,
        "backend_capability_tests": True,
        "frontend_static_ui_components": True,
        "frontend_static_ui_tests": True,
    }

    for key, value in fixture["sparkbot_forbidden_by_preview"].items():
        assert value is False, key


def test_v1_g54_public_sparkbot_validation_is_recorded() -> None:
    validation = _load_fixture()["validation"]

    assert validation["backend_pytest"]["result"] == "5 passed"
    assert validation["frontend_vitest"]["result"] == (
        "1 test file passed, 4 tests passed"
    )
    assert validation["frontend_build"]["result"] == "passed"
    assert validation["sparkbot_range_diff_check"]["result"] == "passed"
    assert validation["target_branch_probe"]["result"] == (
        "81eed8c4067b1a73885bbc79003ea5870b1604a2 "
        "refs/heads/public-work-settings-preview"
    )
    assert validation["target_push_probe"]["result"] == (
        "failed_403_permission_denied"
    )


def test_v1_g54_public_target_audit_preserves_runtime_boundaries() -> None:
    boundaries = _load_fixture()["v1_g54_boundaries"]

    assert boundaries["fake_sdk_egress_harness_remains_candidate_only"] is True
    assert boundaries["runtime_authority_chain_through_g54_metadata_only"] is True

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


def test_v1_g54_public_target_audit_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["target_publication_audit"]).read_text(
        encoding="utf-8"
    )

    assert "# V1-G54 Public Sparkbot Target Publication Audit" in text
    assert "public `sparkpit-labs/Sparkbot` target-branch state" in text
    assert fixture["public_sparkbot_local_commit"] in text
    assert "Target branch present: yes" in text
    assert "Permission to sparkpit-labs/Sparkbot.git denied to armpit-symphony" in text
    assert "Work Page shell preview." in text
    assert "Local AI Settings shell preview." in text
    assert "does not add file reads, file writes, connector calls" in text
    assert "V1-G55 runtime implementation remains blocked" in text
