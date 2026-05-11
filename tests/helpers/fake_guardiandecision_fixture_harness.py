"""Test-only harness for fake GuardianDecision fixture shape validation."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Sequence


ALLOWED_STATUSES = {
    "allow_test_only",
    "deny_test_only",
    "needs_approval_test_only",
    "blocked_test_only",
    "needs_review_test_only",
    "expired_test_only",
    "revoked_test_only",
    "superseded_test_only",
    "failed",
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

NON_EXECUTABLE_STATUSES = {
    "expired_test_only",
    "revoked_test_only",
    "superseded_test_only",
}


@dataclass(frozen=True)
class FakeGuardianDecisionFixtureResult:
    fixture_id: str
    fixture_type: str
    status: str
    expected_status: str
    decision_shape_valid: bool
    missing_decision_fields: Sequence[str] = field(default_factory=tuple)
    safety_notes: Sequence[str] = field(default_factory=tuple)
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class FakeGuardianDecisionFixtureReport:
    total: int
    allow_test_only: int
    deny_test_only: int
    needs_approval_test_only: int
    blocked_test_only: int
    needs_review_test_only: int
    expired_test_only: int
    revoked_test_only: int
    superseded_test_only: int
    safety_critical: int
    failed: int
    results: Sequence[FakeGuardianDecisionFixtureResult] = field(default_factory=tuple)
    metadata: Mapping[str, Any] = field(default_factory=dict)


def load_fake_guardiandecision_fixtures(fixtures_dir: Path) -> list[dict[str, Any]]:
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


def validate_fake_decision_shape(fixture: Mapping[str, Any]) -> Sequence[str]:
    decision = fixture.get("expected_fake_guardian_decision")
    if not isinstance(decision, Mapping):
        return tuple(sorted(REQUIRED_FAKE_DECISION_FIELDS))

    return tuple(sorted(REQUIRED_FAKE_DECISION_FIELDS - set(decision)))


def validate_test_only_status(fixture: Mapping[str, Any]) -> bool:
    decision = fixture.get("expected_fake_guardian_decision")
    if not isinstance(decision, Mapping):
        return False

    status = decision.get("decision_status")
    return isinstance(status, str) and status in ALLOWED_STATUSES and status.endswith("_test_only")


def run_fake_guardiandecision_fixture_regression(
    fixtures: Sequence[Mapping[str, Any]],
) -> FakeGuardianDecisionFixtureReport:
    results: list[FakeGuardianDecisionFixtureResult] = []
    counts = {status: 0 for status in ALLOWED_STATUSES}
    safety_critical = 0

    for fixture in fixtures:
        decision = fixture.get("expected_fake_guardian_decision")
        decision_map = decision if isinstance(decision, Mapping) else {}
        metadata = decision_map.get("metadata", {})
        metadata_map = metadata if isinstance(metadata, Mapping) else {}
        status_value = decision_map.get("decision_status")
        status = status_value if isinstance(status_value, str) else "failed"
        expected_status_value = fixture.get("expected_status")
        expected_status = expected_status_value if isinstance(expected_status_value, str) else "failed"
        missing_fields = validate_fake_decision_shape(fixture)
        shape_valid = len(missing_fields) == 0 and validate_test_only_status(fixture)
        notes = _safety_notes(fixture, decision_map, metadata_map, shape_valid)

        if status not in counts:
            status = "failed"
        counts[status] += 1

        if _is_safety_critical(fixture, decision_map):
            safety_critical += 1

        if not shape_valid or status != expected_status:
            counts["failed"] += 1

        results.append(
            FakeGuardianDecisionFixtureResult(
                fixture_id=str(fixture.get("fixture_id", "")),
                fixture_type=str(fixture.get("fixture_type", "")),
                status=status,
                expected_status=expected_status,
                decision_shape_valid=shape_valid,
                missing_decision_fields=missing_fields,
                safety_notes=tuple(notes),
                metadata=dict(metadata_map),
            )
        )

    return FakeGuardianDecisionFixtureReport(
        total=len(fixtures),
        allow_test_only=counts["allow_test_only"],
        deny_test_only=counts["deny_test_only"],
        needs_approval_test_only=counts["needs_approval_test_only"],
        blocked_test_only=counts["blocked_test_only"],
        needs_review_test_only=counts["needs_review_test_only"],
        expired_test_only=counts["expired_test_only"],
        revoked_test_only=counts["revoked_test_only"],
        superseded_test_only=counts["superseded_test_only"],
        safety_critical=safety_critical,
        failed=counts["failed"],
        results=tuple(results),
        metadata={
            "test_only": True,
            "fake_guardian_decision_only": True,
            "no_real_guardian_decision": True,
            "no_policy_evaluation": True,
            "no_approval_recording": True,
            "no_action_approval": True,
            "no_tool_or_model_calls": True,
            "no_audit_persistence": True,
            "no_sparkbot_calls": True,
            "no_raw_text_inference": True,
        },
    )


def _safety_notes(
    fixture: Mapping[str, Any],
    decision: Mapping[str, Any],
    metadata: Mapping[str, Any],
    shape_valid: bool,
) -> list[str]:
    status = decision.get("decision_status")
    notes: list[str] = []

    if not shape_valid:
        notes.append("fake decision shape invalid")

    if status == "allow_test_only":
        notes.append("allow_test_only is not production authorization")
        if metadata.get("no_execution") is True:
            notes.append("no execution")

    if status == "needs_approval_test_only":
        if decision.get("requires_approval") is True:
            notes.append("requires approval is not approval granted")
        approval_ref = decision.get("approval_ref")
        if metadata.get("approval_ref_is_reference_only") is True or (
            isinstance(approval_ref, str) and approval_ref.startswith("fixture-approval-ref:")
        ):
            notes.append("approval_ref is reference only")
        if metadata.get("no_approval_metadata") is True:
            notes.append("no ApprovalMetadata")

    if status == "blocked_test_only":
        notes.append("blocked_test_only is non-authorizing")
        if decision.get("safety_flags"):
            notes.append("safety flags present")
        if metadata.get("owner_autonomy_override_allowed") is False:
            notes.append("no owner autonomy override")

    if _is_safety_critical(fixture, decision):
        if decision.get("allow") is False:
            notes.append("safety-critical fake decision does not auto-approve")
        if metadata.get("requires_later_guardian_policy_approval_review") is True:
            notes.append("later Guardian/policy/approval review required")

    if status in NON_EXECUTABLE_STATUSES:
        if metadata.get("not_executable") is True:
            notes.append(f"{status} is not executable")
        if metadata.get("not_production_authorization") is True:
            notes.append(f"{status} is not production authorization")
        if status == "superseded_test_only" and metadata.get(
            "supersedes_decision_id_is_reference_only"
        ) is True:
            notes.append("supersedes_decision_id is reference only")

    return notes


def _is_safety_critical(fixture: Mapping[str, Any], decision: Mapping[str, Any]) -> bool:
    fixture_type = str(fixture.get("fixture_type", ""))
    risk_class = str(decision.get("risk_class", ""))
    safety_flags = decision.get("safety_flags", ())

    return (
        "safety_critical" in fixture_type
        or risk_class in {"critical", "safety_critical"}
        or (
            isinstance(safety_flags, Sequence)
            and not isinstance(safety_flags, str)
            and any("safety" in str(flag) for flag in safety_flags)
        )
    )
