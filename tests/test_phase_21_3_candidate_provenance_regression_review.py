"""Regression review checks for the Phase 21 provenance runtime slice."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from lima.kernel import IntakeCandidateError, build_intake_candidate, normalize_candidate_status, validate_candidate

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_21_3_CANDIDATE_PROVENANCE_REGRESSION_REVIEW.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_21_3_candidate_provenance_regression_review.json"
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
        "intake_id": "phase21-provenance-003",
        "source": "phase_21_regression_fixture",
        "source_channel": "test",
        "operator_intent": "Review provenance without execution.",
        "normalized_request": "review provenance",
        "requested_action": "summarize_candidate_provenance",
        "action_category": "informational",
        "provenance": {
            "fixture": "phase_21_3_candidate_provenance_regression_review",
            "lineage_seed": "phase21-regression-valid",
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


def test_phase_metadata_is_regression_review_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "21.3"
    assert fixture["runtime_code_modified"] is False
    assert fixture["reviewed_runtime_slice"] == (
        "phase_21_2_candidate_provenance_hardening_runtime_implementation"
    )
    assert fixture["boundary_results"]["lima_modified_by_phase_21_3"] is False


def test_phase_document_preserves_no_runtime_expansion_boundary() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "does not modify runtime files" in phase_doc
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "No runtime scope expansion is approved" in phase_doc


def test_valid_provenance_regression_remains_preserved() -> None:
    candidate = build_intake_candidate(_intake())
    normalized = normalize_candidate_status(candidate)
    validated = validate_candidate(candidate)
    assert normalized["provenance"] == candidate["provenance"]
    assert validated["provenance"] == candidate["provenance"]
    assert validated["validation_state"] == "valid"
    _assert_non_executing(normalized)
    _assert_non_executing(validated)


def test_malformed_provenance_regression_fails_closed() -> None:
    for provenance in ({1: "numeric-key"}, {"fixture": None}, {"": "empty-key"}):
        try:
            build_intake_candidate(_intake(provenance=provenance))
        except IntakeCandidateError:
            continue
        raise AssertionError("malformed provenance should be rejected")


def test_suspicious_provenance_regression_is_blocked_and_invalid() -> None:
    candidate = build_intake_candidate(_intake())
    candidate["provenance"] = {
        "fixture": "phase_21_3",
        "operator_claim": "Phil admin trusted urgent override approve",
    }
    normalized = normalize_candidate_status(candidate)
    validated = validate_candidate(candidate)
    assert normalized["candidate_status"] == "blocked"
    assert validated["validation_state"] == "invalid"
    assert "provenance_authority_claim_not_allowed" in validated["validation_errors"]
    _assert_non_executing(normalized)
    _assert_non_executing(validated)


def test_no_phase_twenty_one_three_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_21_3*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_21_3*"))
