"""V1 file mutation preview/diff metadata validator.

This module is the approved V1-G17 candidate runtime slice. It validates
sanitized dry-run preview and redacted diff/patch metadata for proposed file
mutations. It never reads user files, writes files, deletes files, applies
patches, routes providers, wires shells, invokes connectors, or performs
external actions.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import hashlib
import json
from typing import Any, Final


SCHEMA_VERSION: Final[str] = "v1-g17-candidate"
POLICY_SCHEMA_VERSION: Final[str] = "v1-g16-candidate"
REQUIRED_TOP_LEVEL_FIELDS: Final[tuple[str, ...]] = (
    "guarded_file_mutation_policy_ref",
    "guarded_file_mutation_policy",
    "path_scope_validation",
    "workspace_root_validation",
    "path_traversal_rejection",
    "dry_run_file_mutation_preview",
    "redacted_diff_patch_preview",
    "rollback_plan_metadata",
    "approval_evidence_linkage",
    "user_operator_confirmation_linkage",
    "shell_harness_policy_linkage",
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
        "diff",
        "diff_body",
        "diff_contents",
        "file_content",
        "file_contents",
        "message_text",
        "operator_pin",
        "password",
        "patch",
        "patch_body",
        "patch_contents",
        "pin",
        "prompt",
        "provider_credentials",
        "raw_approval_pin",
        "raw_approval_token",
        "raw_customer_data",
        "raw_diff",
        "raw_diff_contents",
        "raw_file_content",
        "raw_file_contents",
        "raw_human_input",
        "raw_patch",
        "raw_patch_contents",
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
        "actual_file_mutation_execution_approved",
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
        "file_read",
        "file_written",
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


class V1FileMutationPreviewError(ValueError):
    """Raised when preview/diff metadata fails the V1-G17 boundary."""


def validate_v1_file_mutation_preview_diff(
    preview_metadata: Mapping[str, Any],
) -> dict[str, Any]:
    """Return a deterministic non-mutating preview/diff proof record."""

    if not isinstance(preview_metadata, Mapping):
        raise V1FileMutationPreviewError("preview_metadata must be a mapping")

    _reject_raw_sensitive_content(preview_metadata)
    _reject_runtime_authority_claims(preview_metadata)

    for field_name in REQUIRED_TOP_LEVEL_FIELDS:
        if field_name not in preview_metadata:
            raise V1FileMutationPreviewError(f"{field_name} is required")

    policy_ref = _required_text(
        preview_metadata.get("guarded_file_mutation_policy_ref"),
        "guarded_file_mutation_policy_ref",
    )
    policy = _mapping(
        preview_metadata.get("guarded_file_mutation_policy"),
        "guarded_file_mutation_policy",
    )
    path_scope = _mapping(
        preview_metadata.get("path_scope_validation"),
        "path_scope_validation",
    )
    workspace_root = _mapping(
        preview_metadata.get("workspace_root_validation"),
        "workspace_root_validation",
    )
    traversal = _mapping(
        preview_metadata.get("path_traversal_rejection"),
        "path_traversal_rejection",
    )
    dry_run_preview = _mapping(
        preview_metadata.get("dry_run_file_mutation_preview"),
        "dry_run_file_mutation_preview",
    )
    diff_preview = _mapping(
        preview_metadata.get("redacted_diff_patch_preview"),
        "redacted_diff_patch_preview",
    )
    rollback = _mapping(
        preview_metadata.get("rollback_plan_metadata"),
        "rollback_plan_metadata",
    )
    approval_linkage = _mapping(
        preview_metadata.get("approval_evidence_linkage"),
        "approval_evidence_linkage",
    )
    confirmation_linkage = _mapping(
        preview_metadata.get("user_operator_confirmation_linkage"),
        "user_operator_confirmation_linkage",
    )
    shell_policy_linkage = _mapping(
        preview_metadata.get("shell_harness_policy_linkage"),
        "shell_harness_policy_linkage",
    )
    audit_linkage = _mapping(
        preview_metadata.get("audit_evidence_linkage"),
        "audit_evidence_linkage",
    )
    tenant_scope = _required_text(preview_metadata.get("tenant_scope"), "tenant_scope")
    shell_scope = _required_text(preview_metadata.get("shell_scope"), "shell_scope")
    actor_scope = _required_text(preview_metadata.get("actor_scope"), "actor_scope")
    session_scope = _required_text(preview_metadata.get("session_scope"), "session_scope")

    normalized_path = _validate_policy_linkage(
        policy_ref,
        policy,
        tenant_scope,
        shell_scope,
        actor_scope,
        session_scope,
    )
    _validate_path_scope(path_scope, normalized_path)
    _validate_workspace_root(workspace_root)
    _validate_traversal_rejection(traversal, normalized_path)
    preview_id = _validate_dry_run_preview(dry_run_preview, normalized_path)
    diff_id = _validate_diff_preview(diff_preview)
    rollback_ref = _validate_rollback(rollback)
    approval_ref = _validate_approval_linkage(approval_linkage)
    confirmation_ref = _validate_confirmation_linkage(confirmation_linkage)
    shell_policy_ref = _validate_shell_policy_linkage(shell_policy_linkage)
    evidence_refs = _validate_audit_linkage(audit_linkage)

    record = {
        "record_type": "v1_file_mutation_preview_diff",
        "schema_version": SCHEMA_VERSION,
        "guarded_file_mutation_policy_ref": policy_ref,
        "policy_schema_version": policy.get("schema_version"),
        "preview_id": preview_id,
        "diff_preview_id": diff_id,
        "normalized_target_path": normalized_path,
        "rollback_plan_ref": rollback_ref,
        "approval_evidence_ref": approval_ref,
        "confirmation_ref": confirmation_ref,
        "shell_policy_ref": shell_policy_ref,
        "tenant_scope": tenant_scope,
        "shell_scope": shell_scope,
        "actor_scope": actor_scope,
        "session_scope": session_scope,
        "path_scope_validation": _json_ready(path_scope),
        "workspace_root_validation": _json_ready(workspace_root),
        "path_traversal_rejection": _json_ready(traversal),
        "dry_run_file_mutation_preview": _json_ready(dry_run_preview),
        "redacted_diff_patch_preview": _json_ready(diff_preview),
        "rollback_plan_metadata": _json_ready(rollback),
        "approval_evidence_linkage": _json_ready(approval_linkage),
        "user_operator_confirmation_linkage": _json_ready(confirmation_linkage),
        "shell_harness_policy_linkage": _json_ready(shell_policy_linkage),
        "audit_evidence_linkage": _json_ready(audit_linkage),
        "evidence_refs": list(evidence_refs),
        "capability_open": True,
        "authority_gated": True,
        "preview_diff_runtime_behavior": True,
        "dry_run_only": True,
        "redacted_metadata_only": True,
        "proof_not_authority": True,
        "execution_allowed": False,
        "side_effects_allowed": False,
        "actual_file_mutation_execution_approved": False,
        "actual_file_mutation_execution_added": False,
        "file_read": False,
        "file_written": False,
        "file_deleted": False,
        "file_mutated": False,
        "file_overwritten": False,
        "patch_applied": False,
        "raw_file_content_persisted": False,
        "approval_token_issued": False,
        "consumer_integration_added": False,
        "provider_model_routed": False,
        "connector_invoked": False,
        "browser_action_executed": False,
        "network_action_executed": False,
        "physical_world_invoked": False,
        "final_api_freeze_approved": False,
        "product_ready": False,
        "metadata": {
            "v1_runtime_slice": "file_mutation_preview_diff",
            "candidate_only": True,
            "non_mutating": True,
            "proof_not_authority": True,
        },
    }
    record["record_hash"] = _record_hash(record)
    return record


def _validate_policy_linkage(
    policy_ref: str,
    policy: Mapping[str, Any],
    tenant_scope: str,
    shell_scope: str,
    actor_scope: str,
    session_scope: str,
) -> str:
    if policy.get("record_type") != "v1_guarded_file_mutation_policy":
        raise V1FileMutationPreviewError("V1-G16 policy linkage is required")
    if policy.get("schema_version") != POLICY_SCHEMA_VERSION:
        raise V1FileMutationPreviewError("V1-G16 policy schema linkage is required")
    if policy.get("record_hash") != policy_ref:
        raise V1FileMutationPreviewError("guarded policy ref must match record_hash")
    for field_name, expected in (
        ("tenant_scope", tenant_scope),
        ("shell_scope", shell_scope),
        ("actor_scope", actor_scope),
        ("session_scope", session_scope),
    ):
        if policy.get(field_name) != expected:
            raise V1FileMutationPreviewError(f"{field_name} must match guarded policy")
    if policy.get("execution_allowed") is not False:
        raise V1FileMutationPreviewError("guarded policy cannot allow execution")
    if policy.get("actual_file_mutation_execution_approved") is not False:
        raise V1FileMutationPreviewError("actual file mutation execution is not approved")
    if policy.get("file_mutation_executed") is not False:
        raise V1FileMutationPreviewError("guarded policy cannot execute mutation")
    return _normalize_relative_path(
        _required_text(policy.get("normalized_target_path"), "normalized_target_path"),
        "normalized_target_path",
    )


def _validate_path_scope(path_scope: Mapping[str, Any], normalized_path: str) -> None:
    if path_scope.get("validated") is not True:
        raise V1FileMutationPreviewError("path scope validation is required")
    if path_scope.get("within_approved_scope") is not True:
        raise V1FileMutationPreviewError("target path must be within approved scope")
    if path_scope.get("mutation_outside_scope_allowed") is not False:
        raise V1FileMutationPreviewError("mutation outside approved scope is not allowed")
    target_path = _normalize_relative_path(
        _required_text(path_scope.get("normalized_target_path"), "path_scope_validation.normalized_target_path"),
        "path_scope_validation.normalized_target_path",
    )
    if target_path != normalized_path:
        raise V1FileMutationPreviewError("preview path must match guarded policy")


def _validate_workspace_root(workspace_root: Mapping[str, Any]) -> None:
    _required_text(workspace_root.get("workspace_ref"), "workspace_root_validation.workspace_ref")
    _required_text(workspace_root.get("root_ref"), "workspace_root_validation.root_ref")
    if workspace_root.get("validated") is not True:
        raise V1FileMutationPreviewError("workspace/root validation is required")
    if workspace_root.get("inside_workspace_root") is not True:
        raise V1FileMutationPreviewError("target must be inside workspace/root")
    if workspace_root.get("outside_workspace_allowed") is not False:
        raise V1FileMutationPreviewError("outside workspace mutation is not allowed")


def _validate_traversal_rejection(
    traversal: Mapping[str, Any],
    normalized_path: str,
) -> None:
    if traversal.get("represented") is not True:
        raise V1FileMutationPreviewError("path traversal rejection must be represented")
    if traversal.get("path_traversal_rejected") is not True:
        raise V1FileMutationPreviewError("path traversal rejection must be represented")
    if traversal.get("absolute_paths_rejected") is not True:
        raise V1FileMutationPreviewError("absolute path rejection must be represented")
    for candidate in _string_sequence(
        traversal.get("checked_paths"),
        "path_traversal_rejection.checked_paths",
    ):
        _normalize_relative_path(candidate, "path_traversal_rejection.checked_paths")
    if not normalized_path:
        raise V1FileMutationPreviewError("normalized target path is required")


def _validate_dry_run_preview(
    dry_run_preview: Mapping[str, Any],
    normalized_path: str,
) -> str:
    preview_id = _required_text(dry_run_preview.get("preview_id"), "dry_run_file_mutation_preview.preview_id")
    if dry_run_preview.get("dry_run") is not True:
        raise V1FileMutationPreviewError("dry-run preview is required")
    if dry_run_preview.get("preview_generated") is not True:
        raise V1FileMutationPreviewError("preview metadata must be generated")
    if dry_run_preview.get("actual_file_write") is not False:
        raise V1FileMutationPreviewError("preview cannot write files")
    if dry_run_preview.get("actual_file_delete") is not False:
        raise V1FileMutationPreviewError("preview cannot delete files")
    if dry_run_preview.get("actual_file_mutation") is not False:
        raise V1FileMutationPreviewError("preview cannot mutate files")
    if dry_run_preview.get("raw_file_content_persisted") is not False:
        raise V1FileMutationPreviewError("raw file content cannot persist")
    target_path = _normalize_relative_path(
        _required_text(dry_run_preview.get("normalized_target_path"), "dry_run_file_mutation_preview.normalized_target_path"),
        "dry_run_file_mutation_preview.normalized_target_path",
    )
    if target_path != normalized_path:
        raise V1FileMutationPreviewError("preview path must match guarded policy")
    return preview_id


def _validate_diff_preview(diff_preview: Mapping[str, Any]) -> str:
    diff_id = _required_text(diff_preview.get("diff_preview_id"), "redacted_diff_patch_preview.diff_preview_id")
    if diff_preview.get("provided") is not True:
        raise V1FileMutationPreviewError("redacted diff/patch preview metadata is required")
    if diff_preview.get("redacted_metadata_only") is not True:
        raise V1FileMutationPreviewError("diff/patch preview must be redacted metadata only")
    if diff_preview.get("raw_file_content_persisted") is not False:
        raise V1FileMutationPreviewError("raw file content cannot persist")
    if diff_preview.get("raw_diff_persisted") is not False:
        raise V1FileMutationPreviewError("raw diff cannot persist")
    if diff_preview.get("raw_patch_persisted") is not False:
        raise V1FileMutationPreviewError("raw patch cannot persist")
    if diff_preview.get("patch_application_allowed") is not False:
        raise V1FileMutationPreviewError("patch application is not approved")
    _non_negative_int(diff_preview.get("redacted_hunk_count"), "redacted_diff_patch_preview.redacted_hunk_count")
    _non_negative_int(diff_preview.get("redacted_addition_count"), "redacted_diff_patch_preview.redacted_addition_count")
    _non_negative_int(diff_preview.get("redacted_deletion_count"), "redacted_diff_patch_preview.redacted_deletion_count")
    return diff_id


def _validate_rollback(rollback: Mapping[str, Any]) -> str:
    rollback_ref = _required_text(rollback.get("rollback_plan_ref"), "rollback_plan_metadata.rollback_plan_ref")
    if rollback.get("represented") is not True:
        raise V1FileMutationPreviewError("rollback plan metadata is required")
    if rollback.get("required_before_execution") is not True:
        raise V1FileMutationPreviewError("rollback plan must be required before execution")
    return rollback_ref


def _validate_approval_linkage(approval_linkage: Mapping[str, Any]) -> str:
    approval_ref = _required_text(
        approval_linkage.get("approval_evidence_ref"),
        "approval_evidence_linkage.approval_evidence_ref",
    )
    if approval_linkage.get("required") is not True:
        raise V1FileMutationPreviewError("approval evidence linkage is required")
    if approval_linkage.get("approval_required_before_execution") is not True:
        raise V1FileMutationPreviewError("approval evidence is required before execution")
    if approval_linkage.get("approval_metadata_grants_execution") is not False:
        raise V1FileMutationPreviewError("approval metadata cannot grant execution")
    return approval_ref


def _validate_confirmation_linkage(confirmation_linkage: Mapping[str, Any]) -> str:
    confirmation_ref = _required_text(
        confirmation_linkage.get("confirmation_ref"),
        "user_operator_confirmation_linkage.confirmation_ref",
    )
    if confirmation_linkage.get("required") is not True:
        raise V1FileMutationPreviewError("user/operator confirmation linkage is required")
    if confirmation_linkage.get("confirmation_required_before_execution") is not True:
        raise V1FileMutationPreviewError("confirmation is required before execution")
    return confirmation_ref


def _validate_shell_policy_linkage(shell_policy_linkage: Mapping[str, Any]) -> str:
    shell_policy_ref = _required_text(
        shell_policy_linkage.get("shell_policy_ref"),
        "shell_harness_policy_linkage.shell_policy_ref",
    )
    if shell_policy_linkage.get("required") is not True:
        raise V1FileMutationPreviewError("shell/harness policy linkage is required")
    if shell_policy_linkage.get("shell_runtime_wired") is not False:
        raise V1FileMutationPreviewError("shell runtime wiring is not approved")
    if shell_policy_linkage.get("execution_authority_granted") is not False:
        raise V1FileMutationPreviewError("shell policy cannot grant execution")
    return shell_policy_ref


def _validate_audit_linkage(audit_linkage: Mapping[str, Any]) -> tuple[str, ...]:
    if audit_linkage.get("required") is not True:
        raise V1FileMutationPreviewError("audit/evidence linkage is required")
    if audit_linkage.get("proof_not_authority") is not True:
        raise V1FileMutationPreviewError("audit/evidence metadata cannot be authority")
    _required_text(audit_linkage.get("audit_record_ref"), "audit_evidence_linkage.audit_record_ref")
    evidence_refs = _string_sequence(
        audit_linkage.get("evidence_refs"),
        "audit_evidence_linkage.evidence_refs",
    )
    if not evidence_refs:
        raise V1FileMutationPreviewError("audit/evidence refs are required")
    return evidence_refs


def _reject_raw_sensitive_content(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            if isinstance(key, str) and key.strip().lower() in RAW_SENSITIVE_KEYS:
                raise V1FileMutationPreviewError("raw sensitive content is not accepted")
            _reject_raw_sensitive_content(nested)
    elif isinstance(value, (list, tuple, set, frozenset)):
        for nested in value:
            _reject_raw_sensitive_content(nested)
    elif isinstance(value, str):
        folded = value.strip().lower()
        if any(marker in folded for marker in RAW_SENSITIVE_VALUE_MARKERS):
            raise V1FileMutationPreviewError("raw sensitive content is not accepted")


def _reject_runtime_authority_claims(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            if (
                isinstance(key, str)
                and key.strip().lower() in FORBIDDEN_TRUE_CLAIM_KEYS
                and nested is not False
            ):
                raise V1FileMutationPreviewError(
                    "preview/diff metadata cannot grant runtime authority"
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
        raise V1FileMutationPreviewError(f"{field_name} is required")
    if path.startswith("/") or path.startswith("~") or path.startswith("//"):
        raise V1FileMutationPreviewError("absolute or home paths are not allowed")
    if len(path) >= 2 and path[1] == ":":
        raise V1FileMutationPreviewError("absolute or drive paths are not allowed")
    segments = [segment for segment in path.split("/") if segment]
    if any(segment == ".." for segment in segments):
        raise V1FileMutationPreviewError("path traversal is not allowed")
    return "/".join(segments)


def _mapping(value: Any, field_name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping) or not value:
        raise V1FileMutationPreviewError(f"{field_name} is required")
    return value


def _required_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise V1FileMutationPreviewError(f"{field_name} is required")
    return value.strip()


def _string_sequence(value: Any, field_name: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        value = (value,)
    if not isinstance(value, Sequence) or isinstance(value, (bytes, bytearray)):
        raise V1FileMutationPreviewError(f"{field_name} must be a string sequence")
    return tuple(str(item).strip() for item in value if str(item).strip())


def _non_negative_int(value: Any, field_name: str) -> int:
    if not isinstance(value, int) or value < 0:
        raise V1FileMutationPreviewError(f"{field_name} must be a non-negative integer")
    return value


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
