"""Static checks for the V1 through-G57 candidate test runbook."""

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
    / "v1_through_g57_candidate_test_runbook.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_through_g57_runbook_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["runbook_id"] == "v1_through_g57_candidate_test_runbook"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["date"] == "2026-06-20"
    assert fixture["branch"] == "docs-v1-through-g57-candidate-test-runbook"
    assert fixture["source_lima_commit_before_runbook"] == (
        "7888182b1ba0d53aa42f6480db574e7c1975562d"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_through_g57_runbook_records_branch_map() -> None:
    branches = _load_fixture()["consumer_branches"]

    assert branches["lima_ai_os_source"] == {
        "repository": "armpit-symphony/LIMA-AI-OS",
        "branch": "audit-v1-g57-provider-execution-hardening-authorization-request",
        "commit": "7888182b1ba0d53aa42f6480db574e7c1975562d",
        "pushed": True,
    }
    assert branches["public_sparkbot"] == {
        "repository": "sparkpit-labs/Sparkbot",
        "local_path": "C:\\Users\\limap\\Sparkbot-public",
        "branch": "v1-g56-runtime-authority-chain-audit",
        "commit": "ae5cc9c563ea2b0f08c91af03164a78b4b20e3e2",
        "target_push_blocked": True,
        "target_push_blocker": "github_403_permission_denied_to_armpit_symphony",
    }
    assert branches["accessible_sparkbot"] == {
        "repository": "armpit-symphony/Sparkbot",
        "local_path": "C:\\Users\\limap\\Sparkbot",
        "branch": "v1-g56-consumer-fake-executor-provider-sdk-network-egress-smoke",
        "commit": "ddaa4cc",
        "pushed": True,
    }
    assert branches["arc_bot_shell"] == {
        "repository": "armpit-symphony/Arc-Bot-shell",
        "local_path": "C:\\Users\\limap\\Arc-Bot-shell",
        "branch": "v1-g56-consumer-fake-executor-provider-sdk-network-egress-smoke",
        "commit": "ec06e7670f18eeae192fc0f995b6ffd07481d8c9",
        "pushed": True,
        "unrelated_dirty_worktree_files_present": True,
    }


def test_v1_through_g57_runbook_records_validation_order() -> None:
    commands = _load_fixture()["validation_commands"]

    assert [item["step"] for item in commands] == list(range(1, 11))
    assert commands[0] == {
        "step": 1,
        "repo": "C:\\Users\\limap\\Sparkbot-public",
        "command": "python -m pytest -q tests\\test_sparkbot_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.py -p no:cacheprovider",
        "expected_result": "8 passed",
    }
    assert commands[2] == {
        "step": 3,
        "repo": "C:\\Users\\limap\\Sparkbot",
        "command": "python -m pytest -q tests\\test_sparkbot_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.py -p no:cacheprovider",
        "expected_result": "8 passed",
    }
    assert commands[4] == {
        "step": 5,
        "repo": "C:\\Users\\limap\\Arc-Bot-shell",
        "command": "python -m pytest -q tests\\test_arc_bot_shell_lima_v1_g56_fake_executor_provider_sdk_network_egress_smoke.py -p no:cacheprovider",
        "expected_result": "8 passed",
    }
    assert commands[8] == {
        "step": 9,
        "repo": "C:\\Users\\limap\\LIMA-AI-OS",
        "command": "python -m pytest -q tests -p no:cacheprovider",
        "expected_result": "pass_source_audit_baseline_4978_passed",
    }


def test_v1_through_g57_runbook_candidate_evidence_is_bounded() -> None:
    fixture = _load_fixture()

    assert fixture["candidate_evidence_proven"] == [
        "sparkbot_public_imports_and_calls_g55_wrapper_with_fake_in_process_provider_sdk_network_executor_only",
        "accessible_sparkbot_imports_and_calls_g55_wrapper_with_same_g56_checkpoint",
        "arc_bot_shell_imports_and_calls_g55_wrapper_with_fake_in_process_provider_sdk_network_executor_only",
        "lima_records_g56_latest_completed_candidate_gate",
        "lima_records_g57_next_request_only_operator_gate",
    ]


def test_v1_through_g57_runbook_preserves_boundary_flags() -> None:
    flags = _load_fixture()["boundary_results"]

    for key in (
        "v1_g57_implementation_approved",
        "g57_provider_execution_hardening_authorization_added",
        "lima_runtime_files_changed_by_runbook",
        "public_api_exports_changed_by_runbook",
        "provider_sdk_client_added",
        "built_in_provider_sdk_client_added",
        "sdk_dependencies_added",
        "vendor_provider_sdk_import_added",
        "endpoint_resolution_execution_added",
        "lima_owned_dns_http_socket_network_calls_added",
        "direct_provider_egress_by_lima_added",
        "credential_lookup_or_value_access_added",
        "provider_token_or_api_key_access_added",
        "provider_configuration_changes_added",
        "fallback_execution_added",
        "connector_browser_network_file_device_robotics_physical_world_authority_added",
        "consumer_production_runtime_integration_added",
        "public_sparkbot_target_push_performed",
        "product_ready",
        "production_ready",
        "v1_0_complete",
    ):
        assert flags[key] is False, key


def test_v1_through_g57_runbook_stop_conditions_fail_closed() -> None:
    fixture = _load_fixture()

    assert fixture["stop_conditions"] == [
        "unexpected_branch_or_commit_drift",
        "dirty_worktree_affects_evidence_scope",
        "consumer_validation_failure",
        "lima_validation_failure",
        "secret_credential_token_sdk_endpoint_or_network_required",
        "public_sparkbot_target_write_without_auth",
        "v1_g57_implementation_without_exact_approval",
    ]
    assert fixture["known_blockers"] == {
        "public_sparkbot_target_push_requires_write_credentials": True,
        "v1_g57_requires_exact_operator_choice": True,
        "arc_bot_shell_has_unrelated_dirty_worktree_files_outside_g56_evidence": True,
    }
    assert fixture["recommended_next_step"] == (
        "operator_decision_on_g57_or_public_sparkbot_write_credential_unblock"
    )


def test_v1_through_g57_runbook_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["test_runbook"]).read_text(
        encoding="utf-8"
    )

    assert "# V1 Through G57 Candidate Test Runbook" in text
    assert "`docs-v1-through-g57-candidate-test-runbook`" in text
    assert "7888182b1ba0d53aa42f6480db574e7c1975562d" in text
    assert "ae5cc9c563ea2b0f08c91af03164a78b4b20e3e2" in text
    assert "ddaa4cc" in text
    assert "ec06e7670f18eeae192fc0f995b6ffd07481d8c9" in text
    assert "No V1-G57 implementation approval." in text
    assert "No provider SDK clients." in text
    assert "No LIMA-owned DNS, HTTP, socket, or provider network call." in text
    assert "No product readiness, production readiness, or V1.0 completion claim." in text
    assert "GitHub 403" in text
    assert "V1-G57 remains blocked until the operator records exactly one valid choice" in text


def test_v1_through_g57_runbook_outputs_do_not_include_sensitive_markers() -> None:
    fixture = _load_fixture()
    output = json.dumps(fixture, sort_keys=True)
    output += (REPO_ROOT / fixture["documents"]["test_runbook"]).read_text(
        encoding="utf-8"
    )

    for forbidden in (
        "diff --git",
        "@@",
        "BEGIN PATCH",
        "raw patch body",
        "raw prompt value",
        "raw model response value",
        "raw customer data value",
        "provider credential value",
        "provider token value",
        "api key value",
        "raw-secret-123",
    ):
        assert forbidden not in output
