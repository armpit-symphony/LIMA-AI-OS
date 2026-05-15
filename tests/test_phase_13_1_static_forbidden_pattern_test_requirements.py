"""Static checks for Phase 13.1 forbidden-pattern requirements."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_13_1_STATIC_FORBIDDEN_PATTERN_TEST_REQUIREMENTS.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_13_1_static_forbidden_pattern_test_requirements.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_requirements_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "13.1"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False
    assert fixture["boundary_results"]["static_test_code_added"] is False


def test_forbidden_import_requirements_cover_side_effect_surfaces() -> None:
    imports = set(_load_json(PHASE_FIXTURE_PATH)["future_static_check_requirements"]["forbidden_imports"])
    for expected in {"subprocess", "socket", "requests", "urllib", "httpx", "webbrowser", "threading", "multiprocessing"}:
        assert expected in imports
    assert "sparkbot_modules" in imports
    assert "live_adapter_modules" in imports


def test_forbidden_call_requirements_cover_execution_dispatch_persistence() -> None:
    calls = set(_load_json(PHASE_FIXTURE_PATH)["future_static_check_requirements"]["forbidden_calls"])
    for expected in {"system", "popen", "Popen", "open", "write", "dispatch", "execute", "approve", "persist"}:
        assert expected in calls


def test_forbidden_boundary_names_cover_blocked_runtime_domains() -> None:
    names = set(_load_json(PHASE_FIXTURE_PATH)["future_static_check_requirements"]["forbidden_boundary_names"])
    assert "HumanInputBridge" in names
    assert "IntentCompiler" in names
    assert "GuardianDecision" in names
    assert "Sparkbot" in names
    assert "RoboOSDriver" in names
    assert "ApprovalEnforcer" in names
    assert "AuditWriter" in names


def test_static_checks_are_not_claimed_sufficient_alone() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["static_checks_are_sufficient_alone"] is False
    assert fixture["next_phase"] == "phase_13_2_runtime_contract_test_requirements"


def test_phase_document_blocks_runtime_and_test_support_changes() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "does not add static-test implementation code" in phase_doc
    assert "Static checks are necessary but not sufficient" in phase_doc


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["humaninput_runtime_bridge_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True


def test_no_phase_thirteen_one_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_13_1*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_13_1*"))
