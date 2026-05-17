"""Second-slice safety and scope comparison tests for Phase 35.2."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_35_2_SECOND_SLICE_SAFETY_AND_SCOPE_COMPARISON.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_35_2_second_slice_safety_and_scope_comparison.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_35_2_remains_design_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "35.2"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_implementation_approved"] is False
    assert fixture["runtime_files_changed_in_phase_35"] == []
    assert "does not approve Phase 36 implementation" in phase_doc


def test_candidate_preview_is_recommended_only_for_future_approval() -> None:
    candidate = _load_json(PHASE_FIXTURE_PATH)["recommended_future_candidate"]
    assert candidate["option"] == "C"
    assert candidate["name"] == "non_executing_candidate_preview_helper"
    assert candidate["recommended_for_future_phase_36_approval_question"] is True
    assert candidate["implementation_approved_now"] is False
    assert candidate["risk_level_if_bounded"] == "low"


def test_future_file_scope_is_exact_and_excludes_existing_runtime_files() -> None:
    scope = _load_json(PHASE_FIXTURE_PATH)["future_phase_36_file_scope_if_approved"]
    assert scope["allowed_runtime_files"] == [
        "lima/kernel/candidate_preview.py",
        "lima/kernel/__init__.py_if_safe_public_export_required",
    ]
    assert "lima/kernel/runtime_state.py" in scope["forbidden_runtime_files"]
    assert "lima/kernel/intake_candidate.py" in scope["forbidden_runtime_files"]
    assert "lima/kernel/candidate_status.py" in scope["forbidden_runtime_files"]
    assert scope["tests_support_changes_allowed"] is False


def test_future_candidate_properties_keep_slice_non_executing() -> None:
    properties = _load_json(PHASE_FIXTURE_PATH)["future_candidate_required_properties"]
    assert properties["deterministic"] is True
    assert properties["local_only"] is True
    assert properties["side_effect_free"] is True
    assert properties["read_only"] is True
    assert properties["non_authoritative"] is True
    assert properties["non_executing"] is True
    assert properties["caller_provided_data_only"] is True
    assert properties["safe_under_missing_malformed_unknown_suspicious_nested_bypass_input"] is True


def test_forbidden_behaviors_remain_explicit() -> None:
    forbidden = set(_load_json(PHASE_FIXTURE_PATH)["forbidden_future_candidate_behaviors"])
    assert "humaninput_runtime_bridge_behavior" in forbidden
    assert "sparkbot_wiring" in forbidden
    assert "approval_enforcement" in forbidden
    assert "execution" in forbidden
    assert "dispatch" in forbidden
    assert "persistence" in forbidden
    assert "shell_browser_network_file_mutation" in forbidden
    assert "robotics" in forbidden
    assert "physical_world_behavior" in forbidden
    assert "external_service_calls" in forbidden


def test_no_phase_35_2_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_35_2*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_35_2*"))
