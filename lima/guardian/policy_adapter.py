"""Pure Guardian policy adapter for the governed dry-run runtime kernel.

The adapter preserves the smallest Guardian policy vocabulary without pulling
in Sparkbot application modules, databases, routes, skills, connectors, or
execution paths.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Final, Mapping

from lima.contracts.governed_request import GovernedRequest


SOURCE_POLICY: Final[str] = "lima.guardian.policy_adapter:v0.1"
READ_TOOLS: Final[frozenset[str]] = frozenset(
    {
        "get_datetime",
        "read_status",
        "show_status",
        "preview_status",
        "summarize_status",
        "arc_status_preview",
        "sparkbot_decision_preview",
    }
)
EXTERNAL_WRITE_TOOLS: Final[frozenset[str]] = frozenset(
    {
        "send_email",
        "send_message",
        "send_slack_message",
        "submit_form",
        "update_customer_record",
        "calendar_create_event",
    }
)
EXECUTION_TOOLS: Final[frozenset[str]] = frozenset(
    {
        "shell",
        "terminal",
        "terminal_send",
        "run_command",
        "execute_tool",
        "python_exec",
        "browser_action",
    }
)
VAULT_TOOLS: Final[frozenset[str]] = frozenset(
    {"vault", "vault_reveal", "reveal_secret", "read_secret", "credential_access"}
)


@dataclass(frozen=True)
class PolicyAdapterDecision:
    guardian_semantic: str
    status: str
    allowed: bool
    requires_approval: bool
    risk_level: str
    reason_codes: tuple[str, ...]
    source_policy: str = SOURCE_POLICY


def evaluate_policy(request: GovernedRequest) -> PolicyAdapterDecision:
    """Evaluate a normalized request without executing or importing app code."""

    explicit = _explicit_policy_semantic(request.trust_context)
    if explicit:
        return map_guardian_semantic(explicit)

    tool_name = _fold(request.tool_name)
    action_category = _fold(request.action_category)
    requested_action = _fold(request.requested_action)

    if _looks_privileged_reveal(tool_name, action_category, requested_action):
        return map_guardian_semantic("privileged_reveal")

    if tool_name in EXECUTION_TOOLS or action_category in {
        "execute",
        "execution",
        "shell",
        "terminal",
        "tool_execution",
        "provider_call",
        "model_call",
        "connector_call",
        "browser_network",
        "physical_world",
    }:
        return _decision(
            "deny",
            "denied",
            False,
            False,
            "blocked",
            ("execution_blocked", "dry_run_kernel_only"),
        )

    if tool_name in EXTERNAL_WRITE_TOOLS or action_category in {
        "write",
        "external_write",
        "send",
        "outbound_message",
        "form_submit",
        "record_mutation",
        "file_mutation",
    }:
        return map_guardian_semantic("confirm")

    if (
        action_category in {"read", "status", "informational", "planning", "drafting", "preview"}
        and tool_name in READ_TOOLS
    ):
        return map_guardian_semantic("allow")

    return _decision(
        "deny",
        "denied",
        False,
        False,
        "blocked",
        ("unknown_tool_or_action", "fail_closed"),
    )


def map_guardian_semantic(semantic: str) -> PolicyAdapterDecision:
    """Map Guardian Suite semantics into the public LIMA decision statuses."""

    normalized = _fold(semantic)
    if normalized == "allow":
        return _decision(
            "allow",
            "allowed_dry_run",
            True,
            False,
            "low",
            ("safe_read_or_preview", "dry_run_only"),
        )
    if normalized == "confirm":
        return _decision(
            "confirm",
            "confirm_required",
            False,
            True,
            "medium",
            ("human_confirmation_required", "side_effects_blocked"),
        )
    if normalized == "deny":
        return _decision(
            "deny",
            "denied",
            False,
            False,
            "blocked",
            ("policy_denied", "fail_closed"),
        )
    if normalized == "privileged":
        return _decision(
            "privileged",
            "privileged_required",
            False,
            True,
            "high",
            ("privileged_state_required", "side_effects_blocked"),
        )
    if normalized == "privileged_reveal":
        return _decision(
            "privileged_reveal",
            "privileged_required",
            False,
            True,
            "high",
            ("privileged_reveal_blocked", "operator_privilege_required"),
        )
    return _decision(
        "deny",
        "denied",
        False,
        False,
        "blocked",
        ("unknown_guardian_semantic", "fail_closed"),
    )


def _explicit_policy_semantic(trust_context: Mapping[str, Any]) -> str | None:
    value = (
        trust_context.get("guardian_policy_semantic")
        or trust_context.get("guardian_semantic")
        or trust_context.get("policy_semantic")
    )
    if isinstance(value, str) and value.strip():
        return value
    return None


def _looks_privileged_reveal(
    tool_name: str,
    action_category: str,
    requested_action: str,
) -> bool:
    if tool_name in VAULT_TOOLS:
        return True
    if action_category in {"vault", "secret", "secret_access", "credential_access"}:
        return True
    return any(marker in requested_action for marker in ("vault", "secret", "credential", "reveal"))


def _decision(
    guardian_semantic: str,
    status: str,
    allowed: bool,
    requires_approval: bool,
    risk_level: str,
    reason_codes: tuple[str, ...],
) -> PolicyAdapterDecision:
    return PolicyAdapterDecision(
        guardian_semantic=guardian_semantic,
        status=status,
        allowed=allowed,
        requires_approval=requires_approval,
        risk_level=risk_level,
        reason_codes=reason_codes,
    )


def _fold(value: Any) -> str:
    return str(value or "").strip().lower()
