"""Persistence implementation namespace reserved for future extraction."""

from .v1_audit_store import V1AuditStoreError, V1LocalAuditStore

__all__ = ("V1AuditStoreError", "V1LocalAuditStore")
