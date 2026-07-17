"""Static checks for the V1 consumer Work/Settings test runbook."""

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
    / "v1_consumer_work_settings_test_runbook.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_consumer_work_settings_runbook_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["runbook_id"] == "v1_consumer_work_settings_test_runbook"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["date"] == "2026-06-19"
    assert fixture["branch"] == "docs-v1-consumer-work-settings-test-runbook"
    assert fixture["source_lima_commit_before_runbook"] == (
        "dbdcca147c44539e9c4cdd302b3eb05c1af067ed"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_consumer_work_settings_runbook_records_branch_map() -> None:
    branches = _load_fixture()["consumer_branches"]

    assert branches["lima_ai_os_source"] == {
        "repository": "armpit-symphony/LIMA-AI-OS",
        "branch": "docs-v1-consumer-testability-through-work-settings",
        "commit": "dbdcca147c44539e9c4cdd302b3eb05c1af067ed",
    }
    assert branches["public_sparkbot"] == {
        "repository": "armpit-symphony/Sparkbot",
        "target_repository": "sparkpit-labs/Sparkbot",
        "branch": "public-work-settings-preview",
        "commit": "81eed8c4067b1a73885bbc79003ea5870b1604a2",
        "target_pr_created": False,
        "manual_compare_url": (
            "https://github.com/sparkpit-labs/Sparkbot/compare/"
            "main...armpit-symphony:public-work-settings-preview?expand=1"
        ),
    }
    assert branches["sparkbot_shell"] == {
        "repository": "armpit-symphony/Sparkbot_shell",
        "branch": "sparkbot-shell-work-settings-runtime-preview",
        "commit": "548b6d6aa6cde98b261e867c0c2db86ddbfa83dc",
    }
    assert branches["arc_bot_shell"] == {
        "repository": "armpit-symphony/Arc-Bot-shell",
        "branch": "arc-work-queue-runtime-settings-docs",
        "commit": "a05faea14ab24341b4b4567967911e33e51ce88a",
    }


def test_consumer_work_settings_runbook_records_validation_order() -> None:
    commands = _load_fixture()["validation_commands"]

    assert [item["step"] for item in commands] == list(range(1, 13))
    expected = {
        (
            "C:\\Users\\limap\\Arc-Bot-shell",
            "python -B -m pytest -q tests -p no:cacheprovider",
            "93 passed in 0.27s",
        ),
        ("C:\\Users\\limap\\Arc-Bot-shell", "git diff --check", "pass"),
        (
            "C:\\Users\\limap\\Sparkbot_shell",
            "python -B -m pytest -q tests -p no:cacheprovider",
            "13 passed in 0.04s",
        ),
        (
            "C:\\Users\\limap\\Sparkbot_shell",
            "npm run build",
            "passed: tsc --noEmit && vite build",
        ),
        ("C:\\Users\\limap\\Sparkbot_shell", "git diff --check", "pass"),
        (
            "C:\\Users\\limap\\Sparkbot-public",
            ".\\.venv-public-test\\Scripts\\python.exe -B -m pytest -q "
            "backend\\tests\\test_capabilities.py -p no:cacheprovider",
            "4 passed, 1 Starlette/httpx deprecation warning",
        ),
        (
            "C:\\Users\\limap\\Sparkbot-public\\frontend",
            "npm run test -- --run",
            "1 test file passed, 4 tests passed",
        ),
        (
            "C:\\Users\\limap\\Sparkbot-public\\frontend",
            "npm run build",
            "passed: vite build",
        ),
        ("C:\\Users\\limap\\Sparkbot-public", "git diff --check", "pass"),
        ("C:\\Users\\limap\\LIMA-AI-OS", "python -m compileall lima", "pass"),
        (
            "C:\\Users\\limap\\LIMA-AI-OS",
            "python -m pytest -q tests -p no:cacheprovider",
            "pass; source matrix baseline was 4703 passed before this runbook",
        ),
        ("C:\\Users\\limap\\LIMA-AI-OS", "git diff --check", "pass"),
    }

    assert {
        (item["repo"], item["command"], item["expected_result"])
        for item in commands
    } == expected


def test_consumer_work_settings_runbook_preserves_boundary_flags() -> None:
    flags = _load_fixture()["boundary_results"]

    for key in (
        "v1_g55_implementation_approved",
        "g55_runtime_wrapper_added",
        "lima_runtime_files_changed_by_runbook",
        "public_api_exports_changed_by_runbook",
        "provider_sdk_network_egress_runtime_added",
        "built_in_provider_sdk_client_added",
        "sdk_dependencies_added",
        "endpoint_resolution_execution_added",
        "lima_owned_dns_http_socket_network_calls_added",
        "credential_lookup_or_value_access_added",
        "provider_token_or_api_key_access_added",
        "non_local_endpoint_checks_allowed",
        "connector_browser_network_file_device_robotics_physical_world_authority_added",
        "consumer_production_runtime_integration_added",
        "public_sparkbot_target_pr_created",
        "product_ready",
        "production_ready",
        "v1_0_complete",
    ):
        assert flags[key] is False


def test_consumer_work_settings_runbook_stop_conditions_fail_closed() -> None:
    fixture = _load_fixture()

    assert fixture["stop_conditions"] == [
        "unexpected_branch_or_commit_drift",
        "unreviewed_dirty_worktree",
        "consumer_validation_failure",
        "lima_validation_failure",
        "secret_credential_token_sdk_endpoint_or_network_required",
        "public_sparkbot_target_write_without_auth",
        "v1_g55_implementation_without_exact_approval",
    ]
    assert fixture["known_blockers"] == {
        "public_sparkbot_target_pr_requires_auth_or_cross_repo_pr_path": True,
        "v1_g55_requires_exact_operator_choice": True,
    }


def test_consumer_work_settings_runbook_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["test_runbook"]).read_text(
        encoding="utf-8"
    )

    assert "# V1 Consumer Work/Settings Test Runbook" in text
    assert "`docs-v1-consumer-work-settings-test-runbook`" in text
    assert "dbdcca147c44539e9c4cdd302b3eb05c1af067ed" in text
    assert "81eed8c4067b1a73885bbc79003ea5870b1604a2" in text
    assert "548b6d6aa6cde98b261e867c0c2db86ddbfa83dc" in text
    assert "a05faea14ab24341b4b4567967911e33e51ce88a" in text
    assert "No V1-G55 implementation approval." in text
    assert "No G55 runtime wrapper." in text
    assert "No product readiness, production readiness, or V1.0 completion claim." in text
    assert "V1-G55 remains blocked" in text
    assert fixture["consumer_branches"]["public_sparkbot"]["manual_compare_url"] in text
