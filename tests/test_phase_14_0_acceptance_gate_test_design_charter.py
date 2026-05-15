"""Static checks for Phase 14.0 acceptance-gate test design charter."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_14_0_ACCEPTANCE_GATE_TEST_DESIGN_CHARTER.md"
PHASE_FIXTURE_PATH = REPO_ROOT / "tests" / "fixtures" / "runtime_extraction" / "phase_14_0_acceptance_gate_test_design_charter.json"


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_design_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "14.0"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False


def test_source_requirements_cover_phase_thirteen_outputs() -> None:
    sources = set(_load_json(PHASE_FIXTURE_PATH)["source_requirements"])
    assert sources == {
        "phase_13_1_static_forbidden_pattern_requirements",
        "phase_13_2_runtime_contract_requirements",
        "phase_13_3_threat_fixture_matrix",
        "phase_13_4_future_acceptance_gate_requirements",
    }


def test_design_outputs_cover_phase_fourteen_lane() -> None:
    outputs = set(_load_json(PHASE_FIXTURE_PATH)["design_outputs"])
    assert outputs == {
        "static_forbidden_pattern_test_design",
        "runtime_contract_test_design",
        "threat_fixture_acceptance_test_design",
        "future_runtime_acceptance_gate_closeout",
    }


def test_phase_document_blocks_runtime_scope() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "docs/tests/fixtures-only acceptance-gate test design lane" in phase_doc
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "does not add executable test helpers" in phase_doc


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["test_helper_added"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["humaninput_runtime_bridge_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True


def test_no_phase_fourteen_zero_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_14_0*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_14_0*"))
