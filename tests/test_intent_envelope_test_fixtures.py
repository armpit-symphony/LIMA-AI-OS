"""Shape tests for synthetic IntentEnvelope fixture artifacts."""

from __future__ import annotations

import ast
import json
import re
from pathlib import Path
from typing import Any


FIXTURE_ROOT = Path(__file__).parent / "fixtures" / "intent_envelopes"

FIXTURE_FILES = {
    "typed": FIXTURE_ROOT / "typed_intent_fixtures.json",
    "invalid": FIXTURE_ROOT / "invalid_missing_metadata_fixtures.json",
    "clarification": FIXTURE_ROOT / "clarification_needed_fixtures.json",
    "safety": FIXTURE_ROOT / "safety_critical_intent_fixtures.json",
}

TOP_LEVEL_KEYS = {
    "fixture_id",
    "fixture_type",
    "human_input_ref",
    "raw_text",
    "explicit_metadata",
    "expected_intent_envelope",
    "expected_status",
    "expected_reason",
    "privacy_class",
    "redaction_class",
    "notes",
}

REQUIRED_EXPLICIT_METADATA_FIELDS = {
    "intent_type",
    "action_type",
    "risk_class",
    "target_ref",
    "typed_args",
    "evidence_refs",
    "requested_tool_packs",
    "approval_level",
    "privacy_class",
    "redaction_class",
    "lineage_id",
    "reason",
    "confidence",
}

REQUIRED_ENVELOPE_FIELDS = {
    "intent_id",
    "source_input_id",
    "actor_id",
    "shell_id",
    "normalized_text",
    "intent_type",
    "typed_args",
    "confidence",
    "risk_class",
    "ambiguity_flags",
    "required_evidence",
    "required_approval_level",
    "proposed_tool_packs",
    "metadata",
}

ALLOWED_NON_COMPILED_STATUSES = {"invalid", "unknown", "clarification_needed"}

