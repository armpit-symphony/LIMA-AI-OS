"""Contract-shape tests for non-executing Vault/Auth interfaces."""

from dataclasses import fields


def _public_callables(protocol: type) -> set[str]:
    return {
        name
        for name, value in protocol.__dict__.items()
        if not name.startswith("_") and callable(value)
    }


def test_auth_contracts_instantiate() -> None:
    from lima.contracts import (
        AuthActor,
        AuthActorType,
        AuthContext,
        AuthDecision,
        AuthLevel,
        AuthProviderProtocol,
        AuthRequirement,
    )

    actor = AuthActor(
        actor_id="actor-1",
        actor_type=AuthActorType.OPERATOR,
        display_name="Operator One",
        roles=("guardian_operator",),
        shell_id="sparkbot",
        metadata={"source": "contract-test"},
    )
    context = AuthContext(
        actor=actor,
        session_id="session-1",
        shell_id="sparkbot",
        auth_level=AuthLevel.OPERATOR,
        authenticated_at="2026-05-09T00:00:00Z",
        expires_at="2026-05-09T00:05:00Z",
    )
    requirement = AuthRequirement(
        requirement_id="auth-requirement-1",
        required_level=AuthLevel.OPERATOR,
        reason="Vault reference access needs operator metadata.",
        risk_class="critical",
        action_type="secret_access",
    )
    decision = AuthDecision(
        auth_decision_id="auth-decision-1",
        requirement_id=requirement.requirement_id,
        actor_id=actor.actor_id,
        allowed=False,
        auth_level=context.auth_level,
        reason="Contract test only.",
        created_at="2026-05-09T00:00:01Z",
    )

    assert AuthActorType.UNKNOWN.value == "unknown"
    assert AuthLevel.BREAKGLASS.value == "breakglass"
    assert context.actor is actor
    assert decision.requirement_id == requirement.requirement_id
    assert _public_callables(AuthProviderProtocol) == {
        "describe_actor",
        "describe_context",
        "evaluate_requirement",
    }


def test_vault_contracts_instantiate_without_raw_secret_fields() -> None:
    from lima.contracts import (
        BreakglassProviderProtocol,
        BreakglassSessionRef,
        VaultAccessDecision,
        VaultAccessRequest,
        VaultProviderProtocol,
        VaultSecretRef,
    )

    secret_ref = VaultSecretRef(
        secret_ref="vault:connector/github",
        secret_name="github_token",
        namespace="connectors",
        privacy_class="secret",
        redaction_class="secret_ref_only",
        created_at="2026-05-09T00:00:00Z",
    )
    access_request = VaultAccessRequest(
        request_id="vault-request-1",
        actor_id="actor-1",
        shell_id="sparkbot",
        decision_id="decision-1",
        approval_id="approval-1",
        secret_ref=secret_ref.secret_ref,
        purpose="Describe connector readiness.",
        risk_class="critical",
    )
    access_decision = VaultAccessDecision(
        vault_decision_id="vault-decision-1",
        request_id=access_request.request_id,
        allowed=False,
        reason="Contract test only.",
        constraints={"no_raw_secret": True},
        created_at="2026-05-09T00:00:01Z",
    )
    breakglass_ref = BreakglassSessionRef(
        breakglass_id="breakglass-1",
        actor_id=access_request.actor_id,
        shell_id=access_request.shell_id,
        decision_id=access_request.decision_id,
        approval_id=access_request.approval_id,
        reason="Emergency operator metadata example.",
        scope={"secret_ref": secret_ref.secret_ref},
        created_at="2026-05-09T00:00:00Z",
        expires_at="2026-05-09T00:05:00Z",
    )

    forbidden_secret_fields = {
        "raw_secret",
        "secret_value",
        "value",
        "plaintext",
        "token",
        "password",
    }
    secret_ref_fields = {field.name for field in fields(VaultSecretRef)}

    assert secret_ref.redaction_class == "secret_ref_only"
    assert access_request.secret_ref == secret_ref.secret_ref
    assert access_decision.constraints["no_raw_secret"] is True
    assert breakglass_ref.scope["secret_ref"] == secret_ref.secret_ref
    assert secret_ref_fields.isdisjoint(forbidden_secret_fields)
    assert _public_callables(VaultProviderProtocol) == {
        "describe_secret",
        "request_access",
    }
    assert _public_callables(BreakglassProviderProtocol) == {
        "describe_session",
        "record_session",
    }


def test_auth_vault_protocols_do_not_expose_execution_or_secret_methods() -> None:
    from lima.contracts import (
        AuthProviderProtocol,
        BreakglassProviderProtocol,
        VaultProviderProtocol,
    )

    auth_forbidden = {"execute", "enforce", "verify_pin", "login"}
    vault_forbidden = {
        "get_secret",
        "decrypt",
        "encrypt",
        "read_value",
        "write_value",
    }
    breakglass_forbidden = {"execute", "enforce"}

    assert _public_callables(AuthProviderProtocol).isdisjoint(auth_forbidden)
    assert _public_callables(VaultProviderProtocol).isdisjoint(vault_forbidden)
    assert _public_callables(BreakglassProviderProtocol).isdisjoint(
        breakglass_forbidden
    )
