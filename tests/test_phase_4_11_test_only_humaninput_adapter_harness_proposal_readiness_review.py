"""Static checks for Phase 4.11 test-only harness proposal readiness review."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_4_11_TEST_ONLY_HUMANINPUT_ADAPTER_HARNESS_PROPOSAL_READINESS_REVIEW.md"
)
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_4_11_test_only_humaninput_adapter_harness_proposal_readiness_review.json"
)
PHASE_4_10_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_4_10_test_only_humaninput_adapter_harness_proposal.json"
)

REQUIRED_FINDINGS = {
    "proposal_stays_metadata_only",
    "proposal_does_not_implement_harness_code",
    "proposal_does_not_implement_adapter_code",
    "expected_inputs_are_synthetic",
    "validates_humaninput_shape_only",
    "blocks_live_shell_session_auth_trust_sparkbot_model_tool_terminal_robot_and_production_sources",
    "does_not_create_intentenvelope",
    "does_not_create_guardiandecision",
    "does_not_approve_enforce_execute_or_persist_audit_data",
    "does_not_imply_production_adapter_readiness",
}

REQUIRED_NOT_READY = {
    "test_only_adapter_harness_code",
    "live_adapter_code",
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


def test_fixture_is_valid_phase_four_eleven_non_runtime_readiness_review() -> None:
    fixture = _load_fixture()
    assert fixture["phase"] == "4.11"
    assert fixture["status"] == "non_runtime_test_only_humaninput_adapter_harness_proposal_readiness_review"
    assert fixture["non_runtime"] is True
    assert fixture["docs_tests_fixtures_only"] is True


def test_document_exists_and_states_review_is_not_harness_code() -> None:
    assert DOC_PATH.exists()
    doc = DOC_PATH.read_text(encoding="utf-8")
    assert "readiness-review metadata only" in doc
    assert "not harness code" in doc
    assert "CONDITIONAL GO for Phase 4.12" in doc
    assert "NO-GO for test-only harness implementation" in doc


def test_phase_four_ten_source_is_recorded() -> None:
    fixture = _load_fixture()
    assert fixture["source_phase"] == "4.10"
    assert fixture["source_tag"] == "phase-4.10-nonproduction-test-only-humaninput-adapter-harness-proposal"
    assert fixture["source_merge_commit"] == "e7c7fb2fdaae6981aa1d6f984ba1e74c6a0c1dfe"


def test_review_is_metadata_only_and_not_runtime_or_harness_code() -> None:
    fixture = _load_fixture()
    assert fixture["key_rule"] == "readiness_review_of_test_only_harness_proposal_is_not_harness_code"
    assert all(fixture["review_is"].values())
    assert all(fixture["review_is_not"].values())


def test_review_findings_answer_safety_gate_readiness_question() -> None:
    findings = _load_fixture()["review_findings"]
    assert REQUIRED_FINDINGS == set(findings)
    assert all(findings.values())


def test_phase_four_ten_proposal_continuity_remains_non_runtime() -> None:
    continuity = _load_fixture()["phase_4_10_proposal_continuity"]
    phase_4_10 = _load_json(PHASE_4_10_FIXTURE_PATH)
    assert continuity["remains_non_runtime"] is True
    assert continuity["remains_proposal_metadata_only"] is True
    assert continuity["does_not_add_harness_code"] is True
    assert phase_4_10["non_runtime"] is True
    assert phase_4_10["proposal_is_not"]["test_only_adapter_harness_code"] is True


def test_ready_for_is_limited_to_phase_four_twelve_safety_gate_docs() -> None:
    assert set(_load_fixture()["ready_for"]) == {
        "phase_4_12_test_only_humaninput_adapter_harness_safety_gate_docs",
        "further_non_runtime_review",
    }


def test_not_ready_for_blocks_implementation_runtime_and_authority_paths() -> None:
    assert REQUIRED_NOT_READY <= set(_load_fixture()["not_ready_for"])


def test_decision_allows_only_safety_gate_docs_next() -> None:
    decision = _load_fixture()["decision"]
    assert decision["conditional_go_for_phase_4_12_safety_gate_docs"] is True
    assert decision["no_go_for_test_only_harness_implementation"] is True
    assert decision["no_go_for_live_adapter_implementation"] is True
    assert decision["no_go_for_runtime_extraction_implementation"] is True
    assert decision["no_go_for_sparkbot_integration"] is True
    assert decision["no_go_for_physical_world_action"] is True


def test_boundary_results_show_no_behavior_lima_files_harness_or_live_integration() -> None:
    boundary = _load_fixture()["boundary_results"]
    assert boundary["runtime_behavior_added"] is False
    assert boundary["blocked_behavior_added"] is False
    assert boundary["files_under_lima_modified"] is False
    assert boundary["sparkbot_imported"] is False
    assert boundary["sparkbot_wired"] is False
    assert boundary["live_adapter_code_added"] is False
    assert boundary["test_only_adapter_harness_added"] is False
    assert boundary["real_intentcompiler_added"] is False
    assert boundary["real_guardiandecision_added"] is False
    assert boundary["approval_enforcement_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False


def test_fixture_has_no_private_operational_data() -> None:
    for string_value in _all_strings(_load_fixture()):
        assert not FORBIDDEN_PRIVATE_OR_OPERATIONAL_RE.search(string_value), string_value


def test_no_phase_four_eleven_runtime_modules_live_adapters_or_harness_were_added() -> None:
    forbidden_paths = [
        REPO_ROOT / "lima" / "runtime_extraction.py",
        REPO_ROOT / "lima" / "kernel_pipeline.py",
        REPO_ROOT / "lima" / "adapters" / "sparkbot_runtime.py",
        REPO_ROOT / "lima" / "adapters" / "sparkbot_humaninput_live.py",
        REPO_ROOT / "tests" / "helpers" / "runtime_extraction_harness.py",
        REPO_ROOT / "tests" / "helpers" / "humaninput_adapter_harness.py",
        REPO_ROOT / "tests" / "helpers" / "test_only_humaninput_adapter_harness.py",
    ]
    assert not any(path.exists() for path in forbidden_paths)
