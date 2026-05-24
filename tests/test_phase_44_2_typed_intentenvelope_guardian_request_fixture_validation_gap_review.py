"""Phase 44.2 typed bridge fixture validation gap review tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_44_1_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_44_1_typed_intentenvelope_guardian_request_fixtures.json"
)
PHASE_44_2_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_44_2_typed_intentenvelope_guardian_request_fixture_validation_gap_review.json"
)
PHASE_44_2_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_44_2_TYPED_INTENTENVELOPE_GUARDIAN_REQUEST_FIXTURE_VALIDATION_GAP_REVIEW.md"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_44_2_is_docs_tests_fixtures_only_validation_review() -> None:
    fixture = _load_json(PHASE_44_2_FIXTURE_PATH)
    assert fixture["phase"] == "44.2"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["fixture_validation_only"] is True
    assert fixture["phase_44_1_anchor"] == "a3fb607aa092afea06333de6ac5ca9b09e36e24e"
    assert fixture["phase_44_1_tag"] == "phase-44.1-typed-intentenvelope-guardian-request-fixtures"


def test_phase_44_2_validates_bridge_chain_and_case_coverage() -> None:
    fixture_44_2 = _load_json(PHASE_44_2_FIXTURE_PATH)
    fixture_44_1 = _load_json(PHASE_44_1_FIXTURE_PATH)

    assert fixture_44_2["validated_bridge_chain"] == [
        "source_request_metadata",
        "typed_intentenvelope_candidate_metadata",
        "guardian_request_metadata",
        "future_guardian_decision_metadata_only",
        "no_execution_path",
    ]

    phase_44_1_case_ids = {case["id"] for case in fixture_44_1["cases"]}
    phase_44_2_validated_case_ids = set(fixture_44_2["validated_case_ids"])
    assert phase_44_2_validated_case_ids == phase_44_1_case_ids
    assert fixture_44_2["reviewed_guardian_decision_states"] == [
        "absent",
        "pending",
        "blocked",
    ]


def test_phase_44_2_finds_no_runtime_gap_and_no_runtime_change_needed() -> None:
    fixture = _load_json(PHASE_44_2_FIXTURE_PATH)
    assert fixture["remaining_gaps"] == []
    assert fixture["runtime_gap_found"] is False
    assert fixture["runtime_change_needed"] is False
    assert fixture["lima_change_needed"] is False
    assert fixture["tests_support_change_needed"] is False
    assert fixture["next_runtime_implementation_recommended"] is False


def test_phase_44_2_records_expected_safety_findings() -> None:
    findings = _load_json(PHASE_44_2_FIXTURE_PATH)["findings"]
    assert findings["bridge_shape_coverage_adequate"] is True
    assert findings["guardian_request_non_authoritative"] is True
    assert findings["guardian_request_not_guardian_decision"] is True
    assert findings["guardian_decision_state_metadata_only"] is True
    assert findings["approval_remains_not_granted"] is True
    assert findings["execution_dispatch_persistence_paths_absent"] is True
    assert findings["model_tool_driver_paths_absent"] is True
    assert findings["adapter_external_call_paths_absent"] is True
    assert findings["robotics_physical_world_paths_absent"] is True
    assert findings["malicious_and_bypass_claims_fail_closed"] is True


def test_phase_44_2_recommends_archive_closeout_and_preserves_boundaries() -> None:
    fixture = _load_json(PHASE_44_2_FIXTURE_PATH)
    assert fixture["phase_44_3_recommended"] is True
    assert fixture["phase_44_3_lane"] == "docs_tests_fixtures_only_archive_closeout"

    blocked = set(fixture["blocked_scope"])
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


def test_phase_44_2_doc_records_no_runtime_gap_and_stop_point() -> None:
    text = PHASE_44_2_DOC_PATH.read_text(encoding="utf-8")
    assert "No concrete runtime gap was found." in text
    assert "Guardian request metadata remains request metadata only" in text
    assert "Stop at review for Phase 44.2." in text


def test_phase_44_2_stays_out_of_runtime_and_tests_support() -> None:
    fixture = _load_json(PHASE_44_2_FIXTURE_PATH)
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["runtime_behavior_changed"] is False
    assert not list((REPO_ROOT / "lima").rglob("*phase_44_2*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_44_2*"))
