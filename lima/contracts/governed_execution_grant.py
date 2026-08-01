"""Bounded, single-use execution grant issued by the governed kernel.

A ``GovernedDecision`` can never authorize execution: its ``__post_init__``
rejects any execution flag and ``to_dict`` pins all three to ``False``. That
invariant is load-bearing and is deliberately left untouched here.

This module adds the one contract that *can* carry execution authority. It is a
separate type so that no existing consumer starts authorizing execution merely
because it received a decision. A grant is narrow on purpose:

* it names exactly one capability, tenant, worker, and action type;
* it is bound to the Guardian decision and governed decision that produced it;
* it is short-lived and single-use;
* and it never claims to be sufficient on its own. ``requires_operator_opt_in``
  is pinned ``True`` in v0.1, so a grant is a *necessary* condition for
  execution and never a sufficient one. An enforcer that has not been
  explicitly opted in by an operator must still deny.

Issuing a grant performs no execution, no provider call, and no side effect.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import hashlib
import json
from typing import Any, Mapping


GRANT_CONTRACT = "lima.governed_execution_grant"
GRANT_VERSION = "v0.1"
GRANT_MODE = "single_use_operator_gated"
MAX_TTL_SECONDS = 300

_FIELDS = frozenset(
    {
        "grant_contract",
        "grant_version",
        "grant_mode",
        "grant_id",
        "decision_id",
        "request_id",
        "guardian_decision_id",
        "policy_version",
        "policy_snapshot_hash",
        "guardian_binding_hash",
        "granted_capability",
        "bound_tenant_id",
        "bound_worker_id",
        "bound_action_type",
        "scope_hash",
        "nonce",
        "issued_at",
        "expires_at",
        "execution_allowed",
        "side_effects_allowed",
        "requires_operator_opt_in",
    }
)


@dataclass(frozen=True)
class GovernedExecutionGrant:
    """One bounded authorization to execute a single named capability."""

    grant_id: str
    decision_id: str
    request_id: str
    guardian_decision_id: str
    policy_version: str
    policy_snapshot_hash: str
    guardian_binding_hash: str
    granted_capability: str
    bound_tenant_id: str
    bound_worker_id: str
    bound_action_type: str
    scope_hash: str
    nonce: str
    issued_at: str
    expires_at: str
    side_effects_allowed: bool
    execution_allowed: bool = True
    requires_operator_opt_in: bool = True
    grant_contract: str = GRANT_CONTRACT
    grant_version: str = GRANT_VERSION
    grant_mode: str = GRANT_MODE

    def __post_init__(self) -> None:
        if self.execution_allowed is not True:
            raise ValueError("execution grant must allow execution")
        if self.requires_operator_opt_in is not True:
            raise ValueError(
                "v0.1 execution grants cannot waive the operator opt-in gate"
            )

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "GovernedExecutionGrant":
        if not isinstance(value, Mapping):
            raise ValueError("execution grant must be a mapping")
        unknown = sorted(set(value) - _FIELDS)
        missing = sorted(_FIELDS - set(value))
        if unknown or missing:
            raise ValueError("execution grant fields are invalid")
        grant = cls(
            grant_contract=_required_text(value.get("grant_contract"), "grant_contract"),
            grant_version=_required_text(value.get("grant_version"), "grant_version"),
            grant_mode=_required_text(value.get("grant_mode"), "grant_mode"),
            grant_id=_required_text(value.get("grant_id"), "grant_id"),
            decision_id=_required_text(value.get("decision_id"), "decision_id"),
            request_id=_required_text(value.get("request_id"), "request_id"),
            guardian_decision_id=_required_text(
                value.get("guardian_decision_id"),
                "guardian_decision_id",
            ),
            policy_version=_required_text(value.get("policy_version"), "policy_version"),
            policy_snapshot_hash=_hash_reference(
                value.get("policy_snapshot_hash"),
                "policy_snapshot_hash",
            ),
            guardian_binding_hash=_hash_reference(
                value.get("guardian_binding_hash"),
                "guardian_binding_hash",
            ),
            granted_capability=_required_text(
                value.get("granted_capability"),
                "granted_capability",
            ),
            bound_tenant_id=_required_text(value.get("bound_tenant_id"), "bound_tenant_id"),
            bound_worker_id=_required_text(value.get("bound_worker_id"), "bound_worker_id"),
            bound_action_type=_required_text(
                value.get("bound_action_type"),
                "bound_action_type",
            ),
            scope_hash=_hash_reference(value.get("scope_hash"), "scope_hash"),
            nonce=_required_text(value.get("nonce"), "nonce"),
            issued_at=_timestamp(value.get("issued_at"), "issued_at"),
            expires_at=_timestamp(value.get("expires_at"), "expires_at"),
            execution_allowed=_required_bool(
                value.get("execution_allowed"),
                "execution_allowed",
            ),
            side_effects_allowed=_required_bool(
                value.get("side_effects_allowed"),
                "side_effects_allowed",
            ),
            requires_operator_opt_in=_required_bool(
                value.get("requires_operator_opt_in"),
                "requires_operator_opt_in",
            ),
        )
        grant.validate()
        return grant

    def validate(self, *, now: datetime | None = None) -> None:
        if self.grant_contract != GRANT_CONTRACT:
            raise ValueError("execution grant contract is not supported")
        if self.grant_version != GRANT_VERSION:
            raise ValueError("execution grant version is not supported")
        if self.grant_mode != GRANT_MODE:
            raise ValueError("execution grant mode is not supported")

        issued = _parse_timestamp(self.issued_at, "issued_at")
        expires = _parse_timestamp(self.expires_at, "expires_at")
        if expires <= issued:
            raise ValueError("execution grant expires_at must follow issued_at")
        if expires - issued > timedelta(seconds=MAX_TTL_SECONDS):
            raise ValueError("execution grant lifetime is too broad")

        current = now or datetime.now(timezone.utc)
        if current.tzinfo is None:
            raise ValueError("execution grant validation clock must be timezone-aware")
        if expires <= current.astimezone(timezone.utc):
            raise ValueError("execution grant is expired")

    def validate_binding(
        self,
        *,
        request_id: str,
        decision_id: str,
        guardian_binding_hash: str,
        tenant_id: str,
        worker_id: str,
        action_type: str,
        capability: str,
    ) -> None:
        """Reject a grant presented against anything other than its own subject."""

        expected = {
            "request_id": request_id,
            "decision_id": decision_id,
            "guardian_binding_hash": guardian_binding_hash,
            "bound_tenant_id": tenant_id,
            "bound_worker_id": worker_id,
            "bound_action_type": action_type,
            "granted_capability": capability,
        }
        actual = {
            "request_id": self.request_id,
            "decision_id": self.decision_id,
            "guardian_binding_hash": self.guardian_binding_hash,
            "bound_tenant_id": self.bound_tenant_id,
            "bound_worker_id": self.bound_worker_id,
            "bound_action_type": self.bound_action_type,
            "granted_capability": self.granted_capability,
        }
        if actual != expected:
            raise ValueError("execution grant binding mismatch")

    @property
    def consumption_key(self) -> tuple[str, str, str, str]:
        """Identity an enforcer stores to make this grant single-use.

        The governed kernel deliberately keeps no state, so single-use
        enforcement belongs to whichever component honours the grant. This is
        the tuple it should reserve before permitting execution.
        """

        return (
            self.bound_tenant_id,
            self.bound_worker_id,
            self.grant_id,
            self.nonce,
        )

    @property
    def content_hash(self) -> str:
        canonical = json.dumps(
            self.to_dict(),
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        return f"sha256:{hashlib.sha256(canonical).hexdigest()}"

    def to_dict(self) -> dict[str, Any]:
        return {
            "grant_contract": self.grant_contract,
            "grant_version": self.grant_version,
            "grant_mode": self.grant_mode,
            "grant_id": self.grant_id,
            "decision_id": self.decision_id,
            "request_id": self.request_id,
            "guardian_decision_id": self.guardian_decision_id,
            "policy_version": self.policy_version,
            "policy_snapshot_hash": self.policy_snapshot_hash,
            "guardian_binding_hash": self.guardian_binding_hash,
            "granted_capability": self.granted_capability,
            "bound_tenant_id": self.bound_tenant_id,
            "bound_worker_id": self.bound_worker_id,
            "bound_action_type": self.bound_action_type,
            "scope_hash": self.scope_hash,
            "nonce": self.nonce,
            "issued_at": self.issued_at,
            "expires_at": self.expires_at,
            "execution_allowed": self.execution_allowed,
            "side_effects_allowed": self.side_effects_allowed,
            "requires_operator_opt_in": self.requires_operator_opt_in,
        }


def _required_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"execution grant {field_name} is required")
    return value.strip()


def _required_bool(value: Any, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"execution grant {field_name} must be a boolean")
    return value


def _hash_reference(value: Any, field_name: str) -> str:
    text = _required_text(value, field_name)
    prefix, separator, digest = text.partition(":")
    if (
        separator != ":"
        or prefix != "sha256"
        or len(digest) != 64
        or any(character not in "0123456789abcdef" for character in digest.lower())
    ):
        raise ValueError(f"execution grant {field_name} must be a SHA-256 reference")
    return f"sha256:{digest.lower()}"


def _timestamp(value: Any, field_name: str) -> str:
    text = _required_text(value, field_name)
    return _parse_timestamp(text, field_name).isoformat().replace("+00:00", "Z")


def _parse_timestamp(value: str, field_name: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(
            f"execution grant {field_name} must be an ISO timestamp"
        ) from exc
    if parsed.tzinfo is None:
        raise ValueError(f"execution grant {field_name} must include a timezone")
    return parsed.astimezone(timezone.utc)


__all__ = [
    "GRANT_CONTRACT",
    "GRANT_MODE",
    "GRANT_VERSION",
    "MAX_TTL_SECONDS",
    "GovernedExecutionGrant",
]
