"""Static checks for Phase 4.1 Sparkbot runtime reference refresh."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
REFERENCE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_4_1_SPARKBOT_RUNTIME_REFERENCE_REFRESH.md"
)
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_4_1_sparkbot_runtime_reference_refresh.json"
)

REQUIRED_SURFACES = {
    "chat_websocket_room_surfaces",
    "voice_to_chat_transcription_surface",
    "tool_aware_chat_model_loop",
    "tool_catalogue_and_dispatcher",
    "guardian_policy_decision_surface",
    "guardian_suite_entrypoint",
    "dashboard_approval_execution_surface",
    "breakglass_vault_task_guardian_routes",
    "mcp_registry_explain_plan_and_approval_routes",
    "robotics_bridge_route_and_service",
    "terminal_route_and_pty_manager",
    "workstation_command_center_spine_frontend_surfaces",
}

REQUIRED_NO_GO = {
    "runtime_behavior",
    "executable_pipeline",
    "test_only_composition_harness",
    "sparkbot_import_wiring_route_import_or_code_copy",
    "model_calls",
    "tool_execution",
    "terminal_or_pty_execution",
    "real_intentcompiler",
    "real_guardiandecision",
    "approval_enforcement",
    "policy_enforcement",
    "adaptive_trust_enforcement",
    "audit_persistence",
    "lima_ai_office_implementation",
    "arc_bot_implementation",
    "custom_bot_implementation",
    "robot_control",
    "drone_control",
    "iot_control",
    "physical_world_action",
    "production_shell_implementation",
}

FORBIDDEN_PRIVATE_OR_OPERATIONAL_RE = re.compile(
    r"("
    r"api[_-]?key|password|credential|private[_-]?key|bearer\s+[a-z0-9._-]+|"
    r"secret=|token=|approval[_ -]?token|"
    r"https?://|www\.|\b(?:[a-z0-9-]+\.)+(?:com|net|org|io|dev|cloud|local)\b|"
    r"runtime[_ -]?config|deploy[_ -]?config|model prompt|tool call|"
    r"\b(?:python|python3|git|curl|wget|powershell|cmd|bash|sh|npm|uv|pytest)\s+"
    r")",
    re.IGNORECASE,
)


def _load_fixture() -> dict[str, Any]:
    assert FIXTURE_PATH.exists()
    with FIXTURE_PATH.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def _all_strings(value: Any) -> list[str]:
    strings: list[str] = []
    if isinstance(value, str):
        strings.append(value)
    elif isinstance(value, list):
        for item in value:
            strings.extend(_all_strings(item))
    elif isinstance(value, dict):
        for item in value.values():
            strings.extend(_all_strings(item))
    return strings


def test_phase_four_one_fixture_is_reference_only() -> None:
    fixture = _load_fixture()
    assert fixture["phase"] == "4.1"
    assert fixture["status"] == "sparkbot_runtime_reference_refresh_only"
    assert fixture["non_runtime"] is True


def test_reference_doc_exists_and_blocks_behavior_movement() -> None:
    assert REFERENCE_DOC_PATH.exists()
    reference_doc = REFERENCE_DOC_PATH.read_text(encoding="utf-8")
    assert "Phase 4.1 refreshes Sparkbot runtime reference knowledge" in reference_doc
    assert "It is read-only reference work" in reference_doc
    assert "NO-GO for runtime extraction implementation" in reference_doc


def test_local_sparkbot_reference_snapshot_is_read_only_and_dirty() -> None:
    reference = _load_fixture()["local_sparkbot_reference"]
    assert reference["inspected"] is True
    assert reference["read_only"] is True
    assert reference["path"] == "C:/Users/limap/Sparkbot"
    assert reference["branch"] == "main"
    assert reference["commit"] == "27bd7dd8ce9e164c6068a13b1855ccc62c7bbe7c"
    assert reference["dirty"] is True
    assert reference["untracked_files"] == [
        "scripts/file_v1_6_72_proposals.py",
        "scripts/file_v1_6_75_proposals.py",
    ]
    assert reference["sparkbot_files_modified"] is False
    assert reference["code_copied_into_lima"] is False
    assert reference["sparkbot_imported_or_wired"] is False


def test_reviewed_surfaces_cover_runtime_reference_boundaries() -> None:
    surfaces = set(_load_fixture()["reviewed_surfaces"])
    assert REQUIRED_SURFACES <= surfaces


def test_surface_findings_keep_high_risk_surfaces_deferred() -> None:
    findings = _load_fixture()["surface_findings"]
    assert findings["tool_aware_loop"]["extract_as_single_kernel_primitive"] is False
    assert findings["tool_aware_loop"]["requires_split_boundaries"] is True
    assert findings["tool_catalogue"]["requires_deny_by_default_tool_pack_scoping"] is True
    assert findings["terminal"]["critical_risk"] is True
    assert findings["terminal"]["do_not_extract_first"] is True
    assert findings["robotics"]["critical_risk"] is True
    assert findings["robotics"]["physical_world_action_blocked"] is True
    assert findings["robotics"]["do_not_extract_first"] is True


def test_phase_four_two_recommendation_selects_non_executing_humaninput_boundary() -> None:
    fixture = _load_fixture()
    assert fixture["recommended_phase_4_2_focus"] == "runtime_boundary_candidate_selection"
    assert (
        fixture["recommended_first_candidate"]
        == "humaninput_intake_boundary_for_chat_and_voice"
    )
    rationale = set(fixture["candidate_rationale"])
    assert "can_be_described_without_runtime_execution" in rationale
    assert "does_not_require_sparkbot_imports_or_wiring" in rationale
    assert "does_not_require_tool_model_terminal_robotics_or_physical_world_behavior" in rationale


def test_deferred_candidates_block_execution_and_product_shells() -> None:
    deferred = set(_load_fixture()["deferred_candidates"])
    assert "model_harness_and_tool_aware_loop_extraction" in deferred
    assert "terminal_pty_extraction" in deferred
    assert "robotics_command_execution_extraction" in deferred
    assert "production_sparkbot_adapter_wiring" in deferred
    assert "lima_ai_office_arc_or_custom_bot_implementation" in deferred


def test_phase_four_one_no_go_blocks_runtime_product_and_physical_world() -> None:
    assert REQUIRED_NO_GO <= set(_load_fixture()["phase_4_1_no_go"])


def test_ready_for_only_allows_phase_four_two_candidate_selection() -> None:
    fixture = _load_fixture()
    assert fixture["ready_for"] == ["phase_4_2_runtime_boundary_candidate_selection"]
    assert "runtime_extraction_implementation" in fixture["not_ready_for"]
    assert "sparkbot_runtime_integration" in fixture["not_ready_for"]
    assert "terminal_pty_execution" in fixture["not_ready_for"]
    assert "physical_world_action" in fixture["not_ready_for"]


def test_boundary_results_show_no_behavior_or_sparkbot_movement() -> None:
    boundary = _load_fixture()["boundary_results"]
    assert boundary["runtime_behavior_added"] is False
    assert boundary["blocked_behavior_added"] is False
    assert boundary["files_under_lima_modified"] is False
    assert boundary["sparkbot_files_modified"] is False
    assert boundary["sparkbot_imported"] is False
    assert boundary["sparkbot_wired"] is False
    assert boundary["sparkbot_code_copied"] is False
    assert boundary["model_calls_added"] is False
    assert boundary["tool_execution_added"] is False
    assert boundary["terminal_execution_added"] is False
    assert boundary["robot_control_added"] is False
    assert boundary["physical_world_action_added"] is False


def test_fixture_has_no_private_operational_data() -> None:
    for string_value in _all_strings(_load_fixture()):
        assert not FORBIDDEN_PRIVATE_OR_OPERATIONAL_RE.search(string_value), string_value


def test_no_phase_four_one_runtime_modules_or_sparkbot_adapters_were_added() -> None:
    forbidden_paths = [
        REPO_ROOT / "lima" / "runtime_extraction.py",
        REPO_ROOT / "lima" / "kernel_pipeline.py",
        REPO_ROOT / "lima" / "adapters" / "sparkbot_runtime.py",
        REPO_ROOT / "lima" / "adapters" / "sparkbot_humaninput_live.py",
        REPO_ROOT / "tests" / "helpers" / "runtime_extraction_harness.py",
    ]
    assert not any(path.exists() for path in forbidden_paths)
