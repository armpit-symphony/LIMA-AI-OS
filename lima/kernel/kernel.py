"""Minimal non-executing LIMA Kernel runtime surface."""

from __future__ import annotations

from typing import Any, Final, Mapping

from .plugin_contract import (
    CapabilityProfile,
    ExecutionResult,
    GuardianStubDecision,
    KernelEvent,
    KernelRequest,
)


SAFE_ACTION_CATEGORIES: Final[frozenset[str]] = frozenset(
    {"informational", "planning", "drafting", "text_preview"}
)
APPROVAL_REQUIRED_CAPABILITIES: Final[frozenset[str]] = frozenset(
    {
        "model_calls",
        "memory_write",
        "task_state_write",
        "connector_read",
        "connector_write",
        "external_send",
        "file_write",
        "browser_control",
        "scheduler_run",
    }
)
BLOCKED_CAPABILITIES: Final[frozenset[str]] = frozenset(
    {"process_execute", "device_control", "robotics_actuation", "drone_actuation"}
)
ACTION_CAPABILITY_MAP: Final[dict[str, str]] = {
    "model_call": "model_calls",
    "memory_write": "memory_write",
    "task_state_write": "task_state_write",
    "connector_read": "connector_read",
    "network_action": "connector_read",
    "connector_write": "connector_write",
    "external_send": "external_send",
    "send_message": "external_send",
    "file_write": "file_write",
    "file_operation": "file_write",
    "process_execute": "process_execute",
    "terminal_command": "process_execute",
    "browser_control": "browser_control",
    "browser_action": "browser_control",
    "device_control": "device_control",
    "driver_command": "device_control",
    "robotics_actuation": "robotics_actuation",
    "robot_action": "robotics_actuation",
    "drone_actuation": "drone_actuation",
    "scheduler_run": "scheduler_run",
}
AUTHORITY_CLAIM_MARKERS: Final[frozenset[str]] = frozenset(
    {
        "approve",
        "approved",
        "approval",
        "authorize",
        "authorized",
        "bypass",
        "override",
        "execute",
        "dispatch",
        "persist",
        "trusted",
        "urgent",
        "breakglass",
    }
)
CONNECTION_DISCOVERY_MARKERS: Final[frozenset[str]] = frozenset(
    {
        "wifi",
        "wi",
        "fi",
        "bluetooth",
        "iot",
        "lan",
        "ble",
        "serial",
        "usb",
        "mqtt",
        "matter",
        "mdns",
        "pairing",
        "pair",
        "scan",
        "discovery",
        "discover",
        "connect",
        "connection",
        "autoconnect",
    }
)


