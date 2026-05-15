"""Regression tests for Phase 18.2 acceptance-boundary fixtures."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from lima.kernel import IntakeCandidateError, build_intake_candidate, normalize_candidate_status, validate_candidate

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_18_2_ACCEPTANCE_BOUNDARY_REGRESSION_FIXTURES.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_18_2_acceptance_boundary_regression_fixtures.json"
)
CASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_18_2_acceptance_boundary_regression_cases.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def _cases() -> list[dict[str, Any]]:
    cases = _load_json(CASE_FIXTURE_PATH)["cases"]
    assert isinstance(cases, list)
    return cases


def _case(case_id: str) -> dict[str, Any]:
    for case in _cases():
        if case["case_id"] == case_id:
            return case
    raise AssertionError(f"missing fixture case {case_id}")


def _build_case_candidate(case: dict[str, Any]) -> dict[str, Any]:
    candidate = build_intake_candidate(case["intake"])
    if case.get("candidate_mutation") == "remove_execution_allowed":
        del candidate["execution_allowed"]
    if "candidate_status_override" in case:
        candidate["candidate_status"] = case["candidate_status_override"]
    return candidate


def _assert_non_executing(candidate: dict[str, Any]) -> None:
    assert candidate["executable"] is False
    assert candidate["execution_allowed"] is False
    assert candidate["side_effects_allowed"] is False
    assert candidate["approved"] is False
    assert candidate["approval_state"] != "approved"
    assert candidate["phase_5_humaninput_runtime_bridge_gated"] is True


def test_fixture_metadata_and_rules_are_synthetic_and_inert() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    case_fixture = _load_json(CASE_FIXTURE_PATH)
    assert fixture["phase"] == "18.2"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False
    for rules in (fixture["fixture_rules"], case_fixture["fixture_rules"]):
        assert rules["synthetic"] is True
        assert rules["inert"] is True
        assert rules["non_runtime"] is True
        assert rules["side_effect_free"] is True
        assert rules["not_authorization"] is True
        assert rules["no_credentials"] is True
        assert rules["no_live_shell_commands"] is True
        assert rules["no_live_network_targets"] is True
        assert rules["no_real_file_paths"] is True
        assert rules["no_robot_or_device_actuation_instructions"] is True


def test_expected_case_ids_are_present_exactly_once() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    expected = fixture["expected_case_ids"]
    actual = [case["case_id"] for case in _cases()]
    assert actual == expected
    assert len(actual) == len(set(actual))


@pytest.mark.parametrize(
    "case_id",
    [
        "approval_bypass_wording_regression",
        "shell_attempt_regression",
        "browser_network_attempt_regression",
        "file_mutation_attempt_regression",
        "robotics_physical_world_attempt_regression",
        "sparkbot_integration_attempt_regression",
        "stale_candidate_regression",
        "replayed_candidate_regression",
        "malformed_candidate_regression",
        "unknown_status_regression",
    ],
)
def test_boundary_fixture_cases_remain_non_executing(case_id: str) -> None:
    candidate = _build_case_candidate(_case(case_id))
    normalized = normalize_candidate_status(candidate)
    validated = validate_candidate(candidate)

    assert normalized["candidate_status"] in {"blocked", "needs_review", "proposed"}
    assert validated["candidate_status"] in {"blocked", "needs_review", "proposed"}
    _assert_non_executing(normalized)
    _assert_non_executing(validated)


def test_humaninput_runtime_bridge_attempt_remains_rejected() -> None:
    case = _case("humaninput_runtime_bridge_attempt_regression")
    with pytest.raises(IntakeCandidateError, match="raw HumanInput-like payloads are not accepted"):
        build_intake_candidate(case["intake"])


def test_malformed_and_unknown_status_cases_fail_closed() -> None:
    malformed = validate_candidate(_build_case_candidate(_case("malformed_candidate_regression")))
    unknown = normalize_candidate_status(_build_case_candidate(_case("unknown_status_regression")))

    assert malformed["validation_state"] == "invalid"
    assert malformed["candidate_status"] == "blocked"
    assert "missing_required_candidate_fields:execution_allowed" in malformed["validation_errors"]
    assert unknown["candidate_status"] == "blocked"
    assert unknown["blocked_reason"] == "unknown_candidate_status_not_execution_ready"
    _assert_non_executing(malformed)
    _assert_non_executing(unknown)


def test_phase_document_and_fixture_preserve_boundaries() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "does not execute" in phase_doc
    assert fixture["boundary_results"]["runtime_behavior_changed"] is False
    assert fixture["boundary_results"]["phase_5_runtime_bridge_remains_gated"] is True


def test_no_phase_eighteen_two_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_18_2*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_18_2*"))
