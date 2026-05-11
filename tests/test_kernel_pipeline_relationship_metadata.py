"""Shape checks for Phase 3.3 kernel pipeline relationship metadata."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
METADATA_PATH = (
    REPO_ROOT / "tests" / "fixtures" / "kernel_pipeline" / "pipeline_relationships.json"
)

REQUIRED_FIELDS = {
    "relationship_id",
    "scenario_id",
    "scenario_name",
    "pipeline_stage",
    "current_fixture_ref",
    "previous_stage_ref",
    "next_stage_ref",
    "compatible_with",
    "expected_posture",
    "safety_gate_refs",
    "non_runtime",
    "notes",
}

REQUIRED_SCENARIO_IDS = {
    "low_risk_informational",
    "calendar_scheduling",
    "draft_only_communication",
    "email_send_requires_approval",
    "terminal_critical",
    "robot_safety_critical",
    "secret_access",
    "payment_deploy_admin_destructive",
    "invalid_missing_metadata",
    "clarification_needed",
    "blocked_unsafe_request",
    "expired_revoked_superseded_fake_decision",
}

SAFETY_GATE_REFS = {
    "docs/ADAPTER_SAFETY_GATE.md",
    "docs/INTENTENVELOPE_SAFETY_GATE.md",
    "docs/GUARDIAN_REQUEST_SAFETY_GATE.md",
    "docs/FAKE_GUARDIANDECISION_SAFETY_GATE.md",
}

RUNTIME_WORD_RE = re.compile(r"\b(execute|run|call|trigger)\b", re.IGNORECASE)
SECRET_VALUE_RE = re.compile(
    r"(api[_-]?key|password|credential|private[_-]?key|bearer\s+[a-z0-9._-]+)",
    re.IGNORECASE,
)


def _load_relationships() -> list[dict[str, Any]]:
    assert METADATA_PATH.exists()
    with METADATA_PATH.open(encoding="utf-8") as metadata_file:
        relationships = json.load(metadata_file)
    assert isinstance(relationships, list)
    assert relationships
    return relationships


def _string_values(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [item for item in value if isinstance(item, str)]
    return []


def _all_string_values(relationship: dict[str, Any]) -> list[str]:
    strings: list[str] = []
    for value in relationship.values():
        strings.extend(_string_values(value))
    return strings


def test_relationship_metadata_file_exists_and_is_valid_json() -> None:
    _load_relationships()


def test_every_relationship_includes_required_fields() -> None:
    for relationship in _load_relationships():
        assert REQUIRED_FIELDS <= relationship.keys()


def test_every_relationship_is_non_runtime() -> None:
    for relationship in _load_relationships():
        assert relationship["non_runtime"] is True


def test_stage_refs_are_reference_only_words() -> None:
    for relationship in _load_relationships():
        for value in _all_string_values(relationship):
            assert not RUNTIME_WORD_RE.search(value), value


def test_safety_gate_refs_include_known_gate() -> None:
    for relationship in _load_relationships():
        refs = set(relationship["safety_gate_refs"])
        assert refs
        assert refs <= SAFETY_GATE_REFS
        assert refs & SAFETY_GATE_REFS


def test_required_scenario_groups_are_present() -> None:
    scenario_ids = {relationship["scenario_id"] for relationship in _load_relationships()}
    assert REQUIRED_SCENARIO_IDS <= scenario_ids


def test_no_secret_or_credential_values_are_present() -> None:
    for relationship in _load_relationships():
        for value in relationship.values():
            for string_value in _string_values(value):
                assert not SECRET_VALUE_RE.search(string_value), string_value


def test_no_runtime_pipeline_helpers_were_added() -> None:
    helper_dir = REPO_ROOT / "tests" / "helpers"
    assert not (helper_dir / "kernel_pipeline_fixture_harness.py").exists()
    assert not (helper_dir / "kernel_pipeline_relationship_harness.py").exists()
