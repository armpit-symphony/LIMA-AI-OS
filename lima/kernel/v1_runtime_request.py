"""V1 typed request builder for validated non-executing candidates.

This module is the approved V1-G11 runtime slice boundary. It converts
validated candidate metadata into a typed Guardian request. It does not
parse raw natural language, approve, execute, route, persist, or call any
external system.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, Final

from lima.contracts.guardian import ConsequentialActionRequest, ConsequentialActionType

from .candidate_status import CandidateStatusError, validate_candidate


RAW_INPUT_KEYS: Final[frozenset[str]] = frozenset(
    {
        "human_input",
        "raw_human_input",
        "raw_text",
        "transcript",
        "message_text",
        "prompt",
        "raw_prompt",
        "file_contents",
    }
)
FORGED_AUTHORITY_KEYS: Final[frozenset[str]] = frozenset(
    {
        "approval",
        "approval_id",
        "approval_token",
        "approved_by",
        "decision",
        "decision_id",
        "guardian_decision",
        "guardian_decision_ref",
        "guardian_decision_status",
        "operator_pin",
        "pin",
    }
)
SAFE_ACTION_CATEGORIES: Final[frozenset[str]] = frozenset(
    {"informational", "planning", "drafting"}
)
APPROVAL_REQUIRED_ACTION_CATEGORIES: Final[frozenset[str]] = frozenset(
    {"admin", "file_mutation", "shell"}
)
FUTURE_POLICY_ACTION_CATEGORIES: Final[frozenset[str]] = frozenset(
    {"browser_network", "model_call", "robotics_physical_world", "tool_call"}
)


class V1RuntimeRequestError(ValueError):
    """Raised when candidate metadata cannot enter the V1 request slice."""


def build_v1_runtime_request(candidate: Mapping[str, Any]) -> ConsequentialActionRequest:
    """Build a non-executing Guardian request from validated candidate metadata."""

    if not isinstance(candidate, Mapping):
        raise V1RuntimeRequestError("candidate must be a mapping")

    _reject_raw_input(candidate)
    _reject_forged_authority(candidate)

    try:
        validated = validate_candidate(candidate)
    except CandidateStatusError as exc:
        raise V1RuntimeRequestError(str(exc)) from exc

    if validated.get("validation_state") != "valid":
        errors = ",".join(str(error) for error in validated.get("validation_errors", ()))
        raise V1RuntimeRequestError(f"candidate validation failed:{errors}")

    provenance = _provenance(validated)
    candidate_id = _required_text(validated.get("candidate_id"), "candidate_id")
    intake_id = _required_text(validated.get("intake_id"), "intake_id")
    actor_id = _required_text(
        validated.get("actor_id") or provenance.get("actor_id"),
        "actor_id",
    )
    shell_id = _required_text(
        validated.get("shell_id") or provenance.get("shell_id"),
        "shell_id",
    )
    action_category = _required_text(validated.get("action_category"), "action_category").lower()
    requested_action = _required_text(validated.get("requested_action"), "requested_action")
    target_ref = _optional_text(validated.get("target_ref") or provenance.get("target_ref"))
    intent_id = _optional_text(validated.get("intent_id") or provenance.get("intent_id"))
    evidence_refs = _evidence_refs(validated, provenance, candidate_id)
    request_id = _request_id(candidate_id)
    action_type = _action_type(validated, action_category)
    risk_class = _risk_class(validated, action_category)
    redacted_summary = _redacted_summary(action_category, requested_action, target_ref)

    metadata = {
        "v1_runtime_slice": "typed_request_guardian_decision_preflight",
        "candidate_id": candidate_id,
        "candidate_status": validated.get("candidate_status"),
        "approval_state": validated.get("approval_state"),
        "v1_action_category": action_category,
        "non_executing": True,
        "execution_allowed": False,
        "side_effects_allowed": False,
        "approval_token_issued": False,
        "provider_model_routing_allowed": False,
        "shell_wiring_allowed": False,
        "persistent_storage_allowed": False,
        "audit_evidence_linkage": _audit_linkage(
            request_id=request_id,
            candidate_id=candidate_id,
            input_id=intake_id,
            intent_id=intent_id,
            actor_id=actor_id,
            shell_id=shell_id,
            action_type=action_type,
            target_ref=target_ref,
            risk_class=risk_class,
            evidence_refs=evidence_refs,
            redacted_summary=redacted_summary,
        ),
    }

    return ConsequentialActionRequest(
        request_id=request_id,
        intent_id=intent_id,
        input_id=intake_id,
        actor_id=actor_id,
        shell_id=shell_id,
        action_type=action_type,
        target_ref=target_ref,
        requested_tool_pack=None,
        risk_class=risk_class,
        typed_args={
            "action_category": action_category,
            "requested_action": requested_action,
            "destructive": _is_destructive(validated, requested_action),
            "preflight_only": True,
        },
        evidence_refs=evidence_refs,
        metadata=metadata,
    )


def _reject_raw_input(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            if isinstance(key, str) and key.strip().lower() in RAW_INPUT_KEYS:
                raise V1RuntimeRequestError("raw natural-language payloads are not accepted")
            _reject_raw_input(nested)
    elif isinstance(value, (list, tuple, set, frozenset)):
        for nested in value:
            _reject_raw_input(nested)


def _reject_forged_authority(candidate: Mapping[str, Any]) -> None:
    if candidate.get("approved") is True:
        raise V1RuntimeRequestError("caller-supplied approval claims are not accepted")
    if str(candidate.get("approval_state", "")).strip().lower() == "approved":
        raise V1RuntimeRequestError("caller-supplied approved state is not accepted")
    if str(candidate.get("guardian_decision_created", "")).strip().lower() == "true":
        raise V1RuntimeRequestError("caller-supplied GuardianDecision authority is not accepted")
    _reject_forged_authority_keys(candidate)


def _reject_forged_authority_keys(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            if isinstance(key, str) and key.strip().lower() in FORGED_AUTHORITY_KEYS:
                raise V1RuntimeRequestError("caller-supplied authority metadata is not accepted")
            _reject_forged_authority_keys(nested)
    elif isinstance(value, (list, tuple, set, frozenset)):
        for nested in value:
            _reject_forged_authority_keys(nested)


def _provenance(candidate: Mapping[str, Any]) -> Mapping[str, Any]:
    provenance = candidate.get("provenance")
    if not isinstance(provenance, Mapping) or not provenance:
        raise V1RuntimeRequestError("candidate provenance is required")
    return provenance


def _request_id(candidate_id: str) -> str:
    normalized = candidate_id.replace(":", "-")
    return f"v1-request:{normalized}"


def _action_type(
    candidate: Mapping[str, Any],
    action_category: str,
) -> ConsequentialActionType:
    raw_action_type = str(
        candidate.get("consequential_action_type")
        or candidate.get("action_type")
        or ""
    ).strip()
    if raw_action_type:
        try:
            return ConsequentialActionType(raw_action_type)
        except ValueError:
            return ConsequentialActionType.UNKNOWN

    if action_category == "file_mutation":
        return ConsequentialActionType.FILE_OPERATION
    if action_category == "model_call":
        return ConsequentialActionType.MODEL_CALL
    if action_category == "tool_call":
        return ConsequentialActionType.TOOL_CALL
    if action_category == "browser_network":
        return ConsequentialActionType.BROWSER_ACTION
    if action_category == "robotics_physical_world":
        return ConsequentialActionType.ROBOT_ACTION
    if action_category == "admin":
        return ConsequentialActionType.ADMIN_ACTION
    if action_category == "shell":
        return ConsequentialActionType.TERMINAL_COMMAND
    return ConsequentialActionType.UNKNOWN


def _risk_class(candidate: Mapping[str, Any], action_category: str) -> str:
    if action_category in SAFE_ACTION_CATEGORIES:
        return "low"
    if action_category in APPROVAL_REQUIRED_ACTION_CATEGORIES:
        return "high"
    if action_category in FUTURE_POLICY_ACTION_CATEGORIES:
        return "blocked"
    return str(candidate.get("risk_tier") or "blocked").strip().lower() or "blocked"


def _evidence_refs(
    candidate: Mapping[str, Any],
    provenance: Mapping[str, Any],
    candidate_id: str,
) -> tuple[str, ...]:
    refs = candidate.get("evidence_refs") or provenance.get("evidence_refs") or ()
    if isinstance(refs, str):
        refs = (refs,)
    if not isinstance(refs, Sequence):
        refs = ()
    normalized = tuple(str(ref).strip() for ref in refs if str(ref).strip())
    return normalized or (f"candidate-ref:{candidate_id}",)


def _is_destructive(candidate: Mapping[str, Any], requested_action: str) -> bool:
    if candidate.get("destructive") is True:
        return True
    folded = requested_action.lower()
    return any(marker in folded for marker in ("delete", "edit", "mutate", "overwrite"))


def _audit_linkage(
    *,
    request_id: str,
    candidate_id: str,
    input_id: str,
    intent_id: str | None,
    actor_id: str,
    shell_id: str,
    action_type: ConsequentialActionType,
    target_ref: str | None,
    risk_class: str,
    evidence_refs: tuple[str, ...],
    redacted_summary: str,
) -> dict[str, Any]:
    return {
        "lineage_id": f"v1-lineage:{request_id}",
        "request_id": request_id,
        "candidate_id": candidate_id,
        "input_id": input_id,
        "intent_id": intent_id,
        "actor_id": actor_id,
        "shell_id": shell_id,
        "action_type": action_type.value,
        "target_ref": target_ref,
        "risk_class": risk_class,
        "evidence_refs": evidence_refs,
        "redacted_summary": redacted_summary,
        "persistent": False,
    }


def _redacted_summary(action_category: str, requested_action: str, target_ref: str | None) -> str:
    target = target_ref or "no-target"
    return f"{action_category}:{requested_action[:64]}:{target}"


def _required_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise V1RuntimeRequestError(f"{field_name} is required")
    return value.strip()


def _optional_text(value: Any) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        return None
    return value.strip()
