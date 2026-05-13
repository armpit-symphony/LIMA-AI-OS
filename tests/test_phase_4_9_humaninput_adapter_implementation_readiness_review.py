"""Static checks for Phase 4.9 HumanInput adapter implementation readiness review."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
REVIEW_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_4_9_HUMANINPUT_ADAPTER_IMPLEMENTATION_READINESS_REVIEW.md"
)
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_4_9_humaninput_adapter_implementation_readiness_review.json"
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
PHASE_4_8_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_4_8_humaninput_adapter_safety_gate_docs.json"
)
SAFETY_GATE_PATH = REPO_ROOT / "docs" / "HUMANINPUT_ADAPTER_SAFETY_GATE.md"

REQUIRED_FINDINGS = {
    "humaninput_fixture_contract_remains_synthetic",
    "humaninput_fixture_contract_remains_inert",
    "humaninput_fixture_contract_remains_non_runtime",
    "source_shell_channel_room_actor_session_refs_remain_passive_metadata",
    "trust_autonomy_refs_remain_passive_references_only",
    "transcript_confidence_remains_descriptive_metadata_only",
    "privacy_redaction_retention_visibility_fields_remain_metadata_only",
    "lineage_seed_refs_remain_reference_only",
    "future_intentenvelope_handoff_remains_non_executable",
    "future_guardiandecision_handoff_remains_non_executable",
    "safety_gate_clearly_blocks_live_adapter_code",
    "safety_gate_requires_humaninput_only_output",
    "boundary_ready_for_future_test_only_adapter_harness_proposal",
    "boundary_not_ready_for_production_adapter_implementation",
}

REQUIRED_NOT_READY = {
    "live_adapter_code",
    "test_only_adapter_harness_code",
    "runtime_wiring",
    "production_sparkbot_integration",
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
    r"readiness_|source_|latest_|gate_|required_|test_only_"
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


def test_fixture_is_valid_phase_four_nine_non_runtime_readiness_review() -> None:
    fixture = _load_fixture()
    assert fixture["phase"] == "4.9"
    assert fixture["status"] == "non_runtime_humaninput_adapter_implementation_readiness_review"
    assert fixture["non_runtime"] is True
    assert fixture["docs_tests_fixtures_only"] is True


def test_review_doc_exists_and_states_review_is_not_adapter_or_harness() -> None:
    assert REVIEW_DOC_PATH.exists()
    review_doc = REVIEW_DOC_PATH.read_text(encoding="utf-8")
    assert "readiness-review metadata only" in review_doc
    assert "not a HumanInput adapter" in review_doc
    assert "not a test-only harness" in review_doc
    assert "not readiness for runtime adapter implementation" in review_doc


def test_phase_four_eight_source_is_recorded() -> None:
    fixture = _load_fixture()
    assert fixture["source_phase"] == "4.8"
    assert fixture["source_tag"] == "phase-4.8-humaninput-adapter-safety-gate-docs"
    assert fixture["source_merge_commit"] == "ad72435909ee09b19ca83a10900cd628b88b6a1d"
    assert fixture["boundary_id"] == "humaninput_intake_boundary_for_chat_and_voice"


def test_review_is_metadata_only_and_not_runtime_objects() -> None:
    fixture = _load_fixture()
    assert fixture["key_rule"] == (
        "readiness_to_discuss_future_test_only_adapter_harness_is_not_runtime_adapter_implementation_readiness"
    )
    assert all(fixture["review_is"].values())
    assert all(fixture["review_is_not"].values())


def test_review_findings_cover_requested_readiness_questions() -> None:
    findings = _load_fixture()["review_findings"]
    assert REQUIRED_FINDINGS == set(findings)
    assert all(findings.values())


def test_ready_for_is_limited_to_future_explicit_harness_proposal_or_non_runtime_review() -> None:
    assert set(_load_fixture()["ready_for"]) == {
        "future_explicitly_approved_test_only_humaninput_adapter_harness_proposal_docs_tests_fixtures_only",
        "further_non_runtime_review",
    }


def test_not_ready_for_blocks_live_runtime_sparkbot_and_authority_paths() -> None:
    assert REQUIRED_NOT_READY <= set(_load_fixture()["not_ready_for"])


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
    phase_4_5 = _load_json(PHASE_4_5_FIXTURE_PATH)
    continuity = _load_fixture()["phase_4_5_readiness_continuity"]
    assert phase_4_5["phase"] == "4.5"
    assert phase_4_5["non_runtime"] is True
    assert continuity["remains_non_runtime"] is True
    assert continuity["does_not_approve_runtime_extraction"] is True


def test_phase_four_six_adapter_proposal_remains_non_runtime() -> None:
    phase_4_6 = _load_json(PHASE_4_6_FIXTURE_PATH)
    continuity = _load_fixture()["phase_4_6_proposal_continuity"]
    assert phase_4_6["phase"] == "4.6"
    assert phase_4_6["non_runtime"] is True
    assert phase_4_6["proposal_is_not"]["humaninput_adapter"] is True
    assert continuity["remains_non_runtime"] is True
    assert continuity["remains_not_adapter"] is True


def test_phase_four_eight_safety_gate_remains_non_runtime_and_blocks_live_code() -> None:
    phase_4_8 = _load_json(PHASE_4_8_FIXTURE_PATH)
    continuity = _load_fixture()["phase_4_8_safety_gate_continuity"]
    assert phase_4_8["phase"] == "4.8"
    assert phase_4_8["non_runtime"] is True
    assert phase_4_8["required_adapter_contract"]["future_adapter_must_return_humaninput_only"] is True
    assert "live_adapter_code" in phase_4_8["required_blockers"]
    assert continuity["remains_non_runtime"] is True
    assert continuity["requires_humaninput_only_output"] is True
    assert continuity["blocks_live_adapter_code"] is True
    assert continuity["blocks_test_only_harness_code_in_phase_4_9"] is True


def test_safety_gate_document_blocks_live_adapter_and_requires_humaninput_only() -> None:
    gate_doc = SAFETY_GATE_PATH.read_text(encoding="utf-8")
    assert "produce HumanInput only" in gate_doc
    assert "live adapter code" in gate_doc
    assert "Sparkbot import or wiring" in gate_doc
    assert "real IntentCompiler" in gate_doc
    assert "real GuardianDecision" in gate_doc


def test_decision_allows_only_future_explicit_test_only_harness_proposal() -> None:
    decision = _load_fixture()["decision"]
    assert decision[
        "conditional_go_for_future_explicitly_approved_test_only_adapter_harness_proposal_docs_tests_fixtures_only"
    ] is True
    assert decision["go_for_further_non_runtime_review_if_ambiguity_appears"] is True
    assert decision["no_go_for_live_adapter_implementation"] is True
    assert decision["no_go_for_runtime_extraction_implementation"] is True
    assert decision["no_go_for_sparkbot_integration"] is True
    assert decision["no_go_for_product_shell_implementation"] is True
    assert decision["no_go_for_physical_world_action"] is True


def test_boundary_results_show_no_behavior_lima_files_harness_or_live_integration() -> None:
    boundary = _load_fixture()["boundary_results"]
    assert boundary["runtime_behavior_added"] is False
    assert boundary["blocked_behavior_added"] is False
    assert boundary["files_under_lima_modified"] is False
    assert boundary["sparkbot_files_modified"] is False
    assert boundary["sparkbot_imported"] is False
    assert boundary["sparkbot_wired"] is False
    assert boundary["sparkbot_code_copied"] is False
    assert boundary["live_adapter_code_added"] is False
    assert boundary["test_only_adapter_harness_added"] is False
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


def test_no_phase_four_nine_runtime_modules_live_adapters_or_harness_were_added() -> None:
    forbidden_paths = [
        REPO_ROOT / "lima" / "runtime_extraction.py",
        REPO_ROOT / "lima" / "kernel_pipeline.py",
        REPO_ROOT / "lima" / "adapters" / "sparkbot_runtime.py",
        REPO_ROOT / "lima" / "adapters" / "sparkbot_humaninput_live.py",
        REPO_ROOT / "lima" / "adapters" / "sparkbot_chat_voice.py",
        REPO_ROOT / "lima" / "adapters" / "sparkbot_voice_live.py",
        REPO_ROOT / "tests" / "helpers" / "runtime_extraction_harness.py",
        REPO_ROOT / "tests" / "helpers" / "humaninput_adapter_harness.py",
        REPO_ROOT / "tests" / "helpers" / "test_only_humaninput_adapter_harness.py",
    ]
    assert not any(path.exists() for path in forbidden_paths)
