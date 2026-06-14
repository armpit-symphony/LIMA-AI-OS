"""Runtime tests for the approved V1-G12 audit/evidence persistence slice."""

from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

import pytest

from lima.guardian import review_v1_runtime_request
from lima.kernel import build_v1_runtime_request
from lima.persistence import V1AuditStoreError, V1LocalAuditStore
from lima.spine import (
    V1AuditEvidenceError,
    build_v1_audit_event_record,
    build_v1_audit_lineage_record,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g12_durable_audit_evidence_persistence.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _candidate(
    *,
    action_category: str = "informational",
    requested_action: str = "summarize status",
    risk_tier: str = "low",
    approval_state: str = "proposed",
    target_ref: str = "ref:summary",
    **overrides: Any,
) -> dict[str, Any]:
    candidate = {
        "candidate_id": f"candidate:{action_category}:{requested_action.replace(' ', '-')}",
        "intake_id": f"intake:{action_category}",
        "source": "sparkbot_shell_fixture",
        "source_channel": "chat",
        "operator_intent": "fixture intent",
        "normalized_request": "fixture normalized summary",
        "requested_action": requested_action,
        "action_category": action_category,
        "risk_tier": risk_tier,
        "approval_state": approval_state,
        "blocked_reason": "non_executable_candidate_requires_future_guardian_review",
        "provenance": {
            "actor_id": "user-123",
            "shell_id": "sparkbot-shell",
            "intent_id": f"intent:{action_category}",
            "target_ref": target_ref,
            "evidence_refs": [f"fixture:{action_category}"],
        },
        "target_ref": target_ref,
        "evidence_refs": [f"fixture:{action_category}"],
        "executable": False,
        "execution_allowed": False,
        "side_effects_allowed": False,
        "approved": False,
        "freshness": "fresh",
        "replay_status": "not_replayed",
    }
    candidate.update(overrides)
    return candidate


def _review(candidate: dict[str, Any]):
    request = build_v1_runtime_request(candidate)
    decision = review_v1_runtime_request(request)
    return request, decision


def _metadata(**overrides: Any) -> dict[str, Any]:
    metadata = {
        "event_id": "event:v1-g12:001",
        "tenant_ref": "tenant:alpha",
        "actor_ref": "actor:user-123",
        "occurred_at": "2026-06-14T00:00:00Z",
        "privacy_class": "internal",
        "redaction_class": "summary_only",
        "retention_class": "standard",
        "visibility_class": "security_view",
        "evidence_refs": ["fixture:v1-g12"],
        "redacted_summary": "redacted fixture summary",
        "content_refs": ["content-ref:summary-hash"],
    }
    metadata.update(overrides)
    return metadata


def _event(**metadata_overrides: Any) -> dict[str, Any]:
    request, decision = _review(_candidate())
    return build_v1_audit_event_record(request, decision, _metadata(**metadata_overrides))


def test_v1_g12_fixture_records_approved_scope_and_boundaries() -> None:
    fixture = _load_fixture()

    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g12-durable-audit-evidence-persistence"
    assert fixture["operator_decision"] == "Approve-V1-G12"
    assert fixture["operator"] == "Phil Lima"
    assert fixture["approved_scope"] == "durable_audit_evidence_persistence_runtime_slice"
    assert set(fixture["runtime_symbols"]) == {
        "V1AuditEvidenceError",
        "build_v1_audit_event_record",
        "build_v1_audit_lineage_record",
        "V1AuditStoreError",
        "V1LocalAuditStore",
    }
    assert all(value is False for value in fixture["forbidden_behavior"].values())


def test_v1_g12_safe_metadata_creates_redacted_non_authorizing_event() -> None:
    request, decision = _review(_candidate())
    event = build_v1_audit_event_record(request, decision, _metadata())

    assert event["record_type"] == "v1_audit_event"
    assert event["schema_version"] == "v1-g12-candidate"
    assert event["event_id"] == "event:v1-g12:001"
    assert event["tenant_ref"] == "tenant:alpha"
    assert event["actor_ref"] == "actor:user-123"
    assert event["actor_id"] == request.actor_id
    assert event["shell_id"] == request.shell_id
    assert event["request_id"] == request.request_id
    assert event["decision_id"] == decision.decision_id
    assert event["lineage_id"] == decision.metadata["audit_evidence_linkage"]["lineage_id"]
    assert event["privacy_class"] == "internal"
    assert event["redaction_class"] == "summary_only"
    assert event["retention_class"] == "standard"
    assert event["visibility_class"] == "security_view"
    assert event["redacted_summary"] == "redacted fixture summary"
    assert event["audit_record_is_authority"] is False
    assert event["execution_allowed"] is False
    assert event["side_effects_allowed"] is False
    assert event["approval_token_issued"] is False
    assert event["provider_model_routed"] is False
    assert event["shell_wired"] is False


def test_v1_g12_record_hashes_are_deterministic_for_sanitized_records() -> None:
    request, decision = _review(_candidate())
    first = build_v1_audit_event_record(request, decision, _metadata())
    second = build_v1_audit_event_record(request, decision, _metadata())

    assert first == second
    assert first["record_hash"] == second["record_hash"]


@pytest.mark.parametrize(
    "field,match",
    [
        ("lineage_id", "lineage_id"),
        ("event_id", "event_id"),
        ("tenant_ref", "tenant_ref"),
        ("actor_ref", "actor_ref"),
    ],
)
def test_v1_g12_required_audit_fields_fail_closed(field: str, match: str) -> None:
    request, decision = _review(_candidate())
    metadata = _metadata()
    if field == "lineage_id":
        decision = type(decision)(
            **{
                **asdict(decision),
                "metadata": {
                    **dict(decision.metadata),
                    "audit_evidence_linkage": {
                        **dict(decision.metadata["audit_evidence_linkage"]),
                        "lineage_id": "",
                    },
                },
            }
        )
    else:
        del metadata[field]

    with pytest.raises(V1AuditEvidenceError, match=match):
        build_v1_audit_event_record(request, decision, metadata)


def test_v1_g12_missing_shell_or_decision_fails_closed() -> None:
    request, decision = _review(_candidate())
    missing_shell = type(decision)(**{**asdict(decision), "shell_id": ""})
    with pytest.raises(V1AuditEvidenceError, match="shell_id"):
        build_v1_audit_event_record(request, missing_shell, _metadata())

    missing_decision = type(decision)(**{**asdict(decision), "decision_id": ""})
    with pytest.raises(V1AuditEvidenceError, match="decision_id"):
        build_v1_audit_event_record(request, missing_decision, _metadata())


def test_v1_g12_destructive_edit_delete_requires_approval_evidence() -> None:
    request, decision = _review(
        _candidate(
            action_category="file_mutation",
            requested_action="delete project file",
            risk_tier="high",
            approval_state="approval_required",
            target_ref="file:project.md",
        )
    )

    with pytest.raises(V1AuditEvidenceError, match="approval_id"):
        build_v1_audit_event_record(request, decision, _metadata())

    with pytest.raises(V1AuditEvidenceError, match="approval_evidence_ref"):
        build_v1_audit_event_record(
            request,
            decision,
            _metadata(approval_id="approval:001"),
        )

    event = build_v1_audit_event_record(
        request,
        decision,
        _metadata(
            approval_id="approval:001",
            approval_evidence_ref="approval-evidence:001",
            evidence_refs=["fixture:v1-g12", "approval-evidence:001"],
        ),
    )
    assert event["approval_id"] == "approval:001"
    assert event["approval_evidence_ref"] == "approval-evidence:001"
    assert event["execution_allowed"] is False


@pytest.mark.parametrize(
    "field,value",
    [
        ("raw_secret", "raw-secret-123"),
        ("raw_approval_pin", "approval-pin-123456"),
        ("raw_approval_token", "approval token value"),
        ("raw_prompt", "raw prompt text"),
        ("raw_file_contents", "raw file contents"),
        ("raw_customer_data", "raw customer data"),
    ],
)
def test_v1_g12_raw_sensitive_content_fails_closed(field: str, value: str) -> None:
    request, decision = _review(_candidate())
    with pytest.raises(V1AuditEvidenceError, match="raw sensitive"):
        build_v1_audit_event_record(request, decision, _metadata(**{field: value}))


def test_v1_g12_unknown_privacy_class_fails_closed() -> None:
    request, decision = _review(_candidate())
    with pytest.raises(V1AuditEvidenceError, match="privacy_class"):
        build_v1_audit_event_record(request, decision, _metadata(privacy_class="unknown"))


def test_v1_g12_forged_authority_metadata_fails_closed() -> None:
    request, decision = _review(_candidate())
    with pytest.raises(V1AuditEvidenceError, match="authority|execute"):
        build_v1_audit_event_record(request, decision, _metadata(execution_allowed=True))


@pytest.mark.parametrize(
    "category",
    ["model_call", "tool_call", "browser_network", "robotics_physical_world"],
)
def test_v1_g12_future_policy_records_remain_denied_and_non_executing(category: str) -> None:
    request, decision = _review(
        _candidate(
            action_category=category,
            requested_action=f"{category} request",
            risk_tier="high",
            approval_state="approval_required",
        )
    )
    event = build_v1_audit_event_record(request, decision, _metadata())

    assert event["event_status"] == "denied"
    assert event["decision_status"] == "denied"
    assert event["provider_model_routed"] is False
    assert event["execution_allowed"] is False
    assert event["audit_record_is_authority"] is False


def test_v1_g12_lineage_record_is_redacted_and_non_authorizing() -> None:
    event = _event()
    lineage = build_v1_audit_lineage_record(event)

    assert lineage["record_type"] == "v1_audit_lineage"
    assert lineage["lineage_id"] == event["lineage_id"]
    assert lineage["tenant_ref"] == event["tenant_ref"]
    assert lineage["shell_id"] == event["shell_id"]
    assert lineage["root_event_id"] == event["event_id"]
    assert lineage["latest_event_id"] == event["event_id"]
    assert lineage["decision_id"] == event["decision_id"]
    assert lineage["audit_record_is_authority"] is False
    assert lineage["execution_allowed"] is False
    assert lineage["approval_token_issued"] is False


def test_v1_g12_append_only_store_writes_and_reads_redacted_records() -> None:
    event = _event()
    lineage = build_v1_audit_lineage_record(event)

    with TemporaryDirectory(prefix="lima-v1-g12-") as temp_dir:
        store_dir = Path(temp_dir) / "audit-store"
        store = V1LocalAuditStore(store_dir)

        event_ack = store.append_record(event)
        lineage_ack = store.append_record(lineage)

        assert event_ack["stored"] is True
        assert event_ack["execution_allowed"] is False
        assert lineage_ack["stored"] is True
        assert store.records_path.name == "v1_audit_records.jsonl"
        assert store.records_path.parent == store_dir

        by_event = store.get_by_event_id(
            event["event_id"],
            tenant_ref=event["tenant_ref"],
            shell_id=event["shell_id"],
        )
        by_lineage = store.get_by_lineage_id(
            event["lineage_id"],
            tenant_ref=event["tenant_ref"],
            shell_id=event["shell_id"],
        )
        by_decision = store.get_by_decision_id(
            event["decision_id"],
            tenant_ref=event["tenant_ref"],
            shell_id=event["shell_id"],
        )

        assert by_event == event
        assert event in by_lineage
        assert lineage in by_lineage
        assert event in by_decision
        assert lineage in by_decision


def test_v1_g12_store_is_append_only_for_duplicate_record_keys() -> None:
    event = _event()
    with TemporaryDirectory(prefix="lima-v1-g12-") as temp_dir:
        store = V1LocalAuditStore(Path(temp_dir) / "audit-store")
        store.append_record(event)

        with pytest.raises(V1AuditStoreError, match="append-only|duplicate"):
            store.append_record(event)


def test_v1_g12_cross_tenant_or_shell_lookup_fails_closed() -> None:
    event = _event()
    with TemporaryDirectory(prefix="lima-v1-g12-") as temp_dir:
        store = V1LocalAuditStore(Path(temp_dir) / "audit-store")
        store.append_record(event)

        with pytest.raises(V1AuditStoreError, match="cross-tenant|cross-shell"):
            store.get_by_event_id(
                event["event_id"],
                tenant_ref="tenant:other",
                shell_id=event["shell_id"],
            )

        with pytest.raises(V1AuditStoreError, match="cross-tenant|cross-shell"):
            store.get_by_event_id(
                event["event_id"],
                tenant_ref=event["tenant_ref"],
                shell_id="shell:other",
            )


def test_v1_g12_records_and_acks_do_not_emit_sensitive_values() -> None:
    event = _event()
    lineage = build_v1_audit_lineage_record(event)
    with TemporaryDirectory(prefix="lima-v1-g12-") as temp_dir:
        store = V1LocalAuditStore(Path(temp_dir) / "audit-store")
        ack = store.append_record(event)
        output = json.dumps([event, lineage, ack], sort_keys=True, default=str)

        for forbidden in (
            "raw-secret-123",
            "approval-pin",
            "approval token",
            "raw prompt",
            "raw file contents",
            "raw customer data",
        ):
            assert forbidden not in output
