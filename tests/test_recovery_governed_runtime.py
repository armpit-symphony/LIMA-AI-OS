"""Recovery tests for the public governed dry-run runtime kernel."""

from __future__ import annotations

from typing import Any

import pytest

from lima.contracts import GovernedDecision, GovernedRequest
from lima.governed_kernel import guardian_core_policy_adapter
from lima.governed_kernel.policy_adapter import map_guardian_semantic
from lima.runtime import run_governed_request


@pytest.fixture(autouse=True)
def _force_static_policy_for_recovery_tests(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def unavailable() -> None:
        raise ModuleNotFoundError('guardian_core is intentionally unavailable')

    monkeypatch.setattr(
        guardian_core_policy_adapter,
        '_load_guardian_core_decider',
        unavailable,
    )


def _request(**overrides: Any) -> dict[str, Any]:
    payload = {
        "request_id": "req-1",
        "consumer": "manual",
        "surface": "cli",
        "actor_id": "operator",
        "normalized_request": "show status",
        "requested_action": "read_status",
        "action_category": "read",
        "tool_name": "get_datetime",
        "tool_args": {},
        "trust_context": {},
        "evidence_refs": ["evidence:req-1"],
    }
    payload.update(overrides)
    return payload


def test_public_api_importable() -> None:
    assert callable(run_governed_request)


def test_safe_read_request_returns_allowed_dry_run() -> None:
    decision = run_governed_request(_request())

    assert decision.status == "allowed_dry_run"
    assert decision.allowed is True
    assert decision.requires_approval is False
    assert decision.audit_event.status == "allowed_dry_run"


def test_external_write_request_returns_confirm_required() -> None:
    decision = run_governed_request(
        _request(
            request_id="req-write",
            normalized_request="draft and send email",
            requested_action="send_external_email",
            action_category="external_write",
            tool_name="send_email",
        )
    )

    assert decision.status == "confirm_required"
    assert decision.allowed is False
    assert decision.requires_approval is True


def test_shell_tool_execution_request_returns_denied() -> None:
    decision = run_governed_request(
        _request(
            request_id="req-shell",
            requested_action="run shell command",
            action_category="shell",
            tool_name="terminal_send",
        )
    )

    assert decision.status == "denied"
    assert "execution_blocked" in decision.reason_codes


def test_vault_reveal_request_returns_privileged_required() -> None:
    decision = run_governed_request(
        _request(
            request_id="req-vault",
            requested_action="reveal vault secret",
            action_category="secret_access",
            tool_name="vault_reveal",
        )
    )

    assert decision.status == "privileged_required"
    assert decision.requires_approval is True


def test_unknown_tool_or_action_returns_denied() -> None:
    decision = run_governed_request(
        _request(
            request_id="req-unknown",
            requested_action="do unclear thing",
            action_category="unknown",
            tool_name="mystery_tool",
        )
    )

    assert decision.status == "denied"
    assert "unknown_tool_or_action" in decision.reason_codes


def test_malformed_request_fails_closed() -> None:
    decision = run_governed_request({"request_id": "bad-1", "consumer": "manual"})

    assert decision.status == "denied"
    assert decision.allowed is False
    assert "malformed_request" in decision.reason_codes


def test_sparkbot_shaped_normalized_fixture_returns_decision() -> None:
    decision = run_governed_request(
        _request(
            request_id="sparkbot-preview-1",
            consumer="sparkbot",
            surface="public-preview-api",
            actor_id="public-user",
            normalized_request={
                "message": "Preview whether this status request is allowed",
                "public_notice": "LIMA decision preview is non-executing",
            },
            requested_action="preview_status",
            action_category="preview",
            tool_name="sparkbot_decision_preview",
        )
    )

    assert isinstance(decision, GovernedDecision)
    assert decision.consumer == "sparkbot"
    assert decision.status == "allowed_dry_run"


def test_arc_shaped_normalized_fixture_returns_decision() -> None:
    decision = run_governed_request(
        _request(
            request_id="arc-preflight-1",
            consumer="arc-bot",
            surface="arc_guardian_spine",
            actor_id="arc-operator",
            normalized_request={
                "arc_action_id": "arc-action-1",
                "role": "office-status-worker",
                "intent": "show office status",
            },
            requested_action="read_status",
            action_category="read",
            tool_name="arc_status_preview",
        )
    )

    assert isinstance(decision, GovernedDecision)
    assert decision.consumer == "arc-bot"
    assert decision.status == "allowed_dry_run"


def test_no_decision_allows_execution_or_side_effects() -> None:
    decisions = [
        run_governed_request(_request()),
        run_governed_request(
            _request(
                request_id="req-confirm",
                action_category="external_write",
                tool_name="send_email",
            )
        ),
        run_governed_request(
            _request(
                request_id="req-deny",
                action_category="shell",
                tool_name="terminal_send",
            )
        ),
        run_governed_request(
            _request(
                request_id="req-vault-2",
                action_category="secret_access",
                tool_name="vault_reveal",
            )
        ),
        run_governed_request({"request_id": "bad-2"}),
    ]

    for decision in decisions:
        assert decision.executable is False
        assert decision.execution_allowed is False
        assert decision.side_effects_allowed is False
        assert decision.audit_event.executable is False
        assert decision.audit_event.execution_allowed is False
        assert decision.audit_event.side_effects_allowed is False


def test_guardian_policy_semantic_mapping_is_preserved() -> None:
    assert map_guardian_semantic("allow").status == "allowed_dry_run"
    assert map_guardian_semantic("confirm").status == "confirm_required"
    assert map_guardian_semantic("deny").status == "denied"
    assert map_guardian_semantic("privileged").status == "privileged_required"
    assert map_guardian_semantic("privileged_reveal").status == "privileged_required"


def test_governed_request_dataclass_input_is_supported() -> None:
    request = GovernedRequest.from_mapping(_request(request_id="dataclass-1"))

    decision = run_governed_request(request)

    assert decision.request_id == "dataclass-1"
    assert decision.status == "allowed_dry_run"
