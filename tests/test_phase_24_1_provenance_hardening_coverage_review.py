"""Coverage review tests for Phase 24.1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_24_1_PROVENANCE_HARDENING_COVERAGE_REVIEW.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_24_1_provenance_hardening_coverage_review.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_24_1_is_docs_tests_fixtures_only_coverage_review() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "24.1"
    assert fixture["runtime_code_modified"] is False
    assert "docs/tests/fixtures-only coverage review" in phase_doc
    assert "does not implement runtime behavior" in phase_doc


def test_phase_23_provenance_coverage_is_confirmed() -> None:
    coverage = set(_load_json(PHASE_FIXTURE_PATH)["confirmed_coverage"])
    assert "valid_provenance_preserved" in coverage
    assert "missing_provenance_fail_closed" in coverage
    assert "malformed_provenance_fail_closed" in coverage
    assert "stale_provenance_fail_closed" in coverage
    assert "replayed_provenance_fail_closed" in coverage
    assert "suspicious_provenance_authority_claims_fail_closed" in coverage
    assert "bypass_wording_does_not_bypass_safety" in coverage


def test_non_executing_invariant_coverage_is_confirmed() -> None:
    coverage = set(_load_json(PHASE_FIXTURE_PATH)["confirmed_coverage"])
    assert "risky_attempt_metadata_non_executing" in coverage
    assert "execution_allowed_remains_false" in coverage
    assert "side_effects_allowed_remains_false" in coverage
    assert "approval_state_never_approved" in coverage


def test_coverage_limitations_remain_static_and_non_runtime() -> None:
    limitations = set(_load_json(PHASE_FIXTURE_PATH)["coverage_limitations"])
    assert "deterministic_offline_tests_only" in limitations
    assert "does_not_approve_runtime_expansion" in limitations
    assert "does_not_add_runtime_behavior" in limitations


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


def test_phase_doc_gates_phase_24_2_and_runtime_expansion() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "Phase 24.2 may review remaining candidate invariant gaps only" in phase_doc
    assert "Runtime expansion remains blocked" in phase_doc


def test_no_phase_24_1_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_24_1*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_24_1*"))
