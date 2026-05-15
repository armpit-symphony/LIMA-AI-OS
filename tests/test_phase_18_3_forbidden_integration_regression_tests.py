"""Forbidden integration regression checks for existing candidate runtime files."""

from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_18_3_FORBIDDEN_INTEGRATION_REGRESSION_TESTS.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_18_3_forbidden_integration_regression_tests.json"
)
RUNTIME_FILES = (
    REPO_ROOT / "lima" / "kernel" / "intake_candidate.py",
    REPO_ROOT / "lima" / "kernel" / "candidate_status.py",
    REPO_ROOT / "lima" / "kernel" / "__init__.py",
)

FORBIDDEN_IMPORT_ROOTS = {
    "sparkbot",
    "humaninput",
    "intentcompiler",
    "guardiandecision",
    "subprocess",
    "socket",
    "requests",
    "urllib",
    "http",
    "webbrowser",
    "selenium",
    "playwright",
    "threading",
    "multiprocessing",
    "queue",
    "sqlite3",
}
FORBIDDEN_CALL_NAMES = {
    "approve",
    "dispatch",
    "enforce",
    "eval",
    "exec",
    "execute",
    "open",
    "persist",
    "remove",
    "rename",
    "replace",
    "rmdir",
    "start",
    "unlink",
    "write",
}
FORBIDDEN_MODULE_CALL_ROOTS = {
    "os",
    "subprocess",
    "socket",
    "requests",
    "urllib",
    "http",
    "webbrowser",
    "selenium",
    "playwright",
    "threading",
    "multiprocessing",
    "queue",
    "sqlite3",
}
FORBIDDEN_BOUNDARY_TEXT = {
    "sparkbot",
    "live_adapter",
    "approval_enforcement",
    "audit_persistence",
    "physical_world_action",
}


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def _module(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def _call_name(node: ast.Call) -> str:
    func = node.func
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return ""


def _call_root(node: ast.Call) -> str:
    func = node.func
    while isinstance(func, ast.Attribute):
        func = func.value
    if isinstance(func, ast.Name):
        return func.id
    return ""


def test_phase_metadata_scans_only_candidate_runtime_files() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "18.3"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False
    assert set(fixture["scanned_runtime_files"]) == {
        "lima/kernel/intake_candidate.py",
        "lima/kernel/candidate_status.py",
        "lima/kernel/__init__.py",
    }


def test_candidate_runtime_files_have_no_forbidden_imports() -> None:
    offenders: list[str] = []
    for path in RUNTIME_FILES:
        for node in ast.walk(_module(path)):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    root = alias.name.split(".", 1)[0].lower()
                    if root in FORBIDDEN_IMPORT_ROOTS:
                        offenders.append(f"{path.name}:{alias.name}")
            elif isinstance(node, ast.ImportFrom) and node.module:
                root = node.module.split(".", 1)[0].lower()
                if root in FORBIDDEN_IMPORT_ROOTS:
                    offenders.append(f"{path.name}:{node.module}")
    assert offenders == []


def test_candidate_runtime_files_have_no_forbidden_calls() -> None:
    offenders: list[str] = []
    for path in RUNTIME_FILES:
        for node in ast.walk(_module(path)):
            if isinstance(node, ast.Call):
                name = _call_name(node)
                root = _call_root(node)
                if name in FORBIDDEN_CALL_NAMES or root in FORBIDDEN_MODULE_CALL_ROOTS:
                    offenders.append(f"{path.name}:{root}.{name}".strip("."))
    assert offenders == []


def test_candidate_runtime_files_do_not_name_forbidden_integrations() -> None:
    offenders: list[str] = []
    for path in RUNTIME_FILES:
        source = path.read_text(encoding="utf-8").lower()
        for forbidden in FORBIDDEN_BOUNDARY_TEXT:
            if forbidden in source:
                offenders.append(f"{path.name}:{forbidden}")
    assert offenders == []


def test_static_checker_does_not_add_runtime_or_support_helpers() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    scope = fixture["static_checker_scope"]
    assert scope["test_only"] is True
    assert scope["no_tests_support_helper_added"] is True
    assert scope["no_runtime_scanner_added"] is True
    assert scope["no_runtime_enforcement_added"] is True


def test_phase_document_and_fixture_preserve_boundaries() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "not runtime enforcement" in phase_doc
    assert fixture["boundary_results"]["runtime_behavior_changed"] is False
    assert fixture["boundary_results"]["phase_5_runtime_bridge_remains_gated"] is True


def test_no_phase_eighteen_three_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_18_3*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_18_3*"))
