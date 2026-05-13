"""Static checks for Phase 5.9 HumanInput runtime bridge validation matrix."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_5_9_HUMANINPUT_RUNTIME_BRIDGE_BOUNDARY_VALIDATION_MATRIX.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_5_9_humaninput_runtime_bridge_boundary_validation_matrix.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_fixture_declares_validation_matrix_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "5.9"
    assert fixture["status"] == "humaninput_runtime_bridge_boundary_validation_matrix"
    assert fixture["non_runtime"] is True
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["validation_matrix_only"] is True


def test_doc_says_matrix_is_not_runtime_schema_or_classifier() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "does not implement a runtime bridge" in phase_doc
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "not a runtime schema and is not a classifier implementation" in phase_doc


def test_matrix_contains_required_categories() -> None:
    rows = _load_json(PHASE_FIXTURE_PATH)["validation_matrix"]
    categories = {row["category"] for row in rows}
    assert categories == {
        "low_risk_informational_request",
        "shell_command_request",
        "browser_network_request",
        "file_mutation_request",
        "robotics_physical_world_request",
        "admin_trusted_phil_bypass_attempt",
        "ambiguous_request",
        "empty_request",
        "malformed_request",
        "replayed_stale_request",
    }


def test_all_matrix_rows_are_non_executable_and_side_effects_blocked() -> None:
    rows = _load_json(PHASE_FIXTURE_PATH)["validation_matrix"]
    assert all(row["executable"] is False for row in rows)
    assert all(row["execution_allowed"] is False for row in rows)
    assert all(row["side_effects_allowed"] is False for row in rows)


def test_low_risk_request_is_only_non_executable_proposed_candidate() -> None:
    rows = {
        row["category"]: row for row in _load_json(PHASE_FIXTURE_PATH)["validation_matrix"]
    }
    low_risk = rows["low_risk_informational_request"]
    assert low_risk["expected_classification"] == "allowed_non_executable_proposed"
    assert low_risk["risk_tier"] == "low"
    assert low_risk["approval_state"] == "proposed"
    assert low_risk["blocked_reason_required"] is False


def test_side_effect_categories_require_approval_or_blocked_status() -> None:
    rows = {
        row["category"]: row for row in _load_json(PHASE_FIXTURE_PATH)["validation_matrix"]
    }
    for category in {
        "shell_command_request",
        "browser_network_request",
        "file_mutation_request",
        "robotics_physical_world_request",
    }:
        row = rows[category]
        assert row["expected_classification"] == "approval_required_non_executable"
        assert row["approval_state"] == "approval_required"
        assert row["blocked_reason_required"] is True


def test_bypass_empty_malformed_and_replay_categories_are_blocked_or_rejected() -> None:
    rows = {
        row["category"]: row for row in _load_json(PHASE_FIXTURE_PATH)["validation_matrix"]
    }
    assert rows["admin_trusted_phil_bypass_attempt"]["approval_state"] == "blocked"
    assert rows["empty_request"]["approval_state"] == "rejected"
    assert rows["malformed_request"]["approval_state"] == "rejected"
    assert rows["replayed_stale_request"]["approval_state"] == "blocked"
    assert rows["ambiguous_request"]["approval_state"] == "approval_required"


def test_matrix_rules_do_not_approve_runtime_classifier_or_enforcement() -> None:
    rules = _load_json(PHASE_FIXTURE_PATH)["matrix_rules"]
    assert rules["all_outputs_non_executable"] is True
    assert rules["all_side_effects_blocked"] is True
    assert rules["approval_enforcement_implemented"] is False
    assert rules["runtime_classifier_implemented"] is False
    assert rules["operator_admin_phil_trusted_wording_bypasses_approval"] is False


def test_blocked_scope_preserves_runtime_boundaries() -> None:
    blocked = _load_json(PHASE_FIXTURE_PATH)["blocked_scope"]
    assert all(blocked.values())
    assert blocked["runtime_bridge_implementation"] is True
    assert blocked["files_under_lima"] is True
    assert blocked["tests_support_changes"] is True
    assert blocked["approval_enforcement"] is True
    assert blocked["execution"] is True
    assert blocked["physical_world_action"] is True


def test_ready_only_for_phase_five_ten_closeout() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["ready_for"] == [
        "phase_5_10_docs_tests_fixtures_only_implementation_gate_closeout_review"
    ]
    assert "runtime_bridge_implementation" in fixture["not_ready_for"]
    assert "phase_5_4_helper_runtime_reuse" in fixture["not_ready_for"]


def test_boundary_results_show_no_runtime_or_helper_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["runtime_behavior_added"] is False
    assert boundary["files_under_lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["helper_behavior_changed"] is False
    assert boundary["runtime_bridge_added"] is False


def test_no_phase_five_nine_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_5_9*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_5_9*"))
