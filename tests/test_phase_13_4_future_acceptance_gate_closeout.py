"""Static checks for Phase 13.4 future acceptance gate closeout."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_13_4_FUTURE_ACCEPTANCE_GATE_CLOSEOUT.md"
PHASE_FIXTURE_PATH = REPO_ROOT / "tests" / "fixtures" / "runtime_extraction" / "phase_13_4_future_acceptance_gate_closeout.json"


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_docs_tests_fixtures_only_closeout() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "13.4"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False
    assert fixture["phase_14_requires_explicit_phil_approval"] is True


def test_phase_thirteen_scope_is_listed_complete() -> None:
    assert _load_json(PHASE_FIXTURE_PATH)["completed_phase_13_scope"] == [
        "phase_13_0_threat_derived_test_planning_charter",
        "phase_13_1_static_forbidden_pattern_test_requirements",
        "phase_13_2_runtime_contract_test_requirements",
        "phase_13_3_threat_fixture_matrix",
    ]


def test_future_acceptance_gate_requirements_are_preserved() -> None:
    requirements = set(_load_json(PHASE_FIXTURE_PATH)["future_acceptance_gate_requirements"])
    assert "static_forbidden_pattern_checks" in requirements
    assert "runtime_contract_invariant_checks" in requirements
    assert "synthetic_threat_fixtures" in requirements
    assert "phase_5_runtime_bridge_gate_proof" in requirements
    assert "forbidden_behavior_absence_proof" in requirements


def test_phase_fourteen_question_keeps_runtime_blocked() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["recommended_phase_14_direction"] == "docs_tests_fixtures_only_acceptance_gate_test_design"
    question = fixture["phase_14_approval_question"]
    assert "docs/tests/fixtures-only acceptance-gate test design lane" in question
    assert "forbidding runtime implementation" in question
    assert "Sparkbot wiring" in question
    assert "physical-world action" in question


def test_phase_document_blocks_runtime_and_stops_at_gate() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "closes Phase 13" in phase_doc
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "Do you approve Phase 14" in phase_doc


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["humaninput_runtime_bridge_added"] is False
    assert boundary["approval_enforcement_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True


def test_no_phase_thirteen_four_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_13_4*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_13_4*"))
