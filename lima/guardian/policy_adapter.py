"""Compatibility exports for the governed-kernel static policy adapter."""

from lima.governed_kernel.policy_adapter import (
    PolicyAdapterDecision,
    SOURCE_POLICY,
    evaluate_policy,
    map_guardian_semantic,
)

__all__ = [
    "PolicyAdapterDecision",
    "SOURCE_POLICY",
    "evaluate_policy",
    "map_guardian_semantic",
]
