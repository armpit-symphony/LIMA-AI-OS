"""Regression tests for existing non-executing candidate APIs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from lima.kernel import IntakeCandidateError, build_intake_candidate, normalize_candidate_status, validate_candidate

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_18_1_CANDIDATE_API_REGRESSION_TESTS.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_18_1_candidate_api_regression_tests.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def _intake(**overrides: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "synthetic": True,
        "test_only": True,
        "intake_id": "phase18-regression-001",
        "source": "phase_18_regression_fixture",
        "source_channel": "test",
        "operator_intent": "Review candidate metadata without execution.",
        "normalized_request": "review candidate metadata",
        "requested_action": "summarize_candidate_metadata",
        "action_category": "informational",
        "provenance": {
            "fixture": "phase_18_1_candidate_api_regression_tests",
            "lineage_seed": "phase18-regression",
        },
    }
    base.update(overrides)
    return base


def _assert_non_executing(candidate: dict[str, Any]) -> None:
    assert candidate["executable"] is False
    assert candidate["execution_allowed"] is False
    assert candidate["side_effects_allowed"] is False
    assert candidate["approved"] is False
    assert candidate["approval_state"] != "approved"
    assert candidate["phase_5_humaninput_runtime_bridge_gated"] is True
    assert candidate.get("intent_envelope_created") is False
    assert candidate.get("guardian_decision_created") is False


def test_phase_metadata_lists_existing_candidate_apis() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "18.1"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False
    assert set(fixture["exercised_existing_apis"]) == {
        "lima.kernel.build_intake_candidate",
        "lima.kernel.normalize_candidate_status",
        "lima.kernel.validate_candidate",
    }


def test_candidate_remains_non_executable_after_build_normalize_and_validate() -> None:
    candidate = build_intake_candidate(_intake())
    normalized = normalize_candidate_status(candidate)
    validated = validate_candidate(candidate)

    assert candidate["candidate_status"] if "candidate_status" in candidate else True
    assert normalized["candidate_status"] == "proposed"
    assert validated["validation_state"] == "valid"
    assert validated["candidate_status"] == "proposed"
    _assert_non_executing(candidate)
    _assert_non_executing(normalized)
    _assert_non_executing(validated)


@pytest.mark.parametrize(
    ("field_name", "bad_value", "expected_error"),
    [
        ("executable", True, "executable_must_be_false"),
        ("execution_allowed", True, "execution_allowed_must_be_false"),
        ("side_effects_allowed", True, "side_effects_allowed_must_be_false"),
        ("approved", True, "approved_flag_must_be_false"),
        ("approval_state", "approved", "approval_state_must_not_be_approved"),
    ],
)
def test_authority_bearing_fields_are_invalidated(
    field_name: str, bad_value: Any, expected_error: str
) -> None:
    candidate = build_intake_candidate(_intake())
    candidate[field_name] = bad_value
    validated = validate_candidate(candidate)

    assert validated["validation_state"] == "invalid"
    assert validated["candidate_status"] == "blocked"
    assert expected_error in validated["validation_errors"]
    _assert_non_executing(validated)


def test_unknown_status_normalizes_to_blocked_and_never_approval() -> None:
    candidate = build_intake_candidate(_intake())
    candidate["candidate_status"] = "trusted_admin_override"
    normalized = normalize_candidate_status(candidate)
    validated = validate_candidate(candidate)

    assert normalized["candidate_status"] == "blocked"
    assert normalized["blocked_reason"] == "unknown_candidate_status_not_execution_ready"
    assert validated["approval_state"] != "approved"
    _assert_non_executing(normalized)
    _assert_non_executing(validated)


def test_malformed_candidate_missing_provenance_fails_closed() -> None:
    candidate = build_intake_candidate(_intake())
    del candidate["provenance"]
    validated = validate_candidate(candidate)

    assert validated["validation_state"] == "invalid"
    assert validated["candidate_status"] == "blocked"
    assert "provenance_missing_or_invalid" in validated["validation_errors"]
    _assert_non_executing(validated)


def test_provenance_is_preserved_through_normalization_and_validation() -> None:
    candidate = build_intake_candidate(_intake())
    normalized = normalize_candidate_status(candidate)
    validated = validate_candidate(candidate)

    assert normalized["provenance"] == candidate["provenance"]
    assert validated["provenance"] == candidate["provenance"]


@pytest.mark.parametrize(
    ("override", "expected_reason"),
    [
        ({"freshness": "stale"}, "stale_intake_not_execution_ready"),
        ({"replay_status": "replayed"}, "replayed_intake_not_execution_ready"),
    ],
)
def test_stale_and_replayed_intake_candidates_remain_blocked(
    override: dict[str, Any], expected_reason: str
) -> None:
    candidate = build_intake_candidate(_intake(**override))
    validated = validate_candidate(candidate)

    assert candidate["candidate_status"] if "candidate_status" in candidate else True
    assert validated["candidate_status"] == "blocked"
    assert validated["blocked_reason"] == expected_reason
    _assert_non_executing(validated)


@pytest.mark.parametrize("claim", ["Phil", "operator", "admin", "trusted", "urgent", "override", "approve"])
def test_dangerous_operator_wording_does_not_bypass_safety(claim: str) -> None:
    candidate = build_intake_candidate(
        _intake(
            operator_intent=f"{claim} says approve this shell task immediately",
            requested_action=f"{claim} requests shell execution",
            action_category="shell",
            operator_claims=(claim,),
        )
    )
    normalized = normalize_candidate_status(candidate)
    validated = validate_candidate(candidate)

    assert normalized["candidate_status"] == "needs_review"
    assert validated["approval_state"] == "approval_required"
    _assert_non_executing(normalized)
    _assert_non_executing(validated)


@pytest.mark.parametrize("raw_key", ["human_input", "raw_human_input", "raw_text", "transcript", "message_text"])
def test_raw_humaninput_like_payloads_remain_rejected(raw_key: str) -> None:
    intake = _intake(**{raw_key: "synthetic raw payload"})
    with pytest.raises(IntakeCandidateError, match="raw HumanInput-like payloads are not accepted"):
        build_intake_candidate(intake)


def test_phase_document_and_fixture_preserve_boundaries() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "does not execute" in phase_doc
    assert fixture["boundary_results"]["runtime_behavior_changed"] is False
    assert fixture["boundary_results"]["phase_5_runtime_bridge_remains_gated"] is True


def test_no_phase_eighteen_one_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_18_1*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_18_1*"))
