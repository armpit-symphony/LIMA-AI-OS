"""Guardian Core policy integration tests for LIMA governed runtime."""

from __future__ import annotations

from dataclasses import dataclass
from types import ModuleType
from typing import Any
import sys

import pytest

from lima.guardian.guardian_core_policy_adapter import (
    GUARDIAN_CORE_SOURCE_POLICY,
    STATIC_FALLBACK_SOURCE_POLICY,
)
from lima.runtime import run_governed_request


@dataclass(frozen=True)
class FakeGuardianCoreDecision:
    tool_name: str
    action: str
    high_risk: bool = False
    reason: str = "fake guardian core decision"
    scope: str = "read"
    resource: str = "test"
    action_type: str = "test"


def _request(**overrides: Any) -> dict[str, Any]:
    payload = {
        "request_id": "guardian-core-req-1",
        "consumer": "manual",
        "surface": "test",
        "actor_id": "operator",
        "normalized_request": "show status",
        "requested_action": "read_status",
        "action_category": "read",
        "tool_name": "get_datetime",
        "tool_args": {},
        "trust_context": {},
        "evidence_refs": ["evidence:guardian-core-req-1"],
    }
    payload.update(overrides)
    return payload


def _install_fake_guardian_core(monkeypatch: pytest.MonkeyPatch, action: str | None = None) -> list[dict[str, Any]]:
    calls: list[dict[str, Any]] = []
    guardian_core_module = ModuleType("guardian_core")
    policy_module = ModuleType("guardian_core.policy")

    def decide_tool_use(
        tool_name: str,
        args: dict[str, Any] | None = None,
        *,
        room_execution_allowed: bool | None = None,
        is_operator: bool = False,
        is_privileged: bool = False,
        extra_policies: dict[str, dict[str, Any]] | None = None,
    ) -> FakeGuardianCoreDecision:
        policy = (extra_policies or {}).get(tool_name, {})
        selected_action = action or str(policy.get("default_action") or "deny")
        if tool_name == "server_read_command" and not room_execution_allowed:
            selected_action = "deny"
        calls.append(
            {
                "tool_name": tool_name,
                "args": args or {},
                "room_execution_allowed": room_execution_allowed,
                "is_operator": is_operator,
                "is_privileged": is_privileged,
                "extra_policies": extra_policies or {},
                "action": selected_action,
            }
        )
        return FakeGuardianCoreDecision(
            tool_name=tool_name,
            action=selected_action,
            high_risk=bool(policy.get("high_risk")),
            scope=str(policy.get("scope") or "admin"),
            resource=str(policy.get("resource") or "test"),
            action_type=str(policy.get("action_type") or "test"),
        )

    policy_module.decide_tool_use = decide_tool_use  # type: ignore[attr-defined]
    guardian_core_module.policy = policy_module  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "guardian_core", guardian_core_module)
    monkeypatch.setitem(sys.modules, "guardian_core.policy", policy_module)
    return calls


@pytest.mark.parametrize(
    ("guardian_action", "expected_status", "expected_allowed", "expected_approval"),
    [
        ("allow", "allowed_dry_run", True, False),
        ("confirm", "confirm_required", False, True),
        ("deny", "denied", False, False),
        ("privileged", "privileged_required", False, True),
        ("privileged_reveal", "privileged_required", False, True),
    ],
)
def test_guardian_core_semantics_map_to_lima_decisions(
    monkeypatch: pytest.MonkeyPatch,
    guardian_action: str,
    expected_status: str,
    expected_allowed: bool,
    expected_approval: bool,
) -> None:
    _install_fake_guardian_core(monkeypatch, guardian_action)

    decision = run_governed_request(_request(request_id=f"semantic-{guardian_action}"))

    assert decision.status == expected_status
    assert decision.allowed is expected_allowed
    assert decision.requires_approval is expected_approval
    assert decision.source_policy == GUARDIAN_CORE_SOURCE_POLICY
    assert decision.audit_event.source_policy == GUARDIAN_CORE_SOURCE_POLICY
    assert decision.executable is False
    assert decision.execution_allowed is False
    assert decision.side_effects_allowed is False


