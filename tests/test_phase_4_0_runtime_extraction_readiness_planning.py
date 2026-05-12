"""Static checks for Phase 4.0 runtime extraction readiness planning."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PLANNING_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_4_0_RUNTIME_EXTRACTION_READINESS_PLANNING.md"
)
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_4_0_runtime_extraction_readiness_planning.json"
)

REQUIRED_NO_GO = {
    "runtime_behavior",
    "executable_pipeline",
    "test_only_composition_harness",
    "sparkbot_import_or_wiring",
    "production_route_imports",
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

REQUIRED_SEQUENCE = [
    "phase_4_0_runtime_extraction_readiness_planning",
    "phase_4_1_sparkbot_runtime_reference_refresh",
    "phase_4_2_runtime_boundary_candidate_selection",
    "phase_4_3_boundary_extraction_safety_gate",
    "phase_4_4_boundary_fixture_contract_extension_if_approved",
    "phase_4_5_boundary_readiness_review",
    "explicitly_approved_narrow_nonproduction_extraction_or_adapter_work",
]

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


def test_phase_four_zero_fixture_is_planning_only() -> None:
    fixture = _load_fixture()
    assert fixture["phase"] == "4.0"
    assert fixture["status"] == "runtime_extraction_readiness_planning_only"
    assert fixture["non_runtime"] is True


def test_planning_doc_exists_and_blocks_implementation() -> None:
    assert PLANNING_DOC_PATH.exists()
    planning_doc = PLANNING_DOC_PATH.read_text(encoding="utf-8")
    assert "Phase 4.0 starts Phase 4 as planning only" in planning_doc
    assert "NO-GO for runtime extraction implementation" in planning_doc


def test_phase_three_final_review_source_is_recorded() -> None:
    fixture = _load_fixture()
    assert fixture["source_phase"] == "3.9"
    assert fixture["source_tag"] == "phase-3.9-final-readiness-review"
    assert fixture["source_merge_commit"] == "3c922b3"


def test_recommended_sequence_keeps_readiness_gates_before_behavior() -> None:
    assert _load_fixture()["recommended_phase_4_sequence"] == REQUIRED_SEQUENCE


def test_sparkbot_reference_refresh_is_first_boundary() -> None:
    fixture = _load_fixture()
    assert fixture["recommended_first_boundary"] == "sparkbot_runtime_reference_refresh"
    focus = set(fixture["sparkbot_reference_refresh_focus"])
    assert "humaninput_chat_voice_entrypoints" in focus
    assert "tool_catalogue_and_tool_pack_scoping_boundaries" in focus
    assert "audit_spine_lineage_surfaces" in focus
    assert "robotics_robo_os_adjacent_action_surfaces_if_present" in focus


def test_phase_four_zero_no_go_blocks_runtime_product_and_physical_world() -> None:
    assert REQUIRED_NO_GO <= set(_load_fixture()["phase_4_0_no_go"])


def test_sparkbot_handling_is_reference_only() -> None:
    handling = _load_fixture()["sparkbot_handling"]
    assert handling["sparkbot_is_spec"] is True
    assert handling["phase_4_0_inspects_sparkbot"] is False
    assert handling["phase_4_1_is_first_safe_reference_refresh"] is True
    assert handling["local_sparkbot_may_be_dirty_prototype"] is True
    assert handling["do_not_copy_blindly"] is True
    assert handling["read_only_until_explicit_future_approval"] is True


def test_ready_for_only_allows_phase_four_one_reference_refresh() -> None:
    fixture = _load_fixture()
    assert fixture["ready_for"] == ["phase_4_1_sparkbot_runtime_reference_refresh"]
    assert "runtime_extraction_implementation" in fixture["not_ready_for"]
    assert "sparkbot_runtime_integration" in fixture["not_ready_for"]


def test_phase_four_zero_boundary_does_not_authorize_behavior() -> None:
    boundary = _load_fixture()["phase_4_0_boundary"]
    assert boundary["planning_is_not_implementation"] is True
    assert boundary["planning_is_not_runtime_extraction"] is True
    assert boundary["planning_is_not_sparkbot_integration"] is True
    assert boundary["planning_is_not_product_shell_implementation"] is True
    assert boundary["planning_is_not_robot_control"] is True
    assert boundary["planning_is_not_approval"] is True
    assert boundary["planning_is_not_execution"] is True
    assert boundary["planning_is_not_audit_persistence"] is True


def test_fixture_has_no_private_operational_data() -> None:
    for string_value in _all_strings(_load_fixture()):
        assert not FORBIDDEN_PRIVATE_OR_OPERATIONAL_RE.search(string_value), string_value


def test_no_phase_four_zero_runtime_modules_or_sparkbot_adapters_were_added() -> None:
    forbidden_paths = [
        REPO_ROOT / "lima" / "runtime_extraction.py",
        REPO_ROOT / "lima" / "kernel_pipeline.py",
        REPO_ROOT / "lima" / "adapters" / "sparkbot_runtime.py",
        REPO_ROOT / "tests" / "helpers" / "runtime_extraction_harness.py",
    ]
    assert not any(path.exists() for path in forbidden_paths)
