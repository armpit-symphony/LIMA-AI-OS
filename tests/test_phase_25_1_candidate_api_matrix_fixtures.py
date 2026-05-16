"""Candidate API matrix fixture tests for Phase 25.1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_25_1_CANDIDATE_API_MATRIX_FIXTURES.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_25_1_candidate_api_matrix_fixtures.json"
)
CASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_25_1_candidate_api_matrix_cases.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_25_1_is_test_docs_fixtures_only_fixture_work() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "25.1"
    assert fixture["runtime_code_modified"] is False
    assert "test/docs/fixtures-only fixture work" in phase_doc
    assert "does not implement runtime behavior" in phase_doc


def test_matrix_case_fixture_is_linked_and_parses() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    cases = _load_json(CASE_FIXTURE_PATH)["cases"]
    assert fixture["case_fixture"] == (
        "tests/fixtures/runtime_extraction/phase_25_1_candidate_api_matrix_cases.json"
    )
    assert cases
    assert all("case_id" in case for case in cases)


def test_required_matrix_cases_are_present() -> None:
    case_ids = {case["case_id"] for case in _load_json(CASE_FIXTURE_PATH)["cases"]}
    assert "valid_low_risk_intake" in case_ids
    assert "unknown_candidate_status" in case_ids
    assert "suspicious_provenance_authority_claim" in case_ids
    assert "bypass_wording_shell_request" in case_ids
    assert "stale_candidate" in case_ids
    assert "replayed_candidate" in case_ids
    assert "raw_humaninput_like_intake" in case_ids
    assert "browser_network_attempt" in case_ids
    assert "file_mutation_attempt" in case_ids
    assert "robotics_physical_world_attempt" in case_ids


def test_matrix_cases_declare_expected_outcomes() -> None:
    for case in _load_json(CASE_FIXTURE_PATH)["cases"]:
        assert case["expected_build"] in {"ok", "error"}
        if case["expected_build"] == "ok":
            assert case["expected_status"] in {"proposed", "needs_review", "blocked"}
            assert case["expected_validation_state"] in {"valid", "invalid"}
        else:
            assert "expected_error" in case


def test_boundary_results_show_no_forbidden_behavior() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["humaninput_runtime_bridge_added"] is False
    assert boundary["live_adapter_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["approval_enforcement_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_behavior_added"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True


def test_no_phase_25_1_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_25_1*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_25_1*"))
