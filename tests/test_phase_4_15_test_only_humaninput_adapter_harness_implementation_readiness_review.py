"""Static checks for Phase 4.15 HumanInput harness readiness review."""

from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_4_15_TEST_ONLY_HUMANINPUT_ADAPTER_HARNESS_IMPLEMENTATION_READINESS_REVIEW.md"
)
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_4_15_test_only_humaninput_adapter_harness_implementation_readiness_review.json"
)
PHASE_4_14_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_4_14_test_only_humaninput_adapter_harness.json"
)
HARNESS_PATH = REPO_ROOT / "tests" / "support" / "test_only_humaninput_adapter_harness.py"

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

EXPECTED_READY_FOR = {
    "phase_4_16_humaninput_boundary_lane_closeout_review",
    "further_non_runtime_review",
}

REQUIRED_NOT_READY_FOR = {
    "live_adapter_code",
    "runtime_wiring",
    "production_sparkbot_integration",
    "sparkbot_import_or_wiring",
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


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_fixture_is_valid_phase_four_fifteen_readiness_review() -> None:
    fixture = _load_json(FIXTURE_PATH)
    assert fixture["phase"] == "4.15"
    assert fixture["status"] == (
        "non_runtime_test_only_humaninput_adapter_harness_implementation_readiness_review"
    )
    assert fixture["non_runtime"] is True
    assert fixture["docs_tests_fixtures_only"] is True


def test_doc_exists_and_states_review_adds_no_harness_behavior() -> None:
    assert PHASE_DOC_PATH.exists()
    phase_doc = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "does not add harness behavior" in phase_doc
    assert "runtime code" in phase_doc
    assert "NO-GO for live adapter code" in phase_doc


def test_phase_fourteen_source_is_recorded() -> None:
    fixture = _load_json(FIXTURE_PATH)
    assert fixture["source_phase"] == "4.14"
    assert fixture["source_tag"] == "phase-4.14-test-only-humaninput-adapter-harness-implementation"
    assert fixture["source_merge_commit"] == "1870157a9d1d1dffdf7cb99c8e822cde5d4a9927"


def test_phase_fourteen_harness_fixture_remains_test_only_non_runtime() -> None:
    fixture = _load_json(PHASE_4_14_FIXTURE_PATH)
    assert fixture["test_only"] is True
    assert fixture["non_runtime"] is True
    assert fixture["boundary_results"]["test_only_adapter_harness_added_under_tests"] is True
    assert fixture["boundary_results"]["files_under_lima_modified"] is False


def test_review_is_metadata_only_and_not_runtime_or_new_harness_behavior() -> None:
    fixture = _load_json(FIXTURE_PATH)
    assert fixture["key_rule"] == "readiness_review_is_not_new_harness_behavior"
    assert all(fixture["review_is"].values())
    assert all(fixture["review_is_not"].values())


def test_readiness_findings_confirm_harness_constraints() -> None:
    findings = _load_json(FIXTURE_PATH)["readiness_findings"]
    assert all(findings.values())
    assert findings["harness_lives_under_tests_support"] is True
    assert findings["harness_is_deterministic"] is True
    assert findings["harness_is_synthetic_only"] is True
    assert findings["harness_outputs_are_humaninput_shape_only"] is True
    assert findings["harness_does_not_import_lima_runtime_modules"] is True
    assert findings["harness_does_not_import_sparkbot_modules"] is True


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


def test_harness_source_has_no_external_side_effect_primitives() -> None:
    source = HARNESS_PATH.read_text(encoding="utf-8").lower()
    forbidden_tokens = {
        "subprocess.",
        "socket.",
        "requests.",
        "urllib.",
        "http.client",
        "openai",
        "execute_tool(",
        "stream_chat_with_tools(",
    }
    assert not any(token in source for token in forbidden_tokens)


def test_ready_for_is_limited_to_phase_four_sixteen_or_review() -> None:
    assert set(_load_json(FIXTURE_PATH)["ready_for"]) == EXPECTED_READY_FOR


def test_not_ready_for_blocks_live_runtime_authority_and_physical_paths() -> None:
    assert REQUIRED_NOT_READY_FOR <= set(_load_json(FIXTURE_PATH)["not_ready_for"])


def test_decision_only_allows_phase_four_sixteen_closeout_review_next() -> None:
    decision = _load_json(FIXTURE_PATH)["decision"]
    assert decision["conditional_go_for_phase_4_16_humaninput_boundary_lane_closeout_review"] is True
    assert decision["go_for_further_non_runtime_review"] is True
    assert decision["no_go_for_live_adapter_implementation"] is True
    assert decision["no_go_for_runtime_extraction_implementation"] is True
    assert decision["no_go_for_sparkbot_integration"] is True
    assert decision["no_go_for_physical_world_action"] is True


def test_boundary_results_show_review_added_no_runtime_or_blocked_behavior() -> None:
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


def test_no_phase_four_fifteen_lima_or_forbidden_harness_paths_exist() -> None:
    forbidden_paths = [
        REPO_ROOT / "lima" / "adapters" / "humaninput_adapter.py",
        REPO_ROOT / "lima" / "adapters" / "sparkbot_humaninput_live.py",
        REPO_ROOT / "lima" / "runtime_extraction.py",
        REPO_ROOT / "tests" / "helpers" / "test_only_humaninput_adapter_harness.py",
    ]
    assert not any(path.exists() for path in forbidden_paths)