def test_guardian_core_source_policy_is_reported_when_used(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = _install_fake_guardian_core(monkeypatch)

    decision = run_governed_request(_request(request_id="guardian-core-source"))

    assert calls
    assert calls[0]["tool_name"] == "get_datetime"
    assert decision.source_policy == "guardian_core.policy"
    assert decision.audit_event.source_policy == "guardian_core.policy"
    assert decision.metadata["guardian_semantic"] == "allow"


def test_static_fallback_is_explicit_when_guardian_core_unavailable(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delitem(sys.modules, "guardian_core", raising=False)
    monkeypatch.delitem(sys.modules, "guardian_core.policy", raising=False)

    decision = run_governed_request(_request(request_id="fallback-read"))

    assert decision.status == "allowed_dry_run"
    assert decision.source_policy == STATIC_FALLBACK_SOURCE_POLICY
    assert decision.audit_event.source_policy == STATIC_FALLBACK_SOURCE_POLICY
    assert "guardian_core_unavailable" in decision.reason_codes
    assert "static_policy_fallback" in decision.reason_codes
    assert decision.executable is False
    assert decision.execution_allowed is False
    assert decision.side_effects_allowed is False


@pytest.mark.parametrize(
    ("category", "tool_name", "expected_status"),
    [
        ("read", "get_datetime", "allowed_dry_run"),
        ("informational", "arc_status_preview", "allowed_dry_run"),
        ("planning", "arc_status_preview", "allowed_dry_run"),
        ("drafting", "sparkbot_decision_preview", "allowed_dry_run"),
        ("external_write", "send_email", "confirm_required"),
        ("tool_call", "send_message", "confirm_required"),
        ("shell", "terminal_send", "denied"),
        ("file_mutation", "update_customer_record", "confirm_required"),
        ("model_call", "execute_tool", "denied"),
        ("credential_access", "vault_reveal", "privileged_required"),
        ("connector_call", "browser_action", "denied"),
        ("physical_world", "robot_motion", "denied"),
        ("unknown", "unknown_arc_action", "denied"),
    ],
)
def test_guardian_core_category_mapping_is_stable_and_non_executing(
    monkeypatch: pytest.MonkeyPatch,
    category: str,
    tool_name: str,
    expected_status: str,
) -> None:
    calls = _install_fake_guardian_core(monkeypatch)

    decision = run_governed_request(
        _request(
            request_id=f"category-{category}",
            requested_action=f"test_{category}",
            action_category=category,
            tool_name=tool_name,
        )
    )

    assert calls
    assert decision.status == expected_status
    assert decision.source_policy == GUARDIAN_CORE_SOURCE_POLICY
    assert decision.executable is False
    assert decision.execution_allowed is False
    assert decision.side_effects_allowed is False
    assert decision.audit_event.executable is False
    assert decision.audit_event.execution_allowed is False
    assert decision.audit_event.side_effects_allowed is False


def test_arc_week2b_fixture_categories_return_stable_decisions(monkeypatch: pytest.MonkeyPatch) -> None:
    _install_fake_guardian_core(monkeypatch)
    fixtures = [
        ("arc-read", "status_read", "read", "arc_status_preview", "allowed_dry_run"),
        ("arc-send", "send_email", "external_write", "send_email", "confirm_required"),
        ("arc-shell", "shell_command_execute", "shell", "terminal_send", "denied"),
        ("arc-file", "file_write", "file_mutation", "update_customer_record", "confirm_required"),
        ("arc-model", "provider_model_route", "model_call", "execute_tool", "denied"),
        ("arc-connector", "connector_call", "connector_call", "browser_action", "denied"),
        ("arc-physical", "robot_physical_action", "physical_world", "robot_motion", "denied"),
        ("arc-unknown", "unmapped_future_action", "unknown", "unknown_arc_action", "denied"),
    ]

    for request_id, action, category, tool_name, expected_status in fixtures:
        decision = run_governed_request(
            _request(
                request_id=request_id,
                consumer="arc-bot",
                surface="arc_guardian_spine.lima_preflight",
                actor_id="arc-operator",
                normalized_request={
                    "arc_action_id": request_id,
                    "action_kind": action,
                    "worker_id": "arc-worker-test-001",
                    "tenant_id": "tenant-test",
                },
                requested_action=action,
                action_category=category,
                tool_name=tool_name,
                trust_context={"tenant_id": "tenant-test", "worker_id": "arc-worker-test-001"},
            )
        )

        assert decision.consumer == "arc-bot"
        assert decision.status == expected_status
        assert decision.source_policy == GUARDIAN_CORE_SOURCE_POLICY
        assert decision.executable is False
        assert decision.execution_allowed is False
        assert decision.side_effects_allowed is False


def test_sparkbot_public_preview_fixture_uses_same_guardian_core_path(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_fake_guardian_core(monkeypatch)

    decision = run_governed_request(
        _request(
            request_id="sparkbot-public-preview-guardian-core",
            consumer="sparkbot",
            surface="public-decision-preview",
            actor_id="public-preview-user",
            normalized_request={
                "message": "Preview whether this status request is allowed",
                "public_notice": (
                    "LIMA decision preview is non-executing and does not represent "
                    "active Guardian enforcement."
                ),
            },
            requested_action="preview_status",
            action_category="informational",
            tool_name="sparkbot_decision_preview",
        )
    )

    assert decision.consumer == "sparkbot"
    assert decision.status == "allowed_dry_run"
    assert decision.source_policy == GUARDIAN_CORE_SOURCE_POLICY
    assert decision.executable is False
    assert decision.execution_allowed is False
    assert decision.side_effects_allowed is False
