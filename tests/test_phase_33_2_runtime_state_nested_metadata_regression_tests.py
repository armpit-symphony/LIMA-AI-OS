"""Runtime state nested metadata regression tests for Phase 33.2."""

from __future__ import annotations

import ast
import copy
import json
from pathlib import Path
from typing import Any

from lima.kernel import inspect_runtime_state

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_33_2_RUNTIME_STATE_NESTED_METADATA_REGRESSION_TESTS.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_33_2_runtime_state_nested_metadata_regression_tests.json"
)
CASES_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_33_1_nested_suspicious_metadata_cases.json"
)
RUNTIME_STATE_PATH = REPO_ROOT / "lima" / "kernel" / "runtime_state.py"


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def _assert_safe_snapshot(snapshot: dict[str, Any]) -> None:
    assert snapshot["non_authoritative"] is True
    assert snapshot["advisory_only"] is True
    assert snapshot["read_only"] is True
    assert snapshot["deterministic"] is True
    assert snapshot["local_only"] is True
    assert snapshot["executable"] is False
    assert snapshot["execution_allowed"] is False
    assert snapshot["side_effects_allowed"] is False
    assert snapshot["approved"] is False
    assert snapshot["approval_state"] != "approved"
    assert snapshot["dispatch_allowed"] is False
    assert snapshot["persistence_allowed"] is False
    assert snapshot["phase_5_humaninput_runtime_bridge_gated"] is True
    assert snapshot["humaninput_runtime_bridge_present"] is False
    assert snapshot["sparkbot_wiring_present"] is False
    assert snapshot["live_adapter_present"] is False
    assert snapshot["intent_envelope_created"] is False
    assert snapshot["guardian_decision_created"] is False


def test_phase_33_2_is_test_only_runtime_state_hardening() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert fixture["phase"] == "33.2"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_implementation_approved"] is False
    assert fixture["runtime_files_changed"] == []
    assert fixture["tests_support_changed"] is False
    assert "does not implement runtime behavior" in phase_doc


def test_nested_metadata_cases_match_expected_runtime_state_outcomes() -> None:
    for case in _load_json(CASES_FIXTURE_PATH)["cases"]:
        candidate = case["candidate_state"]
        before = copy.deepcopy(candidate)
        first = inspect_runtime_state(candidate)
        second = inspect_runtime_state(candidate)
        assert first == second
        assert candidate == before
        assert first["candidate_status"] == case["expected_status"]
        assert first["inspection_state"] == case["expected_inspection_state"]
        assert first["status_reason"] == case["expected_reason"]
        _assert_safe_snapshot(first)


def test_nested_bypass_wording_blocks_without_creating_authority() -> None:
    cases = {
        case["id"]: case["candidate_state"]
        for case in _load_json(CASES_FIXTURE_PATH)["cases"]
    }
    for case_id in ("deep_authority_wording", "bridge_adapter_and_sparkbot_claims"):
        snapshot = inspect_runtime_state(cases[case_id])
        assert snapshot["candidate_status"] == "blocked"
        assert snapshot["status_reason"] == "authority_claim_not_allowed_for_runtime_state_inspection"
        _assert_safe_snapshot(snapshot)


def test_external_and_physical_world_claims_remain_inert_caller_data() -> None:
    cases = {
        case["id"]: case["candidate_state"]
        for case in _load_json(CASES_FIXTURE_PATH)["cases"]
    }
    snapshot = inspect_runtime_state(cases["external_action_claims"])
    assert snapshot["candidate_status"] == "proposed"
    assert snapshot["status_reason"] == "read_only_runtime_state_snapshot"
    _assert_safe_snapshot(snapshot)


def test_unknown_and_malformed_nested_metadata_remain_safe() -> None:
    cases = {
        case["id"]: case["candidate_state"]
        for case in _load_json(CASES_FIXTURE_PATH)["cases"]
    }
    malformed = inspect_runtime_state(cases["malformed_top_level_provenance_value"])
    assert malformed["candidate_status"] == "blocked"
    assert malformed["provenance_state"] == "invalid"
    _assert_safe_snapshot(malformed)

    unknown_nested = inspect_runtime_state(cases["unknown_nested_values"])
    assert unknown_nested["candidate_status"] == "proposed"
    assert unknown_nested["provenance_state"] == "valid"
    _assert_safe_snapshot(unknown_nested)

    unknown_status = inspect_runtime_state(cases["unknown_top_level_candidate_status"])
    assert unknown_status["candidate_status"] == "blocked"
    assert unknown_status["status_reason"] == "unknown_candidate_status_not_execution_ready"
    _assert_safe_snapshot(unknown_status)


def test_phase_33_2_regression_coverage_is_recorded() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    coverage = set(fixture["regression_coverage"])
    assert "nested_suspicious_metadata_does_not_enable_execution" in coverage
    assert "nested_suspicious_metadata_does_not_enable_side_effects" in coverage
    assert "bridge_adapter_and_sparkbot_claims_remain_inert" in coverage
    assert "robotics_physical_world_claims_remain_inert" in coverage
    assert "inspection_is_deterministic_and_non_mutating" in coverage
    assert fixture["runtime_state_gap_found"] is False


def test_runtime_state_module_still_has_no_forbidden_imports_or_calls() -> None:
    tree = ast.parse(RUNTIME_STATE_PATH.read_text(encoding="utf-8"))
    forbidden_imports = {
        "asyncio",
        "http",
        "logging",
        "multiprocessing",
        "os",
        "pathlib",
        "queue",
        "random",
        "requests",
        "socket",
        "sqlite3",
        "subprocess",
        "sys",
        "threading",
        "time",
        "urllib",
        "webbrowser",
    }
    forbidden_calls = {"eval", "exec", "open", "print", "__import__"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".")[0] not in forbidden_imports
        if isinstance(node, ast.ImportFrom) and node.module:
            assert node.module.split(".")[0] not in forbidden_imports
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            assert node.func.id not in forbidden_calls


def test_no_phase_33_2_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_33_2*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_33_2*"))
