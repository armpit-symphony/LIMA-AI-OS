"""Redaction and privacy contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Protocol, Sequence


class PrivacyClass(str, Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    PRIVATE = "private"
    CONFIDENTIAL = "confidential"
    SECRET = "secret"
    RESTRICTED = "restricted"
    SAFETY_CRITICAL = "safety_critical"
    BIOMETRIC = "biometric"
    UNKNOWN = "unknown"


class RedactionClass(str, Enum):
    NONE = "none"
    SUMMARY_ONLY = "summary_only"
    REFERENCE_ONLY = "reference_only"
    HASH_ONLY = "hash_only"
    MASKED = "masked"
    SECRET_REF_ONLY = "secret_ref_only"
    DROP = "drop"
    OPERATOR_ONLY = "operator_only"
    BREAKGLASS_ONLY = "breakglass_only"


class RetentionClass(str, Enum):
    EPHEMERAL = "ephemeral"
    SHORT = "short"
    STANDARD = "standard"
    EXTENDED = "extended"
    LEGAL_HOLD = "legal_hold"
    DO_NOT_STORE = "do_not_store"


class VisibilityClass(str, Enum):
    PUBLIC_VIEW = "public_view"
    OPERATOR_VIEW = "operator_view"
    ADMIN_VIEW = "admin_view"
    SECURITY_VIEW = "security_view"
    BREAKGLASS_VIEW = "breakglass_view"
    SYSTEM_ONLY = "system_only"
    NO_VIEW = "no_view"


@dataclass(frozen=True)
class DataReference:
    ref_id: str
    ref_type: str
    uri: str | None
    privacy_class: PrivacyClass | str
    redaction_class: RedactionClass | str
    retention_class: RetentionClass | str
    visibility_class: VisibilityClass | str
    content_hash: str | None
    created_at: str
    expires_at: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RedactionMetadata:
    privacy_class: PrivacyClass | str
    redaction_class: RedactionClass | str
    retention_class: RetentionClass | str
    visibility_class: VisibilityClass | str
    content_refs: Sequence[DataReference] = field(default_factory=tuple)
    evidence_refs: Sequence[str] = field(default_factory=tuple)
    secret_refs: Sequence[str] = field(default_factory=tuple)
    redacted_summary: str | None = None
    contains_secret: bool = False
    contains_biometric: bool = False
    contains_safety_critical: bool = False
    data_subject_ref: str | None = None
    retention_expires_at: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


class PrivacyProtocol(Protocol):
    """Describe privacy/redaction metadata without revealing raw content."""

    def describe_reference(self, ref: DataReference) -> RedactionMetadata:
        """Return contract metadata for a data reference."""
        ...
