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
    assert fixture["branch"] == "docs-v1-current-status-through-g55"
    assert (
        fixture["source_commit_before_alignment"]
        == "c8c0ecf95d0dce6e6e77c66947eb6257838a6b08"
    )
    assert fixture["documents"]["readme"] == "README.md"
    assert fixture["documents"]["current_project_state"] == "docs/CURRENT_PROJECT_STATE.md"
    assert fixture["readme_section"] == "Current V1 Status"
    assert fixture["current_project_state_section"] == "Current V1 Gate Snapshot"
    assert fixture["latest_authority_chain_audit"] == "V1-G54"
    assert fixture["latest_readiness_rollup"] == "V1-G54"
    assert fixture["current_gate"] == "V1-G55"
    assert fixture["v1_g55_approval_request_ready"] is True
    assert fixture["v1_g55_preflight_audit_ready"] is True
    assert fixture["v1_g55_work_order_ready"] is True
    assert fixture["v1_g55_operator_decision_packet_ready"] is True
    assert fixture["v1_g55_implementation_blocker_audit_active"] is True
    assert fixture["v1_g55_operator_decision_recorded_choice"] is None
    assert fixture["v1_g55_operator_decision_packet_records_approval"] is False
    assert fixture["operator_approval_recorded"] is False
    assert fixture["runtime_implementation_approved"] is False
    assert fixture["g55_wrapper_added"] is False
    assert fixture["g55_public_api_exports_changed"] is False
    assert fixture["v1_product_ready"] is False
    assert fixture["production_ready"] is False


def test_v1_readme_status_fixture_names_first_shells() -> None:
    assert set(_load_fixture()["v1_target_shells"]) == {
        "Sparkbot_shell",
        "Sparkbot",
        "Arc-Bot-shell",
    }


def test_v1_readme_status_fixture_adds_no_runtime_or_integration_behavior() -> None:
    fixture = _load_fixture()
    for key in (
        "runtime_behavior_added",
        "tests_support_changed",
        "shell_repos_changed",
        "sparkbot_import_added",
        "sparkbot_code_copied",
        "sparkbot_or_arc_bot_shell_changed_for_g55",
        "provider_sdk_network_egress_invocation_added",
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
        assert fixture[key] is False


def test_v1_readme_status_fixture_points_to_exact_next_step() -> None:
    fixture = _load_fixture()
    assert (
        fixture["if_approved_scope"]
        == "bounded_real_provider_sdk_network_egress_authority_wrapper"
    )
    assert (
        fixture["next_step"]
        == "record_one_valid_operator_choice_in_v1_g55_decision_record"
    )
    assert fixture["valid_operator_choices"] == [
        "Approve-V1-G55",
        "Revise-V1-G55",
        "Pause",
    ]


def test_readme_contains_current_v1_status_and_boundaries() -> None:
    text = README_PATH.read_text(encoding="utf-8")
    assert "## Current V1 Status" in text
    assert "LIMA remains `CANDIDATE_ONLY`." in text
    assert "`Sparkbot_shell`, public `Sparkbot`, and `Arc-Bot-shell`" in text
    assert "audited through `V1-G54`" in text
    assert "`V1-G55` is currently prepared as an approval request only" in text
    assert "implementation blocker audit are ready" in text
    assert "no operator approval is recorded" in text
    assert "no `V1-G55` runtime implementation is approved" in text
    assert "`Approve-V1-G55`, `Revise-V1-G55`, or `Pause`" in text
    assert "do not add the G55 wrapper" in text
    assert "change public API exports for G55" in text
    assert "invoke provider SDK/network egress" in text
    assert "add built-in provider SDK clients" in text
    assert "make LIMA-owned network calls" in text
    assert "read secrets" in text
    assert "access credential values" in text
    assert "change provider configuration" in text
    assert "execute fallback" in text
    assert "wire consumer production runtime behavior" in text
    assert "Existing V1 candidate slices remain non-production evidence only" in text
    assert "does not edit Sparkbot or Arc-Bot-shell" in text
    assert "real SDK, network, credential, connector, browser, file, device, robotics, or physical-world behavior" in text
    assert "production readiness" in text


def test_current_project_state_contains_g55_gate_snapshot() -> None:
    fixture = _load_fixture()
    state_text = (
        REPO_ROOT / fixture["documents"]["current_project_state"]
    ).read_text(encoding="utf-8")

    assert "### Current V1 Gate Snapshot" in state_text
    assert "LIMA remains `CANDIDATE_ONLY`." in state_text
    assert "V1 runtime authority chain audit through G54: complete." in state_text
    assert "V1 readiness rollup through G54: complete." in state_text
    assert "V1-G55 real provider SDK/network egress approval request: prepared, not approved." in state_text
    assert "V1-G55 implementation blocker audit: active." in state_text
    assert "Operator approval recorded for G55: no." in state_text
    assert "G55 runtime implementation approved: no." in state_text
    assert "`Approve-V1-G55`, `Revise-V1-G55`, or `Pause`" in state_text
    assert "do not implement the G55 wrapper" in state_text
    assert "make LIMA-owned DNS/HTTP/socket/network calls" in state_text
    assert "read secrets" in state_text
    assert "edit Sparkbot or Arc-Bot-shell for G55" in state_text
    assert "claim V1/product/production readiness" in state_text
