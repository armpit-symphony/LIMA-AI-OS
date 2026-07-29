"""Reference-only binding to an upstream Guardian authority decision."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
from typing import Any, Mapping


BINDING_MODE = "reference_only_non_authorizing"
_FIELDS = frozenset(
    {
        "binding_mode",
        "decision_id",
        "request_id",
        "policy_version",
        "policy_snapshot_hash",
        "valid_for_action_ref",
        "decision_scope_hash",
        "bound_tenant_id",
        "bound_worker_id",
        "bound_action_type",
        "expires_at",
    }
)


@dataclass(frozen=True)
class GuardianDecisionReference:
    """Safe lineage fields copied from a separately verified Guardian decision.

    This reference never grants authority and is never used to select a policy
    semantic. It lets a trusted Supervisor prove that the LIMA decision it
    accepted was bound to the same Guardian decision, policy snapshot, request,
    payload, tenant, worker, action, and expiry that it verified upstream.
    """

    decision_id: str
    request_id: str
    policy_version: str
    policy_snapshot_hash: str
    valid_for_action_ref: str
    decision_scope_hash: str
    bound_tenant_id: str
    bound_worker_id: str
    bound_action_type: str
    expires_at: str
    binding_mode: str = BINDING_MODE

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "GuardianDecisionReference":
        if not isinstance(value, Mapping):
            raise ValueError("guardian_binding must be a mapping")
        unknown = sorted(set(value) - _FIELDS)
        missing = sorted(_FIELDS - set(value))
        if unknown or missing:
            raise ValueError("guardian_binding fields are invalid")
        reference = cls(
            binding_mode=_required_text(value.get("binding_mode"), "binding_mode"),
            decision_id=_required_text(value.get("decision_id"), "decision_id"),
            request_id=_required_text(value.get("request_id"), "request_id"),
            policy_version=_required_text(value.get("policy_version"), "policy_version"),
            policy_snapshot_hash=_hash_reference(
                value.get("policy_snapshot_hash"),
                "policy_snapshot_hash",
            ),
            valid_for_action_ref=_hash_reference(
                value.get("valid_for_action_ref"),
                "valid_for_action_ref",
            ),
            decision_scope_hash=_hash_reference(
                value.get("decision_scope_hash"),
                "decision_scope_hash",
            ),
            bound_tenant_id=_required_text(
                value.get("bound_tenant_id"),
                "bound_tenant_id",
            ),
            bound_worker_id=_required_text(
                value.get("bound_worker_id"),
                "bound_worker_id",
            ),
            bound_action_type=_required_text(
                value.get("bound_action_type"),
                "bound_action_type",
            ),
            expires_at=_timestamp(value.get("expires_at"), "expires_at"),
        )
        reference.validate()
        return reference

    def validate(self, *, now: datetime | None = None) -> None:
        if self.binding_mode != BINDING_MODE:
            raise ValueError("guardian_binding mode is not supported")
        current = now or datetime.now(timezone.utc)
        if current.tzinfo is None:
            raise ValueError("guardian_binding validation clock must be timezone-aware")
        if _parse_timestamp(self.expires_at) <= current.astimezone(timezone.utc):
            raise ValueError("guardian_binding is expired")

    def validate_request_binding(
        self,
        *,
        request_id: str,
        requested_action: str,
        trust_context: Mapping[str, Any],
    ) -> None:
        expected = {
            "request_id": request_id,
            "bound_action_type": requested_action,
        }
        actual = {
            "request_id": self.request_id,
            "bound_action_type": self.bound_action_type,
        }
        if actual != expected:
            raise ValueError("guardian_binding request or action mismatch")

        trust_expected = {
            "authenticated_tenant_id": self.bound_tenant_id,
            "worker_id": self.bound_worker_id,
            "guardian_decision_id": self.decision_id,
            "guardian_policy_version": self.policy_version,
            "request_hash": self.valid_for_action_ref,
            "payload_hash": self.decision_scope_hash,
        }
        if any(trust_context.get(key) != value for key, value in trust_expected.items()):
            raise ValueError("guardian_binding trust context mismatch")

    @property
    def content_hash(self) -> str:
        canonical = json.dumps(
            self.to_dict(),
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        return f"sha256:{hashlib.sha256(canonical).hexdigest()}"

    def to_dict(self) -> dict[str, str]:
        return {
            "binding_mode": self.binding_mode,
            "decision_id": self.decision_id,
            "request_id": self.request_id,
            "policy_version": self.policy_version,
            "policy_snapshot_hash": self.policy_snapshot_hash,
            "valid_for_action_ref": self.valid_for_action_ref,
            "decision_scope_hash": self.decision_scope_hash,
            "bound_tenant_id": self.bound_tenant_id,
            "bound_worker_id": self.bound_worker_id,
            "bound_action_type": self.bound_action_type,
            "expires_at": self.expires_at,
        }


def _required_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"guardian_binding {field_name} is required")
    return value.strip()


def _hash_reference(value: Any, field_name: str) -> str:
    text = _required_text(value, field_name)
    prefix, separator, digest = text.partition(":")
    if (
        separator != ":"
        or prefix != "sha256"
        or len(digest) != 64
        or any(character not in "0123456789abcdef" for character in digest.lower())
    ):
        raise ValueError(f"guardian_binding {field_name} must be a SHA-256 reference")
    return f"sha256:{digest.lower()}"


def _timestamp(value: Any, field_name: str) -> str:
    text = _required_text(value, field_name)
    parsed = _parse_timestamp(text)
    return parsed.isoformat().replace("+00:00", "Z")


def _parse_timestamp(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("guardian_binding expires_at must be an ISO timestamp") from exc
    if parsed.tzinfo is None:
        raise ValueError("guardian_binding expires_at must include a timezone")
    return parsed.astimezone(timezone.utc)


__all__ = ["BINDING_MODE", "GuardianDecisionReference"]
