"""Non-executing candidate status normalization.

This module normalizes metadata for already-created intake candidates only.
It does not create bridge records, decision records, approvals, execution,
dispatch, persistence, or external side effects.
"""

from __future__ import annotations

from typing import Any, Final, Mapping


ALLOWED_CANDIDATE_STATUSES: Final[frozenset[str]] = frozenset(
    {"proposed", "needs_review", "blocked"}
)
BLOCKED_STATUS: Final[str] = "blocked"
NEEDS_REVIEW_STATUS: Final[str] = "needs_review"
PROPOSED_STATUS: Final[str] = "proposed"
REQUIRED_CANDIDATE_FIELDS: Final[tuple[str, ...]] = (
    "candidate_id",
    "intake_id",
    "source",
    "source_channel",
    "operator_intent",
    "normalized_request",
    "requested_action",
    "action_category",
    "risk_tier",
    "approval_state",
    "blocked_reason",
    "provenance",
    "executable",
    "execution_allowed",
    "side_effects_allowed",
)
PROVENANCE_AUTHORITY_CLAIM_MARKERS: Final[frozenset[str]] = frozenset(
    {"phil", "operator", "admin", "trusted", "urgent", "override", "approve", "approved"}
)


class CandidateStatusError(ValueError):
    """Raised when candidate status normalization cannot inspect metadata."""


def normalize_candidate_status(candidate: Mapping[str, Any]) -> dict[str, Any]:
    """Return a non-executing candidate copy with safe normalized status."""

    if not isinstance(candidate, Mapping):
        raise CandidateStatusError("candidate must be a mapping")

    normalized = dict(candidate)
    status, reason = _derive_status(candidate)

    normalized["candidate_status"] = status
    normalized["status_reason"] = reason
    normalized["executable"] = False
    normalized["execution_allowed"] = False
    normalized["side_effects_allowed"] = False
    normalized["approved"] = False
    normalized["approval_state"] = _safe_approval_state(candidate, status)
    normalized["phase_5_humaninput_runtime_bridge_gated"] = True
    normalized.setdefault("intent_envelope_created", False)
    normalized.setdefault("guardian_decision_created", False)

    if status == BLOCKED_STATUS:
        normalized["blocked_reason"] = reason or "candidate_not_execution_ready"

    return normalized


def validate_candidate(candidate: Mapping[str, Any]) -> dict[str, Any]:
    """Return a fail-closed validation result for candidate metadata."""

    if not isinstance(candidate, Mapping):
        raise CandidateStatusError("candidate must be a mapping")

    errors = _candidate_validation_errors(candidate)
    normalized = normalize_candidate_status(candidate)

    if errors:
        normalized["candidate_status"] = BLOCKED_STATUS
        normalized["approval_state"] = BLOCKED_STATUS
        normalized["blocked_reason"] = ";".join(errors)

    normalized["validation_state"] = "invalid" if errors else "valid"
    normalized["validation_errors"] = tuple(errors)
    normalized["executable"] = False
    normalized["execution_allowed"] = False
    normalized["side_effects_allowed"] = False
    normalized["approved"] = False
    normalized["phase_5_humaninput_runtime_bridge_gated"] = True
    return normalized


