"""Contract-shape tests for descriptive trust context contracts."""

from __future__ import annotations


def _public_callables(protocol: type) -> set[str]:
    return {
        name
        for name, value in protocol.__dict__.items()
        if not name.startswith("_") and callable(value)
    }


def test_trust_level_expected_values_exist() -> None:
    from lima.contracts import TrustLevel

    assert {level.value for level in TrustLevel} == {
        "unknown",
        "untrusted",
        "low",
        "medium",
        "high",
        "owner_verified",
        "operator_verified",
    }


def test_identity_factor_expected_values_exist() -> None:
    from lima.contracts import IdentityFactor

    assert {factor.value for factor in IdentityFactor} == {
        "known_device",
        "login_session",
        "voice_match",
        "face_match",
        "operator_pin",
        "hardware_key",
        "location_context",
        "behavior_pattern",
        "biometric_signal",
        "future_bci_signal",
        "manual_operator_review",
        "unknown",
    }


def test_session_status_expected_values_exist() -> None:
    from lima.contracts import SessionStatus

    assert {status.value for status in SessionStatus} == {
        "unknown",
        "active",
        "expired",
        "revoked",
        "suspicious",
        "locked",
    }


def test_autonomy_authority_expected_values_exist() -> None:
    from lima.contracts import AutonomyAuthority

    assert {authority.value for authority in AutonomyAuthority} == {
        "none",
        "passive_metadata",
        "owner_profile_required",
        "policy_required",
        "guardian_required",
    }


def test_trusted_device_context_instantiates() -> None:
    from lima.contracts import TrustedDeviceContext, TrustLevel

    context = TrustedDeviceContext(
        trusted_context_id="trusted-context-1",
        device_ref="device-1",
        session_ref="session-1",
        actor_ref="actor-1",
        trust_level=TrustLevel.MEDIUM,
        confidence=0.75,
        last_verified_at="2026-05-09T00:00:00Z",
        expires_at="2026-05-09T01:00:00Z",
        signals=("known_device", "login_session"),
        anomaly_flags=(),
        metadata={"descriptive_only": True},
    )

    assert context.trust_level is TrustLevel.MEDIUM
    assert context.confidence == 0.75
    assert context.metadata["descriptive_only"] is True


def test_identity_confidence_instantiates() -> None:
    from lima.contracts import IdentityConfidence, IdentityFactor

    confidence = IdentityConfidence(
        confidence_id="identity-confidence-1",
        actor_ref="actor-1",
        session_ref="session-1",
        trusted_context_ref="trusted-context-1",
        confidence_score=0.8,
        factors=(IdentityFactor.KNOWN_DEVICE, IdentityFactor.LOGIN_SESSION),
        required_threshold=0.9,
        passed=False,
        expires_at="2026-05-09T00:05:00Z",
        metadata={"bci_confirm_only": True},
    )

    assert confidence.confidence_score == 0.8
    assert IdentityFactor.KNOWN_DEVICE in confidence.factors
    assert confidence.passed is False


def test_session_context_instantiates() -> None:
    from lima.contracts import SessionContext, SessionStatus

    session = SessionContext(
        session_ref="session-1",
        actor_ref="actor-1",
        shell_id="sparkbot",
        status=SessionStatus.ACTIVE,
        created_at="2026-05-09T00:00:00Z",
        expires_at="2026-05-09T01:00:00Z",
        scope={"room_id": "room-1"},
        metadata={"verified_live": False},
    )

    assert session.status is SessionStatus.ACTIVE
    assert session.scope["room_id"] == "room-1"
    assert session.metadata["verified_live"] is False


def test_owner_autonomy_context_instantiates() -> None:
    from lima.contracts import AutonomyAuthority, OwnerAutonomyContext

    context = OwnerAutonomyContext(
        autonomy_context_id="autonomy-context-1",
        owner_ref="owner-1",
        profile_ref="owner-profile-1",
        autonomy_level="trusted",
        authority=AutonomyAuthority.OWNER_PROFILE_REQUIRED,
        capability_refs=("draft_content",),
        constraints={"critical_requires_guardian": True},
        metadata={"passive_reference": True},
    )

    assert context.authority is AutonomyAuthority.OWNER_PROFILE_REQUIRED
    assert context.capability_refs == ("draft_content",)
    assert context.constraints["critical_requires_guardian"] is True


def test_trust_context_protocol_is_describe_only() -> None:
    from lima.contracts import TrustContextProtocol

    assert _public_callables(TrustContextProtocol) == {
        "describe_trusted_context",
        "describe_identity_confidence",
        "describe_session",
        "describe_owner_autonomy",
    }


def test_trust_context_contracts_do_not_expose_authority_methods() -> None:
    from lima.contracts import TrustContextProtocol

    forbidden_methods = {
        "verify_identity",
        "authenticate",
        "enforce",
        "approve",
        "authorize",
        "login",
        "verify_pin",
        "face_match_live",
        "voice_match_live",
        "trust_device",
        "grant_autonomy",
        "bypass",
    }

    assert _public_callables(TrustContextProtocol).isdisjoint(forbidden_methods)
