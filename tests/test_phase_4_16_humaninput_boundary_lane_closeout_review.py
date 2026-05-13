"""Static checks for Phase 4.16 HumanInput boundary lane closeout review."""

from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_4_16_HUMANINPUT_BOUNDARY_LANE_CLOSEOUT_REVIEW.md"
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_4_16_humaninput_boundary_lane_closeout_review.json"
)
PHASE_4_14_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_4_14_test_only_humaninput_adapter_harness.json"
)
PHASE_4_15_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_4_15_test_only_humaninput_adapter_harness_implementation_readiness_review.json"
)
HARNESS_PATH = REPO_ROOT / "tests" / "support" / "test_only_humaninput_adapter_harness.py"

EXPECTED_REVIEWED_PHASES = {
    f"phase_4_{phase}"
    for phase in (
        "0_runtime_extraction_readiness_planning",
        "1_sparkbot_runtime_reference_refresh",
        "2_runtime_boundary_candidate_selection",
        "3_boundary_extraction_safety_gate",
        "4_boundary_fixture_contract_extension",
        "5_boundary_readiness_review",
        "6_humaninput_adapter_proposal",
        "7_humaninput_adapter_proposal_readiness_review",
        "8_humaninput_adapter_safety_gate_docs",
        "9_humaninput_adapter_implementation_readiness_review",
        "10_test_only_humaninput_adapter_harness_proposal",
        "11_test_only_harness_proposal_readiness_review",
        "12_test_only_harness_safety_gate_docs",
        "13_humaninput_boundary_readiness_review",
        "14_test_only_humaninput_adapter_harness_implementation",
        "15_test_only_harness_implementation_readiness_review",
    )
}

EXPECTED_READY_FOR = {
    "stop_phase_4_humaninput_boundary_lane",
    "future_explicitly_approved_humaninput_to_intentenvelope_boundary_planning_lane",
    "further_non_runtime_review",
}

REQUIRED_NOT_READY_FOR = {
    "live_adapter_code",
    "runtime_wiring",
    "production_sparkbot_integration",
    "sparkbot_import_or_wiring",
    "humaninput_to_intentenvelope_implementation",
    "real_intentcompiler",
    "real_guardiandecision",
    "approval",
    "approval_enforcement",
    "policy_enforcement",
    "execution",
    "audit_persistence",
    "model_calls",
    "tool_execution",
    "terminal_pty_behavior",
    "robotics_behavior",
    "physical_world_action",
    "live_auth_session_trust_lookup",
    "production_shell_implementation",
}

FORBIDDEN_IMPORT_ROOTS = {
    "lima",
    "sparkbot",
    "requests",
    "urllib",
    "http",
    "socket",
    "subprocess",
    "asyncio",
    "websocket",
}


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_fixture_is_valid_phase_four_sixteen_closeout_review() -> None:
    fixture = _load_json(FIXTURE_PATH)
    assert fixture["phase"] == "4.16"
    assert fixture["status"] == "non_runtime_humaninput_boundary_lane_closeout_review"
    assert fixture["non_runtime"] is True
    assert fixture["docs_tests_fixtures_only"] is True


def test_doc_exists_and_states_closeout_is_not_next_lane_implementation() -> None:
    assert PHASE_DOC_PATH.exists()
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "does not add harness behavior" in phase_doc
    assert "HumanInput to IntentEnvelope boundary planning" in phase_doc
    assert "NO-GO for live adapter code" in phase_doc


def test_phase_fifteen_source_is_recorded() -> None:
    fixture = _load_json(FIXTURE_PATH)
    assert fixture["source_phase"] == "4.15"
    assert fixture["source_tag"] == (
        "phase-4.15-test-only-humaninput-adapter-harness-implementation-readiness-review"
    )
    assert fixture["source_merge_commit"] == "5458123c1dca2a9cf0ef2c59695c48d607497d47"


def test_reviewed_lane_covers_phase_four_zero_through_phase_four_fifteen() -> None:
    assert set(_load_json(FIXTURE_PATH)["reviewed_lane"]) == EXPECTED_REVIEWED_PHASES


def test_review_is_metadata_only_and_not_next_lane_implementation() -> None:
    fixture = _load_json(FIXTURE_PATH)
    assert fixture["key_rule"] == "lane_closeout_is_not_next_lane_implementation"
    assert all(fixture["review_is"].values())
    assert all(fixture["review_is_not"].values())


