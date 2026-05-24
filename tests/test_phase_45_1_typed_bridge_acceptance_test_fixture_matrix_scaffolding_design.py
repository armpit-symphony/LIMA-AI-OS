"""Phase 45.1 typed bridge acceptance-test fixture matrix/scaffolding design tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_45_1_TYPED_BRIDGE_ACCEPTANCE_TEST_FIXTURE_MATRIX_SCAFFOLDING_DESIGN.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_45_1_typed_bridge_acceptance_test_fixture_matrix_scaffolding_design.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_45_1_opens_no_code_fixture_matrix_design_lane() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "45.1"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["fixture_matrix_design_only"] is True
    assert fixture["runtime_test_harness_created"] is False
    assert fixture["phase_45_0_anchor"] == "f15e771436d0159a7be701feea044ad86e921c7e"
    assert fixture["phase_45_0_tag"] == "phase-45.0-typed-bridge-acceptance-test-design"


def test_phase_45_1_matrix_chain_and_columns_are_defined() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["matrix_chain_under_test"] == [
        "source_request_metadata",
        "typed_intentenvelope_candidate_metadata",
        "guardian_request_metadata",
        "future_guardian_decision_metadata",
        "still_no_execution",
    ]
    assert fixture["matrix_columns"] == [
        "matrix_row_id",
        "test_family",
        "input_profile",
        "expected_bridge_state",
        "expected_guardian_decision_state",
        "expected_blocked_claims",
        "required_invariant_flags",
    ]


def test_phase_45_1_matrix_rows_cover_positive_and_fail_closed_categories() -> None:
    rows = set(_load_json(PHASE_FIXTURE_PATH)["matrix_rows"])
    assert "source_request_shape_positive_row" in rows
    assert "typed_intent_shape_positive_row" in rows
    assert "guardian_request_shape_positive_row" in rows
    assert "guardian_decision_metadata_boundary_row" in rows
    assert "malicious_approval_bypass_fail_closed_row" in rows
    assert "forged_guardian_decision_fail_closed_row" in rows
    assert "missing_identity_lineage_fail_closed_row" in rows
    assert "background_dispatch_fail_closed_row" in rows
    assert "adapter_external_call_fail_closed_row" in rows
    assert "model_tool_driver_call_fail_closed_row" in rows
    assert "robotics_physical_world_fail_closed_row" in rows
    assert "runtime_support_boundary_row" in rows


def test_phase_45_1_expected_state_categories_are_non_executing() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["expected_bridge_states"] == ["needs_review", "blocked"]
    assert fixture["expected_guardian_decision_states"] == ["absent", "pending", "blocked"]
    blocked_claim_categories = set(fixture["required_blocked_claim_categories"])
    assert "approval_bypass_claim" in blocked_claim_categories
    assert "guardian_decision_authority_claim" in blocked_claim_categories
    assert "missing_identity_lineage_claim" in blocked_claim_categories
    assert "background_dispatch_claim" in blocked_claim_categories
    assert "adapter_external_call_claim" in blocked_claim_categories
    assert "model_tool_driver_call_claim" in blocked_claim_categories
    assert "robotics_physical_world_claim" in blocked_claim_categories


def test_phase_45_1_required_flags_keep_runtime_and_harness_inactive() -> None:
    flags = _load_json(PHASE_FIXTURE_PATH)["required_invariant_flags"]
    for key in ("non_authoritative", "safe_by_default", "local_only", "deterministic"):
        assert flags[key] is True
    for key in (
        "execution_allowed",
        "dispatch_allowed",
        "persistence_allowed",
        "approval_granted",
        "external_calls_allowed",
        "model_calls_allowed",
        "tool_calls_allowed",
        "driver_calls_allowed",
        "adapter_calls_allowed",
        "robotics_allowed",
        "physical_world_allowed",
        "guardian_decision_created",
        "runtime_test_harness_active",
    ):
        assert flags[key] is False


def test_phase_45_1_blocks_runtime_expansion_and_recommends_no_implementation() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    blocked = set(fixture["blocked_scope"])
    assert "runtime_implementation" in blocked
    assert "lima_changes" in blocked
    assert "tests_support_changes" in blocked
    assert "runtime_test_harness_creation" in blocked
    assert "sparkbot_wiring" in blocked
    assert "arc_bot_implementation" in blocked
    assert "humaninput_bridge_behavior" in blocked
    assert "real_intentcompiler_behavior" in blocked
    assert "real_guardian_request_runtime_behavior" in blocked
    assert "guardian_decision_creation" in blocked
    assert "model_tool_driver_calls" in blocked
    assert "robotics_hardware_control_physical_world_behavior" in blocked
    assert (
        "background_workers_queues_daemons_subprocesses_threads_database_writes_hidden_side_effects"
        in blocked
    )
    assert fixture["remaining_gaps"] == []
    assert fixture["runtime_gap_found"] is False
    assert fixture["runtime_change_needed"] is False
    assert fixture["lima_change_needed"] is False
    assert fixture["tests_support_change_needed"] is False
    assert fixture["next_runtime_implementation_recommended"] is False


def test_phase_45_1_doc_declares_design_only_and_no_harness_behavior() -> None:
    text = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "docs/tests/fixtures-only no-code acceptance-test fixture matrix and scaffolding design" in text
    assert "does not create a runtime test harness" in text
    assert "Phase 45.1 remains acceptance-test fixture matrix/scaffolding design only." in text
    assert "Runtime implementation remains blocked." in text


def test_phase_45_1_stays_out_of_runtime_and_tests_support() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["runtime_behavior_changed"] is False
    assert not list((REPO_ROOT / "lima").rglob("*phase_45_1*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_45_1*"))