class LimaKernel:
    """Shell-facing fail-closed kernel object for dry-run evaluation only."""

    def __init__(
        self,
        *,
        kernel_id: str = "lima-minimal-kernel",
        shell_manifest: Mapping[str, Any] | None = None,
        guardian: Any | None = None,
        event_sink: Any | None = None,
        provider_registry: Any | None = None,
        storage: Any | None = None,
        humaninput_bridge: Any | None = None,
        driver_registry: Any | None = None,
    ) -> None:
        self.kernel_id = _non_empty_text(kernel_id, "kernel_id")
        self.shell_manifest = dict(shell_manifest or {})
        self.guardian = guardian
        self.event_sink = event_sink
        self.provider_registry = provider_registry
        self.storage = storage
        self.humaninput_bridge = humaninput_bridge
        self.driver_registry = driver_registry
        self._events: list[KernelEvent] = []

    @property
    def events(self) -> tuple[KernelEvent, ...]:
        """Return redacted in-memory events emitted by this kernel instance."""

        return tuple(self._events)

    def evaluate(self, request: KernelRequest | Mapping[str, Any]) -> ExecutionResult:
        """Evaluate already-normalized metadata without executing anything."""

        kernel_request = _coerce_request(request)
        decision = self._evaluate_guardian_stub(kernel_request)
        event_refs = (
            self._append_event(kernel_request, "kernel.request_received", decision),
            self._append_event(kernel_request, "kernel.guardian_stub_evaluated", decision),
        )
        return ExecutionResult(
            request_id=kernel_request.request_id,
            kernel_id=self.kernel_id,
            shell_id=kernel_request.shell_id,
            actor_id=kernel_request.actor_id,
            session_id=kernel_request.session_id,
            state=decision.guardian_state,
            guardian_summary=decision,
            event_refs=event_refs,
            redacted_audit_summary=_redacted_summary(
                kernel_request,
                decision.guardian_state,
                decision.reason_code,
            ),
            blocked_reason=decision.reason_code if decision.guardian_state == "blocked" else None,
            approval_reason=(
                decision.reason_code if decision.guardian_state == "approval_required" else None
            ),
            warnings=_warnings(kernel_request, decision),
            metadata={
                "non_executing_minimal_kernel": True,
                "provider_registry_present": self.provider_registry is not None,
                "storage_present": self.storage is not None,
                "humaninput_bridge_present": self.humaninput_bridge is not None,
                "driver_registry_present": self.driver_registry is not None,
            },
        )

    def _evaluate_guardian_stub(self, request: KernelRequest) -> GuardianStubDecision:
        capability = _requested_capability(request)
        reviewed = (capability,) if capability else ()

        if self.provider_registry is not None:
            return _blocked("provider_registry_not_allowed_in_minimal_kernel", reviewed)
        if self.storage is not None:
            return _blocked("storage_not_allowed_in_minimal_kernel", reviewed)
        if self.humaninput_bridge is not None:
            return _blocked("humaninput_bridge_not_allowed_in_minimal_kernel", reviewed)
        if self.driver_registry is not None:
            return _blocked("driver_registry_not_allowed_in_minimal_kernel", reviewed)
        if _contains_authority_claim(request.normalized_intent) or _contains_authority_claim(
            request.metadata
        ):
            return _blocked("authority_claim_not_allowed", reviewed)
        if _contains_connection_discovery_claim(request.normalized_intent):
            return _blocked("connection_discovery_claim_not_allowed", reviewed)
        if not capability:
            action_category = _action_category(request)
            if action_category in SAFE_ACTION_CATEGORIES:
                return GuardianStubDecision(
                    guardian_state="proposed",
                    reason_code="text_preview_or_planning_proposed",
                    capabilities_reviewed=(),
                )
            return _blocked("unknown_action_category_blocked", ())
        if not getattr(request.capability_profile, capability):
            return _blocked(f"disabled_capability_blocked:{capability}", reviewed)
        if capability in BLOCKED_CAPABILITIES:
            return _blocked(f"dangerous_capability_blocked:{capability}", reviewed)
        if capability in APPROVAL_REQUIRED_CAPABILITIES:
            return GuardianStubDecision(
                guardian_state="approval_required",
                reason_code=f"consequential_capability_requires_approval:{capability}",
                capabilities_reviewed=reviewed,
            )
        return _blocked(f"unknown_capability_blocked:{capability}", reviewed)

    def _append_event(
        self,
        request: KernelRequest,
        event_type: str,
        decision: GuardianStubDecision,
    ) -> str:
        event_id = f"kernel-event:{len(self._events) + 1}"
        privacy_class = str(request.source_surface.get("privacy_class") or "unknown")
        event = KernelEvent(
            event_id=event_id,
            request_id=request.request_id,
            kernel_id=self.kernel_id,
            shell_id=request.shell_id,
            actor_id=request.actor_id,
            session_id=request.session_id,
            event_type=event_type,
            state=decision.guardian_state,
            reason_code=decision.reason_code,
            redacted_summary=_redacted_summary(
                request,
                decision.guardian_state,
                decision.reason_code,
            ),
            privacy_class=privacy_class,
            metadata={
                "source_surface": _safe_surface_name(request.source_surface),
                "in_memory_only": True,
            },
        )
        self._events.append(event)
        return event_id


