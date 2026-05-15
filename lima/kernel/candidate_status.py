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


def _derive_status(candidate: Mapping[str, Any]) -> tuple[str, str]:
    if candidate.get("execution_allowed") is not False:
        return BLOCKED_STATUS, "execution_not_allowed_for_candidate"
    if candidate.get("side_effects_allowed") is not False:
        return BLOCKED_STATUS, "side_effects_not_allowed_for_candidate"
    if str(candidate.get("approval_state", "")).strip().lower() == "approved":
        return BLOCKED_STATUS, "candidate_cannot_be_approved_by_status_normalization"
    if candidate.get("approved") is True:
        return BLOCKED_STATUS, "candidate_cannot_be_approved_by_status_normalization"

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
