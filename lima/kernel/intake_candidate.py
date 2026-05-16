"""Non-executing intake-to-candidate coordinator.

This module builds candidate metadata only. It does not parse natural
language, create IntentEnvelope records, create GuardianDecision records,
approve, execute, dispatch, persist, or call external systems.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Final, Mapping


SAFE_ACTION_CATEGORIES: Final[frozenset[str]] = frozenset(
    {"informational", "planning", "drafting"}
)
APPROVAL_REQUIRED_ACTION_CATEGORIES: Final[frozenset[str]] = frozenset(
    {
        "admin",
        "browser_network",
        "file_mutation",
        "model_call",
        "robotics_physical_world",
        "shell",
        "tool_call",
    }
)
RAW_INPUT_KEYS: Final[frozenset[str]] = frozenset(
    {"human_input", "raw_human_input", "raw_text", "transcript", "message_text"}
)


class IntakeCandidateError(ValueError):
    """Raised when intake metadata is not eligible for candidate construction."""


@dataclass(frozen=True)
class IntakeCandidate:
    candidate_id: str
    intake_id: str
    source: str
    source_channel: str
    operator_intent: str
    normalized_request: str
    requested_action: str
    action_category: str
    risk_tier: str
    approval_state: str
    blocked_reason: str
    provenance: Mapping[str, Any]
    executable: bool = False
    execution_allowed: bool = False
    side_effects_allowed: bool = False
    approved: bool = False
    needs_guardian_review: bool = True
    intent_envelope_created: bool = False
    guardian_decision_created: bool = False
    phase_5_humaninput_runtime_bridge_gated: bool = True
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_intake_candidate(intake: Mapping[str, Any]) -> dict[str, Any]:
    """Return non-executable candidate metadata from normalized synthetic intake."""

    _validate_intake(intake)
    action_category = _normalized_text(intake["action_category"], "action_category")
    risk_tier, approval_state, blocked_reason = _classify_candidate(intake, action_category)

    candidate = IntakeCandidate(
        candidate_id=f"candidate:{_normalized_text(intake['intake_id'], 'intake_id')}",
        intake_id=_normalized_text(intake["intake_id"], "intake_id"),
        source=_normalized_text(intake["source"], "source"),
        source_channel=_normalized_text(intake["source_channel"], "source_channel"),
        operator_intent=_normalized_text(intake["operator_intent"], "operator_intent"),
        normalized_request=_normalized_text(intake["normalized_request"], "normalized_request"),
        requested_action=_normalized_text(intake["requested_action"], "requested_action"),
        action_category=action_category,
        risk_tier=risk_tier,
        approval_state=approval_state,
        blocked_reason=blocked_reason,
        provenance=dict(intake["provenance"]),
        metadata={
            "source_boundary": "synthetic_normalized_intake",
            "candidate_kind": "non_executing_intake_candidate",
            "future_guardian_review_required": True,
            "operator_claims": tuple(intake.get("operator_claims", ())),
        },
    )
    return candidate.to_dict()


def _validate_intake(intake: Mapping[str, Any]) -> None:
    if not isinstance(intake, Mapping):
        raise IntakeCandidateError("intake must be a mapping")

    if any(raw_key in intake for raw_key in RAW_INPUT_KEYS):
        raise IntakeCandidateError("raw HumanInput-like payloads are not accepted")

    if intake.get("synthetic") is not True or intake.get("test_only") is not True:
        raise IntakeCandidateError("intake must be marked synthetic and test_only")

    required_fields = (
        "intake_id",
        "source",
        "source_channel",
        "operator_intent",
        "normalized_request",
        "requested_action",
        "action_category",
        "provenance",
    )
    missing = [field_name for field_name in required_fields if field_name not in intake]
    if missing:
        raise IntakeCandidateError(f"intake missing required fields: {', '.join(missing)}")

    for field_name in required_fields:
        if field_name == "provenance":
            continue
        _normalized_text(intake[field_name], field_name)

    provenance = intake["provenance"]
    _validate_provenance(provenance)


def _classify_candidate(intake: Mapping[str, Any], action_category: str) -> tuple[str, str, str]:
    freshness = str(intake.get("freshness", "fresh")).strip().lower()
    replay_status = str(intake.get("replay_status", "not_replayed")).strip().lower()

    if freshness != "fresh":
        return "blocked", "blocked", "stale_intake_not_execution_ready"
    if replay_status != "not_replayed":
        return "blocked", "blocked", "replayed_intake_not_execution_ready"
    if action_category in SAFE_ACTION_CATEGORIES:
        return "low", "proposed", "non_executable_candidate_requires_future_guardian_review"
    if action_category in APPROVAL_REQUIRED_ACTION_CATEGORIES:
        return "high", "approval_required", "risky_request_requires_future_guardian_review"
    return "blocked", "blocked", "unknown_action_category_not_execution_ready"


def _normalized_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise IntakeCandidateError(f"{field_name} must be a non-empty string")
    return value.strip().lower() if field_name == "action_category" else value.strip()


def _validate_provenance(provenance: Any) -> None:
    if not isinstance(provenance, Mapping) or not provenance:
        raise IntakeCandidateError("provenance must be a non-empty mapping")

    for key, value in provenance.items():
        if not isinstance(key, str) or not key.strip():
            raise IntakeCandidateError("provenance keys must be non-empty strings")
        if value is None:
            raise IntakeCandidateError("provenance values must not be missing")