def _coerce_request(request: KernelRequest | Mapping[str, Any]) -> KernelRequest:
    if isinstance(request, KernelRequest):
        return request
    if not isinstance(request, Mapping):
        raise TypeError("request must be KernelRequest or mapping")

    profile = request.get("capability_profile", CapabilityProfile())
    if isinstance(profile, Mapping):
        profile = CapabilityProfile(**dict(profile))
    if not isinstance(profile, CapabilityProfile):
        raise TypeError("capability_profile must be CapabilityProfile or mapping")

    return KernelRequest(
        request_id=_non_empty_text(request.get("request_id"), "request_id"),
        shell_id=_non_empty_text(request.get("shell_id"), "shell_id"),
        actor_id=_non_empty_text(request.get("actor_id"), "actor_id"),
        session_id=request.get("session_id") if isinstance(request.get("session_id"), str) else None,
        normalized_intent=_mapping(request.get("normalized_intent"), "normalized_intent"),
        capability_profile=profile,
        actor_context=_mapping(request.get("actor_context", {}), "actor_context"),
        shell_context=_mapping(request.get("shell_context", {}), "shell_context"),
        session_context=_mapping(request.get("session_context", {}), "session_context"),
        memory_refs=tuple(str(ref) for ref in request.get("memory_refs", ())),
        source_surface=_mapping(request.get("source_surface", {}), "source_surface"),
        metadata=_mapping(request.get("metadata", {}), "metadata"),
    )


def _requested_capability(request: KernelRequest) -> str | None:
    intent = request.normalized_intent
    explicit = intent.get("requested_capability") or intent.get("capability")
    if isinstance(explicit, str) and explicit.strip():
        return explicit.strip().lower()
    return ACTION_CAPABILITY_MAP.get(_action_category(request))


def _action_category(request: KernelRequest) -> str:
    value = (
        request.normalized_intent.get("action_category")
        or request.normalized_intent.get("task_type")
        or request.normalized_intent.get("intent_type")
        or request.normalized_intent.get("requested_action")
        or "unknown"
    )
    return str(value).strip().lower()


def _blocked(reason_code: str, capabilities: tuple[str, ...]) -> GuardianStubDecision:
    return GuardianStubDecision(
        guardian_state="blocked",
        reason_code=reason_code,
        capabilities_reviewed=capabilities,
    )


def _warnings(request: KernelRequest, decision: GuardianStubDecision) -> tuple[str, ...]:
    warnings: list[str] = ["dry_run_only", "no_execution_authority"]
    if decision.guardian_state == "approval_required":
        warnings.append("approval_not_enforced")
    if decision.guardian_state == "blocked":
        warnings.append("blocked_fail_closed")
    if request.memory_refs:
        warnings.append("memory_refs_reference_only")
    return tuple(warnings)


def _redacted_summary(request: KernelRequest, state: str, reason_code: str) -> str:
    category = _action_category(request)
    return f"{state}:{category}:{reason_code}"


def _safe_surface_name(surface: Mapping[str, Any]) -> str:
    value = surface.get("surface") or surface.get("source") or "unknown"
    if not isinstance(value, str) or not value.strip():
        return "unknown"
    return value.strip()[:80]


def _contains_authority_claim(value: Any) -> bool:
    if isinstance(value, Mapping):
        return any(
            _contains_authority_claim(nested_key) or _contains_authority_claim(nested_value)
            for nested_key, nested_value in value.items()
        )
    if isinstance(value, (list, tuple, set, frozenset)):
        return any(_contains_authority_claim(item) for item in value)
    if not isinstance(value, str):
        return False
    words = tuple(
        part for part in "".join(char.lower() if char.isalnum() else " " for char in value).split()
    )
    return any(marker in words for marker in AUTHORITY_CLAIM_MARKERS)


def _contains_connection_discovery_claim(value: Any) -> bool:
    if isinstance(value, Mapping):
        return any(
            _contains_connection_discovery_claim(nested_key)
            or _contains_connection_discovery_claim(nested_value)
            for nested_key, nested_value in value.items()
        )
    if isinstance(value, (list, tuple, set, frozenset)):
        return any(_contains_connection_discovery_claim(item) for item in value)
    if not isinstance(value, str):
        return False
    words = tuple(
        part for part in "".join(char.lower() if char.isalnum() else " " for char in value).split()
    )
    joined = "".join(words)
    return any(marker in words or marker == joined for marker in CONNECTION_DISCOVERY_MARKERS)


def _non_empty_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _mapping(value: Any, field_name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{field_name} must be a mapping")
    return dict(value)
