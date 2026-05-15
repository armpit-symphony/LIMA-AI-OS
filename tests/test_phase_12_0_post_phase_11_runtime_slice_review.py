"""Static checks for Phase 12.0 post-Phase-11 runtime slice review."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_12_0_POST_PHASE_11_RUNTIME_SLICE_REVIEW.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_12_0_post_phase_11_runtime_slice_review.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_docs_tests_fixtures_only_planning() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "12.0"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False


def test_phase_eleven_runtime_file_scope_is_preserved() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase_11_runtime_files_touched"] == [
        "lima/kernel/candidate_status.py",
        "lima/kernel/__init__.py",
    ]
    assert fixture["phase_11_eligible_runtime_files_not_touched"] == [
        "lima/kernel/intake_candidate.py"
    ]


def test_preserved_boundaries_keep_runtime_non_executing() -> None:
    boundaries = _load_json(PHASE_FIXTURE_PATH)["preserved_boundaries"]
    assert boundaries["runtime_remains_non_executing"] is True
    assert boundaries["execution_allowed_always_false"] is True
    assert boundaries["side_effects_allowed_always_false"] is True
    assert boundaries["approval_state_never_approved"] is True
    assert boundaries["phase_5_runtime_bridge_remains_gated"] is True
    assert boundaries["operator_admin_phil_trusted_bypass"] is False


def test_phase_twelve_options_are_planning_only() -> None:
    options = set(_load_json(PHASE_FIXTURE_PATH)["phase_12_options_to_review"])
    assert "pause_and_preserve_current_runtime_state" in options
    assert "future_narrow_non_executing_runtime_slice_design" in options
    assert "sparkbot_integration_boundary_design" in options
    assert "robo_os_physical_world_boundary_design" in options
    assert "threat_model_security_test_strengthening" in options


def test_phase_document_blocks_runtime_and_external_behavior() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "docs/tests/fixtures-only planning lane" in phase_doc
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "does not add a HumanInput runtime bridge" in phase_doc
    assert "does not execute" in phase_doc
    assert "does not dispatch" in phase_doc
    assert "does not persist audit" in phase_doc


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["candidate_status_expanded"] is False
    assert boundary["intake_candidate_expanded"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["humaninput_runtime_bridge_added"] is False
    assert boundary["live_adapter_added"] is False
    assert boundary["approval_enforcement_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False


def test_no_phase_twelve_zero_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_12_0*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_12_0*"))
