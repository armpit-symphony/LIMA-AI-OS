"""Static checks for the V1 Arc runtime UI scope-lock packet audit."""

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
    / "v1_arc_runtime_ui_scope_lock_packet_audit.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_arc_scope_lock_packet_audit_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["audit_id"] == "v1_arc_runtime_ui_scope_lock_packet_audit"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["date"] == "2026-06-19"
    assert fixture["audit_branch"] == "audit-v1-arc-runtime-ui-scope-lock-packet"
    assert fixture["source_lima_commit_before_audit"] == (
        "2d169f3571aa846f39b2191c3949091950664577"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_arc_scope_lock_packet_audit_records_consumer_checkpoint() -> None:
    checkpoint = _load_fixture()["consumer_checkpoint"]

    assert checkpoint == {
        "repository": "armpit-symphony/Arc-Bot-shell",
        "branch": "arc-bot-runtime-ui-scaffold-foundation-phase-chain",
        "commit": "2c14a9bfa892bb7b1ed5043fb3e92044274a6501",
        "source_commit_before_checkpoint": "b714bda6ddfff30750c9522bc706a592f7e43bb9",
        "pr_url": (
            "https://github.com/armpit-symphony/Arc-Bot-shell/pull/new/"
            "arc-bot-runtime-ui-scaffold-foundation-phase-chain"
        ),
    }


def test_arc_scope_lock_packet_audit_records_expected_artifacts() -> None:
    evidence = set(_load_fixture()["accepted_evidence"])

    assert evidence == {
        "README.md",
        "docs/ROADMAP_SCOPE_LOCK_PUNCH_LIST.md",
        "tests/fixtures/arc_bot_runtime_ui_scaffold_phase0_scope_lock_chain_packet.json",
        "tests/test_arc_bot_runtime_ui_scaffold_phase_chain.py",
    }


def test_arc_scope_lock_packet_audit_records_validation_results() -> None:
    commands = _load_fixture()["validation_commands"]

    expected = {
        (
            "python -m json.tool "
            "tests\\fixtures\\arc_bot_runtime_ui_scaffold_phase0_scope_lock_chain_packet.json",
            "passed",
        ),
        (
            "python -B -m pytest -q "
            "tests\\test_arc_bot_runtime_ui_scaffold_phase_chain.py -p no:cacheprovider",
            "5 passed in 0.04s",
        ),
        ("git diff --check", "passed"),
        ("git diff --cached --check", "passed before commit"),
    }

    assert {(item["command"], item["result"]) for item in commands} == expected
    assert {item["repo"] for item in commands} == {"C:\\Users\\limap\\Arc-Bot-shell"}


def test_arc_scope_lock_packet_audit_scope_and_boundaries_are_false() -> None:
    fixture = _load_fixture()

    assert fixture["scope_audit"]["arc_branch_saved_and_pushed"] is True
    assert fixture["scope_audit"]["arc_docs_tests_fixtures_and_existing_test_only"] is True
    assert fixture["scope_audit"]["lima_docs_tests_fixtures_only"] is True
    for key in (
        "lima_runtime_files_changed",
        "lima_public_api_exports_changed",
        "public_sparkbot_files_changed",
        "sparkbot_shell_files_changed",
        "arc_consumer_production_runtime_integration_approved",
        "v1_g55_implementation_approved_or_started",
    ):
        assert fixture["scope_audit"][key] is False

    for key, value in fixture["boundary_results"].items():
        assert value is False, key


def test_arc_scope_lock_packet_audit_records_known_warnings() -> None:
    warnings = set(_load_fixture()["known_status_warnings"])

    assert warnings == {
        (
            "Arc-Bot-shell git status emits: could not open directory "
            "'.pytest_cache/': Permission denied"
        ),
        (
            "Arc-Bot-shell git status emits: could not open directory "
            "'.pytest-tmp/': Permission denied after local pytest --basetemp execution"
        ),
    }


def test_arc_scope_lock_packet_audit_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["audit"]).read_text(encoding="utf-8")

    assert "# V1 Arc Runtime UI Scope Lock Packet Audit" in text
    assert "`audit-v1-arc-runtime-ui-scope-lock-packet`" in text
    assert "2d169f3571aa846f39b2191c3949091950664577" in text
    assert "2c14a9bfa892bb7b1ed5043fb3e92044274a6501" in text
    assert "arc-bot-runtime-ui-scaffold-foundation-phase-chain" in text
    assert "5 tests" in text
    assert "Live model calls added by Arc packet branch: no." in text
    assert "V1-G55 implementation approved or started by this audit: no." in text
    assert "not product readiness" in text
