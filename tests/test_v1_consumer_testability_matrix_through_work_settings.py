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
