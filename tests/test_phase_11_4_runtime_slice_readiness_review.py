"""Static and behavioral checks for Phase 11.4 readiness review."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from lima.kernel import normalize_candidate_status, validate_candidate
from lima.kernel.intake_candidate import build_intake_candidate


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_11_4_RUNTIME_SLICE_READINESS_REVIEW.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_11_4_runtime_slice_readiness_review.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def _candidate(**overrides: Any) -> dict[str, Any]:
    intake = {
        "synthetic": True,
        "test_only": True,
        "intake_id": "intake-11-4",
        "source": "test_shell",
        "source_channel": "test_room",
        "operator_intent": "summarize a harmless status note",
        "normalized_request": "summarize status note",
        "requested_action": "summarize",
        "action_category": "informational",
        "provenance": {"fixture": "phase_11_4", "lineage_seed": "seed-11-4"},
    }
    intake.update(overrides)
    return build_intake_candidate(intake)


def test_phase_is_docs_tests_fixtures_only_readiness_review() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "11.4"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False


def test_reviewed_runtime_files_are_limited_to_approved_kernel_files() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["reviewed_runtime_files"] == [
        "lima/kernel/candidate_status.py",
        "lima/kernel/__init__.py",
    ]


def test_readiness_findings_cover_non_executing_guarantees() -> None:
    findings = set(_load_json(PHASE_FIXTURE_PATH)["readiness_findings"])
    assert "inside_phase_10_2_file_map" in findings
    assert "status_normalization_non_authoritative" in findings
    assert "validation_fails_closed" in findings
    assert "execution_allowed_false" in findings
    assert "side_effects_allowed_false" in findings
    assert "approval_state_never_approved" in findings
    assert "provenance_preserved" in findings
    assert "phase_5_runtime_bridge_remains_gated" in findings


def test_runtime_behavior_remains_non_authoritative_under_review() -> None:
    candidate = _candidate()
    normalized = normalize_candidate_status(candidate)
    validated = validate_candidate(candidate)
    assert normalized["execution_allowed"] is False
    assert normalized["side_effects_allowed"] is False
    assert normalized["approved"] is False
    assert validated["validation_state"] == "valid"
    assert validated["execution_allowed"] is False
    assert validated["side_effects_allowed"] is False
    assert validated["approved"] is False


def test_readiness_outcome_allows_only_archive_or_non_runtime_review() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["ready_for"] == [
        "phase_11_5_audit_archive_closeout",
        "further_non_runtime_review",
    ]
    not_ready = set(fixture["not_ready_for"])
    assert "runtime_expansion" in not_ready
    assert "humaninput_runtime_bridge" in not_ready
    assert "sparkbot_wiring" in not_ready
    assert "live_adapter" in not_ready
    assert "approval_enforcement" in not_ready
    assert "execution" in not_ready
    assert "dispatch" in not_ready
    assert "audit_persistence" in not_ready


def test_phase_document_says_review_only_and_no_runtime_changes() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "docs/tests/fixtures only" in phase_doc
    assert "does not modify `lima/`" in phase_doc
    assert "does not change runtime behavior" in phase_doc
    assert "Ready for:" in phase_doc
    assert "Not ready for:" in phase_doc


def test_next_phase_is_archive_closeout() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["next_phase"] == "phase_11_5_phase_11_runtime_slice_audit_archive_closeout"


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["helper_behavior_changed"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["humaninput_runtime_bridge_added"] is False
    assert boundary["live_adapter_added"] is False
    assert boundary["intentcompiler_runtime_behavior_changed"] is False
    assert boundary["guardiandecision_runtime_behavior_changed"] is False
    assert boundary["approval_enforcement_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False


def test_no_phase_eleven_four_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_11_4*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_11_4*"))
