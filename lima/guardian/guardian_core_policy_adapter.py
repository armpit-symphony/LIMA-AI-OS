"""Compatibility exports for the governed-kernel Guardian Core seam."""

from lima.governed_kernel.guardian_core_policy_adapter import (
    GUARDIAN_CORE_SOURCE_POLICY,
    SOURCE_POLICY,
    STATIC_FALLBACK_SOURCE_POLICY,
    evaluate_policy,
)

__all__ = [
    "GUARDIAN_CORE_SOURCE_POLICY",
    "SOURCE_POLICY",
    "STATIC_FALLBACK_SOURCE_POLICY",
    "evaluate_policy",
]
