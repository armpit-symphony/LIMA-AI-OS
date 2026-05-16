"""Nested suspicious metadata fixture design tests for Phase 33.1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_33_1_NESTED_SUSPICIOUS_METADATA_FIXTURE_DESIGN.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_33_1_nested_suspicious_metadata_fixture_design.json"
)
CASES_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_33_1_nested_suspicious_metadata_cases.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_33_1_is_fixture_design_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "33.1"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_implementation_approved"] is False
    assert fixture["runtime_files_changed"] == []
    assert fixture["tests_support_changed"] is False
    assert "does not implement runtime behavior" in phase_doc


def test_phase_33_1_fixture_design_covers_required_nested_risks() -> None:
    coverage = set(_load_json(PHASE_FIXTURE_PATH)["coverage"])
    assert coverage == {
        "nested_authority_wording",
        "nested_sparkbot_wiring_claim",
        "nested_humaninput_bridge_claim",
        "nested_live_adapter_claim",
        "nested_shell_browser_network_file_mutation_claim",
        "nested_robotics_physical_world_claim",
        "nested_external_service_and_background_work_claim",
        "malformed_nested_metadata",
        "unknown_nested_values",
    }


def test_phase_33_1_expected_safety_invariants_are_recorded() -> None:
    expected = _load_json(PHASE_FIXTURE_PATH)["expected_safety"]
    assert expected["non_authoritative"] is True
    assert expected["execution_allowed"] is False
    assert expected["side_effects_allowed"] is False
    assert expected["approved"] is False
    assert expected["approval_state_never_approved"] is True
    assert expected["dispatch_allowed"] is False
    assert expected["persistence_allowed"] is False
    assert expected["phase_5_humaninput_runtime_bridge_gated"] is True
    assert expected["sparkbot_wiring_present"] is False
    assert expected["humaninput_runtime_bridge_present"] is False
    assert expected["live_adapter_present"] is False


def test_phase_33_1_cases_are_caller_provided_fixture_data() -> None:
    cases = _load_json(CASES_FIXTURE_PATH)["cases"]
    assert len(cases) >= 6
    for case in cases:
        assert isinstance(case["id"], str)
        assert isinstance(case["candidate_state"], dict)
        assert case["expected_status"] in {"proposed", "blocked", "needs_review"}
        assert case["expected_inspection_state"] in {"valid", "blocked"}
        assert isinstance(case["expected_reason"], str)


def test_no_phase_33_1_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_33_1*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_33_1*"))
