"""Static checks for Phase 7.1 first runtime slice eligibility mapping."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_7_1_FIRST_RUNTIME_SLICE_ELIGIBILITY_MAP.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_7_1_first_runtime_slice_eligibility_map.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_declares_eligibility_map_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "7.1"
    assert fixture["non_runtime"] is True
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["eligibility_map_only"] is True


def test_future_eligible_existing_files_are_exact_and_contract_bounded() -> None:
    eligible = _load_json(PHASE_FIXTURE_PATH)["future_eligible_existing_files"]
    assert eligible == [
        "lima/contracts/boundary.py",
        "lima/contracts/intent.py",
        "lima/contracts/guardian.py",
        "lima/contracts/events.py",
        "lima/contracts/privacy.py",
        "lima/__init__.py",
    ]


def test_future_new_kernel_files_require_explicit_approval() -> None:
    eligible_new = _load_json(PHASE_FIXTURE_PATH)["future_eligible_new_files_if_explicitly_approved"]
    assert eligible_new == [
        "lima/kernel/__init__.py",
        "lima/kernel/intake_candidate.py",
    ]


def test_first_slice_forbids_execution_surfaces_and_tests_support() -> None:
    forbidden = set(_load_json(PHASE_FIXTURE_PATH)["forbidden_for_first_slice"])
    assert "lima/adapters/**" in forbidden
    assert "lima/guardian/**" in forbidden
    assert "lima/harness/**" in forbidden
    assert "lima/io/**" in forbidden
    assert "lima/packs/**" in forbidden
    assert "lima/persistence/**" in forbidden
    assert "lima/services/**" in forbidden
    assert "lima/shells/**" in forbidden
    assert "lima/spine/**" in forbidden
    assert "tests/support/**" in forbidden


def test_eligibility_rules_keep_future_code_non_executing() -> None:
    rules = _load_json(PHASE_FIXTURE_PATH)["eligibility_rules"]
    assert rules["eligible_files_are_future_candidates_only"] is True
    assert rules["future_code_non_executing_candidate_metadata_only"] is True
    assert rules["future_code_fails_closed_on_missing_typed_input"] is True
    assert rules["future_code_must_not_parse_raw_natural_language"] is True
    assert rules["future_code_must_not_create_real_guardiandecision"] is True
    assert rules["future_code_must_not_approve_enforce_execute_persist_audit_or_handoff_to_drivers"] is True


def test_ready_only_for_phase_seven_two_safety_preconditions() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["ready_for"] == [
        "phase_7_2_docs_tests_fixtures_only_kernel_runtime_safety_preconditions"
    ]
    assert "runtime_behavior" in fixture["not_ready_for"]
    assert "lima_changes" in fixture["not_ready_for"]
    assert "tests_support_changes" in fixture["not_ready_for"]
    assert "approval_enforcement" in fixture["not_ready_for"]


def test_doc_says_eligibility_is_not_current_approval() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "It is docs/tests/fixtures only" in phase_doc
    assert "does not implement runtime behavior" in phase_doc
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "Eligibility here is not approval to modify these files now" in phase_doc
    assert "Runtime implementation remains blocked" in phase_doc


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["runtime_behavior_added"] is False
    assert boundary["files_under_lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["helper_behavior_changed"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["intentcompiler_runtime_changed"] is False
    assert boundary["guardiandecision_runtime_changed"] is False
    assert boundary["execution_added"] is False
    assert boundary["physical_world_action_added"] is False


def test_no_phase_seven_one_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_7_1*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_7_1*"))
