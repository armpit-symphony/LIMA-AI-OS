"""Phase 32 next-lane decision matrix tests for Phase 31.3."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_31_3_PHASE_32_NEXT_LANE_DECISION_MATRIX.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_31_3_phase_32_next_lane_decision_matrix.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_31_3_is_next_lane_decision_metadata_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "31.3"
    assert fixture["runtime_code_modified"] is False
    assert "next-lane decision metadata only" in phase_doc
    assert "does not implement new runtime behavior" in phase_doc


def test_phase_31_3_records_no_runtime_file_changes() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["runtime_state_py_changed_in_phase_31"] is False
    assert fixture["kernel_init_changed_in_phase_31"] is False


def test_all_phase_32_options_are_evaluated() -> None:
    options = _load_json(PHASE_FIXTURE_PATH)["options_evaluated"]
    assert options["option_a_docs_tests_fixtures_only_design_review"] == "recommended"
    assert options["option_b_additional_test_only_hardening"] == (
        "fallback_only_if_concrete_gap_exists"
    )
    assert options["option_c_second_narrow_read_only_runtime_slice"] == (
        "not_immediate_default_requires_design_and_explicit_approval"
    )
    assert options["option_d_humaninput_bridge_boundary_planning"] == (
        "valid_but_not_immediate_default"
    )
    assert options["option_e_sparkbot_integration_boundary_planning"] == (
        "valid_but_not_immediate_default"
    )
    assert options["option_f_pause_and_preserve"] == "not_required_no_unresolved_phase_30_risk"


def test_recommended_phase_32_direction_is_no_code_design_review() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["recommended_phase_32_direction"] == (
        "docs_tests_fixtures_only_design_review_for_next_narrow_runtime_slice"
    )
    assert fixture["phase_32_runtime_implementation_approved"] is False


def test_phase_32_approval_question_preserves_forbidden_scope() -> None:
    question = _load_json(PHASE_FIXTURE_PATH)["phase_32_approval_question"]
    assert "Do you approve Phase 32" in question
    assert "docs/tests/fixtures-only design review" in question
    assert "no new runtime implementation" in question
    assert "no new `lima/` changes" in question
    assert "no `tests/support/` changes" in question
    assert "no Sparkbot wiring" in question
    assert "no HumanInput runtime bridge behavior" in question
    assert "no live adapters" in question
    assert "no approval enforcement" in question
    assert "no execution" in question
    assert "no dispatch" in question
    assert "no audit persistence" in question
    assert "no hidden side effects" in question


def test_no_phase_31_3_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_31_3*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_31_3*"))
