"""Readiness checks for Phase 3.4 relationship metadata review."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
READINESS_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "kernel_pipeline"
    / "relationship_metadata_readiness_review.json"
)
RELATIONSHIP_METADATA_PATH = (
    REPO_ROOT / "tests" / "fixtures" / "kernel_pipeline" / "pipeline_relationships.json"
)

PHASE_3_3_TAG = "phase-3.3-nonproduction-kernel-pipeline-relationship-metadata"
PHASE_3_3_MERGE_COMMIT = "ecb41b1825ff9f4537846c81739f25d3d7184f83"

SAFETY_GATES = {
    "docs/ADAPTER_SAFETY_GATE.md",
    "docs/INTENTENVELOPE_SAFETY_GATE.md",
    "docs/GUARDIAN_REQUEST_SAFETY_GATE.md",
    "docs/FAKE_GUARDIANDECISION_SAFETY_GATE.md",
}

ALLOWED_READY_FOR = {
    "non_production_report_map_artifact_work",
    "documentation_review_of_fixture_relationships",
    "safety_gate_backed_review_artifacts",
}

REQUIRED_NOT_READY_FOR = {
    "executable_pipeline",
    "runtime_pipeline_composition",
    "runtime_behavior",
    "production_integration",
    "production_sparkbot_wiring",
    "real_intentcompiler",
    "real_guardiandecision",
    "approval",
    "enforcement",
    "execution",
    "audit_persistence",
    "sparkbot_wiring",
    "robot_control",
}

REQUIRED_DEFERRED = {
    "lima_product_family_and_adaptive_trust_doctrine",
    "arc_bot_and_custom_business_bot_shell_doctrine",
    "adaptive_trust_gates_as_default_ux",
    "practical_human_safety_doctrine",
}

SECRET_OR_PRIVATE_RE = re.compile(
    r"(api[_-]?key|password|credential|private[_-]?key|bearer\s+[a-z0-9._-]+|token=|secret=)",
    re.IGNORECASE,
)
HOST_OR_URL_RE = re.compile(
    r"(https?://|www\.|\b(?:[a-z0-9-]+\.)+(?:com|net|org|io|dev|cloud|local)\b)",
    re.IGNORECASE,
)
COMMAND_STRING_RE = re.compile(
    r"(^|\s)(python|python3|git|curl|wget|powershell|cmd|bash|sh|npm|uv|pytest)\s+",
    re.IGNORECASE,
)
CALLABLE_PIPELINE_RE = re.compile(
    r"\b(function|callable|handler|callback|entrypoint|execute_step|run_step|trigger_step|shell command|tool call|model prompt)\b",
    re.IGNORECASE,
)


def _load_readiness_review() -> dict[str, Any]:
    assert READINESS_PATH.exists()
    with READINESS_PATH.open(encoding="utf-8") as review_file:
        review = json.load(review_file)
    assert isinstance(review, dict)
    return review


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


def test_readiness_review_fixture_exists_and_is_valid_json() -> None:
    review = _load_readiness_review()
    assert review["phase"] == "3.4"


def test_readiness_review_references_phase_three_three_source() -> None:
    review = _load_readiness_review()
    assert review["source_phase"] == "3.3"
    assert review["source_tag"] == PHASE_3_3_TAG
    assert review["source_merge_commit"] == PHASE_3_3_MERGE_COMMIT


def test_readiness_review_status_is_non_runtime() -> None:
    review = _load_readiness_review()
    assert review["status"] == "non_runtime_readiness_review"


def test_ready_for_only_allows_non_runtime_next_work() -> None:
    review = _load_readiness_review()
    ready_for = set(review["ready_for"])
    assert ready_for
    assert ready_for <= ALLOWED_READY_FOR
    assert "non_production_report_map_artifact_work" in ready_for


def test_not_ready_for_blocks_runtime_and_integration_work() -> None:
    review = _load_readiness_review()
    not_ready_for = set(review["not_ready_for"])
    assert REQUIRED_NOT_READY_FOR <= not_ready_for


def test_future_product_family_and_adaptive_trust_doctrine_is_deferred() -> None:
    review = _load_readiness_review()
    deferred = set(review["deferred_to_future_phase"])
    assert REQUIRED_DEFERRED <= deferred
    assert "lima_product_family_and_adaptive_trust_doctrine" in deferred


def test_safety_gates_are_referenced() -> None:
    review = _load_readiness_review()
    assert set(review["safety_gates"]) == SAFETY_GATES


def test_no_commands_secrets_hosts_or_private_operational_data() -> None:
    review = _load_readiness_review()
    for string_value in _all_strings(review):
        assert not SECRET_OR_PRIVATE_RE.search(string_value), string_value
        assert not HOST_OR_URL_RE.search(string_value), string_value
        assert not COMMAND_STRING_RE.search(string_value), string_value


def test_fixture_does_not_contain_callable_pipeline_helpers() -> None:
    review = _load_readiness_review()
    for string_value in _all_strings(review):
        assert not CALLABLE_PIPELINE_RE.search(string_value), string_value


def test_existing_relationship_metadata_remains_non_runtime() -> None:
    with RELATIONSHIP_METADATA_PATH.open(encoding="utf-8") as metadata_file:
        relationships = json.load(metadata_file)
    assert relationships
    assert all(relationship["non_runtime"] is True for relationship in relationships)
