"""Runtime acceptance tests for Phase 21 candidate provenance hardening."""

from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any

import pytest

from lima.kernel import IntakeCandidateError, build_intake_candidate, normalize_candidate_status, validate_candidate

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_21_2_CANDIDATE_PROVENANCE_HARDENING_RUNTIME_IMPLEMENTATION.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_21_2_candidate_provenance_hardening_runtime_implementation.json"
)
APPROVED_RUNTIME_FILES = (
    REPO_ROOT / "lima" / "kernel" / "intake_candidate.py",
    REPO_ROOT / "lima" / "kernel" / "candidate_status.py",
)
FORBIDDEN_RUNTIME_FILE = REPO_ROOT / "lima" / "kernel" / "__init__.py"
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
        "intake_id": "phase21-provenance-002",
        "source": "phase_21_runtime_fixture",
        "source_channel": "test",
        "operator_intent": "Review provenance without execution.",
        "normalized_request": "review provenance",
        "requested_action": "summarize_candidate_provenance",
        "action_category": "informational",
        "provenance": {
            "fixture": "phase_21_2_candidate_provenance_hardening_runtime_implementation",
            "lineage_seed": "phase21-runtime-valid",
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


def test_phase_metadata_declares_exact_runtime_touch_scope() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "21.2"
    assert fixture["runtime_files_touched"] == [
        "lima/kernel/intake_candidate.py",
        "lima/kernel/candidate_status.py",
    ]
    assert "lima/kernel/__init__.py" in fixture["forbidden_runtime_files_untouched"]
    assert "status_normalization_blocks_suspicious_provenance_authority_claims" in fixture[
        "implemented_guarantees"
    ]


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


@pytest.mark.parametrize(
    "provenance, expected_message",
    [
        ({1: "numeric-key"}, "provenance keys must be non-empty strings"),
        ({"fixture": None}, "provenance values must not be missing"),
        ({"": "empty-key"}, "provenance keys must be non-empty strings"),
    ],
)
def test_candidate_construction_rejects_malformed_provenance(
    provenance: dict[Any, Any], expected_message: str
) -> None:
    with pytest.raises(IntakeCandidateError, match=expected_message):
        build_intake_candidate(_intake(provenance=provenance))


@pytest.mark.parametrize(
    "provenance, expected_error",
    [
        ({}, "provenance_missing_or_invalid"),
        ({1: "numeric-key"}, "provenance_key_missing_or_invalid"),
        ({"fixture": None}, "provenance_value_missing_or_invalid"),
        (
            {
                "fixture": "phase_21_2",
                "operator_claim": "Phil admin trusted urgent override approve",
            },
            "provenance_authority_claim_not_allowed",
        ),
    ],
)
def test_candidate_validation_marks_bad_provenance_invalid(
    provenance: dict[Any, Any], expected_error: str
) -> None:
    candidate = build_intake_candidate(_intake())
    candidate["provenance"] = provenance
    validated = validate_candidate(candidate)

    assert validated["validation_state"] == "invalid"
    assert validated["candidate_status"] == "blocked"
    assert expected_error in validated["validation_errors"]
    _assert_non_executing(validated)


def test_status_normalization_blocks_suspicious_provenance_without_approval() -> None:
    candidate = build_intake_candidate(_intake())
    candidate["provenance"] = {
        "fixture": "phase_21_2",
        "operator_claim": "Phil admin trusted urgent override approve",
    }
    normalized = normalize_candidate_status(candidate)

    assert normalized["candidate_status"] == "blocked"
    assert normalized["blocked_reason"] == "provenance_authority_claim_not_allowed"
    _assert_non_executing(normalized)


def test_stale_and_replayed_provenance_remain_blocked_or_invalid() -> None:
    stale = validate_candidate(build_intake_candidate(_intake(freshness="stale")))
    replayed = validate_candidate(build_intake_candidate(_intake(replay_status="replayed")))

    assert stale["candidate_status"] == "blocked"
    assert replayed["candidate_status"] == "blocked"
    assert stale["blocked_reason"] == "stale_intake_not_execution_ready"
    assert replayed["blocked_reason"] == "replayed_intake_not_execution_ready"
    _assert_non_executing(stale)
    _assert_non_executing(replayed)


def test_authority_flags_still_cannot_approve_or_dispatch() -> None:
    candidate = build_intake_candidate(_intake())
    candidate["execution_allowed"] = True
    candidate["side_effects_allowed"] = True
    candidate["approval_state"] = "approved"
    candidate["approved"] = True
    validated = validate_candidate(candidate)

    assert validated["validation_state"] == "invalid"
    assert "execution_allowed_must_be_false" in validated["validation_errors"]
    assert "side_effects_allowed_must_be_false" in validated["validation_errors"]
    assert "approval_state_must_not_be_approved" in validated["validation_errors"]
    assert "approved_flag_must_be_false" in validated["validation_errors"]
    _assert_non_executing(validated)


def test_runtime_candidate_files_do_not_import_or_call_forbidden_surfaces() -> None:
    for runtime_file in APPROVED_RUNTIME_FILES:
        tree = ast.parse(runtime_file.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                imported = [alias.name for alias in node.names]
                assert not (set(imported) & FORBIDDEN_NAMES)
            if isinstance(node, ast.Name):
                assert node.id not in FORBIDDEN_NAMES
            if isinstance(node, ast.Attribute):
                assert node.attr not in FORBIDDEN_NAMES


def test_forbidden_runtime_and_support_scope_remains_absent() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert "does not modify `lima/kernel/__init__.py`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert FORBIDDEN_RUNTIME_FILE.exists()
    assert fixture["boundary_results"]["tests_support_modified"] is False
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_21_2*"))
