"""Static checks for the root README V1 status alignment."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
README_PATH = REPO_ROOT / "README.md"
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_readme_status_alignment.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_readme_status_fixture_preserves_candidate_only_boundary() -> None:
    fixture = _load_fixture()

    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == (
        "prepare-v1-g57-provider-execution-hardening-authorization-approval-request"
    )
    assert fixture["source_commit_before_alignment"] == (
        "7c7f7ee6f566cbbc1d6eac5b3bd9e6a0ad2dba16"
    )
    assert fixture["documents"]["readme"] == "README.md"
    assert fixture["documents"]["current_project_state"] == "docs/CURRENT_PROJECT_STATE.md"
    assert fixture["readme_section"] == "Current V1 Status"
    assert fixture["current_project_state_section"] == "Current V1 Gate Snapshot"
    assert fixture["latest_completed_gate"] == "V1-G56"
    assert fixture["latest_authority_chain_audit"] == "V1-G56"
    assert fixture["latest_readiness_rollup"] == "V1-G56"
    assert fixture["current_gate"] == "V1-G57"
    assert fixture["next_lane_request_only"] is True
    assert fixture["g56_request_packet_prepared"] is True
    assert fixture["g56_operator_approval_recorded"] is True
    assert fixture["g56_runtime_implementation_approved"] is True
    assert fixture["g56_independent_audit_complete"] is True
    assert fixture["g57_request_packet_prepared"] is True
    assert fixture["g57_operator_approval_recorded"] is False
    assert fixture["g57_runtime_implementation_approved"] is False
    assert fixture["g57_valid_operator_choices"] == [
        "Approve-V1-G57",
        "Revise-V1-G57",
        "Pause",
    ]
    assert fixture["v1_g55_operator_approval_recorded"] is True
    assert fixture["v1_g55_runtime_implementation_approved"] is True
    assert fixture["v1_g55_independent_audit_complete"] is True
    assert fixture["g55_wrapper_added"] is True
    assert fixture["g55_public_api_exports_changed"] is True
    assert fixture["g55_public_api_change_limited_to_approved_harness_exports"] is True
    assert fixture["g55_caller_injected_provider_sdk_network_executor_only"] is True
    assert fixture["v1_product_ready"] is False
    assert fixture["production_ready"] is False

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_v1_readme_status_fixture_names_first_shells() -> None:
    assert set(_load_fixture()["v1_target_shells"]) == {
        "Sparkbot_shell",
        "Sparkbot",
        "Arc-Bot-shell",
    }


def test_v1_readme_status_fixture_adds_no_new_runtime_or_integration_behavior() -> None:
    fixture = _load_fixture()

    for key in (
        "runtime_behavior_added_by_status_refresh",
        "tests_support_changed",
        "shell_repos_changed",
        "sparkbot_import_added",
        "sparkbot_code_copied",
        "sparkbot_or_arc_bot_shell_changed_for_g57",
        "g57_provider_execution_hardening_authorization_added",
        "built_in_provider_sdk_client_added",
        "sdk_dependency_added",
        "vendor_sdk_import_added",
        "provider_endpoint_resolution_by_lima_added",
        "network_call_performed_by_lima",
        "secret_lookup_added",
        "credential_value_access_added",
        "provider_token_or_api_key_access_added",
        "provider_configuration_changes_added",
        "fallback_execution_added",
        "consumer_production_runtime_integration_added",
        "connector_browser_network_file_device_robotics_physical_world_behavior_added",
    ):
        assert fixture[key] is False, key


def test_v1_readme_status_fixture_points_to_exact_next_step() -> None:
    fixture = _load_fixture()

    assert fixture["next_recommended_lane"] == (
        "operator_decision_v1_g57_provider_execution_hardening_authorization"
    )
    assert fixture["next_step"] == "record_v1_g57_operator_decision"


def test_readme_contains_current_v1_status_and_boundaries() -> None:
    text = README_PATH.read_text(encoding="utf-8")

    assert "## Current V1 Status" in text
    assert "LIMA remains `CANDIDATE_ONLY`." in text
    assert "`Sparkbot_shell`, public `Sparkbot`, and `Arc-Bot-shell`" in text
    assert "audited through `V1-G56`" in text
    assert "V1-G57 provider execution hardening authorization approval request is prepared" in text
    assert "`V1-G56` is complete as consumer fake-executor provider SDK/network egress smoke evidence" in text
    assert "fake in-process provider SDK/network executors only" in text
    assert "The active next V1 lane is operator decision on the request-only `V1-G57" in text
    assert "`Approve-V1-G57`, `Revise-V1-G57`, or `Pause`" in text
    assert "do not implement G57 authorization evidence" in text
    assert "edit consumer repositories for G57" in text
    assert "add built-in provider SDK clients" in text
    assert "make LIMA-owned network calls" in text
    assert "read secrets" in text
    assert "access credential values" in text
    assert "change provider configuration" in text
    assert "execute fallback" in text
    assert "wire consumer production runtime behavior" in text
    assert "Existing V1 candidate slices remain non-production evidence only" in text
    assert "does not authorize built-in SDK, LIMA-owned network, credential" in text
    assert "physical-world behavior" in text


def test_current_project_state_contains_post_g56_gate_snapshot() -> None:
    fixture = _load_fixture()
    state_text = (
        REPO_ROOT / fixture["documents"]["current_project_state"]
    ).read_text(encoding="utf-8")

    assert "### Current V1 Gate Snapshot" in state_text
    assert "LIMA remains `CANDIDATE_ONLY`." in state_text
    assert "V1 runtime authority chain audit through G56: complete." in state_text
    assert "V1 readiness rollup through G56: complete." in state_text
    assert "V1 post-G56 next-lane decision matrix: complete." in state_text
    assert "V1-G55 real provider SDK/network egress wrapper: implemented and independently audited" in state_text
    assert "V1-G56 consumer fake-executor provider SDK/network egress smoke: implemented and audited" in state_text
    assert "V1-G57 provider execution hardening authorization approval packet: prepared for operator decision, not approved." in state_text
    assert "V1-G57 valid operator choices: `Approve-V1-G57`, `Revise-V1-G57`, or `Pause`." in state_text
    assert "V1-G57 implementation approval recorded: no." in state_text
    assert "The next smallest safe V1 step is to record exactly one operator choice" in state_text
    assert "do not implement G57 authorization evidence" in state_text
    assert "make LIMA-owned DNS/HTTP/socket/network calls" in state_text
    assert "read secrets" in state_text
    assert "edit Sparkbot or Arc-Bot-shell for G57" in state_text
    assert "claim V1/product/production readiness" in state_text
