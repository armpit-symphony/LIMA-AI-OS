"""Candidate provenance regression tests for Phase 23.1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from lima.kernel import IntakeCandidateError, build_intake_candidate, normalize_candidate_status, validate_candidate

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_23_1_CANDIDATE_PROVENANCE_REGRESSION_TESTS.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_23_1_candidate_provenance_regression_tests.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def _intake(**overrides: Any) -> dict[str, Any]:
    intake: dict[str, Any] = {
        "synthetic": True,
        "test_only": True,
        "intake_id": "phase23-provenance-regression",
        "source": "phase_23_1_fixture",
        "source_channel": "test",
        "operator_intent": "Review candidate provenance without execution.",
        "normalized_request": "review candidate provenance",
        "requested_action": "summarize_candidate_provenance",
        "action_category": "informational",
        "provenance": {
            "fixture": "phase_23_1_candidate_provenance_regression_tests",
            "lineage_seed": "phase23-valid-lineage",
        },
    }
    intake.update(overrides)
    return intake


def _assert_non_executing(candidate: dict[str, Any]) -> None:
    assert candidate["executable"] is False
    assert candidate["execution_allowed"] is False
    assert candidate["side_effects_allowed"] is False
    assert candidate["approved"] is False
    assert candidate["approval_state"] != "approved"
    assert candidate["phase_5_humaninput_runtime_bridge_gated"] is True
    assert candidate.get("intent_envelope_created") is False
    assert candidate.get("guardian_decision_created") is False


def test_phase_metadata_describes_regression_coverage() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "23.1"
    assert fixture["runtime_code_modified"] is False
    assert "valid_provenance_preserved" in fixture["coverage"]
    assert "non_executing_invariants_preserved" in fixture["coverage"]


def test_valid_provenance_is_preserved_across_candidate_apis() -> None:
    candidate = build_intake_candidate(_intake())
    normalized = normalize_candidate_status(candidate)
    validated = validate_candidate(candidate)
    assert candidate["provenance"] == _intake()["provenance"]
    assert normalized["provenance"] == candidate["provenance"]
    assert validated["provenance"] == candidate["provenance"]
    assert validated["validation_state"] == "valid"
    _assert_non_executing(candidate)
    _assert_non_executing(normalized)
    _assert_non_executing(validated)


def test_missing_provenance_is_rejected_at_construction_and_invalid_at_validation() -> None:
    intake = _intake()
    del intake["provenance"]
    with pytest.raises(IntakeCandidateError, match="intake missing required fields"):
        build_intake_candidate(intake)

    candidate = build_intake_candidate(_intake())
    del candidate["provenance"]
    validated = validate_candidate(candidate)
    assert validated["validation_state"] == "invalid"
    assert validated["candidate_status"] == "blocked"
    assert "missing_required_candidate_fields:provenance" in validated["validation_errors"]
    assert "provenance_missing_or_invalid" in validated["validation_errors"]
    _assert_non_executing(validated)


@pytest.mark.parametrize(
    "provenance, expected_error",
    [
        ({}, "provenance must be a non-empty mapping"),
        ({1: "numeric-key"}, "provenance keys must be non-empty strings"),
        ({"fixture": None}, "provenance values must not be missing"),
        ("not-a-mapping", "provenance must be a non-empty mapping"),
    ],
)
def test_malformed_provenance_is_rejected_at_construction(
    provenance: Any, expected_error: str
) -> None:
    with pytest.raises(IntakeCandidateError, match=expected_error):
        build_intake_candidate(_intake(provenance=provenance))


@pytest.mark.parametrize(
    "provenance, expected_validation_error",
    [
        ({}, "provenance_missing_or_invalid"),
        ({1: "numeric-key"}, "provenance_key_missing_or_invalid"),
        ({"fixture": None}, "provenance_value_missing_or_invalid"),
        ("not-a-mapping", "provenance_missing_or_invalid"),
    ],
)
def test_malformed_provenance_is_invalid_at_validation(
    provenance: Any, expected_validation_error: str
) -> None:
    candidate = build_intake_candidate(_intake())
    candidate["provenance"] = provenance
    validated = validate_candidate(candidate)
    assert validated["validation_state"] == "invalid"
    assert validated["candidate_status"] == "blocked"
    assert expected_validation_error in validated["validation_errors"]
    _assert_non_executing(validated)


@pytest.mark.parametrize(
    "override, expected_blocked_reason",
    [
        ({"freshness": "stale"}, "stale_intake_not_execution_ready"),
        ({"replay_status": "replayed"}, "replayed_intake_not_execution_ready"),
    ],
)
def test_stale_and_replayed_candidates_remain_blocked(
    override: dict[str, str], expected_blocked_reason: str
) -> None:
    candidate = build_intake_candidate(_intake(**override))
    validated = validate_candidate(candidate)
    assert candidate["approval_state"] == "blocked"
    assert validated["candidate_status"] == "blocked"
    assert validated["blocked_reason"] == expected_blocked_reason
    _assert_non_executing(candidate)
    _assert_non_executing(validated)


def test_phase_document_and_boundary_fixture_keep_scope_test_only() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert "test-only hardening" in phase_doc
    assert "does not modify `lima/`" in phase_doc
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False


def test_no_phase_23_1_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_23_1*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_23_1*"))
