"""Static checks for Phase 16.4 test-only acceptance readiness review."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_16_4_TEST_ONLY_ACCEPTANCE_IMPLEMENTATION_READINESS_REVIEW.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_16_4_test_only_acceptance_implementation_readiness_review.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_readiness_review_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "16.4"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False


def test_reviewed_implementation_lists_acceptance_test_phases() -> None:
    reviewed = set(_load_json(PHASE_FIXTURE_PATH)["reviewed_implementation"])
    assert reviewed == {
        "phase_16_1_static_forbidden_pattern_acceptance_tests",
        "phase_16_2_runtime_contract_acceptance_tests",
        "phase_16_3_threat_fixture_acceptance_tests",
    }


def test_readiness_findings_keep_gate_test_only() -> None:
    findings = _load_json(PHASE_FIXTURE_PATH)["readiness_findings"]
    assert findings["acceptance_gate_remains_test_only"] is True
    assert findings["runtime_behavior_added"] is False
    assert findings["lima_files_touched"] is False
    assert findings["tests_support_files_touched"] is False
    assert findings["synthetic_fixtures_only"] is True
    assert findings["phase_5_humaninput_runtime_bridge_remains_gated"] is True
    assert findings["ready_for_phase_16_5_archive_closeout"] is True


def test_not_ready_for_runtime_or_integration() -> None:
    not_ready = set(_load_json(PHASE_FIXTURE_PATH)["not_ready_for"])
    assert "runtime_implementation" in not_ready
    assert "sparkbot_wiring" in not_ready
    assert "humaninput_runtime_bridge_behavior" in not_ready
    assert "live_adapters" in not_ready
    assert "approval_enforcement" in not_ready
    assert "execution" in not_ready
    assert "dispatch" in not_ready
    assert "audit_persistence" in not_ready
    assert "physical_world_behavior" in not_ready


def test_phase_document_preserves_forbidden_scope() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "The acceptance gate remains test-only" in phase_doc
    assert "The gate adds no runtime behavior" in phase_doc


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["helper_behavior_changed"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["humaninput_runtime_bridge_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False
    assert boundary["phase_5_runtime_bridge_remains_gated"] is True


def test_no_phase_sixteen_four_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_16_4*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_16_4*"))
