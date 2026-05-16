"""Suspicious provenance fixture hardening tests for Phase 23.2."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from lima.kernel import build_intake_candidate, normalize_candidate_status, validate_candidate

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_23_2_SUSPICIOUS_PROVENANCE_FIXTURE_HARDENING.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_23_2_suspicious_provenance_fixture_hardening.json"
)
CASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_23_2_suspicious_provenance_cases.json"
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
        "intake_id": "phase23-suspicious-provenance",
        "source": "phase_23_2_fixture",
        "source_channel": "test",
        "operator_intent": "Review suspicious provenance without execution.",
        "normalized_request": "review suspicious provenance",
        "requested_action": "summarize_suspicious_provenance",
        "action_category": "informational",
        "provenance": {
            "fixture": "phase_23_2_suspicious_provenance_fixture_hardening",
            "lineage_seed": "phase23-suspicious-valid",
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


def test_phase_metadata_links_case_fixture_and_boundaries() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "23.2"
    assert fixture["runtime_code_modified"] is False
    assert fixture["case_fixture"] == (
        "tests/fixtures/runtime_extraction/phase_23_2_suspicious_provenance_cases.json"
    )
    assert "authority_claim_in_nested_provenance_mapping" in fixture["coverage"]


@pytest.mark.parametrize("case", _load_json(CASE_FIXTURE_PATH)["cases"])
def test_suspicious_and_risky_provenance_fixtures_fail_closed(case: dict[str, Any]) -> None:
    intake = _intake(
        provenance=case["provenance"],
        action_category=case.get("action_category", "informational"),
    )
    candidate = build_intake_candidate(intake)
    normalized = normalize_candidate_status(candidate)
    validated = validate_candidate(candidate)

    _assert_non_executing(candidate)
    _assert_non_executing(normalized)
    _assert_non_executing(validated)

    if "expected_validation_error" in case:
        assert normalized["candidate_status"] == "blocked"
        assert validated["validation_state"] == "invalid"
        assert case["expected_validation_error"] in validated["validation_errors"]
    else:
        assert normalized["candidate_status"] == case["expected_status"]
        assert validated["validation_state"] == "valid"
        assert validated["approval_state"] != "approved"


def test_case_fixture_contains_required_suspicious_shapes() -> None:
    case_ids = {case["case_id"] for case in _load_json(CASE_FIXTURE_PATH)["cases"]}
    assert "value_claims_phil_override" in case_ids
    assert "key_claims_operator" in case_ids
    assert "nested_mapping_claims_admin" in case_ids
    assert "list_claims_emergency_override" in case_ids
    assert "shell_attempt_metadata" in case_ids
    assert "robotics_attempt_metadata" in case_ids


def test_phase_document_preserves_test_only_scope() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "test-only hardening" in phase_doc
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


def test_no_phase_23_2_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_23_2*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_23_2*"))
