"""Static checks for the V1 Arc runtime gating readiness integration audit."""

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
    / "v1_arc_runtime_gating_readiness_integration_audit.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_arc_runtime_gating_readiness_integration_audit_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["audit_id"] == "v1_arc_runtime_gating_readiness_integration_audit"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["date"] == "2026-06-19"
    assert fixture["audit_branch"] == "audit-v1-arc-runtime-gating-readiness-integration"
    assert fixture["source_lima_commit_before_audit"] == (
        "380d69be5a4d0993b4deb98f844b3bc838073224"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_arc_runtime_gating_readiness_integration_records_consumer_checkpoint() -> None:
    checkpoint = _load_fixture()["consumer_checkpoint"]

    assert checkpoint == {
        "repository": "armpit-symphony/Arc-Bot-shell",
        "branch": "arc-bot-runtime-ui-scaffold-foundation-phase-chain",
        "commit": "3004367aa7aa96b4b2518c0e3783cf5afba979c0",
        "source_commit_before_checkpoint": (
            "a3f0ffc6713358cf5b9fbd40bfd402b8a12d9b1f"
        ),
        "remote_commit_verified": True,
    }


def test_arc_runtime_gating_readiness_integration_records_expected_artifacts() -> None:
    evidence = set(_load_fixture()["accepted_evidence"])

    assert evidence == {
        "docs/ROADMAP_SCOPE_LOCK_PUNCH_LIST.md",
        "docs/proof_packets/ARC_BOT_PHASE1_READINESS_BUNDLE_PACKET.md",
        "phase1_readiness/bundle.py",
        "tests/fixtures/arc_bot_phase1_readiness_bundle_projection.json",
        "tests/test_arc_bot_phase1_readiness_bundle.py",
        "tests/test_arc_bot_phase1_readiness_bundle_packet.py",
    }


def test_arc_runtime_gating_readiness_integration_records_gate_state() -> None:
    fixture = _load_fixture()

    assert fixture["integrated_projection"] == "runtime_authority_gating"
    assert fixture["required_future_gates"] == [
        "approval_token_lineage",
        "connector_authority_approval",
        "evidence_and_rollback_gate",
        "guardian_runtime_authority_approval",
        "production_readiness_approval",
    ]


def test_arc_runtime_gating_readiness_integration_records_validation_results() -> None:
    commands = _load_fixture()["validation_commands"]

    expected = {
        (
            "python -B -m phase1_readiness.bundle --snapshot-path "
            "tests\\fixtures\\arc_bot_phase1_readiness_bundle_projection.json",
            "passed with rendered JSON and runpy preload warning",
        ),
        (
            "python -B -m pytest -q tests\\test_arc_bot_phase1_readiness_bundle.py "
            "tests\\test_arc_bot_phase1_readiness_bundle_packet.py "
            "tests\\test_arc_bot_phase1_runtime_authority_gating.py "
            "-p no:cacheprovider --basetemp=.pytest-arc-readiness-gating-integration-v2",
            "15 passed in 0.07s",
        ),
        (
            "python -B -m json.tool "
            "tests\\fixtures\\arc_bot_phase1_readiness_bundle_projection.json",
            "passed",
        ),
        (
            "python -B -m compileall phase1_readiness phase1_runtime_authority_gating",
            "passed",
        ),
        ("git diff --check", "passed with line-ending warnings only"),
        (
            "python -B -m pytest -q tests -p no:cacheprovider "
            "--basetemp=.pytest-arc-full-v5",
            "225 passed in 0.41s",
        ),
        (
            "git show --check --stat --oneline HEAD",
            "passed for committed checkpoint 3004367",
        ),
    }

    assert {(item["command"], item["result"]) for item in commands} == expected
    assert {item["repo"] for item in commands} == {"C:\\Users\\limap\\Arc-Bot-shell"}


def test_arc_runtime_gating_readiness_integration_records_validation_notes() -> None:
    notes = _load_fixture()["validation_notes"]

    assert notes == {
        "runpy_preload_warning_observed": True,
        "git_line_ending_warnings_observed": True,
        "fresh_repo_local_basetemp_full_suite_passed": True,
    }


def test_arc_runtime_gating_readiness_integration_scope_flags() -> None:
    scope = _load_fixture()["scope_audit"]

    for key in (
        "arc_branch_saved_and_pushed",
        "arc_readiness_bundle_docs_fixture_tests_helper_only",
        "runtime_authority_gating_default_in_readiness_bundle",
        "runtime_authority_gating_explicit_exclusion_supported",
        "runtime_authority_gating_fixture_backed",
        "required_future_gates_remain_unresolved",
        "readiness_fixture_deterministic_json_valid",
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


def test_arc_runtime_gating_readiness_integration_boundaries_are_false() -> None:
    for key, value in _load_fixture()["boundary_results"].items():
        assert value is False, key


def test_arc_runtime_gating_readiness_integration_text_matches_fixture() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["audit"]).read_text(encoding="utf-8")

    assert "# V1 Arc Runtime Gating Readiness Integration Audit" in text
    assert "`audit-v1-arc-runtime-gating-readiness-integration`" in text
    assert "380d69be5a4d0993b4deb98f844b3bc838073224" in text
    assert "3004367aa7aa96b4b2518c0e3783cf5afba979c0" in text
    assert "a3f0ffc6713358cf5b9fbd40bfd402b8a12d9b1f" in text
    assert "runtime authority gating projection" in text
    assert "15 tests" in text
    assert "225 tests" in text
    assert "Live model/provider calls added: no." in text
    assert "V1-G55 implementation approved or started by this audit: no." in text
    assert "not product readiness" in text
