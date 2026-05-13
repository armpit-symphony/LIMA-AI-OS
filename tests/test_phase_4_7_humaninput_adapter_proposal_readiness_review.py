"""Static checks for Phase 4.7 HumanInput adapter proposal readiness review."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
REVIEW_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_4_7_NONPRODUCTION_HUMANINPUT_ADAPTER_PROPOSAL_READINESS_REVIEW.md"
)
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_4_7_humaninput_adapter_proposal_readiness_review.json"
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
PHASE_4_6_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_4_6_humaninput_adapter_proposal.json"
)

REQUIRED_FINDINGS = {
    "future_adapter_proposal_still_non_runtime",
    "source_shell_channel_room_actor_session_refs_remain_passive_metadata",
    "passive_trust_autonomy_refs_remain_reference_only",
    "transcript_confidence_metadata_remains_descriptive_only",
    "privacy_redaction_retention_visibility_fields_remain_metadata_only",
    "lineage_seed_refs_remain_reference_only",
    "handoff_requirements_toward_future_intentenvelope_remain_non_executable",
    "handoff_requirements_toward_future_guardiandecision_remain_non_executable",
    "proposal_ready_for_future_adapter_safety_gate_docs",
    "proposal_not_ready_for_live_adapter_code",
}

REQUIRED_NOT_READY = {
    "live_adapter_code",
    "runtime_wiring",
    "sparkbot_integration",
    "sparkbot_import_or_wiring",
    "real_intentcompiler",
    "real_guardiandecision",
    "approval",
    "approval_enforcement",
    "policy_enforcement",
    "execution",
    "audit_persistence",
    "model_calls",
    "tool_execution",
    "terminal_pty_behavior",
    "robotics_behavior",
    "physical_world_action",
    "live_auth_session_trust_lookup",
    "production_shell_implementation",
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
    r"permission_to_|future_|expected_|proposal_|conditional_|review_|"
    r"readiness_|source_|latest_"
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


def test_fixture_is_valid_phase_four_seven_non_runtime_readiness_review() -> None:
    fixture = _load_fixture()
    assert fixture["phase"] == "4.7"
    assert fixture["status"] == "non_runtime_humaninput_adapter_proposal_readiness_review"
    assert fixture["non_runtime"] is True
    assert fixture["docs_tests_fixtures_only"] is True


def test_review_doc_exists_and_states_review_is_not_adapter() -> None:
    assert REVIEW_DOC_PATH.exists()
    review_doc = REVIEW_DOC_PATH.read_text(encoding="utf-8")
    assert "This is readiness-review metadata only" in review_doc
    assert "not a HumanInput adapter" in review_doc
    assert "CONDITIONAL GO for Phase 4.8 HumanInput Adapter Safety Gate Docs" in review_doc
    assert "NO-GO for live adapter implementation" in review_doc


def test_phase_four_six_source_is_recorded() -> None:
    fixture = _load_fixture()
    assert fixture["source_phase"] == "4.6"
    assert fixture["source_tag"] == "phase-4.6-nonproduction-humaninput-adapter-proposal"
    assert fixture["source_merge_commit"] == "cedfad75b9a72ce346214993a47d50c63edf404b"
    assert fixture["boundary_id"] == "humaninput_intake_boundary_for_chat_and_voice"


def test_review_is_metadata_only_and_not_runtime_objects() -> None:
    fixture = _load_fixture()
    assert fixture["key_rule"] == "a_readiness_review_of_an_adapter_proposal_is_not_an_adapter"
    assert all(fixture["review_is"].values())
    assert all(fixture["review_is_not"].values())


def test_review_findings_cover_requested_readiness_questions() -> None:
    findings = _load_fixture()["review_findings"]
    assert REQUIRED_FINDINGS == set(findings)
    assert all(findings.values())


def test_ready_for_is_limited_to_safety_gate_docs_or_non_runtime_review() -> None:
    assert set(_load_fixture()["ready_for"]) == {
        "phase_4_8_humaninput_adapter_safety_gate_docs",
        "further_non_runtime_review",
    }


def test_not_ready_for_blocks_live_adapter_runtime_and_authority_paths() -> None:
    assert REQUIRED_NOT_READY <= set(_load_fixture()["not_ready_for"])


def test_explicit_blocked_interpretations_cover_runtime_and_authority_paths() -> None:
    assert REQUIRED_BLOCKED_INTERPRETATIONS <= set(
        _load_fixture()["explicit_blocked_interpretations"]
    )


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
    assert continuity["does_not_approve_runtime_extraction"] is True
    phase_4_5 = _load_json(PHASE_4_5_FIXTURE_PATH)
    assert phase_4_5["phase"] == "4.5"
    assert phase_4_5["non_runtime"] is True
    assert phase_4_5["decision"]["no_go_for_runtime_extraction_implementation"] is True


def test_phase_four_six_adapter_proposal_remains_non_runtime() -> None:
    continuity = _load_fixture()["phase_4_6_proposal_continuity"]
    assert continuity["remains_non_runtime"] is True
    assert continuity["remains_proposal_metadata_only"] is True
    assert continuity["remains_not_adapter"] is True
    assert continuity["remains_not_executable"] is True
    assert continuity["remains_not_trust_lookup"] is True
    phase_4_6 = _load_json(PHASE_4_6_FIXTURE_PATH)
    assert phase_4_6["phase"] == "4.6"
    assert phase_4_6["non_runtime"] is True
    assert phase_4_6["proposal_is"]["proposal_metadata_only"] is True
    assert phase_4_6["proposal_is_not"]["humaninput_adapter"] is True
    assert phase_4_6["proposal_is_not"]["trust_lookup"] is True


def test_decision_allows_only_adapter_safety_gate_docs_not_implementation() -> None:
    decision = _load_fixture()["decision"]
    assert decision["conditional_go_for_phase_4_8_humaninput_adapter_safety_gate_docs"] is True
    assert decision["no_go_for_live_adapter_implementation"] is True
    assert decision["no_go_for_runtime_extraction_implementation"] is True
    assert decision["no_go_for_sparkbot_integration"] is True
    assert decision["no_go_for_product_shell_implementation"] is True
    assert decision["no_go_for_physical_world_action"] is True


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


def test_readiness_fixture_does_not_introduce_unblocked_runtime_execution_language() -> None:
    for string_value in _all_strings(_load_fixture()):
        if RUNTIME_EXECUTION_LANGUAGE_RE.search(string_value):
            assert ALLOWED_EXECUTION_LANGUAGE_CONTEXT.search(string_value), string_value


def test_no_phase_four_seven_runtime_modules_or_live_adapters_were_added() -> None:
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
