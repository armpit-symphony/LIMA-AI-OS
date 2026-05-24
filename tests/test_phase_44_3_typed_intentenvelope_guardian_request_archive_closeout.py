"""Phase 44.3 typed IntentEnvelope Guardian request archive closeout tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_44_3_TYPED_INTENTENVELOPE_GUARDIAN_REQUEST_ARCHIVE_CLOSEOUT.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_44_3_typed_intentenvelope_guardian_request_archive_closeout.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_44_3_archives_phase_44_lane() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "44.3"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["typed_bridge_lane_archived"] is True
    assert fixture["phase_44_2_anchor"] == "cc81476c119389870df1328f0b98f0eece571276"
    assert fixture["phase_44_2_tag"] == "phase-44.2-typed-bridge-fixture-validation-gap-review"
    assert fixture["completed_phases"] == ["44.0", "44.1", "44.2", "44.3"]


def test_phase_44_3_records_closeout_findings() -> None:
    findings = _load_json(PHASE_FIXTURE_PATH)["archived_findings"]
    assert findings["phase_44_0_opened_no_code_bridge_design"] is True
    assert findings["phase_44_1_added_inert_fixture_corpus"] is True
    assert findings["phase_44_2_validated_fixture_coverage"] is True
    assert findings["phase_44_2_found_no_concrete_runtime_gap"] is True
    assert findings["guardian_request_non_authoritative"] is True
    assert findings["guardian_request_not_guardiandecision_authority"] is True
    assert findings["guardiandecision_state_metadata_only"] is True
    assert findings["no_execution_dispatch_persistence_path"] is True
    assert findings["no_model_tool_driver_call_path"] is True
    assert findings["no_adapter_external_call_path"] is True
    assert findings["no_robotics_physical_world_path"] is True


def test_phase_44_3_finds_no_runtime_gap_and_no_runtime_recommendation() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["remaining_gaps"] == []
    assert fixture["runtime_gap_found"] is False
    assert fixture["runtime_change_needed"] is False
    assert fixture["lima_change_needed"] is False
    assert fixture["tests_support_change_needed"] is False
    assert fixture["next_runtime_implementation_recommended"] is False
    assert fixture["recommended_next_direction"] == "stop_at_merge_tag_approval_gate_for_phase_44_stack"


def test_phase_44_3_blocks_runtime_expansion_scope() -> None:
    blocked = set(_load_json(PHASE_FIXTURE_PATH)["blocked_scope"])
    assert "runtime_implementation" in blocked
    assert "lima_changes" in blocked
    assert "tests_support_changes" in blocked
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


def test_phase_44_3_doc_records_archive_closeout_boundary() -> None:
    text = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "Phase 44.3 archives Phase 44 as a completed docs/tests/fixtures-only" in text
    assert "Phase 44.2 validated fixture coverage and found no concrete runtime gap." in text
    assert "No runtime implementation is needed for this closeout." in text
    assert "Stop at the merge/tag approval gate for the Phase 44 stack." in text


def test_phase_44_3_stays_out_of_runtime_and_tests_support() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["runtime_behavior_changed"] is False
    assert not list((REPO_ROOT / "lima").rglob("*phase_44_3*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_44_3*"))
