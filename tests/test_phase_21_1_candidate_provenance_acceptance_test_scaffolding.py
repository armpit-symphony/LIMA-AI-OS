"""Acceptance scaffolding for Phase 21 candidate provenance hardening."""

from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any

import pytest

from lima.kernel import IntakeCandidateError, build_intake_candidate, normalize_candidate_status, validate_candidate

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_21_1_CANDIDATE_PROVENANCE_ACCEPTANCE_TEST_SCAFFOLDING.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_21_1_candidate_provenance_acceptance_test_scaffolding.json"
)
CASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_21_1_candidate_provenance_acceptance_cases.json"
)
RUNTIME_FILES = (
    REPO_ROOT / "lima" / "kernel" / "intake_candidate.py",
    REPO_ROOT / "lima" / "kernel" / "candidate_status.py",
)
FORBIDDEN_NAMES = {
    "subprocess",
    "requests",
    "urllib",
    "httpx",
    "socket",
    "selenium",
    "playwright",
    "Sparkbot",
    "HumanInputBridge",
    "IntentCompiler",
    "GuardianDecision",
    "dispatch",
    "execute",
    "persist",
    "threading",
    "queue",
}


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def _intake(**overrides: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "synthetic": True,
        "test_only": True,
        "intake_id": "phase21-provenance-001",
        "source": "phase_21_acceptance_fixture",
        "source_channel": "test",
        "operator_intent": "Review provenance without executing anything.",
        "normalized_request": "review provenance",
        "requested_action": "summarize_candidate_provenance",
        "action_category": "informational",
        "provenance": {
            "fixture": "phase_21_1_candidate_provenance_acceptance_test_scaffolding",
            "lineage_seed": "phase21-default",
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


def test_phase_metadata_scaffolds_provenance_acceptance_coverage() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "21.1"
    assert fixture["runtime_code_modified"] is False
    assert fixture["approved_future_runtime_files"] == [
        "lima/kernel/intake_candidate.py",
        "lima/kernel/candidate_status.py",
    ]
    assert "valid_non_executing_candidate_preserves_provenance" in fixture["acceptance_coverage"]
    assert "forbidden_integrations_unreachable" in fixture["acceptance_coverage"]


def test_valid_non_executing_candidate_preserves_provenance() -> None:
    candidate = build_intake_candidate(_intake())
    normalized = normalize_candidate_status(candidate)
    validated = validate_candidate(candidate)

    assert normalized["provenance"] == candidate["provenance"]
    assert validated["provenance"] == candidate["provenance"]
    assert validated["validation_state"] == "valid"
    _assert_non_executing(candidate)
    _assert_non_executing(normalized)
    _assert_non_executing(validated)


@pytest.mark.parametrize("case", _load_json(CASE_FIXTURE_PATH)["cases"])
def test_fixture_provenance_cases_are_safe(case: dict[str, Any]) -> None:
    intake = _intake()
    if case.get("omit_provenance"):
        del intake["provenance"]
    elif "provenance" in case:
        intake["provenance"] = case["provenance"]
    for field in ("freshness", "replay_status", "operator_intent", "requested_action", "action_category"):
        if field in case:
            intake[field] = case[field]

    if case["expected"] == "valid":
        candidate = build_intake_candidate(intake)
        validated = validate_candidate(candidate)
        assert validated["validation_state"] == "valid"
        assert validated["provenance"] == case["provenance"]
        _assert_non_executing(validated)
        return

    if case["expected"] == "invalid":
        with pytest.raises(IntakeCandidateError):
            build_intake_candidate(intake)
        return

    candidate = build_intake_candidate(intake)
    normalized = normalize_candidate_status(candidate)
    validated = validate_candidate(candidate)
    _assert_non_executing(normalized)
    _assert_non_executing(validated)

    if case["expected"] == "blocked":
        assert validated["candidate_status"] == "blocked"
    elif case["expected"] == "needs_review_or_blocked":
        assert validated["candidate_status"] in {"needs_review", "blocked"}
        assert validated["approval_state"] != "approved"


def test_authority_bearing_fields_still_fail_closed() -> None:
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


def test_runtime_candidate_files_do_not_import_or_call_forbidden_surfaces() -> None:
    for runtime_file in RUNTIME_FILES:
        tree = ast.parse(runtime_file.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                imported = [alias.name for alias in node.names]
                assert not (set(imported) & FORBIDDEN_NAMES)
            if isinstance(node, ast.Name):
                assert node.id not in FORBIDDEN_NAMES
            if isinstance(node, ast.Attribute):
                assert node.attr not in FORBIDDEN_NAMES


def test_phase_document_and_fixture_preserve_boundaries() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "does not implement provenance hardening" in phase_doc
    assert fixture["boundary_results"]["phase_5_runtime_bridge_remains_gated"] is True
    assert fixture["boundary_results"]["runtime_behavior_changed"] is False


def test_no_phase_twenty_one_one_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_21_1*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_21_1*"))
