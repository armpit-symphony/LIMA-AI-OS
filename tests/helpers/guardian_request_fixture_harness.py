"""Test-only shape harness for Guardian request fixture artifacts."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


STATUS_VALID = "valid"
STATUS_INVALID = "invalid"
STATUS_NEEDS_REVIEW = "needs_review"
STATUS_CLARIFICATION_NEEDED = "clarification_needed"
STATUS_SAFETY_CRITICAL = "safety_critical"
STATUS_APPROVAL_REQUIRED = "approval_required"
STATUS_FAILED = "failed"

ALLOWED_INVALID_EXPECTED_STATUSES = {
    STATUS_INVALID,
    STATUS_NEEDS_REVIEW,
    STATUS_CLARIFICATION_NEEDED,
}

REQUIRED_REQUEST_FIELDS = (
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
)

FORBIDDEN_SHAPE_FIELDS = {
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


@dataclass(frozen=True)
class GuardianRequestFixtureResult:
    fixture_id: str
    fixture_type: str
    status: str
    expected_status: str
    request_shape_valid: bool
    missing_request_fields: Sequence[str] = field(default_factory=tuple)
    safety_notes: Sequence[str] = field(default_factory=tuple)
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class GuardianRequestFixtureReport:
    total: int
    valid: int
    invalid: int
    needs_review: int
    safety_critical: int
    approval_required: int
    failed: int
    results: Sequence[GuardianRequestFixtureResult] = field(default_factory=tuple)
    metadata: Mapping[str, Any] = field(default_factory=dict)


def load_guardian_request_fixtures(fixtures_dir: Path) -> list[dict[str, Any]]:
    """Load synthetic Guardian request fixture objects from JSON files."""

    fixtures: list[dict[str, Any]] = []
    for path in sorted(fixtures_dir.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise ValueError(f"{path.name} must contain a JSON list")
        for item in data:
            if not isinstance(item, dict):
                raise ValueError(f"{path.name} contains a non-object fixture")
            fixtures.append(item)
    return fixtures


def validate_explicit_request(fixture: Mapping[str, Any]) -> Sequence[str]:
    """Return missing explicit request fields from fixture metadata only."""

    explicit_request = fixture.get("explicit_request")
    if not isinstance(explicit_request, Mapping):
        return REQUIRED_REQUEST_FIELDS

    missing: list[str] = []
    for field_name in REQUIRED_REQUEST_FIELDS:
        if field_name not in explicit_request or _is_missing(explicit_request[field_name]):
            missing.append(field_name)

    requested_tool_packs = explicit_request.get("requested_tool_packs")
    if "requested_tool_packs" not in missing and not isinstance(requested_tool_packs, list):
        missing.append("requested_tool_packs")
    return tuple(missing)


def validate_expected_guardian_request_shape(fixture: Mapping[str, Any]) -> bool:
    """Validate expected Guardian request shape without creating a decision."""

    expected_request = fixture.get("expected_guardian_request")
    explicit_request = fixture.get("explicit_request")
    if not isinstance(expected_request, Mapping) or not isinstance(
        explicit_request, Mapping
    ):
        return False
    if any(field_name not in expected_request for field_name in REQUIRED_REQUEST_FIELDS):
        return False
    if _contains_forbidden_shape_field(expected_request):
        return False
    if not isinstance(expected_request.get("requested_tool_packs"), list):
        return False

    expected_metadata = expected_request.get("metadata")
    return (
        _request_field_values_match(explicit_request, expected_request)
        and isinstance(expected_metadata, Mapping)
        and expected_metadata.get("source") == "explicit_request"
        and expected_metadata.get("no_approval") is True
        and expected_metadata.get("no_execution") is True
        and expected_metadata.get("no_audit_persistence") is True
    )


def run_guardian_request_fixture_regression(
    fixtures: Sequence[Mapping[str, Any]],
) -> GuardianRequestFixtureReport:
    """Validate synthetic Guardian request fixtures as test-only shapes."""

    results = tuple(_validate_fixture(fixture) for fixture in fixtures)
    return GuardianRequestFixtureReport(
        total=len(results),
        valid=sum(1 for result in results if result.status == STATUS_VALID),
        invalid=sum(1 for result in results if result.status == STATUS_INVALID),
        needs_review=sum(
            1
            for result in results
            if result.status in {STATUS_NEEDS_REVIEW, STATUS_CLARIFICATION_NEEDED}
        ),
        safety_critical=sum(
            1 for result in results if result.status == STATUS_SAFETY_CRITICAL
        ),
        approval_required=sum(
            1 for result in results if result.status == STATUS_APPROVAL_REQUIRED
        ),
        failed=sum(1 for result in results if result.status == STATUS_FAILED),
        results=results,
        metadata={
            "fixture_harness": "guardian_request_shape_only",
            "test_only": True,
            "fixtures_only": True,
            "guardian_request_is_not_decision": True,
            "guardian_request_is_not_approval": True,
            "requested_tool_packs_are_requests_only": True,
            "approval_requirement_ref_is_descriptive": True,
            "autonomy_context_ref_is_passive": True,
            "privacy_redaction_metadata_not_enforcement": True,
            "no_guardian_decision": True,
            "no_enforcement": True,
            "no_approval": True,
            "no_execution": True,
            "no_audit_persistence": True,
            "non_production": True,
        },
    )


def _validate_fixture(fixture: Mapping[str, Any]) -> GuardianRequestFixtureResult:
    fixture_id = _required_str(fixture, "fixture_id")
    fixture_type = _required_str(fixture, "fixture_type")
    expected_status = _required_str(fixture, "expected_status")
    missing_request_fields = tuple(validate_explicit_request(fixture))
    request_shape_valid = validate_expected_guardian_request_shape(fixture)
    safety_notes = _safety_notes(fixture)

    status = _status_for_fixture(
        fixture=fixture,
        fixture_type=fixture_type,
        expected_status=expected_status,
        missing_request_fields=missing_request_fields,
        request_shape_valid=request_shape_valid,
        safety_notes=safety_notes,
    )

    return GuardianRequestFixtureResult(
        fixture_id=fixture_id,
        fixture_type=fixture_type,
        status=status,
        expected_status=expected_status,
        request_shape_valid=request_shape_valid,
        missing_request_fields=missing_request_fields,
        safety_notes=safety_notes,
        metadata={
            "test_only": True,
            "expected_request_present": isinstance(
                fixture.get("expected_guardian_request"), Mapping
            ),
            "non_authorizing": True,
            "no_guardian_decision": True,
            "no_approval": True,
            "no_execution": True,
            "requested_tool_packs_are_requests_only": True,
        },
    )


def _status_for_fixture(
    *,
    fixture: Mapping[str, Any],
    fixture_type: str,
    expected_status: str,
    missing_request_fields: Sequence[str],
    request_shape_valid: bool,
    safety_notes: Sequence[str],
) -> str:
    if fixture_type == "valid_guardian_request":
        if not missing_request_fields and request_shape_valid and expected_status == STATUS_VALID:
            return STATUS_VALID
        return STATUS_FAILED

    if fixture_type == "invalid_guardian_request":
        if (
            missing_request_fields
            and expected_status in ALLOWED_INVALID_EXPECTED_STATUSES
            and fixture.get("expected_guardian_request") is None
        ):
            return expected_status
        return STATUS_FAILED

    if fixture_type == "safety_critical_guardian_request":
        if (
            not missing_request_fields
            and request_shape_valid
            and _risk_class(fixture) in {"critical", STATUS_SAFETY_CRITICAL}
            and _has_later_review_note(safety_notes)
            and _has_no_authorization_note(safety_notes)
        ):
            return STATUS_SAFETY_CRITICAL
        return STATUS_FAILED

    if fixture_type == "approval_required_guardian_request":
        if (
            not missing_request_fields
            and request_shape_valid
            and expected_status == STATUS_APPROVAL_REQUIRED
            and _has_descriptive_approval_ref(fixture)
            and not _contains_forbidden_shape_field(fixture)
        ):
            return STATUS_APPROVAL_REQUIRED
        return STATUS_FAILED

    return STATUS_FAILED


def _request_field_values_match(
    explicit_request: Mapping[str, Any],
    expected_request: Mapping[str, Any],
) -> bool:
    for field_name in REQUIRED_REQUEST_FIELDS:
        if expected_request.get(field_name) != explicit_request.get(field_name):
            if field_name != "metadata":
                return False
    return True


def _safety_notes(fixture: Mapping[str, Any]) -> tuple[str, ...]:
    fixture_type = str(fixture.get("fixture_type", ""))
    expected_status = str(fixture.get("expected_status", ""))
    notes_text = str(fixture.get("notes", ""))

    notes = [
        "Guardian request is not GuardianDecision",
        "Guardian request is not approval",
        "requested_tool_packs are requests only",
        "approval_requirement_ref is descriptive only",
        "autonomy_context_ref is passive only",
        "privacy/redaction metadata is not enforcement",
        "no authorization",
    ]

    if fixture_type == "safety_critical_guardian_request" or _risk_class(fixture) in {
        "critical",
        STATUS_SAFETY_CRITICAL,
    }:
        notes.append("requires later Guardian/policy/approval review")
        notes.append("no auto-approval")

    if fixture_type == "approval_required_guardian_request" or expected_status == (
        STATUS_APPROVAL_REQUIRED
    ):
        notes.append("approval_requirement_ref remains descriptive")
        notes.append("no approval is granted")

    if "no execution" in notes_text:
        notes.append("no execution")
    return tuple(dict.fromkeys(notes))


def _has_later_review_note(notes: Sequence[str]) -> bool:
    return any("Guardian/policy/approval review" in note for note in notes)


def _has_no_authorization_note(notes: Sequence[str]) -> bool:
    return any("no authorization" in note for note in notes)


def _has_descriptive_approval_ref(fixture: Mapping[str, Any]) -> bool:
    explicit_request = fixture.get("explicit_request")
    expected_request = fixture.get("expected_guardian_request")
    if not isinstance(explicit_request, Mapping) or not isinstance(
        expected_request, Mapping
    ):
        return False
    metadata = expected_request.get("metadata")
    return (
        isinstance(explicit_request.get("approval_requirement_ref"), str)
        and isinstance(expected_request.get("approval_requirement_ref"), str)
        and isinstance(metadata, Mapping)
        and metadata.get("approval_requirement_is_descriptive") is True
    )


def _contains_forbidden_shape_field(value: Any) -> bool:
    return bool(FORBIDDEN_SHAPE_FIELDS.intersection(_all_keys(value)))


def _all_keys(value: Any) -> set[str]:
    if isinstance(value, Mapping):
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


def _risk_class(fixture: Mapping[str, Any]) -> str:
    explicit_request = fixture.get("explicit_request")
    if isinstance(explicit_request, Mapping):
        risk_class = explicit_request.get("risk_class")
        if isinstance(risk_class, str):
            return risk_class
    return ""


def _is_missing(value: object) -> bool:
    return value is None or value == "" or value == [] or value == {}


def _required_str(fixture: Mapping[str, Any], key: str) -> str:
    value = fixture.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"{key} must be a non-empty string")
    return value
