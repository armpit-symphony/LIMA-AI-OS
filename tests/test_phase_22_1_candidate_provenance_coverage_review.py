"""Static coverage review checks for Phase 22.1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_22_1_CANDIDATE_PROVENANCE_COVERAGE_REVIEW.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_22_1_candidate_provenance_coverage_review.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_22_1_is_docs_tests_fixtures_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "22.1"
    assert fixture["runtime_code_modified"] is False
    assert fixture["boundary_results"]["lima_modified"] is False
    assert fixture["boundary_results"]["tests_support_modified"] is False


def test_coverage_review_lists_existing_protection() -> None:
    covered = set(_load_json(PHASE_FIXTURE_PATH)["covered_areas"])
    assert "valid_provenance_preservation" in covered
    assert "malformed_provenance_rejection_or_invalidation" in covered
    assert "suspicious_authority_wording_blocked_or_invalid" in covered
    assert "non_executing_candidate_invariants" in covered
    assert "no_humaninput_runtime_bridge" in covered


def test_coverage_review_lists_remaining_test_only_limits() -> None:
    limits = set(_load_json(PHASE_FIXTURE_PATH)["coverage_limits"])
    assert "broader_nested_provenance_fixture_cases" in limits
    assert "authority_wording_inside_lists_and_nested_mappings" in limits
    assert "side_by_side_construction_normalization_validation_matrix" in limits
    assert "static_guardrails_for_future_runtime_expansion" in limits


def test_phase_document_keeps_runtime_expansion_blocked() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "docs/tests/fixtures only" in phase_doc
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "does not recommend runtime expansion" in phase_doc


def test_boundary_results_preserve_phase_5_gate() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["humaninput_runtime_bridge_added"] is False
    assert boundary["live_adapter_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["approval_enforcement_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True


def test_no_phase_22_1_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_22_1*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_22_1*"))
