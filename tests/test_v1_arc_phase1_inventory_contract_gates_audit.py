"""Static checks for the V1 Arc Phase-1 inventory contract gates audit."""

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
    / "v1_arc_phase1_inventory_contract_gates_audit.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_arc_phase1_inventory_contract_gates_audit_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["audit_id"] == "v1_arc_phase1_inventory_contract_gates_audit"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["date"] == "2026-06-19"
    assert fixture["audit_branch"] == "audit-v1-arc-phase1-inventory-contract-gates"
    assert fixture["source_lima_commit_before_audit"] == (
        "4fcb2868dcc87145ff1db6c6c5670cde2c4a2633"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_arc_phase1_inventory_contract_gates_records_consumer_checkpoint() -> None:
    checkpoint = _load_fixture()["consumer_checkpoint"]

    assert checkpoint == {
        "repository": "armpit-symphony/Arc-Bot-shell",
        "branch": "arc-bot-runtime-ui-scaffold-foundation-phase-chain",
        "commit": "e8bb9d96bf2015d4eb927781580cd76bd89524fe",
        "source_commit_before_checkpoint": "0a71a476e3528b66ca68b7218d9c9de1a8c96240",
        "pr_url": (
            "https://github.com/armpit-symphony/Arc-Bot-shell/pull/new/"
            "arc-bot-runtime-ui-scaffold-foundation-phase-chain"
        ),
        "remote_commit_verified": True,
    }


def test_arc_phase1_inventory_contract_gates_records_expected_artifacts() -> None:
    evidence = set(_load_fixture()["accepted_evidence"])

    assert evidence == {
        "README.md",
        "docs/ROADMAP.md",
        "docs/contracts/schemas/arc_bot_phase1_business_inventory.schema.json",
        "docs/proof_packets/ARC_BOT_PHASE1_BUSINESS_INVENTORY_MIGRATION_GATE_PACKET.md",
        "docs/proof_packets/ARC_BOT_PHASE1_BUSINESS_INVENTORY_PROOF_PACKET.md",
        "docs/wireframes/ARC_BOT_PHASE1_BUSINESS_INVENTORY_WIREFRAMES.md",
        "tests/fixtures/arc_bot_phase1_business_inventory_migration_gate_packet.json",
        "tests/test_arc_bot_phase1_business_inventory_contracts.py",
    }


def test_arc_phase1_inventory_contract_gates_records_validation_results() -> None:
    commands = _load_fixture()["validation_commands"]

    expected = {
        (
            "python -B -m pytest -q "
            "tests\\test_arc_bot_phase1_business_inventory_contracts.py "
            "tests\\test_arc_bot_phase1_business_shell_inventory.py "
            "-p no:cacheprovider --basetemp=.pytest-arc-phase1-contracts",
            "12 passed in 0.05s",
        ),
        (
            "python -B -m pytest -q -p no:cacheprovider --basetemp=.pytest-arc-full",
            "191 passed in 0.38s",
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
            "python -B -m json.tool "
            "tests\\fixtures\\arc_bot_phase1_business_inventory_migration_gate_packet.json",
            "passed",
        ),
        (
            "python -B -m json.tool "
            "docs\\contracts\\schemas\\arc_bot_phase1_business_inventory.schema.json",
            "passed",
        ),
        ("git diff --check", "passed"),
        ("git diff --cached --check", "passed before commit"),
    }

    assert {(item["command"], item["result"]) for item in commands} == expected
    assert {item["repo"] for item in commands} == {"C:\\Users\\limap\\Arc-Bot-shell"}


def test_arc_phase1_inventory_contract_gates_scope_flags() -> None:
    scope = _load_fixture()["scope_audit"]

    for key in (
        "arc_branch_saved_and_pushed",
        "arc_docs_contracts_schema_wireframe_proof_fixture_tests_only",
        "phase1_inventory_schema_static_only",
        "migration_gates_require_guardian_review",
        "migration_gates_require_evidence_refs",
        "migration_gates_require_rollback_metadata",
        "migration_gates_require_future_approval",
        "lima_docs_tests_fixtures_only",
    ):
        assert scope[key] is True

    for key in (
        "wireframe_frontend_routes_added",
        "wireframe_interactive_controls_added",
        "lima_runtime_files_changed",
        "lima_public_api_exports_changed",
        "public_sparkbot_files_changed",
        "sparkbot_shell_files_changed",
        "arc_consumer_production_runtime_integration_approved",
        "v1_g55_implementation_approved_or_started",
    ):
        assert scope[key] is False


def test_arc_phase1_inventory_contract_gates_boundaries_are_false() -> None:
    for key, value in _load_fixture()["boundary_results"].items():
        assert value is False, key


def test_arc_phase1_inventory_contract_gates_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["audit"]).read_text(encoding="utf-8")

    assert "# V1 Arc Phase-1 Inventory Contract Gates Audit" in text
    assert "`audit-v1-arc-phase1-inventory-contract-gates`" in text
    assert "4fcb2868dcc87145ff1db6c6c5670cde2c4a2633" in text
    assert "e8bb9d96bf2015d4eb927781580cd76bd89524fe" in text
    assert "arc-bot-runtime-ui-scaffold-foundation-phase-chain" in text
    assert "12 tests" in text
    assert "191 tests" in text
    assert "Live model calls added by Arc checkpoint: no." in text
    assert "V1-G55 implementation approved or started by this audit: no." in text
    assert "not product readiness" in text
