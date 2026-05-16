"""Cross-API non-execution invariant tests for Phase 25.2."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from lima.kernel import (
    IntakeCandidateError,
    build_intake_candidate,
    normalize_candidate_status,
    validate_candidate,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_25_2_CROSS_API_NON_EXECUTION_INVARIANT_TESTS.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_25_2_cross_api_non_execution_invariant_tests.json"
)
CASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_25_1_candidate_api_matrix_cases.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def _intake_for_case(case: dict[str, Any]) -> dict[str, Any]:
    intake: dict[str, Any] = {
        "synthetic": True,
        "test_only": True,
        "intake_id": f"phase25-{case['case_id']}",
        "source": "phase_25_1_matrix_fixture",
        "source_channel": "test",
        "operator_intent": case.get("operator_intent", "Review candidate invariant matrix."),
        "normalized_request": "review candidate invariant matrix",
        "requested_action": case.get("requested_action", "review_candidate_matrix"),
        "action_category": case["action_category"],
        "provenance": case["provenance"],
    }
    intake.update(case.get("extra_intake", {}))
    return intake


def _candidate_for_case(case: dict[str, Any]) -> dict[str, Any]:
    candidate = build_intake_candidate(_intake_for_case(case))
    candidate.update(case.get("candidate_overrides", {}))
    return candidate


def _assert_non_executing(candidate: dict[str, Any]) -> None:
    assert candidate["executable"] is False
    assert candidate["execution_allowed"] is False
    assert candidate["side_effects_allowed"] is False
    assert candidate["approved"] is False
    assert candidate["approval_state"] != "approved"
    assert candidate["phase_5_humaninput_runtime_bridge_gated"] is True


def test_phase_metadata_links_matrix_fixture_and_boundaries() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "25.2"
    assert fixture["runtime_code_modified"] is False
    assert fixture["case_fixture"] == (
        "tests/fixtures/runtime_extraction/phase_25_1_candidate_api_matrix_cases.json"
    )
    assert "build_intake_candidate" in fixture["apis_under_test"]
    assert "execution_allowed_false" in fixture["invariants_asserted"]


@pytest.mark.parametrize("case", _load_json(CASE_FIXTURE_PATH)["cases"])
def test_cross_api_non_execution_invariants(case: dict[str, Any]) -> None:
    if case["expected_build"] == "error":
        with pytest.raises(IntakeCandidateError, match=case["expected_error"]):
            build_intake_candidate(_intake_for_case(case))
        return

    candidate = _candidate_for_case(case)
    normalized = normalize_candidate_status(candidate)
    validated = validate_candidate(candidate)

    _assert_non_executing(candidate)
    _assert_non_executing(normalized)
    _assert_non_executing(validated)

    assert normalized["candidate_status"] == case["expected_status"]
    assert validated["validation_state"] == case["expected_validation_state"]


def test_all_constructible_cases_remain_without_dispatch_or_runtime_bridge() -> None:
    for case in _load_json(CASE_FIXTURE_PATH)["cases"]:
        if case["expected_build"] == "error":
            continue
        candidate = _candidate_for_case(case)
        normalized = normalize_candidate_status(candidate)
        validated = validate_candidate(candidate)
        for result in (candidate, normalized, validated):
            assert result.get("intent_envelope_created") is False
            assert result.get("guardian_decision_created") is False
            assert result["phase_5_humaninput_runtime_bridge_gated"] is True


def test_phase_document_preserves_test_only_scope() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "test/docs/fixtures-only hardening" in phase_doc
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "Runtime expansion remains blocked" in phase_doc


def test_boundary_results_show_no_forbidden_behavior() -> None:
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


def test_no_phase_25_2_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_25_2*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_25_2*"))
