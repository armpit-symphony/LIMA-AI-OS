"""Non-authoritative candidate preview helper.

This module previews caller-provided candidate metadata only. It does not
bridge HumanInput, approve, execute, dispatch, persist, mutate files, call
external systems, or create live adapter behavior.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Final, Mapping


SAFE_STATUSES: Final[frozenset[str]] = frozenset({"proposed", "needs_review", "blocked"})
PROPOSED_ALIASES: Final[frozenset[str]] = frozenset({"proposed", "preview", "candidate"})
NEEDS_REVIEW_ALIASES: Final[frozenset[str]] = frozenset(
    {"needs_review", "review", "requires_review", "approval_required"}
)
BLOCKED_ALIASES: Final[frozenset[str]] = frozenset({"blocked", "invalid", "denied"})
CLAIM_MARKERS: Final[dict[str, tuple[str, ...]]] = {
    "authority_claim": (
        "phil",
        "operator",
        "admin",
        "trusted",
        "urgent",
        "override",
        "approve",
        "approved",
        "emergency",
    ),
    "execution_claim": ("execute", "execution", "executable", "run", "command"),
    "dispatch_claim": ("dispatch", "route", "send"),
    "persistence_claim": ("persist", "persistence", "audit", "database", "sqlite"),
    "shell_browser_network_claim": (
        "shell",
        "browser",
        "network",
        "http",
        "https",
        "socket",
        "urllib",
    ),
    "file_mutation_claim": ("file", "filesystem", "write", "mutate", "delete"),
    "background_work_claim": (
        "worker",
        "background",
        "queue",
        "daemon",
        "subprocess",
        "thread",
    ),
    "humaninput_bridge_claim": ("humaninput", "human", "input", "bridge", "intentenvelope"),
    "sparkbot_claim": ("sparkbot",),
    "live_adapter_claim": ("adapter", "live"),
    "robotics_physical_world_claim": (
        "robot",
        "robotics",
        "robo",
        "physical",
        "world",
        "drone",
        "hardware",
        "motion",
    ),
}
SAFE_CONTROL_KEYS: Final[frozenset[str]] = frozenset(
    {
        "approval_granted",
        "approval_state",
        "approved",
        "blocked_reason",
        "candidate_id",
        "candidate_status",
        "dispatch_allowed",
        "execution_allowed",
        "persistence_allowed",
        "preview_state",
        "provenance",
        "side_effects_allowed",
        "status",
        "summary",
    }
)


@dataclass(frozen=True)
class CandidatePreview:
    """Immutable safe preview for caller-provided candidate-like metadata."""

    preview_type: str
    preview_state: str
    status_reason: str
    input_present: bool
    normalized_status: str
    caller_provided_keys: tuple[str, ...]
    blocked_claims: tuple[str, ...]
    warnings: tuple[str, ...]
    non_authoritative: bool = True
    read_only: bool = True
    local_only: bool = True
    deterministic: bool = True
    safe_by_default: bool = True
    execution_allowed: bool = False
    side_effects_allowed: bool = False
    approval_granted: bool = False
    dispatch_allowed: bool = False
    persistence_allowed: bool = False
    phase_5_humaninput_runtime_bridge_gated: bool = True
    humaninput_bridge_active: bool = False
    sparkbot_wiring_active: bool = False
    live_adapter_active: bool = False
    external_calls_allowed: bool = False
    robotics_allowed: bool = False
    physical_world_allowed: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Return plain preview metadata for tests and documentation."""

        return asdict(self)


