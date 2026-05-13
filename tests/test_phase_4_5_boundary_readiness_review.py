"""Static checks for Phase 4.5 boundary readiness review."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
REVIEW_DOC_PATH = REPO_ROOT / "docs" / "PHASE_4_5_BOUNDARY_READINESS_REVIEW.md"
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_4_5_boundary_readiness_review.json"
)

REQUIRED_READY_INPUTS = {
    "selected_boundary_identity",
    "synthetic_text_fixture_shape",
    "synthetic_voice_transcript_fixture_shape",
    "reference_only_shell_channel_room_metadata",
    "reference_only_actor_session_metadata",
    "passive_trust_autonomy_references",
    "transcript_confidence_metadata",
    "privacy_redaction_retention_visibility_metadata",
    "lineage_seed_references",
    "handoff_requirements_toward_intentenvelope_and_guardiandecision",
    "inert_capability_flags",
    "all_can_flags_false_hardening_rule",
    "authority_and_live_integration_identifiers_forbidden_rule",
}

REQUIRED_REVIEWED_SOURCES = {
    "phase_4_1_sparkbot_runtime_reference_refresh",
    "phase_4_2_runtime_boundary_candidate_selection",
    "phase_4_3_boundary_extraction_safety_gate",
    "phase_4_4_boundary_fixture_contract_extension",
    "phase_4_4_fixture_contract_hardening",
}

REQUIRED_BLOCKED = {
    "runtime_behavior",
    "live_adapter_code",
    "sparkbot_imports_route_imports_wiring_or_code_copy",
    "production_sparkbot_integration",
    "live_auth_session_trust_lookup",
    "natural_language_parsing_into_action",
    "real_intentcompiler",
    "real_guardiandecision",
    "model_calls",
    "tool_exposure_or_execution",
    "terminal_or_pty_behavior",
    "robotics_behavior",
    "approval_enforcement",
    "policy_enforcement",
    "adaptive_trust_enforcement",
    "audit_persistence",
    "lima_ai_office_implementation",
    "arc_bot_implementation",
    "custom_bot_implementation",
    "robot_drone_iot_or_physical_world_control",
}

REQUIRED_NO_GO = {
    "runtime_behavior",
    "executable_pipeline",
    "test_only_composition_harness",
    "live_adapter_code",
    "sparkbot_import_wiring_route_import_or_code_copy",
    "model_calls",
    "tool_execution",
    "terminal_or_pty_behavior",
    "robotics_behavior",
    "live_auth_session_trust_lookup",
    "real_intentcompiler",
    "real_guardiandecision",
    "approval_enforcement",
    "policy_enforcement",
    "adaptive_trust_enforcement",
    "audit_persistence",
    "lima_ai_office_implementation",
    "arc_bot_implementation",
    "custom_bot_implementation",
    "robot_control",
    "drone_control",
    "iot_control",
    "physical_world_action",
    "production_shell_implementation",
}

FORBIDDEN_PRIVATE_OR_OPERATIONAL_RE = re.compile(
    r"("
    r"api[_-]?key|password|credential|private[_-]?key|bearer\s+[a-z0-9._-]+|"
    r"secret=|token=|approval[_ -]?token|"
    r"https?://|www\.|\b(?:[a-z0-9-]+\.)+(?:com|net|org|io|dev|cloud|local)\b|"
    r"runtime[_ -]?config|deploy[_ -]?config|model prompt|tool call|"
    r"\b(?:python|python3|git|curl|wget|powershell|cmd|bash|sh|npm|uv|pytest)\s+"
    r")",
    re.IGNORECASE,
)


def _load_fixture() -> dict[str, Any]:
    assert FIXTURE_PATH.exists()
    with FIXTURE_PATH.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def _all_strings(value: Any) -> list[str]:
    strings: list[str] = []
    if isinstance(value, str):
        strings.append(value)
    elif isinstance(value, list):
        for item in value:
            strings.extend(_all_strings(item))
    elif isinstance(value, dict):
        for item in value.values():
            strings.extend(_all_strings(item))
    return strings


def test_phase_four_five_fixture_is_readiness_review_only() -> None:
    fixture = _load_fixture()
    assert fixture["phase"] == "4.5"
    assert fixture["status"] == "boundary_readiness_review_only"
    assert fixture["non_runtime"] is True


def test_review_doc_exists_and_blocks_implementation() -> None:
    assert REVIEW_DOC_PATH.exists()
    review_doc = REVIEW_DOC_PATH.read_text(encoding="utf-8")
    assert "Phase 4.5 reviews the selected HumanInput intake boundary" in review_doc
    assert "It is readiness review only" in review_doc
    assert "NO-GO for runtime extraction implementation" in review_doc


def test_phase_four_four_hardening_source_is_recorded() -> None:
    fixture = _load_fixture()
    assert fixture["source_phase"] == "4.4"
    assert fixture["source_tag"] == "phase-4.4-boundary-fixture-contract-hardening"
    assert fixture["source_merge_commit"] == "db02a25"
    assert fixture["reviewed_boundary"] == "humaninput_intake_boundary_for_chat_and_voice"


def test_review_covers_phase_four_reference_candidate_gate_fixture_and_hardening() -> None:
    assert REQUIRED_REVIEWED_SOURCES <= set(_load_fixture()["reviewed_sources"])


def test_readiness_result_is_conditional_and_non_runtime() -> None:
    result = _load_fixture()["readiness_result"]
    assert result["ready_for_future_explicitly_approved_narrow_nonproduction_proposal"] is True
    assert result["ready_for_runtime_extraction_implementation"] is False
    assert result["ready_for_production_sparkbot_integration"] is False
    assert result["ready_for_live_adapter_code"] is False
    assert result["ready_for_model_calls"] is False
    assert result["ready_for_tool_execution"] is False
    assert result["ready_for_terminal_pty_behavior"] is False
    assert result["ready_for_robotics_behavior"] is False
    assert result["ready_for_approval_enforcement_execution_or_audit_persistence"] is False
    assert result["ready_for_physical_world_action"] is False


def test_ready_review_inputs_include_fixture_and_hardening_evidence() -> None:
    assert REQUIRED_READY_INPUTS <= set(_load_fixture()["ready_review_inputs"])


def test_still_blocked_keeps_runtime_and_product_surfaces_closed() -> None:
    assert REQUIRED_BLOCKED <= set(_load_fixture()["still_blocked"])


def test_future_proposal_conditions_require_explicit_approval_and_boundaries() -> None:
    conditions = set(_load_fixture()["future_proposal_conditions"])
    assert "explicit_approval_before_work_starts" in conditions
    assert "humaninput_remains_non_authorizing_input" in conditions
    assert "intentenvelope_remains_next_semantic_boundary" in conditions
    assert "guardiandecision_required_before_consequential_behavior" in conditions
    assert "import_boundary_tests_before_any_adapter_code" in conditions
    assert "terminal_robotics_and_physical_world_action_out_of_scope" in conditions


def test_decision_is_no_go_for_runtime_sparkbot_product_and_physical_world() -> None:
    decision = _load_fixture()["decision"]
    assert decision["conditional_go_for_future_explicitly_approved_narrow_nonproduction_humaninput_intake_proposal"] is True
    assert decision["no_go_for_runtime_extraction_implementation"] is True
    assert decision["no_go_for_sparkbot_integration"] is True
    assert decision["no_go_for_product_shell_implementation"] is True
    assert decision["no_go_for_physical_world_action"] is True


def test_phase_four_five_no_go_blocks_all_hard_boundaries() -> None:
    assert REQUIRED_NO_GO <= set(_load_fixture()["phase_4_5_no_go"])


def test_ready_for_requires_explicit_operator_approval() -> None:
    fixture = _load_fixture()
    assert fixture["ready_for"] == [
        "explicit_operator_approval_for_next_narrow_nonproduction_phase"
    ]
    assert "runtime_extraction_implementation" in fixture["not_ready_for"]
    assert "sparkbot_runtime_integration" in fixture["not_ready_for"]
    assert "terminal_pty_execution" in fixture["not_ready_for"]
    assert "physical_world_action" in fixture["not_ready_for"]


def test_boundary_results_show_no_behavior_or_live_integration() -> None:
    boundary = _load_fixture()["boundary_results"]
    assert boundary["runtime_behavior_added"] is False
    assert boundary["blocked_behavior_added"] is False
    assert boundary["files_under_lima_modified"] is False
    assert boundary["sparkbot_files_modified"] is False
    assert boundary["sparkbot_imported"] is False
    assert boundary["sparkbot_wired"] is False
    assert boundary["sparkbot_code_copied"] is False
    assert boundary["live_adapter_code_added"] is False
    assert boundary["model_calls_added"] is False
    assert boundary["tool_execution_added"] is False
    assert boundary["terminal_behavior_added"] is False
    assert boundary["robotics_behavior_added"] is False
    assert boundary["live_auth_session_trust_lookup_added"] is False
    assert boundary["real_intentcompiler_added"] is False
    assert boundary["real_guardiandecision_added"] is False
    assert boundary["approval_enforcement_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False


def test_fixture_has_no_private_operational_data() -> None:
    for string_value in _all_strings(_load_fixture()):
        assert not FORBIDDEN_PRIVATE_OR_OPERATIONAL_RE.search(string_value), string_value


def test_no_phase_four_five_runtime_modules_or_live_adapters_were_added() -> None:
    forbidden_paths = [
        REPO_ROOT / "lima" / "runtime_extraction.py",
        REPO_ROOT / "lima" / "kernel_pipeline.py",
        REPO_ROOT / "lima" / "adapters" / "sparkbot_runtime.py",
        REPO_ROOT / "lima" / "adapters" / "sparkbot_humaninput_live.py",
        REPO_ROOT / "lima" / "adapters" / "sparkbot_chat_voice.py",
        REPO_ROOT / "lima" / "adapters" / "sparkbot_voice_live.py",
        REPO_ROOT / "tests" / "helpers" / "runtime_extraction_harness.py",
    ]
    assert not any(path.exists() for path in forbidden_paths)
