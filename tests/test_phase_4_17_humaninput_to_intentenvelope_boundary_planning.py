"""Static checks for Phase 4.17 HumanInput to IntentEnvelope planning."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_4_17_HUMANINPUT_TO_INTENTENVELOPE_BOUNDARY_PLANNING.md"
)
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_4_17_humaninput_to_intentenvelope_boundary_planning.json"
)

EXPECTED_READY_FOR = {
    "phase_4_18_humaninput_to_intentenvelope_boundary_schema_contract_proposal",
    "further_non_runtime_review",
}

REQUIRED_NOT_READY_FOR = {
    "humaninput_to_intentenvelope_implementation",
    "test_only_bridge_code",
    "runtime_wiring",
    "live_adapter_code",
    "real_intentcompiler",
    "real_guardiandecision",
    "approval",
    "approval_enforcement",
    "execution",
    "audit_persistence",
    "model_calls",
    "tool_execution",
    "terminal_pty_behavior",
    "robotics_behavior",
    "physical_world_action",
    "sparkbot_import_or_wiring",
    "production_shell_implementation",
}


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_fixture_is_valid_phase_four_seventeen_planning() -> None:
    fixture = _load_json(FIXTURE_PATH)
    assert fixture["phase"] == "4.17"
    assert fixture["status"] == "non_runtime_humaninput_to_intentenvelope_boundary_planning"
    assert fixture["non_runtime"] is True
    assert fixture["docs_tests_fixtures_only"] is True


def test_doc_exists_and_states_planning_is_not_implementation() -> None:
    assert PHASE_DOC_PATH.exists()
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "does not implement a bridge" in phase_doc
    assert "No hidden parser" in phase_doc
    assert "Phase 4.18" in phase_doc


def test_phase_sixteen_source_is_recorded() -> None:
    fixture = _load_json(FIXTURE_PATH)
    assert fixture["source_phase"] == "4.16"
    assert fixture["source_tag"] == "phase-4.16-humaninput-boundary-lane-closeout-review"
    assert fixture["source_merge_commit"] == "e69d6813513dad7e709358334d74a2b590e254af"


def test_standing_gate_refs_exist() -> None:
    for ref in _load_json(FIXTURE_PATH)["standing_gate_refs"]:
        assert (REPO_ROOT / ref).exists()


def test_planning_is_not_schema_or_bridge_or_runtime() -> None:
    fixture = _load_json(FIXTURE_PATH)
    assert fixture["key_rule"] == "planning_is_not_schema_or_implementation"
    assert all(fixture["planning_is"].values())
    assert all(fixture["planning_is_not"].values())


def test_required_invariants_preserve_intentenvelope_safety_gate() -> None:
    invariants = _load_json(FIXTURE_PATH)["required_invariants"]
    assert all(invariants.values())
    assert invariants["humaninput_is_not_intentenvelope"] is True
    assert invariants["intentenvelope_is_not_authorization"] is True
    assert invariants["guardiandecision_remains_mandatory"] is True
    assert invariants["raw_text_is_inert"] is True
    assert invariants["no_hidden_parser"] is True


def test_ready_for_is_limited_to_schema_proposal_or_review() -> None:
    assert set(_load_json(FIXTURE_PATH)["ready_for"]) == EXPECTED_READY_FOR


def test_not_ready_for_blocks_implementation_runtime_and_authority_paths() -> None:
    assert REQUIRED_NOT_READY_FOR <= set(_load_json(FIXTURE_PATH)["not_ready_for"])


def test_boundary_results_show_no_runtime_or_blocked_behavior() -> None:
    boundary = _load_json(FIXTURE_PATH)["boundary_results"]
    assert boundary["runtime_behavior_added"] is False
    assert boundary["blocked_behavior_added"] is False
    assert boundary["files_under_lima_modified"] is False
    assert boundary["sparkbot_imported"] is False
    assert boundary["sparkbot_wired"] is False
    assert boundary["live_adapter_code_added"] is False
    assert boundary["test_only_bridge_code_added"] is False
    assert boundary["real_intentcompiler_added"] is False
    assert boundary["real_guardiandecision_added"] is False
    assert boundary["approval_enforcement_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False


def test_no_phase_four_seventeen_runtime_bridge_or_lima_files_exist() -> None:
    forbidden_paths = [
        REPO_ROOT / "lima" / "intent_compiler.py",
        REPO_ROOT / "lima" / "humaninput_to_intentenvelope.py",
        REPO_ROOT / "tests" / "support" / "humaninput_to_intentenvelope_bridge.py",
        REPO_ROOT / "tests" / "helpers" / "humaninput_to_intentenvelope_bridge.py",
    ]
    assert not any(path.exists() for path in forbidden_paths)
