"""Consumer-facing request contract for the governed dry-run runtime kernel."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence


@dataclass(frozen=True)
class GovernedRequest:
    """Normalized request submitted by Sparkbot, Arc Bot, or another shell."""

    request_id: str
    consumer: str
    surface: str
    actor_id: str
    normalized_request: Any
    requested_action: str
    action_category: str
    tool_name: str | None
    tool_args: Mapping[str, Any] = field(default_factory=dict)
    trust_context: Mapping[str, Any] = field(default_factory=dict)
    evidence_refs: Sequence[str] = field(default_factory=tuple)

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "GovernedRequest":
        return cls(
            request_id=_required_text(value.get("request_id"), "request_id"),
            consumer=_required_text(value.get("consumer"), "consumer"),
            surface=_required_text(value.get("surface"), "surface"),
            actor_id=_required_text(value.get("actor_id"), "actor_id"),
            normalized_request=value.get("normalized_request"),
            requested_action=_required_text(value.get("requested_action"), "requested_action"),
            action_category=_required_text(value.get("action_category"), "action_category"),
            tool_name=_optional_text(value.get("tool_name")),
            tool_args=_mapping(value.get("tool_args"), "tool_args"),
            trust_context=_mapping(value.get("trust_context"), "trust_context"),
            evidence_refs=_text_sequence(value.get("evidence_refs"), "evidence_refs"),
        )

    def validate(self) -> None:
        _required_text(self.request_id, "request_id")
        _required_text(self.consumer, "consumer")
        _required_text(self.surface, "surface")
        _required_text(self.actor_id, "actor_id")
        _required_text(self.requested_action, "requested_action")
        _required_text(self.action_category, "action_category")
        if self.normalized_request is None:
            raise ValueError("normalized_request is required")
        _mapping(self.tool_args, "tool_args")
        _mapping(self.trust_context, "trust_context")
        _text_sequence(self.evidence_refs, "evidence_refs")

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "consumer": self.consumer,
            "surface": self.surface,
            "actor_id": self.actor_id,
            "normalized_request": self.normalized_request,
            "requested_action": self.requested_action,
            "action_category": self.action_category,
            "tool_name": self.tool_name,
            "tool_args": dict(self.tool_args),
            "trust_context": dict(self.trust_context),
            "evidence_refs": tuple(self.evidence_refs),
        }


def _required_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} is required")
    return value.strip()


def _optional_text(value: Any) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError("tool_name must be text or None")
    normalized = value.strip()
    return normalized or None


def _mapping(value: Any, field_name: str) -> Mapping[str, Any]:
    if value is None:
        return {}
    if not isinstance(value, Mapping):
        raise ValueError(f"{field_name} must be a mapping")
    return dict(value)


def _text_sequence(value: Any, field_name: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value.strip(),) if value.strip() else ()
    if not isinstance(value, Sequence):
        raise ValueError(f"{field_name} must be a sequence")
    return tuple(str(item).strip() for item in value if str(item).strip())