def test_closeout_findings_confirm_humaninput_lane_can_stop() -> None:
    findings = _load_json(FIXTURE_PATH)["closeout_findings"]
    assert all(findings.values())
    assert findings["humaninput_boundary_selected_and_bounded"] is True
    assert findings["test_only_harness_exists_under_tests_support"] is True
    assert findings["test_only_harness_outputs_humaninput_shape_only"] is True
    assert findings["test_only_harness_does_not_create_intentenvelope"] is True
    assert findings["phase_4_humaninput_lane_can_stop"] is True


def test_phase_fourteen_and_fifteen_artifacts_remain_constrained() -> None:
    phase_fourteen = _load_json(PHASE_4_14_FIXTURE_PATH)
    phase_fifteen = _load_json(PHASE_4_15_FIXTURE_PATH)
    assert phase_fourteen["boundary_results"]["test_only_adapter_harness_added_under_tests"] is True
    assert phase_fourteen["boundary_results"]["files_under_lima_modified"] is False
    assert phase_fifteen["boundary_results"]["new_harness_behavior_added"] is False
    assert phase_fifteen["boundary_results"]["test_only_adapter_harness_remained_under_tests"] is True


def test_harness_imports_still_exclude_runtime_sparkbot_network_and_subprocess() -> None:
    tree = ast.parse(HARNESS_PATH.read_text(encoding="utf-8"))
    imported_roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported_roots.add(alias.name.split(".")[0].lower())
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_roots.add(node.module.split(".")[0].lower())
    assert not (FORBIDDEN_IMPORT_ROOTS & imported_roots)


def test_known_gaps_keep_runtime_and_next_lane_work_unimplemented() -> None:
    gaps = set(_load_json(FIXTURE_PATH)["known_gaps"])
    assert "no_live_humaninput_adapter_exists" in gaps
    assert "no_runtime_extraction_implementation_exists" in gaps
    assert "no_humaninput_to_intentenvelope_planning_lane_is_approved_yet" in gaps
    assert "no_real_intentcompiler_behavior_exists" in gaps
    assert "no_real_guardiandecision_behavior_exists" in gaps


def test_ready_for_is_limited_to_stop_next_planning_proposal_or_review() -> None:
    assert set(_load_json(FIXTURE_PATH)["ready_for"]) == EXPECTED_READY_FOR


def test_not_ready_for_blocks_live_runtime_authority_and_physical_paths() -> None:
    assert REQUIRED_NOT_READY_FOR <= set(_load_json(FIXTURE_PATH)["not_ready_for"])


def test_decision_stops_lane_and_only_proposes_next_planning_lane() -> None:
    decision = _load_json(FIXTURE_PATH)["decision"]
    assert decision["conditional_go_to_stop_humaninput_boundary_lane"] is True
    assert decision[
        "conditional_go_to_propose_humaninput_to_intentenvelope_boundary_planning_lane"
    ] is True
    assert decision["go_for_further_non_runtime_review"] is True
    assert decision["no_go_for_live_adapter_implementation"] is True
    assert decision["no_go_for_runtime_extraction_implementation"] is True
    assert decision["no_go_for_sparkbot_integration"] is True
    assert decision["no_go_for_physical_world_action"] is True


def test_boundary_results_show_no_runtime_blocked_behavior_or_harness_changes() -> None:
    boundary = _load_json(FIXTURE_PATH)["boundary_results"]
    assert boundary["runtime_behavior_added"] is False
    assert boundary["blocked_behavior_added"] is False
    assert boundary["files_under_lima_modified"] is False
    assert boundary["sparkbot_imported"] is False
    assert boundary["sparkbot_wired"] is False
    assert boundary["live_adapter_code_added"] is False
    assert boundary["new_harness_behavior_added"] is False
    assert boundary["test_only_adapter_harness_remained_under_tests"] is True
    assert boundary["real_intentcompiler_added"] is False
    assert boundary["real_guardiandecision_added"] is False
    assert boundary["approval_enforcement_added"] is False
    assert boundary["audit_persistence_added"] is False
    assert boundary["physical_world_action_added"] is False


def test_no_phase_four_sixteen_lima_or_forbidden_runtime_paths_exist() -> None:
    forbidden_paths = [
        REPO_ROOT / "lima" / "adapters" / "humaninput_adapter.py",
        REPO_ROOT / "lima" / "adapters" / "sparkbot_humaninput_live.py",
        REPO_ROOT / "lima" / "intent_compiler.py",
        REPO_ROOT / "lima" / "runtime_extraction.py",
        REPO_ROOT / "tests" / "helpers" / "test_only_humaninput_adapter_harness.py",
    ]
    assert not any(path.exists() for path in forbidden_paths)
