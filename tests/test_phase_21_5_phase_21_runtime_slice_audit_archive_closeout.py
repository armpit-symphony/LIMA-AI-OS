"""Archive checks for the Phase 21 candidate provenance runtime slice."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from lima.kernel import build_intake_candidate, normalize_candidate_status, validate_candidate

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_21_5_PHASE_21_RUNTIME_SLICE_AUDIT_ARCHIVE_CLOSEOUT.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_21_5_phase_21_runtime_slice_audit_archive_closeout.json"
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
        "intake_id": "phase21-provenance-005",
        "source": "phase_21_archive_fixture",
        "source_channel": "test",
        "operator_intent": "Archive Phase 21 without execution.",
        "normalized_request": "archive phase 21",
        "requested_action": "summarize_candidate_archive",
        "action_category": "informational",
        "provenance": {
            "fixture": "phase_21_5_phase_21_runtime_slice_audit_archive_closeout",
            "lineage_seed": "phase21-archive-valid",
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


def test_phase_metadata_archives_completed_phase_21_scope() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "21.5"
    assert fixture["runtime_code_modified"] is False
    assert fixture["phase_21_completed_scope"] == [
        "phase_21_0_runtime_slice_preflight_audit_eligible_file_confirmation",
        "phase_21_1_candidate_provenance_acceptance_test_scaffolding",
        "phase_21_2_candidate_provenance_hardening_runtime_implementation",
        "phase_21_3_candidate_provenance_regression_review",
        "phase_21_4_runtime_slice_readiness_review",
    ]


def test_archive_lists_exact_runtime_files_touched() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase_21_runtime_files_touched"] == [
        "lima/kernel/intake_candidate.py",
        "lima/kernel/candidate_status.py",
    ]
    assert "lima/kernel/__init__.py" in fixture["runtime_files_not_touched"]
    assert "new_runtime_modules" in fixture["runtime_files_not_touched"]
    assert "all_other_lima_files" in fixture["runtime_files_not_touched"]


def test_phase_document_preserves_archive_boundaries_and_phase_22_gate() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "docs/tests/fixtures only" in phase_doc
    assert "does not modify `lima/`" in phase_doc
    assert "`lima/kernel/__init__.py` remained unchanged" in phase_doc
    assert "Phase 22 remains gated" in phase_doc
    assert "new explicit Phil approval" in phase_doc


def test_archive_runtime_safety_guarantees_still_hold() -> None:
    candidate = build_intake_candidate(_intake())
    normalized = normalize_candidate_status(candidate)
    validated = validate_candidate(candidate)
    assert normalized["provenance"] == candidate["provenance"]
    assert validated["provenance"] == candidate["provenance"]
    assert validated["validation_state"] == "valid"
    _assert_non_executing(candidate)
    _assert_non_executing(normalized)
    _assert_non_executing(validated)


def test_archive_suspicious_provenance_still_fails_closed() -> None:
    candidate = build_intake_candidate(_intake())
    candidate["provenance"] = {
        "fixture": "phase_21_5",
        "authority_claim": "Phil admin trusted urgent override approve",
    }
    validated = validate_candidate(candidate)
    assert validated["validation_state"] == "invalid"
    assert validated["candidate_status"] == "blocked"
    assert "provenance_authority_claim_not_allowed" in validated["validation_errors"]
    _assert_non_executing(validated)


def test_archive_boundary_results_show_no_forbidden_behavior() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified_by_phase_21_5"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["humaninput_runtime_bridge_added"] is False
    assert boundary["live_adapter_added"] is False
    assert boundary["intentcompiler_runtime_behavior_changed"] is False
    assert boundary["guardiandecision_runtime_behavior_changed"] is False
    assert boundary["approval_enforcement_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["shell_browser_network_file_mutation_robotics_physical_world_added"] is False
    assert boundary["background_worker_queue_daemon_subprocess_thread_database_write_added"] is False


def test_no_phase_twenty_one_five_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_21_5*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_21_5*"))
