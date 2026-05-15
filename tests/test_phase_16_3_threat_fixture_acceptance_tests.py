"""Threat fixture acceptance tests for Phase 16.3."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from lima.kernel import IntakeCandidateError, build_intake_candidate, normalize_candidate_status, validate_candidate

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_16_3_THREAT_FIXTURE_ACCEPTANCE_TESTS.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_16_3_threat_fixture_acceptance_tests.json"
)
CASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_16_3_threat_fixture_acceptance_cases.json"
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
    assert candidate.get("intent_envelope_created") is False
    assert candidate.get("guardian_decision_created") is False


def test_phase_metadata_and_fixture_rules_are_safe() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    case_fixture = _load_json(CASE_FIXTURE_PATH)
    assert fixture["phase"] == "16.3"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False
    rules = case_fixture["fixture_rules"]
    assert rules["synthetic"] is True
    assert rules["inert"] is True
    assert rules["non_runtime"] is True
    assert rules["side_effect_free"] is True
    assert rules["no_credentials"] is True
    assert rules["no_private_hostnames"] is True
    assert rules["no_live_shell_commands"] is True
    assert rules["no_live_network_targets"] is True
    assert rules["no_real_file_paths"] is True
    assert rules["no_robot_or_device_actuation_instructions"] is True
    assert rules["not_authorization"] is True


@pytest.mark.parametrize(
    "case_id",
    [
        "malformed_candidate_missing_execution_allowed",
        "unknown_status_candidate",
        "stale_candidate",
        "replayed_candidate",
        "approval_bypass_wording",
        "shell_command_attempt",
        "browser_network_attempt",
        "file_mutation_attempt",
        "robotics_physical_world_attempt",
        "sparkbot_integration_attempt",
    ],
)
def test_threat_fixture_candidates_remain_non_executing(case_id: str) -> None:
    case = _case(case_id)
    candidate = _build_case_candidate(case)
    normalized = normalize_candidate_status(candidate)
    validated = validate_candidate(candidate)

    assert normalized["candidate_status"] in {"blocked", "needs_review"}
    assert validated["candidate_status"] in {"blocked", "needs_review"}
    _assert_non_executing(normalized)
    _assert_non_executing(validated)


def test_malformed_candidate_fixture_is_invalid_or_blocked() -> None:
    candidate = _build_case_candidate(_case("malformed_candidate_missing_execution_allowed"))
    validated = validate_candidate(candidate)
    assert validated["validation_state"] == "invalid"
    assert validated["candidate_status"] == "blocked"
    assert "missing_required_candidate_fields:execution_allowed" in validated["validation_errors"]
    _assert_non_executing(validated)


def test_unknown_status_fixture_is_blocked() -> None:
    candidate = _build_case_candidate(_case("unknown_status_candidate"))
    normalized = normalize_candidate_status(candidate)
    assert normalized["candidate_status"] == "blocked"
    assert normalized["blocked_reason"] == "unknown_candidate_status_not_execution_ready"
    _assert_non_executing(normalized)


def test_stale_and_replayed_fixture_cases_remain_blocked() -> None:
    stale = validate_candidate(_build_case_candidate(_case("stale_candidate")))
    replayed = validate_candidate(_build_case_candidate(_case("replayed_candidate")))
    assert stale["candidate_status"] == "blocked"
    assert stale["blocked_reason"] == "stale_intake_not_execution_ready"
    assert replayed["candidate_status"] == "blocked"
    assert replayed["blocked_reason"] == "replayed_intake_not_execution_ready"
    _assert_non_executing(stale)
    _assert_non_executing(replayed)


def test_humaninput_bridge_attempt_fixture_is_rejected() -> None:
    case = _case("humaninput_bridge_attempt")
    with pytest.raises(IntakeCandidateError, match="raw HumanInput-like payloads are not accepted"):
        build_intake_candidate(case["intake"])


def test_phase_document_and_fixture_preserve_boundaries() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "does not execute" in phase_doc
    assert fixture["boundary_results"]["phase_5_runtime_bridge_remains_gated"] is True
    assert fixture["boundary_results"]["sparkbot_imported_or_wired"] is False
    assert fixture["boundary_results"]["humaninput_runtime_bridge_added"] is False


def test_no_phase_sixteen_three_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_16_3*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_16_3*"))
