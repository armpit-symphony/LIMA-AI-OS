"""Test-only fake AuthContext/trust metadata fixtures for the adapter skeleton."""

from __future__ import annotations

import ast
from pathlib import Path

from lima.adapters import (
    SparkbotChatInputPayload,
    SparkbotHumanInputAdapter,
    SparkbotOperatorInputPayload,
    SparkbotVoiceInputPayload,
)
from lima.contracts import (
    AuthActor,
    AuthActorType,
    AuthContext,
    AuthLevel,
    AutonomyAuthority,
    IdentityConfidence,
    IdentityFactor,
    OwnerAutonomyContext,
    TrustLevel,
    TrustedDeviceContext,
)
from lima.contracts.intent import HumanInput, HumanInputSource


def _adapter_source() -> str:
    return (
        Path(__file__).resolve().parents[1]
        / "lima"
        / "adapters"
        / "sparkbot_humaninput.py"
    ).read_text(encoding="utf-8")


def _fake_auth_actor() -> AuthActor:
    return AuthActor(
        actor_id="actor-fixture",
        actor_type=AuthActorType.USER,
        display_name="Fixture Actor",
        roles=("user",),
        shell_id="sparkbot-shell",
        metadata={"fixture_only": True},
    )


def _fake_auth_context(actor: AuthActor) -> AuthContext:
    return AuthContext(
        actor=actor,
        session_id="session-fixture",
        shell_id="sparkbot-shell",
        auth_level=AuthLevel.USER,
        authenticated_at="2026-05-09T00:00:00Z",
        expires_at="2026-05-09T01:00:00Z",
        metadata={"fake_authcontext_only": True, "verified_live": False},
    )


def _fake_trusted_context() -> TrustedDeviceContext:
    return TrustedDeviceContext(
        trusted_context_id="trusted-context-fixture",
        device_ref="device-fixture",
        session_ref="session-fixture",
        actor_ref="actor-fixture",
        trust_level=TrustLevel.MEDIUM,
        confidence=0.7,
        last_verified_at="2026-05-09T00:00:00Z",
        expires_at="2026-05-09T01:00:00Z",
        signals=("known_device", "login_session"),
        anomaly_flags=(),
        metadata={"fixture_only": True, "enforced": False},
    )


def _fake_identity_confidence() -> IdentityConfidence:
    return IdentityConfidence(
        confidence_id="identity-confidence-fixture",
        actor_ref="actor-fixture",
        session_ref="session-fixture",
        trusted_context_ref="trusted-context-fixture",
        confidence_score=0.72,
        factors=(IdentityFactor.KNOWN_DEVICE, IdentityFactor.LOGIN_SESSION),
        required_threshold=0.9,
        passed=False,
        expires_at="2026-05-09T00:05:00Z",
        metadata={"fixture_only": True, "biometric_verified_live": False},
    )


def _fake_owner_autonomy_context() -> OwnerAutonomyContext:
    return OwnerAutonomyContext(
        autonomy_context_id="autonomy-context-fixture",
        owner_ref="owner-fixture",
        profile_ref="owner-profile-fixture",
        autonomy_level="assistive",
        authority=AutonomyAuthority.PASSIVE_METADATA,
        capability_refs=("draft_content",),
        constraints={"critical_requires_guardian": True},
        metadata={"fixture_only": True, "enforced": False},
    )


def _assert_no_authority_records_created(result: HumanInput) -> None:
    forbidden_metadata_keys = {
        "approval_id",
        "approval_metadata",
        "auth_decision_id",
        "decision_id",
        "guardian_decision",
        "intent",
        "intent_id",
        "policy_decision",
        "risk_decision",
    }

    assert type(result) is HumanInput
    assert forbidden_metadata_keys.isdisjoint(result.metadata)


