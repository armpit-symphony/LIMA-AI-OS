"""Minimal non-executing LIMA Kernel plugin contracts."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True)
class CapabilityProfile:
    """Caller-declared capabilities for a dry-run kernel request."""

    profile_id: str = "default-deny"
    profile_version: str = "0.1"
    source: str = "caller"
    allowed_tool_packs: tuple[str, ...] = ()
    denied_tool_packs: tuple[str, ...] = ()
    approval_required_capabilities: tuple[str, ...] = ()
    model_calls: bool = False
    memory_write: bool = False
    task_state_write: bool = False
    connector_read: bool = False
    connector_write: bool = False
    external_send: bool = False
    file_write: bool = False
    process_execute: bool = False
    browser_control: bool = False
    device_control: bool = False
    robotics_actuation: bool = False
    drone_actuation: bool = False
    scheduler_run: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class KernelRequest:
    """Already-normalized request metadata accepted by the minimal kernel."""

    request_id: str
    shell_id: str
    actor_id: str
    normalized_intent: Mapping[str, Any]
    capability_profile: CapabilityProfile = field(default_factory=CapabilityProfile)
    session_id: str | None = None
    actor_context: Mapping[str, Any] = field(default_factory=dict)
    shell_context: Mapping[str, Any] = field(default_factory=dict)
    session_context: Mapping[str, Any] = field(default_factory=dict)
    memory_refs: tuple[str, ...] = ()
    source_surface: Mapping[str, Any] = field(default_factory=dict)
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class GuardianStubDecision:
    """Non-authoritative fail-closed Guardian stub metadata."""

    guardian_state: str
    reason_code: str
    decision_ref: None = None
    policy_stub: str = "minimal_fail_closed_guardian_stub"
    policy_version: str = "0.1"
    capabilities_reviewed: tuple[str, ...] = ()
    constraints: tuple[str, ...] = (
        "non_authoritative",
        "no_guardian_decision_created",
        "no_approval_enforcement",
        "no_execution_authority",
    )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class KernelEvent:
    """Redacted in-memory event emitted by the minimal kernel."""

    event_id: str
    request_id: str
    kernel_id: str
    shell_id: str
    actor_id: str
    event_type: str
    state: str
    reason_code: str
    redacted_summary: str
    session_id: str | None = None
    privacy_class: str = "unknown"
    contains_secret: bool = False
    contains_raw_prompt: bool = False
    contains_unsafe_payload: bool = False
    durable: bool = False
    in_memory_only: bool = True
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExecutionResult:
    """Dry-run result returned by the minimal non-executing kernel."""

    request_id: str
    kernel_id: str
    shell_id: str
    actor_id: str
    state: str
    guardian_summary: GuardianStubDecision
    event_refs: tuple[str, ...]
    redacted_audit_summary: str
    session_id: str | None = None
    blocked_reason: str | None = None
    approval_reason: str | None = None
    warnings: tuple[str, ...] = ()
    executable: bool = False
    execution_allowed: bool = False
    side_effects_allowed: bool = False
    dry_run: bool = True
    dispatch_allowed: bool = False
    persistence_allowed: bool = False
    model_calls_allowed: bool = False
    model_calls_executed: bool = False
    physical_world_allowed: bool = False
    physical_world_executed: bool = False
    guardian_decision_created: bool = False
    approval_enforced: bool = False
    humaninput_bridge_active: bool = False
    sparkbot_wiring_active: bool = False
    robo_os_wiring_active: bool = False
    adapter_active: bool = False
    tool_execution_allowed: bool = False
    driver_execution_allowed: bool = False
    scheduler_active: bool = False
    external_calls_allowed: bool = False
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["guardian_summary"] = self.guardian_summary.to_dict()
        return result
