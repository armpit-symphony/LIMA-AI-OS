"""Read-only runtime state inspection for non-executing candidates.

This module produces advisory snapshot metadata only. It does not create
candidates, bridge HumanInput, approve, execute, dispatch, persist, or call
external systems.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Final, Mapping


SAFE_STATUSES: Final[frozenset[str]] = frozenset({"proposed", "needs_review", "blocked"})
AUTHORITY_CLAIM_MARKERS: Final[frozenset[str]] = frozenset(
    {"phil", "operator", "admin", "trusted", "urgent", "override", "approve", "approved", "emergency"}
)


@dataclass(frozen=True)
class RuntimeStateSnapshot:
    """Immutable advisory snapshot for caller-provided candidate state."""

    inspection_state: str
    candidate_present: bool
    candidate_status: str
    status_reason: str
    provenance_present: bool
    provenance_state: str
    provenance_keys: tuple[str, ...]
    non_authoritative: bool = True
    advisory_only: bool = True
    read_only: bool = True
    deterministic: bool = True
    local_only: bool = True
    executable: bool = False
    execution_allowed: bool = False
    side_effects_allowed: bool = False
    approved: bool = False
    approval_state: str = "blocked"
    dispatch_allowed: bool = False
    persistence_allowed: bool = False
    phase_5_humaninput_runtime_bridge_gated: bool = True
    humaninput_runtime_bridge_present: bool = False
    sparkbot_wiring_present: bool = False
    live_adapter_present: bool = False
    intent_envelope_created: bool = False
    guardian_decision_created: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Return plain metadata for tests and documentation."""

        return asdict(self)


def inspect_runtime_state(candidate_state: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Return a deterministic, non-authoritative read-only state snapshot."""

    if not isinstance(candidate_state, Mapping):
        return _snapshot(
            inspection_state="invalid",
            candidate_present=False,
            candidate_status="blocked",
            status_reason="missing_or_invalid_candidate_state",
            provenance_present=False,
            provenance_state="invalid",
            provenance_keys=(),
        ).to_dict()

    provenance = candidate_state.get("provenance")
    provenance_present = isinstance(provenance, Mapping) and bool(provenance)
    provenance_errors = _provenance_errors(provenance)
    candidate_status, status_reason = _derive_candidate_status(candidate_state, provenance_errors)

    return _snapshot(
        inspection_state="valid" if candidate_status in {"proposed", "needs_review"} else "blocked",
        candidate_present=True,
        candidate_status=candidate_status,
        status_reason=status_reason,
        provenance_present=provenance_present,
        provenance_state="valid" if not provenance_errors else "invalid",
        provenance_keys=_provenance_keys(provenance),
    ).to_dict()


def _snapshot(
    *,
    inspection_state: str,
    candidate_present: bool,
    candidate_status: str,
    status_reason: str,
    provenance_present: bool,
    provenance_state: str,
    provenance_keys: tuple[str, ...],
) -> RuntimeStateSnapshot:
    return RuntimeStateSnapshot(
        inspection_state=inspection_state,
        candidate_present=candidate_present,
        candidate_status=candidate_status,
        status_reason=status_reason,
        provenance_present=provenance_present,
        provenance_state=provenance_state,
        provenance_keys=provenance_keys,
    )


def _derive_candidate_status(
    candidate_state: Mapping[str, Any], provenance_errors: tuple[str, ...]
) -> tuple[str, str]:
    if candidate_state.get("execution_allowed") is not False:
        return "blocked", "execution_not_allowed_for_runtime_state_inspection"
    if candidate_state.get("side_effects_allowed") is not False:
        return "blocked", "side_effects_not_allowed_for_runtime_state_inspection"
    if candidate_state.get("approved") is True:
        return "blocked", "approval_not_allowed_for_runtime_state_inspection"
    if str(candidate_state.get("approval_state", "")).strip().lower() == "approved":
        return "blocked", "approval_not_allowed_for_runtime_state_inspection"
    if candidate_state.get("dispatch_allowed") is True:
        return "blocked", "dispatch_not_allowed_for_runtime_state_inspection"
    if candidate_state.get("persistence_allowed") is True:
        return "blocked", "persistence_not_allowed_for_runtime_state_inspection"
    if _contains_authority_claim(candidate_state):
        return "blocked", "authority_claim_not_allowed_for_runtime_state_inspection"
    if provenance_errors:
        return "blocked", ";".join(provenance_errors)

    raw_status = str(
        candidate_state.get("candidate_status")
        or candidate_state.get("status")
        or candidate_state.get("approval_state")
        or ""
    ).strip().lower()
    if raw_status in SAFE_STATUSES:
        if raw_status == "blocked":
            return "blocked", str(
                candidate_state.get("blocked_reason") or "candidate_not_execution_ready"
            )
        return raw_status, "read_only_runtime_state_snapshot"
    return "blocked", "unknown_candidate_status_not_execution_ready"


def _provenance_errors(provenance: Any) -> tuple[str, ...]:
    if not isinstance(provenance, Mapping) or not provenance:
        return ("provenance_missing_or_invalid",)

    errors: list[str] = []
    for key, value in provenance.items():
        if not isinstance(key, str) or not key.strip():
            errors.append("provenance_key_missing_or_invalid")
        if value is None:
            errors.append("provenance_value_missing_or_invalid")
    return tuple(dict.fromkeys(errors))


def _provenance_keys(provenance: Any) -> tuple[str, ...]:
    if not isinstance(provenance, Mapping):
        return ()
    return tuple(sorted(key.strip() for key in provenance if isinstance(key, str) and key.strip()))


def _contains_authority_claim(value: Any) -> bool:
    if isinstance(value, Mapping):
        return any(_contains_authority_claim(nested_value) for nested_value in value.values())
    if isinstance(value, (list, tuple, set, frozenset)):
        return any(_contains_authority_claim(item) for item in value)
    if not isinstance(value, str):
        return False

    folded = value.strip().lower()
    return any(marker in folded.split() for marker in AUTHORITY_CLAIM_MARKERS)
