"""Static checks for the V1 consumer testability matrix through Work/Settings."""

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
    / "v1_consumer_testability_matrix_through_work_settings.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_consumer_testability_matrix_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["matrix_id"] == (
        "v1_consumer_testability_matrix_through_work_settings"
    )
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "docs-v1-consumer-testability-through-work-settings"
    assert fixture["source_lima_commit_before_matrix"] == (
        "525648d1d7ef536dc89e793095db89f69728c015"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_consumer_testability_matrix_records_branch_commits() -> None:
    branches = _load_fixture()["consumer_branches"]

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
    assert branches["lima_ai_os"] == {
        "repository": "armpit-symphony/LIMA-AI-OS",
        "branch": "audit-v1-consumer-work-settings-readiness",
        "commit": "525648d1d7ef536dc89e793095db89f69728c015",
    }


def test_consumer_testability_matrix_records_validation_commands() -> None:
    commands = _load_fixture()["validation_commands"]

    expected = {
        (
            "C:\\Users\\limap\\Arc-Bot-shell",
            "python -B -m pytest -q tests -p no:cacheprovider",
            "93 passed in 0.27s",
        ),
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
        (
            "C:\\Users\\limap\\Sparkbot-public",
            ".\\.venv-public-test\\Scripts\\python.exe -B -m pytest -q backend\\tests\\test_capabilities.py -p no:cacheprovider",
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
        (
            "C:\\Users\\limap\\LIMA-AI-OS",
            "python -m pytest -q tests -p no:cacheprovider",
            "4698 passed",
        ),
    }

    assert {
        (item["repo"], item["command"], item["result"]) for item in commands
    } == expected


def test_consumer_testability_matrix_records_current_g61_refresh() -> None:
    refresh = _load_fixture()["current_status_refresh"]

    assert refresh["current_gate"] == "V1-G61"
    assert refresh["latest_completed_gate"] == "V1-G60"
    assert refresh["latest_authority_chain_audit"] == "V1-G56"
    assert refresh["required_next_action"] == "record_exactly_one_v1_g61_operator_choice"
    assert refresh["valid_operator_choices"] == [
        "Approve-V1-G61",
        "Revise-V1-G61",
        "Pause",
    ]
    assert refresh["v1_g61_operator_approval_recorded"] is False
    assert refresh["v1_g61_runtime_vendor_sdk_import_execution_proof_implemented"] is False
    assert refresh["g61_operator_decision_packet_status_audit"] == (
        "awaiting_exactly_one_valid_operator_choice"
    )
    assert refresh["historical_g55_gate_superseded_for_current_action"] is True
    assert refresh["latest_post_g61_request_refresh_focused_tests_passed"] == 8
    assert refresh["latest_post_g61_request_refresh_broader_tests_passed"] == 117
    assert refresh["latest_post_g61_request_refresh_full_lima_suite_tests_passed"] == 5362
    assert refresh["latest_quickstart_artifact_refresh_focused_tests_passed"] == 7
    assert refresh["latest_quickstart_artifact_refresh_adjacent_tests_passed"] == 64
    assert refresh["latest_quickstart_artifact_refresh_broader_tests_passed"] == 133
    assert refresh["latest_quickstart_artifact_refresh_full_lima_suite_tests_passed"] == 5364
    assert refresh["latest_handoff_freshness_authority_created"] is False


def test_consumer_testability_matrix_is_not_readiness_completion() -> None:
    not_proven = _load_fixture()["does_not_prove"]

    for key in (
        "v1_g55_implementation_approved",
        "lima_provider_sdk_network_egress_runtime_added",
        "built_in_provider_sdk_client_added",
        "provider_model_generation_through_lima_added",
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
        assert not_proven[key] is False


def test_consumer_testability_matrix_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (
        REPO_ROOT / fixture["documents"]["consumer_testability_matrix"]
    ).read_text(encoding="utf-8")

    assert "# V1 Consumer Testability Matrix Through Work/Settings" in text
    assert "`docs-v1-consumer-testability-through-work-settings`" in text
    assert "## Current Status Refresh" in text
    assert "This matrix is historical Work/Settings testability evidence." in text
    assert "Current active gate: `V1-G61`." in text
    assert "Valid V1-G61 choices: `Approve-V1-G61`, `Revise-V1-G61`, or `Pause`." in text
    assert "V1_G61_OPERATOR_DECISION_PACKET_STATUS_AUDIT.md" in text
    assert "records `Approve-V1-G61` for bounded local import-proof evidence only" in text
    assert "V1_CANDIDATE_TEST_HANDOFF_MANIFEST.md" in text
    assert "latest post-G61 request readiness-refresh evidence passing 8 focused tests, 117 broader G61/readiness tests, and 5362 full-suite tests" in text
    assert "V1_CANDIDATE_HARNESS_QUICKSTART.md" in text
    assert "latest quickstart artifact refresh evidence passing 7 focused tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5364 full-suite tests" in text
    assert "does not override the current G61 operator-decision blocker" in text
    assert "81eed8c4067b1a73885bbc79003ea5870b1604a2" in text
    assert "548b6d6aa6cde98b261e867c0c2db86ddbfa83dc" in text
    assert "a05faea14ab24341b4b4567967911e33e51ce88a" in text
    assert "525648d1d7ef536dc89e793095db89f69728c015" in text
    assert "93 passed in 0.27s" in text
    assert "13 passed in 0.04s" in text
    assert "4 passed, 1 Starlette/httpx deprecation warning" in text
    assert "4698 passed" in text
    assert "No V1-G55 implementation approval." in text
    assert "No product readiness, production readiness, or V1.0 completion." in text
    assert fixture["consumer_branches"]["public_sparkbot"]["manual_compare_url"] in text
    assert (
        "Current next step is to record exactly one valid cutover operator choice in `docs/readiness/V1_RELEASE_CANDIDATE_CUTOVER_AUTHORIZATION_PACKET.md`, "
        "then execute the runbook before any branch, tag, cutover, or readiness claim. Stop before additional implementation "
        "beyond the bounded proof already recorded."
        in text
    )