SECRET_PATTERNS = (
    re.compile(r"sk-[A-Za-z0-9]"),
    re.compile(r"api[_-]?key", re.IGNORECASE),
    re.compile(r"password", re.IGNORECASE),
    re.compile(r"bearer\s+", re.IGNORECASE),
    re.compile(r"https?://", re.IGNORECASE),
    re.compile(r"@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
)


def _load(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(data, list)
    assert data
    assert all(isinstance(item, dict) for item in data)
    return data


def _all_fixtures() -> list[dict[str, Any]]:
    fixtures: list[dict[str, Any]] = []
    for path in FIXTURE_FILES.values():
        fixtures.extend(_load(path))
    return fixtures


def _all_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        strings: list[str] = []
        for key, item in value.items():
            strings.extend(_all_strings(key))
            strings.extend(_all_strings(item))
        return strings
    if isinstance(value, list):
        strings = []
        for item in value:
            strings.extend(_all_strings(item))
        return strings
    return []


def test_fixture_files_exist_and_are_valid_json() -> None:
    assert (FIXTURE_ROOT / "README.md").exists()

    for path in FIXTURE_FILES.values():
        assert path.exists()
        fixtures = _load(path)
        assert all(set(fixture) == TOP_LEVEL_KEYS for fixture in fixtures)


def test_all_fixtures_are_synthetic_and_contain_no_secrets() -> None:
    for fixture in _all_fixtures():
        assert fixture["fixture_id"].startswith("intent-")
        assert fixture["human_input_ref"]["input_id"].startswith("humaninput-")
        assert fixture["human_input_ref"]["actor_id"].startswith("fixture-actor")
        assert fixture["human_input_ref"]["shell_id"] == "lima-test-shell"

        serialized_strings = _all_strings(fixture)
        assert any("fixture" in item for item in serialized_strings)
        violations = [
            string
            for string in serialized_strings
            for pattern in SECRET_PATTERNS
            if pattern.search(string)
        ]
        assert violations == []


def test_valid_typed_intent_fixtures_include_required_explicit_metadata() -> None:
    for fixture in _load(FIXTURE_FILES["typed"]):
        explicit_metadata = fixture["explicit_metadata"]

        assert fixture["fixture_type"] == "typed_intent"
        assert REQUIRED_EXPLICIT_METADATA_FIELDS <= set(explicit_metadata)
        assert explicit_metadata["typed_args"]
        assert explicit_metadata["evidence_refs"]
        assert explicit_metadata["requested_tool_packs"]


def test_valid_typed_intent_fixtures_include_expected_intent_envelope() -> None:
    for fixture in _load(FIXTURE_FILES["typed"]):
        envelope = fixture["expected_intent_envelope"]
        explicit_metadata = fixture["explicit_metadata"]

        assert isinstance(envelope, dict)
        assert REQUIRED_ENVELOPE_FIELDS <= set(envelope)
        assert envelope["source_input_id"] == fixture["human_input_ref"]["input_id"]
        assert envelope["actor_id"] == fixture["human_input_ref"]["actor_id"]
        assert envelope["shell_id"] == fixture["human_input_ref"]["shell_id"]
        assert envelope["intent_type"] == explicit_metadata["intent_type"]
        assert envelope["typed_args"] == explicit_metadata["typed_args"]
        assert envelope["risk_class"] == explicit_metadata["risk_class"]
        assert envelope["required_evidence"] == explicit_metadata["evidence_refs"]
        assert envelope["required_approval_level"] == explicit_metadata["approval_level"]
        assert envelope["proposed_tool_packs"] == explicit_metadata["requested_tool_packs"]
        assert envelope["metadata"]["source"] == "explicit_metadata"


def test_invalid_missing_metadata_fixtures_do_not_imply_envelope_creation() -> None:
    for fixture in _load(FIXTURE_FILES["invalid"]):
        explicit_metadata = fixture["explicit_metadata"]

        assert fixture["fixture_type"] == "invalid_missing_metadata"
        assert set(explicit_metadata) != REQUIRED_EXPLICIT_METADATA_FIELDS
        assert not REQUIRED_EXPLICIT_METADATA_FIELDS <= set(explicit_metadata)
        assert fixture["expected_intent_envelope"] is None
        assert fixture["expected_status"] in ALLOWED_NON_COMPILED_STATUSES
        assert "GuardianDecision" in fixture["notes"]
        assert "raw_text" in fixture["expected_reason"] or "metadata" in fixture["expected_reason"]


def test_clarification_needed_fixtures_require_clarification() -> None:
    for fixture in _load(FIXTURE_FILES["clarification"]):
        assert fixture["fixture_type"] == "clarification_needed"
        assert fixture["expected_status"] == "clarification_needed"
        assert fixture["expected_intent_envelope"] is None
        assert "clarif" in fixture["expected_reason"].lower()


def test_safety_critical_fixtures_mark_critical_risk_and_no_authorization() -> None:
    for fixture in _load(FIXTURE_FILES["safety"]):
        explicit_metadata = fixture["explicit_metadata"]
        envelope = fixture["expected_intent_envelope"]
        safety_text = " ".join(
            [
                fixture["expected_reason"],
                fixture["notes"],
                json.dumps(envelope.get("metadata", {}), sort_keys=True),
            ]
        ).lower()

        assert fixture["fixture_type"] == "safety_critical_intent"
        assert explicit_metadata["risk_class"] in {"critical", "safety_critical"}
        assert envelope["risk_class"] in {"critical", "safety_critical"}
        assert "no authorization" in safety_text
        assert "no auto-approval" in safety_text
        assert "guardian/policy/approval review" in safety_text
        assert envelope["metadata"]["no_auto_approval"] is True
        assert envelope["required_approval_level"] in {
            "operator_pin",
            "breakglass",
            "guardian_review",
        }


def test_raw_text_is_inert_and_not_source_of_intent() -> None:
    for fixture in _all_fixtures():
        assert isinstance(fixture["raw_text"], str)
        assert fixture["raw_text"]

        envelope = fixture["expected_intent_envelope"]
        if envelope is None:
            continue

        assert envelope["metadata"]["source"] == "explicit_metadata"
        assert "raw_text" not in envelope["metadata"]
        assert envelope["intent_type"] == fixture["explicit_metadata"]["intent_type"]
        assert envelope["typed_args"] == fixture["explicit_metadata"]["typed_args"]


def test_no_guardian_decision_expected_or_created_in_fixture_shape() -> None:
    forbidden_keys = {
        "guardian_decision",
        "guardian_decision_id",
        "decision_id",
        "approval_metadata",
        "approval_id",
        "policy_decision",
        "execution_id",
    }

    for fixture in _all_fixtures():
        serialized_keys = {
            key
            for item in _all_strings(fixture)
            for key in forbidden_keys
            if item == key
        }
        assert serialized_keys == set()

        envelope = fixture["expected_intent_envelope"]
        if envelope is not None:
            assert forbidden_keys.isdisjoint(envelope)
            assert forbidden_keys.isdisjoint(envelope["metadata"])


def test_fixture_test_file_does_not_import_sparkbot_or_runtime_services() -> None:
    path = Path(__file__)
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imported_modules: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_modules.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            imported_modules.append(node.module)

    imported_text = "\n".join(imported_modules).lower()
    forbidden_imports = {
        "sparkbot",
        "fastapi",
        "websocket",
        "requests",
        "httpx",
        "aiohttp",
        "sqlite",
        "sqlalchemy",
        "openai",
        "anthropic",
        "google.generativeai",
    }

    assert all(forbidden not in imported_text for forbidden in forbidden_imports)
