"""Test-only shape harness for IntentEnvelope fixture artifacts."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


STATUS_VALID = "valid"
STATUS_INVALID = "invalid"
STATUS_CLARIFICATION_NEEDED = "clarification_needed"
STATUS_SAFETY_CRITICAL = "safety_critical"
STATUS_FAILED = "failed"

ALLOWED_NON_VALID_EXPECTED_STATUSES = {
    "invalid",
    "unknown",
    STATUS_CLARIFICATION_NEEDED,
}

REQUIRED_EXPLICIT_METADATA_FIELDS = (
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
)

REQUIRED_ENVELOPE_FIELDS = (
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
)


@dataclass(frozen=True)
class IntentEnvelopeFixtureResult:
    fixture_id: str
    fixture_type: str
    status: str
    expected_status: str
    envelope_shape_valid: bool
    missing_metadata_fields: Sequence[str] = field(default_factory=tuple)
    safety_notes: Sequence[str] = field(default_factory=tuple)
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class IntentEnvelopeFixtureReport:
    total: int
    valid: int
    invalid: int
    clarification_needed: int
    safety_critical: int
    failed: int
    results: Sequence[IntentEnvelopeFixtureResult] = field(default_factory=tuple)
    metadata: Mapping[str, Any] = field(default_factory=dict)


def load_intent_fixtures(fixtures_dir: Path) -> list[dict[str, Any]]:
    """Load synthetic IntentEnvelope fixture objects from JSON files."""

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


def validate_explicit_metadata(fixture: Mapping[str, Any]) -> Sequence[str]:
    """Return missing explicit metadata fields without inspecting inert text."""

    metadata = fixture.get("explicit_metadata")
    if not isinstance(metadata, Mapping):
        return REQUIRED_EXPLICIT_METADATA_FIELDS

    missing: list[str] = []
    for field_name in REQUIRED_EXPLICIT_METADATA_FIELDS:
        if field_name not in metadata or _is_missing(metadata[field_name]):
            missing.append(field_name)
    return tuple(missing)


def validate_expected_envelope_shape(fixture: Mapping[str, Any]) -> bool:
    """Validate expected IntentEnvelope-like shape from explicit fixture metadata."""

    envelope = fixture.get("expected_intent_envelope")
    explicit_metadata = fixture.get("explicit_metadata")
    human_input_ref = fixture.get("human_input_ref")
    if not (
        isinstance(envelope, Mapping)
        and isinstance(explicit_metadata, Mapping)
        and isinstance(human_input_ref, Mapping)
    ):
        return False
    if any(field_name not in envelope for field_name in REQUIRED_ENVELOPE_FIELDS):
        return False

    envelope_metadata = envelope.get("metadata")
    return (
        envelope.get("source_input_id") == human_input_ref.get("input_id")
        and envelope.get("actor_id") == human_input_ref.get("actor_id")
        and envelope.get("shell_id") == human_input_ref.get("shell_id")
        and envelope.get("intent_type") == explicit_metadata.get("intent_type")
        and envelope.get("typed_args") == explicit_metadata.get("typed_args")
        and envelope.get("risk_class") == explicit_metadata.get("risk_class")
        and envelope.get("required_evidence") == explicit_metadata.get("evidence_refs")
        and envelope.get("required_approval_level")
        == explicit_metadata.get("approval_level")
        and envelope.get("proposed_tool_packs")
        == explicit_metadata.get("requested_tool_packs")
        and isinstance(envelope_metadata, Mapping)
        and envelope_metadata.get("source") == "explicit_metadata"
    )


def run_intent_fixture_regression(
    fixtures: Sequence[Mapping[str, Any]],
) -> IntentEnvelopeFixtureReport:
    """Validate synthetic intent fixtures without compiling, approving, or executing."""

    results = tuple(_validate_fixture(fixture) for fixture in fixtures)
    return IntentEnvelopeFixtureReport(
        total=len(results),
        valid=sum(1 for result in results if result.status == STATUS_VALID),
        invalid=sum(1 for result in results if result.status == STATUS_INVALID),
        clarification_needed=sum(
            1 for result in results if result.status == STATUS_CLARIFICATION_NEEDED
        ),
        safety_critical=sum(
            1 for result in results if result.status == STATUS_SAFETY_CRITICAL
        ),
        failed=sum(1 for result in results if result.status == STATUS_FAILED),
        results=results,
        metadata={
            "fixture_harness": "intent_envelope_shape_only",
            "test_only": True,
            "explicit_metadata_only": True,
            "raw_text_inert": True,
            "non_production": True,
            "no_real_intent_compiler": True,
            "no_natural_language_inference": True,
            "no_guardian_decision": True,
            "no_execution": True,
        },
    )


def _validate_fixture(
    fixture: Mapping[str, Any],
) -> IntentEnvelopeFixtureResult:
    fixture_id = _required_str(fixture, "fixture_id")
    fixture_type = _required_str(fixture, "fixture_type")
    expected_status = _required_str(fixture, "expected_status")
    missing_metadata_fields = tuple(validate_explicit_metadata(fixture))
    envelope_shape_valid = validate_expected_envelope_shape(fixture)
    safety_notes = _safety_notes(fixture)

    status = _status_for_fixture(
        fixture=fixture,
        fixture_type=fixture_type,
        expected_status=expected_status,
        missing_metadata_fields=missing_metadata_fields,
        envelope_shape_valid=envelope_shape_valid,
        safety_notes=safety_notes,
    )

    return IntentEnvelopeFixtureResult(
        fixture_id=fixture_id,
        fixture_type=fixture_type,
        status=status,
        expected_status=expected_status,
        envelope_shape_valid=envelope_shape_valid,
        missing_metadata_fields=missing_metadata_fields,
        safety_notes=safety_notes,
        metadata={
            "test_only": True,
            "explicit_metadata_only": True,
            "raw_text_inert": True,
            "expected_envelope_present": isinstance(
                fixture.get("expected_intent_envelope"), Mapping
            ),
            "intent_envelope_is_not_authorization": True,
            "guardian_remains_mandatory": True,
        },
    )


def _status_for_fixture(
    *,
    fixture: Mapping[str, Any],
    fixture_type: str,
    expected_status: str,
    missing_metadata_fields: Sequence[str],
    envelope_shape_valid: bool,
    safety_notes: Sequence[str],
) -> str:
    if fixture_type == "typed_intent":
        if not missing_metadata_fields and envelope_shape_valid:
            return STATUS_VALID
        return STATUS_FAILED

    if fixture_type == "invalid_missing_metadata":
        if (
            missing_metadata_fields
            and expected_status in ALLOWED_NON_VALID_EXPECTED_STATUSES
            and fixture.get("expected_intent_envelope") is None
        ):
            return STATUS_INVALID
        return STATUS_FAILED

    if fixture_type == STATUS_CLARIFICATION_NEEDED:
        if (
            expected_status == STATUS_CLARIFICATION_NEEDED
            and fixture.get("expected_intent_envelope") is None
        ):
            return STATUS_CLARIFICATION_NEEDED
        return STATUS_FAILED

    if fixture_type == "safety_critical_intent":
        if (
            not missing_metadata_fields
            and envelope_shape_valid
            and _risk_class(fixture) in {"critical", STATUS_SAFETY_CRITICAL}
            and _has_later_guardian_review_note(safety_notes)
            and _has_no_authorization_note(safety_notes)
        ):
            return STATUS_SAFETY_CRITICAL
        return STATUS_FAILED

    return STATUS_FAILED


def _safety_notes(fixture: Mapping[str, Any]) -> tuple[str, ...]:
    fixture_type = str(fixture.get("fixture_type", ""))
    envelope = fixture.get("expected_intent_envelope")
    envelope_metadata: Mapping[str, Any] = {}
    if isinstance(envelope, Mapping) and isinstance(envelope.get("metadata"), Mapping):
        envelope_metadata = envelope["metadata"]

    notes = [
        "raw_text is inert fixture text only",
        "IntentEnvelope is not authorization",
        "Guardian remains mandatory",
        "no GuardianDecision is created",
    ]
    if fixture_type == "safety_critical_intent" or _risk_class(fixture) in {
        "critical",
        STATUS_SAFETY_CRITICAL,
    }:
        notes.extend(
            [
                "requires later Guardian/policy/approval review",
                "no authorization",
                "no auto-approval",
            ]
        )
    if envelope_metadata.get("no_auto_approval") is True:
        notes.append("expected envelope marks no_auto_approval")
    return tuple(dict.fromkeys(notes))


def _has_later_guardian_review_note(notes: Sequence[str]) -> bool:
    return any("Guardian/policy/approval review" in note for note in notes)


def _has_no_authorization_note(notes: Sequence[str]) -> bool:
    return any("no authorization" in note for note in notes)


def _risk_class(fixture: Mapping[str, Any]) -> str:
    metadata = fixture.get("explicit_metadata")
    if isinstance(metadata, Mapping):
        risk_class = metadata.get("risk_class")
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
