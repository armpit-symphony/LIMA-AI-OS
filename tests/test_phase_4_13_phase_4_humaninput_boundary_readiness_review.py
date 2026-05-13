"""Static checks for Phase 4.13 HumanInput boundary readiness review."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_4_13_PHASE_4_HUMANINPUT_BOUNDARY_READINESS_REVIEW.md"
)
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_4_13_phase_4_humaninput_boundary_readiness_review.json"
)
PHASE_4_4_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_4_4_humaninput_intake_fixture_contract.json"
)
PHASE_4_8_GATE_DOC_PATH = REPO_ROOT / "docs" / "HUMANINPUT_ADAPTER_SAFETY_GATE.md"
PHASE_4_12_GATE_DOC_PATH = (
    REPO_ROOT / "docs" / "TEST_ONLY_HUMANINPUT_ADAPTER_HARNESS_SAFETY_GATE.md"
)

REQUIRED_INPUTS = {
    "phase_4_4_humaninput_fixture_contract_extension",
    "phase_4_5_boundary_readiness_review",
    "phase_4_6_humaninput_adapter_proposal",
    "phase_4_7_adapter_proposal_readiness_review",
    "phase_4_8_humaninput_adapter_safety_gate_docs",
    "phase_4_9_humaninput_adapter_implementation_readiness_review",
    "phase_4_10_test_only_humaninput_adapter_harness_proposal",
    "phase_4_11_test_only_harness_proposal_readiness_review",
    "phase_4_12_test_only_humaninput_adapter_harness_safety_gate_docs",
}

EXPECTED_READY_FOR = {
    "future_explicitly_approved_test_only_humaninput_adapter_harness_implementation_phase",
    "further_non_runtime_review",
}

REQUIRED_NOT_READY_FOR = {
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


def test_fixture_is_valid_phase_four_thirteen_non_runtime_readiness_review() -> None:
    fixture = _load_fixture()
    assert fixture["phase"] == "4.13"
    assert fixture["status"] == "non_runtime_phase_4_humaninput_boundary_readiness_review"
    assert fixture["non_runtime"] is True
    assert fixture["docs_tests_fixtures_only"] is True


def test_doc_exists_and_states_review_is_not_runtime_or_harness_implementation() -> None:
    assert PHASE_DOC_PATH.exists()
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "not harness implementation" in phase_doc
    assert "not adapter implementation" in phase_doc
    assert "not runtime wiring" in phase_doc
    assert "It does not start that implementation." in phase_doc


def test_phase_four_twelve_source_is_recorded() -> None:
    fixture = _load_fixture()
    assert fixture["source_phase"] == "4.12"
    assert fixture["source_tag"] == (
        "phase-4.12-test-only-humaninput-adapter-harness-safety-gate-docs"
    )
    assert fixture["source_merge_commit"] == "e855614c5c3b8028021e059084330d01103dc844"


def test_review_inputs_cover_full_humaninput_boundary_lane() -> None:
    assert REQUIRED_INPUTS == set(_load_fixture()["review_inputs"])


def test_review_is_metadata_only_and_not_runtime_or_harness_code() -> None:
    fixture = _load_fixture()
    assert fixture["key_rule"] == (
        "readiness_for_future_test_only_harness_implementation_is_not_runtime_readiness"
    )
    assert all(fixture["review_is"].values())
    assert all(fixture["review_is_not"].values())


def test_readiness_findings_keep_metadata_passive_and_handoffs_non_executable() -> None:
    findings = _load_fixture()["readiness_findings"]
    assert all(findings.values())
    assert findings["humaninput_fixture_contract_is_synthetic_inert_non_runtime"] is True
    assert findings["source_refs_remain_passive_metadata"] is True
    assert findings["trust_and_autonomy_refs_remain_passive"] is True
    assert findings["intentenvelope_handoff_remains_future_non_executable"] is True
    assert findings["guardiandecision_handoff_remains_future_non_executable"] is True


def test_known_gaps_show_no_runtime_adapter_harness_or_authority_path_exists() -> None:
    gaps = set(_load_fixture()["known_gaps"])
    assert "no_test_only_humaninput_adapter_harness_implementation_exists" in gaps
    assert "no_live_humaninput_adapter_exists" in gaps
    assert "no_sparkbot_production_integration_exists" in gaps
    assert "no_runtime_extraction_implementation_exists" in gaps
    assert "no_approval_enforcement_execution_audit_path_exists" in gaps


def test_ready_for_is_limited_to_future_explicit_harness_phase_or_review() -> None:
    assert set(_load_fixture()["ready_for"]) == EXPECTED_READY_FOR


def test_not_ready_for_blocks_live_runtime_sparkbot_authority_and_physical_paths() -> None:
    assert REQUIRED_NOT_READY_FOR <= set(_load_fixture()["not_ready_for"])


def test_decision_does_not_approve_runtime_or_production_paths() -> None:
    decision = _load_fixture()["decision"]
    assert decision[
        "conditional_go_for_future_explicitly_approved_test_only_humaninput_adapter_harness_implementation_phase"
    ] is True
    assert decision["go_for_further_non_runtime_review"] is True
    assert decision["no_go_for_live_adapter_implementation"] is True
    assert decision["no_go_for_runtime_extraction_implementation"] is True
    assert decision["no_go_for_sparkbot_integration"] is True
    assert decision["no_go_for_physical_world_action"] is True
    assert decision["no_go_for_approval_enforcement_execution_or_audit_persistence"] is True


def test_phase_four_four_fixture_and_safety_gates_remain_non_runtime() -> None:
    phase_four_four = _load_json(PHASE_4_4_FIXTURE_PATH)
    assert phase_four_four["non_runtime"] is True
    for record in phase_four_four["fixture_records"]:
        assert record["synthetic"] is True
        assert record["non_runtime"] is True
    assert PHASE_4_8_GATE_DOC_PATH.exists()
    assert PHASE_4_12_GATE_DOC_PATH.exists()
    assert "not runtime wiring" in PHASE_4_8_GATE_DOC_PATH.read_text(encoding="utf-8")
    assert "not runtime wiring" in PHASE_4_12_GATE_DOC_PATH.read_text(encoding="utf-8")


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


def test_no_phase_four_thirteen_runtime_modules_live_adapters_or_harness_were_added() -> None:
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
