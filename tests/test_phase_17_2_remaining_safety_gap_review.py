"""Static checks for Phase 17.2 remaining safety gap review."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_17_2_REMAINING_SAFETY_GAP_REVIEW.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_17_2_remaining_safety_gap_review.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_gap_review_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "17.2"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False


def test_remaining_gaps_capture_static_and_runtime_limits() -> None:
    gaps = set(_load_json(PHASE_FIXTURE_PATH)["remaining_gaps"])
    assert "future_runtime_file_coverage_must_be_re_evaluated_per_slice" in gaps
    assert "static_checks_are_not_runtime_policy_enforcement" in gaps
    assert "contract_tests_cover_current_non_executing_candidate_apis_only" in gaps
    assert "synthetic_threat_fixtures_are_not_live_integration_traffic" in gaps
    assert "approval_semantics_remain_non_enforcing" in gaps
    assert "audit_persistence_remains_unimplemented" in gaps


def test_runtime_expansion_blockers_are_explicit() -> None:
    blockers = set(_load_json(PHASE_FIXTURE_PATH)["runtime_expansion_blockers"])
    assert "exact_runtime_file_touch_scope_required" in blockers
    assert "acceptance_tests_for_next_slice_required" in blockers
    assert "rollback_and_audit_proof_required" in blockers
    assert "approval_semantics_decision_required" in blockers
    assert "phase_5_humaninput_runtime_bridge_gating_required" in blockers


def test_blocked_future_work_remains_blocked() -> None:
    blocked = _load_json(PHASE_FIXTURE_PATH)["blocked_future_work"]
    assert blocked["runtime_expansion"] is True
    assert blocked["sparkbot_integration"] is True
    assert blocked["humaninput_runtime_bridge"] is True
    assert blocked["live_adapters"] is True
    assert blocked["approval_enforcement"] is True
    assert blocked["audit_persistence"] is True
    assert blocked["physical_world_behavior"] is True


def test_phase_document_preserves_boundary_language() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "does not change runtime behavior" in phase_doc
    assert "Approval semantics remain non-enforcing" in phase_doc
    assert "Phase 17.3 should compare" in phase_doc


def test_no_phase_seventeen_two_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_17_2*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_17_2*"))
