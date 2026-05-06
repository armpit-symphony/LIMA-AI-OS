"""Persistence contracts."""

from __future__ import annotations

from contextlib import AbstractContextManager
from typing import Any, Protocol


class StorageProtocol(Protocol):
    """One persistence interface over local, hosted, memory, and vault backends."""

    def transaction(self) -> AbstractContextManager[Any]:
        """Open a storage transaction."""
        ...

    def put_event(self, event_id: str, event: dict[str, Any]) -> None:
        """Persist a sanitized event."""
        ...

    def get_event(self, event_id: str) -> dict[str, Any] | None:
        """Load a persisted event by identifier."""
        ...

    def put_secret_ref(self, name: str, secret_ref: str) -> None:
        """Persist a vault reference or handle, never a raw secret value."""
        ...
