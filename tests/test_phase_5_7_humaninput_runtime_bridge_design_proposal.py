"""Static checks for Phase 5.7 HumanInput runtime bridge design proposal."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_5_7_HUMANINPUT_RUNTIME_BRIDGE_DESIGN_PROPOSAL.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_5_7_humaninput_runtime_bridge_design_proposal.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_fixture_declares_design_proposal_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "5.7"
    assert fixture["status"] == "humaninput_runtime_bridge_design_proposal"
    assert fixture["non_runtime"] is True
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["design_proposal_only"] is True


def test_doc_says_no_runtime_bridge_or_live_adapter_is_implemented() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "does not implement a runtime bridge" in phase_doc
    assert "does not add live adapter code" in phase_doc
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc


def test_future_bridge_design_keeps_candidates_non_executable() -> None:
    design = _load_json(PHASE_FIXTURE_PATH)["future_bridge_design"]
    assert design["runtime_implementation_approved"] is False
    assert design["live_adapter_approved"] is False
    assert design["humaninput_is_intent_context_not_execution_permission"] is True
    assert design["candidate_executable_default"] is False
    assert design["candidate_execution_allowed_default"] is False
    assert design["candidate_side_effects_allowed_default"] is False


def test_allowed_and_rejected_inputs_are_explicit() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert "approved_runtime_humaninput_boundary_record" in fixture["allowed_inputs"]
    assert "source_shell_channel_room_actor_session_metadata" in fixture["allowed_inputs"]
    assert "missing_input" in fixture["rejected_inputs"]
    assert "malformed_input" in fixture["rejected_inputs"]
    assert "replayed_input" in fixture["rejected_inputs"]
    assert "approval_claimed_by_operator_admin_phil_trusted_wording" in fixture["rejected_inputs"]


def test_candidate_required_fields_include_safety_metadata() -> None:
    required_fields = set(_load_json(PHASE_FIXTURE_PATH)["candidate_required_fields"])
    assert {
        "source",
        "source_channel",
        "operator_intent",
        "raw_text",
        "normalized_request",
        "requested_action",
        "risk_tier",
        "approval_state",
        "blocked_reason",
        "provenance",
        "executable",
        "execution_allowed",
        "side_effects_allowed",
    } <= required_fields


def test_trust_autonomy_and_operator_words_do_not_bypass_guardian_review() -> None:
    rules = _load_json(PHASE_FIXTURE_PATH)["trust_and_autonomy_rules"]
    assert rules["operator_intent_may_raise_priority"] is True
    assert rules["operator_intent_bypasses_guardian_review"] is False
    assert rules["trust_reference_enforced_by_phase_5_7"] is False
    assert rules["autonomy_reference_enforced_by_phase_5_7"] is False
    assert rules["operator_admin_phil_trusted_wording_bypasses_approval"] is False


def test_blocked_scope_preserves_runtime_boundaries() -> None:
    blocked = _load_json(PHASE_FIXTURE_PATH)["blocked_scope"]
    assert all(blocked.values())
    assert blocked["runtime_bridge_implementation"] is True
    assert blocked["live_adapter_code"] is True
    assert blocked["tests_support_changes"] is True
    assert blocked["files_under_lima"] is True
    assert blocked["approval_enforcement"] is True
    assert blocked["execution"] is True
    assert blocked["physical_world_action"] is True


def test_ready_only_for_phase_five_eight_threat_model() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["ready_for"] == ["phase_5_8_docs_tests_fixtures_only_threat_model"]
    assert "runtime_bridge_implementation" in fixture["not_ready_for"]
    assert "phase_5_4_helper_runtime_reuse" in fixture["not_ready_for"]


def test_boundary_results_show_no_runtime_or_helper_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["runtime_behavior_added"] is False
    assert boundary["files_under_lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["helper_behavior_changed"] is False
    assert boundary["new_helper_implementation_added"] is False
    assert boundary["runtime_bridge_added"] is False


def test_no_phase_five_seven_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_5_7*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_5_7*"))
