"""Runtime tests for the approved V1-G11 request decision gate."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

import pytest

from lima.contracts.guardian import GuardianDecisionStatus
from lima.guardian import V1GuardianDecisionGateError, review_v1_runtime_request
from lima.kernel import V1RuntimeRequestError, build_v1_runtime_request


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g11_runtime_request_decision_gate.json"
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
    blocked_reason: str = "non_executable_candidate_requires_future_guardian_review",
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
        "blocked_reason": blocked_reason,
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


def _serialized_output(*values: Any) -> str:
    return json.dumps([asdict(value) for value in values], sort_keys=True, default=str)


def test_v1_g11_fixture_records_approved_scope_and_boundaries() -> None:
    fixture = _load_fixture()

    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g11-runtime-request-decision-gate"
    assert fixture["operator_decision"] == "Approve-V1-G11"
    assert fixture["operator"] == "Phil Lima"
    assert fixture["approved_scope"] == "typed_request_guardian_decision_preflight_runtime_slice"
    assert set(fixture["runtime_symbols"]) == {
        "V1RuntimeRequestError",
        "build_v1_runtime_request",
        "V1GuardianDecisionGateError",
        "review_v1_runtime_request",
    }
    assert all(value is False for value in fixture["forbidden_behavior"].values())


@pytest.mark.parametrize("category", ["informational", "planning", "drafting"])
def test_v1_g11_safe_candidate_produces_reviewed_non_executing_decision(
    category: str,
) -> None:
    request, decision = _review(
        _candidate(action_category=category, requested_action=f"{category} response")
    )

    assert request.metadata["non_executing"] is True
    assert request.metadata["execution_allowed"] is False
    assert request.metadata["approval_token_issued"] is False
    assert decision.status is GuardianDecisionStatus.APPROVED
    assert decision.constraints["non_executing"] is True
    assert decision.constraints["execution_allowed"] is False
    assert decision.constraints["approval_token_issued"] is False
    assert decision.allowed_tool_packs == ()


@pytest.mark.parametrize("requested_action", ["edit project file", "delete project file"])
def test_v1_g11_destructive_edit_delete_requires_operator_approval(
    requested_action: str,
) -> None:
    request, decision = _review(
        _candidate(
            action_category="file_mutation",
            requested_action=requested_action,
            risk_tier="high",
            approval_state="approval_required",
            blocked_reason="risky_request_requires_future_guardian_review",
            target_ref="file:project.md",
        )
    )

    assert request.typed_args["destructive"] is True
    assert decision.status is GuardianDecisionStatus.NEEDS_OPERATOR_PIN
    assert decision.approval_level == "operator_pin"
    assert decision.constraints["execution_allowed"] is False
    assert decision.metadata["approval_token_issued"] is False


def test_v1_g11_caller_supplied_approval_claim_is_blocked() -> None:
    with pytest.raises(V1RuntimeRequestError, match="approval"):
        build_v1_runtime_request(_candidate(approved=True))


def test_v1_g11_caller_supplied_guardian_decision_authority_is_blocked() -> None:
    with pytest.raises(V1RuntimeRequestError, match="GuardianDecision|authority"):
        build_v1_runtime_request(_candidate(guardian_decision_created=True))


@pytest.mark.parametrize(
    "field,value,match",
    [
        ("freshness", "stale", "stale"),
        ("replay_status", "replayed", "replayed"),
    ],
)
def test_v1_g11_stale_or_replayed_candidate_is_blocked(
    field: str,
    value: str,
    match: str,
) -> None:
    candidate = _candidate()
    candidate[field] = value

    with pytest.raises(V1RuntimeRequestError, match=match):
        build_v1_runtime_request(candidate)


def test_v1_g11_missing_provenance_is_blocked() -> None:
    candidate = _candidate()
    del candidate["provenance"]

    with pytest.raises(V1RuntimeRequestError, match="provenance|validation"):
        build_v1_runtime_request(candidate)


def test_v1_g11_raw_natural_language_payload_is_blocked() -> None:
    with pytest.raises(V1RuntimeRequestError, match="raw natural-language"):
        build_v1_runtime_request(_candidate(raw_text="delete that file"))


def test_v1_g11_unknown_action_type_is_denied_without_execution() -> None:
    _request, decision = _review(
        _candidate(
            action_category="unknown",
            requested_action="unknown future action",
            risk_tier="blocked",
            approval_state="blocked",
            blocked_reason="unknown_action_category_not_execution_ready",
        )
    )

    assert decision.status is GuardianDecisionStatus.DENIED
    assert decision.constraints["execution_allowed"] is False


@pytest.mark.parametrize(
    "category",
    ["model_call", "tool_call", "browser_network", "robotics_physical_world"],
)
def test_v1_g11_future_policy_claims_do_not_route_or_execute(category: str) -> None:
    request, decision = _review(
        _candidate(
            action_category=category,
            requested_action=f"{category} request",
            risk_tier="high",
            approval_state="approval_required",
            blocked_reason="risky_request_requires_future_guardian_review",
        )
    )

    assert request.metadata["provider_model_routing_allowed"] is False
    assert decision.status is GuardianDecisionStatus.DENIED
    assert decision.constraints["provider_model_routed"] is False
    assert decision.constraints["shell_wired"] is False
    assert decision.constraints["execution_allowed"] is False


def test_v1_g11_audit_evidence_linkage_is_present_and_non_persistent() -> None:
    request, decision = _review(_candidate())

    request_linkage = request.metadata["audit_evidence_linkage"]
    decision_linkage = decision.metadata["audit_evidence_linkage"]

    assert request_linkage["lineage_id"] == decision_linkage["lineage_id"]
    assert decision_linkage["decision_id"] == decision.decision_id
    assert decision_linkage["request_id"] == request.request_id
    assert decision_linkage["input_id"] == request.input_id
    assert decision_linkage["actor_id"] == request.actor_id
    assert decision_linkage["shell_id"] == request.shell_id
    assert decision_linkage["persistent"] is False
    assert decision.constraints["persistent"] is False


def test_v1_g11_outputs_do_not_emit_raw_sensitive_values() -> None:
    request, decision = _review(
        _candidate(
            metadata={"secret_value": "raw-secret-123"},
            normalized_request="summarize without raw prompt",
        )
    )
    output = _serialized_output(request, decision)

    for forbidden in (
        "raw-secret-123",
        "approval-pin",
        "approval-token-value",
        "raw file contents",
    ):
        assert forbidden not in output


def test_v1_g11_gate_rejects_forged_request_authority_metadata() -> None:
    request = build_v1_runtime_request(_candidate())
    forged = type(request)(
        **{
            **asdict(request),
            "metadata": {
                **dict(request.metadata),
                "guardian_decision": "forged-decision",
            },
        }
    )

    with pytest.raises(V1GuardianDecisionGateError, match="authority"):
        review_v1_runtime_request(forged)
