"""Static checks for the V1 consumer Work/Settings runbook execution audit."""

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
    / "v1_consumer_work_settings_test_runbook_execution_audit.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_consumer_work_settings_runbook_execution_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["audit_id"] == (
        "v1_consumer_work_settings_test_runbook_execution_audit"
    )
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["date"] == "2026-06-19"
    assert fixture["audit_branch"] == (
        "audit-v1-consumer-work-settings-test-runbook-execution"
    )
    assert fixture["source_lima_commit_before_audit"] == (
        "7f90c83946d7974e5f60294b1a602a1de3be4e51"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_consumer_work_settings_runbook_execution_records_branch_commits() -> None:
    branches = _load_fixture()["branch_commits"]

    assert branches["lima_ai_os"] == {
        "repository": "armpit-symphony/LIMA-AI-OS",
        "branch": "docs-v1-consumer-work-settings-test-runbook",
        "commit": "7f90c83946d7974e5f60294b1a602a1de3be4e51",
        "clean_before_audit_branch": True,
    }
    assert branches["public_sparkbot"] == {
        "repository": "armpit-symphony/Sparkbot",
        "target_repository": "sparkpit-labs/Sparkbot",
        "branch": "public-work-settings-preview",
        "commit": "81eed8c4067b1a73885bbc79003ea5870b1604a2",
        "clean": True,
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
        "clean": True,
    }
    assert branches["arc_bot_shell"] == {
        "repository": "armpit-symphony/Arc-Bot-shell",
        "branch": "arc-work-queue-runtime-settings-docs",
        "commit": "a05faea14ab24341b4b4567967911e33e51ce88a",
        "clean_during_initial_branch_commit_check": True,
        "post_validation_dirty_observed": True,
        "post_validation_dirty_paths": [
            "README.md",
            "docs/OPERATOR_CONSOLE_FOUNDATION.md",
            "docs/ROADMAP.md",
            "tests/test_arc_bot_phase0_scope_lock_runtime_ui.py",
        ],
        "known_status_warning": (
            "could not open directory '.pytest_cache/': Permission denied"
        ),
        "dirty_paths_staged_or_committed_by_lima_audit": False,
    }


def test_consumer_work_settings_runbook_execution_records_validation_results() -> None:
    commands = _load_fixture()["validation_commands"]

    expected = {
        (
            "C:\\Users\\limap\\Arc-Bot-shell",
            "python -B -m pytest -q tests -p no:cacheprovider",
            "93 passed in 0.24s",
        ),
        ("C:\\Users\\limap\\Arc-Bot-shell", "git diff --check", "passed"),
        (
            "C:\\Users\\limap\\Sparkbot_shell",
            "python -B -m pytest -q tests -p no:cacheprovider",
            "13 passed in 0.04s",
        ),
        (
            "C:\\Users\\limap\\Sparkbot_shell",
            "npm run build",
            "passed: tsc --noEmit && vite build; Vite built 61 modules",
        ),
        ("C:\\Users\\limap\\Sparkbot_shell", "git diff --check", "passed"),
        (
            "C:\\Users\\limap\\Sparkbot-public",
            ".\\.venv-public-test\\Scripts\\python.exe -B -m pytest -q "
            "backend\\tests\\test_capabilities.py -p no:cacheprovider",
            "4 passed, 1 StarletteDeprecationWarning in 0.27s",
        ),
        (
            "C:\\Users\\limap\\Sparkbot-public\\frontend",
            "npm run test -- --run",
            "1 test file passed, 4 tests passed",
        ),
        (
            "C:\\Users\\limap\\Sparkbot-public\\frontend",
            "npm run build",
            "passed: vite build; Vite built 32 modules",
        ),
        ("C:\\Users\\limap\\Sparkbot-public", "git diff --check", "passed"),
        ("C:\\Users\\limap\\LIMA-AI-OS", "python --version", "Python 3.12.10"),
        ("C:\\Users\\limap\\LIMA-AI-OS", "python -m compileall lima", "passed"),
        (
            "C:\\Users\\limap\\LIMA-AI-OS",
            "python -m pytest -q tests -p no:cacheprovider",
            "4709 passed in 4.04s",
        ),
        ("C:\\Users\\limap\\LIMA-AI-OS", "git diff --check", "passed"),
    }

    assert {
        (item["repo"], item["command"], item["result"]) for item in commands
    } == expected


def test_consumer_work_settings_runbook_execution_scope_stays_docs_only() -> None:
    scope = _load_fixture()["scope_audit"]

    assert scope["docs_tests_fixtures_only"] is True
    assert scope["post_validation_arc_bot_shell_dirty_observed"] is True
    for key in (
        "lima_runtime_files_changed",
        "public_api_exports_changed",
        "consumer_repository_files_changed",
        "public_sparkbot_target_repository_state_changed",
        "public_sparkbot_target_pr_created",
        "v1_g55_implementation_approved_or_started",
    ):
        assert scope[key] is False


def test_consumer_work_settings_runbook_execution_boundary_flags_are_false() -> None:
    flags = _load_fixture()["boundary_results"]

    for key in (
        "g55_runtime_wrapper_added",
        "provider_sdk_network_egress_runtime_added",
        "built_in_provider_sdk_client_added",
        "sdk_dependencies_or_vendor_sdk_imports_added",
        "endpoint_resolution_execution_added",
        "lima_owned_dns_http_socket_network_calls_or_direct_provider_egress_added",
        "secret_lookup_or_credential_value_access_added",
        "provider_token_or_api_key_access_added",
        "provider_configuration_change_or_fallback_execution_added",
        "non_local_endpoint_checks_allowed",
        "lima_connector_browser_network_file_device_robotics_physical_world_authority_added",
        "consumer_production_runtime_integration_added",
        "product_ready",
        "production_ready",
        "v1_0_complete",
    ):
        assert flags[key] is False


def test_consumer_work_settings_runbook_execution_sanitization_and_blockers() -> None:
    fixture = _load_fixture()

    sanitization = fixture["sanitization"]
    assert sanitization["command_status_metadata_only"] is True
    for key in (
        "raw_prompts_stored",
        "raw_model_responses_stored",
        "raw_customer_data_stored",
        "secrets_or_credential_values_stored",
        "provider_tokens_or_api_keys_stored",
        "raw_file_contents_diffs_or_patch_bodies_stored",
    ):
        assert sanitization[key] is False
    assert sanitization["public_sparkbot_warning"] == "StarletteDeprecationWarning"

    assert fixture["known_blockers"] == {
        "public_sparkbot_target_pr_requires_auth_or_cross_repo_pr_path": True,
        "v1_g55_requires_exact_operator_choice": True,
        "v1_product_readiness_not_established": True,
    }
    assert fixture["audit_decision"] == "pass_current_consumer_work_settings_stack"


def test_consumer_work_settings_runbook_execution_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["execution_audit"]).read_text(
        encoding="utf-8"
    )

    assert "# V1 Consumer Work/Settings Test Runbook Execution Audit" in text
    assert "`audit-v1-consumer-work-settings-test-runbook-execution`" in text
    assert "7f90c83946d7974e5f60294b1a602a1de3be4e51" in text
    assert "81eed8c4067b1a73885bbc79003ea5870b1604a2" in text
    assert "548b6d6aa6cde98b261e867c0c2db86ddbfa83dc" in text
    assert "a05faea14ab24341b4b4567967911e33e51ce88a" in text
    assert "93 passed in 0.24s" in text
    assert "13 passed in 0.04s" in text
    assert "4 passed, 1 StarletteDeprecationWarning in 0.27s" in text
    assert "1 test file passed, 4 tests passed" in text
    assert "4709 passed in 4.04s" in text
    assert "Runbook execution status: `pass_current_consumer_work_settings_stack`." in text
    assert "Post-validation Consumer Status Note" in text
    assert "tests/test_arc_bot_phase0_scope_lock_runtime_ui.py" in text
    assert "No V1-G55 implementation approval" not in text
    assert "V1-G55 remains blocked" in text
