"""Static checks for the Phase 3 final readiness review."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
REVIEW_DOC_PATH = REPO_ROOT / "docs" / "PHASE_3_FINAL_READINESS_REVIEW.md"
PHASE_DOC_PATH = REPO_ROOT / "docs" / "PHASE_3_9_FINAL_READINESS_REVIEW.md"
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "kernel_pipeline"
    / "phase_3_final_readiness_review.json"
)

REQUIRED_BLOCKED = {
    "runtime_behavior",
    "executable_pipeline",
    "test_only_composition_harness_unless_separately_approved",
    "runtime_composition",
    "production_sparkbot_integration",
    "sparkbot_import_or_wiring",
    "live_routes",
    "model_calls",
    "tool_execution",
    "terminal_or_pty_execution",
    "real_intentcompiler",
    "real_guardiandecision",
    "adaptive_trust_enforcement",
    "approval_enforcement",
    "policy_enforcement",
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


def test_phase_three_final_review_fixture_is_non_runtime() -> None:
    fixture = _load_fixture()
    assert fixture["phase"] == "3.9"
    assert fixture["status"] == "non_runtime_phase_3_final_readiness_review"
    assert fixture["non_runtime"] is True


def test_final_readiness_docs_exist_and_define_phase_four_planning_only() -> None:
    assert REVIEW_DOC_PATH.exists()
    assert PHASE_DOC_PATH.exists()
    review_doc = REVIEW_DOC_PATH.read_text(encoding="utf-8")
    assert "GO for Phase 4 planning only" in review_doc
    assert "No Phase 4 implementation is approved" in review_doc


def test_source_phase_three_eight_is_recorded() -> None:
    fixture = _load_fixture()
    assert fixture["source_phase"] == "3.8"
    assert fixture["source_tag"] == "phase-3.8-pipeline-composition-safety-gate-readiness-review"
    assert fixture["source_merge_commit"] == "5062553b041ee881beedda72378ff6090b71ac75"


def test_all_phase_three_milestones_are_reviewed() -> None:
    assert set(_load_fixture()["reviewed_phase_3_milestones"]) == {
        "3.0",
        "3.1",
        "3.2",
        "3.3",
        "3.4",
        "3.5",
        "3.6",
        "3.7",
        "3.8",
    }


def test_readiness_result_allows_only_phase_four_planning() -> None:
    fixture = _load_fixture()
    assert fixture["readiness_result"] == "phase_3_complete_go_for_phase_4_planning_only"
    assert fixture["ready_for"] == ["phase_4_0_runtime_extraction_readiness_planning"]
    assert "phase_4_runtime_extraction_implementation" in fixture["not_ready_for"]


def test_phase_three_did_not_prove_runtime_or_product_readiness() -> None:
    did_not_prove = set(_load_fixture()["phase_3_did_not_prove"])
    assert "runtime_compatibility" in did_not_prove
    assert "production_sparkbot_integration_readiness" in did_not_prove
    assert "lima_ai_office_implementation_readiness" in did_not_prove
    assert "robot_drone_iot_physical_world_control_readiness" in did_not_prove


def test_still_blocked_covers_runtime_product_and_physical_world_scope() -> None:
    assert REQUIRED_BLOCKED <= set(_load_fixture()["still_blocked"])


def test_recommended_next_phase_is_planning_only() -> None:
    fixture = _load_fixture()
    assert fixture["recommended_next_branch"] == "phase-4-0-runtime-extraction-readiness-planning"
    assert fixture["recommended_next_milestone"] == "Phase 4.0 - Runtime Extraction Readiness Planning"


def test_phase_three_nine_boundary_does_not_authorize_phase_four_behavior() -> None:
    boundary = _load_fixture()["phase_3_9_boundary"]
    assert boundary["final_review_is_not_runtime_extraction"] is True
    assert boundary["final_review_is_not_sparkbot_integration"] is True
    assert boundary["final_review_is_not_product_shell_implementation"] is True
    assert boundary["final_review_is_not_robot_control"] is True
    assert boundary["final_review_is_not_approval"] is True
    assert boundary["final_review_is_not_execution"] is True
    assert boundary["final_review_is_not_audit_persistence"] is True
    assert boundary["phase_4_planning_only"] is True


def test_fixture_has_no_private_operational_data() -> None:
    for string_value in _all_strings(_load_fixture()):
        assert not FORBIDDEN_PRIVATE_OR_OPERATIONAL_RE.search(string_value), string_value


def test_no_phase_three_final_review_runtime_modules_or_harnesses_were_added() -> None:
    forbidden_paths = [
        REPO_ROOT / "lima" / "kernel_pipeline.py",
        REPO_ROOT / "lima" / "pipeline.py",
        REPO_ROOT / "lima" / "composition.py",
        REPO_ROOT / "tests" / "helpers" / "kernel_pipeline_composition_harness.py",
    ]
    assert not any(path.exists() for path in forbidden_paths)
