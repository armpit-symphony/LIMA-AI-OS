"""Contract and issuance proofs for the bounded execution grant."""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timedelta, timezone
from typing import Any

import pytest

from lima.contracts.governed_decision import GovernedDecision
from lima.contracts.governed_execution_grant import (
    GRANT_CONTRACT,
    GRANT_MODE,
    GRANT_VERSION,
    MAX_TTL_SECONDS,
    GovernedExecutionGrant,
)
from lima.contracts.guardian_decision_reference import (
    BINDING_MODE,
    GuardianDecisionReference,
)
from lima.runtime import ExecutionGrantDenied, issue_execution_grant, run_governed_request


# Anchored to the real clock so the fixtures never age into expiry.
NOW = datetime.now(timezone.utc).replace(microsecond=0)
_HASH_A = "sha256:" + "a" * 64
_HASH_B = "sha256:" + "b" * 64
_HASH_C = "sha256:" + "c" * 64


def _binding(**overrides: Any) -> GuardianDecisionReference:
    values: dict[str, Any] = {
        "binding_mode": BINDING_MODE,
        "decision_id": "gd-001",
        "request_id": "req-001",
        "policy_version": "guardian-policy-lab-v1",
        "policy_snapshot_hash": _HASH_A,
        "valid_for_action_ref": _HASH_B,
        "decision_scope_hash": _HASH_C,
        "bound_tenant_id": "tenant-1",
        "bound_worker_id": "worker-1",
        "bound_action_type": "arc.safe_read",
        "expires_at": (NOW + timedelta(minutes=10)).isoformat().replace("+00:00", "Z"),
    }
    values.update(overrides)
    return GuardianDecisionReference.from_mapping(values)


def _request(**overrides: Any) -> dict[str, Any]:
    binding = overrides.pop("binding", _binding())
    payload: dict[str, Any] = {
        "request_id": "req-001",
        "consumer": "lima_office_supervisor",
        "surface": "arc_assignment_preview",
        "actor_id": "operator-1",
        "normalized_request": {"action": "arc.safe_read"},
        "requested_action": "arc.safe_read",
        "action_category": "informational",
        "tool_name": "arc_safe_read",
        "tool_args": {},
        "trust_context": {
            "authenticated_tenant_id": "tenant-1",
            "worker_id": "worker-1",
            "guardian_decision_id": "gd-001",
            "guardian_policy_version": "guardian-policy-lab-v1",
            "request_hash": _HASH_B,
            "payload_hash": _HASH_C,
        },
        "evidence_refs": ["evidence://arc/req-001"],
    }
    if binding is not None:
        payload["guardian_binding"] = binding.to_dict()
    payload.update(overrides)
    return payload


def _allowed_pair() -> tuple[dict[str, Any], GovernedDecision]:
    payload = _request()
    decision = run_governed_request(payload)
    assert decision.status == "allowed_dry_run"
    assert decision.allowed is True
    return payload, decision


def _grant(**kwargs: Any) -> GovernedExecutionGrant:
    payload, decision = _allowed_pair()
    params: dict[str, Any] = {
        "capability": "arc.safe_read",
        "side_effects_allowed": False,
        "now": NOW,
    }
    params.update(kwargs)
    return issue_execution_grant(payload, decision, **params)


# --------------------------------------------------------------------------
# The decision contract must remain incapable of authorizing execution.
# --------------------------------------------------------------------------


def test_governed_decision_still_cannot_authorize_execution() -> None:
    _, decision = _allowed_pair()
    assert decision.executable is False
    assert decision.execution_allowed is False
    assert decision.side_effects_allowed is False
    published = decision.to_dict()
    assert published["executable"] is False
    assert published["execution_allowed"] is False
    assert published["side_effects_allowed"] is False
    assert "grant" not in published
    assert "execution_grant" not in published

    for field in ("executable", "execution_allowed", "side_effects_allowed"):
        with pytest.raises(ValueError):
            replace(decision, **{field: True})


# --------------------------------------------------------------------------
# Happy path.
# --------------------------------------------------------------------------


def test_issued_grant_is_bound_and_authorizes_execution() -> None:
    grant = _grant()
    assert grant.execution_allowed is True
    assert grant.requires_operator_opt_in is True
    assert grant.side_effects_allowed is False
    assert grant.grant_contract == GRANT_CONTRACT
    assert grant.grant_version == GRANT_VERSION
    assert grant.grant_mode == GRANT_MODE
    assert grant.request_id == "req-001"
    assert grant.guardian_decision_id == "gd-001"
    assert grant.bound_tenant_id == "tenant-1"
    assert grant.bound_worker_id == "worker-1"
    assert grant.bound_action_type == "arc.safe_read"
    assert grant.granted_capability == "arc.safe_read"


def test_grant_round_trips_through_mapping() -> None:
    grant = _grant()
    restored = GovernedExecutionGrant.from_mapping(grant.to_dict())
    assert restored == grant
    assert restored.content_hash == grant.content_hash


