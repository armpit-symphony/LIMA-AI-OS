"""Nested metadata coverage evidence review tests for Phase 34.1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_34_1_NESTED_METADATA_COVERAGE_EVIDENCE_REVIEW.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_34_1_nested_metadata_coverage_evidence_review.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_34_1_is_docs_tests_fixtures_only_evidence() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "34.1"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_implementation_approved"] is False
    assert fixture["runtime_files_changed"] == []
    assert fixture["tests_support_changed"] is False
    assert "does not implement runtime behavior" in phase_doc


def test_phase_34_1_evidence_sources_exist() -> None:
    for source in _load_json(PHASE_FIXTURE_PATH)["evidence_sources"]:
        assert (REPO_ROOT / source).exists()


def test_phase_34_1_confirms_all_nested_metadata_coverage() -> None:
    coverage = set(_load_json(PHASE_FIXTURE_PATH)["coverage_confirmed"])
    assert coverage == {
        "nested_authority_bypass_wording",
        "nested_sparkbot_wiring_claims",
        "nested_humaninput_bridge_claims",
        "nested_live_adapter_claims",
        "nested_shell_browser_network_file_mutation_claims",
        "nested_robotics_physical_world_claims",
        "nested_external_service_background_work_claims",
        "malformed_nested_metadata",
        "unknown_nested_values",
    }


def test_phase_34_1_records_safety_evidence() -> None:
    evidence = _load_json(PHASE_FIXTURE_PATH)["safety_evidence"]
    assert evidence["authority_bypass_wording_blocks_or_remains_safe"] is True
    assert evidence["sparkbot_humaninput_live_adapter_claims_inert"] is True
    assert evidence["shell_browser_network_file_claims_inert"] is True
    assert evidence["robotics_physical_world_claims_inert"] is True
    assert evidence["external_background_claims_inert"] is True
    assert evidence["malformed_nested_metadata_safe"] is True
    assert evidence["unknown_nested_values_safe"] is True
    assert evidence["inspection_deterministic_and_non_mutating"] is True
    assert evidence["safety_booleans_remain_denied"] is True


def test_no_phase_34_1_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_34_1*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_34_1*"))
