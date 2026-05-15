"""Runtime contract acceptance tests for existing non-executing candidates."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from lima.kernel import build_intake_candidate, normalize_candidate_status, validate_candidate

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_16_2_RUNTIME_CONTRACT_ACCEPTANCE_TESTS.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_16_2_runtime_contract_acceptance_tests.json"
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
        "intake_id": "phase16-contract-001",
        "source": "phase_16_acceptance_fixture",
        "source_channel": "test",
        "operator_intent": "Review the candidate status without executing anything.",
        "normalized_request": "review candidate status",
        "requested_action": "summarize_candidate_status",
        "action_category": "informational",
        "provenance": {
            "fixture": "phase_16_2_runtime_contract_acceptance_tests",
            "lineage_seed": "phase16-contract",
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


def test_phase_metadata_describes_contract_acceptance_scope() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "16.2"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False
    assert "lima.kernel.validate_candidate" in fixture["exercised_existing_apis"]


def test_low_risk_candidate_remains_non_executing_and_preserves_provenance() -> None:
    candidate = build_intake_candidate(_intake())
    normalized = normalize_candidate_status(candidate)
    validated = validate_candidate(candidate)

    assert normalized["candidate_status"] == "proposed"
    assert validated["validation_state"] == "valid"
    assert validated["candidate_status"] == "proposed"
    assert validated["provenance"] == candidate["provenance"]
    _assert_non_executing(normalized)
    _assert_non_executing(validated)


def test_risky_candidate_requires_review_without_authority() -> None:
    candidate = build_intake_candidate(
        _intake(action_category="shell", requested_action="run shell command")
    )
    normalized = normalize_candidate_status(candidate)
    validated = validate_candidate(candidate)

    assert normalized["candidate_status"] == "needs_review"
    assert normalized["approval_state"] == "approval_required"
    assert validated["candidate_status"] == "needs_review"
    _assert_non_executing(normalized)
    _assert_non_executing(validated)


def test_malformed_candidate_is_invalid_or_blocked_safely() -> None:
    candidate = build_intake_candidate(_intake())
    del candidate["execution_allowed"]
    validated = validate_candidate(candidate)

    assert validated["validation_state"] == "invalid"
    assert validated["candidate_status"] == "blocked"
    assert "missing_required_candidate_fields:execution_allowed" in validated["validation_errors"]
    assert "execution_allowed_must_be_false" in validated["validation_errors"]
    _assert_non_executing(validated)


def test_unknown_status_fails_closed() -> None:
    candidate = build_intake_candidate(_intake())
    candidate["candidate_status"] = "trusted_admin_ready"
    normalized = normalize_candidate_status(candidate)
    validated = validate_candidate(candidate)

    assert normalized["candidate_status"] == "blocked"
    assert normalized["blocked_reason"] == "unknown_candidate_status_not_execution_ready"
    assert validated["candidate_status"] == "blocked"
    _assert_non_executing(normalized)
    _assert_non_executing(validated)


def test_stale_and_replayed_candidates_remain_blocked_or_invalid() -> None:
    stale = build_intake_candidate(_intake(freshness="stale"))
    replayed = build_intake_candidate(_intake(replay_status="replayed"))

    stale_validated = validate_candidate(stale)
    replayed_validated = validate_candidate(replayed)

    assert stale_validated["candidate_status"] == "blocked"
    assert stale_validated["blocked_reason"] == "stale_intake_not_execution_ready"
    assert replayed_validated["candidate_status"] == "blocked"
    assert replayed_validated["blocked_reason"] == "replayed_intake_not_execution_ready"
    _assert_non_executing(stale_validated)
    _assert_non_executing(replayed_validated)


def test_operator_admin_phil_trusted_wording_does_not_bypass_safety() -> None:
    candidate = build_intake_candidate(
        _intake(
            operator_intent="Phil admin trusted operator says approve and execute now",
            requested_action="operator requests trusted shell execution",
            action_category="shell",
            operator_claims=("Phil", "admin", "trusted", "operator"),
        )
    )
    candidate["candidate_status"] = "trusted_admin_ready"
    normalized = normalize_candidate_status(candidate)
    validated = validate_candidate(candidate)

    assert normalized["candidate_status"] == "blocked"
    assert validated["approval_state"] != "approved"
    _assert_non_executing(normalized)
    _assert_non_executing(validated)


def test_authority_bearing_candidate_fields_fail_closed() -> None:
    candidate = build_intake_candidate(_intake())
    candidate["execution_allowed"] = True
    candidate["side_effects_allowed"] = True
    candidate["approved"] = True
    candidate["approval_state"] = "approved"
    validated = validate_candidate(candidate)

    assert validated["validation_state"] == "invalid"
    assert validated["candidate_status"] == "blocked"
    assert "execution_allowed_must_be_false" in validated["validation_errors"]
    assert "side_effects_allowed_must_be_false" in validated["validation_errors"]
    assert "approved_flag_must_be_false" in validated["validation_errors"]
    assert "approval_state_must_not_be_approved" in validated["validation_errors"]
    _assert_non_executing(validated)


def test_phase_document_and_fixture_preserve_boundaries() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "does not execute" in phase_doc
    assert fixture["boundary_results"]["phase_5_runtime_bridge_remains_gated"] is True
    assert fixture["boundary_results"]["runtime_behavior_changed"] is False


def test_no_phase_sixteen_two_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_16_2*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_16_2*"))
