"""Static checks for Phase 18.4 regression hardening readiness review."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_18_4_REGRESSION_HARDENING_READINESS_REVIEW.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_18_4_regression_hardening_readiness_review.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_readiness_review_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "18.4"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False


def test_reviewed_phase_eighteen_scope_is_listed() -> None:
    reviewed = set(_load_json(PHASE_FIXTURE_PATH)["reviewed_phase_18_scope"])
    assert reviewed == {
        "phase_18_1_candidate_api_regression_tests",
        "phase_18_2_acceptance_boundary_regression_fixtures",
        "phase_18_3_forbidden_integration_regression_tests",
    }


def test_readiness_finds_archive_ready_but_runtime_blocked() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert "archive_closeout" in fixture["ready_for"]
    not_ready = set(fixture["not_ready_for"])
    assert "runtime_implementation" in not_ready
    assert "lima_changes" in not_ready
    assert "tests_support_changes" in not_ready
    assert "sparkbot_wiring" in not_ready
    assert "humaninput_runtime_bridge" in not_ready
    assert "execution" in not_ready
    assert "audit_persistence" in not_ready
    assert "physical_world_behavior" in not_ready


def test_readiness_findings_confirm_test_only_package() -> None:
    findings = _load_json(PHASE_FIXTURE_PATH)["readiness_findings"]
    assert findings["candidate_api_regression_tests_added"] is True
    assert findings["acceptance_boundary_regression_fixtures_added"] is True
    assert findings["forbidden_integration_regression_tests_added"] is True
    assert findings["tests_are_deterministic_and_offline"] is True
    assert findings["runtime_code_modified"] is False
    assert findings["lima_modified"] is False
    assert findings["tests_support_modified"] is False


def test_phase_document_preserves_boundaries_and_next_step() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "does not change runtime behavior" in phase_doc
    assert "Phase 18.5 should archive Phase 18" in phase_doc


def test_no_phase_eighteen_four_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_18_4*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_18_4*"))