def preview_candidate(candidate_data: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Return a deterministic, non-authoritative candidate preview."""

    if not isinstance(candidate_data, Mapping):
        return _preview(
            preview_state="invalid",
            status_reason="missing_or_invalid_candidate_preview_input",
            input_present=False,
            normalized_status="blocked",
            caller_provided_keys=(),
            blocked_claims=(),
            warnings=("input_missing_or_invalid",),
        ).to_dict()

    blocked_claims = _blocked_claims(candidate_data)
    status, reason = _derive_status(candidate_data, blocked_claims)
    warnings = _warnings(candidate_data, status, blocked_claims)

    return _preview(
        preview_state=status,
        status_reason=reason,
        input_present=True,
        normalized_status=status,
        caller_provided_keys=_caller_provided_keys(candidate_data),
        blocked_claims=blocked_claims,
        warnings=warnings,
    ).to_dict()


def _preview(
    *,
    preview_state: str,
    status_reason: str,
    input_present: bool,
    normalized_status: str,
    caller_provided_keys: tuple[str, ...],
    blocked_claims: tuple[str, ...],
    warnings: tuple[str, ...],
) -> CandidatePreview:
    return CandidatePreview(
        preview_type="candidate_preview",
        preview_state=preview_state,
        status_reason=status_reason,
        input_present=input_present,
        normalized_status=normalized_status,
        caller_provided_keys=caller_provided_keys,
        blocked_claims=blocked_claims,
        warnings=warnings,
    )


def _derive_status(
    candidate_data: Mapping[str, Any], blocked_claims: tuple[str, ...]
) -> tuple[str, str]:
    if candidate_data.get("execution_allowed") is not False:
        return "blocked", "execution_not_allowed_for_candidate_preview"
    if candidate_data.get("side_effects_allowed") is not False:
        return "blocked", "side_effects_not_allowed_for_candidate_preview"
    if candidate_data.get("approval_granted") is True or candidate_data.get("approved") is True:
        return "blocked", "approval_not_allowed_for_candidate_preview"
    if str(candidate_data.get("approval_state", "")).strip().lower() == "approved":
        return "blocked", "approval_not_allowed_for_candidate_preview"
    if candidate_data.get("dispatch_allowed") is True:
        return "blocked", "dispatch_not_allowed_for_candidate_preview"
    if candidate_data.get("persistence_allowed") is True:
        return "blocked", "persistence_not_allowed_for_candidate_preview"
    if blocked_claims:
        return "blocked", "caller_provided_claim_not_allowed_for_candidate_preview"

    raw_status = str(
        candidate_data.get("candidate_status")
        or candidate_data.get("status")
        or candidate_data.get("preview_state")
        or ""
    ).strip().lower()
    if raw_status in PROPOSED_ALIASES:
        return "proposed", "non_authoritative_candidate_preview"
    if raw_status in NEEDS_REVIEW_ALIASES:
        return "needs_review", "candidate_preview_requires_review"
    if raw_status in BLOCKED_ALIASES:
        return "blocked", str(candidate_data.get("blocked_reason") or "candidate_preview_blocked")
    if raw_status in SAFE_STATUSES:
        return raw_status, "safe_candidate_preview_status"
    return "blocked", "unknown_candidate_preview_status_not_authoritative"


def _warnings(
    candidate_data: Mapping[str, Any], status: str, blocked_claims: tuple[str, ...]
) -> tuple[str, ...]:
    warnings: list[str] = []
    if blocked_claims:
        warnings.append("blocked_claims_present")
    if status == "blocked":
        warnings.append("preview_blocked")
    if "provenance" not in candidate_data:
        warnings.append("provenance_not_supplied_to_preview")
    return tuple(dict.fromkeys(warnings))


def _caller_provided_keys(candidate_data: Mapping[str, Any]) -> tuple[str, ...]:
    return tuple(sorted(key.strip() for key in candidate_data if isinstance(key, str) and key.strip()))


def _blocked_claims(value: Any) -> tuple[str, ...]:
    claims: list[str] = []
    _collect_blocked_claims(value, claims)
    return tuple(dict.fromkeys(sorted(claims)))


def _collect_blocked_claims(value: Any, claims: list[str]) -> None:
    if isinstance(value, Mapping):
        for nested_key, nested_value in value.items():
            if not (isinstance(nested_key, str) and nested_key in SAFE_CONTROL_KEYS):
                _collect_blocked_claims(nested_key, claims)
            _collect_blocked_claims(nested_value, claims)
        return
    if isinstance(value, (list, tuple, set, frozenset)):
        for item in value:
            _collect_blocked_claims(item, claims)
        return
    if not isinstance(value, str):
        return

    words = frozenset(_words(value))
    for claim_name, markers in CLAIM_MARKERS.items():
        if any(marker in words for marker in markers):
            claims.append(claim_name)


def _words(value: str) -> tuple[str, ...]:
    normalized = "".join(character.lower() if character.isalnum() else " " for character in value)
    return tuple(part for part in normalized.split() if part)
