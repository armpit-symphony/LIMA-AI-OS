"""Non-authoritative Guardian decision authority preview for LIMA Kernel."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Final, Mapping

from .guardian_lifecycle import (
    ACTION_CAPABILITY_MAP,
    APPROVAL_REQUIRED_CAPABILITIES,
    BLOCKED_CAPABILITIES,
    SAFE_ACTION_CATEGORIES,
)
from .plugin_contract import CapabilityProfile, KernelRequest


ELIGIBLE_DECISION_STATUSES: Final[frozenset[str]] = frozenset({"approved"})
BLOCKING_DECISION_STATUSES: Final[frozenset[str]] = frozenset(
    {"denied", "blocked", "expired", "revoked", "superseded", "escalated"}
)
REVIEW_DECISION_STATUSES: Final[frozenset[str]] = frozenset(
    {
        "needs_clarification",
        "needs_human_confirmation",
        "needs_operator_pin",
        "needs_breakglass",
    }
)
KNOWN_DECISION_STATUSES: Final[frozenset[str]] = (
    ELIGIBLE_DECISION_STATUSES | BLOCKING_DECISION_STATUSES | REVIEW_DECISION_STATUSES
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
EXECUTION_SEEKING_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "connect",
        "connection_attempt",
        "dispatch",
        "execute",
        "execution_requested",
        "external_send",
        "file_write",
        "mutate",
        "pair",
        "persist",
        "scan",
        "send",
        "session_open",
    }
)
FORBIDDEN_EVENT_MARKERS: Final[frozenset[str]] = frozenset(
    {
        "apikey",
        "credential",
        "header",
        "password",
        "pairing",
        "secret",
        "token",
    }
)


@dataclass(frozen=True)
class GuardianDecisionAuthorityPreview:
    """Decision-authority requirement metadata that grants no authority."""

    authority_preview_id: str
    request_id: str
    actor_id: str
    shell_id: str
    session_id: str | None
    action_category: str
    requested_capability: str | None
    state: str
    reason_code: str
    decision_required: bool
    existing_decision_status: str | None = None
    status_reviewed: bool = False
    scope_reviewed: bool = False
    approval_reviewed: bool = False
    decision_authority_created: bool = False
    guardian_decision_created: bool = False
    approval_enforced: bool = False
    execution_allowed: bool = False
    dispatch_allowed: bool = False
    persistence_allowed: bool = False
    redacted_summary: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class GuardianDecisionAuthorityPreviewEvent:
    """Redacted in-memory decision authority preview event."""

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
class GuardianDecisionAuthorityPreviewResult:
    """Dry-run result for future GuardianDecision authority requirements."""

    request_id: str
    kernel_id: str
    state: str
    reason_code: str
    authority_preview: GuardianDecisionAuthorityPreview
    event_refs: tuple[str, ...]
    events: tuple[GuardianDecisionAuthorityPreviewEvent, ...]
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
    decision_authority_created: bool = False
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
        result["authority_preview"] = self.authority_preview.to_dict()
        result["events"] = tuple(event.to_dict() for event in self.events)
        return result


def preview_guardian_decision_authority(
    request: KernelRequest | Mapping[str, Any],
    *,
    kernel_id: str = "lima-minimal-kernel",
    runtime_dependencies_present: Mapping[str, bool] | None = None,
) -> GuardianDecisionAuthorityPreviewResult:
    """Classify future decision authority needs without creating authority."""

    kernel_request = _coerce_request(request)
    runtime_dependency = _runtime_dependency_blocker(runtime_dependencies_present or {})
    action_category = _action_category(kernel_request)
    capability = _requested_capability(kernel_request)
    existing_decision = _existing_decision_metadata(kernel_request)

    if runtime_dependency:
        state = "blocked"
        reason_code = runtime_dependency
        decision_required = False
    else:
        state, reason_code, decision_required = _classify_authority_need(
            kernel_request,
            action_category,
            capability,
            existing_decision,
        )

    redacted_summary = _redacted_summary(state, action_category, reason_code)
    authority_preview = GuardianDecisionAuthorityPreview(
        authority_preview_id=f"guardian-decision-authority-preview:{kernel_request.request_id}",
        request_id=kernel_request.request_id,
        actor_id=kernel_request.actor_id,
        shell_id=kernel_request.shell_id,
        session_id=kernel_request.session_id,
        action_category=action_category,
        requested_capability=capability,
        state=state,
        reason_code=reason_code,
        decision_required=decision_required,
        existing_decision_status=_decision_status(existing_decision),
        status_reviewed=existing_decision is not None,
        scope_reviewed=existing_decision is not None,
        approval_reviewed=existing_decision is not None,
        redacted_summary=redacted_summary,
    )
    events = _events(kernel_request.request_id, state, reason_code, redacted_summary)
    return GuardianDecisionAuthorityPreviewResult(
        request_id=kernel_request.request_id,
        kernel_id=kernel_id,
        state=state,
        reason_code=reason_code,
        authority_preview=authority_preview,
        event_refs=tuple(event.event_id for event in events),
        events=events,
        warnings=_warnings(state, decision_required),
        metadata={
            "non_authoritative_decision_authority_preview": True,
            "decision_required": decision_required,
            "no_guardian_decision_created": True,
            "no_approval_enforcement": True,
            "no_dispatch": True,
            "no_persistence": True,
        },
    )


def _classify_authority_need(
    request: KernelRequest,
    action_category: str,
    capability: str | None,
    existing_decision: Mapping[str, Any] | None,
) -> tuple[str, str, bool]:
    blocked_reason = _input_blocker(request, action_category, capability)
    if blocked_reason:
        return "blocked", blocked_reason, False

    if existing_decision is not None:
        decision_blocker = _decision_blocker(request, action_category, capability, existing_decision)
        if decision_blocker:
            return "blocked", decision_blocker, True
        return "authority_required", "guardian_decision_required_not_created", True

    if _execution_seeking(request):
        return "blocked", "guardian_decision_absent_for_execution", True
    if capability in APPROVAL_REQUIRED_CAPABILITIES:
        return "authority_required", f"guardian_decision_required:{capability}", True
    if action_category in SAFE_ACTION_CATEGORIES:
        return "authority_not_required", "guardian_decision_not_required_for_text_preview", False
    return "blocked", "unknown_action_category_blocked", False


def _input_blocker(
    request: KernelRequest,
    action_category: str,
    capability: str | None,
) -> str | None:
    if _contains_raw_input(request.normalized_intent) or _contains_raw_input(request.metadata):
        return "raw_executable_input_not_allowed"
    if _contains_authority_claim(request.normalized_intent) or _contains_authority_claim(
        request.metadata
    ):
        return "decision_authority_claim_not_allowed"
    if _unsafe_source_surface(request.source_surface):
        return "unsafe_source_surface_blocked"
    if capability and not getattr(request.capability_profile, capability, False):
        return f"disabled_capability_blocked:{capability}"
    if capability in BLOCKED_CAPABILITIES:
        return f"dangerous_capability_blocked:{capability}"
    if capability is None and action_category not in SAFE_ACTION_CATEGORIES:
        return None
    return None


def _decision_blocker(
    request: KernelRequest,
    action_category: str,
    capability: str | None,
    decision: Mapping[str, Any],
) -> str | None:
    status = _decision_status(decision)
    if status is None or status not in KNOWN_DECISION_STATUSES:
        return "unknown_guardian_decision_status_blocked"
    if status in BLOCKING_DECISION_STATUSES:
        return f"guardian_decision_status_blocked:{status}"
    if status in REVIEW_DECISION_STATUSES:
        return f"guardian_decision_review_state_not_authority:{status}"
    if decision.get("expired") is True:
        return "guardian_decision_expired_blocked"
    if decision.get("revoked") is True:
        return "guardian_decision_revoked_blocked"
    if decision.get("superseded") is True:
        return "guardian_decision_superseded_blocked"
    if _decision_value(decision, "actor_id") not in {None, request.actor_id}:
        return "guardian_decision_scope_mismatch:actor_id"
    if _decision_value(decision, "shell_id") not in {None, request.shell_id}:
        return "guardian_decision_scope_mismatch:shell_id"
    if _decision_value(decision, "session_id") not in {None, request.session_id}:
        return "guardian_decision_scope_mismatch:session_id"
    if _decision_value(decision, "action_category") not in {None, action_category}:
        return "guardian_decision_scope_mismatch:action_category"
    if _decision_value(decision, "requested_capability") not in {None, capability}:
        return "guardian_decision_scope_mismatch:requested_capability"
    if _approval_required(decision) and not _decision_value(decision, "approval_ref"):
        return "approval_required_but_missing"
    return None


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


def _runtime_dependency_blocker(runtime_dependencies_present: Mapping[str, bool]) -> str | None:
    for dependency_name, present in sorted(runtime_dependencies_present.items()):
        if present:
            return f"runtime_dependency_not_allowed:{dependency_name}"
    return None


def _existing_decision_metadata(request: KernelRequest) -> Mapping[str, Any] | None:
    value = request.metadata.get("guardian_decision_preview")
    if isinstance(value, Mapping):
        return dict(value)
    value = request.normalized_intent.get("guardian_decision_preview")
    if isinstance(value, Mapping):
        return dict(value)
    return None


def _decision_status(decision: Mapping[str, Any] | None) -> str | None:
    if decision is None:
        return None
    value = decision.get("decision_status") or decision.get("status")
    if not isinstance(value, str) or not value.strip():
        return None
    return value.strip().lower()


def _decision_value(decision: Mapping[str, Any], field_name: str) -> str | None:
    value = decision.get(field_name)
    if not isinstance(value, str) or not value.strip():
        return None
    return value.strip().lower()


def _approval_required(decision: Mapping[str, Any]) -> bool:
    value = decision.get("approval_required") or decision.get("approval_requirement")
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() not in {"", "none", "not_required", "false"}
    return False


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


def _events(
    request_id: str,
    state: str,
    reason_code: str,
    redacted_summary: str,
) -> tuple[GuardianDecisionAuthorityPreviewEvent, ...]:
    return (
        GuardianDecisionAuthorityPreviewEvent(
            event_id="guardian-decision-authority-preview-event:1",
            request_id=request_id,
            event_type="guardian_decision_authority_preview_requested",
            state=state,
            reason_code=reason_code,
            redacted_summary=redacted_summary,
        ),
        GuardianDecisionAuthorityPreviewEvent(
            event_id="guardian-decision-authority-preview-event:2",
            request_id=request_id,
            event_type=f"guardian_decision_authority_preview_{state}",
            state=state,
            reason_code=reason_code,
            redacted_summary=redacted_summary,
        ),
    )


def _warnings(state: str, decision_required: bool) -> tuple[str, ...]:
    warnings = ["dry_run_only", "non_authoritative", "no_guardian_decision_created"]
    if decision_required:
        warnings.append("decision_required_not_created")
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


def _execution_seeking(request: KernelRequest) -> bool:
    return _contains_marker(request.normalized_intent, EXECUTION_SEEKING_FIELDS) or _contains_marker(
        request.metadata,
        EXECUTION_SEEKING_FIELDS,
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
        return any(
            (
                isinstance(nested_key, str)
                and nested_key.strip().lower() in AUTHORITY_CLAIM_FIELDS
                and bool(nested_value)
            )
            or _contains_authority_claim(nested_value)
            for nested_key, nested_value in value.items()
        )
    if isinstance(value, (list, tuple, set, frozenset)):
        return any(_contains_authority_claim(item) for item in value)
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
