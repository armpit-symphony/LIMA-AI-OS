"""Non-executing vault and breakglass interface contracts for LIMA Runtime."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Protocol


@dataclass(frozen=True)
class VaultSecretRef:
    """Reference metadata for a secret; never contains a raw secret value."""

    secret_ref: str
    secret_name: str | None
    namespace: str | None
    privacy_class: str
    redaction_class: str
    created_at: str | None
    expires_at: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class VaultAccessRequest:
    request_id: str
    actor_id: str
    shell_id: str
    decision_id: str
    approval_id: str | None
    secret_ref: str
    purpose: str | None
    risk_class: str | None
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class VaultAccessDecision:
    vault_decision_id: str
    request_id: str
    allowed: bool
    reason: str | None
    constraints: Mapping[str, Any]
    created_at: str
    expires_at: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class BreakglassSessionRef:
    breakglass_id: str
    actor_id: str
    shell_id: str
    decision_id: str
    approval_id: str | None
    reason: str
    scope: Mapping[str, Any]
    created_at: str
    expires_at: str
    revoked_at: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


class VaultProviderProtocol(Protocol):
    """Describe secret references and access decisions without revealing secrets."""

    def describe_secret(self, secret_ref: str) -> VaultSecretRef | None:
        """Describe a secret reference without returning any raw value."""
        ...

    def request_access(self, request: VaultAccessRequest) -> VaultAccessDecision:
        """Return vault access metadata without decrypting or executing access."""
        ...


class BreakglassProviderProtocol(Protocol):
    """Describe and record breakglass session metadata without enforcement."""

    def describe_session(self, breakglass_id: str) -> BreakglassSessionRef | None:
        """Describe a breakglass session reference without enforcing it."""
        ...

    def record_session(self, session: BreakglassSessionRef) -> None:
        """Record breakglass metadata without creating runtime privileges."""
        ...
