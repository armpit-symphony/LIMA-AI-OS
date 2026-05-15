"""Static checks for Phase 18.0 regression hardening charter."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_18_0_REGRESSION_HARDENING_CHARTER.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_18_0_regression_hardening_charter.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_test_only_regression_charter() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "18.0"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False


def test_lane_scope_targets_existing_non_executing_boundaries() -> None:
    scope = set(_load_json(PHASE_FIXTURE_PATH)["lane_scope"])
    assert "existing_non_executing_candidate_apis" in scope
    assert "acceptance_gate_boundaries" in scope
    assert "phase_5_humaninput_runtime_bridge_gating" in scope
    assert "absence_of_sparkbot_wiring_and_live_adapters" in scope


def test_planned_phase_eighteen_work_is_listed() -> None:
    planned = set(_load_json(PHASE_FIXTURE_PATH)["planned_phase_18_work"])
    assert planned == {
        "phase_18_1_candidate_api_regression_tests",
        "phase_18_2_acceptance_boundary_regression_fixtures",
        "phase_18_3_forbidden_integration_regression_tests",
        "phase_18_4_regression_hardening_readiness_review",
        "phase_18_5_phase_18_archive_closeout",
    }


def test_runtime_and_integration_scope_is_not_approved() -> None:
    not_approved = set(_load_json(PHASE_FIXTURE_PATH)["not_approved"])
    assert "runtime_implementation" in not_approved
    assert "lima_changes" in not_approved
    assert "tests_support_changes" in not_approved
    assert "sparkbot_integration" in not_approved
    assert "humaninput_runtime_bridge" in not_approved
    assert "execution" in not_approved
    assert "audit_persistence" in not_approved
    assert "physical_world_behavior" in not_approved


def test_phase_document_preserves_boundaries() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "does not change runtime behavior" in phase_doc
    assert "Phase 18.0 does not approve runtime implementation" in phase_doc


def test_no_phase_eighteen_zero_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_18_0*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_18_0*"))
