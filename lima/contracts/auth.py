"""Non-executing auth interface contracts for LIMA Runtime."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Protocol, Sequence


class AuthActorType(str, Enum):
    USER = "user"
    OPERATOR = "operator"
    SERVICE = "service"
    AGENT = "agent"
    SYSTEM = "system"
    UNKNOWN = "unknown"


class AuthLevel(str, Enum):
    ANONYMOUS = "anonymous"
    USER = "user"
    OPERATOR = "operator"
    ADMIN = "admin"
    BREAKGLASS = "breakglass"
    SYSTEM = "system"


@dataclass(frozen=True)
class AuthActor:
    actor_id: str
    actor_type: AuthActorType | str
    display_name: str | None
    roles: Sequence[str] = field(default_factory=tuple)
    shell_id: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AuthContext:
    actor: AuthActor
    session_id: str | None
    shell_id: str
    auth_level: AuthLevel | str
    authenticated_at: str | None
    expires_at: str | None
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AuthRequirement:
    requirement_id: str
    required_level: AuthLevel | str
    reason: str | None
    risk_class: str | None
    action_type: str | None
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AuthDecision:
    auth_decision_id: str
    requirement_id: str
    actor_id: str
    allowed: bool
    auth_level: AuthLevel | str
    reason: str | None
    created_at: str
    expires_at: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


class AuthProviderProtocol(Protocol):
    """Describe auth state and requirements without logging in or verifying PINs."""

    def describe_actor(self, actor_id: str) -> AuthActor | None:
        """Describe an actor by reference without loading Sparkbot models."""
        ...

    def describe_context(self, session_id: str) -> AuthContext | None:
        """Describe an auth context by reference without opening a DB session."""
        ...

    def evaluate_requirement(
        self,
        requirement: AuthRequirement,
        context: AuthContext,
    ) -> AuthDecision:
        """Evaluate auth requirement metadata without enforcing runtime access."""
        ...
