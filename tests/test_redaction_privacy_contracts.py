"""Contract-shape tests for redaction/privacy metadata."""


def test_redaction_privacy_contract_imports() -> None:
    from lima.contracts import (
        DataReference,
        PrivacyClass,
        PrivacyProtocol,
        RedactionClass,
        RedactionMetadata,
        RetentionClass,
        VisibilityClass,
    )

    assert PrivacyClass.PUBLIC.value == "public"
    assert PrivacyClass.SECRET.value == "secret"
    assert PrivacyClass.SAFETY_CRITICAL.value == "safety_critical"
    assert PrivacyClass.BIOMETRIC.value == "biometric"
    assert PrivacyClass.UNKNOWN.value == "unknown"
    assert RedactionClass.NONE.value == "none"
    assert RedactionClass.REFERENCE_ONLY.value == "reference_only"
    assert RedactionClass.SECRET_REF_ONLY.value == "secret_ref_only"
    assert RedactionClass.DROP.value == "drop"
    assert RetentionClass.EPHEMERAL.value == "ephemeral"
    assert RetentionClass.LEGAL_HOLD.value == "legal_hold"
    assert RetentionClass.DO_NOT_STORE.value == "do_not_store"
    assert VisibilityClass.PUBLIC_VIEW.value == "public_view"
    assert VisibilityClass.BREAKGLASS_VIEW.value == "breakglass_view"
    assert VisibilityClass.NO_VIEW.value == "no_view"
    assert all(
        item is not None
        for item in (
            DataReference,
            PrivacyProtocol,
            RedactionMetadata,
        )
    )


def test_redaction_privacy_contracts_instantiate() -> None:
    from datetime import datetime, timezone

    from lima.contracts import (
        AuditEvent,
        DataReference,
        PrivacyClass,
        PrivacyProtocol,
        RedactionClass,
        RedactionMetadata,
        RetentionClass,
        SpineAuditEvent,
        SpineEvent,
        VisibilityClass,
    )

    ref = DataReference(
        ref_id="transcript-ref-1",
        ref_type="transcript_ref",
        uri=None,
        privacy_class=PrivacyClass.BIOMETRIC,
        redaction_class=RedactionClass.REFERENCE_ONLY,
        retention_class=RetentionClass.SHORT,
        visibility_class=VisibilityClass.OPERATOR_VIEW,
        content_hash="sha256:example",
        created_at="2026-05-08T00:00:00Z",
        expires_at="2026-05-09T00:00:00Z",
    )
    metadata = RedactionMetadata(
        privacy_class=PrivacyClass.BIOMETRIC,
        redaction_class=RedactionClass.REFERENCE_ONLY,
        retention_class=RetentionClass.SHORT,
        visibility_class=VisibilityClass.OPERATOR_VIEW,
        content_refs=(ref,),
        evidence_refs=("evidence-ref-1",),
        secret_refs=("vault:secret-ref-1",),
        redacted_summary="Voice transcript stored by reference.",
        contains_secret=True,
        contains_biometric=True,
        data_subject_ref="actor:operator-1",
        retention_expires_at=ref.expires_at,
    )
    audit_event = AuditEvent(
        event_id="event-privacy-1",
        actor_id="operator-1",
        shell_id="sparkbot",
        event_type="human_input",
        created_at=datetime(2026, 5, 8, tzinfo=timezone.utc),
        privacy_class=PrivacyClass.BIOMETRIC.value,
        redaction_class=RedactionClass.REFERENCE_ONLY.value,
        retention_class=RetentionClass.SHORT.value,
        visibility_class=VisibilityClass.OPERATOR_VIEW.value,
        content_refs=(ref,),
        secret_refs=("vault:secret-ref-1",),
        redacted_summary=metadata.redacted_summary,
        contains_secret=True,
        contains_biometric=True,
        data_subject_ref=metadata.data_subject_ref,
        retention_expires_at=metadata.retention_expires_at,
    )
    spine_audit_event = SpineAuditEvent(
        event_id="spine-audit-privacy-1",
        lineage_id="lineage-1",
        event_type="human_input",
        status="received",
        timestamp="2026-05-08T00:00:00Z",
        actor_id="operator-1",
        shell_id="sparkbot",
        privacy_class=PrivacyClass.BIOMETRIC.value,
        redaction_class=RedactionClass.REFERENCE_ONLY.value,
        retention_class=RetentionClass.SHORT.value,
        visibility_class=VisibilityClass.OPERATOR_VIEW.value,
        content_refs=(ref,),
        redacted_summary=metadata.redacted_summary,
        contains_biometric=True,
    )
    spine_event = SpineEvent(
        event_id="spine-privacy-1",
        event_type="human_input",
        source="audit",
        created_at=datetime(2026, 5, 8, tzinfo=timezone.utc),
        lineage_id="lineage-1",
        privacy_class=PrivacyClass.BIOMETRIC.value,
        redaction_class=RedactionClass.REFERENCE_ONLY.value,
        retention_class=RetentionClass.SHORT.value,
        visibility_class=VisibilityClass.OPERATOR_VIEW.value,
        content_refs=(ref,),
        redacted_summary=metadata.redacted_summary,
        contains_biometric=True,
    )
    public_callables = {
        name
        for name, value in PrivacyProtocol.__dict__.items()
        if not name.startswith("_") and callable(value)
    }

    assert metadata.content_refs == (ref,)
    assert metadata.contains_secret is True
    assert audit_event.content_refs == (ref,)
    assert audit_event.secret_refs == ("vault:secret-ref-1",)
    assert spine_audit_event.privacy_class == PrivacyClass.BIOMETRIC.value
    assert spine_event.redaction_class == RedactionClass.REFERENCE_ONLY.value
    assert public_callables == {"describe_reference"}
    assert "execute" not in public_callables
    assert "enforce" not in public_callables
    assert "reveal" not in public_callables
