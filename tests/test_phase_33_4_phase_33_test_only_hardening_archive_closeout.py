"""Phase 33 test-only hardening archive closeout tests for Phase 33.4."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_33_4_PHASE_33_TEST_ONLY_HARDENING_ARCHIVE_CLOSEOUT.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_33_4_phase_33_test_only_hardening_archive_closeout.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_33_4_archives_completed_phase_33_scope() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "33.4"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_implementation_approved"] is False
    assert fixture["phase_33_completed_phases"] == ["33.0", "33.1", "33.2", "33.3"]
    assert "archives Phase 33 as a completed test-only hardening lane" in phase_doc


def test_phase_33_4_records_no_runtime_or_support_changes() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["runtime_files_changed"] == []
    assert fixture["runtime_state_py_changed_in_phase_33"] is False
    assert fixture["kernel_init_changed_in_phase_33"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["runtime_behavior_changed"] is False


def test_phase_33_4_records_boundary_absence() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase_5_runtime_bridge_remains_gated"] is True
    assert fixture["execution_approval_dispatch_persistence_absent"] is True
    assert fixture["sparkbot_wiring_imports_absent"] is True
    assert fixture["shell_browser_network_file_robotics_physical_world_absent"] is True


def test_phase_33_4_records_nested_metadata_coverage() -> None:
    coverage = set(_load_json(PHASE_FIXTURE_PATH)["nested_suspicious_metadata_coverage_added"])
    assert coverage == {
        "nested_authority_wording",
        "nested_bypass_wording",
        "nested_sparkbot_wiring_claim",
        "nested_humaninput_bridge_claim",
        "nested_live_adapter_claim",
        "nested_shell_browser_network_file_mutation_claim",
        "nested_robotics_physical_world_claim",
        "nested_external_service_and_background_work_claim",
        "malformed_nested_metadata",
        "unknown_nested_values",
    }


def test_phase_33_4_records_no_runtime_state_gap_and_no_remaining_gaps() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["runtime_state_gap_found"] is False
    assert fixture["remaining_gaps"] == []
    assert (
        fixture["recommended_phase_34_direction"]
        == "docs_tests_fixtures_only_audit_archive_for_phase_33_hardening"
    )


def test_phase_33_4_preserves_phase_34_approval_question() -> None:
    question = _load_json(PHASE_FIXTURE_PATH)["approval_question"]
    assert question.startswith("Do you approve Phase 34 as a docs/tests/fixtures-only audit/archive lane")
    assert "no runtime implementation" in question
    assert "no new `lima/` changes" in question
    assert "no `tests/support/` changes" in question
    assert "no Sparkbot wiring" in question
    assert "no HumanInput runtime bridge behavior" in question
    assert "no hidden side effects" in question


def test_no_phase_33_4_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_33_4*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_33_4*"))
