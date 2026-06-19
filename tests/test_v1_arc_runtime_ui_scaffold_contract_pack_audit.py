"""Static checks for the V1 Arc runtime UI scaffold contract pack audit."""

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
    / "v1_arc_runtime_ui_scaffold_contract_pack_audit.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_arc_runtime_ui_scaffold_audit_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["audit_id"] == "v1_arc_runtime_ui_scaffold_contract_pack_audit"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["date"] == "2026-06-19"
    assert fixture["audit_branch"] == "audit-v1-arc-runtime-ui-scaffold-contract-pack"
    assert fixture["source_lima_commit_before_audit"] == (
        "8414b3baa92ad3a1c5fd72c9bbb1dfccac37d83c"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_arc_runtime_ui_scaffold_audit_records_consumer_checkpoint() -> None:
    checkpoint = _load_fixture()["consumer_checkpoint"]

    assert checkpoint == {
        "repository": "armpit-symphony/Arc-Bot-shell",
        "branch": "arc-runtime-ui-scaffold-contract-pack",
        "commit": "f11f726eebcae07f056421bd3ff46ee337c9f708",
        "pr_url": (
            "https://github.com/armpit-symphony/Arc-Bot-shell/pull/new/"
            "arc-runtime-ui-scaffold-contract-pack"
        ),
        "source_commit_before_branch": "a05faea14ab24341b4b4567967911e33e51ce88a",
    }


def test_arc_runtime_ui_scaffold_audit_records_expected_artifacts() -> None:
    evidence = set(_load_fixture()["accepted_evidence"])

    assert evidence == {
        "docs/ROADMAP.md",
        "README.md",
        "docs/OPERATOR_CONSOLE_FOUNDATION.md",
        "docs/contracts/ARC_BOT_OPERATOR_CONSOLE_STATE.md",
        "docs/contracts/schemas/arc_bot_console_state_envelope.schema.json",
        "docs/contracts/schemas/arc_bot_work_queue_state.schema.json",
        "docs/contracts/schemas/arc_bot_runtime_settings_state.schema.json",
        "tests/fixtures/arc_bot_phase0_work_queue_state_snapshot.json",
        "tests/fixtures/arc_bot_phase0_runtime_settings_state_snapshot.json",
        "tests/fixtures/arc_bot_runtime_ui_scaffold_contract_pack.json",
        "tests/test_arc_bot_phase0_scope_lock_runtime_ui.py",
        "tests/test_arc_bot_runtime_ui_scaffold_contracts.py",
        "tests/test_arc_bot_operator_console_work_queue_runtime_settings.py",
    }


def test_arc_runtime_ui_scaffold_audit_records_validation_results() -> None:
    commands = _load_fixture()["validation_commands"]

    expected = {
        (
            "python -m json.tool docs\\contracts\\schemas\\arc_bot_console_state_envelope.schema.json",
            "passed",
        ),
        (
            "python -m json.tool docs\\contracts\\schemas\\arc_bot_work_queue_state.schema.json",
            "passed",
        ),
        (
            "python -m json.tool docs\\contracts\\schemas\\arc_bot_runtime_settings_state.schema.json",
            "passed",
        ),
        (
            "python -m json.tool tests\\fixtures\\arc_bot_runtime_ui_scaffold_contract_pack.json",
            "passed",
        ),
        (
            "python -m pytest -q tests\\test_arc_bot_phase0_scope_lock_runtime_ui.py "
            "tests\\test_arc_bot_runtime_ui_scaffold_contracts.py "
            "tests\\test_arc_bot_operator_console_work_queue_runtime_settings.py "
            "-p no:cacheprovider",
            "13 passed in 0.03s",
        ),
        ("python -B -m pytest -q tests -p no:cacheprovider", "100 passed in 0.14s"),
        ("git diff --check", "passed"),
        ("git diff --cached --check", "passed before commit"),
    }

    assert {(item["command"], item["result"]) for item in commands} == expected
    assert {item["repo"] for item in commands} == {"C:\\Users\\limap\\Arc-Bot-shell"}


def test_arc_runtime_ui_scaffold_audit_scope_and_boundaries_are_false() -> None:
    fixture = _load_fixture()

    assert fixture["scope_audit"]["arc_docs_tests_fixtures_schema_only"] is True
    assert fixture["scope_audit"]["arc_branch_saved_and_pushed"] is True
    assert fixture["scope_audit"]["lima_docs_tests_fixtures_only"] is True
    for key in (
        "lima_runtime_files_changed",
        "lima_public_api_exports_changed",
        "public_sparkbot_files_changed",
        "sparkbot_shell_files_changed",
        "v1_g55_implementation_approved_or_started",
    ):
        assert fixture["scope_audit"][key] is False

    for key, value in fixture["boundary_results"].items():
        assert value is False, key


def test_arc_runtime_ui_scaffold_audit_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["audit"]).read_text(encoding="utf-8")

    assert "# V1 Arc Runtime UI Scaffold Contract Pack Audit" in text
    assert "`audit-v1-arc-runtime-ui-scaffold-contract-pack`" in text
    assert "8414b3baa92ad3a1c5fd72c9bbb1dfccac37d83c" in text
    assert "f11f726eebcae07f056421bd3ff46ee337c9f708" in text
    assert "arc-runtime-ui-scaffold-contract-pack" in text
    assert "100 tests" in text
    assert "13 tests" in text
    assert "Live model calls added by Arc scaffold branch: no." in text
    assert "V1-G55 implementation approved or started by this audit: no." in text
    assert "not product readiness" in text
