"""Static checks for Phase 5.3 bridge harness readiness review."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_5_3_TEST_ONLY_BRIDGE_HARNESS_READINESS_REVIEW.md"
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_5_3_test_only_bridge_harness_readiness_review.json"
)
PHASE_5_2_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_5_2_test_only_bridge_harness_proposal.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_fixture_is_valid_phase_five_three_readiness_review() -> None:
    fixture = _load_json(FIXTURE_PATH)
    assert fixture["phase"] == "5.3"
    assert fixture["status"] == "non_runtime_test_only_bridge_harness_readiness_review"
    assert fixture["non_runtime"] is True
    assert fixture["docs_tests_fixtures_only"] is True


def test_doc_exists_and_stops_at_implementation_gate() -> None:
    assert PHASE_DOC_PATH.exists()
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "does not implement the harness" in phase_doc
    assert "ready for an implementation gate" in phase_doc
    assert "not ready for implementation without explicit operator approval" in phase_doc
    assert "Stop at the implementation gate" in phase_doc


def test_phase_five_two_source_is_recorded() -> None:
    fixture = _load_json(FIXTURE_PATH)
    assert fixture["source_phase"] == "5.2"
    assert fixture["source_tag"] == "phase-5.2-test-only-bridge-harness-proposal"
    assert fixture["source_merge_commit"] == "cf4bfb06c7f5372927531582983cb10ef5676b2d"


def test_phase_five_two_proposal_remains_proposal_only() -> None:
    fixture = _load_json(PHASE_5_2_FIXTURE_PATH)
    assert fixture["phase"] == "5.2"
    assert fixture["proposal_is"]["harness_proposal_only"] is True
    assert fixture["proposal_is_not"]["test_only_bridge_code"] is True
    assert fixture["boundary_results"]["test_only_bridge_code_added"] is False
    assert fixture["boundary_results"]["intentenvelope_created"] is False


def test_review_is_metadata_only_and_not_implementation() -> None:
    fixture = _load_json(FIXTURE_PATH)
    assert all(fixture["review_is"].values())
    assert all(fixture["review_is_not"].values())
    assert fixture["review_is"]["implementation_gate_review"] is True
    assert fixture["review_is_not"]["test_only_bridge_code"] is True
    assert fixture["review_is_not"]["intentenvelope_created"] is True


def test_findings_preserve_non_runtime_boundary() -> None:
    findings = _load_json(FIXTURE_PATH)["findings"]
    assert all(findings.values())
    assert findings["phase_5_2_remains_proposal_only"] is True
    assert findings["future_harness_is_synthetic_fixture_only"] is True
    assert findings["operator_intent_is_not_automatic_permission"] is True
    assert findings["guardian_decision_remains_required_before_consequential_behavior"] is True


def test_implementation_gate_requires_explicit_operator_approval() -> None:
    gate = _load_json(FIXTURE_PATH)["implementation_gate"]
    assert all(gate.values()) is False
    assert gate["gate_reached"] is True
    assert gate["implementation_preapproved"] is False
    assert gate["requires_explicit_operator_approval"] is True
    assert gate["future_phase_must_define_allowed_write_scope"] is True
    assert gate["future_phase_must_define_blocked_behavior_tests"] is True


def test_ready_for_is_limited_to_operator_decision_or_review() -> None:
    assert set(_load_json(FIXTURE_PATH)["ready_for"]) == {
        "explicit_operator_test_only_bridge_harness_implementation_scope_decision",
        "further_non_runtime_review",
    }


def test_not_ready_for_blocks_unapproved_implementation_and_live_paths() -> None:
    not_ready_for = set(_load_json(FIXTURE_PATH)["not_ready_for"])
    assert "test_only_bridge_harness_implementation_without_explicit_operator_approval" in not_ready_for
    assert "humaninput_to_intentenvelope_runtime_implementation" in not_ready_for
    assert "runtime_wiring" in not_ready_for
    assert "real_intentcompiler" in not_ready_for
    assert "real_guardiandecision" in not_ready_for
    assert "approval_enforcement" in not_ready_for
    assert "execution" in not_ready_for
    assert "audit_persistence" in not_ready_for
    assert "physical_world_action" in not_ready_for


def test_boundary_results_show_no_runtime_or_blocked_behavior() -> None:
    boundary = _load_json(FIXTURE_PATH)["boundary_results"]
    assert all(value is False for value in boundary.values())


def test_no_phase_five_three_runtime_bridge_or_lima_files_exist() -> None:
    forbidden_paths = [
        REPO_ROOT / "lima" / "intent_compiler.py",
        REPO_ROOT / "lima" / "humaninput_to_intentenvelope.py",
        REPO_ROOT / "tests" / "support" / "humaninput_to_intentenvelope_bridge.py",
        REPO_ROOT / "tests" / "helpers" / "humaninput_to_intentenvelope_bridge.py",
    ]
    assert not any(path.exists() for path in forbidden_paths)
