"""Static checks for Phase 4.12 test-only HumanInput adapter harness safety gate docs."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_4_12_TEST_ONLY_HUMANINPUT_ADAPTER_HARNESS_SAFETY_GATE_DOCS.md"
)
GATE_DOC_PATH = REPO_ROOT / "docs" / "TEST_ONLY_HUMANINPUT_ADAPTER_HARNESS_SAFETY_GATE.md"
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_4_12_test_only_humaninput_adapter_harness_safety_gate_docs.json"
)

REQUIRED_RULES = {
    "harness_input_is_synthetic_only",
    "harness_output_is_validation_result_metadata_only",
    "harness_validates_humaninput_shape_only",
    "harness_does_not_create_humaninput_from_live_sources",
    "harness_does_not_create_intentenvelope",
    "harness_does_not_create_guardiandecision",
    "harness_does_not_call_models",
    "harness_does_not_call_tools",
    "harness_does_not_write_terminal_or_pty_input",
    "harness_does_not_call_robots_or_physical_world_drivers",
    "harness_does_not_perform_live_trust_auth_or_session_lookup",
    "harness_does_not_approve_enforce_execute_or_persist_audit_data",
    "harness_does_not_imply_production_adapter_readiness",
}

REQUIRED_BLOCKERS = {
    "files_under_lima_before_explicit_implementation_approval",
    "live_adapter_implementation",
    "production_adapter_implementation",
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


def test_fixture_is_valid_phase_four_twelve_non_runtime_safety_gate_docs() -> None:
    fixture = _load_fixture()
    assert fixture["phase"] == "4.12"
    assert fixture["status"] == "non_runtime_test_only_humaninput_adapter_harness_safety_gate_docs"
    assert fixture["non_runtime"] is True
    assert fixture["docs_tests_fixtures_only"] is True


def test_docs_exist_and_state_gate_is_not_runtime_or_sparkbot_integration() -> None:
    assert PHASE_DOC_PATH.exists()
    assert GATE_DOC_PATH.exists()
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    gate_doc = GATE_DOC_PATH.read_text(encoding="utf-8")
    assert "not harness implementation" in phase_doc
    assert "not Sparkbot integration" in gate_doc
    assert "cannot imply production adapter readiness" in phase_doc
    assert "cannot prove live adapter safety" in gate_doc


def test_phase_four_eleven_source_is_recorded() -> None:
    fixture = _load_fixture()
    assert fixture["source_phase"] == "4.11"
    assert fixture["source_tag"] == (
        "phase-4.11-test-only-humaninput-adapter-harness-proposal-readiness-review"
    )
    assert fixture["source_merge_commit"] == "f1442326a9290c70b341c177d876fc68de87091b"


def test_gate_is_metadata_only_and_not_runtime_or_harness_code() -> None:
    fixture = _load_fixture()
    assert fixture["key_rule"] == (
        "test_only_humaninput_adapter_harness_safety_gate_docs_are_not_harness_implementation"
    )
    assert all(fixture["gate_is"].values())
    assert all(fixture["gate_is_not"].values())


def test_required_harness_rules_block_runtime_and_authority_paths() -> None:
    rules = _load_fixture()["required_harness_rules"]
    assert REQUIRED_RULES == set(rules)
    assert all(rules.values())


def test_required_blockers_cover_live_runtime_sparkbot_and_physical_paths() -> None:
    assert REQUIRED_BLOCKERS <= set(_load_fixture()["required_blockers"])


def test_production_readiness_warning_is_explicit() -> None:
    warning = _load_fixture()["production_readiness_warning"]
    assert all(warning.values())
    assert warning["does_not_prove_live_adapter_safety"] is True
    assert warning["does_not_prove_sparkbot_integration_safety"] is True
    assert warning["does_not_prove_runtime_wiring_safety"] is True
    assert warning["does_not_prove_physical_world_safety"] is True


def test_ready_for_is_limited_to_phase_four_thirteen_readiness_review() -> None:
    assert set(_load_fixture()["ready_for"]) == {
        "phase_4_13_phase_4_humaninput_boundary_readiness_review",
        "further_non_runtime_review",
    }


def test_decision_allows_only_phase_four_thirteen_review_next() -> None:
    decision = _load_fixture()["decision"]
    assert decision["conditional_go_for_phase_4_13_humaninput_boundary_readiness_review"] is True
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


def test_no_phase_four_twelve_runtime_modules_live_adapters_or_harness_were_added() -> None:
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
