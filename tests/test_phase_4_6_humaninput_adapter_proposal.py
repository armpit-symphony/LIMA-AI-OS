"""Static checks for Phase 4.6 non-production HumanInput adapter proposal."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PROPOSAL_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_4_6_NONPRODUCTION_HUMANINPUT_ADAPTER_PROPOSAL.md"
)
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_4_6_humaninput_adapter_proposal.json"
)
PHASE_4_4_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_4_4_humaninput_intake_fixture_contract.json"
)
PHASE_4_5_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_4_5_boundary_readiness_review.json"
)

REQUIRED_SOURCE_INPUTS = {
    "shell_ref",
    "channel_ref",
    "room_ref",
    "conversation_ref",
    "input_kind",
    "actor_ref",
    "session_ref",
    "passive_trust_context_ref",
    "owner_autonomy_ref",
    "redacted_content_ref_or_summary",
    "transcript_confidence_for_voice",
    "attachment_file_refs",
    "privacy_redaction_retention_visibility_hints",
}

REQUIRED_OUTPUT_CONTRACT = {
    "fixture_id",
    "boundary_id",
    "input_kind",
    "synthetic",
    "non_runtime",
    "content",
    "source",
    "actor",
    "session",
    "trust_context",
    "privacy",
    "lineage",
    "handoff",
    "capability_flags",
    "blocked_capabilities",
}

REQUIRED_BLOCKED_INTERPRETATIONS = {
    "permission_to_add_live_adapter_code",
    "permission_to_modify_lima_files",
    "permission_to_import_or_wire_sparkbot",
    "permission_to_implement_arc_bot",
    "permission_to_implement_custom_bots",
    "permission_to_add_runtime_behavior",
    "permission_to_call_models",
    "permission_to_expose_or_execute_tools",
    "permission_to_write_terminal_or_pty_input",
    "permission_to_call_robotics_or_physical_world_drivers",
    "permission_to_perform_live_auth_session_trust_lookup",
    "permission_to_implement_real_intentcompiler",
    "permission_to_implement_real_guardiandecision",
    "permission_to_enforce_approval_or_policy",
    "permission_to_execute_actions",
    "permission_to_persist_audit_events",
}

REQUIRED_NO_GO = {
    "runtime_behavior",
    "executable_pipeline",
    "test_only_composition_harness",
    "live_adapter_code",
    "files_under_lima",
    "sparkbot_import_wiring_route_import_or_code_copy",
    "arc_bot_implementation",
    "custom_bot_implementation",
    "model_calls",
    "tool_execution",
    "terminal_or_pty_behavior",
    "robotics_behavior",
    "robot_or_physical_world_behavior",
    "live_auth_session_trust_lookup",
    "real_intentcompiler",
    "real_guardiandecision",
    "approval_enforcement",
    "policy_enforcement",
    "adaptive_trust_enforcement",
    "execution",
    "audit_persistence",
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

RUNTIME_EXECUTION_LANGUAGE_RE = re.compile(
    r"\b(executes?|runs?|calls?|invokes?|dispatches?|authorizes?|approves?|enforces?|persists?)\b",
    re.IGNORECASE,
)
ALLOWED_EXECUTION_LANGUAGE_CONTEXT = re.compile(
    r"\b("
    r"not|no|non_|before_|blocked|forbidden|no_go|not_ready|cannot|does_not|"
    r"permission_to_|future_|expected_|proposal_|conditional_"
    r")",
    re.IGNORECASE,
)


def _load_json(path: Path) -> dict[str, Any]:
    assert path.exists()
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def _load_fixture() -> dict[str, Any]:
    return _load_json(FIXTURE_PATH)


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


def test_fixture_is_valid_phase_four_six_non_runtime_proposal() -> None:
    fixture = _load_fixture()
    assert fixture["phase"] == "4.6"
    assert fixture["status"] == "non_runtime_humaninput_adapter_proposal_only"
    assert fixture["non_runtime"] is True
    assert fixture["docs_tests_fixtures_only"] is True


def test_proposal_doc_exists_and_states_adapter_proposal_is_not_adapter() -> None:
    assert PROPOSAL_DOC_PATH.exists()
    proposal_doc = PROPOSAL_DOC_PATH.read_text(encoding="utf-8")
    assert "This is proposal metadata only" in proposal_doc
    assert "not a HumanInput adapter" in proposal_doc
    assert "NO-GO for live adapter implementation" in proposal_doc


def test_phase_four_five_source_is_recorded() -> None:
    fixture = _load_fixture()
    assert fixture["source_phase"] == "4.5"
    assert fixture["source_tag"] == "phase-4.5-boundary-readiness-review"
    assert fixture["source_merge_commit"] == "d826810"
    assert fixture["boundary_id"] == "humaninput_intake_boundary_for_chat_and_voice"


def test_proposal_is_metadata_only_and_not_runtime_objects() -> None:
    fixture = _load_fixture()
    assert fixture["key_rule"] == "a_humaninput_adapter_proposal_is_not_a_humaninput_adapter"
    assert all(fixture["proposal_is"].values())
    assert all(fixture["proposal_is_not"].values())


def test_future_adapter_boundary_stays_before_semantic_and_execution_boundaries() -> None:
    boundary = _load_fixture()["future_adapter_boundary"]
    assert boundary["input_side"] == "selected_shell_input_context_references"
    assert boundary["output_side"] == "phase_4_4_humaninput_fixture_contract_shape"
    assert boundary["before_intentenvelope"] is True
    assert boundary["before_guardiandecision"] is True
    assert boundary["before_model_harness"] is True
    assert boundary["before_tool_exposure"] is True
    assert boundary["before_execution"] is True


def test_expected_source_inputs_and_output_contract_are_reference_shapes() -> None:
    fixture = _load_fixture()
    assert REQUIRED_SOURCE_INPUTS <= set(fixture["expected_source_inputs"])
    assert REQUIRED_OUTPUT_CONTRACT <= set(fixture["expected_humaninput_output_contract"])


def test_metadata_handling_preserves_passive_references_and_handoff() -> None:
    handling = _load_fixture()["metadata_handling"]
    assert handling["source_metadata_reference_only"] is True
    assert handling["actor_session_metadata_reference_only"] is True
    assert handling["trust_autonomy_metadata_passive_and_non_granting"] is True
    assert handling["privacy_redaction_retention_visibility_explicit"] is True
    assert handling["voice_requires_transcript_confidence"] is True
    assert handling["lineage_seed_reference_only"] is True
    assert handling["handoff_toward_future_intentenvelope"] is True
    assert handling["handoff_toward_future_guardiandecision"] is True
    assert handling["all_can_flags_false"] is True
    assert handling["authority_identifiers_forbidden"] is True
    assert handling["live_integration_identifiers_forbidden"] is True


def test_explicit_blocked_interpretations_cover_runtime_and_authority_paths() -> None:
    assert REQUIRED_BLOCKED_INTERPRETATIONS <= set(
        _load_fixture()["explicit_blocked_interpretations"]
    )


def test_phase_four_six_no_go_blocks_all_hard_boundaries() -> None:
    assert REQUIRED_NO_GO <= set(_load_fixture()["phase_4_6_no_go"])


def test_phase_four_four_contract_remains_synthetic_inert_non_runtime() -> None:
    continuity = _load_fixture()["phase_4_4_contract_continuity"]
    assert continuity["remains_synthetic"] is True
    assert continuity["remains_inert"] is True
    assert continuity["remains_non_runtime"] is True
    assert continuity["all_can_flags_remain_false"] is True
    phase_4_4 = _load_json(PHASE_4_4_FIXTURE_PATH)
    assert phase_4_4["phase"] == "4.4"
    for record in phase_4_4["fixture_records"]:
        assert record["synthetic"] is True
        assert record["non_runtime"] is True
        assert all(value is False for value in record["capability_flags"].values())


def test_phase_four_five_readiness_review_remains_non_runtime() -> None:
    continuity = _load_fixture()["phase_4_5_readiness_continuity"]
    assert continuity["remains_non_runtime"] is True
    assert continuity["requires_explicit_approval_for_next_narrow_nonproduction_phase"] is True
    phase_4_5 = _load_json(PHASE_4_5_FIXTURE_PATH)
    assert phase_4_5["phase"] == "4.5"
    assert phase_4_5["non_runtime"] is True
    assert phase_4_5["ready_for"] == [
        "explicit_operator_approval_for_next_narrow_nonproduction_phase"
    ]


def test_decision_allows_only_future_design_review_not_implementation() -> None:
    decision = _load_fixture()["decision"]
    assert decision["conditional_go_for_future_explicitly_approved_humaninput_adapter_design_review"] is True
    assert decision["no_go_for_live_adapter_implementation"] is True
    assert decision["no_go_for_runtime_extraction_implementation"] is True
    assert decision["no_go_for_sparkbot_integration"] is True
    assert decision["no_go_for_product_shell_implementation"] is True
    assert decision["no_go_for_physical_world_action"] is True


def test_ready_for_requires_explicit_future_design_review_approval() -> None:
    fixture = _load_fixture()
    assert fixture["ready_for"] == [
        "explicit_operator_approval_for_future_humaninput_adapter_design_review"
    ]
    assert "live_humaninput_adapter_code" in fixture["not_ready_for"]
    assert "runtime_extraction_implementation" in fixture["not_ready_for"]
    assert "sparkbot_runtime_integration" in fixture["not_ready_for"]
    assert "terminal_pty_execution" in fixture["not_ready_for"]
    assert "physical_world_action" in fixture["not_ready_for"]


def test_boundary_results_show_no_behavior_lima_files_or_live_integration() -> None:
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


def test_proposal_fixture_does_not_introduce_unblocked_runtime_execution_language() -> None:
    for string_value in _all_strings(_load_fixture()):
        if RUNTIME_EXECUTION_LANGUAGE_RE.search(string_value):
            assert ALLOWED_EXECUTION_LANGUAGE_CONTEXT.search(string_value), string_value


def test_no_phase_four_six_runtime_modules_or_live_adapters_were_added() -> None:
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
