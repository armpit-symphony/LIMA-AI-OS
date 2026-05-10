"""Shape tests for synthetic Guardian request fixture artifacts."""

from __future__ import annotations

import ast
import json
import re
from pathlib import Path
from typing import Any


FIXTURE_ROOT = Path(__file__).parent / "fixtures" / "guardian_requests"

FIXTURE_FILES = {
    "valid": FIXTURE_ROOT / "valid_guardian_request_fixtures.json",
    "invalid": FIXTURE_ROOT / "invalid_guardian_request_fixtures.json",
    "safety": FIXTURE_ROOT / "safety_critical_guardian_request_fixtures.json",
    "approval": FIXTURE_ROOT / "approval_required_guardian_request_fixtures.json",
}

TOP_LEVEL_KEYS = {
    "fixture_id",
    "fixture_type",
    "intent_envelope_ref",
    "explicit_request",
    "expected_guardian_request",
    "expected_status",
    "expected_reason",
    "privacy_class",
    "redaction_class",
    "notes",
}

REQUIRED_REQUEST_FIELDS = {
    "request_id",
    "lineage_id",
    "intent_envelope_ref",
    "actor_ref",
    "session_ref",
    "shell_id",
    "action_type",
    "risk_class",
    "requested_tool_packs",
    "target_ref",
    "typed_args",
    "evidence_refs",
    "privacy_class",
    "redaction_class",
    "approval_requirement_ref",
    "autonomy_context_ref",
    "reason",
    "confidence",
    "created_at",
    "metadata",
}

ALLOWED_INVALID_STATUSES = {"invalid", "needs_review", "clarification_needed"}

FORBIDDEN_KEYS = {
    "guardian_decision",
    "guardian_decision_id",
    "decision_id",
    "approval_metadata",
    "approval_id",
    "approval_granted",
    "allowed_tool_packs",
    "granted_tool_packs",
    "policy_decision",
    "execution_id",
    "audit_record_id",
}

