"""Cross-API provenance and status invariant tests for Phase 25.3."""

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
PHASE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_25_3_CROSS_API_PROVENANCE_AND_STATUS_INVARIANT_TESTS.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_25_3_cross_api_provenance_and_status_invariant_tests.json"
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


def _cases() -> list[dict[str, Any]]:
    return list(_load_json(CASE_FIXTURE_PATH)["cases"])


def _case(case_id: str) -> dict[str, Any]:
    return next(case for case in _cases() if case["case_id"] == case_id)


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


def _assert_never_approved_or_bridge_created(result: dict[str, Any]) -> None:
    assert result["approval_state"] != "approved"
    assert result["execution_allowed"] is False
    assert result["side_effects_allowed"] is False
    assert result.get("intent_envelope_created") is False
    assert result.get("guardian_decision_created") is False
    assert result["phase_5_humaninput_runtime_bridge_gated"] is True


def test_phase_metadata_links_matrix_fixture_and_boundaries() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "25.3"
    assert fixture["runtime_code_modified"] is False
    assert fixture["case_fixture"] == (
        "tests/fixtures/runtime_extraction/phase_25_1_candidate_api_matrix_cases.json"
    )
    assert "valid_provenance_preserved" in fixture["assertions"]
    assert "status_and_validation_never_create_bridge_records" in fixture["assertions"]


def test_valid_provenance_is_preserved_across_candidate_apis() -> None:
    case = _case("valid_low_risk_intake")
    candidate = _candidate_for_case(case)
    normalized = normalize_candidate_status(candidate)
    validated = validate_candidate(candidate)

    assert candidate["provenance"] == case["provenance"]
    assert normalized["provenance"] == case["provenance"]
    assert validated["provenance"] == case["provenance"]
    assert normalized["candidate_status"] == "proposed"
    assert validated["validation_state"] == "valid"


def test_unknown_status_is_blocked_without_approval() -> None:
    candidate = _candidate_for_case(_case("unknown_candidate_status"))
    normalized = normalize_candidate_status(candidate)
    validated = validate_candidate(candidate)

    assert normalized["candidate_status"] == "blocked"
    assert normalized["blocked_reason"] == "unknown_candidate_status_not_execution_ready"
    assert validated["candidate_status"] == "blocked"
    assert validated["validation_state"] == "valid"
    _assert_never_approved_or_bridge_created(normalized)
    _assert_never_approved_or_bridge_created(validated)


def test_suspicious_provenance_is_invalid_and_blocked() -> None:
    case = _case("suspicious_provenance_authority_claim")
    candidate = _candidate_for_case(case)
    normalized = normalize_candidate_status(candidate)
    validated = validate_candidate(candidate)

    assert normalized["candidate_status"] == "blocked"
    assert validated["validation_state"] == "invalid"
    assert case["expected_validation_error"] in validated["validation_errors"]
    _assert_never_approved_or_bridge_created(normalized)
    _assert_never_approved_or_bridge_created(validated)


@pytest.mark.parametrize("case_id", ["stale_candidate", "replayed_candidate"])
def test_stale_and_replayed_candidates_are_invalid_or_blocked(case_id: str) -> None:
    case = _case(case_id)
    candidate = _candidate_for_case(case)
    normalized = normalize_candidate_status(candidate)
    validated = validate_candidate(candidate)

    assert normalized["candidate_status"] == "blocked"
    assert validated["validation_state"] == "invalid"
    assert case["expected_validation_error"] in validated["validation_errors"]
    _assert_never_approved_or_bridge_created(normalized)
    _assert_never_approved_or_bridge_created(validated)


def test_bypass_wording_risky_request_remains_review_only() -> None:
    candidate = _candidate_for_case(_case("bypass_wording_shell_request"))
    normalized = normalize_candidate_status(candidate)
    validated = validate_candidate(candidate)

    assert normalized["candidate_status"] == "needs_review"
    assert validated["validation_state"] == "valid"
    assert validated["approval_state"] == "approval_required"
    _assert_never_approved_or_bridge_created(normalized)
    _assert_never_approved_or_bridge_created(validated)


def test_malformed_humaninput_like_intake_is_rejected() -> None:
    case = _case("raw_humaninput_like_intake")
    with pytest.raises(IntakeCandidateError, match=case["expected_error"]):
        build_intake_candidate(_intake_for_case(case))


def test_risky_action_categories_remain_needs_review_not_approved() -> None:
    risky_case_ids = [
        "browser_network_attempt",
        "file_mutation_attempt",
        "robotics_physical_world_attempt",
    ]
    for case_id in risky_case_ids:
        candidate = _candidate_for_case(_case(case_id))
        normalized = normalize_candidate_status(candidate)
        validated = validate_candidate(candidate)
        assert normalized["candidate_status"] == "needs_review"
        assert validated["validation_state"] == "valid"
        _assert_never_approved_or_bridge_created(normalized)
        _assert_never_approved_or_bridge_created(validated)


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


def test_no_phase_25_3_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_25_3*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_25_3*"))
