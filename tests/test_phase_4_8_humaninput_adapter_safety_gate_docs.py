"""Static checks for Phase 4.8 HumanInput adapter safety gate docs."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_4_8_HUMANINPUT_ADAPTER_SAFETY_GATE_DOCS.md"
GATE_DOC_PATH = REPO_ROOT / "docs" / "HUMANINPUT_ADAPTER_SAFETY_GATE.md"
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_4_8_humaninput_adapter_safety_gate_docs.json"
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
PHASE_4_7_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_4_7_humaninput_adapter_proposal_readiness_review.json"
)

REQUIRED_ADAPTER_CONTRACT = {
    "future_adapter_must_return_humaninput_only",
    "source_metadata_reference_only",
    "shell_channel_room_actor_session_refs_passive",
    "trust_autonomy_refs_non_granting",
    "transcript_confidence_descriptive_only",
    "privacy_redaction_retention_visibility_metadata_only",
    "lineage_seed_refs_reference_only",
    "cannot_create_intentenvelope",
    "cannot_create_guardiandecision",
    "capability_flags_non_authorizing",
    "blocked_capabilities_explicit",
}

REQUIRED_BLOCKERS = {
    "files_under_lima_before_explicit_implementation_approval",
    "live_adapter_code",
    "sparkbot_import_or_wiring",
    "sparkbot_route_import_or_code_copy",
    "runtime_behavior",
    "natural_language_parsing_into_action",
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
    r"readiness_|source_|latest_|gate_|required_"
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


def test_fixture_is_valid_phase_four_eight_non_runtime_safety_gate_docs() -> None:
    fixture = _load_fixture()
    assert fixture["phase"] == "4.8"
    assert fixture["status"] == "non_runtime_humaninput_adapter_safety_gate_docs"
    assert fixture["non_runtime"] is True
    assert fixture["docs_tests_fixtures_only"] is True


def test_phase_and_gate_docs_exist_and_state_gate_is_not_adapter_code() -> None:
    assert PHASE_DOC_PATH.exists()
    assert GATE_DOC_PATH.exists()
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    gate_doc = GATE_DOC_PATH.read_text(encoding="utf-8")
    assert "This is docs/tests/fixtures only" in phase_doc
    assert "not a HumanInput adapter" in phase_doc
    assert "not adapter code" in gate_doc
    assert "produce HumanInput only" in gate_doc


def test_phase_four_seven_source_is_recorded() -> None:
    fixture = _load_fixture()
    assert fixture["source_phase"] == "4.7"
    assert fixture["source_tag"] == (
        "phase-4.7-nonproduction-humaninput-adapter-proposal-readiness-review"
    )
    assert fixture["source_merge_commit"] == "94ca10c66090f57da6e20d5105849e96abfb1f0a"
    assert fixture["boundary_id"] == "humaninput_intake_boundary_for_chat_and_voice"


def test_gate_is_metadata_only_and_not_runtime_objects() -> None:
    fixture = _load_fixture()
    assert fixture["key_rule"] == "humaninput_adapter_safety_gate_docs_are_not_adapter_code"
    assert all(fixture["gate_is"].values())
    assert all(fixture["gate_is_not"].values())


def test_required_adapter_contract_forces_humaninput_only_boundary() -> None:
    contract = _load_fixture()["required_adapter_contract"]
    assert REQUIRED_ADAPTER_CONTRACT == set(contract)
    assert all(contract.values())


def test_required_blockers_cover_live_runtime_and_authority_paths() -> None:
    assert REQUIRED_BLOCKERS <= set(_load_fixture()["required_blockers"])


def test_review_checklist_blocks_production_and_private_operational_data() -> None:
    checklist = _load_fixture()["review_checklist"]
    assert checklist["adapter_returns_humaninput_only"] is True
    assert checklist["no_intentenvelope_created"] is True
    assert checklist["no_guardiandecision_created"] is True
    assert checklist["no_approval_enforcement_execution_or_audit_persistence"] is True
    assert checklist["no_model_tool_terminal_robot_or_physical_world_behavior"] is True
    assert checklist["no_live_auth_session_or_trust_lookup"] is True
    assert checklist["no_sparkbot_code_copied_imported_or_wired"] is True
    assert checklist["no_production_integration_identifiers"] is True
    assert checklist["no_secrets_credentials_tokens_hostnames_deploy_details_or_private_operational_data"] is True
    assert checklist["explicit_approval_required_for_any_future_code"] is True


def test_ready_for_is_limited_to_explicit_non_runtime_adapter_design_review() -> None:
    assert set(_load_fixture()["ready_for"]) == {
        "future_explicit_non_runtime_adapter_design_review",
        "further_non_runtime_review",
    }


def test_not_ready_for_blocks_live_adapter_runtime_and_authority_paths() -> None:
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


def test_phase_four_five_six_and_seven_remain_non_runtime() -> None:
    phase_4_5 = _load_json(PHASE_4_5_FIXTURE_PATH)
    phase_4_6 = _load_json(PHASE_4_6_FIXTURE_PATH)
    phase_4_7 = _load_json(PHASE_4_7_FIXTURE_PATH)
    assert phase_4_5["non_runtime"] is True
    assert phase_4_6["non_runtime"] is True
    assert phase_4_7["non_runtime"] is True
    assert phase_4_6["proposal_is_not"]["humaninput_adapter"] is True
    assert phase_4_7["decision"]["conditional_go_for_phase_4_8_humaninput_adapter_safety_gate_docs"] is True
    assert _load_fixture()["phase_4_7_readiness_continuity"]["recommends_safety_gate_docs_only"] is True


def test_decision_allows_only_future_explicit_non_runtime_design_review() -> None:
    decision = _load_fixture()["decision"]
    assert decision["conditional_go_for_future_explicit_non_runtime_adapter_design_review"] is True
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


def test_safety_gate_fixture_does_not_introduce_unblocked_runtime_execution_language() -> None:
    for string_value in _all_strings(_load_fixture()):
        if RUNTIME_EXECUTION_LANGUAGE_RE.search(string_value):
            assert ALLOWED_EXECUTION_LANGUAGE_CONTEXT.search(string_value), string_value


def test_no_phase_four_eight_runtime_modules_or_live_adapters_were_added() -> None:
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
