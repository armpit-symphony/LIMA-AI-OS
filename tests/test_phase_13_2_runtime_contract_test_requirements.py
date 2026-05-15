"""Static checks for Phase 13.2 runtime contract test requirements."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_13_2_RUNTIME_CONTRACT_TEST_REQUIREMENTS.md"
PHASE_FIXTURE_PATH = REPO_ROOT / "tests" / "fixtures" / "runtime_extraction" / "phase_13_2_runtime_contract_test_requirements.json"


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_is_requirements_only() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "13.2"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_code_modified"] is False
    assert fixture["contract_test_code_added"] is False


def test_contract_requirements_cover_non_executing_invariants() -> None:
    requirements = set(_load_json(PHASE_FIXTURE_PATH)["future_contract_requirements"])
    for expected in {
        "execution_allowed_always_false",
        "side_effects_allowed_always_false",
        "approval_state_never_approved",
        "approved_flag_never_true",
        "provenance_preserved",
        "malformed_candidate_safe",
        "unknown_status_safe",
        "stale_or_replayed_safe",
        "operator_admin_phil_trusted_no_bypass",
        "phase_5_runtime_bridge_remains_gated",
        "no_intent_envelope_or_guardian_decision_created",
    }:
        assert expected in requirements


def test_phase_document_blocks_runtime_changes() -> None:
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "does not modify `lima/`" in phase_doc
    assert "does not modify `tests/support/`" in phase_doc
    assert "does not add contract-test implementation code" in phase_doc
    assert "These are requirements for future tests, not new runtime behavior" in phase_doc


def test_boundary_results_show_no_forbidden_changes() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["boundary_results"]
    assert boundary["lima_modified"] is False
    assert boundary["tests_support_modified"] is False
    assert boundary["runtime_behavior_changed"] is False
    assert boundary["contract_test_code_added"] is False
    assert boundary["sparkbot_imported_or_wired"] is False
    assert boundary["humaninput_runtime_bridge_added"] is False
    assert boundary["approval_enforcement_added"] is False
    assert boundary["execution_added"] is False
    assert boundary["dispatch_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False


def test_next_phase_is_fixture_matrix() -> None:
    assert _load_json(PHASE_FIXTURE_PATH)["next_phase"] == "phase_13_3_threat_fixture_matrix"


def test_no_phase_thirteen_two_files_exist_under_lima_or_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_13_2*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_13_2*"))
