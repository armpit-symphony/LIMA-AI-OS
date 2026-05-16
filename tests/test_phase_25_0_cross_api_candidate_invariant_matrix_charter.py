"""Cross-API candidate invariant matrix charter tests for Phase 25.0."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_25_0_CROSS_API_CANDIDATE_INVARIANT_MATRIX_CHARTER.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_25_0_cross_api_candidate_invariant_matrix_charter.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_25_0_is_test_docs_fixtures_only_charter() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "25.0"
    assert fixture["runtime_code_modified"] is False
    assert fixture["scope"] == "test_docs_fixtures_only"
    assert "does not implement runtime behavior" in phase_doc
    assert "does not modify `lima/`" in phase_doc


def test_matrix_apis_are_declared() -> None:
    apis = set(_load_json(PHASE_FIXTURE_PATH)["matrix_apis"])
    assert "build_intake_candidate" in apis
    assert "normalize_candidate_status" in apis
    assert "validate_candidate" in apis
    assert "provenance_hardening_behavior" in apis


def test_matrix_invariants_are_declared() -> None:
    invariants = set(_load_json(PHASE_FIXTURE_PATH)["matrix_invariants"])
    assert "execution_allowed_remains_false" in invariants
    assert "side_effects_allowed_remains_false" in invariants
    assert "approval_state_never_approved" in invariants
    assert "provenance_preserved_or_safely_rejected" in invariants
    assert "malformed_input_safe" in invariants
    assert "unknown_status_safe" in invariants
    assert "suspicious_provenance_safe" in invariants
    assert "bypass_wording_does_not_change_safety" in invariants


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


def test_phase_doc_gates_phase_25_1_and_runtime_expansion() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "Phase 25.1 may add synthetic matrix fixtures only" in phase_doc
    assert "Runtime expansion remains blocked" in phase_doc


def test_no_phase_25_0_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_25_0*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_25_0*"))
