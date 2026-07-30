"""Guardian-to-LIMA decision lineage tests for the governed runtime."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

import pytest

from lima.contracts.guardian_decision_reference import (
    BINDING_MODE,
    GuardianDecisionReference,
)
from lima.runtime import run_governed_request


HASH_A = "sha256:" + ("a" * 64)
HASH_B = "sha256:" + ("b" * 64)
HASH_C = "sha256:" + ("c" * 64)
EXPIRES = "2099-01-01T00:00:00Z"


def _binding(**overrides: Any) -> dict[str, Any]:
    value = {
        "binding_mode": BINDING_MODE,
        "decision_id": "guardian-decision:operator-request-001",
        "request_id": "operator-request-001",
        "policy_version": "guardian-policy-lab-v1",
        "policy_snapshot_hash": HASH_A,
        "valid_for_action_ref": HASH_B,
        "decision_scope_hash": HASH_C,
        "bound_tenant_id": "tenant-lab-001",
        "bound_worker_id": "arc-worker-001",
        "bound_action_type": "safe_read",
        "expires_at": EXPIRES,
    }
    value.update(overrides)
    return value


def _request(**overrides: Any) -> dict[str, Any]:
    binding = deepcopy(overrides.pop("guardian_binding", _binding()))
    trust_context = {
        "authenticated_tenant_id": binding["bound_tenant_id"],
        "worker_id": binding["bound_worker_id"],
        "guardian_decision_id": binding["decision_id"],
        "guardian_policy_version": binding["policy_version"],
        "request_hash": binding["valid_for_action_ref"],
        "payload_hash": binding["decision_scope_hash"],
        "room_execution_allowed": False,
        "execution_gate_present": False,
    }
    payload = {
        "request_id": binding["request_id"],
        "consumer": "lima_office_supervisor",
        "surface": "arc_assignment_preview",
        "actor_id": "operator-lab-001",
        "normalized_request": {
            "action": binding["bound_action_type"],
            "classification_authority": "supervisor_server_derived",
        },
        "requested_action": binding["bound_action_type"],
        "action_category": "read",
        "tool_name": "arc_status_preview",
        "guardian_binding": binding,
        "tool_args": {},
        "trust_context": trust_context,
        "evidence_refs": ["event:guardian-decision"],
    }
    payload.update(overrides)
    return payload


def test_reference_contract_round_trips_only_safe_lineage_fields() -> None:
    reference = GuardianDecisionReference.from_mapping(_binding())

    assert reference.to_dict() == _binding()
    assert reference.content_hash.startswith("sha256:")
    assert len(reference.content_hash) == 71


def test_runtime_echoes_exact_reference_without_granting_authority() -> None:
    request = _request()
    decision = run_governed_request(request)

    assert decision.metadata["guardian_binding"] == request["guardian_binding"]
    assert decision.metadata["guardian_binding_present"] is True
    assert decision.metadata["guardian_decision_id"] == request["guardian_binding"]["decision_id"]
    assert decision.metadata["guardian_binding_mode"] == BINDING_MODE
    assert decision.audit_event.metadata["guardian_decision_id"] == request[
        "guardian_binding"
    ]["decision_id"]
    assert decision.audit_event.metadata["guardian_binding_hash"] == decision.metadata[
        "guardian_binding_hash"
    ]
    assert decision.executable is False
    assert decision.execution_allowed is False
    assert decision.side_effects_allowed is False


def test_decision_identity_is_bound_to_guardian_reference() -> None:
    first = run_governed_request(_request())
    second_binding = _binding(decision_id="guardian-decision:operator-request-002")
    second = run_governed_request(_request(guardian_binding=second_binding))

    assert first.request_id == second.request_id
    assert first.decision_id != second.decision_id
    assert first.metadata["guardian_binding_hash"] != second.metadata[
        "guardian_binding_hash"
    ]


@pytest.mark.parametrize(
    ("binding_update", "request_update"),
    [
        ({"request_id": "other-request"}, {}),
        ({"bound_action_type": "external_write"}, {}),
        ({"bound_tenant_id": "other-tenant"}, {}),
        ({"bound_worker_id": "other-worker"}, {}),
        ({"valid_for_action_ref": HASH_A}, {}),
        ({"decision_scope_hash": HASH_A}, {}),
        ({"policy_version": "other-policy"}, {}),
        ({"decision_id": "other-decision"}, {}),
        ({}, {"requested_action": "external_write"}),
    ],
)
def test_mismatched_reference_fails_closed(
    binding_update: dict[str, Any],
    request_update: dict[str, Any],
) -> None:
    binding = _binding(**binding_update)
    request = _request()
    request["guardian_binding"] = binding
    request.update(request_update)
    decision = run_governed_request(request)

    assert decision.status == "denied"
    assert decision.allowed is False
    assert tuple(decision.reason_codes) == ("malformed_request", "fail_closed")
    assert decision.executable is False
    assert decision.execution_allowed is False
    assert decision.side_effects_allowed is False


def test_expired_or_extended_reference_fails_closed() -> None:
    expired = _binding(expires_at="2020-01-01T00:00:00Z")
    extended = _binding()
    extended["unexpected_authority"] = True

    for binding in (expired, extended):
        decision = run_governed_request(_request(guardian_binding=binding))
        assert decision.status == "denied"
        assert tuple(decision.reason_codes) == ("malformed_request", "fail_closed")
        assert decision.metadata.get("guardian_binding") is None


@pytest.mark.parametrize(
    ("action", "category", "tool_name", "expected_status"),
    [
        ("external_write", "external_write", "send_email", "confirm_required"),
        ("shell", "shell", "terminal_send", "denied"),
        ("credential_access", "credential_access", "vault_reveal", "privileged_required"),
        ("unknown", "unknown", "unknown_arc_action", "denied"),
    ],
)
def test_reference_never_overrides_policy_semantics(
    action: str,
    category: str,
    tool_name: str,
    expected_status: str,
) -> None:
    binding = _binding(bound_action_type=action)
    decision = run_governed_request(
        _request(
            guardian_binding=binding,
            requested_action=action,
            action_category=category,
            tool_name=tool_name,
        )
    )

    assert decision.status == expected_status
    assert decision.executable is False
    assert decision.execution_allowed is False
    assert decision.side_effects_allowed is False


def test_requests_without_reference_remain_compatible_and_non_executing() -> None:
    request = _request()
    request["guardian_binding"] = None
    request["trust_context"] = {}

    decision = run_governed_request(request)

    assert decision.metadata["guardian_binding"] is None
    assert decision.metadata["guardian_binding_present"] is False
    assert decision.metadata["guardian_binding_hash"] is None
    assert decision.executable is False
    assert decision.execution_allowed is False
    assert decision.side_effects_allowed is False
