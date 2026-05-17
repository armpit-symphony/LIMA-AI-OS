"""Phase 34 hardening archive closeout tests for Phase 34.4."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_34_4_PHASE_34_HARDENING_ARCHIVE_CLOSEOUT.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_34_4_phase_34_hardening_archive_closeout.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_34_4_archives_completed_phase_34_scope() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "34.4"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_implementation_approved"] is False
    assert fixture["phase_34_completed_phases"] == ["34.0", "34.1", "34.2", "34.3"]
    assert "archives Phase 34 as a completed docs/tests/fixtures-only audit/archive lane" in phase_doc


def test_phase_34_4_records_no_runtime_or_support_changes() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["runtime_files_changed"] == []
    assert fixture["runtime_state_py_changed_in_phase_34"] is False
    assert fixture["kernel_init_changed_in_phase_34"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["runtime_behavior_changed"] is False


def test_phase_34_4_records_boundary_absence() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase_5_runtime_bridge_remains_gated"] is True
    assert fixture["execution_approval_dispatch_persistence_absent"] is True
    assert fixture["sparkbot_wiring_imports_absent"] is True
    assert fixture["shell_browser_network_file_robotics_physical_world_absent"] is True


def test_phase_34_4_records_nested_metadata_audit_result() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    coverage = set(fixture["nested_suspicious_metadata_coverage_confirmed"])
    assert fixture["nested_suspicious_metadata_audit_result"] == "PASS"
    assert coverage == {
        "nested_authority_bypass_wording",
        "nested_sparkbot_wiring_claims",
        "nested_humaninput_bridge_claims",
        "nested_live_adapter_claims",
        "nested_shell_browser_network_file_mutation_claims",
        "nested_robotics_physical_world_claims",
        "nested_external_service_background_work_claims",
        "malformed_nested_metadata",
        "unknown_nested_values",
    }


def test_phase_34_4_records_no_remaining_gaps_and_phase_35_direction() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["runtime_state_gap_found"] is False
    assert fixture["remaining_gaps"] == []
    assert (
        fixture["recommended_phase_35_direction"]
        == "docs_tests_fixtures_only_no_code_design_review_for_second_narrow_runtime_slice"
    )


def test_phase_34_4_preserves_phase_35_approval_question() -> None:
    question = _load_json(PHASE_FIXTURE_PATH)["approval_question"]
    assert question.startswith("Do you approve Phase 35 as a docs/tests/fixtures-only no-code design review")
    assert "no runtime implementation" in question
    assert "no new `lima/` changes" in question
    assert "no `tests/support/` changes" in question
    assert "no Sparkbot wiring" in question
    assert "no HumanInput runtime bridge behavior" in question
    assert "no hidden side effects" in question


def test_no_phase_34_4_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_34_4*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_34_4*"))