SECRET_PATTERNS = (
    re.compile(r"\bsk-[A-Za-z0-9]"),
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


def _all_keys(value: Any) -> set[str]:
    if isinstance(value, dict):
        keys = set(value)
        for item in value.values():
            keys.update(_all_keys(item))
        return keys
    if isinstance(value, list):
        keys: set[str] = set()
        for item in value:
            keys.update(_all_keys(item))
        return keys
    return set()


def test_guardian_request_fixture_files_exist_and_are_valid_json() -> None:
    assert (FIXTURE_ROOT / "README.md").exists()

    for path in FIXTURE_FILES.values():
        assert path.exists()
        fixtures = _load(path)
        assert all(set(fixture) == TOP_LEVEL_KEYS for fixture in fixtures)


def test_all_guardian_request_fixtures_are_synthetic_and_contain_no_secrets() -> None:
    for fixture in _all_fixtures():
        assert fixture["fixture_id"].startswith("guardian-request-")
        assert fixture["intent_envelope_ref"]["source_fixture_id"].startswith(
            ("intent-", "intent-synthetic-")
        )

        serialized_strings = _all_strings(fixture)
        assert any("fixture" in item for item in serialized_strings)
        violations = [
            string
            for string in serialized_strings
            for pattern in SECRET_PATTERNS
            if pattern.search(string)
        ]
        assert violations == []


def test_valid_guardian_request_fixtures_include_required_request_fields() -> None:
    for fixture in _load(FIXTURE_FILES["valid"]):
        explicit_request = fixture["explicit_request"]
        expected_request = fixture["expected_guardian_request"]

        assert fixture["fixture_type"] == "valid_guardian_request"
        assert REQUIRED_REQUEST_FIELDS <= set(explicit_request)
        assert REQUIRED_REQUEST_FIELDS <= set(expected_request)
        assert explicit_request["requested_tool_packs"]
        assert isinstance(explicit_request["requested_tool_packs"], list)
        assert expected_request["metadata"]["source"] == "explicit_request"
        assert expected_request["metadata"]["no_approval"] is True
        assert expected_request["metadata"]["no_execution"] is True
        assert expected_request["metadata"]["no_audit_persistence"] is True


def test_invalid_guardian_request_fixtures_are_missing_required_fields() -> None:
    for fixture in _load(FIXTURE_FILES["invalid"]):
        explicit_request = fixture["explicit_request"]

        assert fixture["fixture_type"] == "invalid_guardian_request"
        assert fixture["expected_status"] in ALLOWED_INVALID_STATUSES
        assert fixture["expected_guardian_request"] is None
        assert (
            not REQUIRED_REQUEST_FIELDS <= set(explicit_request)
            or not isinstance(explicit_request.get("requested_tool_packs"), list)
        )
        assert "guardiandecision" in fixture["notes"].lower()
        assert "no execution" in fixture["notes"]


def test_safety_critical_guardian_request_fixtures_remain_non_authorizing() -> None:
    for fixture in _load(FIXTURE_FILES["safety"]):
        explicit_request = fixture["explicit_request"]
        expected_request = fixture["expected_guardian_request"]
        safety_text = " ".join(
            [
                fixture["expected_reason"],
                fixture["notes"],
                json.dumps(expected_request.get("metadata", {}), sort_keys=True),
            ]
        ).lower()

        assert fixture["fixture_type"] == "safety_critical_guardian_request"
        assert explicit_request["risk_class"] in {"critical", "safety_critical"}
        assert expected_request["risk_class"] in {"critical", "safety_critical"}
        assert "guardian/policy/approval review" in safety_text
        assert "no auto-approval" in safety_text
        assert "no_execution" in safety_text or "no execution" in safety_text
        assert expected_request["metadata"]["no_auto_approval"] is True
        assert expected_request["metadata"]["no_approval"] is True
        assert expected_request["metadata"]["no_execution"] is True


def test_approval_required_fixtures_do_not_create_approval_metadata() -> None:
    for fixture in _load(FIXTURE_FILES["approval"]):
        explicit_request = fixture["explicit_request"]
        expected_request = fixture["expected_guardian_request"]
        notes = fixture["notes"]

        assert fixture["fixture_type"] == "approval_required_guardian_request"
        assert explicit_request["approval_requirement_ref"]
        assert expected_request["approval_requirement_ref"]
        assert expected_request["metadata"]["approval_requirement_is_descriptive"] is True
        assert expected_request["metadata"]["no_approval"] is True
        assert "ApprovalMetadata is created" in notes
        assert "no approval is granted" in notes
        assert "no GuardianDecision is created" in notes
        assert FORBIDDEN_KEYS.isdisjoint(_all_keys(fixture))


def test_requested_tool_packs_are_requests_only() -> None:
    for fixture in _all_fixtures():
        keys = _all_keys(fixture)
        assert "requested_tool_packs" in keys
        assert "allowed_tool_packs" not in keys
        assert "granted_tool_packs" not in keys


def test_autonomy_context_ref_is_passive() -> None:
    for fixture in _all_fixtures():
        explicit_request = fixture["explicit_request"]
        expected_request = fixture["expected_guardian_request"]

        if expected_request is None:
            candidate_refs = [explicit_request.get("autonomy_context_ref", "")]
        else:
            candidate_refs = [
                explicit_request["autonomy_context_ref"],
                expected_request["autonomy_context_ref"],
            ]

        assert all("passive" in ref for ref in candidate_refs if ref)


def test_privacy_and_redaction_metadata_is_not_enforcement() -> None:
    for fixture in _all_fixtures():
        explicit_request = fixture["explicit_request"]

        assert explicit_request["privacy_class"] == fixture["privacy_class"]
        assert explicit_request["redaction_class"] == fixture["redaction_class"]
        assert "enforcement" not in explicit_request["privacy_class"]
        assert "enforcement" not in explicit_request["redaction_class"]

        expected_request = fixture["expected_guardian_request"]
        if expected_request is not None:
            assert expected_request["privacy_class"] == fixture["privacy_class"]
            assert expected_request["redaction_class"] == fixture["redaction_class"]


def test_no_guardian_decision_or_execution_expected_in_fixture_shape() -> None:
    for fixture in _all_fixtures():
        keys = _all_keys(fixture)
        assert FORBIDDEN_KEYS.isdisjoint(keys)
        serialized = "\n".join(_all_strings(fixture)).lower()
        assert "guardian_decision" not in serialized
        assert "no execution" in serialized or "no_execution" in serialized

        expected_request = fixture["expected_guardian_request"]
        if expected_request is not None:
            assert expected_request["metadata"].get("no_approval") is True
            assert expected_request["metadata"].get("no_execution") is True


def test_guardian_request_fixture_test_does_not_import_sparkbot_or_services() -> None:
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
        "stream_chat_with_tools",
        "execute_tool",
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
