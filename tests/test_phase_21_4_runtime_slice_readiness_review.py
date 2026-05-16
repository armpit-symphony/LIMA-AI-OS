"""Readiness review checks for the Phase 21 runtime slice."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from lima.kernel import build_intake_candidate, normalize_candidate_status, validate_candidate

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_21_4_RUNTIME_SLICE_READINESS_REVIEW.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_21_4_runtime_slice_readiness_review.json"
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
        "intake_id": "phase21-provenance-004",
        "source": "phase_21_readiness_fixture",
        "source_channel": "test",
        "operator_intent": "Review readiness without execution.",
        "normalized_request": "review readiness",
        "requested_action": "summarize_candidate_readiness",
        "action_category": "informational",
        "provenance": {
            "fixture": "phase_21_4_runtime_slice_readiness_review",
            "lineage_seed": "phase21-readiness-valid",
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


def test_phase_metadata_marks_ready_for_archive_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "21.4"
    assert fixture["runtime_code_modified"] is False
    assert fixture["readiness_result"] == "ready_for_phase_21_5_archive_closeout"
    assert "phase_21_2_candidate_provenance_hardening_runtime_implementation" in fixture[
        "completed_phase_21_scope"
    ]
    assert fixture["readiness_findings"]["phase_22_requires_explicit_phil_approval"] is True


def test_phase_document_keeps_runtime_expansion_gated() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "docs/tests/fixtures only" in phase_doc
    assert "does not modify `lima/`" in phase_doc
    assert "Phase 22 must remain gated" in phase_doc
    assert "requires a new explicit Phil approval" in phase_doc


def test_readiness_checks_runtime_slice_invariants() -> None:
    candidate = build_intake_candidate(_intake())
    normalized = normalize_candidate_status(candidate)
    validated = validate_candidate(candidate)
    assert normalized["provenance"] == candidate["provenance"]
    assert validated["validation_state"] == "valid"
    _assert_non_executing(candidate)
    _assert_non_executing(normalized)
    _assert_non_executing(validated)


def test_readiness_checks_suspicious_provenance_fail_closed() -> None:
    candidate = build_intake_candidate(_intake())
    candidate["provenance"] = {
        "fixture": "phase_21_4",
        "authority_claim": "Phil admin trusted urgent override approve",
    }
    validated = validate_candidate(candidate)
    assert validated["validation_state"] == "invalid"
    assert validated["candidate_status"] == "blocked"
    assert "provenance_authority_claim_not_allowed" in validated["validation_errors"]
    _assert_non_executing(validated)


def test_boundary_results_show_no_forbidden_phase_21_4_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified_by_phase_21_4"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["humaninput_runtime_bridge_added"] is False
    assert boundary["live_adapter_added"] is False
    assert boundary["approval_enforcement_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_behavior_added"] is False


def test_no_phase_twenty_one_four_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_21_4*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_21_4*"))
