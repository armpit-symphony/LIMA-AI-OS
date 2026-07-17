"""Runtime tests for the approved V1-G14 approval-enforcement slice."""

from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path
from typing import Any

import pytest

from lima.contracts.guardian import GuardianDecisionStatus
from lima.guardian import (
    V1ApprovalEnforcementError,
    enforce_v1_destructive_approval,
    review_v1_runtime_request,
)
from lima.kernel import build_v1_runtime_request


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g14_destructive_approval_enforcement.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _candidate(
    *,
    action_category: str = "file_mutation",
    requested_action: str = "delete project file",
    risk_tier: str = "high",
    approval_state: str = "approval_required",
    target_ref: str = "file:project.md",
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
        "blocked_reason": "risky_request_requires_future_guardian_review",
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


def _approval_metadata(request: Any, decision: Any, **overrides: Any) -> dict[str, Any]:
    metadata = {
        "approval_id": "approval:v1-g14:001",
        "approval_evidence_ref": "approval-evidence:v1-g14:001",
        "approving_actor_ref": "operator:phil-lima",
        "approval_recorded_at": "2026-06-15T00:00:00Z",
        "approval_scope": "destructive_edit_delete_file_mutation",
        "approval_state": "granted",
        "approval_freshness": "fresh",
        "approval_replay_status": "not_replayed",
        "tenant_ref": "tenant:alpha",
        "request_id": request.request_id,
        "decision_id": decision.decision_id,
        "actor_id": request.actor_id,
        "shell_id": request.shell_id,
        "target_ref": request.target_ref,
        "evidence_refs": ["fixture:v1-g14", "approval-evidence:v1-g14:001"],
    }
    metadata.update(overrides)
    return metadata


def test_v1_g14_fixture_records_approved_scope_and_boundaries() -> None:
    fixture = _load_fixture()

    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g14-destructive-approval-enforcement"
    assert fixture["operator_decision"] == "Approve-V1-G14"
    assert fixture["approved_scope"] == "destructive_edit_delete_approval_enforcement_runtime_slice"
    assert set(fixture["runtime_symbols"]) == {
        "V1ApprovalEnforcementError",
        "enforce_v1_destructive_approval",
    }
    assert fixture["runtime_behavior_added"] is True
    assert fixture["approval_enforcement_added"] is True
    assert all(value is False for value in fixture["forbidden_behavior"].values())


def test_v1_g14_complete_sanitized_approval_evidence_creates_non_executing_record() -> None:
    request, decision = _review(_candidate())
    record = enforce_v1_destructive_approval(
        request,
        decision,
        _approval_metadata(request, decision),
    )

    assert decision.status is GuardianDecisionStatus.NEEDS_OPERATOR_PIN
    assert record["record_type"] == "v1_approval_enforcement"
    assert record["schema_version"] == "v1-g14-candidate"
    assert record["approval_enforcement_status"] == "satisfied"
    assert record["request_id"] == request.request_id
    assert record["decision_id"] == decision.decision_id
    assert record["approval_id"] == "approval:v1-g14:001"
    assert record["approval_evidence_ref"] == "approval-evidence:v1-g14:001"
    assert record["approval_scope"] == "destructive_edit_delete_file_mutation"
    assert record["approval_state"] == "granted"
    assert record["execution_allowed"] is False
    assert record["side_effects_allowed"] is False
    assert record["approval_token_issued"] is False
    assert record["provider_model_routed"] is False
    assert record["shell_wired"] is False
    assert record["file_mutation_executed"] is False
    assert record["approval_enforcement_record_is_authority"] is False
    assert record["metadata"]["proof_not_authority"] is True


def test_v1_g14_records_are_deterministic_for_sanitized_metadata() -> None:
    request, decision = _review(_candidate())
    first = enforce_v1_destructive_approval(
        request,
        decision,
        _approval_metadata(request, decision),
    )
    second = enforce_v1_destructive_approval(
        request,
        decision,
        _approval_metadata(request, decision),
    )

    assert first == second
    assert first["record_hash"] == second["record_hash"]


@pytest.mark.parametrize(
    "field,match",
    [
        ("approval_id", "approval_id"),
        ("approval_evidence_ref", "approval_evidence_ref"),
        ("approving_actor_ref", "approving_actor_ref"),
        ("approval_recorded_at", "approval_recorded_at"),
        ("approval_scope", "approval_scope"),
        ("tenant_ref", "tenant_ref"),
        ("shell_id", "shell_id"),
    ],
)
def test_v1_g14_missing_required_approval_metadata_fails_closed(
    field: str,
    match: str,
) -> None:
    request, decision = _review(_candidate())
    metadata = _approval_metadata(request, decision)
    del metadata[field]

    with pytest.raises(V1ApprovalEnforcementError, match=match):
        enforce_v1_destructive_approval(request, decision, metadata)


def test_v1_g14_destructive_request_without_metadata_fails_closed() -> None:
    request, decision = _review(_candidate())

    with pytest.raises(V1ApprovalEnforcementError, match="approval_metadata"):
        enforce_v1_destructive_approval(request, decision, None)  # type: ignore[arg-type]


def test_v1_g14_safe_requests_are_not_upgraded_to_approval_enforcement() -> None:
    request, decision = _review(
        _candidate(
            action_category="informational",
            requested_action="summarize status",
            risk_tier="low",
            approval_state="proposed",
            target_ref="ref:summary",
        )
    )

    with pytest.raises(V1ApprovalEnforcementError, match="operator approval|file operation"):
        enforce_v1_destructive_approval(
            request,
            decision,
            _approval_metadata(request, decision),
        )


@pytest.mark.parametrize(
    "field,value,match",
    [
        ("request_id", "v1-request:other", "request_id"),
        ("decision_id", "v1-decision:other", "decision_id"),
        ("actor_id", "user-other", "actor_id"),
        ("shell_id", "shell-other", "shell_id"),
        ("target_ref", "file:other.md", "target_ref"),
        ("approval_scope", "different_scope", "approval_scope"),
    ],
)
def test_v1_g14_approval_scope_mismatch_fails_closed(
    field: str,
    value: str,
    match: str,
) -> None:
    request, decision = _review(_candidate())

    with pytest.raises(V1ApprovalEnforcementError, match=match):
        enforce_v1_destructive_approval(
            request,
            decision,
            _approval_metadata(request, decision, **{field: value}),
        )


def test_v1_g14_tenant_mismatch_fails_closed_when_decision_links_tenant() -> None:
    request, decision = _review(_candidate())
    decision_with_tenant = type(decision)(
        **{
            **asdict(decision),
            "metadata": {
                **dict(decision.metadata),
                "audit_evidence_linkage": {
                    **dict(decision.metadata["audit_evidence_linkage"]),
                    "tenant_ref": "tenant:alpha",
                },
            },
        }
    )

    with pytest.raises(V1ApprovalEnforcementError, match="tenant_ref"):
        enforce_v1_destructive_approval(
            request,
            decision_with_tenant,
            _approval_metadata(request, decision_with_tenant, tenant_ref="tenant:other"),
        )


def test_v1_g14_request_decision_identity_mismatch_fails_closed() -> None:
    request, decision = _review(_candidate())
    mismatched_decision = type(decision)(
        **{
            **asdict(decision),
            "request_id": "v1-request:other",
        }
    )

    with pytest.raises(V1ApprovalEnforcementError, match="request_id"):
        enforce_v1_destructive_approval(
            request,
            mismatched_decision,
            _approval_metadata(request, decision),
        )


def test_v1_g14_approval_evidence_ref_must_be_in_evidence_refs() -> None:
    request, decision = _review(_candidate())

    with pytest.raises(V1ApprovalEnforcementError, match="approval_evidence_ref"):
        enforce_v1_destructive_approval(
            request,
            decision,
            _approval_metadata(request, decision, evidence_refs=["fixture:v1-g14"]),
        )


@pytest.mark.parametrize(
    "field,value,match",
    [
        ("approval_state", "expired", "approval_state"),
        ("approval_state", "revoked", "approval_state"),
        ("approval_state", "denied", "approval_state"),
        ("approval_state", "superseded", "approval_state"),
        ("approval_freshness", "stale", "stale"),
        ("approval_replay_status", "replayed", "replayed"),
    ],
)
def test_v1_g14_expired_revoked_denied_stale_or_replayed_evidence_fails_closed(
    field: str,
    value: str,
    match: str,
) -> None:
    request, decision = _review(_candidate())

    with pytest.raises(V1ApprovalEnforcementError, match=match):
        enforce_v1_destructive_approval(
            request,
            decision,
            _approval_metadata(request, decision, **{field: value}),
        )


@pytest.mark.parametrize(
    "field,value",
    [
        ("raw_approval_pin", "approval-pin-123456"),
        ("raw_approval_token", "approval token value"),
        ("raw_secret", "raw-secret-123"),
        ("raw_prompt", "raw prompt text"),
        ("raw_file_contents", "raw file contents"),
        ("raw_customer_data", "raw customer data"),
    ],
)
def test_v1_g14_raw_sensitive_content_fails_closed(field: str, value: str) -> None:
    request, decision = _review(_candidate())

    with pytest.raises(V1ApprovalEnforcementError, match="raw sensitive"):
        enforce_v1_destructive_approval(
            request,
            decision,
            _approval_metadata(request, decision, **{field: value}),
        )


@pytest.mark.parametrize(
    "field,value,match",
    [
        ("approved", True, "authority|forged"),
        ("guardian_decision", "forged", "authority|forged"),
        ("approval_token_issued", True, "authority|execute"),
        ("execution_allowed", True, "authority|execute"),
        ("provider_model_routed", True, "authority|execute"),
        ("tool_executed", True, "authority|execute"),
        ("browser_action_executed", True, "authority|execute"),
        ("network_action_executed", True, "authority|execute"),
        ("device_command_invoked", True, "authority|execute"),
        ("robotics_invoked", True, "authority|execute"),
        ("physical_world_invoked", True, "authority|execute"),
    ],
)
def test_v1_g14_forged_or_forbidden_surface_claims_fail_closed(
    field: str,
    value: Any,
    match: str,
) -> None:
    request, decision = _review(_candidate())

    with pytest.raises(V1ApprovalEnforcementError, match=match):
        enforce_v1_destructive_approval(
            request,
            decision,
            _approval_metadata(request, decision, **{field: value}),
        )


def test_v1_g14_outputs_do_not_emit_sensitive_values() -> None:
    request, decision = _review(_candidate())
    record = enforce_v1_destructive_approval(
        request,
        decision,
        _approval_metadata(request, decision),
    )
    output = json.dumps(record, sort_keys=True, default=str)

    for forbidden in (
        "approval-pin",
        "approval token",
        "raw-secret-123",
        "raw prompt",
        "raw file contents",
        "raw customer data",
    ):
        assert forbidden not in output
