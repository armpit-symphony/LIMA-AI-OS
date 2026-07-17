"""Static checks for the V1 Arc Phase-1 runtime authority gating audit."""

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
    / "v1_arc_phase1_runtime_authority_gating_audit.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_arc_phase1_runtime_authority_gating_audit_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["audit_id"] == "v1_arc_phase1_runtime_authority_gating_audit"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["date"] == "2026-06-19"
    assert fixture["audit_branch"] == "audit-v1-arc-phase1-runtime-authority-gating"
    assert fixture["source_lima_commit_before_audit"] == (
        "c76b54aec3dd8f774d8267c666e1e9a0eb2ce1a4"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_arc_phase1_runtime_authority_gating_records_consumer_checkpoint() -> None:
    checkpoint = _load_fixture()["consumer_checkpoint"]

    assert checkpoint == {
        "repository": "armpit-symphony/Arc-Bot-shell",
        "branch": "arc-bot-runtime-ui-scaffold-foundation-phase-chain",
        "commit": "a3f0ffc6713358cf5b9fbd40bfd402b8a12d9b1f",
        "source_commit_before_checkpoint": (
            "8b2002036bda180d6a0d6a01e67c1316f77623c1"
        ),
        "remote_commit_verified": True,
    }


def test_arc_phase1_runtime_authority_gating_records_expected_artifacts() -> None:
    evidence = set(_load_fixture()["accepted_evidence"])

    assert evidence == {
        "README.md",
        "docs/ROADMAP_PHASE1_BUSINESS_MVP.md",
        "docs/proof_packets/ARC_BOT_PHASE1_MVP_ROADMAP_PACKET.md",
        "docs/proof_packets/ARC_BOT_PHASE1_READINESS_BUNDLE_PACKET.md",
        "docs/proof_packets/ARC_BOT_PHASE1_RUNTIME_AUTHORITY_GATING_PACKET.md",
        "phase1_runtime_authority_gating/__init__.py",
        "phase1_runtime_authority_gating/gating.py",
        "tests/fixtures/arc_bot_phase1_runtime_authority_gating_packet.json",
        "tests/test_arc_bot_business_mvp_roadmap.py",
        "tests/test_arc_bot_phase1_readiness_bundle_packet.py",
        "tests/test_arc_bot_phase1_runtime_authority_gating.py",
    }


def test_arc_phase1_runtime_authority_gating_records_required_gates() -> None:
    assert _load_fixture()["required_future_gates"] == [
        "approval_token_lineage",
        "connector_authority_approval",
        "evidence_and_rollback_gate",
        "guardian_runtime_authority_approval",
        "production_readiness_approval",
    ]


def test_arc_phase1_runtime_authority_gating_records_validation_results() -> None:
    commands = _load_fixture()["validation_commands"]

    expected = {
        (
            "python -B -m pytest -q "
            "tests\\test_arc_bot_phase1_runtime_authority_gating.py "
            "tests\\test_arc_bot_business_mvp_roadmap.py "
            "tests\\test_arc_bot_phase1_readiness_bundle_packet.py "
            "-p no:cacheprovider --basetemp=.pytest-arc-runtime-authority-gating-v2",
            "9 passed in 0.05s",
        ),
        (
            "python -B -m phase1_runtime_authority_gating.gating --compact",
            "passed with compact JSON and runpy preload warning",
        ),
        (
            "python -B -m json.tool "
            "tests\\fixtures\\arc_bot_phase1_runtime_authority_gating_packet.json",
            "passed",
        ),
        ("python -B -m compileall phase1_runtime_authority_gating", "passed"),
        (
            "python -B -m pytest -q tests -p no:cacheprovider "
            "--basetemp=.pytest-arc-full-v3",
            "223 passed in 0.41s",
        ),
        ("git diff --check", "passed"),
        ("git diff --cached --check", "passed before commit"),
    }

    assert {(item["command"], item["result"]) for item in commands} == expected
    assert {item["repo"] for item in commands} == {"C:\\Users\\limap\\Arc-Bot-shell"}


def test_arc_phase1_runtime_authority_gating_scope_flags() -> None:
    scope = _load_fixture()["scope_audit"]

    for key in (
        "arc_branch_saved_and_pushed",
        "arc_planning_docs_proof_fixture_tests_projection_helpers_only",
        "runtime_authority_gating_fixture_backed",
        "runtime_authority_gating_read_only",
        "runtime_authority_gating_phase_gated",
        "all_required_future_gates_unresolved",
        "runtime_boundary_flags_all_false",
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


def test_arc_phase1_runtime_authority_gating_boundaries_are_false() -> None:
    for key, value in _load_fixture()["boundary_results"].items():
        assert value is False, key


def test_arc_phase1_runtime_authority_gating_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["audit"]).read_text(encoding="utf-8")

    assert "# V1 Arc Phase-1 Runtime Authority Gating Audit" in text
    assert "`audit-v1-arc-phase1-runtime-authority-gating`" in text
    assert "c76b54aec3dd8f774d8267c666e1e9a0eb2ce1a4" in text
    assert "a3f0ffc6713358cf5b9fbd40bfd402b8a12d9b1f" in text
    assert "all gates unresolved" in text
    assert "223 tests" in text
    assert "Live model/provider calls added: no." in text
    assert "V1-G55 implementation approved or started by this audit: no." in text
    assert "not product readiness" in text
