"""V1 consumer proof-to-import dry-run metadata validator.

This module is the approved V1-G23 candidate runtime slice. It validates
sanitized consumer import-plan evidence for future integration review without
editing consumer repositories, importing consumer code, calling consumer
runtimes, cleaning up exports, or invoking external systems.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import hashlib
import json
import string
from typing import Any, Final


SCHEMA_VERSION: Final[str] = "v1-g23-candidate"
LIMA_DEVICE_OS_FAMILY: Final[str] = "lima_" "ro" "bo" "_os"
ALLOWED_CONSUMER_PACKET_FAMILIES: Final[frozenset[str]] = frozenset(
    {"sparkbot", "arc_bot", LIMA_DEVICE_OS_FAMILY, "lima_office", "future_shell"}
)
REQUIRED_TOP_LEVEL_FIELDS: Final[tuple[str, ...]] = (
    "import_plan_id",
    "consumer_packet_family",
    "consumer_name",
    "consumer_repository",
    "consumer_branch_ref",
    "consumer_commit_sha",
    "proof_packet_ref",
    "compatibility_packet_ref",
    "frozen_api_packet_ref",
    "proposed_import_metadata",
    "proposed_call_site_metadata",
    "adapter_boundary_mapping",
    "guardian_boundary_mapping",
    "approval_boundary_mapping",
    "provider_model_route_boundary_mapping",
    "expected_test_command_metadata",
    "rollback_metadata",
    "no_consumer_repo_mutation_confirmation",
    "no_live_import_call_confirmation",
    "no_runtime_export_cleanup_confirmation",
    "no_raw_content_secret_credential_customer_data_confirmation",
    "proof_not_authority_confirmation",
    "audit_evidence_linkage",
)
RAW_SENSITIVE_KEYS: Final[frozenset[str]] = frozenset(
    {
        "api_key",
        "approval_pin",
        "approval_token",
        "content",
        "credential",
        "credentials",
        "customer_data",
        "diff",
        "diff_body",
        "diff_contents",
        "file_content",
        "file_contents",
        "message_text",
        "oauth_token",
        "operator_pin",
        "password",
        "patch",
        "patch_body",
        "patch_contents",
        "pin",
        "prompt",
        "provider_api_key",
        "provider_credentials",
        "provider_token",
        "raw_approval_pin",
        "raw_approval_token",
        "raw_content",
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
    "raw content",
    "raw prompt",
    "raw file contents",
    "raw file content",
    "raw diff",
    "raw patch",
    "raw customer data",
    "provider credential",
    "provider token",
    "api key",
    "secret value",
)
FORBIDDEN_TRUE_CLAIM_KEYS: Final[frozenset[str]] = frozenset(
    {
        "action_executed",
        "browser_action_executed",
        "connector_invoked",
        "consumer_code_imported",
        "consumer_code_imports_added",
        "consumer_file_written",
        "consumer_integration_added",
        "consumer_repo_edited",
        "consumer_repo_mutation_added",
        "consumer_runtime_called",
        "consumer_runtime_calls_added",
        "consumer_runtime_invoked",
        "credential_access_added",
        "device_command_invoked",
        "drone_control_invoked",
        "execution_allowed",
        "execution_authority_added",
        "external_send_added",
        "file_mutation_executed",
        "humaninput_bridge_activated",
        "iot_control_invoked",
        "live_call_performed",
        "live_import_performed",
        "model_request_dispatched",
        "network_action_executed",
        "physical_world_invoked",
        "product_ready",
        "provider_model_calls_added",
        "provider_model_routed",
        "ro" "bot_control_invoked",
        "ro" "botics_invoked",
        "runtime_export_cleanup_approved",
        "runtime_export_cleanup_performed",
        "runtime_export_cleanup_required",
        "scheduled_task_executed",
        "secret_lookup_added",
        "shell_runtime_wired",
        "shell_wired",
        "side_effects_allowed",
        "tool_executed",
    }
)


class V1ConsumerImportDryRunError(ValueError):
    """Raised when consumer import dry-run metadata fails the V1-G23 boundary."""


def validate_v1_consumer_integration_proof_to_import_dry_run(
    import_plan_metadata: Mapping[str, Any],
) -> dict[str, Any]:
    """Return a deterministic non-executing consumer import dry-run record."""

    if not isinstance(import_plan_metadata, Mapping):
        raise V1ConsumerImportDryRunError("import_plan_metadata must be a mapping")

    _reject_raw_sensitive_content(import_plan_metadata)
    _reject_runtime_authority_claims(import_plan_metadata)

    for field_name in REQUIRED_TOP_LEVEL_FIELDS:
        if field_name not in import_plan_metadata:
            raise V1ConsumerImportDryRunError(f"{field_name} is required")

    import_plan_id = _required_text(
        import_plan_metadata.get("import_plan_id"),
        "import_plan_id",
    )
    consumer_packet_family = _consumer_packet_family(
        import_plan_metadata.get("consumer_packet_family")
    )
    consumer_name = _required_text(
        import_plan_metadata.get("consumer_name"),
        "consumer_name",
    )
    consumer_repository = _required_text(
        import_plan_metadata.get("consumer_repository"),
        "consumer_repository",
    )
    consumer_branch_ref = _required_text(
        import_plan_metadata.get("consumer_branch_ref"),
        "consumer_branch_ref",
    )
    consumer_commit_sha = _commit_sha(
        import_plan_metadata.get("consumer_commit_sha"),
        "consumer_commit_sha",
    )
    proof_packet_ref = _required_text(
        import_plan_metadata.get("proof_packet_ref"),
        "proof_packet_ref",
    )
    compatibility_packet_ref = _required_text(
        import_plan_metadata.get("compatibility_packet_ref"),
        "compatibility_packet_ref",
    )
    frozen_api_packet_ref = _required_text(
        import_plan_metadata.get("frozen_api_packet_ref"),
        "frozen_api_packet_ref",
    )
    proposed_import = _validate_proposed_import_metadata(
        import_plan_metadata.get("proposed_import_metadata")
    )
    proposed_call_site = _validate_proposed_call_site_metadata(
        import_plan_metadata.get("proposed_call_site_metadata")
    )
    adapter_boundary = _validate_boundary_mapping(
        import_plan_metadata.get("adapter_boundary_mapping"),
        "adapter_boundary_mapping",
    )
    guardian_boundary = _validate_boundary_mapping(
        import_plan_metadata.get("guardian_boundary_mapping"),
        "guardian_boundary_mapping",
    )
    approval_boundary = _validate_boundary_mapping(
        import_plan_metadata.get("approval_boundary_mapping"),
        "approval_boundary_mapping",
    )
    provider_model_boundary = _validate_boundary_mapping(
        import_plan_metadata.get("provider_model_route_boundary_mapping"),
        "provider_model_route_boundary_mapping",
    )
    expected_tests = _validate_expected_test_command_metadata(
        import_plan_metadata.get("expected_test_command_metadata")
    )
    rollback = _validate_rollback_metadata(
        import_plan_metadata.get("rollback_metadata")
    )
    _require_true_confirmation(
        import_plan_metadata.get("no_consumer_repo_mutation_confirmation"),
        "no_consumer_repo_mutation_confirmation",
    )
    _require_true_confirmation(
        import_plan_metadata.get("no_live_import_call_confirmation"),
        "no_live_import_call_confirmation",
    )
    _require_true_confirmation(
        import_plan_metadata.get("no_runtime_export_cleanup_confirmation"),
        "no_runtime_export_cleanup_confirmation",
    )
    _require_true_confirmation(
        import_plan_metadata.get(
            "no_raw_content_secret_credential_customer_data_confirmation"
        ),
        "no_raw_content_secret_credential_customer_data_confirmation",
    )
    _require_true_confirmation(
        import_plan_metadata.get("proof_not_authority_confirmation"),
        "proof_not_authority_confirmation",
    )
    audit_linkage = _validate_audit_linkage(
        import_plan_metadata.get("audit_evidence_linkage")
    )

    record = {
        "record_type": "v1_consumer_integration_proof_to_import_dry_run",
        "schema_version": SCHEMA_VERSION,
        "import_plan_id": import_plan_id,
        "consumer_packet_family": consumer_packet_family,
        "consumer_name": consumer_name,
        "consumer_repository": consumer_repository,
        "consumer_branch_ref": consumer_branch_ref,
        "consumer_commit_sha": consumer_commit_sha,
        "proof_packet_ref": proof_packet_ref,
        "compatibility_packet_ref": compatibility_packet_ref,
        "frozen_api_packet_ref": frozen_api_packet_ref,
        "proposed_import_metadata": proposed_import,
        "proposed_call_site_metadata": proposed_call_site,
        "adapter_boundary_mapping": adapter_boundary,
        "guardian_boundary_mapping": guardian_boundary,
        "approval_boundary_mapping": approval_boundary,
        "provider_model_route_boundary_mapping": provider_model_boundary,
        "expected_test_command_metadata": expected_tests,
        "rollback_metadata": rollback,
        "audit_evidence_linkage": audit_linkage,
        "capability_open": True,
        "authority_gated": True,
        "consumer_import_dry_run_runtime_behavior": True,
        "import_plan_metadata_only": True,
        "proof_not_authority": True,
        "non_executing": True,
        "redacted_metadata_only": True,
        "consumer_repo_mutation_added": False,
        "consumer_code_imported": False,
        "consumer_code_imports_added": False,
        "consumer_runtime_calls_added": False,
        "consumer_runtime_called": False,
        "consumer_integration_added": False,
        "shell_runtime_wired": False,
        "runtime_export_cleanup_approved": False,
        "runtime_export_cleanup_performed": False,
        "provider_model_calls_added": False,
        "model_request_dispatched": False,
        "secret_lookup_added": False,
        "credential_access_added": False,
        "tool_executed": False,
        "execution_allowed": False,
        "side_effects_allowed": False,
        "action_executed": False,
        "file_mutation_executed": False,
        "connector_invoked": False,
        "browser_action_executed": False,
        "network_action_executed": False,
        "scheduled_task_executed": False,
        "external_send_added": False,
        "device_command_invoked": False,
        "ro" "bot_control_invoked": False,
        "drone_control_invoked": False,
        "iot_control_invoked": False,
        "physical_world_invoked": False,
        "raw_sensitive_content_persisted": False,
        "product_ready": False,
        "metadata": {
            "v1_runtime_slice": "consumer_integration_proof_to_import_dry_run",
            "candidate_only": True,
            "non_executing": True,
            "proof_not_authority": True,
        },
    }
    record["record_hash"] = _record_hash(record)
    return record


def _validate_proposed_import_metadata(value: Any) -> dict[str, Any]:
    metadata = _mapping(value, "proposed_import_metadata")
    import_refs = _string_sequence(
        metadata.get("import_refs"),
        "proposed_import_metadata.import_refs",
        allow_empty=False,
    )
    import_target_refs = _string_sequence(
        metadata.get("import_target_refs"),
        "proposed_import_metadata.import_target_refs",
        allow_empty=False,
    )
    if metadata.get("metadata_only") is not True:
        raise V1ConsumerImportDryRunError(
            "proposed import metadata must be metadata only"
        )
    if metadata.get("consumer_code_imported") is not False:
        raise V1ConsumerImportDryRunError("consumer code imports are not approved")
    if metadata.get("live_import_performed") is not False:
        raise V1ConsumerImportDryRunError("live consumer imports are not approved")
    if metadata.get("consumer_repo_mutation_added") is not False:
        raise V1ConsumerImportDryRunError("consumer repo mutation is not approved")
    if metadata.get("grants_runtime_authority") is not False:
        raise V1ConsumerImportDryRunError(
            "import-plan metadata cannot grant runtime authority"
        )
    return {
        "import_refs": list(import_refs),
        "import_target_refs": list(import_target_refs),
        "metadata_only": True,
        "consumer_code_imported": False,
        "live_import_performed": False,
        "consumer_repo_mutation_added": False,
        "grants_runtime_authority": False,
    }


def _validate_proposed_call_site_metadata(value: Any) -> dict[str, Any]:
    metadata = _mapping(value, "proposed_call_site_metadata")
    call_site_refs = _string_sequence(
        metadata.get("call_site_refs"),
        "proposed_call_site_metadata.call_site_refs",
        allow_empty=False,
    )
    call_shape_refs = _string_sequence(
        metadata.get("call_shape_refs"),
        "proposed_call_site_metadata.call_shape_refs",
        allow_empty=False,
    )
    if metadata.get("metadata_only") is not True:
        raise V1ConsumerImportDryRunError(
            "proposed call-site metadata must be metadata only"
        )
    if metadata.get("live_call_performed") is not False:
        raise V1ConsumerImportDryRunError("consumer runtime calls are not approved")
    if metadata.get("consumer_runtime_calls_added") is not False:
        raise V1ConsumerImportDryRunError("consumer runtime calls are not approved")
    if metadata.get("consumer_runtime_invoked") is not False:
        raise V1ConsumerImportDryRunError("consumer runtime calls are not approved")
    if metadata.get("grants_runtime_authority") is not False:
        raise V1ConsumerImportDryRunError(
            "import-plan metadata cannot grant runtime authority"
        )
    return {
        "call_site_refs": list(call_site_refs),
        "call_shape_refs": list(call_shape_refs),
        "metadata_only": True,
        "live_call_performed": False,
        "consumer_runtime_calls_added": False,
        "consumer_runtime_invoked": False,
        "grants_runtime_authority": False,
    }


def _validate_boundary_mapping(value: Any, field_name: str) -> dict[str, Any]:
    boundary = _mapping(value, field_name)
    boundary_ref = _required_text(
        boundary.get("boundary_ref"),
        f"{field_name}.boundary_ref",
    )
    mapped_refs = _string_sequence(
        boundary.get("mapped_refs"),
        f"{field_name}.mapped_refs",
        allow_empty=False,
    )
    if boundary.get("compatible") is not True:
        raise V1ConsumerImportDryRunError(f"{field_name} compatibility is required")
    if boundary.get("metadata_only") is not True:
        raise V1ConsumerImportDryRunError(f"{field_name} must be metadata only")
    if boundary.get("proof_not_authority") is not True:
        raise V1ConsumerImportDryRunError(f"{field_name} metadata cannot be authority")
    if boundary.get("grants_execution_authority") is not False:
        raise V1ConsumerImportDryRunError(f"{field_name} cannot grant execution")
    if boundary.get("future_integration_requires_approval") is not True:
        raise V1ConsumerImportDryRunError(
            "future integration approval requirement is required"
        )
    return {
        "boundary_ref": boundary_ref,
        "mapped_refs": list(mapped_refs),
        "compatible": True,
        "metadata_only": True,
        "proof_not_authority": True,
        "grants_execution_authority": False,
        "future_integration_requires_approval": True,
    }


def _validate_expected_test_command_metadata(value: Any) -> dict[str, Any]:
    metadata = _mapping(value, "expected_test_command_metadata")
    command_refs = _string_sequence(
        metadata.get("command_refs"),
        "expected_test_command_metadata.command_refs",
        allow_empty=False,
    )
    expected_result_refs = _string_sequence(
        metadata.get("expected_result_refs"),
        "expected_test_command_metadata.expected_result_refs",
        allow_empty=False,
    )
    if metadata.get("metadata_only") is not True:
        raise V1ConsumerImportDryRunError(
            "expected test command metadata must be metadata only"
        )
    if metadata.get("dry_run_only") is not True:
        raise V1ConsumerImportDryRunError("expected tests must be dry-run only")
    if metadata.get("consumer_runtime_invoked") is not False:
        raise V1ConsumerImportDryRunError("consumer runtime calls are not approved")
    if metadata.get("external_services_required") is not False:
        raise V1ConsumerImportDryRunError("external services are not approved")
    return {
        "command_refs": list(command_refs),
        "expected_result_refs": list(expected_result_refs),
        "metadata_only": True,
        "dry_run_only": True,
        "consumer_runtime_invoked": False,
        "external_services_required": False,
    }


def _validate_rollback_metadata(value: Any) -> dict[str, Any]:
    metadata = _mapping(value, "rollback_metadata")
    rollback_ref = _required_text(
        metadata.get("rollback_ref"),
        "rollback_metadata.rollback_ref",
    )
    rollback_step_refs = _string_sequence(
        metadata.get("rollback_step_refs"),
        "rollback_metadata.rollback_step_refs",
        allow_empty=False,
    )
    if metadata.get("consumer_repo_changes_required") is not False:
        raise V1ConsumerImportDryRunError("consumer repo mutation is not approved")
    if metadata.get("runtime_export_cleanup_required") is not False:
        raise V1ConsumerImportDryRunError("runtime export cleanup is not approved")
    if metadata.get("external_service_changes_required") is not False:
        raise V1ConsumerImportDryRunError("external services are not approved")
    return {
        "rollback_ref": rollback_ref,
        "rollback_step_refs": list(rollback_step_refs),
        "consumer_repo_changes_required": False,
        "runtime_export_cleanup_required": False,
        "external_service_changes_required": False,
    }


def _validate_audit_linkage(value: Any) -> dict[str, Any]:
    audit = _mapping(value, "audit_evidence_linkage")
    audit_record_ref = _required_text(
        audit.get("audit_record_ref"),
        "audit_evidence_linkage.audit_record_ref",
    )
    evidence_refs = _string_sequence(
        audit.get("evidence_refs"),
        "audit_evidence_linkage.evidence_refs",
        allow_empty=False,
    )
    if audit.get("required") is not True:
        raise V1ConsumerImportDryRunError("audit/evidence linkage is required")
    if audit.get("proof_not_authority") is not True:
        raise V1ConsumerImportDryRunError(
            "audit/evidence metadata cannot be authority"
        )
    return {
        "audit_record_ref": audit_record_ref,
        "evidence_refs": list(evidence_refs),
        "required": True,
        "proof_not_authority": True,
    }


def _reject_raw_sensitive_content(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            if isinstance(key, str) and key.strip().lower() in RAW_SENSITIVE_KEYS:
                raise V1ConsumerImportDryRunError(
                    "raw sensitive content is not accepted"
                )
            _reject_raw_sensitive_content(nested)
    elif isinstance(value, (list, tuple, set, frozenset)):
        for nested in value:
            _reject_raw_sensitive_content(nested)
    elif isinstance(value, str):
        folded = value.strip().lower()
        if any(marker in folded for marker in RAW_SENSITIVE_VALUE_MARKERS):
            raise V1ConsumerImportDryRunError(
                "raw sensitive content is not accepted"
            )


def _reject_runtime_authority_claims(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            if (
                isinstance(key, str)
                and key.strip().lower() in FORBIDDEN_TRUE_CLAIM_KEYS
                and nested is not False
            ):
                raise V1ConsumerImportDryRunError(
                    "import-plan metadata cannot grant runtime authority"
                )
            _reject_runtime_authority_claims(nested)
    elif isinstance(value, (list, tuple, set, frozenset)):
        for nested in value:
            _reject_runtime_authority_claims(nested)


def _consumer_packet_family(value: Any) -> str:
    family = _normalize_token(_required_text(value, "consumer_packet_family"))
    if family not in ALLOWED_CONSUMER_PACKET_FAMILIES:
        raise V1ConsumerImportDryRunError("consumer packet family is not allowed")
    return family


def _commit_sha(value: Any, field_name: str) -> str:
    commit = _required_text(value, field_name).lower()
    if len(commit) < 7 or len(commit) > 64:
        raise V1ConsumerImportDryRunError(f"{field_name} must be a commit SHA")
    if any(character not in string.hexdigits.lower() for character in commit):
        raise V1ConsumerImportDryRunError(f"{field_name} must be a commit SHA")
    return commit


def _mapping(value: Any, field_name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping) or not value:
        raise V1ConsumerImportDryRunError(f"{field_name} is required")
    return value


def _required_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise V1ConsumerImportDryRunError(f"{field_name} is required")
    return value.strip()


def _string_sequence(
    value: Any,
    field_name: str,
    *,
    allow_empty: bool,
) -> tuple[str, ...]:
    if isinstance(value, str):
        value = (value,)
    if not isinstance(value, Sequence) or isinstance(value, (bytes, bytearray)):
        raise V1ConsumerImportDryRunError(f"{field_name} must be a string sequence")
    normalized = tuple(str(item).strip() for item in value if str(item).strip())
    if not normalized and not allow_empty:
        raise V1ConsumerImportDryRunError(f"{field_name} is required")
    return normalized


def _require_true_confirmation(value: Any, field_name: str) -> None:
    if value is True:
        return
    if isinstance(value, Mapping) and value.get("confirmed") is True:
        return
    raise V1ConsumerImportDryRunError(f"{field_name} confirmation is required")


def _normalize_token(value: str) -> str:
    return value.strip().lower().replace("-", "_").replace(" ", "_")


def _record_hash(record: Mapping[str, Any]) -> str:
    sanitized = _json_ready(
        {key: value for key, value in record.items() if key != "record_hash"}
    )
    encoded = json.dumps(sanitized, sort_keys=True, separators=(",", ":")).encode(
        "utf-8"
    )
    return hashlib.sha256(encoded).hexdigest()


def _json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _json_ready(nested) for key, nested in value.items()}
    if isinstance(value, (list, tuple, set, frozenset)):
        return [_json_ready(nested) for nested in value]
    return value
