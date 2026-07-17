"""V1 guarded file mutation policy contract.

This module is the approved V1-G16 candidate contract slice. It validates
policy metadata for guarded file edit/delete/file-mutation requests without
reading user files, writing files, deleting files, applying patches, routing
providers, wiring shells, invoking connectors, or performing external actions.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import hashlib
import json
from typing import Any, Final


SCHEMA_VERSION: Final[str] = "v1-g16-candidate"
ALLOWED_REQUEST_TYPES: Final[frozenset[str]] = frozenset(
    {"file_edit", "file_delete", "file_mutation"}
)
ALLOWED_MUTATION_KINDS: Final[frozenset[str]] = frozenset(
    {"destructive_edit", "destructive_delete", "destructive_file_mutation"}
)
REQUIRED_TOP_LEVEL_FIELDS: Final[tuple[str, ...]] = (
    "request_classification",
    "mutation_intent_scope",
    "workspace_root_boundary",
    "target_path_expectations",
    "shell_harness_file_authority",
    "operator_approval_evidence_requirements",
    "dry_run_preview_requirement",
    "diff_patch_preview_expectation",
    "rollback_expectation",
    "destructive_delete_confirmation_expectation",
    "audit_evidence_linkage",
    "tenant_scope",
    "shell_scope",
    "actor_scope",
    "session_scope",
)
RAW_SENSITIVE_KEYS: Final[frozenset[str]] = frozenset(
    {
        "api_key",
        "approval_pin",
        "approval_token",
        "content",
        "customer_data",
        "diff_contents",
        "file_content",
        "file_contents",
        "message_text",
        "operator_pin",
        "password",
        "patch_contents",
        "pin",
        "prompt",
        "provider_credentials",
        "raw_approval_pin",
        "raw_approval_token",
        "raw_customer_data",
        "raw_diff",
        "raw_file_content",
        "raw_file_contents",
        "raw_human_input",
        "raw_patch",
        "raw_prompt",
        "raw_secret",
        "raw_text",
        "secret",
        "secret_value",
        "token",
        "transcript",
    }
)
RAW_SENSITIVE_VALUE_MARKERS: Final[tuple[str, ...]] = (
    "raw-secret-",
    "raw secret",
    "approval-pin",
    "approval token",
    "raw prompt",
    "raw file contents",
    "raw file content",
    "raw diff",
    "raw patch",
    "raw customer data",
    "provider credential",
)
FORBIDDEN_TRUE_CLAIM_KEYS: Final[frozenset[str]] = frozenset(
    {
        "actual_file_mutation_execution_added",
        "approval_token_issued",
        "browser_action_executed",
        "connector_invoked",
        "consumer_integration_added",
        "delete_executed",
        "device_command_invoked",
        "execution_allowed",
        "external_send_added",
        "file_deleted",
        "file_mutated",
        "file_mutation_executed",
        "file_overwritten",
        "final_api_freeze_approved",
        "humaninput_bridge_activated",
        "model_routed",
        "mutation_executed",
        "network_action_executed",
        "patch_applied",
        "physical_world_invoked",
        "product_ready",
        "provider_model_routed",
        "robotics_invoked",
        "shell_wired",
        "side_effects_allowed",
        "tool_executed",
        "user_file_read",
        "write_executed",
    }
)


class V1FileMutationPolicyError(ValueError):
    """Raised when guarded file mutation policy metadata fails closed."""


def validate_v1_guarded_file_mutation_policy(
    policy_metadata: Mapping[str, Any],
) -> dict[str, Any]:
    """Return a deterministic non-executing guarded file mutation policy record."""

    if not isinstance(policy_metadata, Mapping):
        raise V1FileMutationPolicyError("policy_metadata must be a mapping")

    _reject_raw_sensitive_content(policy_metadata)
    _reject_runtime_authority_claims(policy_metadata)

    for field_name in REQUIRED_TOP_LEVEL_FIELDS:
        if field_name not in policy_metadata:
            raise V1FileMutationPolicyError(f"{field_name} is required")

    classification = _mapping(
        policy_metadata.get("request_classification"),
        "request_classification",
    )
    intent_scope = _mapping(
        policy_metadata.get("mutation_intent_scope"),
        "mutation_intent_scope",
    )
    workspace_boundary = _mapping(
        policy_metadata.get("workspace_root_boundary"),
        "workspace_root_boundary",
    )
    path_expectations = _mapping(
        policy_metadata.get("target_path_expectations"),
        "target_path_expectations",
    )
    shell_authority = _mapping(
        policy_metadata.get("shell_harness_file_authority"),
        "shell_harness_file_authority",
    )
    approval_requirements = _mapping(
        policy_metadata.get("operator_approval_evidence_requirements"),
        "operator_approval_evidence_requirements",
    )
    dry_run_preview = _mapping(
        policy_metadata.get("dry_run_preview_requirement"),
        "dry_run_preview_requirement",
    )
    diff_preview = _mapping(
        policy_metadata.get("diff_patch_preview_expectation"),
        "diff_patch_preview_expectation",
    )
    rollback = _mapping(policy_metadata.get("rollback_expectation"), "rollback_expectation")
    delete_confirmation = _mapping(
        policy_metadata.get("destructive_delete_confirmation_expectation"),
        "destructive_delete_confirmation_expectation",
    )
    audit_linkage = _mapping(
        policy_metadata.get("audit_evidence_linkage"),
        "audit_evidence_linkage",
    )
    tenant_scope = _required_text(policy_metadata.get("tenant_scope"), "tenant_scope")
    shell_scope = _required_text(policy_metadata.get("shell_scope"), "shell_scope")
    actor_scope = _required_text(policy_metadata.get("actor_scope"), "actor_scope")
    session_scope = _required_text(policy_metadata.get("session_scope"), "session_scope")

    request_type, mutation_kind = _validate_classification(classification)
    normalized_target_path = _validate_intent_scope(intent_scope)
    _validate_workspace_boundary(workspace_boundary)
    _validate_path_expectations(
        path_expectations,
        normalized_target_path,
        intent_scope,
    )
    _validate_shell_authority(shell_authority)
    _validate_approval_requirements(approval_requirements)
    _validate_preview_expectations(dry_run_preview, diff_preview)
    _validate_rollback(rollback)
    _validate_delete_confirmation(delete_confirmation, request_type)
    evidence_refs = _validate_audit_linkage(audit_linkage)

    record = {
        "record_type": "v1_guarded_file_mutation_policy",
        "schema_version": SCHEMA_VERSION,
        "request_type": request_type,
        "mutation_kind": mutation_kind,
        "normalized_target_path": normalized_target_path,
        "tenant_scope": tenant_scope,
        "shell_scope": shell_scope,
        "actor_scope": actor_scope,
        "session_scope": session_scope,
        "request_classification": _json_ready(classification),
        "mutation_intent_scope": _json_ready(intent_scope),
        "workspace_root_boundary": _json_ready(workspace_boundary),
        "target_path_expectations": _json_ready(path_expectations),
        "shell_harness_file_authority": _json_ready(shell_authority),
        "operator_approval_evidence_requirements": _json_ready(approval_requirements),
        "dry_run_preview_requirement": _json_ready(dry_run_preview),
        "diff_patch_preview_expectation": _json_ready(diff_preview),
        "rollback_expectation": _json_ready(rollback),
        "destructive_delete_confirmation_expectation": _json_ready(delete_confirmation),
        "audit_evidence_linkage": _json_ready(audit_linkage),
        "evidence_refs": list(evidence_refs),
        "capability_open": True,
        "authority_gated": True,
        "policy_authority_contract": True,
        "preview_dry_run_behavior_implemented": False,
        "actual_file_mutation_execution_approved": False,
        "execution_allowed": False,
        "side_effects_allowed": False,
        "mutation_without_approval_allowed": False,
        "mutation_outside_approved_scope_allowed": False,
        "file_mutation_executed": False,
        "file_deleted": False,
        "file_overwritten": False,
        "patch_applied": False,
        "user_file_read": False,
        "approval_token_issued": False,
        "raw_file_content_persisted": False,
        "consumer_integration_added": False,
        "provider_model_routed": False,
        "connector_invoked": False,
        "browser_action_executed": False,
        "network_action_executed": False,
        "physical_world_invoked": False,
        "final_api_freeze_approved": False,
        "product_ready": False,
        "metadata": {
            "v1_runtime_slice": "guarded_file_mutation_policy_contract",
            "candidate_only": True,
            "non_executing": True,
            "proof_not_authority": True,
        },
    }
    record["record_hash"] = _record_hash(record)
    return record


def _validate_classification(classification: Mapping[str, Any]) -> tuple[str, str]:
    request_type = _required_text(
        classification.get("request_type"),
        "request_classification.request_type",
    ).lower()
    if request_type not in ALLOWED_REQUEST_TYPES:
        raise V1FileMutationPolicyError("request classification is not allowed")

    mutation_kind = _required_text(
        classification.get("mutation_kind"),
        "request_classification.mutation_kind",
    ).lower()
    if mutation_kind not in ALLOWED_MUTATION_KINDS:
        raise V1FileMutationPolicyError("mutation classification is not allowed")
    if classification.get("destructive_mutation") is not True:
        raise V1FileMutationPolicyError("destructive mutation classification is required")
    if classification.get("requires_operator_approval") is not True:
        raise V1FileMutationPolicyError("file mutation requires operator approval")
    if classification.get("actual_execution_requested") is not False:
        raise V1FileMutationPolicyError("actual file mutation execution is not approved")

    if request_type == "file_delete" and mutation_kind != "destructive_delete":
        raise V1FileMutationPolicyError("file delete must use destructive_delete classification")
    if request_type == "file_edit" and mutation_kind not in {
        "destructive_edit",
        "destructive_file_mutation",
    }:
        raise V1FileMutationPolicyError("file edit must use destructive edit classification")
    return request_type, mutation_kind


def _validate_intent_scope(intent_scope: Mapping[str, Any]) -> str:
    _required_text(intent_scope.get("scope_id"), "mutation_intent_scope.scope_id")
    target_ref = _required_text(
        intent_scope.get("target_ref"),
        "mutation_intent_scope.target_ref",
    )
    target_path = _required_text(
        intent_scope.get("target_path"),
        "mutation_intent_scope.target_path",
    )
    normalized_target_path_ref = _required_text(
        intent_scope.get("normalized_target_path_ref"),
        "mutation_intent_scope.normalized_target_path_ref",
    )
    if intent_scope.get("path_traversal_rejected") is not True:
        raise V1FileMutationPolicyError("path traversal rejection must be represented")
    if intent_scope.get("target_path_normalization_required") is not True:
        raise V1FileMutationPolicyError("target path normalization is required")
    if intent_scope.get("mutation_outside_scope_allowed") is not False:
        raise V1FileMutationPolicyError("mutation outside approved scope is not allowed")

    normalized = _normalize_relative_path(target_path, "mutation_intent_scope.target_path")
    normalized_ref = _normalize_relative_path(
        normalized_target_path_ref,
        "mutation_intent_scope.normalized_target_path_ref",
    )
    if normalized != normalized_ref:
        raise V1FileMutationPolicyError("target path normalization mismatch")
    if not target_ref.strip():
        raise V1FileMutationPolicyError("mutation_intent_scope.target_ref is required")
    return normalized


def _validate_workspace_boundary(workspace_boundary: Mapping[str, Any]) -> None:
    _required_text(workspace_boundary.get("workspace_ref"), "workspace_root_boundary.workspace_ref")
    _required_text(workspace_boundary.get("root_ref"), "workspace_root_boundary.root_ref")
    if workspace_boundary.get("root_boundary_required") is not True:
        raise V1FileMutationPolicyError("workspace/root boundary is required")
    if workspace_boundary.get("outside_workspace_allowed") is not False:
        raise V1FileMutationPolicyError("mutation outside workspace/root is not allowed")
    if workspace_boundary.get("path_traversal_rejected") is not True:
        raise V1FileMutationPolicyError("path traversal rejection must be represented")


def _validate_path_expectations(
    path_expectations: Mapping[str, Any],
    normalized_target_path: str,
    intent_scope: Mapping[str, Any],
) -> None:
    if path_expectations.get("normalization_required") is not True:
        raise V1FileMutationPolicyError("target path normalization is required")
    if path_expectations.get("path_traversal_rejected") is not True:
        raise V1FileMutationPolicyError("path traversal rejection must be represented")
    if path_expectations.get("absolute_paths_rejected") is not True:
        raise V1FileMutationPolicyError("absolute path rejection must be represented")
    if path_expectations.get("outside_workspace_rejected") is not True:
        raise V1FileMutationPolicyError("outside workspace rejection must be represented")

    prefixes = _string_sequence(
        intent_scope.get("approved_path_prefixes"),
        "mutation_intent_scope.approved_path_prefixes",
    )
    if not prefixes:
        raise V1FileMutationPolicyError("approved path prefixes are required")
    normalized_prefixes = tuple(
        _normalize_relative_path(prefix, "mutation_intent_scope.approved_path_prefixes")
        for prefix in prefixes
    )
    if not any(
        normalized_target_path == prefix
        or normalized_target_path.startswith(f"{prefix.rstrip('/')}/")
        for prefix in normalized_prefixes
    ):
        raise V1FileMutationPolicyError("target path is outside approved scope")


def _validate_shell_authority(shell_authority: Mapping[str, Any]) -> None:
    _required_text(
        shell_authority.get("authority_ref"),
        "shell_harness_file_authority.authority_ref",
    )
    if shell_authority.get("provided_by_shell_or_harness") is not True:
        raise V1FileMutationPolicyError("shell/harness file authority is required")
    if shell_authority.get("authority_required") is not True:
        raise V1FileMutationPolicyError("shell/harness file authority is required")
    if shell_authority.get("execution_authority_granted") is not False:
        raise V1FileMutationPolicyError("shell/harness authority cannot grant execution")
    if not _string_sequence(
        shell_authority.get("authority_scope_refs"),
        "shell_harness_file_authority.authority_scope_refs",
    ):
        raise V1FileMutationPolicyError("shell/harness authority scope refs are required")


def _validate_approval_requirements(approval_requirements: Mapping[str, Any]) -> None:
    if approval_requirements.get("approval_required") is not True:
        raise V1FileMutationPolicyError("operator approval evidence is required")
    _required_text(
        approval_requirements.get("approval_policy_ref"),
        "operator_approval_evidence_requirements.approval_policy_ref",
    )
    if approval_requirements.get("approval_evidence_required") is not True:
        raise V1FileMutationPolicyError("operator approval evidence is required")
    if approval_requirements.get("mutation_without_approval_allowed") is not False:
        raise V1FileMutationPolicyError("mutation without approval is not allowed")
    if approval_requirements.get("approval_state_required") != "granted":
        raise V1FileMutationPolicyError("approval state must require granted")
    if approval_requirements.get("approval_freshness_required") != "fresh":
        raise V1FileMutationPolicyError("approval freshness must require fresh")
    if approval_requirements.get("approval_replay_status_required") != "not_replayed":
        raise V1FileMutationPolicyError("approval replay status must require not_replayed")


def _validate_preview_expectations(
    dry_run_preview: Mapping[str, Any],
    diff_preview: Mapping[str, Any],
) -> None:
    if dry_run_preview.get("required") is not True:
        raise V1FileMutationPolicyError("dry-run preview is required")
    if dry_run_preview.get("actual_mutation_allowed_in_preview") is not False:
        raise V1FileMutationPolicyError("dry-run preview cannot allow mutation")
    if diff_preview.get("required") is not True:
        raise V1FileMutationPolicyError("diff/patch preview is required")
    if diff_preview.get("redacted_metadata_only") is not True:
        raise V1FileMutationPolicyError("diff/patch preview must be redacted metadata only")
    if diff_preview.get("raw_file_content_allowed") is not False:
        raise V1FileMutationPolicyError("raw file content is not allowed")


def _validate_rollback(rollback: Mapping[str, Any]) -> None:
    if rollback.get("required") is not True:
        raise V1FileMutationPolicyError("rollback expectation is required")
    _required_text(rollback.get("rollback_plan_ref"), "rollback_expectation.rollback_plan_ref")


def _validate_delete_confirmation(
    delete_confirmation: Mapping[str, Any],
    request_type: str,
) -> None:
    if delete_confirmation.get("required_for_delete") is not True:
        raise V1FileMutationPolicyError("destructive delete confirmation policy is required")
    if delete_confirmation.get("confirmation_ref_required") is not True:
        raise V1FileMutationPolicyError("destructive delete confirmation ref is required")
    if request_type == "file_delete":
        _required_text(
            delete_confirmation.get("confirmation_policy_ref"),
            "destructive_delete_confirmation_expectation.confirmation_policy_ref",
        )


def _validate_audit_linkage(audit_linkage: Mapping[str, Any]) -> tuple[str, ...]:
    if audit_linkage.get("required") is not True:
        raise V1FileMutationPolicyError("audit/evidence linkage is required")
    if audit_linkage.get("proof_not_authority") is not True:
        raise V1FileMutationPolicyError("audit/evidence metadata cannot be authority")
    _required_text(audit_linkage.get("audit_record_ref"), "audit_evidence_linkage.audit_record_ref")
    evidence_refs = _string_sequence(
        audit_linkage.get("evidence_refs"),
        "audit_evidence_linkage.evidence_refs",
    )
    if not evidence_refs:
        raise V1FileMutationPolicyError("audit/evidence refs are required")
    return evidence_refs


def _reject_raw_sensitive_content(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            if isinstance(key, str) and key.strip().lower() in RAW_SENSITIVE_KEYS:
                raise V1FileMutationPolicyError("raw sensitive content is not accepted")
            _reject_raw_sensitive_content(nested)
    elif isinstance(value, (list, tuple, set, frozenset)):
        for nested in value:
            _reject_raw_sensitive_content(nested)
    elif isinstance(value, str):
        folded = value.strip().lower()
        if any(marker in folded for marker in RAW_SENSITIVE_VALUE_MARKERS):
            raise V1FileMutationPolicyError("raw sensitive content is not accepted")


def _reject_runtime_authority_claims(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            if (
                isinstance(key, str)
                and key.strip().lower() in FORBIDDEN_TRUE_CLAIM_KEYS
                and nested is not False
            ):
                raise V1FileMutationPolicyError(
                    "file mutation policy cannot grant runtime authority"
                )
            _reject_runtime_authority_claims(nested)
    elif isinstance(value, (list, tuple, set, frozenset)):
        for nested in value:
            _reject_runtime_authority_claims(nested)


def _normalize_relative_path(path_value: str, field_name: str) -> str:
    path = _required_text(path_value, field_name).replace("\\", "/").strip()
    while path.startswith("./"):
        path = path[2:]
    if not path:
        raise V1FileMutationPolicyError(f"{field_name} is required")
    if path.startswith("/") or path.startswith("~") or path.startswith("//"):
        raise V1FileMutationPolicyError("absolute or home paths are not allowed")
    if len(path) >= 2 and path[1] == ":":
        raise V1FileMutationPolicyError("absolute or drive paths are not allowed")
    segments = [segment for segment in path.split("/") if segment]
    if any(segment == ".." for segment in segments):
        raise V1FileMutationPolicyError("path traversal is not allowed")
    return "/".join(segments)


def _mapping(value: Any, field_name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping) or not value:
        raise V1FileMutationPolicyError(f"{field_name} is required")
    return value


def _required_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise V1FileMutationPolicyError(f"{field_name} is required")
    return value.strip()


def _string_sequence(value: Any, field_name: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        value = (value,)
    if not isinstance(value, Sequence) or isinstance(value, (bytes, bytearray)):
        raise V1FileMutationPolicyError(f"{field_name} must be a string sequence")
    return tuple(str(item).strip() for item in value if str(item).strip())


def _record_hash(record: Mapping[str, Any]) -> str:
    sanitized = _json_ready({key: value for key, value in record.items() if key != "record_hash"})
    encoded = json.dumps(sanitized, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _json_ready(nested) for key, nested in value.items()}
    if isinstance(value, (list, tuple, set, frozenset)):
        return [_json_ready(nested) for nested in value]
    return value
