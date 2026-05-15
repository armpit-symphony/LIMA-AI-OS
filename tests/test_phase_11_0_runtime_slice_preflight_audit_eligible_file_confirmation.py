"""Static checks for Phase 11.0 runtime preflight audit."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_11_0_RUNTIME_SLICE_PREFLIGHT_AUDIT_ELIGIBLE_FILE_CONFIRMATION.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_11_0_runtime_slice_preflight_audit_eligible_file_confirmation.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_docs_tests_fixtures_only_preflight() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "11.0"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False
    assert fixture["preflight_result"] == "pass"


def test_eligible_runtime_files_are_exact() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["eligible_runtime_files"] == [
        "lima/kernel/intake_candidate.py",
        "lima/kernel/__init__.py",
        "lima/kernel/candidate_status.py",
    ]


def test_candidate_status_file_is_absent_before_implementation() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["candidate_status_exists_before_implementation"] is False
    assert "lima/kernel/candidate_status.py" in fixture["eligible_runtime_files"]


def test_preflight_does_not_authorize_runtime_implementation_yet() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase_11_scope"] == "candidate_validation_and_candidate_status_normalization"
    assert fixture["phase_11_implementation_allowed_after_preflight"] is False
    assert fixture["next_phase"] == "phase_11_1_candidate_status_acceptance_test_scaffolding"


def test_phase_document_preserves_boundaries() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "docs/tests/fixtures only" in phase_doc
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "No other runtime files are eligible for Phase 11" in phase_doc
    assert "Phase 5 HumanInput runtime bridge gate" in phase_doc


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["helper_behavior_changed"] is False
    assert boundary["candidate_status_added"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["humaninput_runtime_bridge_added"] is False
    assert boundary["live_adapter_added"] is False
    assert boundary["intentcompiler_runtime_behavior_changed"] is False
    assert boundary["guardiandecision_runtime_behavior_changed"] is False
    assert boundary["approval_enforcement_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False


def test_no_phase_eleven_zero_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_11_0*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_11_0*"))
