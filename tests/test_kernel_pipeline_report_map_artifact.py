"""Static checks for the Phase 3.6 kernel pipeline report/map artifact."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "kernel_pipeline"
    / "pipeline_report_map_artifact.json"
)
RELATIONSHIP_METADATA_PATH = (
    REPO_ROOT / "tests" / "fixtures" / "kernel_pipeline" / "pipeline_relationships.json"
)
READINESS_METADATA_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "kernel_pipeline"
    / "relationship_metadata_readiness_review.json"
)
PRODUCT_FAMILY_PATH = (
    REPO_ROOT / "tests" / "fixtures" / "product_family" / "lima_product_family.json"
)
ADAPTIVE_TRUST_PATH = (
    REPO_ROOT / "tests" / "fixtures" / "safety" / "adaptive_trust_gates.json"
)
HUMAN_SAFETY_PATH = (
    REPO_ROOT / "tests" / "fixtures" / "safety" / "human_safety_doctrine.json"
)

PHASE_3_3_TAG = "phase-3.3-nonproduction-kernel-pipeline-relationship-metadata"
PHASE_3_4_TAG = (
    "phase-3.4-nonproduction-kernel-pipeline-relationship-metadata-readiness-review"
)
PHASE_3_5_TAG = "phase-3.5-lima-product-family-adaptive-trust-doctrine"

PHASE_3_3_COMMIT = "ecb41b1825ff9f4537846c81739f25d3d7184f83"
PHASE_3_4_COMMIT = "ce8c8172f06d61c996af486dc20fd32046323361"
PHASE_3_5_COMMIT = "5b0c8586267f6f7bab544634422b4a04d2221d2a"

REQUIRED_SOURCE_FIXTURES = {
    "pipeline_relationships.json",
    "relationship_metadata_readiness_review.json",
    "lima_product_family.json",
    "adaptive_trust_gates.json",
    "human_safety_doctrine.json",
}

REQUIRED_REPORT_SECTIONS = {
    "purpose",
    "source phases",
    "conceptual stage map",
    "relationship summary",
    "readiness summary",
    "doctrine context",
    "known gaps",
    "blocked interpretations",
    "ready_for",
    "not_ready_for",
}

REQUIRED_BLOCKED = {
    "executable_pipeline",
    "test_only_composition_harness",
    "runtime_composition",
    "production_sparkbot_integration",
    "real_intentcompiler",
    "real_guardiandecision",
    "approval",
    "enforcement",
    "execution",
    "audit_persistence",
    "arc_bot_implementation",
    "custom_bot_implementation",
    "robot_control",
    "physical_world_action",
}

ALLOWED_READY_FOR = {
    "non_production_pipeline_composition_safety_gate_documentation",
    "further_non_runtime_review_of_mapped_fixture_path",
    "future_readiness_review_before_any_test_only_harness",
}

FORBIDDEN_PRIVATE_OR_OPERATIONAL_RE = re.compile(
    r"("
    r"api[_-]?key|password|credential|private[_-]?key|bearer\s+[a-z0-9._-]+|"
    r"secret=|token=|approval[_ -]?token|"
    r"https?://|www\.|\b(?:[a-z0-9-]+\.)+(?:com|net|org|io|dev|cloud|local)\b|"
    r"runtime[_ -]?config|deploy[_ -]?config|shell script|model prompt|tool call|"
    r"\b(?:python|python3|git|curl|wget|powershell|cmd|bash|sh|npm|uv|pytest)\s+"
    r")",
    re.IGNORECASE,
)


def _load_json(path: Path) -> Any:
    assert path.exists()
    with path.open(encoding="utf-8") as fixture_file:
        return json.load(fixture_file)


def _load_artifact() -> dict[str, Any]:
    artifact = _load_json(ARTIFACT_PATH)
    assert isinstance(artifact, dict)
    return artifact


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


def test_report_map_artifact_fixture_exists_and_is_valid_json() -> None:
    assert _load_artifact()


def test_phase_status_and_non_runtime_boundary_are_explicit() -> None:
    artifact = _load_artifact()
    assert artifact["phase"] == "3.6"
    assert artifact["status"] == "non_runtime_report_map_artifact"
    assert artifact["non_runtime"] is True


def test_source_phases_tags_commits_and_fixtures_are_recorded() -> None:
    artifact = _load_artifact()
    assert {"3.3", "3.4", "3.5"} <= set(artifact["source_phases"])
    assert {PHASE_3_3_TAG, PHASE_3_4_TAG, PHASE_3_5_TAG} <= set(
        artifact["source_tags"]
    )
    commits = {item["merge_commit"] for item in artifact["source_commits"]}
    assert {PHASE_3_3_COMMIT, PHASE_3_4_COMMIT, PHASE_3_5_COMMIT} <= commits
    assert REQUIRED_SOURCE_FIXTURES <= set(artifact["source_fixtures"])


def test_report_sections_cover_required_review_areas() -> None:
    artifact = _load_artifact()
    assert REQUIRED_REPORT_SECTIONS <= set(artifact["report_sections"])


def test_conceptual_stage_map_is_descriptive_only() -> None:
    artifact = _load_artifact()
    stage_map = artifact["conceptual_stage_map"]
    assert stage_map
    for stage in stage_map:
        assert stage["descriptive_only"] is True
        assert stage["does_not_define_execution_order"] is True
        assert stage["does_not_define_callable_behavior"] is True


def test_relationship_summary_does_not_imply_order_or_runtime_compatibility() -> None:
    summary = _load_artifact()["relationship_summary"]
    assert summary["relationship_metadata_status"] == "non_runtime_relationship_metadata"
    assert summary["relationship_map_is_not_execution_order"] is True
    assert summary["relationship_map_is_not_compatibility_proof"] is True
    assert summary["relationship_map_does_not_prove_runtime_compatibility"] is True
    assert summary["relationship_map_does_not_authorize_runtime_integration"] is True


def test_readiness_summary_does_not_imply_authority_or_behavior() -> None:
    summary = _load_artifact()["readiness_summary"]
    assert summary["phase_3_4_status"] == "non_runtime_readiness_review"
    assert summary["readiness_finding_is_not_authorization"] is True
    assert summary["readiness_finding_is_not_approval"] is True
    assert summary["readiness_finding_is_not_enforcement"] is True
    assert summary["readiness_finding_is_not_execution"] is True
    assert summary["readiness_finding_is_not_audit_persistence"] is True


def test_doctrine_context_does_not_imply_runtime_enforcement_or_control() -> None:
    context = _load_artifact()["doctrine_context"]
    assert context["context_only"] is True
    assert context["non_runtime"] is True
    assert context["non_executable"] is True
    assert context["doctrine_references_are_not_policy_enforcement"] is True
    assert context["product_family_references_do_not_imply_shell_implementation"] is True
    assert context["future_driver_plane_references_do_not_imply_robot_control"] is True
    assert context["adaptive_trust_references_do_not_imply_adaptive_trust_enforcement"]
    assert context["human_safety_references_do_not_imply_executable_policy"] is True


def test_blocked_interpretations_cover_runtime_composition_and_physical_world() -> None:
    artifact = _load_artifact()
    blocked = set(artifact["blocked_interpretations"])
    assert REQUIRED_BLOCKED <= blocked
    assert REQUIRED_BLOCKED <= set(artifact["not_ready_for"])


def test_ready_for_only_includes_non_runtime_next_work() -> None:
    ready_for = set(_load_artifact()["ready_for"])
    assert ready_for
    assert ready_for <= ALLOWED_READY_FOR
    assert "non_production_pipeline_composition_safety_gate_documentation" in ready_for
    assert "future_readiness_review_before_any_test_only_harness" in ready_for


def test_artifact_has_no_commands_secrets_hosts_or_private_operational_data() -> None:
    for string_value in _all_strings(_load_artifact()):
        assert not FORBIDDEN_PRIVATE_OR_OPERATIONAL_RE.search(string_value), string_value


def test_no_phase_three_six_runtime_modules_or_harnesses_were_added() -> None:
    forbidden_paths = [
        REPO_ROOT / "lima" / "kernel_pipeline_report_map.py",
        REPO_ROOT / "lima" / "kernel_pipeline.py",
        REPO_ROOT / "lima" / "pipeline.py",
        REPO_ROOT / "tests" / "helpers" / "kernel_pipeline_composition_harness.py",
        REPO_ROOT / "tests" / "helpers" / "kernel_pipeline_report_generator.py",
    ]
    assert not any(path.exists() for path in forbidden_paths)


def test_existing_phase_three_three_relationships_remain_non_runtime() -> None:
    relationships = _load_json(RELATIONSHIP_METADATA_PATH)
    assert isinstance(relationships, list)
    assert len(relationships) == 60
    assert all(relationship["non_runtime"] is True for relationship in relationships)


def test_existing_phase_three_four_readiness_metadata_remains_non_runtime() -> None:
    readiness = _load_json(READINESS_METADATA_PATH)
    assert readiness["status"] == "non_runtime_readiness_review"
    assert "runtime_pipeline_composition" in readiness["not_ready_for"]
    assert "approval" in readiness["not_ready_for"]
    assert "enforcement" in readiness["not_ready_for"]
    assert "execution" in readiness["not_ready_for"]
    assert "audit_persistence" in readiness["not_ready_for"]


def test_existing_phase_three_five_doctrine_metadata_remains_non_runtime() -> None:
    product_family = _load_json(PRODUCT_FAMILY_PATH)
    adaptive_trust = _load_json(ADAPTIVE_TRUST_PATH)
    human_safety = _load_json(HUMAN_SAFETY_PATH)
    assert product_family["phase"] == "3.5"
    assert product_family["non_runtime"] is True
    assert adaptive_trust["phase"] == "3.5"
    assert adaptive_trust["non_runtime"] is True
    assert human_safety["phase"] == "3.5"
    assert human_safety["non_runtime"] is True
