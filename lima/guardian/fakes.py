"""In-memory provider fakes for contract validation."""

from __future__ import annotations

from collections.abc import Iterable, Mapping

from lima.contracts.auth import (
    AuthActor,
    AuthContext,
    AuthDecision,
    AuthLevel,
    AuthProviderProtocol,
    AuthRequirement,
)
from lima.contracts.vault import (
    BreakglassProviderProtocol,
    BreakglassSessionRef,
    VaultAccessDecision,
    VaultAccessRequest,
    VaultProviderProtocol,
    VaultSecretRef,
)


_AUTH_LEVEL_ORDER: Mapping[str, int] = {
    AuthLevel.ANONYMOUS.value: 0,
    AuthLevel.USER.value: 1,
    AuthLevel.OPERATOR.value: 2,
    AuthLevel.ADMIN.value: 3,
    AuthLevel.BREAKGLASS.value: 4,
    AuthLevel.SYSTEM.value: 5,
}


def _auth_level_key(auth_level: AuthLevel | str) -> str:
    if isinstance(auth_level, AuthLevel):
        return auth_level.value
    return str(auth_level)


class FakeAuthProvider(AuthProviderProtocol):
    """In-memory auth metadata provider for tests."""

    def __init__(
        self,
        actors: Iterable[AuthActor] = (),
        contexts: Iterable[AuthContext] = (),
    ) -> None:
        self._actors = {actor.actor_id: actor for actor in actors}
        self._contexts = {
            context.session_id: context
            for context in contexts
            if context.session_id is not None
        }

    def describe_actor(self, actor_id: str) -> AuthActor | None:
        return self._actors.get(actor_id)

    def describe_context(self, session_id: str) -> AuthContext | None:
        return self._contexts.get(session_id)

    def evaluate_requirement(
        self,
        requirement: AuthRequirement,
        context: AuthContext,
    ) -> AuthDecision:
        current_rank = _AUTH_LEVEL_ORDER.get(_auth_level_key(context.auth_level), -1)
        required_rank = _AUTH_LEVEL_ORDER.get(_auth_level_key(requirement.required_level), -1)
        allowed = current_rank >= required_rank and required_rank >= 0
        reason = "fake requirement satisfied" if allowed else "fake requirement not satisfied"
        return AuthDecision(
            auth_decision_id=f"fake-auth:{requirement.requirement_id}:{context.actor.actor_id}",
            requirement_id=requirement.requirement_id,
            actor_id=context.actor.actor_id,
            allowed=allowed,
            auth_level=context.auth_level,
            reason=reason,
            created_at="fake",
            expires_at=context.expires_at,
            metadata={"fake_provider": "auth"},
        )


class FakeVaultProvider(VaultProviderProtocol):
    """In-memory vault metadata provider for tests."""

    def __init__(
        self,
        secret_refs: Iterable[VaultSecretRef] = (),
        allowed_refs: Iterable[str] | None = None,
    ) -> None:
        self._secret_refs = {secret.secret_ref: secret for secret in secret_refs}
        self._allowed_refs = set(allowed_refs) if allowed_refs is not None else set(self._secret_refs)

    def describe_secret(self, secret_ref: str) -> VaultSecretRef | None:
        return self._secret_refs.get(secret_ref)

    def request_access(self, request: VaultAccessRequest) -> VaultAccessDecision:
        known = request.secret_ref in self._secret_refs
        allowed = known and request.secret_ref in self._allowed_refs
        reason = "fake reference allowed" if allowed else "fake reference denied"
        return VaultAccessDecision(
            vault_decision_id=f"fake-vault:{request.request_id}",
            request_id=request.request_id,
            allowed=allowed,
            reason=reason,
            constraints={"metadata_only": True, "in_memory_only": True},
            created_at="fake",
            expires_at=None,
            metadata={"fake_provider": "vault"},
        )


class FakeBreakglassProvider(BreakglassProviderProtocol):
    """In-memory breakglass metadata provider for tests."""

    def __init__(self, sessions: Iterable[BreakglassSessionRef] = ()) -> None:
        self._sessions = {session.breakglass_id: session for session in sessions}

    def describe_session(self, breakglass_id: str) -> BreakglassSessionRef | None:
        return self._sessions.get(breakglass_id)

    def record_session(self, session: BreakglassSessionRef) -> None:
        self._sessions[session.breakglass_id] = session
