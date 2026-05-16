"""Read-only runtime state inspection implementation tests for Phase 30.2."""

from __future__ import annotations

import ast
import copy
import json
from pathlib import Path
from typing import Any

from lima.kernel import RuntimeStateSnapshot, inspect_runtime_state

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_30_2_READ_ONLY_RUNTIME_STATE_INSPECTION_IMPLEMENTATION.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_30_2_read_only_runtime_state_inspection_implementation.json"
)
CASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_30_2_read_only_runtime_state_inspection_cases.json"
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


def test_phase_30_2_metadata_records_only_approved_runtime_files() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "30.2"
    assert fixture["runtime_code_modified"] is True
    assert fixture["runtime_files_changed"] == [
        "lima/kernel/runtime_state.py",
        "lima/kernel/__init__.py",
    ]
    assert fixture["runtime_state_py_added"] is True
    assert fixture["kernel_init_changed_for_safe_export"] is True
    assert fixture["forbidden_runtime_files_changed"] is False
    assert fixture["tests_support_changed"] is False


def test_runtime_state_snapshot_is_frozen_and_exported() -> None:
    snapshot = RuntimeStateSnapshot(
        inspection_state="blocked",
        candidate_present=False,
        candidate_status="blocked",
        status_reason="test",
        provenance_present=False,
        provenance_state="invalid",
        provenance_keys=(),
    )
    assert snapshot.to_dict()["read_only"] is True
    assert inspect_runtime_state()["candidate_status"] == "blocked"


def test_inspection_is_deterministic_and_does_not_mutate_input() -> None:
    candidate = _load_json(CASE_FIXTURE_PATH)["cases"][0]["candidate_state"]
    before = copy.deepcopy(candidate)
    first = inspect_runtime_state(candidate)
    second = inspect_runtime_state(candidate)
    assert first == second
    assert candidate == before
    assert first["candidate_status"] == "proposed"
    assert first["inspection_state"] == "valid"
    assert first["provenance_keys"] == ("fixture", "lineage_seed")
    _assert_safe_snapshot(first)


def test_missing_and_malformed_input_are_safe_by_default() -> None:
    for value in (None, "not-a-mapping", ["not", "mapping"]):
        snapshot = inspect_runtime_state(value)  # type: ignore[arg-type]
        assert snapshot["inspection_state"] == "invalid"
        assert snapshot["candidate_status"] == "blocked"
        assert snapshot["status_reason"] == "missing_or_invalid_candidate_state"
        _assert_safe_snapshot(snapshot)


def test_fixture_cases_preserve_safe_runtime_state_outcomes() -> None:
    for case in _load_json(CASE_FIXTURE_PATH)["cases"]:
        snapshot = inspect_runtime_state(case["candidate_state"])
        assert snapshot["candidate_status"] == case["expected_status"]
        assert snapshot["inspection_state"] == case["expected_inspection_state"]
        _assert_safe_snapshot(snapshot)


def test_unknown_values_and_bypass_wording_do_not_enable_authority() -> None:
    unknown = inspect_runtime_state(
        {
            "candidate_status": "run_now",
            "approval_state": "approved",
            "execution_allowed": True,
            "side_effects_allowed": True,
            "approved": True,
            "dispatch_allowed": True,
            "persistence_allowed": True,
            "provenance": {"claim": "operator trusted override approve emergency"},
        }
    )
    assert unknown["candidate_status"] == "blocked"
    assert unknown["status_reason"] == "execution_not_allowed_for_runtime_state_inspection"
    _assert_safe_snapshot(unknown)


def test_runtime_state_module_has_no_forbidden_imports_or_calls() -> None:
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
    forbidden_calls = {
        "eval",
        "exec",
        "open",
        "print",
        "__import__",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".")[0] not in forbidden_imports
        if isinstance(node, ast.ImportFrom) and node.module:
            assert node.module.split(".")[0] not in forbidden_imports
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            assert node.func.id not in forbidden_calls


def test_phase_document_preserves_no_bridge_no_execution_scope() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "does not modify `lima/kernel/intake_candidate.py`" in phase_doc
    assert "does not modify `lima/kernel/candidate_status.py`" in phase_doc
    assert "does not add a HumanInput runtime bridge" in phase_doc
    assert "does not approve, execute, dispatch, persist audit" in phase_doc
