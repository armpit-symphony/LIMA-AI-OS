"""Static checks for Phase 17.1 acceptance-test coverage review."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_17_1_ACCEPTANCE_TEST_COVERAGE_REVIEW.md"
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_17_1_acceptance_test_coverage_review.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_coverage_review_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "17.1"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False


def test_coverage_review_maps_phase_sixteen_test_groups() -> None:
    review = _load_json(PHASE_FIXTURE_PATH)["coverage_review"]
    assert review["static_forbidden_pattern_tests"]["phase"] == "16.1"
    assert review["runtime_contract_tests"]["phase"] == "16.2"
    assert review["threat_fixture_tests"]["phase"] == "16.3"
    assert "forbidden_imports" in review["static_forbidden_pattern_tests"]["coverage"]
    assert "approval_state_never_approved" in review["runtime_contract_tests"]["coverage"]
    assert "humaninput_bridge_attempt" in review["threat_fixture_tests"]["coverage"]


def test_coverage_conclusion_does_not_approve_runtime_expansion() -> None:
    conclusion = _load_json(PHASE_FIXTURE_PATH)["coverage_conclusion"]
    assert conclusion["phase_16_strengthens_gate"] is True
    assert conclusion["runtime_expansion_approved"] is False
    assert conclusion["sparkbot_wiring_approved"] is False
    assert conclusion["humaninput_runtime_bridge_approved"] is False
    assert conclusion["execution_or_dispatch_approved"] is False
    assert conclusion["approval_enforcement_or_audit_persistence_approved"] is False
    assert conclusion["physical_world_behavior_approved"] is False


def test_static_limitations_are_explicit() -> None:
    limitations = set(_load_json(PHASE_FIXTURE_PATH)["static_limitations"])
    assert "explicit_runtime_file_scope_only" in limitations
    assert "existing_non_executing_api_scope_only" in limitations
    assert "synthetic_inert_fixture_scope_only" in limitations
    assert "not_live_safety_monitoring" in limitations


def test_phase_document_keeps_forbidden_scope_blocked() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "does not change runtime behavior" in phase_doc
    assert "not a runtime implementation approval" in phase_doc
    assert "Phase 17.2 should review remaining safety gaps" in phase_doc


def test_no_phase_seventeen_one_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_17_1*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_17_1*"))