def _derive_status(candidate: Mapping[str, Any]) -> tuple[str, str]:
    if candidate.get("execution_allowed") is not False:
        return BLOCKED_STATUS, "execution_not_allowed_for_candidate"
    if candidate.get("side_effects_allowed") is not False:
        return BLOCKED_STATUS, "side_effects_not_allowed_for_candidate"
    if str(candidate.get("approval_state", "")).strip().lower() == "approved":
        return BLOCKED_STATUS, "candidate_cannot_be_approved_by_status_normalization"
    if candidate.get("approved") is True:
        return BLOCKED_STATUS, "candidate_cannot_be_approved_by_status_normalization"

    provenance_errors = _provenance_validation_errors(candidate.get("provenance"))
    if provenance_errors:
        return BLOCKED_STATUS, ";".join(provenance_errors)

    freshness = str(candidate.get("freshness", "fresh")).strip().lower()
    replay_status = str(candidate.get("replay_status", "not_replayed")).strip().lower()
    if freshness != "fresh":
        return BLOCKED_STATUS, "stale_candidate_not_execution_ready"
    if replay_status != "not_replayed":
        return BLOCKED_STATUS, "replayed_candidate_not_execution_ready"

    raw_status = str(
        candidate.get("candidate_status")
        or candidate.get("status")
        or candidate.get("approval_state")
        or ""
    ).strip().lower()

    if raw_status in {"proposed", "low"}:
        return PROPOSED_STATUS, "candidate_proposed_for_future_review"
    if raw_status in {"needs_review", "review", "approval_required", "requires_review"}:
        return NEEDS_REVIEW_STATUS, "candidate_requires_future_review"
    if raw_status == "blocked":
        return BLOCKED_STATUS, str(
            candidate.get("blocked_reason") or "candidate_not_execution_ready"
        )
    return BLOCKED_STATUS, "unknown_candidate_status_not_execution_ready"


def _safe_approval_state(candidate: Mapping[str, Any], status: str) -> str:
    raw_approval_state = str(candidate.get("approval_state", "")).strip().lower()
    if raw_approval_state == "approved":
        return BLOCKED_STATUS
    if status == PROPOSED_STATUS:
        return PROPOSED_STATUS
    if status == NEEDS_REVIEW_STATUS:
        return "approval_required"
    return BLOCKED_STATUS


def _candidate_validation_errors(candidate: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = [field_name for field_name in REQUIRED_CANDIDATE_FIELDS if field_name not in candidate]
    if missing:
        errors.append(f"missing_required_candidate_fields:{','.join(missing)}")

    errors.extend(_provenance_validation_errors(candidate.get("provenance")))

    if candidate.get("executable") is not False:
        errors.append("executable_must_be_false")
    if candidate.get("execution_allowed") is not False:
        errors.append("execution_allowed_must_be_false")
    if candidate.get("side_effects_allowed") is not False:
        errors.append("side_effects_allowed_must_be_false")
    if str(candidate.get("approval_state", "")).strip().lower() == "approved":
        errors.append("approval_state_must_not_be_approved")
    if candidate.get("approved") is True:
        errors.append("approved_flag_must_be_false")

    freshness = str(candidate.get("freshness", "fresh")).strip().lower()
    replay_status = str(candidate.get("replay_status", "not_replayed")).strip().lower()
    if freshness != "fresh":
        errors.append("candidate_must_not_be_stale")
    if replay_status != "not_replayed":
        errors.append("candidate_must_not_be_replayed")

    return errors


def _provenance_validation_errors(provenance: Any) -> list[str]:
    if not isinstance(provenance, Mapping) or not provenance:
        return ["provenance_missing_or_invalid"]

    errors: list[str] = []
    for key, value in provenance.items():
        if not isinstance(key, str) or not key.strip():
            errors.append("provenance_key_missing_or_invalid")
        if value is None:
            errors.append("provenance_value_missing_or_invalid")
        if _contains_authority_claim(key) or _contains_authority_claim(value):
            errors.append("provenance_authority_claim_not_allowed")

    return list(dict.fromkeys(errors))


def _contains_authority_claim(value: Any) -> bool:
    if isinstance(value, Mapping):
        return any(
            _contains_authority_claim(nested_key) or _contains_authority_claim(nested_value)
            for nested_key, nested_value in value.items()
        )
    if isinstance(value, (list, tuple, set, frozenset)):
        return any(_contains_authority_claim(item) for item in value)
    if not isinstance(value, str):
        return False

    folded = value.strip().lower()
    return any(marker in folded.split() for marker in PROVENANCE_AUTHORITY_CLAIM_MARKERS)
