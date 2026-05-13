"""Static checks for Phase 4.4 HumanInput intake fixture contract extension."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_4_4_BOUNDARY_FIXTURE_CONTRACT_EXTENSION.md"
)
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_4_4_humaninput_intake_fixture_contract.json"
)

REQUIRED_RECORD_FIELDS = {
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

REQUIRED_FALSE_FLAGS = {
    "can_parse_action",
    "can_call_model",
    "can_select_tools",
    "can_expose_tools",
    "can_execute_tools",
    "can_write_terminal",
    "can_call_robotics",
    "can_approve",
    "can_enforce_policy",
    "can_persist_audit",
    "can_perform_live_auth_session_trust_lookup",
    "can_import_sparkbot",
    "can_wire_sparkbot",
}

FORBIDDEN_AUTHORITY_KEYS = {
    "approval_id",
    "authorization_id",
    "decision_id",
    "execution_id",
    "tool_call_id",
    "tool_invocation_id",
    "runtime_session_id",
    "production_session_id",
    "live_route_id",
    "integration_id",
    "sparkbot_route_id",
}

REQUIRED_BLOCKED_CAPABILITIES = {
    "natural_language_parsing_into_action",
    "model_calls",
    "tool_exposure_or_execution",
    "terminal_pty_behavior",
    "robotics_behavior",
    "approval_or_policy_enforcement",
    "audit_persistence",
    "live_auth_session_trust_lookup",
    "sparkbot_import_or_wiring",
    "production_integration",
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

ALLOWED_PRIVACY_CLASSES = {"private", "confidential"}
ALLOWED_REDACTION_CLASSES = {"reference_only", "summary_only"}
ALLOWED_RETENTION_CLASSES = {"short_lived", "review_limited"}
ALLOWED_VISIBILITY_CLASSES = {"operator_only", "owner_only"}

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


def _records() -> list[dict[str, Any]]:
    records = _load_fixture()["fixture_records"]
    assert isinstance(records, list)
    assert len(records) == 2
    for record in records:
        assert isinstance(record, dict)
    return records


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


def _all_mapping_keys(value: Any) -> list[str]:
    keys: list[str] = []
    if isinstance(value, dict):
        keys.extend(str(key) for key in value)
        for item in value.values():
            keys.extend(_all_mapping_keys(item))
    elif isinstance(value, list):
        for item in value:
            keys.extend(_all_mapping_keys(item))
    return keys


def test_phase_four_four_fixture_is_contract_extension_only() -> None:
    fixture = _load_fixture()
    assert fixture["phase"] == "4.4"
    assert fixture["status"] == "boundary_fixture_contract_extension_only"
    assert fixture["non_runtime"] is True


def test_contract_doc_exists_and_blocks_runtime_behavior() -> None:
    assert CONTRACT_DOC_PATH.exists()
    contract_doc = CONTRACT_DOC_PATH.read_text(encoding="utf-8")
    assert "Phase 4.4 extends fixture/contract metadata" in contract_doc
    assert "This phase is docs/tests/fixtures only" in contract_doc
    assert "NO-GO for runtime extraction implementation" in contract_doc


def test_phase_four_three_source_is_recorded() -> None:
    fixture = _load_fixture()
    assert fixture["source_phase"] == "4.3"
    assert fixture["source_tag"] == "phase-4.3-boundary-extraction-safety-gate"
    assert fixture["source_merge_commit"] == "9e2acfa"
    assert fixture["boundary_id"] == "humaninput_intake_boundary_for_chat_and_voice"


def test_contract_shape_requires_expected_record_fields() -> None:
    shape = _load_fixture()["contract_shape"]
    assert REQUIRED_RECORD_FIELDS <= set(shape["required_record_fields"])
    assert shape["input_kinds"] == ["text", "voice_transcript"]
    assert shape["voice_required_fields"] == ["voice"]


def test_hardening_rules_forbid_authority_and_unknown_capabilities() -> None:
    rules = _load_fixture()["hardening_rules"]
    assert rules["all_can_flags_must_be_false"] is True
    assert rules["authority_ids_forbidden"] is True
    assert rules["synthetic_refs_only"] is True
    assert rules["unknown_affirmative_capabilities_forbidden"] is True
    assert rules["live_integration_identifiers_forbidden"] is True


def test_records_include_synthetic_text_and_voice_shapes() -> None:
    kinds = {record["input_kind"] for record in _records()}
    assert kinds == {"text", "voice_transcript"}
    for record in _records():
        assert REQUIRED_RECORD_FIELDS <= set(record)
        assert record["boundary_id"] == "humaninput_intake_boundary_for_chat_and_voice"
        assert record["synthetic"] is True
        assert record["non_runtime"] is True


def test_fixture_content_is_synthetic_referenced_and_not_raw() -> None:
    for record in _records():
        content = record["content"]
        assert content["content_ref"].startswith("ref.synthetic.")
        assert "synthetic" in content["content_summary"]
        assert content["raw_content_included"] is False
        assert content["normalized_language"] == "en"
        assert all(ref.startswith("ref.synthetic.") for ref in content["attachment_refs"])


def test_voice_record_requires_transcript_confidence_and_no_raw_audio() -> None:
    voice_records = [record for record in _records() if record["input_kind"] == "voice_transcript"]
    assert len(voice_records) == 1
    voice = voice_records[0]["voice"]
    assert voice["transcript_ref"].startswith("transcript.synthetic.")
    assert isinstance(voice["transcript_confidence"], float)
    assert 0.0 <= voice["transcript_confidence"] <= 1.0
    assert voice["transcript_confidence_required"] is True
    assert voice["raw_audio_included"] is False
    assert voice["audio_ref"].startswith("audio.synthetic.")


def test_source_actor_session_and_trust_metadata_are_reference_only() -> None:
    for record in _records():
        source = record["source"]
        actor = record["actor"]
        session = record["session"]
        trust_context = record["trust_context"]
        assert source["shell_ref"].startswith("shell.synthetic.")
        assert source["channel_ref"].startswith("channel.synthetic.")
        assert source["live_route"] is False
        assert source["sparkbot_wired"] is False
        assert actor["actor_ref"].startswith("actor.synthetic.")
        assert actor["identity_verified"] is False
        assert actor["live_lookup_performed"] is False
        assert session["session_ref"].startswith("session.synthetic.")
        assert session["live_session"] is False
        assert session["auth_lookup_performed"] is False
        assert session["trust_lookup_performed"] is False
        assert trust_context["trust_context_ref"].startswith("trust.synthetic.")
        assert trust_context["owner_autonomy_ref"].startswith("autonomy.synthetic.")
        assert trust_context["grants_trust"] is False
        assert trust_context["enforces_trust"] is False
        assert trust_context["live_lookup_performed"] is False


def test_privacy_fields_are_explicit_and_raw_content_blocked() -> None:
    for record in _records():
        privacy = record["privacy"]
        assert privacy["privacy_class"] in ALLOWED_PRIVACY_CLASSES
        assert privacy["redaction_class"] in ALLOWED_REDACTION_CLASSES
        assert privacy["retention_class"] in ALLOWED_RETENTION_CLASSES
        assert privacy["visibility_class"] in ALLOWED_VISIBILITY_CLASSES
        assert privacy["raw_content_allowed_in_fixture"] is False


def test_lineage_is_seed_only_and_not_audit_persistence() -> None:
    for record in _records():
        lineage = record["lineage"]
        assert lineage["lineage_seed_ref"].startswith("lineage.synthetic.seed.")
        assert lineage["audit_persisted"] is False
        assert lineage["spine_event_created"] is False


def test_handoff_requires_future_boundaries_without_authority() -> None:
    for record in _records():
        handoff = record["handoff"]
        assert handoff["next_boundary"] == "future_intentenvelope"
        assert handoff["requires_intentenvelope"] is True
        assert handoff["requires_guardiandecision_before_consequential_behavior"] is True
        assert handoff["authorizes_action"] is False
        assert handoff["approves_action"] is False
        assert handoff["executes_action"] is False


def test_capability_flags_prove_records_are_inert() -> None:
    for record in _records():
        flags = record["capability_flags"]
        assert REQUIRED_FALSE_FLAGS <= set(flags)
        for flag_name, flag_value in flags.items():
            assert flag_name.startswith("can_"), flag_name
            assert flag_value is False, flag_name
        assert REQUIRED_BLOCKED_CAPABILITIES <= set(record["blocked_capabilities"])


def test_records_do_not_carry_authority_or_live_integration_identifiers() -> None:
    for record in _records():
        keys = set(_all_mapping_keys(record))
        assert keys.isdisjoint(FORBIDDEN_AUTHORITY_KEYS)


def test_phase_four_four_no_go_blocks_all_hard_boundaries() -> None:
    assert REQUIRED_NO_GO <= set(_load_fixture()["phase_4_4_no_go"])


def test_ready_for_only_allows_phase_four_five_readiness_review() -> None:
    fixture = _load_fixture()
    assert fixture["ready_for"] == ["phase_4_5_boundary_readiness_review"]
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


def test_no_phase_four_four_live_runtime_modules_or_wiring_were_added() -> None:
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
