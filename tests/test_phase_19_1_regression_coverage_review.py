"""Static checks for Phase 19.1 regression coverage review."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_19_1_REGRESSION_COVERAGE_REVIEW.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_19_1_regression_coverage_review.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_docs_tests_fixtures_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "19.1"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False


def test_phase_eighteen_coverage_groups_are_reviewed() -> None:
    groups = set(_load_json(PHASE_FIXTURE_PATH)["reviewed_phase_18_groups"])
    assert groups == {
        "candidate_api_regression_tests",
        "acceptance_boundary_regression_fixtures",
        "forbidden_integration_regression_tests",
        "readiness_and_archive_checks",
    }


def test_coverage_review_includes_key_candidate_boundaries() -> None:
    covered = set(_load_json(PHASE_FIXTURE_PATH)["covered_boundaries"])
    assert "non_executing_candidate_invariants" in covered
    assert "malformed_candidate_safety" in covered
    assert "unknown_status_safety" in covered
    assert "stale_or_replayed_candidate_safety" in covered
    assert "approval_bypass_wording_no_bypass" in covered


def test_coverage_review_includes_forbidden_integration_boundaries() -> None:
    covered = set(_load_json(PHASE_FIXTURE_PATH)["covered_boundaries"])
    assert "sparkbot_integration_absent" in covered
    assert "humaninput_runtime_bridge_absent" in covered
    assert "live_adapter_absent" in covered
    assert "approval_enforcement_execution_dispatch_audit_persistence_absent" in covered


def test_phase_document_preserves_static_limitations_and_gate() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "They do not create runtime enforcement" in phase_doc
    assert "does not approve Phase 20" in phase_doc
    assert "Phase 5 HumanInput runtime bridge remains gated" in phase_doc


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["helper_behavior_changed"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["humaninput_runtime_bridge_added"] is False
    assert boundary["live_adapter_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True
    assert boundary["phase_20_approved"] is False


def test_no_phase_nineteen_one_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_19_1*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_19_1*"))