def test_chat_payload_carries_fake_authcontext_trust_refs_passively() -> None:
    actor = _fake_auth_actor()
    auth_context = _fake_auth_context(actor)
    trusted_context = _fake_trusted_context()
    identity_confidence = _fake_identity_confidence()
    autonomy_context = _fake_owner_autonomy_context()
    adapter = SparkbotHumanInputAdapter()

    payload = SparkbotChatInputPayload(
        message_id="msg-auth-fixture",
        actor_ref=actor.actor_id,
        shell_id=auth_context.shell_id,
        session_ref=auth_context.session_id,
        text="Summarize my notes",
        text_ref="text-ref-auth-fixture",
        source_ref="source-auth-fixture",
        trusted_context_ref=trusted_context.trusted_context_id,
        autonomy_notes={
            "owner_autonomy_context_ref": autonomy_context.autonomy_context_id,
            "authority": autonomy_context.authority.value,
        },
        metadata={
            "auth_context_ref": auth_context.session_id,
            "auth_actor_ref": actor.actor_id,
            "identity_confidence_ref": identity_confidence.confidence_id,
            "trusted_context_ref": trusted_context.trusted_context_id,
            "owner_autonomy_context_ref": autonomy_context.autonomy_context_id,
            "fixture_metadata_only": True,
        },
    )

    result = adapter.adapt_chat_payload(payload)

    assert result.source is HumanInputSource.TEXT
    assert result.actor_id == actor.actor_id
    assert result.shell_id == auth_context.shell_id
    assert result.metadata["session_ref"] == auth_context.session_id
    assert result.metadata["trusted_context_ref"] == trusted_context.trusted_context_id
    assert result.metadata["autonomy_notes"] == {
        "owner_autonomy_context_ref": autonomy_context.autonomy_context_id,
        "authority": AutonomyAuthority.PASSIVE_METADATA.value,
    }
    assert result.metadata["payload_metadata"] == {
        "auth_context_ref": auth_context.session_id,
        "auth_actor_ref": actor.actor_id,
        "identity_confidence_ref": identity_confidence.confidence_id,
        "trusted_context_ref": trusted_context.trusted_context_id,
        "owner_autonomy_context_ref": autonomy_context.autonomy_context_id,
        "fixture_metadata_only": True,
    }
    assert "verified_identity" not in result.metadata
    assert "auth_verified" not in result.metadata
    _assert_no_authority_records_created(result)


def test_voice_payload_carries_identity_confidence_metadata_passively() -> None:
    identity_confidence = _fake_identity_confidence()
    adapter = SparkbotHumanInputAdapter()
    payload = SparkbotVoiceInputPayload(
        transcript_ref="transcript-auth-fixture",
        actor_ref=identity_confidence.actor_ref or "actor-fixture",
        shell_id="sparkbot-voice",
        session_ref=identity_confidence.session_ref,
        confidence=0.61,
        trusted_context_ref=identity_confidence.trusted_context_ref,
        metadata={
            "identity_confidence_ref": identity_confidence.confidence_id,
            "identity_confidence_score": identity_confidence.confidence_score,
            "identity_confidence_passed": identity_confidence.passed,
            "voice_recognition_performed": False,
            "biometric_verification_performed": False,
        },
    )

    result = adapter.adapt_voice_payload(payload)

    assert result.source is HumanInputSource.VOICE
    assert result.confidence == 0.61
    assert result.metadata["transcript_ref"] == "transcript-auth-fixture"
    assert result.metadata["contains_biometric_signal"] is True
    assert result.metadata["payload_metadata"]["identity_confidence_ref"] == (
        identity_confidence.confidence_id
    )
    assert result.metadata["payload_metadata"]["identity_confidence_passed"] is False
    assert result.metadata["payload_metadata"]["voice_recognition_performed"] is False
    assert result.metadata["payload_metadata"]["biometric_verification_performed"] is False
    assert "voice_match_live" not in _adapter_source()
    _assert_no_authority_records_created(result)


def test_operator_payload_trusted_context_remains_passive() -> None:
    trusted_context = _fake_trusted_context()
    adapter = SparkbotHumanInputAdapter()
    payload = SparkbotOperatorInputPayload(
        actor_ref=trusted_context.actor_ref or "operator-fixture",
        shell_id="sparkbot-operator",
        session_ref=trusted_context.session_ref,
        command_ref="command-auth-fixture",
        trusted_context_ref=trusted_context.trusted_context_id,
        metadata={
            "command_ref": "command-auth-fixture",
            "trusted_context_ref": trusted_context.trusted_context_id,
            "trust_level": trusted_context.trust_level.value,
            "trusted_context_fixture_only": True,
        },
    )

    result = adapter.adapt_operator_payload(payload)

    assert result.source is HumanInputSource.CONSOLE
    assert result.content_ref == "command-auth-fixture"
    assert result.metadata["privacy_class"] == "confidential"
    assert result.metadata["redaction_class"] == "reference_only"
    assert result.metadata["trusted_context_ref"] == trusted_context.trusted_context_id
    assert result.metadata["payload_metadata"]["trust_level"] == TrustLevel.MEDIUM.value
    assert "risk_class" not in result.metadata
    assert "approval_level" not in result.metadata
    _assert_no_authority_records_created(result)


