"""Static charter checks for Phase 23.0."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_23_0_PROVENANCE_INVARIANT_TEST_HARDENING_CHARTER.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_23_0_provenance_invariant_test_hardening_charter.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_23_0_is_test_only_charter() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "23.0"
    assert fixture["runtime_code_modified"] is False
    assert fixture["approved_lane"] == "test_only_hardening_for_provenance_candidate_invariants"


def test_allowed_write_scope_excludes_runtime_and_support() -> None:
    scope = set(_load_json(PHASE_FIXTURE_PATH)["allowed_write_scope"])
    assert "tests/test_phase_23_*.py" in scope
    assert "tests/fixtures/runtime_extraction/phase_23_*.json" in scope
    assert "docs/PHASE_23_*.md" in scope
    assert "lima/" not in scope
    assert "tests/support/" not in scope


def test_hardening_goals_cover_required_invariants() -> None:
    goals = set(_load_json(PHASE_FIXTURE_PATH)["hardening_goals"])
    assert "valid_provenance_preserved" in goals
    assert "missing_provenance_fails_closed" in goals
    assert "malformed_provenance_fails_closed" in goals
    assert "suspicious_provenance_fails_closed" in goals
    assert "approval_bypass_wording_cannot_change_safety" in goals
    assert "non_executing_invariants_preserved" in goals
    assert "phase_5_runtime_bridge_remains_gated" in goals


def test_phase_document_blocks_runtime_expansion() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "test-only hardening lane" in phase_doc
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "Runtime expansion remains blocked" in phase_doc


def test_boundary_results_show_no_forbidden_behavior() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["humaninput_runtime_bridge_added"] is False
    assert boundary["live_adapter_added"] is False
    assert boundary["approval_enforcement_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_behavior_added"] is False


def test_no_phase_23_0_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_23_0*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_23_0*"))
