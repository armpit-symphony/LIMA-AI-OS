"""Deterministic test-only HumanInput adapter harness.

This module validates synthetic fixture records and converts them into
HumanInput-shaped dictionaries for tests only. It does not import LIMA runtime
modules, Sparkbot modules, adapters, models, tools, subprocesses, or network
clients.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence


REQUIRED_RECORD_FIELDS = (
    "fixture_id",
    "boundary_id",
    "input_kind",
    "synthetic",
    "non_runtime",
    "content",
    "source",
    "actor",
    "session",
    "trust_context",
    "privacy",
    "lineage",
    "handoff",
    "capability_flags",
    "blocked_capabilities",
)

VOICE_REQUIRED_FIELDS = ("voice",)

ALLOWED_INPUT_KINDS = ("text", "voice_transcript")

FORBIDDEN_KEYS = {
    "authorization",
    "approval",
    "approval_token",
    "approved",
    "audit_record",
    "audit_persistence",
    "auth_lookup_result",
    "execute",
    "execution",
    "guardian_decision",
    "guardiandecision",
    "intent_envelope",
    "intentenvelope",
    "model_call",
    "robot_command",
    "sparkbot_route",
    "terminal_command",
    "tool_call",
    "trust_lookup_result",
}

REQUIRED_FALSE_FLAGS = (
    "can_parse_action",
    "can_call_model",
    "can_select_tools",
    "can_expose_tools",
    "can_execute_tools",
    "can_write_terminal",
    "can_call_robotics",
    "can_approve",
    "can_enforce_policy",
    "can_persist_audit",
    "can_perform_live_auth_session_trust_lookup",
    "can_import_sparkbot",
    "can_wire_sparkbot",
)


class HumanInputHarnessRejection(ValueError):
    """Raised when a fixture would escape the test-only HumanInput boundary."""


@dataclass(frozen=True)
class HumanInputHarnessResult:
    fixture_id: str
    input_kind: str
    status: str
    humaninput_shape: Mapping[str, Any] | None
    rejection_reasons: Sequence[str] = field(default_factory=tuple)
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class HumanInputHarnessReport:
    total: int
    converted: int
    rejected: int
    results: Sequence[HumanInputHarnessResult] = field(default_factory=tuple)
    metadata: Mapping[str, Any] = field(default_factory=dict)


def convert_synthetic_fixture_to_humaninput_shape(
    fixture: Mapping[str, Any],
) -> dict[str, Any]:
    """Convert one synthetic fixture into a HumanInput-shaped test dictionary."""

    rejection_reasons = validate_synthetic_fixture(fixture)
    if rejection_reasons:
        raise HumanInputHarnessRejection("; ".join(rejection_reasons))

    humaninput_shape: dict[str, Any] = {
        "input_id": f"test-only:{fixture['fixture_id']}",
        "boundary_id": fixture["boundary_id"],
        "input_kind": fixture["input_kind"],
        "synthetic": True,
        "test_only": True,
        "non_runtime": True,
        "content": dict(_mapping(fixture["content"], "content")),
        "source": dict(_mapping(fixture["source"], "source")),
        "actor": dict(_mapping(fixture["actor"], "actor")),
        "session": dict(_mapping(fixture["session"], "session")),
        "trust_context": dict(_mapping(fixture["trust_context"], "trust_context")),
        "privacy": dict(_mapping(fixture["privacy"], "privacy")),
        "lineage": dict(_mapping(fixture["lineage"], "lineage")),
        "handoff": dict(_mapping(fixture["handoff"], "handoff")),
        "capability_flags": dict(_mapping(fixture["capability_flags"], "capability_flags")),
        "blocked_capabilities": tuple(_sequence(fixture["blocked_capabilities"])),
        "harness_metadata": {
            "harness": "test_only_humaninput_adapter_harness",
            "deterministic": True,
            "synthetic_fixture_only": True,
            "humaninput_shape_only": True,
            "not_authorization": True,
            "no_intentenvelope": True,
            "no_guardiandecision": True,
            "no_approval": True,
            "no_enforcement": True,
            "no_execution": True,
            "no_audit_persistence": True,
            "no_live_lookup": True,
            "no_runtime_imports": True,
            "no_sparkbot_imports": True,
        },
    }

    if fixture["input_kind"] == "voice_transcript":
        humaninput_shape["voice"] = dict(_mapping(fixture["voice"], "voice"))

    return humaninput_shape


def validate_synthetic_fixture(fixture: Mapping[str, Any]) -> tuple[str, ...]:
    """Return fail-closed rejection reasons for one fixture."""

    reasons: list[str] = []
    missing_fields = [field for field in REQUIRED_RECORD_FIELDS if field not in fixture]
    if missing_fields:
        reasons.append(f"missing required fields: {', '.join(sorted(missing_fields))}")

    if fixture.get("input_kind") not in ALLOWED_INPUT_KINDS:
        reasons.append("input_kind is not allowed")

    if fixture.get("input_kind") == "voice_transcript":
        missing_voice_fields = [field for field in VOICE_REQUIRED_FIELDS if field not in fixture]
        if missing_voice_fields:
            reasons.append(f"missing voice fields: {', '.join(sorted(missing_voice_fields))}")

    if fixture.get("synthetic") is not True:
        reasons.append("synthetic marker must be true")
    if fixture.get("non_runtime") is not True:
        reasons.append("non_runtime marker must be true")

    reasons.extend(_validate_passive_sections(fixture))
    reasons.extend(_validate_capability_flags(fixture))
    reasons.extend(_validate_no_forbidden_keys(fixture))
    return tuple(dict.fromkeys(reasons))


def validate_humaninput_shape(shape: Mapping[str, Any]) -> tuple[str, ...]:
    """Return validation errors for a generated HumanInput-shaped dictionary."""

    required_shape_fields = {
        "input_id",
        "boundary_id",
        "input_kind",
        "synthetic",
        "test_only",
        "non_runtime",
        "content",
        "source",
        "actor",
        "session",
        "trust_context",
        "privacy",
        "lineage",
        "handoff",
        "capability_flags",
        "blocked_capabilities",
        "harness_metadata",
    }
    missing = sorted(required_shape_fields - set(shape))
    errors = [f"missing shape fields: {', '.join(missing)}"] if missing else []

    if shape.get("synthetic") is not True:
        errors.append("shape must remain synthetic")
    if shape.get("test_only") is not True:
        errors.append("shape must remain test_only")
    if shape.get("non_runtime") is not True:
        errors.append("shape must remain non_runtime")

    metadata = shape.get("harness_metadata")
    if not isinstance(metadata, Mapping):
        errors.append("harness_metadata must be a mapping")
    else:
        for marker in (
            "not_authorization",
            "no_intentenvelope",
            "no_guardiandecision",
            "no_approval",
            "no_enforcement",
            "no_execution",
            "no_audit_persistence",
            "no_runtime_imports",
            "no_sparkbot_imports",
        ):
            if metadata.get(marker) is not True:
                errors.append(f"{marker} marker must be true")

    errors.extend(_validate_no_forbidden_keys(shape))
    return tuple(dict.fromkeys(errors))


def run_test_only_humaninput_harness(
    fixtures: Sequence[Mapping[str, Any]],
) -> HumanInputHarnessReport:
    """Validate and convert fixture records without any external side effects."""

    results: list[HumanInputHarnessResult] = []
    for fixture in fixtures:
        fixture_id = str(fixture.get("fixture_id", ""))
        input_kind = str(fixture.get("input_kind", ""))
        try:
            humaninput_shape = convert_synthetic_fixture_to_humaninput_shape(fixture)
            shape_errors = validate_humaninput_shape(humaninput_shape)
            if shape_errors:
                results.append(
                    HumanInputHarnessResult(
                        fixture_id=fixture_id,
                        input_kind=input_kind,
                        status="rejected",
                        humaninput_shape=None,
                        rejection_reasons=shape_errors,
                        metadata=_result_metadata(),
                    )
                )
            else:
                results.append(
                    HumanInputHarnessResult(
                        fixture_id=fixture_id,
                        input_kind=input_kind,
                        status="converted_test_only",
                        humaninput_shape=humaninput_shape,
                        metadata=_result_metadata(),
                    )
                )
        except HumanInputHarnessRejection as exc:
            results.append(
                HumanInputHarnessResult(
                    fixture_id=fixture_id,
                    input_kind=input_kind,
                    status="rejected",
                    humaninput_shape=None,
                    rejection_reasons=tuple(str(exc).split("; ")),
                    metadata=_result_metadata(),
                )
            )

    return HumanInputHarnessReport(
        total=len(results),
        converted=sum(1 for result in results if result.status == "converted_test_only"),
        rejected=sum(1 for result in results if result.status == "rejected"),
        results=tuple(results),
        metadata={
            "test_only": True,
            "non_runtime": True,
            "deterministic": True,
            "synthetic_fixture_only": True,
            "humaninput_shape_only": True,
            "not_production_adapter_readiness": True,
            "no_sparkbot_imports": True,
            "no_runtime_imports": True,
            "no_external_side_effects": True,
        },
    )


def _validate_passive_sections(fixture: Mapping[str, Any]) -> list[str]:
    reasons: list[str] = []
    source = _optional_mapping(fixture.get("source"))
    actor = _optional_mapping(fixture.get("actor"))
    session = _optional_mapping(fixture.get("session"))
    trust_context = _optional_mapping(fixture.get("trust_context"))
    lineage = _optional_mapping(fixture.get("lineage"))
    handoff = _optional_mapping(fixture.get("handoff"))

    if source.get("live_route") is not False:
        reasons.append("source.live_route must be false")
    if source.get("sparkbot_wired") is not False:
        reasons.append("source.sparkbot_wired must be false")
    if actor.get("identity_verified") is not False:
        reasons.append("actor.identity_verified must be false")
    if actor.get("live_lookup_performed") is not False:
        reasons.append("actor.live_lookup_performed must be false")
    if session.get("live_session") is not False:
        reasons.append("session.live_session must be false")
    if session.get("auth_lookup_performed") is not False:
        reasons.append("session.auth_lookup_performed must be false")
    if session.get("trust_lookup_performed") is not False:
        reasons.append("session.trust_lookup_performed must be false")
    if trust_context.get("grants_trust") is not False:
        reasons.append("trust_context.grants_trust must be false")
    if trust_context.get("enforces_trust") is not False:
        reasons.append("trust_context.enforces_trust must be false")
    if trust_context.get("live_lookup_performed") is not False:
        reasons.append("trust_context.live_lookup_performed must be false")
    if lineage.get("audit_persisted") is not False:
        reasons.append("lineage.audit_persisted must be false")
    if lineage.get("spine_event_created") is not False:
        reasons.append("lineage.spine_event_created must be false")
    if handoff.get("next_boundary") != "future_intentenvelope":
        reasons.append("handoff.next_boundary must be future_intentenvelope")
    if handoff.get("authorizes_action") is not False:
        reasons.append("handoff.authorizes_action must be false")
    if handoff.get("approves_action") is not False:
        reasons.append("handoff.approves_action must be false")
    if handoff.get("executes_action") is not False:
        reasons.append("handoff.executes_action must be false")
    return reasons


def _validate_capability_flags(fixture: Mapping[str, Any]) -> list[str]:
    flags = _optional_mapping(fixture.get("capability_flags"))
    reasons: list[str] = []
    for flag in REQUIRED_FALSE_FLAGS:
        if flags.get(flag) is not False:
            reasons.append(f"capability_flags.{flag} must be false")
    return reasons


def _validate_no_forbidden_keys(value: Any) -> list[str]:
    found = sorted(FORBIDDEN_KEYS.intersection(_all_keys(value)))
    if found:
        return [f"forbidden keys present: {', '.join(found)}"]
    return []


def _all_keys(value: Any) -> set[str]:
    if isinstance(value, Mapping):
        keys = {str(key).lower() for key in value}
        for item in value.values():
            keys.update(_all_keys(item))
        return keys
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        keys: set[str] = set()
        for item in value:
            keys.update(_all_keys(item))
        return keys
    return set()


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise HumanInputHarnessRejection(f"{name} must be a mapping")
    return value


def _optional_mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sequence(value: Any) -> Sequence[Any]:
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return value
    raise HumanInputHarnessRejection("blocked_capabilities must be a sequence")


def _result_metadata() -> dict[str, bool]:
    return {
        "test_only": True,
        "non_runtime": True,
        "no_authorization": True,
        "no_approval": True,
        "no_enforcement": True,
        "no_execution": True,
        "no_audit_persistence": True,
    }
