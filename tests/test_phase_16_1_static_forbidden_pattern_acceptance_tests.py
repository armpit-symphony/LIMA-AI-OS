"""Static forbidden-pattern acceptance checks for Phase 16.1."""

from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_16_1_STATIC_FORBIDDEN_PATTERN_ACCEPTANCE_TESTS.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_16_1_static_forbidden_pattern_acceptance_tests.json"
)
RUNTIME_FILES = (
    REPO_ROOT / "lima" / "kernel" / "intake_candidate.py",
    REPO_ROOT / "lima" / "kernel" / "candidate_status.py",
    REPO_ROOT / "lima" / "kernel" / "__init__.py",
)
FORBIDDEN_IMPORT_ROOTS = {
    "sparkbot",
    "app",
    "apps",
    "adapters",
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
    "open",
    "exec",
    "eval",
    "compile",
    "dispatch",
    "execute",
    "approve",
    "enforce",
    "persist",
    "write",
    "unlink",
    "remove",
    "rmdir",
    "mkdir",
    "replace",
    "rename",
    "start",
    "Thread",
    "Process",
}
FORBIDDEN_MODULE_CALL_ROOTS = {
    "subprocess",
    "os",
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


def test_phase_metadata_describes_static_acceptance_scope() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "16.1"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False
    assert set(fixture["scanned_runtime_files"]) == {
        "lima/kernel/intake_candidate.py",
        "lima/kernel/candidate_status.py",
        "lima/kernel/__init__.py",
    }


def test_runtime_files_have_no_forbidden_imports() -> None:
    offenders: list[str] = []
    for path in RUNTIME_FILES:
        for node in ast.walk(_module(path)):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    root = alias.name.split(".", 1)[0]
                    if root in FORBIDDEN_IMPORT_ROOTS:
                        offenders.append(f"{path.name}:{alias.name}")
            elif isinstance(node, ast.ImportFrom) and node.module:
                root = node.module.split(".", 1)[0]
                if root in FORBIDDEN_IMPORT_ROOTS:
                    offenders.append(f"{path.name}:{node.module}")
    assert offenders == []


def test_runtime_files_have_no_forbidden_side_effect_calls() -> None:
    offenders: list[str] = []
    for path in RUNTIME_FILES:
        for node in ast.walk(_module(path)):
            if isinstance(node, ast.Call):
                name = _call_name(node)
                root = _call_root(node)
                if name in FORBIDDEN_CALL_NAMES or root in FORBIDDEN_MODULE_CALL_ROOTS:
                    offenders.append(f"{path.name}:{root}.{name}".strip("."))
    assert offenders == []


def test_runtime_files_do_not_assign_authority_true_values() -> None:
    offenders: list[str] = []
    authority_names = {"execution_allowed", "side_effects_allowed", "approved", "executable"}
    for path in RUNTIME_FILES:
        for node in ast.walk(_module(path)):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id in authority_names:
                        if isinstance(node.value, ast.Constant) and node.value.value is True:
                            offenders.append(f"{path.name}:{target.id}=True")
            if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                if node.target.id in authority_names and isinstance(node.value, ast.Constant):
                    if node.value.value is True:
                        offenders.append(f"{path.name}:{node.target.id}=True")
    assert offenders == []


def test_runtime_files_do_not_create_approved_approval_state() -> None:
    offenders: list[str] = []
    for path in RUNTIME_FILES:
        for node in ast.walk(_module(path)):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    is_approval_state = isinstance(target, ast.Name) and target.id == "approval_state"
                    if is_approval_state and isinstance(node.value, ast.Constant):
                        if str(node.value.value).lower() == "approved":
                            offenders.append(f"{path.name}:approval_state='approved'")
    assert offenders == []


def test_phase_document_and_fixture_block_forbidden_scope() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert fixture["static_checker_scope"]["no_production_scanner_added"] is True
    assert fixture["static_checker_scope"]["no_runtime_import_execution"] is True
    assert fixture["static_checker_scope"]["no_subprocess"] is True
    assert fixture["static_checker_scope"]["no_network"] is True
    assert fixture["boundary_results"]["phase_5_runtime_bridge_remains_gated"] is True


def test_no_phase_sixteen_one_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_16_1*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_16_1*"))
