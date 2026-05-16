"""Phase 33 eligibility and test plan matrix tests for Phase 32.3."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_32_3_PHASE_33_ELIGIBILITY_AND_TEST_PLAN_MATRIX.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_32_3_phase_33_eligibility_and_test_plan_matrix.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_32_3_is_not_phase_33_approval_or_runtime_work() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "32.3"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_implementation_approved"] is False
    assert fixture["recommended_phase_33_implementation_file_scope"] == []
    assert "does not approve Phase 33" in phase_doc


def test_phase_32_3_phase_33_allowed_scope_is_test_only() -> None:
    allowed = _load_json(PHASE_FIXTURE_PATH)["phase_33_allowed_paths"]
    assert "docs/PHASE_33_*.md" in allowed
    assert "tests/fixtures/runtime_extraction/phase_33_*.json" in allowed
    assert "tests/test_phase_33_*.py" in allowed


def test_phase_32_3_phase_33_forbidden_scope_blocks_runtime_and_support() -> None:
    forbidden = set(_load_json(PHASE_FIXTURE_PATH)["phase_33_forbidden_scope"])
    assert "lima/**" in forbidden
    assert "tests/support/**" in forbidden
    assert "runtime_implementation" in forbidden
    assert "sparkbot_wiring" in forbidden
    assert "humaninput_runtime_bridge" in forbidden
    assert "execution" in forbidden
    assert "dispatch" in forbidden
    assert "audit_persistence" in forbidden
    assert "robotics_physical_world_action" in forbidden


def test_phase_32_3_required_tests_cover_runtime_state_boundaries() -> None:
    required = set(_load_json(PHASE_FIXTURE_PATH)["phase_33_required_tests"])
    assert "nested_suspicious_metadata_remains_non_authoritative" in required
    assert "nested_suspicious_metadata_cannot_enable_execution" in required
    assert "nested_suspicious_metadata_cannot_enable_side_effects" in required
    assert "runtime_state_remains_deterministic_local_only_read_only_non_authoritative_non_executing_side_effect_free" in required
    assert "phase_5_humaninput_runtime_bridge_remains_gated" in required
    assert "no_lima_files_changed" in required
    assert "no_tests_support_files_changed" in required


def test_phase_32_3_preserves_exact_phase_33_approval_question() -> None:
    question = _load_json(PHASE_FIXTURE_PATH)["approval_question"]
    assert question.startswith("Do you approve Phase 33 as a test-only hardening lane")
    assert "no runtime implementation" in question
    assert "no new `lima/` changes" in question
    assert "no `tests/support/` changes" in question
    assert "no Sparkbot wiring" in question
    assert "no HumanInput runtime bridge behavior" in question
    assert "no hidden side effects" in question


def test_no_phase_32_3_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_32_3*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_32_3*"))
