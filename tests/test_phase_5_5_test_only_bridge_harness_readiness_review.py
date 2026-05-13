"""Static checks for Phase 5.5 bridge harness readiness review."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_5_5_TEST_ONLY_BRIDGE_HARNESS_READINESS_REVIEW.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_5_5_test_only_bridge_harness_readiness_review.json"
)
PHASE_5_4_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_5_4_test_only_humaninput_to_intentenvelope_bridge_harness_implementation.json"
)
PHASE_5_4_HELPER_PATH = (
    REPO_ROOT / "tests" / "support" / "test_only_humaninput_to_intentenvelope_bridge.py"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_fixture_declares_docs_tests_fixtures_only_readiness_review() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "5.5"
    assert fixture["status"] == "test_only_bridge_harness_readiness_review"
    assert fixture["non_runtime"] is True
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["readiness_review_only"] is True


def test_docs_identify_phase_five_four_helper_as_test_only() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "reviews the Phase 5.4 test-only" in phase_doc
    assert "docs/tests/fixtures only" in phase_doc
    assert "does not change helper behavior" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc


def test_docs_forbid_runtime_reuse_of_helper_classifier() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "must not be reused as runtime classifier logic" in phase_doc
    assert "Live/runtime HumanInput to IntentEnvelope implementation remains blocked" in phase_doc


def test_fixture_says_live_runtime_implementation_is_not_approved() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase_5_6_gate"]["live_runtime_implementation_approved"] is False
    assert "humaninput_to_intentenvelope_runtime_implementation" in fixture["not_ready_for"]
    assert "runtime_classifier_reuse" in fixture["not_ready_for"]


def test_fixture_says_phase_five_six_or_next_phase_is_gated() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    gate = fixture["phase_5_6_gate"]
    assert gate["gate_reached"] is True
    assert gate["phase_5_6_preapproved"] is False
    assert gate["requires_explicit_operator_scope_decision"] is True
    assert set(fixture["ready_for"]) == {
        "explicit_operator_phase_5_6_scope_decision",
        "further_docs_tests_fixtures_only_review",
    }


def test_fixture_repeats_no_lima_runtime_sparkbot_execution_boundaries() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["files_under_lima_modified"] is False
    assert boundary["runtime_behavior_added"] is False
    assert boundary["sparkbot_imported"] is False
    assert boundary["sparkbot_wired"] is False
    assert boundary["live_adapter_code_added"] is False
    assert boundary["approval_enforcement_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False


def test_phase_five_four_helper_still_exists_only_under_tests_support() -> None:
    assert PHASE_5_4_HELPER_PATH.exists()
    assert "tests/support" in PHASE_5_4_HELPER_PATH.as_posix()
    assert not (REPO_ROOT / "lima" / "test_only_humaninput_to_intentenvelope_bridge.py").exists()
    assert not (REPO_ROOT / "tests" / "helpers" / "test_only_humaninput_to_intentenvelope_bridge.py").exists()


def test_no_new_helper_implementation_files_are_added_for_phase_five_five() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    boundary = fixture["boundary_results"]
    assert boundary["tests_support_helper_modified"] is False
    assert boundary["new_helper_implementation_added"] is False
    assert not (REPO_ROOT / "tests" / "support" / "phase_5_5_bridge_helper.py").exists()
    assert not (REPO_ROOT / "tests" / "support" / "test_only_phase_5_5_bridge.py").exists()


def test_phase_five_four_helper_outputs_remain_non_executable_by_contract() -> None:
    phase_five_four = _load_json(PHASE_5_4_FIXTURE_PATH)
    assert phase_five_four["implementation_is"]["non_executable"] is True
    assert phase_five_four["implementation_is_not"]["live_runtime_bridge"] is True
    assert "executable" in phase_five_four["required_output_fields"]
    assert "execution_allowed" in phase_five_four["required_output_fields"]
    assert "side_effects_allowed" in phase_five_four["required_output_fields"]


def test_readiness_findings_preserve_candidate_semantics_and_operator_boundary() -> None:
    findings = _load_json(PHASE_FIXTURE_PATH)["review_findings"]
    assert findings["all_candidates_non_executable"] is True
    assert findings["execution_allowed_always_false"] is True
    assert findings["side_effects_allowed_always_false"] is True
    assert findings["risky_requests_require_approval_or_blocked"] is True
    assert findings["operator_admin_phil_trusted_wording_does_not_bypass_approval"] is True
    assert findings["provenance_required"] is True
    assert findings["blocked_reason_required"] is True


def test_no_intentcompiler_or_guardiandecision_runtime_behavior_changed() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    boundary = fixture["boundary_results"]
    assert boundary["real_intentcompiler_added"] is False
    assert boundary["real_guardiandecision_added"] is False
    assert "real_intentcompiler" in fixture["not_ready_for"]
    assert "real_guardiandecision" in fixture["not_ready_for"]
