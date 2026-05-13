"""Deterministic test-only HumanInput to IntentEnvelope bridge harness.

This helper accepts synthetic HumanInput-shaped dictionaries and returns
IntentEnvelope-candidate-shaped dictionaries for tests only. It does not import
LIMA runtime modules, Sparkbot modules, adapters, tools, subprocesses, network
clients, browser clients, filesystem mutation helpers, or robotics APIs.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence


REQUIRED_INPUT_FIELDS = (
    "humaninput_ref",
    "synthetic",
    "test_only",
    "non_runtime",
    "raw_text",
    "source",
    "source_channel",
    "operator_intent",
    "requested_action",
    "provenance",
)

AUTHORITY_WORDS = (
    "admin",
    "administrator",
    "authorized",
    "operator",
    "phil",
    "trusted",
)

SHELL_WORDS = (
    "cmd",
    "command",
    "powershell",
    "shell",
    "subprocess",
    "terminal",
)

BROWSER_NETWORK_WORDS = (
    "api",
    "browser",
    "download",
    "fetch",
    "http",
    "internet",
    "network",
    "open url",
    "post request",
    "web",
)

FILE_MUTATION_WORDS = (
    "delete",
    "edit file",
    "file mutation",
    "modify file",
    "move file",
    "overwrite",
    "rename",
    "save file",
    "write file",
)

PHYSICAL_WORLD_WORDS = (
    "actuator",
    "drone",
    "humanoid",
    "iot",
    "motor",
    "physical-world",
    "robot",
    "robotics",
)


class IntentEnvelopeBridgeRejection(ValueError):
    """Raised when synthetic HumanInput cannot become a safe test candidate."""


@dataclass(frozen=True)
class IntentEnvelopeBridgeResult:
    status: str
    candidate: Mapping[str, Any] | None
    rejection_reasons: Sequence[str] = field(default_factory=tuple)
    metadata: Mapping[str, Any] = field(default_factory=dict)


def convert_synthetic_humaninput_to_intentenvelope_candidate(
    humaninput: Mapping[str, Any],
) -> dict[str, Any]:
    """Return a non-executable IntentEnvelope-candidate-shaped test dictionary."""

    rejection_reasons = validate_synthetic_humaninput(humaninput)
    if rejection_reasons:
        raise IntentEnvelopeBridgeRejection("; ".join(rejection_reasons))

    raw_text = _clean_text(humaninput["raw_text"])
    requested_action = _clean_text(humaninput["requested_action"])
    operator_intent = _clean_text(humaninput["operator_intent"])
    risk = classify_test_only_risk(raw_text=raw_text, requested_action=requested_action)
    approval_state = _approval_state_for_risk(risk)

    return {
        "candidate_id": f"test-only-intentenvelope-candidate:{humaninput['humaninput_ref']}",
        "candidate_kind": "intentenvelope_candidate",
        "synthetic": True,
        "test_only": True,
        "non_runtime": True,
        "source": humaninput["source"],
        "source_channel": humaninput["source_channel"],
        "operator_intent": operator_intent,
        "raw_text": raw_text,
        "normalized_request": _normalize_request(raw_text),
        "requested_action": requested_action,
        "risk_tier": risk,
        "approval_state": approval_state,
        "executable": False,
        "execution_allowed": False,
        "side_effects_allowed": False,
        "blocked_reason": _blocked_reason_for(risk, approval_state),
        "authority_context": {
            "operator_words_present": _contains_any(raw_text, AUTHORITY_WORDS),
            "operator_words_do_not_bypass_approval": True,
            "no_default_trust_bypass": True,
        },
        "provenance": _provenance(humaninput),
        "boundary_markers": {
            "not_authorization": True,
            "not_approval": True,
            "not_execution": True,
            "not_audit_persistence": True,
            "not_guardian_decision": True,
            "not_intentcompiler_runtime": True,
            "not_live_adapter": True,
            "not_sparkbot_integration": True,
        },
    }


def validate_synthetic_humaninput(humaninput: Mapping[str, Any]) -> tuple[str, ...]:
    """Return fail-closed rejection reasons for synthetic HumanInput test input."""

    reasons: list[str] = []
    missing = [field for field in REQUIRED_INPUT_FIELDS if field not in humaninput]
    if missing:
        reasons.append(f"missing required fields: {', '.join(sorted(missing))}")

    if humaninput.get("synthetic") is not True:
        reasons.append("synthetic marker must be true")
    if humaninput.get("test_only") is not True:
        reasons.append("test_only marker must be true")
    if humaninput.get("non_runtime") is not True:
        reasons.append("non_runtime marker must be true")

    raw_text = humaninput.get("raw_text")
    if not isinstance(raw_text, str) or not raw_text.strip():
        reasons.append("raw_text must be a non-empty string")

    for field_name in ("humaninput_ref", "source", "source_channel", "operator_intent", "requested_action"):
        value = humaninput.get(field_name)
        if not isinstance(value, str) or not value.strip():
            reasons.append(f"{field_name} must be a non-empty string")

    provenance = humaninput.get("provenance")
    if not isinstance(provenance, Mapping):
        reasons.append("provenance must be a mapping")
    else:
        if provenance.get("live_source") is not False:
            reasons.append("provenance.live_source must be false")
        if provenance.get("audit_persisted") is not False:
            reasons.append("provenance.audit_persisted must be false")
        if provenance.get("lineage_seed_ref") in (None, ""):
            reasons.append("provenance.lineage_seed_ref is required")

    if humaninput.get("live_runtime") is True:
        reasons.append("live_runtime marker is forbidden")
    if humaninput.get("production") is True:
        reasons.append("production marker is forbidden")
    if humaninput.get("approved") is True:
        reasons.append("approved marker is forbidden")

    return tuple(dict.fromkeys(reasons))


def classify_test_only_risk(*, raw_text: str, requested_action: str) -> str:
    """Conservatively classify requested action risk without executing anything."""

    combined = f"{raw_text} {requested_action}".lower()
    if _contains_any(combined, PHYSICAL_WORLD_WORDS):
        return "critical"
    if _contains_any(combined, SHELL_WORDS) or _contains_any(combined, FILE_MUTATION_WORDS):
        return "high"
    if _contains_any(combined, BROWSER_NETWORK_WORDS):
        return "medium"
    if "unknown" in combined or "ambiguous" in combined or "do something" in combined:
        return "unknown"
    return "low"


def validate_intentenvelope_candidate(candidate: Mapping[str, Any]) -> tuple[str, ...]:
    """Return validation errors for a test-only IntentEnvelope candidate."""

    required = {
        "source",
        "source_channel",
        "operator_intent",
        "raw_text",
        "normalized_request",
        "requested_action",
        "risk_tier",
        "approval_state",
        "executable",
        "execution_allowed",
        "side_effects_allowed",
        "blocked_reason",
        "provenance",
    }
    errors: list[str] = []
    missing = sorted(required - set(candidate))
    if missing:
        errors.append(f"missing candidate fields: {', '.join(missing)}")
    for marker in ("synthetic", "test_only", "non_runtime"):
        if candidate.get(marker) is not True:
            errors.append(f"{marker} marker must be true")
    for marker in ("executable", "execution_allowed", "side_effects_allowed"):
        if candidate.get(marker) is not False:
            errors.append(f"{marker} must be false")
    boundary = candidate.get("boundary_markers")
    if not isinstance(boundary, Mapping):
        errors.append("boundary_markers must be a mapping")
    elif not all(value is True for value in boundary.values()):
        errors.append("all boundary_markers must be true")
    return tuple(dict.fromkeys(errors))


def run_test_only_bridge_harness(
    humaninputs: Sequence[Mapping[str, Any]],
) -> tuple[IntentEnvelopeBridgeResult, ...]:
    """Convert synthetic HumanInput records without side effects."""

    results: list[IntentEnvelopeBridgeResult] = []
    for humaninput in humaninputs:
        try:
            candidate = convert_synthetic_humaninput_to_intentenvelope_candidate(humaninput)
            errors = validate_intentenvelope_candidate(candidate)
            if errors:
                results.append(
                    IntentEnvelopeBridgeResult(
                        status="rejected",
                        candidate=None,
                        rejection_reasons=errors,
                        metadata=_result_metadata(),
                    )
                )
            else:
                results.append(
                    IntentEnvelopeBridgeResult(
                        status="candidate_created_test_only",
                        candidate=candidate,
                        metadata=_result_metadata(),
                    )
                )
        except IntentEnvelopeBridgeRejection as exc:
            results.append(
                IntentEnvelopeBridgeResult(
                    status="rejected",
                    candidate=None,
                    rejection_reasons=tuple(str(exc).split("; ")),
                    metadata=_result_metadata(),
                )
            )
    return tuple(results)


def _approval_state_for_risk(risk: str) -> str:
    if risk == "low":
        return "proposed"
    if risk == "unknown":
        return "blocked_missing_metadata"
    return "approval_required"


def _blocked_reason_for(risk: str, approval_state: str) -> str:
    if approval_state == "proposed":
        return "candidate_non_executable_test_only"
    if approval_state == "blocked_missing_metadata":
        return "blocked_unknown_or_ambiguous_test_only_request"
    return f"{risk}_risk_requires_future_guardian_review"


def _provenance(humaninput: Mapping[str, Any]) -> dict[str, Any]:
    provenance = humaninput["provenance"]
    assert isinstance(provenance, Mapping)
    return {
        "humaninput_ref": humaninput["humaninput_ref"],
        "lineage_seed_ref": provenance["lineage_seed_ref"],
        "source_fixture": provenance.get("source_fixture"),
        "bridge_helper": "tests/support/test_only_humaninput_to_intentenvelope_bridge.py",
        "live_source": False,
        "audit_persisted": False,
        "test_only": True,
    }


def _normalize_request(raw_text: str) -> str:
    return " ".join(raw_text.strip().split()).lower()


def _clean_text(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise IntentEnvelopeBridgeRejection("text value must be a non-empty string")
    return " ".join(value.strip().split())


def _contains_any(text: str, words: Sequence[str]) -> bool:
    lower_text = text.lower()
    return any(word in lower_text for word in words)


def _result_metadata() -> dict[str, bool]:
    return {
        "test_only": True,
        "non_runtime": True,
        "no_authorization": True,
        "no_approval_enforcement": True,
        "no_execution": True,
        "no_audit_persistence": True,
        "no_external_side_effects": True,
    }
