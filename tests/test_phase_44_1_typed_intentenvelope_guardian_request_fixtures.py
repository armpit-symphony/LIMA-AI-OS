"""Phase 44.1 typed IntentEnvelope Guardian request fixture corpus tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_44_1_TYPED_INTENTENVELOPE_GUARDIAN_REQUEST_FIXTURES.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_44_1_typed_intentenvelope_guardian_request_fixtures.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_44_1_fixture_corpus_is_docs_tests_fixtures_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "44.1"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["fixture_data_only"] is True
    assert fixture["phase_44_0_anchor"] == "f3b056af9b41b70e874d993fb0352bb49e4043c5"
    assert fixture["phase_44_0_tag"] == "phase-44.0-typed-intentenvelope-guardian-request-bridge-design"
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["runtime_behavior_changed"] is False


def test_phase_44_1_includes_required_bridge_cases() -> None:
    fixture_ids = {case["id"] for case in _load_json(PHASE_FIXTURE_PATH)["cases"]}
    assert fixture_ids == {
        "safe_draft_only_natural_language_request",
        "ambiguous_request_requires_clarification",
        "external_write_request_requires_guardian_review",
        "tool_pack_scope_request",
        "scheduled_background_request_without_dispatch",
        "physical_world_request_blocked_before_drivers",
        "emergency_stop_request_no_execution_path",
        "malicious_typed_intent_claiming_approval",
        "malicious_guardian_request_claiming_decision_authority",
        "missing_actor_tenant_or_lineage_metadata",
    }


def test_phase_44_1_cases_carry_required_safe_control_flags() -> None:
    required_flags = _load_json(PHASE_FIXTURE_PATH)["required_case_flags"]
    for case in _load_json(PHASE_FIXTURE_PATH)["cases"]:
        assert case["control_flags"] == required_flags
        assert case["guardian_decision_state"] in {"absent", "pending", "blocked"}
        assert case["expected_bridge_state"] in {"needs_review", "blocked"}
        assert isinstance(case["expected_blocked_claims"], list)
        assert isinstance(case["source_request_metadata"], dict)
        assert isinstance(case["intentenvelope_candidate_metadata"], dict)
        assert isinstance(case["guardian_request_metadata"], dict)


def test_phase_44_1_risky_or_malicious_cases_fail_closed() -> None:
    cases = {case["id"]: case for case in _load_json(PHASE_FIXTURE_PATH)["cases"]}
    blocked_ids = {
        "external_write_request_requires_guardian_review",
        "scheduled_background_request_without_dispatch",
        "physical_world_request_blocked_before_drivers",
        "emergency_stop_request_no_execution_path",
        "malicious_typed_intent_claiming_approval",
        "malicious_guardian_request_claiming_decision_authority",
        "missing_actor_tenant_or_lineage_metadata",
    }
    for case_id in blocked_ids:
        assert cases[case_id]["expected_bridge_state"] == "blocked"
        assert cases[case_id]["expected_blocked_claims"]


def test_phase_44_1_safe_or_review_cases_never_claim_authority() -> None:
    cases = {case["id"]: case for case in _load_json(PHASE_FIXTURE_PATH)["cases"]}
    for case_id in {
        "safe_draft_only_natural_language_request",
        "ambiguous_request_requires_clarification",
        "tool_pack_scope_request",
    }:
        assert cases[case_id]["expected_bridge_state"] == "needs_review"
        flags = cases[case_id]["control_flags"]
        assert flags["guardian_decision_created"] is False
        assert flags["approval_granted"] is False
        assert flags["execution_allowed"] is False
        assert flags["dispatch_allowed"] is False
        assert flags["persistence_allowed"] is False
        assert flags["external_calls_allowed"] is False
        assert flags["model_calls_allowed"] is False
        assert flags["tool_calls_allowed"] is False
        assert flags["driver_calls_allowed"] is False
        assert flags["robotics_allowed"] is False
        assert flags["physical_world_allowed"] is False


def test_phase_44_1_blocks_runtime_and_support_scope() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
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


def test_phase_44_1_documented_as_inert_fixture_work() -> None:
    text = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "docs/tests/fixtures-only inert fixture data" in text
    assert "does not implement a bridge" in text
    assert "GuardianDecision creation" in text
    assert "Stop at review for Phase 44.1." in text


def test_phase_44_1_stays_out_of_runtime_and_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_44_1*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_44_1*"))
