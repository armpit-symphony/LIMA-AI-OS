"""Coverage review tests for Phase 26.1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_26_1_CROSS_API_INVARIANT_COVERAGE_REVIEW.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_26_1_cross_api_invariant_coverage_review.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_26_1_is_coverage_review_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "26.1"
    assert fixture["runtime_code_modified"] is False
    assert "coverage review only" in phase_doc
    assert "does not implement runtime behavior" in phase_doc


def test_confirmed_coverage_lists_cross_api_invariants() -> None:
    coverage = set(_load_json(PHASE_FIXTURE_PATH)["confirmed_coverage"])
    assert "candidate_construction_non_executing" in coverage
    assert "candidate_status_normalization_preserves_non_execution" in coverage
    assert "candidate_validation_preserves_non_execution" in coverage
    assert "valid_provenance_preserved" in coverage
    assert "malformed_candidate_safe" in coverage
    assert "unknown_status_blocked_invalid_or_needs_review" in coverage
    assert "suspicious_provenance_rejected_blocked_invalid_or_needs_review" in coverage
    assert "stale_replayed_signal_safe_where_supported" in coverage
    assert "bypass_wording_does_not_approve" in coverage
    assert "risky_action_categories_do_not_become_executable" in coverage


def test_boundary_coverage_keeps_forbidden_integrations_absent() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_coverage"]
    assert boundary["sparkbot_wiring_absent"] is True
    assert boundary["humaninput_runtime_bridge_absent"] is True
    assert boundary["live_adapter_absent"] is True
    assert boundary["approval_enforcement_absent"] is True
    assert boundary["execution_absent"] is True
    assert boundary["dispatch_absent"] is True
    assert boundary["audit_persistence_absent"] is True
    assert boundary["physical_world_behavior_absent"] is True
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True


def test_static_limitations_do_not_approve_runtime_expansion() -> None:
    limitations = set(_load_json(PHASE_FIXTURE_PATH)["limitations"])
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "static_docs_tests_fixtures_review_only" in limitations
    assert "does_not_approve_future_runtime_expansion" in limitations
    assert "does_not_modify_candidate_runtime_apis" in limitations
    assert "does not approve runtime expansion" in phase_doc


def test_next_phase_is_gap_review() -> None:
    assert _load_json(PHASE_FIXTURE_PATH)["next_phase"] == "26.2"
    assert "Continue only to Phase 26.2" in PHASE_DOC_PATH.read_text(encoding="utf-8")


def test_no_phase_26_1_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_26_1*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_26_1*"))
