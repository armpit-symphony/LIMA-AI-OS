"""Shape tests for synthetic fake GuardianDecision fixture artifacts."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


FIXTURE_ROOT = Path(__file__).parent / "fixtures" / "fake_guardian_decisions"

FIXTURE_FILES = {
    "allow": FIXTURE_ROOT / "allow_test_only_decision_fixtures.json",
    "deny": FIXTURE_ROOT / "deny_test_only_decision_fixtures.json",
    "needs_approval": FIXTURE_ROOT / "needs_approval_test_only_decision_fixtures.json",
    "blocked": FIXTURE_ROOT / "blocked_test_only_decision_fixtures.json",
    "safety_critical": FIXTURE_ROOT / "safety_critical_decision_fixtures.json",
    "expired_revoked_superseded": (
        FIXTURE_ROOT / "expired_revoked_superseded_decision_fixtures.json"
    ),
}

TOP_LEVEL_KEYS = {
    "fixture_id",
    "fixture_type",
    "guardian_request_ref",
    "explicit_decision",
    "expected_fake_guardian_decision",
    "expected_status",
    "expected_reason",
    "privacy_class",
    "redaction_class",
    "notes",
}

REQUIRED_FAKE_DECISION_FIELDS = {
    "decision_id",
    "request_id",
    "lineage_id",
    "decision_status",
    "risk_class",
    "action_type",
    "allow",
    "requires_approval",
    "denied",
    "blocked",
    "reason",
    "policy_refs",
    "approval_requirement_ref",
    "approval_ref",
    "tool_pack_refs",
    "safety_flags",
    "privacy_class",
    "redaction_class",
    "expires_at",
    "supersedes_decision_id",
    "metadata",
}

ALLOWED_TEST_ONLY_STATUSES = {
    "allow_test_only",
    "deny_test_only",
    "needs_approval_test_only",
    "blocked_test_only",
    "needs_review_test_only",
    "expired_test_only",
    "revoked_test_only",
    "superseded_test_only",
}

FORBIDDEN_KEYS = {
    "approval_metadata",
    "approval_granted",
    "approval_id",
    "execution_id",
    "audit_record_id",
    "audit_persistence",
    "real_guardian_decision",
    "production_authorization",
}

SECRET_PATTERNS = (
    re.compile(r"\bsk-[A-Za-z0-9]"),
    re.compile(r"api[_-]?key", re.IGNORECASE),
    re.compile(r"password", re.IGNORECASE),
    re.compile(r"bearer\s+", re.IGNORECASE),
    re.compile(r"https?://", re.IGNORECASE),
    re.compile(r"www\.", re.IGNORECASE),
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


def _decision(fixture: dict[str, Any]) -> dict[str, Any]:
    decision = fixture["expected_fake_guardian_decision"]
    assert isinstance(decision, dict)
    return decision


def test_fake_guardian_decision_fixture_files_exist_and_are_valid_json() -> None:
    assert (FIXTURE_ROOT / "README.md").exists()

    for path in FIXTURE_FILES.values():
        assert path.exists()
        fixtures = _load(path)
        assert all(set(fixture) == TOP_LEVEL_KEYS for fixture in fixtures)


def test_all_fake_guardian_decision_fixtures_are_synthetic_and_secret_free() -> None:
    for fixture in _all_fixtures():
        decision = _decision(fixture)
        metadata = decision["metadata"]

        assert fixture["fixture_id"].startswith("fake-guardian-decision-")
        assert decision["decision_id"].startswith("fake-guardian-decision-")
        assert fixture["guardian_request_ref"]["request_id"].startswith("guardian-request-")
        assert metadata["fixture_only"] is True
        assert metadata["fake_guardian_decision_only"] is True
        assert metadata["not_production_authorization"] is True

        serialized_strings = _all_strings(fixture)
        assert any("Synthetic" in item for item in serialized_strings)
        violations = [
            string
            for string in serialized_strings
            for pattern in SECRET_PATTERNS
            if pattern.search(string)
        ]
        assert violations == []


def test_each_fake_decision_includes_required_shape_fields() -> None:
    for fixture in _all_fixtures():
        decision = _decision(fixture)

        assert set(decision) == REQUIRED_FAKE_DECISION_FIELDS
        assert decision["privacy_class"] == fixture["privacy_class"]
        assert decision["redaction_class"] == fixture["redaction_class"]
        assert decision["decision_status"] == fixture["expected_status"]
        assert isinstance(decision["policy_refs"], list)
        assert isinstance(decision["tool_pack_refs"], list)
        assert isinstance(decision["safety_flags"], list)
        assert isinstance(decision["metadata"], dict)


def test_all_decision_statuses_are_test_only() -> None:
    for fixture in _all_fixtures():
        decision = _decision(fixture)
        status = decision["decision_status"]

        assert status in ALLOWED_TEST_ONLY_STATUSES
        assert status.endswith("_test_only")
        assert fixture["expected_status"] == status


def test_allow_test_only_fixtures_are_not_production_authorization() -> None:
    for fixture in _load(FIXTURE_FILES["allow"]):
        decision = _decision(fixture)
        notes = fixture["notes"]

        assert decision["decision_status"] == "allow_test_only"
        assert decision["allow"] is True
        assert decision["requires_approval"] is False
        assert decision["denied"] is False
        assert decision["blocked"] is False
        assert decision["metadata"]["not_production_authorization"] is True
        assert decision["metadata"]["no_execution"] is True
        assert decision["metadata"]["no_approval_metadata"] is True
        assert "not production authorization" in notes
        assert "no execution" in notes


def test_needs_approval_test_only_fixtures_do_not_create_approval() -> None:
    for fixture in _load(FIXTURE_FILES["needs_approval"]):
        decision = _decision(fixture)
        keys = _all_keys(fixture)
        notes = fixture["notes"]

        assert decision["decision_status"] == "needs_approval_test_only"
        assert decision["allow"] is False
        assert decision["requires_approval"] is True
        assert decision["approval_requirement_ref"]
        assert decision["approval_ref"]
        assert decision["approval_ref"].startswith("fixture-approval-ref:")
        assert decision["metadata"]["approval_ref_is_reference_only"] is True
        assert decision["metadata"]["no_approval_metadata"] is True
        assert decision["metadata"]["no_execution"] is True
        assert "approval_metadata" not in keys
        assert "approval_granted" not in keys
        assert "no approval is granted" in notes or "not approved" in notes
        assert "ApprovalMetadata is created" in notes


def test_blocked_test_only_fixtures_include_safety_flags_and_no_owner_override() -> None:
    for fixture in _load(FIXTURE_FILES["blocked"]):
        decision = _decision(fixture)

        assert decision["decision_status"] == "blocked_test_only"
        assert decision["allow"] is False
        assert decision["blocked"] is True
        assert decision["safety_flags"]
        assert decision["metadata"]["owner_autonomy_override_allowed"] is False
        assert decision["metadata"]["no_execution"] is True
        assert (
            "owner autonomy override" in fixture["notes"]
            or "override owner command" in fixture["notes"]
        )


def test_safety_critical_fixtures_do_not_auto_approve() -> None:
    for fixture in _load(FIXTURE_FILES["safety_critical"]):
        decision = _decision(fixture)
        metadata = decision["metadata"]

        assert decision["risk_class"] in {"critical", "safety_critical"}
        assert decision["allow"] is False
        assert metadata["no_auto_approval"] is True
        assert metadata["requires_later_guardian_policy_approval_review"] is True
        assert metadata["safety_critical_fake_decision_is_not_approval"] is True
        assert metadata["no_approval_metadata"] is True
        assert metadata["no_execution"] is True
        assert "safety-critical fake decision is not approval" in fixture["notes"]
        assert "later Guardian/policy/approval review" in fixture["notes"]


def test_expired_revoked_superseded_fixtures_are_not_executable() -> None:
    for fixture in _load(FIXTURE_FILES["expired_revoked_superseded"]):
        decision = _decision(fixture)
        status = decision["decision_status"]
        metadata = decision["metadata"]

        assert status in {"expired_test_only", "revoked_test_only", "superseded_test_only"}
        assert decision["allow"] is False
        assert metadata["not_executable"] is True
        assert metadata["not_production_authorization"] is True
        assert metadata["no_execution"] is True

        if status == "superseded_test_only":
            assert decision["supersedes_decision_id"]
            assert metadata["supersedes_decision_id_is_reference_only"] is True
            assert "supersedes_decision_id is reference only" in fixture["notes"]
        else:
            assert decision["supersedes_decision_id"] is None


def test_no_audit_persistence_or_real_guardian_decision_is_expected() -> None:
    for fixture in _all_fixtures():
        decision = _decision(fixture)
        metadata = decision["metadata"]
        keys = _all_keys(fixture)

        assert metadata["fake_guardian_decision_only"] is True
        assert metadata["no_audit_persistence"] is True
        assert metadata["no_execution"] is True
        assert FORBIDDEN_KEYS.isdisjoint(keys)


def test_requested_or_referenced_tool_packs_are_not_executed() -> None:
    for fixture in _all_fixtures():
        decision = _decision(fixture)
        metadata = decision["metadata"]

        assert metadata["no_execution"] is True
        assert "allowed_tool_packs" not in _all_keys(fixture)
        assert "granted_tool_packs" not in _all_keys(fixture)
        for tool_pack_ref in decision["tool_pack_refs"]:
            assert tool_pack_ref.startswith("fixture-tool-pack-ref:")
            assert "not-executed" in tool_pack_ref or "not-granted" in tool_pack_ref