def test_grant_exposes_a_consumption_key_for_single_use_enforcement() -> None:
    grant = _grant()
    assert grant.consumption_key == (
        "tenant-1",
        "worker-1",
        grant.grant_id,
        grant.nonce,
    )


def test_distinct_issuances_are_individually_consumable() -> None:
    first = _grant(nonce="nonce-one")
    second = _grant(nonce="nonce-two")
    assert first.grant_id != second.grant_id
    assert first.consumption_key != second.consumption_key


# --------------------------------------------------------------------------
# The operator opt-in gate cannot be waived in v0.1.
# --------------------------------------------------------------------------


def test_grant_cannot_waive_the_operator_opt_in_gate() -> None:
    grant = _grant()
    with pytest.raises(ValueError):
        replace(grant, requires_operator_opt_in=False)

    payload = dict(grant.to_dict())
    payload["requires_operator_opt_in"] = False
    with pytest.raises(ValueError):
        GovernedExecutionGrant.from_mapping(payload)


def test_grant_cannot_disclaim_execution() -> None:
    grant = _grant()
    with pytest.raises(ValueError):
        replace(grant, execution_allowed=False)


# --------------------------------------------------------------------------
# Issuance preconditions. Every one of these must deny.
# --------------------------------------------------------------------------


def test_issuance_requires_a_guardian_binding() -> None:
    payload = _request(binding=None)
    decision = run_governed_request(payload)
    with pytest.raises(ExecutionGrantDenied) as excinfo:
        issue_execution_grant(
            payload,
            decision,
            capability="arc.safe_read",
            side_effects_allowed=False,
            now=NOW,
        )
    assert excinfo.value.reason_code == "guardian_binding_required"


@pytest.mark.parametrize(
    ("action_kind", "expected_status"),
    [
        ("arc.shell_command", "denied"),
        ("arc.credential_access", "privileged_required"),
    ],
)
def test_issuance_denies_non_allowed_decisions(
    action_kind: str,
    expected_status: str,
) -> None:
    binding = _binding(bound_action_type=action_kind)
    payload = _request(binding=binding)
    payload["requested_action"] = action_kind
    payload["action_category"] = (
        "shell" if action_kind == "arc.shell_command" else "credential_access"
    )
    payload["trust_context"] = dict(payload["trust_context"])
    decision = run_governed_request(payload)
    assert decision.status != "allowed_dry_run"

    with pytest.raises(ExecutionGrantDenied) as excinfo:
        issue_execution_grant(
            payload,
            decision,
            capability=action_kind,
            side_effects_allowed=False,
            now=NOW,
        )
    assert excinfo.value.reason_code in {
        "decision_not_allowed",
        "decision_status_not_grantable",
        "approval_still_required",
    }


def test_issuance_denies_a_decision_for_a_different_request() -> None:
    payload, _ = _allowed_pair()
    other_payload = _request(binding=_binding(request_id="req-002"))
    other_payload["request_id"] = "req-002"
    other_decision = run_governed_request(other_payload)

    with pytest.raises(ExecutionGrantDenied) as excinfo:
        issue_execution_grant(
            payload,
            other_decision,
            capability="arc.safe_read",
            side_effects_allowed=False,
            now=NOW,
        )
    assert excinfo.value.reason_code == "decision_request_mismatch"


def test_issuance_denies_a_fail_closed_decision() -> None:
    malformed = {"request_id": "req-001", "consumer": "arc-bot"}
    fail_closed = run_governed_request(malformed)
    assert fail_closed.source_policy == "lima.runtime.fail_closed:v0.1"

    payload, _ = _allowed_pair()
    with pytest.raises(ExecutionGrantDenied) as excinfo:
        issue_execution_grant(
            payload,
            fail_closed,
            capability="arc.safe_read",
            side_effects_allowed=False,
            now=NOW,
        )
    assert excinfo.value.reason_code in {
        "guardian_core_policy_required",
        "decision_not_allowed",
    }


def test_issuance_denies_a_malformed_request() -> None:
    _, decision = _allowed_pair()
    with pytest.raises(ExecutionGrantDenied) as excinfo:
        issue_execution_grant(
            {"request_id": "req-001"},
            decision,
            capability="arc.safe_read",
            side_effects_allowed=False,
            now=NOW,
        )
    assert excinfo.value.reason_code == "malformed_request"


@pytest.mark.parametrize("capability", ["", "   ", None, 5])
def test_issuance_requires_an_explicit_capability(capability: Any) -> None:
    payload, decision = _allowed_pair()
    with pytest.raises(ExecutionGrantDenied) as excinfo:
        issue_execution_grant(
            payload,
            decision,
            capability=capability,
            side_effects_allowed=False,
            now=NOW,
        )
    assert excinfo.value.reason_code == "capability_required"


@pytest.mark.parametrize("ttl", [0, -1, MAX_TTL_SECONDS + 1, True, 1.5, "60"])
def test_issuance_rejects_out_of_bounds_ttl(ttl: Any) -> None:
    payload, decision = _allowed_pair()
    with pytest.raises(ExecutionGrantDenied) as excinfo:
        issue_execution_grant(
            payload,
            decision,
            capability="arc.safe_read",
            side_effects_allowed=False,
            ttl_seconds=ttl,
            now=NOW,
        )
    assert excinfo.value.reason_code == "ttl_invalid"


