"""Static checks for Phase 4.3 boundary extraction safety gate."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
SAFETY_GATE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_4_3_BOUNDARY_EXTRACTION_SAFETY_GATE.md"
)
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_4_3_boundary_extraction_safety_gate.json"
)

REQUIRED_ALLOWED_TOPICS = {
    "synthetic_input_identifiers",
    "input_kind_text_or_voice",
    "shell_reference_metadata",
    "channel_room_or_conversation_reference_metadata",
    "actor_and_session_reference_metadata",
    "passive_trust_context_reference_metadata",
    "redacted_content_references_or_summaries",
    "transcript_confidence_and_normalization_metadata",
    "attachment_file_references",
    "privacy_redaction_retention_visibility_classes",
    "owner_autonomy_context_references",
    "lineage_seed_references",
    "handoff_requirements_to_future_intentenvelope_and_guardiandecision",
}

REQUIRED_HARD_BLOCKERS = {
    "sparkbot_imports_wiring_route_imports_or_code_copy",
    "production_sparkbot_adapter_implementation",
    "real_auth_session_trust_lookup",
    "natural_language_parsing_into_action",
    "real_intentcompiler",
    "real_guardiandecision",
    "model_calls",
    "tool_exposure_or_execution",
    "terminal_pty_execution",
    "robotics_command_execution",
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


def test_phase_four_three_fixture_is_safety_gate_only() -> None:
    fixture = _load_fixture()
    assert fixture["phase"] == "4.3"
    assert fixture["status"] == "boundary_extraction_safety_gate_only"
    assert fixture["non_runtime"] is True


def test_safety_gate_doc_exists_and_blocks_extraction() -> None:
    assert SAFETY_GATE_DOC_PATH.exists()
    safety_gate_doc = SAFETY_GATE_DOC_PATH.read_text(encoding="utf-8")
    assert "Phase 4.3 defines the safety gate" in safety_gate_doc
    assert "It is a safety gate only" in safety_gate_doc
    assert "NO-GO for runtime extraction implementation" in safety_gate_doc


def test_phase_four_two_source_is_recorded() -> None:
    fixture = _load_fixture()
    assert fixture["source_phase"] == "4.2"
    assert fixture["source_tag"] == "phase-4.2-runtime-boundary-candidate-selection"
    assert fixture["source_merge_commit"] == "0149c0b"


def test_selected_candidate_remains_humaninput_intake() -> None:
    fixture = _load_fixture()
    assert fixture["selected_candidate"] == "humaninput_intake_boundary_for_chat_and_voice"
    classification = set(fixture["candidate_classification"])
    assert "non_executing_input_boundary" in classification
    assert "before_intentenvelope" in classification
    assert "before_guardiandecision" in classification
    assert "before_tool_exposure" in classification
    assert "before_execution" in classification


def test_allowed_phase_four_four_topics_are_metadata_only() -> None:
    topics = set(_load_fixture()["allowed_phase_4_4_fixture_contract_topics_if_approved"])
    assert REQUIRED_ALLOWED_TOPICS <= topics


def test_safety_requirements_block_hidden_runtime_behavior() -> None:
    requirements = _load_fixture()["safety_requirements"]
    assert requirements["humaninput_cannot_parse_action"] is True
    assert requirements["humaninput_cannot_call_models"] is True
    assert requirements["humaninput_cannot_select_or_execute_tools"] is True
    assert requirements["humaninput_cannot_approve_or_enforce_policy"] is True
    assert requirements["humaninput_cannot_write_terminal_input"] is True
    assert requirements["humaninput_cannot_call_robotics_or_physical_world_drivers"] is True
    assert requirements["humaninput_cannot_persist_audit"] is True
    assert requirements["humaninput_cannot_perform_live_auth_session_trust_lookup"] is True
    assert requirements["humaninput_cannot_import_or_wire_sparkbot"] is True
    assert requirements["fixtures_use_synthetic_redacted_or_referenced_content"] is True
    assert requirements["identity_trust_and_autonomy_fields_are_references_only"] is True
    assert requirements["next_boundary_remains_intentenvelope_or_intentcompiler"] is True
    assert requirements["consequential_behavior_waits_for_later_guardiandecision_gate"] is True


def test_required_phase_four_four_tests_cover_input_and_import_boundaries() -> None:
    required_tests = set(_load_fixture()["required_phase_4_4_tests_if_approved"])
    assert "fixture_shape_tests_for_text_and_voice_examples" in required_tests
    assert "input_records_have_no_execution_capability" in required_tests
    assert "no_sparkbot_modules_imported" in required_tests
    assert "no_runtime_adapter_modules_added" in required_tests
    assert "voice_examples_include_transcript_confidence_metadata" in required_tests
    assert "source_identity_fields_are_references_not_live_lookup" in required_tests
    assert "no_model_tool_terminal_robotics_approval_enforcement_or_audit_persistence_path" in required_tests


def test_hard_blockers_cover_high_risk_and_product_surfaces() -> None:
    assert REQUIRED_HARD_BLOCKERS <= set(_load_fixture()["hard_blockers"])


def test_phase_four_three_no_go_blocks_runtime_product_and_physical_world() -> None:
    assert REQUIRED_NO_GO <= set(_load_fixture()["phase_4_3_no_go"])


def test_ready_for_requires_explicit_approval_for_phase_four_four() -> None:
    fixture = _load_fixture()
    assert fixture["ready_for"] == [
        "phase_4_4_boundary_fixture_contract_extension_if_explicitly_approved"
    ]
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


def test_no_phase_four_three_runtime_modules_or_sparkbot_adapters_were_added() -> None:
    forbidden_paths = [
        REPO_ROOT / "lima" / "runtime_extraction.py",
        REPO_ROOT / "lima" / "kernel_pipeline.py",
        REPO_ROOT / "lima" / "adapters" / "sparkbot_runtime.py",
        REPO_ROOT / "lima" / "adapters" / "sparkbot_humaninput_live.py",
        REPO_ROOT / "lima" / "adapters" / "sparkbot_chat_voice.py",
        REPO_ROOT / "tests" / "helpers" / "runtime_extraction_harness.py",
    ]
    assert not any(path.exists() for path in forbidden_paths)
