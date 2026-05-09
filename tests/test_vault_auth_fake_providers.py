"""Tests for in-memory Vault/Auth provider fakes."""

from dataclasses import fields


def _public_callables(provider: type) -> set[str]:
    return {
        name
        for name, value in provider.__dict__.items()
        if not name.startswith("_") and callable(value)
    }


def test_fake_auth_provider_describes_context_and_evaluates_requirements() -> None:
    from lima.contracts import (
        AuthActor,
        AuthActorType,
        AuthContext,
        AuthLevel,
        AuthRequirement,
    )
    from lima.guardian import FakeAuthProvider

    actor = AuthActor(
        actor_id="actor-1",
        actor_type=AuthActorType.OPERATOR,
        display_name="Operator One",
        roles=("guardian_operator",),
        shell_id="test-shell",
    )
    context = AuthContext(
        actor=actor,
        session_id="session-1",
        shell_id="test-shell",
        auth_level=AuthLevel.OPERATOR,
        authenticated_at="2026-05-09T00:00:00Z",
        expires_at="2026-05-09T00:05:00Z",
    )
    requirement = AuthRequirement(
        requirement_id="requirement-1",
        required_level=AuthLevel.USER,
        reason="Contract validation.",
        risk_class="low",
        action_type="metadata_check",
    )
    provider = FakeAuthProvider(actors=(actor,), contexts=(context,))
    decision = provider.evaluate_requirement(requirement, context)

    forbidden_methods = {"login", "verify_pin", "authenticate_live"}

    assert provider.describe_actor(actor.actor_id) is actor
    assert provider.describe_context("session-1") is context
    assert provider.describe_context("missing-session") is None
    assert decision.allowed is True
    assert decision.actor_id == actor.actor_id
    assert decision.requirement_id == requirement.requirement_id
    assert _public_callables(FakeAuthProvider).isdisjoint(forbidden_methods)


def test_fake_vault_provider_uses_reference_metadata_only() -> None:
    from lima.contracts import VaultAccessRequest, VaultSecretRef
    from lima.guardian import FakeVaultProvider

    secret_ref = VaultSecretRef(
        secret_ref="vault:metadata/service-ref",
        secret_name="service_ref",
        namespace="test",
        privacy_class="secret",
        redaction_class="secret_ref_only",
        created_at="2026-05-09T00:00:00Z",
    )
    request = VaultAccessRequest(
        request_id="vault-request-1",
        actor_id="actor-1",
        shell_id="test-shell",
        decision_id="decision-1",
        approval_id=None,
        secret_ref=secret_ref.secret_ref,
        purpose="Contract validation.",
        risk_class="low",
    )
    provider = FakeVaultProvider(secret_refs=(secret_ref,))
    decision = provider.request_access(request)
    forbidden_methods = {
        "get_secret",
        "decrypt",
        "encrypt",
        "read_value",
        "write_value",
        "return_secret",
    }
    forbidden_fields = {
        "raw_secret",
        "secret_value",
        "value",
        "plaintext",
        "token",
        "password",
    }

    assert provider.describe_secret(secret_ref.secret_ref) is secret_ref
    assert provider.describe_secret("vault:metadata/missing") is None
    assert decision.allowed is True
    assert decision.constraints["metadata_only"] is True
    assert decision.constraints["in_memory_only"] is True
    assert {field.name for field in fields(VaultSecretRef)}.isdisjoint(forbidden_fields)
    assert _public_callables(FakeVaultProvider).isdisjoint(forbidden_methods)


def test_fake_breakglass_provider_records_metadata_only() -> None:
    from lima.contracts import BreakglassSessionRef
    from lima.guardian import FakeBreakglassProvider

    session = BreakglassSessionRef(
        breakglass_id="breakglass-1",
        actor_id="actor-1",
        shell_id="test-shell",
        decision_id="decision-1",
        approval_id="approval-1",
        reason="Contract validation.",
        scope={"risk_class": "critical"},
        created_at="2026-05-09T00:00:00Z",
        expires_at="2026-05-09T00:05:00Z",
    )
    provider = FakeBreakglassProvider()
    provider.record_session(session)
    forbidden_methods = {"open_live_session", "bypass", "enforce", "execute"}

    assert provider.describe_session(session.breakglass_id) is session
    assert provider.describe_session("missing-session") is None
    assert _public_callables(FakeBreakglassProvider).isdisjoint(forbidden_methods)
