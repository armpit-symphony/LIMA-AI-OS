"""Runtime state hardening gap review tests for Phase 34.2."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_34_2_RUNTIME_STATE_HARDENING_GAP_REVIEW.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_34_2_runtime_state_hardening_gap_review.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_34_2_is_docs_tests_fixtures_only_gap_review() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "34.2"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_implementation_approved"] is False
    assert fixture["runtime_files_changed"] == []
    assert fixture["tests_support_changed"] is False
    assert "does not implement runtime behavior" in phase_doc


def test_phase_34_2_records_no_runtime_state_gap() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["runtime_state_gap_found"] is False
    assert fixture["runtime_code_change_needed"] is False
    assert fixture["additional_test_only_hardening_needed_immediately"] is False


def test_phase_34_2_reviews_all_phase_33_hardening_categories() -> None:
    reviewed = set(_load_json(PHASE_FIXTURE_PATH)["coverage_reviewed"])
    assert reviewed == {
        "authority_bypass_wording",
        "sparkbot_humaninput_live_adapter_claims",
        "shell_browser_network_file_mutation_claims",
        "robotics_physical_world_claims",
        "external_service_background_work_claims",
        "malformed_nested_metadata",
        "unknown_nested_values",
    }


def test_phase_34_2_keeps_runtime_files_forbidden() -> None:
    forbidden = set(_load_json(PHASE_FIXTURE_PATH)["forbidden_runtime_files_remain_forbidden"])
    assert "lima/kernel/runtime_state.py" in forbidden
    assert "lima/kernel/__init__.py" in forbidden
    assert "lima/kernel/intake_candidate.py" in forbidden
    assert "lima/kernel/candidate_status.py" in forbidden
    assert "all other lima/ files" in forbidden


def test_no_phase_34_2_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_34_2*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_34_2*"))
