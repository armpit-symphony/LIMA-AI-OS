"""Non-authoritative Guardian lifecycle preview objects for LIMA Kernel."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Final, Mapping

from .plugin_contract import CapabilityProfile, KernelRequest


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
    {
        "process_execute",
        "device_control",
        "robotics_actuation",
        "drone_actuation",
        "connection_attempt",
        "device_pairing",
        "credential_use",
        "iot_control",
        "physical_world_actuation",
        "robotics_endpoint_discovery",
        "drone_endpoint_discovery",
    }
)
ACTION_CAPABILITY_MAP: Final[dict[str, str]] = {
    "model_call": "model_calls",
    "memory_write": "memory_write",
    "task_state_write": "task_state_write",
    "connector_read": "connector_read",
    "connector_write": "connector_write",
    "external_send": "external_send",
    "file_write": "file_write",
    "process_execute": "process_execute",
    "terminal_command": "process_execute",
    "browser_control": "browser_control",
    "device_control": "device_control",
    "robotics_actuation": "robotics_actuation",
    "drone_actuation": "drone_actuation",
    "scheduler_run": "scheduler_run",
    "connection_attempt": "connection_attempt",
    "device_pairing": "device_pairing",
    "credential_use": "credential_use",
    "iot_control": "iot_control",
    "physical_world_actuation": "physical_world_actuation",
}
AUTHORITY_MARKERS: Final[frozenset[str]] = frozenset(
    {
        "approve",
        "approved",
        "approval",
        "authorize",
        "authorized",
        "bypass",
        "override",
        "dispatch",
        "execute",
        "grant",
        "trusted",
    }
)
RAW_INPUT_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "raw_text",
        "raw_prompt",
        "raw_chat",
        "chat_text",
        "raw_message",
        "raw_office_task",
        "office_task_text",
        "customer_record",
        "provider_payload",
        "tool_arguments",
        "connector_record",
    }
)
STRUCTURED_ACTION_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "action_category",
        "capability",
        "intent_type",
        "requested_action",
        "requested_capability",
        "task_type",
    }
)
AUTHORITY_CLAIM_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "allowed_tool_packs",
        "approval_granted",
        "approved",
        "authority_created",
        "decision_ref",
        "dispatch_allowed",
        "execution_allowed",
        "guardian_decision_created",
        "policy_enforced",
        "tool_packs_granted",
    }
)
FORBIDDEN_EVENT_MARKERS: Final[frozenset[str]] = frozenset(
    {
        "credential",
        "header",
        "password",
        "pairing",
        "secret",
        "token",
    }
)


@dataclass(frozen=True)
class IntentEnvelopeCandidatePreview:
    """Structured intent preview that grants no runtime authority."""

    intent_id: str
    request_id: str
    actor_id: str
    shell_id: str
    session_id: str | None
    state: str
    action_category: str
    risk_class: str
    requested_capability: str | None
    requested_tool_packs: tuple[str, ...] = ()
    redacted_summary: str = ""
    evidence_refs: tuple[str, ...] = ()
    authority_created: bool = False
    executable: bool = False
    dispatch_allowed: bool = False
    persistence_allowed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class GuardianRequestPreview:
    """Guardian request-shaped preview that is not a GuardianDecision."""

    guardian_request_id: str
    intent_id: str
    request_id: str
    actor_id: str
    shell_id: str
    session_id: str | None
    state: str
    action_type: str
    risk_class: str
    requested_capability: str | None
    reason_code: str
    requested_tool_packs: tuple[str, ...] = ()
    allowed_tool_packs: tuple[str, ...] = ()
    decision_ref: None = None
    approval_ref: None = None
    dry_run: bool = True
    non_authoritative: bool = True
    guardian_decision_created: bool = False
    approval_enforced: bool = False
    execution_allowed: bool = False
    dispatch_allowed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class GuardianLifecyclePreviewEvent:
    """Redacted in-memory lifecycle preview event."""

    event_id: str
    request_id: str
    event_type: str
    state: str
    reason_code: str
    redacted_summary: str
    durable: bool = False
    in_memory_only: bool = True
    contains_secret: bool = False
    contains_raw_prompt: bool = False
    contains_unsafe_payload: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class GuardianLifecyclePreviewResult:
    """Dry-run lifecycle preview result with no decision authority."""

    request_id: str
    kernel_id: str
    state: str
    reason_code: str
    intent_candidate: IntentEnvelopeCandidatePreview
    guardian_request: GuardianRequestPreview
    event_refs: tuple[str, ...]
    events: tuple[GuardianLifecyclePreviewEvent, ...]
    warnings: tuple[str, ...] = ()
    dry_run: bool = True
    executable: bool = False
    execution_allowed: bool = False
    side_effects_allowed: bool = False
    dispatch_allowed: bool = False
    persistence_allowed: bool = False
    model_calls_allowed: bool = False
    model_calls_executed: bool = False
    guardian_decision_created: bool = False
    approval_enforced: bool = False
    approval_metadata_recorded: bool = False
    tool_execution_allowed: bool = False
    connector_access_allowed: bool = False
    storage_persistence_allowed: bool = False
    event_spine_persistence_allowed: bool = False
    humaninput_bridge_active: bool = False
    sparkbot_wiring_active: bool = False
    arc_bot_wiring_active: bool = False
    robo_os_wiring_active: bool = False
    live_discovery_executed: bool = False
    connection_attempted: bool = False
    pairing_attempted: bool = False
    credentials_used: bool = False
    session_opened: bool = False
    device_control_executed: bool = False
    physical_world_allowed: bool = False
    physical_world_executed: bool = False
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["intent_candidate"] = self.intent_candidate.to_dict()
        result["guardian_request"] = self.guardian_request.to_dict()
        result["events"] = tuple(event.to_dict() for event in self.events)
        return result


def preview_guardian_lifecycle(
    request: KernelRequest | Mapping[str, Any],
    *,
    kernel_id: str = "lima-minimal-kernel",
    runtime_dependencies_present: Mapping[str, bool] | None = None,
) -> GuardianLifecyclePreviewResult:
    """Build a fail-closed, non-authoritative Guardian lifecycle preview."""

    kernel_request = _coerce_request(request)
    blocked_reason = _blocked_reason(kernel_request, runtime_dependencies_present or {})
    action_category = _action_category(kernel_request)
    risk_class = _risk_class(kernel_request)
    capability = _requested_capability(kernel_request)
    requested_tool_packs = _requested_tool_packs(kernel_request)

    if blocked_reason:
        state = "blocked"
        candidate_state = "blocked_before_guardian"
        guardian_request_state = "blocked_before_decision"
        reason_code = blocked_reason
    elif capability in APPROVAL_REQUIRED_CAPABILITIES:
        state = "approval_required"
        candidate_state = "ready_for_guardian_request"
        guardian_request_state = "ready_for_policy_review"
        reason_code = f"guardian_lifecycle_requires_future_decision:{capability}"
    elif action_category in SAFE_ACTION_CATEGORIES:
        state = "proposed"
        candidate_state = "ready_for_guardian_request"
        guardian_request_state = "ready_for_policy_review"
        reason_code = "guardian_lifecycle_preview_proposed"
    else:
        state = "blocked"
        candidate_state = "blocked_before_guardian"
        guardian_request_state = "blocked_before_decision"
        reason_code = "unknown_action_category_blocked"

    intent_id = f"intent-preview:{kernel_request.request_id}"
    guardian_request_id = f"guardian-request-preview:{kernel_request.request_id}"
    redacted_summary = _redacted_summary(state, action_category, reason_code)
    candidate = IntentEnvelopeCandidatePreview(
        intent_id=intent_id,
        request_id=kernel_request.request_id,
        actor_id=kernel_request.actor_id,
        shell_id=kernel_request.shell_id,
        session_id=kernel_request.session_id,
        state=candidate_state,
        action_category=action_category,
        risk_class=risk_class,
        requested_capability=capability,
        requested_tool_packs=requested_tool_packs,
        redacted_summary=redacted_summary,
        evidence_refs=_safe_refs(kernel_request.metadata.get("evidence_refs", ())),
    )
    guardian_request = GuardianRequestPreview(
        guardian_request_id=guardian_request_id,
        intent_id=intent_id,
        request_id=kernel_request.request_id,
        actor_id=kernel_request.actor_id,
        shell_id=kernel_request.shell_id,
        session_id=kernel_request.session_id,
        state=guardian_request_state,
        action_type=action_category,
        risk_class=risk_class,
        requested_capability=capability,
        reason_code=reason_code,
        requested_tool_packs=requested_tool_packs,
    )
    events = _events(kernel_request.request_id, state, reason_code, redacted_summary)
    return GuardianLifecyclePreviewResult(
        request_id=kernel_request.request_id,
        kernel_id=kernel_id,
        state=state,
        reason_code=reason_code,
        intent_candidate=candidate,
        guardian_request=guardian_request,
        event_refs=tuple(event.event_id for event in events),
        events=events,
        warnings=_warnings(state),
        metadata={
            "non_authoritative_lifecycle_preview": True,
            "guardian_request_is_not_decision": True,
            "intent_candidate_is_not_authority": True,
            "no_guardian_decision_created": True,
            "no_approval_enforcement": True,
            "no_dispatch": True,
        },
    )


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


def _blocked_reason(
    request: KernelRequest,
    runtime_dependencies_present: Mapping[str, bool],
) -> str | None:
    for dependency_name, present in sorted(runtime_dependencies_present.items()):
        if present:
            return f"runtime_dependency_not_allowed:{dependency_name}"
    if _contains_raw_input(request.normalized_intent) or _contains_raw_input(request.metadata):
        return "raw_executable_input_not_allowed"
    if _contains_authority_claim(request.normalized_intent) or _contains_authority_claim(
        request.metadata
    ):
        return "authority_claim_not_allowed"
    if _unsafe_source_surface(request.source_surface):
        return "unsafe_source_surface_blocked"
    requested_tool_packs = _requested_tool_packs(request)
    if requested_tool_packs and not set(requested_tool_packs).issubset(
        set(request.capability_profile.allowed_tool_packs)
    ):
        return "requested_tool_pack_not_allowed"
    capability = _requested_capability(request)
    if capability and not getattr(request.capability_profile, capability, False):
        return f"disabled_capability_blocked:{capability}"
    if capability in BLOCKED_CAPABILITIES:
        return f"dangerous_capability_blocked:{capability}"
    if _risk_class(request) == "unknown" and _action_category(request) not in SAFE_ACTION_CATEGORIES:
        return "unknown_risk_class_blocked"
    return None


def _requested_capability(request: KernelRequest) -> str | None:
    explicit = request.normalized_intent.get("requested_capability") or request.normalized_intent.get(
        "capability"
    )
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


def _risk_class(request: KernelRequest) -> str:
    value = request.normalized_intent.get("risk_class") or "unknown"
    return str(value).strip().lower()


def _requested_tool_packs(request: KernelRequest) -> tuple[str, ...]:
    value = request.normalized_intent.get("requested_tool_packs", ())
    if isinstance(value, str):
        return (value.strip().lower(),) if value.strip() else ()
    if isinstance(value, (list, tuple, set, frozenset)):
        return tuple(str(item).strip().lower() for item in value if str(item).strip())
    return ()


def _safe_refs(value: Any) -> tuple[str, ...]:
    if isinstance(value, str):
        refs = (value,)
    elif isinstance(value, (list, tuple, set, frozenset)):
        refs = tuple(str(item) for item in value)
    else:
        return ()
    return tuple(ref[:80] for ref in refs if ref.strip() and not _contains_forbidden_event_marker(ref))


def _events(
    request_id: str,
    state: str,
    reason_code: str,
    redacted_summary: str,
) -> tuple[GuardianLifecyclePreviewEvent, ...]:
    return (
        GuardianLifecyclePreviewEvent(
            event_id="guardian-lifecycle-preview-event:1",
            request_id=request_id,
            event_type="guardian_lifecycle_preview_requested",
            state=state,
            reason_code=reason_code,
            redacted_summary=redacted_summary,
        ),
        GuardianLifecyclePreviewEvent(
            event_id="guardian-lifecycle-preview-event:2",
            request_id=request_id,
            event_type=f"guardian_lifecycle_preview_{state}",
            state=state,
            reason_code=reason_code,
            redacted_summary=redacted_summary,
        ),
    )


def _warnings(state: str) -> tuple[str, ...]:
    warnings = ["dry_run_only", "non_authoritative", "no_guardian_decision_created"]
    if state == "approval_required":
        warnings.append("approval_not_enforced")
    if state == "blocked":
        warnings.append("blocked_fail_closed")
    return tuple(warnings)


def _redacted_summary(state: str, action_category: str, reason_code: str) -> str:
    return f"{state}:{action_category}:{reason_code}"


def _unsafe_source_surface(source_surface: Mapping[str, Any]) -> bool:
    return any(
        source_surface.get(field_name) is True
        for field_name in ("contains_secret", "contains_raw_prompt", "contains_unsafe_payload")
    )


def _contains_raw_input(value: Any) -> bool:
    if isinstance(value, Mapping):
        return any(
            (
                isinstance(nested_key, str)
                and nested_key.strip().lower() in RAW_INPUT_FIELDS
                and bool(nested_value)
            )
            or _contains_raw_input(nested_value)
            for nested_key, nested_value in value.items()
        )
    if isinstance(value, (list, tuple, set, frozenset)):
        return any(_contains_raw_input(item) for item in value)
    return False


def _contains_authority_claim(value: Any) -> bool:
    if isinstance(value, Mapping):
        for nested_key, nested_value in value.items():
            key = str(nested_key).strip().lower()
            if key in AUTHORITY_CLAIM_FIELDS:
                return True
            if key in STRUCTURED_ACTION_FIELDS:
                continue
            if _contains_marker(nested_key, AUTHORITY_MARKERS) or _contains_authority_claim(
                nested_value
            ):
                return True
        return False
    if isinstance(value, (list, tuple, set, frozenset)):
        return any(_contains_authority_claim(item) for item in value)
    return _contains_marker(value, AUTHORITY_MARKERS)


def _contains_forbidden_event_marker(value: Any) -> bool:
    return _contains_marker(value, FORBIDDEN_EVENT_MARKERS)


def _contains_marker(value: Any, markers: frozenset[str]) -> bool:
    if isinstance(value, Mapping):
        return any(
            _contains_marker(nested_key, markers) or _contains_marker(nested_value, markers)
            for nested_key, nested_value in value.items()
        )
    if isinstance(value, (list, tuple, set, frozenset)):
        return any(_contains_marker(item, markers) for item in value)
    if not isinstance(value, str):
        return False
    words = tuple(
        part for part in "".join(char.lower() if char.isalnum() else " " for char in value).split()
    )
    joined = "".join(words)
    return any(marker in words or marker == joined for marker in markers)


def _non_empty_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _mapping(value: Any, field_name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{field_name} must be a mapping")
    return dict(value)
