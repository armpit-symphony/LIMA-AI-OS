"""Static checks for the V1 Arc Phase-1 readiness bundle audit."""

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
    / "v1_arc_phase1_readiness_bundle_audit.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_arc_phase1_readiness_bundle_audit_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["audit_id"] == "v1_arc_phase1_readiness_bundle_audit"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["date"] == "2026-06-19"
    assert fixture["audit_branch"] == "audit-v1-arc-phase1-readiness-bundle"
    assert fixture["source_lima_commit_before_audit"] == (
        "bc21c09edb9464444af77f812c4839a75bfab2ff"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_arc_phase1_readiness_bundle_records_consumer_checkpoint() -> None:
    checkpoint = _load_fixture()["consumer_checkpoint"]

    assert checkpoint == {
        "repository": "armpit-symphony/Arc-Bot-shell",
        "branch": "arc-bot-runtime-ui-scaffold-foundation-phase-chain",
        "commit": "8b2002036bda180d6a0d6a01e67c1316f77623c1",
        "source_commit_before_checkpoint": (
            "6cce9c125359822cce060a248924fec63a8ef1f8"
        ),
        "pr_url": (
            "https://github.com/armpit-symphony/Arc-Bot-shell/pull/new/"
            "arc-bot-runtime-ui-scaffold-foundation-phase-chain"
        ),
        "remote_commit_verified": True,
    }


def test_arc_phase1_readiness_bundle_records_expected_artifacts() -> None:
    evidence = set(_load_fixture()["accepted_evidence"])

    assert evidence == {
        ".gitignore",
        "README.md",
        "docs/ROADMAP.md",
        "docs/ROADMAP_PHASE1_BUSINESS_MVP.md",
        "docs/ROADMAP_SCOPE_LOCK_PUNCH_LIST.md",
        "docs/proof_packets/ARC_BOT_PHASE1_CLIENT_CONFIGURATION_MIGRATION_GATE_PACKET.md",
        "docs/proof_packets/ARC_BOT_PHASE1_CLIENT_CONFIGURATION_NO_EXECUTION_PACKET.md",
        "docs/proof_packets/ARC_BOT_PHASE1_MVP_ROADMAP_PACKET.md",
        "docs/proof_packets/ARC_BOT_PHASE1_READINESS_BUNDLE_PACKET.md",
        "docs/proof_packets/ARC_BOT_RUNTIME_UI_SCAFFOLD_PHASE0_SCOPE_LOCK_STATUS_SNAPSHOT_PROOF_PACKET.md",
        "phase1_client_configuration/__init__.py",
        "phase1_client_configuration/configuration.py",
        "phase1_readiness/__init__.py",
        "phase1_readiness/bundle.py",
        "tests/fixtures/arc_bot_phase1_client_configuration_migration_gate_packet.json",
        "tests/fixtures/arc_bot_phase1_client_configuration_no_execution_packet.json",
        "tests/fixtures/arc_bot_phase1_readiness_bundle_projection.json",
        "tests/test_arc_bot_business_mvp_roadmap.py",
        "tests/test_arc_bot_phase1_client_configuration_contracts.py",
        "tests/test_arc_bot_phase1_client_configuration_projection.py",
        "tests/test_arc_bot_phase1_readiness_bundle.py",
        "tests/test_arc_bot_phase1_readiness_bundle_packet.py",
    }


def test_arc_phase1_readiness_bundle_records_validation_results() -> None:
    commands = _load_fixture()["validation_commands"]

    expected = {
        (
            "python -B -m pytest -q "
            "tests\\test_arc_bot_phase1_client_configuration_no_execution.py "
            "-p no:cacheprovider --basetemp=.pytest-arc-client-config",
            "9 passed in 0.02s",
        ),
        (
            "python -B -m pytest -q "
            "tests\\test_arc_bot_phase1_client_configuration_projection.py "
            "-p no:cacheprovider --basetemp=.pytest-arc-client-config-projection",
            "5 passed in 0.02s",
        ),
        (
            "python -B -m pytest -q "
            "tests\\test_arc_bot_phase1_client_configuration_contracts.py "
            "-p no:cacheprovider --basetemp=.pytest-arc-client-config-contracts",
            "4 passed in 0.01s",
        ),
        (
            "python -B -m pytest -q tests\\test_arc_bot_phase1_readiness_bundle.py "
            "tests\\test_arc_bot_phase1_readiness_bundle_packet.py "
            "-p no:cacheprovider --basetemp=.pytest-arc-phase1-readiness",
            "6 passed in 0.04s",
        ),
        (
            "python -B -m pytest -q tests\\test_arc_bot_business_mvp_roadmap.py "
            "tests\\test_arc_bot_foundation_documents.py "
            "-p no:cacheprovider --basetemp=.pytest-arc-mvp-roadmap",
            "2 passed in 0.02s",
        ),
        (
            "python -B -m phase1_client_configuration.configuration --compact",
            "passed with compact JSON and runpy preload warning",
        ),
        (
            "python -B -m phase1_readiness.bundle --compact",
            "passed with compact JSON and runpy preload warning",
        ),
        (
            "python -B -m json.tool "
            "tests\\fixtures\\arc_bot_phase1_client_configuration.json",
            "passed",
        ),
        (
            "python -B -m json.tool "
            "tests\\fixtures\\arc_bot_phase1_client_configuration_no_execution_packet.json",
            "passed",
        ),
        (
            "python -B -m json.tool "
            "tests\\fixtures\\arc_bot_phase1_client_configuration_migration_gate_packet.json",
            "passed",
        ),
        (
            "python -B -m json.tool "
            "tests\\fixtures\\arc_bot_phase1_readiness_bundle_projection.json",
            "passed",
        ),
        (
            "python -B -m json.tool "
            "docs\\contracts\\schemas\\arc_bot_client_configuration.schema.json",
            "passed",
        ),
        (
            "python -B -m compileall phase0_runtime_ui_scaffold "
            "phase1_business_shell_inventory phase1_client_configuration "
            "phase1_readiness",
            "passed",
        ),
        (
            "python -B -m pytest -q tests -p no:cacheprovider "
            "--basetemp=.pytest-arc-full-v2",
            "216 passed in 0.40s",
        ),
        ("git diff --check", "passed"),
        ("git diff --cached --check", "passed before commit"),
    }

    assert {(item["command"], item["result"]) for item in commands} == expected
    assert {item["repo"] for item in commands} == {"C:\\Users\\limap\\Arc-Bot-shell"}


def test_arc_phase1_readiness_bundle_records_validation_notes() -> None:
    notes = _load_fixture()["validation_notes"]

    assert notes == {
        "prior_broad_full_suite_temp_cleanup_error": True,
        "prior_broad_full_suite_error_reason": (
            "existing .pytest-arc-full directory was ACL-locked on local Windows host"
        ),
        "fresh_repo_local_basetemp_full_suite_passed": True,
    }


def test_arc_phase1_readiness_bundle_scope_flags() -> None:
    scope = _load_fixture()["scope_audit"]

    for key in (
        "arc_branch_saved_and_pushed",
        "arc_planning_docs_proof_fixture_tests_projection_helpers_only",
        "readiness_bundle_fixture_backed",
        "readiness_bundle_read_only",
        "client_configuration_projection_fixture_backed",
        "client_configuration_projection_read_only",
        "client_configuration_projection_phase_gated",
        "migration_gates_require_guardian_review",
        "migration_gates_require_evidence_refs",
        "migration_gates_require_rollback_metadata",
        "migration_gates_require_future_approval",
        "lima_docs_tests_fixtures_only",
    ):
        assert scope[key] is True

    for key in (
        "lima_runtime_files_changed",
        "lima_public_api_exports_changed",
        "public_sparkbot_files_changed",
        "sparkbot_shell_files_changed",
        "arc_consumer_production_runtime_integration_approved",
        "v1_g55_implementation_approved_or_started",
    ):
        assert scope[key] is False


def test_arc_phase1_readiness_bundle_boundaries_are_false() -> None:
    for key, value in _load_fixture()["boundary_results"].items():
        assert value is False, key


def test_arc_phase1_readiness_bundle_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["audit"]).read_text(encoding="utf-8")

    assert "# V1 Arc Phase-1 Readiness Bundle Audit" in text
    assert "`audit-v1-arc-phase1-readiness-bundle`" in text
    assert "bc21c09edb9464444af77f812c4839a75bfab2ff" in text
    assert "8b2002036bda180d6a0d6a01e67c1316f77623c1" in text
    assert "arc-bot-runtime-ui-scaffold-foundation-phase-chain" in text
    assert "Phase-1 business MVP roadmap" in text
    assert "client-configuration migration gates" in text
    assert "216 tests" in text
    assert "Live model/provider calls added: no." in text
    assert "V1-G55 implementation approved or started by this audit: no." in text
    assert "not product readiness" in text
