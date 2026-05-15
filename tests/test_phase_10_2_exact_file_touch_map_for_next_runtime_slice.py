"""Static checks for Phase 10.2 exact future file-touch map."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_10_2_EXACT_FILE_TOUCH_MAP_FOR_NEXT_RUNTIME_SLICE.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_10_2_exact_file_touch_map_for_next_runtime_slice.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_no_code_file_touch_mapping_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "10.2"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False
    assert fixture["phase_11_runtime_implementation_approved_now"] is False


def test_future_eligible_runtime_files_are_exact() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["future_eligible_runtime_files"] == [
        "lima/kernel/intake_candidate.py",
        "lima/kernel/__init__.py",
        "lima/kernel/candidate_status.py",
    ]


def test_future_file_limits_are_non_executing_and_side_effect_free() -> None:
    limits = _load_json(PHASE_FIXTURE_PATH)["future_file_limits"]
    assert "no_execution" in limits["lima/kernel/intake_candidate.py"]
    assert "no_approval" in limits["lima/kernel/intake_candidate.py"]
    assert "no_dispatch" in limits["lima/kernel/intake_candidate.py"]
    assert "no_persistence" in limits["lima/kernel/intake_candidate.py"]
    assert "no_external_service_calls" in limits["lima/kernel/intake_candidate.py"]
    assert "import_must_remain_side_effect_free" in limits["lima/kernel/__init__.py"]
    assert "pure_in_process_non_executing_authority_free" in limits["lima/kernel/candidate_status.py"]


def test_forbidden_runtime_surfaces_exclude_broad_runtime_work() -> None:
    forbidden = set(_load_json(PHASE_FIXTURE_PATH)["forbidden_runtime_surfaces"])
    assert "lima/adapters/**" in forbidden
    assert "lima/contracts/**" in forbidden
    assert "lima/guardian/**" in forbidden
    assert "lima/harness/**" in forbidden
    assert "lima/io/**" in forbidden
    assert "lima/persistence/**" in forbidden
    assert "lima/services/**" in forbidden
    assert "lima/spine/**" in forbidden
    assert "sparkbot_files" in forbidden
    assert "tests/support/**" in forbidden


def test_required_future_scope_limits_preserve_phase_nine_safety() -> None:
    limits = _load_json(PHASE_FIXTURE_PATH)["required_future_scope_limits"]
    assert limits["execution_allowed_false"] is True
    assert limits["side_effects_allowed_false"] is True
    assert limits["approval_state_never_approved"] is True
    assert limits["provenance_preserved"] is True
    assert limits["unsafe_candidates_blocked_or_not_ready"] is True
    assert limits["phase_5_runtime_bridge_remains_gated"] is True


def test_phase_document_does_not_approve_runtime_implementation() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "It does not implement that slice" in phase_doc
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "may be created only if Phase 11 is explicitly approved" in phase_doc


def test_next_phase_is_acceptance_test_and_rollback_plan() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["next_phase"] == "phase_10_3_acceptance_test_and_rollback_plan"


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["helper_behavior_changed"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["live_adapter_added"] is False
    assert boundary["approval_enforcement_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False


def test_no_phase_ten_two_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_10_2*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_10_2*"))
