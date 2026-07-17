"""Static checks for the V1 Arc Phase-1 inventory snapshot exports audit."""

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
    / "v1_arc_phase1_inventory_snapshot_exports_audit.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_arc_phase1_inventory_snapshot_exports_audit_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["audit_id"] == "v1_arc_phase1_inventory_snapshot_exports_audit"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["date"] == "2026-06-19"
    assert fixture["audit_branch"] == "audit-v1-arc-phase1-inventory-snapshot-exports"
    assert fixture["source_lima_commit_before_audit"] == (
        "8fb157ef0d0d62de0c8f797a073eeccc6de8e5d0"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_arc_phase1_inventory_snapshot_exports_records_consumer_checkpoint() -> None:
    checkpoint = _load_fixture()["consumer_checkpoint"]

    assert checkpoint == {
        "repository": "armpit-symphony/Arc-Bot-shell",
        "branch": "arc-bot-runtime-ui-scaffold-foundation-phase-chain",
        "commit": "0a71a476e3528b66ca68b7218d9c9de1a8c96240",
        "source_commit_before_checkpoint": "0a23848cf1b05195e58c1b4b4b29e0d8d4e3af8e",
        "pr_url": (
            "https://github.com/armpit-symphony/Arc-Bot-shell/pull/new/"
            "arc-bot-runtime-ui-scaffold-foundation-phase-chain"
        ),
        "remote_commit_verified": True,
    }


def test_arc_phase1_inventory_snapshot_exports_records_expected_artifacts() -> None:
    evidence = set(_load_fixture()["accepted_evidence"])

    assert evidence == {
        ".gitignore",
        "README.md",
        "docs/ROADMAP.md",
        "docs/ROADMAP_SCOPE_LOCK_PUNCH_LIST.md",
        "docs/proof_packets/ARC_BOT_PHASE1_BUSINESS_INVENTORY_PROOF_PACKET.md",
        (
            "docs/proof_packets/"
            "ARC_BOT_RUNTIME_UI_SCAFFOLD_PHASE0_SCOPE_LOCK_STATUS_SNAPSHOT_PROOF_PACKET.md"
        ),
        "phase0_runtime_ui_scaffold/__init__.py",
        "phase0_runtime_ui_scaffold/guardian_suite_seam.py",
        "phase0_runtime_ui_scaffold/phase2_runtime_control.py",
        "phase0_runtime_ui_scaffold/phase_chain.py",
        "phase0_runtime_ui_scaffold/preview.py",
        "phase0_runtime_ui_scaffold/read_feed.py",
        "phase0_runtime_ui_scaffold/runtime_consumer.py",
        "phase0_runtime_ui_scaffold/runtime_control_consumer.py",
        "phase1_business_shell_inventory/__init__.py",
        "phase1_business_shell_inventory/inventory.py",
        "tests/fixtures/arc_bot_phase1_business_inventory.json",
        "tests/test_arc_bot_phase1_business_shell_inventory.py",
        "tests/test_arc_bot_runtime_ui_scaffold_guardian_suite_seam.py",
        "tests/test_arc_bot_runtime_ui_scaffold_phase1_read_feed_preview.py",
        "tests/test_arc_bot_runtime_ui_scaffold_phase_chain.py",
        "tests/test_arc_bot_runtime_ui_scaffold_preview.py",
        "tests/test_arc_bot_runtime_ui_scaffold_runtime_consumer.py",
        "tests/test_arc_bot_runtime_ui_scaffold_runtime_control_consumer.py",
    }


def test_arc_phase1_inventory_snapshot_exports_records_validation_results() -> None:
    commands = _load_fixture()["validation_commands"]

    expected = {
        (
            "python -B -m pytest -q "
            "tests\\test_arc_bot_runtime_ui_scaffold_phase_chain.py "
            "tests\\test_arc_bot_runtime_ui_scaffold_preview.py "
            "tests\\test_arc_bot_runtime_ui_scaffold_guardian_suite_seam.py "
            "tests\\test_arc_bot_runtime_ui_scaffold_phase1_read_feed_preview.py "
            "tests\\test_arc_bot_runtime_ui_scaffold_runtime_consumer.py "
            "tests\\test_arc_bot_runtime_ui_scaffold_runtime_control_consumer.py "
            "tests\\test_arc_bot_phase1_business_shell_inventory.py "
            "-p no:cacheprovider --basetemp=.pytest-arc-focused",
            "49 passed in 0.16s",
        ),
        (
            "python -B -m pytest -q -p no:cacheprovider --basetemp=.pytest-arc-full",
            "184 passed in 0.38s",
        ),
        (
            "python -B -m compileall phase0_runtime_ui_scaffold "
            "phase1_business_shell_inventory",
            "passed",
        ),
        (
            "python -B -m json.tool "
            "tests\\fixtures\\arc_bot_phase1_business_inventory.json",
            "passed",
        ),
        (
            "python -B -m phase0_runtime_ui_scaffold.phase_chain "
            "--emit-status-snapshot --with-guardian-suite-seam --compact",
            "passed_with_compact_json_and_known_runpy_warning",
        ),
        (
            "python -B -m phase1_business_shell_inventory.inventory --compact",
            "passed_with_compact_json_and_known_runpy_warning",
        ),
        ("git diff --check", "passed"),
        ("git diff --cached --check", "passed before commit"),
    }

    assert {(item["command"], item["result"]) for item in commands} == expected
    assert {item["repo"] for item in commands} == {"C:\\Users\\limap\\Arc-Bot-shell"}


def test_arc_phase1_inventory_snapshot_exports_scope_flags() -> None:
    scope = _load_fixture()["scope_audit"]

    for key in (
        "arc_branch_saved_and_pushed",
        "arc_readonly_scaffold_exporters_added",
        "arc_phase1_business_inventory_readonly_planning_added",
        "arc_pytest_artifacts_ignored",
        "operator_invoked_snapshot_file_export_added",
        "phase1_business_inventory_phase_gated",
        "phase1_business_inventory_runtime_authority_blocked",
        "lima_docs_tests_fixtures_only",
    ):
        assert scope[key] is True

    for key in (
        "hidden_background_file_writes_added",
        "runtime_customer_file_mutation_authority_added",
        "lima_runtime_files_changed",
        "lima_public_api_exports_changed",
        "public_sparkbot_files_changed",
        "sparkbot_shell_files_changed",
        "arc_consumer_production_runtime_integration_approved",
        "v1_g55_implementation_approved_or_started",
    ):
        assert scope[key] is False


def test_arc_phase1_inventory_snapshot_exports_boundaries_are_false() -> None:
    for key, value in _load_fixture()["boundary_results"].items():
        assert value is False, key


def test_arc_phase1_inventory_snapshot_exports_records_known_warnings() -> None:
    warnings = set(_load_fixture()["known_status_warnings"])

    assert warnings == {
        (
            "Arc-Bot-shell Python -m execution emits a known runpy warning caused by "
            "package-level re-exports."
        ),
        (
            "Repo-local pytest basetemp paths were used to avoid the Windows global "
            "temp ACL issue."
        ),
    }


def test_arc_phase1_inventory_snapshot_exports_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["audit"]).read_text(encoding="utf-8")

    assert "# V1 Arc Phase-1 Inventory Snapshot Exports Audit" in text
    assert "`audit-v1-arc-phase1-inventory-snapshot-exports`" in text
    assert "8fb157ef0d0d62de0c8f797a073eeccc6de8e5d0" in text
    assert "0a71a476e3528b66ca68b7218d9c9de1a8c96240" in text
    assert "arc-bot-runtime-ui-scaffold-foundation-phase-chain" in text
    assert "49 tests" in text
    assert "184 tests" in text
    assert "Live model calls added by Arc checkpoint: no." in text
    assert "V1-G55 implementation approved or started by this audit: no." in text
    assert "not product readiness" in text