def test_issuance_requires_a_real_governed_decision() -> None:
    payload, decision = _allowed_pair()
    with pytest.raises(ExecutionGrantDenied) as excinfo:
        issue_execution_grant(
            payload,
            decision.to_dict(),  # a mapping, not a GovernedDecision
            capability="arc.safe_read",
            side_effects_allowed=False,
            now=NOW,
        )
    assert excinfo.value.reason_code == "governed_decision_required"


# --------------------------------------------------------------------------
# Presentation-time binding and expiry.
# --------------------------------------------------------------------------


def _binding_kwargs(grant: GovernedExecutionGrant) -> dict[str, Any]:
    return {
        "request_id": grant.request_id,
        "decision_id": grant.decision_id,
        "guardian_binding_hash": grant.guardian_binding_hash,
        "tenant_id": grant.bound_tenant_id,
        "worker_id": grant.bound_worker_id,
        "action_type": grant.bound_action_type,
        "capability": grant.granted_capability,
    }


def test_validate_binding_accepts_its_own_subject() -> None:
    grant = _grant()
    grant.validate_binding(**_binding_kwargs(grant))


@pytest.mark.parametrize(
    "field",
    [
        "request_id",
        "decision_id",
        "guardian_binding_hash",
        "tenant_id",
        "worker_id",
        "action_type",
        "capability",
    ],
)
def test_validate_binding_rejects_any_substituted_subject(field: str) -> None:
    grant = _grant()
    kwargs = _binding_kwargs(grant)
    kwargs[field] = "substituted-value"
    with pytest.raises(ValueError):
        grant.validate_binding(**kwargs)


def test_grant_expires() -> None:
    grant = _grant(ttl_seconds=60)
    grant.validate(now=NOW + timedelta(seconds=59))
    with pytest.raises(ValueError):
        grant.validate(now=NOW + timedelta(seconds=61))


def test_grant_lifetime_cannot_be_widened_after_issuance() -> None:
    grant = _grant(ttl_seconds=60)
    widened = dict(grant.to_dict())
    widened["expires_at"] = (
        (NOW + timedelta(seconds=MAX_TTL_SECONDS + 60))
        .isoformat()
        .replace("+00:00", "Z")
    )
    with pytest.raises(ValueError):
        GovernedExecutionGrant.from_mapping(widened)


def test_validation_clock_must_be_timezone_aware() -> None:
    grant = _grant()
    with pytest.raises(ValueError):
        grant.validate(now=datetime(2026, 7, 31, 12, 0, 0))


# --------------------------------------------------------------------------
# Contract shape.
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "field",
    ["grant_contract", "grant_version", "grant_mode"],
)
def test_unsupported_contract_identity_is_rejected(field: str) -> None:
    grant = _grant()
    payload = dict(grant.to_dict())
    payload[field] = "something-else"
    with pytest.raises(ValueError):
        GovernedExecutionGrant.from_mapping(payload)


def test_unknown_or_missing_fields_are_rejected() -> None:
    grant = _grant()
    extra = dict(grant.to_dict())
    extra["smuggled"] = True
    with pytest.raises(ValueError):
        GovernedExecutionGrant.from_mapping(extra)

    missing = dict(grant.to_dict())
    del missing["nonce"]
    with pytest.raises(ValueError):
        GovernedExecutionGrant.from_mapping(missing)


@pytest.mark.parametrize(
    "field",
    ["policy_snapshot_hash", "guardian_binding_hash", "scope_hash"],
)
def test_hash_fields_must_be_sha256_references(field: str) -> None:
    grant = _grant()
    payload = dict(grant.to_dict())
    payload[field] = "not-a-hash"
    with pytest.raises(ValueError):
        GovernedExecutionGrant.from_mapping(payload)


@pytest.mark.parametrize(
    "field",
    ["execution_allowed", "side_effects_allowed", "requires_operator_opt_in"],
)
def test_flag_fields_must_be_real_booleans(field: str) -> None:
    grant = _grant()
    payload = dict(grant.to_dict())
    payload[field] = "true"
    with pytest.raises(ValueError):
        GovernedExecutionGrant.from_mapping(payload)


def test_scope_hash_covers_the_side_effect_flag() -> None:
    without = _grant(side_effects_allowed=False, nonce="fixed-nonce")
    with_effects = _grant(side_effects_allowed=True, nonce="fixed-nonce")
    assert without.scope_hash != with_effects.scope_hash


def test_issuance_performs_no_execution_and_leaks_no_internal_detail() -> None:
    payload, decision = _allowed_pair()
    grant = issue_execution_grant(
        payload,
        decision,
        capability="arc.safe_read",
        side_effects_allowed=False,
        now=NOW,
    )
    published = repr(grant.to_dict())
    assert "Traceback" not in published
    assert "lima\\runtime.py" not in published
    assert "/lima/runtime.py" not in published
    # The decision that authorized the grant still authorizes nothing itself.
    assert decision.execution_allowed is False
