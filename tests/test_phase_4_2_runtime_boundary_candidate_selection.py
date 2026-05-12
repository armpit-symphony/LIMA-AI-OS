"""Static checks for Phase 4.2 runtime boundary candidate selection."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
SELECTION_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_4_2_RUNTIME_BOUNDARY_CANDIDATE_SELECTION.md"
)
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_4_2_runtime_boundary_candidate_selection.json"
)

REQUIRED_CANDIDATE_SCOPE = {
    "text_input_source_metadata",
    "voice_transcript_source_metadata",
    "shell_session_actor_reference_metadata",
    "channel_room_or_conversation_reference_metadata",
    "transcript_confidence_and_normalization_metadata",
    "privacy_redaction_reference_requirements_for_raw_user_content",
    "attachment_and_file_reference_metadata",
    "owner_autonomy_context_references",
    "downstream_handoff_requirements_to_intentenvelope_and_guardiandecision",
}

REQUIRED_SAFETY_GATE_REQUIREMENTS = {
    "no_sparkbot_imports_wiring_route_imports_or_code_copy",
    "no_runtime_behavior",
    "no_model_calls",
    "no_tool_execution",
    "no_terminal_pty_execution",
    "no_robotics_command_execution",
    "no_real_intentcompiler",
    "no_real_guardiandecision",
    "no_approval_enforcement",
    "no_policy_enforcement",
    "no_adaptive_trust_enforcement",
    "no_audit_persistence",
    "synthetic_or_redacted_fixture_material_only",
    "privacy_and_redaction_rules_for_raw_text_and_transcripts",
    "actor_session_trust_fields_are_references_not_live_lookup",
    "import_boundary_tests_prevent_sparkbot_runtime_dependencies",
    "proof_humaninput_intake_cannot_execute_or_approve",
}

REQUIRED_NO_GO = {
    "runtime_behavior",
    "executable_pipeline",
    "test_only_composition_harness",
    "sparkbot_import_wiring_route_import_or_code_copy",
    "model_calls",
    "tool_execution",
    "terminal_or_pty_execution",
    "robotics_command_execution",
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


def test_phase_four_two_fixture_is_selection_only() -> None:
    fixture = _load_fixture()
    assert fixture["phase"] == "4.2"
    assert fixture["status"] == "runtime_boundary_candidate_selection_only"
    assert fixture["non_runtime"] is True


def test_selection_doc_exists_and_blocks_extraction() -> None:
    assert SELECTION_DOC_PATH.exists()
    selection_doc = SELECTION_DOC_PATH.read_text(encoding="utf-8")
    assert "Phase 4.2 selects the first runtime boundary candidate" in selection_doc
    assert "It is selection work only" in selection_doc
    assert "NO-GO for runtime extraction implementation" in selection_doc


def test_phase_four_one_source_is_recorded() -> None:
    fixture = _load_fixture()
    assert fixture["source_phase"] == "4.1"
    assert fixture["source_tag"] == "phase-4.1-sparkbot-runtime-reference-refresh"
    assert fixture["source_merge_commit"] == "8fb9a09"


def test_selected_candidate_is_humaninput_intake_and_not_extraction() -> None:
    selected = _load_fixture()["selected_candidate"]
    assert selected["id"] == "humaninput_intake_boundary_for_chat_and_voice"
    assert selected["candidate_type"] == "non_executing_boundary_candidate"
    assert selected["next_gate"] == "phase_4_3_boundary_extraction_safety_gate"
    assert selected["selected_for_extraction_now"] is False
    assert selected["selected_for_safety_gate"] is True


def test_source_basis_uses_phase_four_one_findings() -> None:
    basis = set(_load_fixture()["source_basis"])
    assert "sparkbot_text_and_voice_converge_into_shared_reference_path" in basis
    assert "tool_aware_loop_is_too_coupled_to_extract_first" in basis
    assert "terminal_and_robotics_are_critical_risk_and_deferred" in basis
    assert "frontend_surfaces_are_shell_reference_not_kernel_code" in basis


def test_candidate_scope_stays_on_input_metadata_and_handoff_requirements() -> None:
    scope = set(_load_fixture()["candidate_scope"])
    assert REQUIRED_CANDIDATE_SCOPE <= scope


def test_candidate_invariants_prevent_hidden_execution_or_approval() -> None:
    invariants = _load_fixture()["candidate_invariants"]
    assert invariants["raw_language_cannot_execute"] is True
    assert invariants["humaninput_cannot_parse_action"] is True
    assert invariants["humaninput_cannot_select_tools"] is True
    assert invariants["humaninput_cannot_call_models"] is True
    assert invariants["humaninput_cannot_approve"] is True
    assert invariants["humaninput_cannot_enforce_policy"] is True
    assert invariants["humaninput_cannot_persist_audit"] is True
    assert invariants["humaninput_cannot_touch_terminal"] is True
    assert invariants["humaninput_cannot_touch_robotics"] is True
    assert invariants["humaninput_requires_later_intent_and_guardian_boundaries"] is True


def test_deferred_boundaries_keep_high_risk_surfaces_out_of_first_candidate() -> None:
    deferred = set(_load_fixture()["deferred_boundaries"])
    assert "model_harness_and_tool_aware_loop_extraction" in deferred
    assert "broad_tool_catalogue_dispatcher_extraction" in deferred
    assert "real_guardian_policy_or_enforcement_extraction" in deferred
    assert "terminal_pty_extraction" in deferred
    assert "robotics_command_execution" in deferred
    assert "production_sparkbot_adapter_wiring" in deferred
    assert "robot_drone_iot_or_physical_world_control" in deferred


def test_phase_four_three_safety_gate_requirements_are_explicit() -> None:
    requirements = set(_load_fixture()["phase_4_3_safety_gate_requirements"])
    assert REQUIRED_SAFETY_GATE_REQUIREMENTS <= requirements


def test_phase_four_two_no_go_blocks_runtime_product_and_physical_world() -> None:
    assert REQUIRED_NO_GO <= set(_load_fixture()["phase_4_2_no_go"])


def test_ready_for_only_allows_phase_four_three_safety_gate() -> None:
    fixture = _load_fixture()
    assert fixture["ready_for"] == ["phase_4_3_boundary_extraction_safety_gate"]
    assert "runtime_extraction_implementation" in fixture["not_ready_for"]
    assert "sparkbot_runtime_integration" in fixture["not_ready_for"]
    assert "terminal_pty_execution" in fixture["not_ready_for"]
    assert "physical_world_action" in fixture["not_ready_for"]


def test_boundary_results_show_no_behavior_or_sparkbot_movement() -> None:
    boundary = _load_fixture()["boundary_results"]
    assert boundary["runtime_behavior_added"] is False
    assert boundary["blocked_behavior_added"] is False
    assert boundary["files_under_lima_modified"] is False
    assert boundary["sparkbot_files_modified"] is False
    assert boundary["sparkbot_imported"] is False
    assert boundary["sparkbot_wired"] is False
    assert boundary["sparkbot_code_copied"] is False
    assert boundary["model_calls_added"] is False
    assert boundary["tool_execution_added"] is False
    assert boundary["terminal_execution_added"] is False
    assert boundary["robot_control_added"] is False
    assert boundary["physical_world_action_added"] is False


def test_fixture_has_no_private_operational_data() -> None:
    for string_value in _all_strings(_load_fixture()):
        assert not FORBIDDEN_PRIVATE_OR_OPERATIONAL_RE.search(string_value), string_value


def test_no_phase_four_two_runtime_modules_or_sparkbot_adapters_were_added() -> None:
    forbidden_paths = [
        REPO_ROOT / "lima" / "runtime_extraction.py",
        REPO_ROOT / "lima" / "kernel_pipeline.py",
        REPO_ROOT / "lima" / "adapters" / "sparkbot_runtime.py",
        REPO_ROOT / "lima" / "adapters" / "sparkbot_humaninput_live.py",
        REPO_ROOT / "lima" / "adapters" / "sparkbot_chat_voice.py",
        REPO_ROOT / "tests" / "helpers" / "runtime_extraction_harness.py",
    ]
    assert not any(path.exists() for path in forbidden_paths)