def test_owner_autonomy_notes_do_not_enforce_autonomy() -> None:
    autonomy_context = _fake_owner_autonomy_context()
    adapter = SparkbotHumanInputAdapter()
    payload = SparkbotChatInputPayload(
        message_id="msg-autonomy-fixture",
        actor_ref="actor-autonomy-fixture",
        shell_id="sparkbot-shell",
        text="Draft a message",
        autonomy_notes={
            "owner_autonomy_context_ref": autonomy_context.autonomy_context_id,
            "capability_refs": list(autonomy_context.capability_refs),
            "constraints": dict(autonomy_context.constraints),
        },
        metadata={"owner_autonomy_fixture_only": True},
    )

    result = adapter.adapt_chat_payload(payload)

    assert result.metadata["autonomy_metadata_passive"] is True
    assert result.metadata["autonomy_notes"] == {
        "owner_autonomy_context_ref": autonomy_context.autonomy_context_id,
        "capability_refs": ["draft_content"],
        "constraints": {"critical_requires_guardian": True},
    }
    assert "capability_decision" not in result.metadata
    assert "risk_class" not in result.metadata
    assert "approval_level" not in result.metadata
    assert "guardian_decision" not in result.metadata
    _assert_no_authority_records_created(result)


def test_references_are_not_authority_and_adapter_has_no_auth_methods() -> None:
    adapter = SparkbotHumanInputAdapter()
    payload = SparkbotChatInputPayload(
        message_id="msg-reference-only",
        actor_ref="actor-reference",
        shell_id="sparkbot-shell",
        session_ref="session-reference",
        text_ref="text-ref-reference",
        trusted_context_ref="trusted-context-reference",
        metadata={
            "actor_ref": "actor-reference",
            "session_ref": "session-reference",
            "trusted_context_ref": "trusted-context-reference",
            "references_are_not_authority": True,
        },
    )

    result = adapter.adapt_chat_payload(payload)
    public_callables = {
        name
        for name, value in SparkbotHumanInputAdapter.__dict__.items()
        if not name.startswith("_") and callable(value)
    }
    forbidden_methods = {
        "verify_identity",
        "authenticate",
        "trust_device",
        "grant_autonomy",
        "approve",
        "enforce",
    }

    assert result.actor_id == "actor-reference"
    assert result.metadata["session_ref"] == "session-reference"
    assert result.metadata["trusted_context_ref"] == "trusted-context-reference"
    assert result.metadata["payload_metadata"]["references_are_not_authority"] is True
    assert public_callables == {
        "adapt_chat_payload",
        "adapt_voice_payload",
        "adapt_meeting_payload",
        "adapt_operator_payload",
    }
    assert public_callables.isdisjoint(forbidden_methods)
    _assert_no_authority_records_created(result)


def test_authcontext_fixture_tests_do_not_add_sparkbot_or_runtime_imports() -> None:
    test_source = Path(__file__).read_text(encoding="utf-8")
    adapter_source = _adapter_source()
    tree = ast.parse(test_source)
    imported_modules: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_modules.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            imported_modules.append(node.module)

    forbidden_import_fragments = {
        "Sparkbot",
        "sparkbot.",
        "backend.",
        "app.",
        "requests",
        "httpx",
        "sqlite3",
        "sqlalchemy",
        "sqlmodel",
        "dotenv",
        "os",
    }
    forbidden_adapter_symbols = {
        "GuardianDecision",
        "ApprovalMetadata",
        "PolicyDecision",
        "IntentEnvelope",
        "stream_chat_with_tools",
        "execute_tool",
    }

    imported_text = "\n".join(imported_modules)
    assert all(fragment not in imported_text for fragment in forbidden_import_fragments)
    assert all(symbol not in adapter_source for symbol in forbidden_adapter_symbols)
