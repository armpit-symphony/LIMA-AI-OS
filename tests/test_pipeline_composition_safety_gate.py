"""Static checks for the Phase 3.7 pipeline composition safety gate."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
SAFETY_GATE_PATH = REPO_ROOT / "docs" / "PIPELINE_COMPOSITION_SAFETY_GATE.md"
PHASE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_3_7_PIPELINE_COMPOSITION_SAFETY_GATE_DOCS.md"
)
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "kernel_pipeline"
    / "pipeline_composition_safety_gate.json"
)

REQUIRED_BLOCKED = {
    "executable_pipeline",
    "test_only_composition_harness",
    "runtime_composition",
    "production_sparkbot_integration",
    "sparkbot_import_or_wiring",
    "real_intentcompiler",
    "real_guardiandecision",
    "model_calls",
    "tool_execution",
    "terminal_or_pty_execution",
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

REQUIRED_PRECONDITIONS = {
    "phase_3_6_merged_and_tagged",
    "fixtures_are_synthetic_and_lima_owned",
    "relationships_remain_non_runtime",
    "stage_maps_are_descriptive_only",
    "relationship_maps_are_not_compatibility_proofs",
    "readiness_findings_are_not_authorization",
    "doctrine_references_are_context_only",
    "no_private_operational_data",
    "unsupported_categories_are_explicit",
    "critical_unknown_destructive_secret_payment_deploy_admin_robot_drone_iot_physical_scenarios_cannot_auto_approve",
    "separate_design_review_required_before_any_test_only_harness",
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


def test_phase_three_seven_fixture_is_non_runtime() -> None:
    fixture = _load_fixture()
    assert fixture["phase"] == "3.7"
    assert fixture["status"] == "non_runtime_pipeline_composition_safety_gate_docs"
    assert fixture["non_runtime"] is True


def test_safety_gate_docs_exist() -> None:
    assert SAFETY_GATE_PATH.exists()
    assert PHASE_DOC_PATH.exists()
    assert "not a harness" in SAFETY_GATE_PATH.read_text(encoding="utf-8").lower()


def test_source_phase_three_six_is_recorded() -> None:
    fixture = _load_fixture()
    assert fixture["source_phase"] == "3.6"
    assert (
        fixture["source_tag"]
        == "phase-3.6-nonproduction-kernel-pipeline-report-map-artifact"
    )
    assert fixture["source_merge_commit"] == "8073df2af44560986af5bc07142e413fde4be58a"


def test_required_preconditions_are_explicit() -> None:
    fixture = _load_fixture()
    assert REQUIRED_PRECONDITIONS <= set(fixture["required_preconditions"])


def test_blocked_interpretations_cover_runtime_and_physical_world_scope() -> None:
    fixture = _load_fixture()
    blocked = set(fixture["blocked_interpretations"])
    assert REQUIRED_BLOCKED <= blocked
    assert {
        "executable_pipeline",
        "test_only_composition_harness",
        "runtime_composition",
        "robot_control",
        "drone_control",
        "iot_control",
        "physical_world_action",
    } <= set(fixture["not_ready_for"])


def test_future_harness_conditions_fail_closed_and_remain_tests_only() -> None:
    conditions = _load_fixture()["future_test_only_harness_conditions"]
    assert conditions["requires_later_readiness_review"] is True
    assert conditions["tests_only"] is True
    assert conditions["synthetic_lima_owned_fixtures_only"] is True
    assert conditions["no_sparkbot_imports"] is True
    assert conditions["no_model_calls"] is True
    assert conditions["no_tool_execution"] is True
    assert conditions["critical_and_unknown_risk_fail_closed"] is True
    assert conditions["no_real_approvals_or_guardian_decisions"] is True
    assert conditions["no_audit_persistence"] is True
    assert conditions["not_a_production_adapter"] is True


def test_ready_for_only_allows_readiness_review_not_harness() -> None:
    ready_for = set(_load_fixture()["ready_for"])
    assert "phase_3_8_pipeline_composition_safety_gate_readiness_review" in ready_for
    assert "test_only_composition_harness" not in ready_for
    assert "executable_pipeline" not in ready_for


def test_boundary_flags_prevent_authority_and_runtime_interpretation() -> None:
    boundary = _load_fixture()["phase_3_7_boundary"]
    assert boundary["safety_gate_is_not_a_pipeline"] is True
    assert boundary["safety_gate_is_not_a_harness"] is True
    assert boundary["safety_gate_is_not_authorization"] is True
    assert boundary["safety_gate_is_not_approval"] is True
    assert boundary["safety_gate_is_not_enforcement"] is True
    assert boundary["safety_gate_is_not_execution"] is True
    assert boundary["safety_gate_is_not_audit_persistence"] is True
    assert boundary["safety_gate_is_not_production_wiring"] is True


def test_fixture_has_no_private_operational_data() -> None:
    for string_value in _all_strings(_load_fixture()):
        assert not FORBIDDEN_PRIVATE_OR_OPERATIONAL_RE.search(string_value), string_value


def test_no_phase_three_seven_runtime_modules_or_harnesses_were_added() -> None:
    forbidden_paths = [
        REPO_ROOT / "lima" / "kernel_pipeline.py",
        REPO_ROOT / "lima" / "pipeline.py",
        REPO_ROOT / "lima" / "composition.py",
        REPO_ROOT / "tests" / "helpers" / "kernel_pipeline_composition_harness.py",
    ]
    assert not any(path.exists() for path in forbidden_paths)
