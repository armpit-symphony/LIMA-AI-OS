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


class TrustLevel(str, Enum):
    UNKNOWN = "unknown"
    UNTRUSTED = "untrusted"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    OWNER_VERIFIED = "owner_verified"
    OPERATOR_VERIFIED = "operator_verified"


class IdentityFactor(str, Enum):
    KNOWN_DEVICE = "known_device"
    LOGIN_SESSION = "login_session"
    VOICE_MATCH = "voice_match"
    FACE_MATCH = "face_match"
    OPERATOR_PIN = "operator_pin"
    HARDWARE_KEY = "hardware_key"
    LOCATION_CONTEXT = "location_context"
    BEHAVIOR_PATTERN = "behavior_pattern"
    BIOMETRIC_SIGNAL = "biometric_signal"
    FUTURE_BCI_SIGNAL = "future_bci_signal"
    MANUAL_OPERATOR_REVIEW = "manual_operator_review"
    UNKNOWN = "unknown"


class SessionStatus(str, Enum):
    UNKNOWN = "unknown"
    ACTIVE = "active"
    EXPIRED = "expired"
    REVOKED = "revoked"
    SUSPICIOUS = "suspicious"
    LOCKED = "locked"


class AutonomyAuthority(str, Enum):
    NONE = "none"
    PASSIVE_METADATA = "passive_metadata"
    OWNER_PROFILE_REQUIRED = "owner_profile_required"
    POLICY_REQUIRED = "policy_required"
    GUARDIAN_REQUIRED = "guardian_required"


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


@dataclass(frozen=True)
class TrustedDeviceContext:
    """Describe trusted device/session evidence without enforcing trust."""

    trusted_context_id: str
    device_ref: str | None
    session_ref: str | None
    actor_ref: str | None
    trust_level: TrustLevel | str
    confidence: float | None
    last_verified_at: str | None
    expires_at: str | None
    signals: Sequence[str] = field(default_factory=tuple)
    anomaly_flags: Sequence[str] = field(default_factory=tuple)
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class IdentityConfidence:
    """Record identity confidence evidence without verifying identity."""

    confidence_id: str
    actor_ref: str | None
    session_ref: str | None
    trusted_context_ref: str | None
    confidence_score: float
    factors: Sequence[IdentityFactor | str] = field(default_factory=tuple)
    required_threshold: float | None = None
    passed: bool = False
    expires_at: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SessionContext:
    """Describe session state and scope without creating or validating sessions."""

    session_ref: str
    actor_ref: str | None
    shell_id: str | None
    status: SessionStatus | str
    created_at: str | None
    expires_at: str | None
    scope: Mapping[str, Any] = field(default_factory=dict)
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class OwnerAutonomyContext:
    """Reference owner autonomy policy without granting autonomy."""

    autonomy_context_id: str
    owner_ref: str
    profile_ref: str | None
    autonomy_level: str | None
    authority: AutonomyAuthority | str
    capability_refs: Sequence[str] = field(default_factory=tuple)
    constraints: Mapping[str, Any] = field(default_factory=dict)
    metadata: Mapping[str, Any] = field(default_factory=dict)


class AuthProviderProtocol(Protocol):
    """Describe auth state and requirements without logging in or verifying PINs."""

    def describe_actor(self, actor_id: str) -> AuthActor | None:
        """Describe an actor by reference without loading backend app models."""
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


class TrustContextProtocol(Protocol):
    """Describe trust context metadata without verifying or enforcing authority."""

    def describe_trusted_context(
        self,
        trusted_context_id: str,
    ) -> TrustedDeviceContext | None:
        """Describe trusted-device evidence by reference only."""
        ...

    def describe_identity_confidence(
        self,
        confidence_id: str,
    ) -> IdentityConfidence | None:
        """Describe identity confidence evidence by reference only."""
        ...

    def describe_session(self, session_ref: str) -> SessionContext | None:
        """Describe session context by reference only."""
        ...

    def describe_owner_autonomy(
        self,
        autonomy_context_id: str,
    ) -> OwnerAutonomyContext | None:
        """Describe owner autonomy context by reference only."""
        ...
