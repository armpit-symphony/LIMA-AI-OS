"""Next-slice safety and scope comparison tests for Phase 32.2."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_32_2_NEXT_SLICE_SAFETY_AND_SCOPE_COMPARISON.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_32_2_next_slice_safety_and_scope_comparison.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_32_2_is_docs_tests_fixtures_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "32.2"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_implementation_approved"] is False
    assert "does not approve Phase 33 runtime implementation" in phase_doc


def test_phase_32_2_recommends_no_runtime_implementation() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["recommended_option"] == "runtime_state_test_only_hardening"
    assert fixture["recommended_option_ready"] is True
    assert fixture["runtime_implementation_recommended"] is False
    assert fixture["phase_33_option_a_file_scope"]["implementation_file_scope"] == []


def test_phase_32_2_marks_runtime_options_not_ready() -> None:
    comparison = _load_json(PHASE_FIXTURE_PATH)["comparison"]
    assert comparison["second_read_only_runtime_inspection_slice"]["readiness"] == "not_ready"
    assert comparison["non_executing_candidate_preview_helper"]["readiness"] == "not_ready"
    assert comparison["candidate_status_read_only_normalization_hardening"]["readiness"] == "not_ready"


def test_phase_32_2_phase_33_option_a_scope_excludes_runtime_and_support() -> None:
    scope = _load_json(PHASE_FIXTURE_PATH)["phase_33_option_a_file_scope"]
    assert "docs/PHASE_33_*.md" in scope["allowed_paths"]
    assert "tests/fixtures/runtime_extraction/phase_33_*.json" in scope["allowed_paths"]
    assert "tests/test_phase_33_*.py" in scope["allowed_paths"]
    assert "lima/**" in scope["forbidden_paths"]
    assert "tests/support/**" in scope["forbidden_paths"]


def test_no_phase_32_2_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_32_2*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_32_2*"))
