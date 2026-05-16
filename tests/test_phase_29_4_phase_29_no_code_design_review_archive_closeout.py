"""Phase 29 no-code design review archive tests for Phase 29.4."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_29_4_PHASE_29_NO_CODE_DESIGN_REVIEW_ARCHIVE_CLOSEOUT.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_29_4_phase_29_no_code_design_review_archive_closeout.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_29_4_archives_phase_29_as_no_code_design_review() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "29.4"
    assert fixture["phase_28_audit_result"] == "PASS"
    assert fixture["runtime_code_modified"] is False
    assert fixture["completed_phases"] == ["29.0", "29.1", "29.2", "29.3"]
    assert "completed docs/tests/fixtures-only no-code design review" in phase_doc


def test_archive_preserves_recommended_future_slice_and_file_scope() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    eligible = set(fixture["future_eligible_runtime_files"])
    forbidden = set(fixture["future_forbidden_runtime_files"])
    assert fixture["recommended_future_runtime_slice"] == "read_only_runtime_state_inspection"
    assert eligible == {
        "lima/kernel/runtime_state.py",
        "lima/kernel/__init__.py_only_if_safe_public_export_required",
    }
    assert "lima/kernel/intake_candidate.py" in forbidden
    assert "lima/kernel/candidate_status.py" in forbidden
    assert "all_other_lima_files" in forbidden
    assert "tests/support" in forbidden


def test_archive_confirms_phase_29_added_no_forbidden_behavior() -> None:
    did_not_add = _load_json(PHASE_FIXTURE_PATH)["phase_29_did_not_add"]
    assert did_not_add["runtime_implementation"] is True
    assert did_not_add["lima_changes"] is False
    assert did_not_add["tests_support_changes"] is False
    assert did_not_add["sparkbot_wiring"] is False
    assert did_not_add["humaninput_runtime_bridge"] is False
    assert did_not_add["live_adapter"] is False
    assert did_not_add["intentcompiler_runtime_behavior"] is False
    assert did_not_add["guardiandecision_runtime_behavior"] is False
    assert did_not_add["approval_enforcement"] is False
    assert did_not_add["execution"] is False
    assert did_not_add["dispatch"] is False
    assert did_not_add["audit_persistence"] is False
    assert did_not_add["shell_browser_network_file_robotics_physical_world_behavior"] is False
    assert did_not_add["external_service_calls"] is False
    assert (
        did_not_add[
            "background_workers_queues_daemons_subprocesses_threads_database_writes_hidden_side_effects"
        ]
        is False
    )


def test_future_eligibility_requires_approval_tests_rollback_and_audit() -> None:
    eligibility = _load_json(PHASE_FIXTURE_PATH)["future_implementation_eligibility"]
    assert eligibility["explicit_phil_approval_required"] is True
    assert eligibility["tests_before_runtime_edits"] is True
    assert eligibility["rollback_plan_required"] is True
    assert eligibility["audit_proof_required"] is True
    assert eligibility["deterministic_local_only_read_only"] is True
    assert eligibility["non_authoritative_output_only"] is True
    assert eligibility["execution_allowed_remains_false"] is True
    assert eligibility["side_effects_allowed_remains_false"] is True
    assert eligibility["approval_state_never_approved"] is True
    assert eligibility["phase_5_runtime_bridge_remains_gated"] is True


def test_phase_30_remains_unapproved_and_question_is_exactly_preserved() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    question = fixture["phase_30_approval_question"]
    assert fixture["phase_30_approved"] is False
    assert "Do you approve Phase 30" in question
    assert "read-only runtime state inspection" in question
    assert "lima/kernel/runtime_state.py" in question
    assert "lima/kernel/__init__.py" in question
    assert "lima/kernel/intake_candidate.py" in question
    assert "lima/kernel/candidate_status.py" in question
    assert "all other `lima/` files" in question
    assert "tests/support/" in question
    assert "Sparkbot wiring" in question
    assert "HumanInput runtime bridge behavior" in question
    assert "approval enforcement" in question
    assert "execution" in question
    assert "dispatch" in question
    assert "audit persistence" in question
    assert "hidden side effects" in question


def test_no_phase_29_4_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_29_4*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_29_4*"))
