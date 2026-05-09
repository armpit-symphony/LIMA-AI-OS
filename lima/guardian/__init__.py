"""Guardian implementation namespace reserved for future extraction."""

from .fakes import FakeAuthProvider, FakeBreakglassProvider, FakeVaultProvider

__all__ = [
    "FakeAuthProvider",
    "FakeBreakglassProvider",
    "FakeVaultProvider",
]
