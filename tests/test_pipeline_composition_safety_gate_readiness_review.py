"""Static checks for the Phase 3.8 pipeline composition safety gate review."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
REVIEW_DOC_PATH = (
    REPO_ROOT / "docs" / "PIPELINE_COMPOSITION_SAFETY_GATE_READINESS_REVIEW.md"
)
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_3_8_PIPELINE_COMPOSITION_SAFETY_GATE_READINESS_REVIEW.md"
)
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "kernel_pipeline"
    / "pipeline_composition_safety_gate_readiness_review.json"
)

REQUIRED_NOT_READY = {
    "executable_pipeline",
    "test_only_composition_harness",
    "runtime_composition",
    "production_sparkbot_integration",
    "sparkbot_import_or_wiring",
    "lima_ai_office_implementation",
    "arc_bot_implementation",
    "custom_bot_implementation",
    "robot_control",
    "drone_control",
    "iot_control",
    "physical_world_action",
    "real_intentcompiler",
    "real_guardiandecision",
    "approval_enforcement",
    "policy_enforcement",
    "adaptive_trust_enforcement",
    "execution",
    "audit_persistence",
    "production_wiring",
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


def test_phase_three_eight_fixture_is_non_runtime_review() -> None:
    fixture = _load_fixture()
    assert fixture["phase"] == "3.8"
    assert fixture["status"] == "non_runtime_pipeline_composition_safety_gate_readiness_review"
    assert fixture["non_runtime"] is True


def test_readiness_review_docs_exist() -> None:
    assert REVIEW_DOC_PATH.exists()
    assert PHASE_DOC_PATH.exists()
    review_doc = REVIEW_DOC_PATH.read_text(encoding="utf-8")
    assert "GO for Phase 3 final readiness review" in review_doc
    assert "A future test-only composition harness is not approved" in review_doc


def test_source_phase_three_seven_is_recorded() -> None:
    fixture = _load_fixture()
    assert fixture["source_phase"] == "3.7"
    assert fixture["source_tag"] == "phase-3.7-pipeline-composition-safety-gate-docs"
    assert fixture["source_merge_commit"] == "b34a8eb69f6a939daa22afda7640bb16ac9d5a90"


def test_gate_findings_preserve_safety_boundaries() -> None:
    findings = _load_fixture()["gate_findings"]
    assert findings["safety_gate_is_clear_enough_to_stand"] is True
    assert findings["safety_gate_is_not_a_pipeline"] is True
    assert findings["safety_gate_is_not_a_harness"] is True
    assert findings["stage_maps_remain_descriptive_only"] is True
    assert findings["relationship_maps_are_not_compatibility_proof"] is True
    assert findings["readiness_findings_are_not_authorization"] is True
    assert findings["future_harness_conditions_require_later_review"] is True


def test_future_harness_is_not_approved_by_review() -> None:
    harness = _load_fixture()["future_test_only_harness"]
    assert harness["approved_by_this_review"] is False
    assert harness["requires_separate_design_review"] is True
    assert harness["requires_operator_explicit_scope"] is True
    assert harness["must_not_import_sparkbot"] is True
    assert harness["must_not_execute_tools"] is True
    assert harness["must_not_call_models"] is True
    assert harness["must_not_persist_audit_events"] is True
    assert harness["must_not_touch_physical_world"] is True


def test_readiness_result_only_allows_final_review_and_phase_four_planning() -> None:
    fixture = _load_fixture()
    assert fixture["readiness_result"] == "go_for_phase_3_final_readiness_review"
    assert set(fixture["ready_for"]) == {
        "phase_3_final_readiness_review",
        "phase_4_planning_after_final_readiness_only",
    }


def test_not_ready_for_keeps_runtime_harness_and_physical_world_blocked() -> None:
    assert REQUIRED_NOT_READY <= set(_load_fixture()["not_ready_for"])


def test_phase_three_eight_boundary_does_not_authorize_behavior() -> None:
    boundary = _load_fixture()["phase_3_8_boundary"]
    assert boundary["review_is_not_authorization"] is True
    assert boundary["review_is_not_approval"] is True
    assert boundary["review_is_not_enforcement"] is True
    assert boundary["review_is_not_execution"] is True
    assert boundary["review_is_not_audit_persistence"] is True
    assert boundary["review_is_not_runtime_wiring"] is True
    assert boundary["review_does_not_start_phase_4"] is True


def test_fixture_has_no_private_operational_data() -> None:
    for string_value in _all_strings(_load_fixture()):
        assert not FORBIDDEN_PRIVATE_OR_OPERATIONAL_RE.search(string_value), string_value


def test_no_phase_three_eight_runtime_modules_or_harnesses_were_added() -> None:
    forbidden_paths = [
        REPO_ROOT / "lima" / "kernel_pipeline.py",
        REPO_ROOT / "lima" / "pipeline.py",
        REPO_ROOT / "lima" / "composition.py",
        REPO_ROOT / "tests" / "helpers" / "kernel_pipeline_composition_harness.py",
    ]
    assert not any(path.exists() for path in forbidden_paths)
