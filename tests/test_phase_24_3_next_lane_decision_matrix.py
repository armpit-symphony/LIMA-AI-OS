"""Next-lane decision matrix tests for Phase 24.3."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_24_3_NEXT_LANE_DECISION_MATRIX.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_24_3_next_lane_decision_matrix.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_24_3_is_docs_tests_fixtures_only_decision_review() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "24.3"
    assert fixture["runtime_code_modified"] is False
    assert "docs/tests/fixtures-only decision review" in phase_doc
    assert "does not implement runtime behavior" in phase_doc


def test_all_required_phase_25_options_are_evaluated() -> None:
    options = {option["id"]: option for option in _load_json(PHASE_FIXTURE_PATH)["options"]}
    assert options["A"]["direction"] == "no_code_design_lane_for_next_narrow_runtime_slice"
    assert options["B"]["direction"] == "additional_test_only_hardening"
    assert options["C"]["direction"] == "sparkbot_integration_boundary_planning"
    assert options["D"]["direction"] == "robo_os_physical_world_boundary_planning"
    assert options["E"]["direction"] == "pause_and_preserve_current_runtime_test_state"


def test_exactly_one_phase_25_direction_is_recommended() -> None:
    options = _load_json(PHASE_FIXTURE_PATH)["options"]
    recommended = [option for option in options if option["decision"] == "recommended"]
    assert recommended == [
        {
            "id": "B",
            "direction": "additional_test_only_hardening",
            "decision": "recommended",
        }
    ]
    assert _load_json(PHASE_FIXTURE_PATH)["recommended_phase_25_direction"] == (
        "test_only_cross_api_candidate_invariant_matrix_hardening"
    )


def test_phase_25_approval_question_preserves_forbidden_scope() -> None:
    question = _load_json(PHASE_FIXTURE_PATH)["phase_25_approval_question"]
    assert "test-only hardening lane" in question
    assert "cross-API candidate invariant matrix" in question
    assert "runtime implementation" in question
    assert "lima/ changes" in question
    assert "tests/support/ changes" in question
    assert "Sparkbot wiring" in question
    assert "HumanInput runtime bridge" in question
    assert "approval enforcement" in question
    assert "execution" in question
    assert "dispatch" in question
    assert "audit persistence" in question
    assert "physical-world action" in question
    assert "hidden side effects" in question


def test_boundary_results_show_no_forbidden_behavior_and_phase_25_gate() -> None:
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
    assert boundary["phase_25_requires_explicit_approval"] is True


def test_phase_doc_gates_phase_24_4_and_runtime_expansion() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "Phase 24.4 may archive Phase 24" in phase_doc
    assert "Runtime expansion remains blocked" in phase_doc


def test_no_phase_24_3_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_24_3*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_24_3*"))
