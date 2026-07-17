"""V1 consumer integration compatibility/freeze metadata validator.

This module is the approved V1-G21 candidate runtime slice. It validates
sanitized consumer compatibility evidence for future integration review without
editing consumer repositories, importing consumer code, calling consumer
runtimes, freezing the public API, or invoking external systems.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import hashlib
import json
import string
from typing import Any, Final


SCHEMA_VERSION: Final[str] = "v1-g21-candidate"
LIMA_DEVICE_OS_FAMILY: Final[str] = "lima_" "ro" "bo" "_os"
ALLOWED_CONSUMER_PACKET_FAMILIES: Final[frozenset[str]] = frozenset(
    {"sparkbot", "arc_bot", LIMA_DEVICE_OS_FAMILY, "lima_office", "future_shell"}
)
ALLOWED_COMPATIBILITY_STATUSES: Final[frozenset[str]] = frozenset(
    {
        "candidate_compatible",
        "candidate_compatible_with_warnings",
        "candidate_blocked",
        "candidate_incompatible",
        "not_reviewed",
    }
)
REQUIRED_TOP_LEVEL_FIELDS: Final[tuple[str, ...]] = (
    "compatibility_packet_id",
    "consumer_packet_family",
    "consumer_name",
    "consumer_repository",
    "consumer_branch_ref",
    "consumer_commit_sha",
    "candidate_export_surface_refs",
    "runtime_symbol_refs",
    "import_surface_expectations",
    "fixture_compatibility_matrix",
    "version_compatibility_metadata",
    "guardian_boundary_compatibility",
    "approval_boundary_compatibility",
    "provider_model_route_boundary_compatibility",
    "consumer_runtime_call_prohibition",
    "no_consumer_repo_mutation_confirmation",
    "no_live_import_call_confirmation",
    "final_public_api_freeze_not_claimed_confirmation",
    "audit_evidence_linkage",
    "proof_not_authority_confirmation",
    "no_raw_content_secret_credential_customer_data_confirmation",
    "no_execution_authority_confirmation",
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
        "final_api_freeze_approved",
        "final_public_api_freeze_claimed",
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
        "scheduled_task_executed",
        "secret_lookup_added",
        "shell_runtime_wired",
        "shell_wired",
        "side_effects_allowed",
        "tool_executed",
    }
)


class V1ConsumerIntegrationCompatibilityError(ValueError):
    """Raised when consumer compatibility metadata fails the V1-G21 boundary."""


def validate_v1_consumer_integration_compatibility_freeze(
    compatibility_metadata: Mapping[str, Any],
) -> dict[str, Any]:
    """Return a deterministic non-executing consumer compatibility record."""

    if not isinstance(compatibility_metadata, Mapping):
        raise V1ConsumerIntegrationCompatibilityError(
            "compatibility_metadata must be a mapping"
        )

    _reject_raw_sensitive_content(compatibility_metadata)
    _reject_runtime_authority_claims(compatibility_metadata)

    for field_name in REQUIRED_TOP_LEVEL_FIELDS:
        if field_name not in compatibility_metadata:
            raise V1ConsumerIntegrationCompatibilityError(f"{field_name} is required")

    compatibility_packet_id = _required_text(
        compatibility_metadata.get("compatibility_packet_id"),
        "compatibility_packet_id",
    )
    consumer_packet_family = _consumer_packet_family(
        compatibility_metadata.get("consumer_packet_family")
    )
    consumer_name = _required_text(
        compatibility_metadata.get("consumer_name"),
        "consumer_name",
    )
    consumer_repository = _required_text(
        compatibility_metadata.get("consumer_repository"),
        "consumer_repository",
    )
    consumer_branch_ref = _required_text(
        compatibility_metadata.get("consumer_branch_ref"),
        "consumer_branch_ref",
    )
    consumer_commit_sha = _commit_sha(
        compatibility_metadata.get("consumer_commit_sha"),
        "consumer_commit_sha",
    )
    candidate_export_surface_refs = _string_sequence(
        compatibility_metadata.get("candidate_export_surface_refs"),
        "candidate_export_surface_refs",
        allow_empty=False,
    )
    runtime_symbol_refs = _string_sequence(
        compatibility_metadata.get("runtime_symbol_refs"),
        "runtime_symbol_refs",
        allow_empty=False,
    )
    import_surface = _validate_import_surface_expectations(
        compatibility_metadata.get("import_surface_expectations")
    )
    fixture_matrix = _validate_fixture_compatibility_matrix(
        compatibility_metadata.get("fixture_compatibility_matrix")
    )
    version_compatibility = _validate_version_compatibility(
        compatibility_metadata.get("version_compatibility_metadata")
    )
    guardian_boundary = _validate_boundary_compatibility(
        compatibility_metadata.get("guardian_boundary_compatibility"),
        "guardian_boundary_compatibility",
    )
    approval_boundary = _validate_boundary_compatibility(
        compatibility_metadata.get("approval_boundary_compatibility"),
        "approval_boundary_compatibility",
    )
    provider_model_boundary = _validate_boundary_compatibility(
        compatibility_metadata.get("provider_model_route_boundary_compatibility"),
        "provider_model_route_boundary_compatibility",
    )
    runtime_prohibition = _validate_consumer_runtime_call_prohibition(
        compatibility_metadata.get("consumer_runtime_call_prohibition")
    )
    _require_true_confirmation(
        compatibility_metadata.get("no_consumer_repo_mutation_confirmation"),
        "no_consumer_repo_mutation_confirmation",
    )
    _require_true_confirmation(
        compatibility_metadata.get("no_live_import_call_confirmation"),
        "no_live_import_call_confirmation",
    )
    _require_true_confirmation(
        compatibility_metadata.get("final_public_api_freeze_not_claimed_confirmation"),
        "final_public_api_freeze_not_claimed_confirmation",
    )
    audit_linkage = _validate_audit_linkage(
        compatibility_metadata.get("audit_evidence_linkage")
    )
    _require_true_confirmation(
        compatibility_metadata.get("proof_not_authority_confirmation"),
        "proof_not_authority_confirmation",
    )
    _require_true_confirmation(
        compatibility_metadata.get(
            "no_raw_content_secret_credential_customer_data_confirmation"
        ),
        "no_raw_content_secret_credential_customer_data_confirmation",
    )
    _require_true_confirmation(
        compatibility_metadata.get("no_execution_authority_confirmation"),
        "no_execution_authority_confirmation",
    )

    record = {
        "record_type": "v1_consumer_integration_compatibility_freeze",
        "schema_version": SCHEMA_VERSION,
        "compatibility_packet_id": compatibility_packet_id,
        "consumer_packet_family": consumer_packet_family,
        "consumer_name": consumer_name,
        "consumer_repository": consumer_repository,
        "consumer_branch_ref": consumer_branch_ref,
        "consumer_commit_sha": consumer_commit_sha,
        "candidate_export_surface_refs": list(candidate_export_surface_refs),
        "runtime_symbol_refs": list(runtime_symbol_refs),
        "import_surface_expectations": import_surface,
        "fixture_compatibility_matrix": fixture_matrix,
        "version_compatibility_metadata": version_compatibility,
        "guardian_boundary_compatibility": guardian_boundary,
        "approval_boundary_compatibility": approval_boundary,
        "provider_model_route_boundary_compatibility": provider_model_boundary,
        "consumer_runtime_call_prohibition": runtime_prohibition,
        "audit_evidence_linkage": audit_linkage,
        "capability_open": True,
        "authority_gated": True,
        "consumer_integration_compatibility_freeze_runtime_behavior": True,
        "compatibility_metadata_only": True,
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
        "final_api_freeze_approved": False,
        "runtime_export_cleanup_approved": False,
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
            "v1_runtime_slice": "consumer_integration_compatibility_freeze",
            "candidate_only": True,
            "non_executing": True,
            "proof_not_authority": True,
        },
    }
    record["record_hash"] = _record_hash(record)
    return record


def _validate_import_surface_expectations(value: Any) -> dict[str, Any]:
    surface = _mapping(value, "import_surface_expectations")
    expected_import_refs = _string_sequence(
        surface.get("expected_import_refs"),
        "import_surface_expectations.expected_import_refs",
        allow_empty=False,
    )
    expected_call_shape_refs = _string_sequence(
        surface.get("expected_call_shape_refs"),
        "import_surface_expectations.expected_call_shape_refs",
        allow_empty=False,
    )
    if surface.get("metadata_only") is not True:
        raise V1ConsumerIntegrationCompatibilityError(
            "import surface expectations must be metadata only"
        )
    if surface.get("live_import_performed") is not False:
        raise V1ConsumerIntegrationCompatibilityError(
            "live consumer imports are not approved"
        )
    if surface.get("live_call_performed") is not False:
        raise V1ConsumerIntegrationCompatibilityError(
            "consumer runtime calls are not approved"
        )
    if surface.get("consumer_code_imported") is not False:
        raise V1ConsumerIntegrationCompatibilityError(
            "consumer code imports are not approved"
        )
    if surface.get("grants_runtime_authority") is not False:
        raise V1ConsumerIntegrationCompatibilityError(
            "compatibility metadata cannot grant runtime authority"
        )
    return {
        "expected_import_refs": list(expected_import_refs),
        "expected_call_shape_refs": list(expected_call_shape_refs),
        "metadata_only": True,
        "live_import_performed": False,
        "live_call_performed": False,
        "consumer_code_imported": False,
        "grants_runtime_authority": False,
    }


def _validate_fixture_compatibility_matrix(value: Any) -> dict[str, Any]:
    matrix = _mapping(value, "fixture_compatibility_matrix")
    matrix_ref = _required_text(
        matrix.get("matrix_ref"),
        "fixture_compatibility_matrix.matrix_ref",
    )
    fixture_refs = _string_sequence(
        matrix.get("fixture_refs"),
        "fixture_compatibility_matrix.fixture_refs",
        allow_empty=False,
    )
    compatibility_status = _compatibility_status(
        matrix.get("compatibility_status"),
        "fixture_compatibility_matrix.compatibility_status",
    )
    if matrix.get("raw_fixture_content_included") is not False:
        raise V1ConsumerIntegrationCompatibilityError(
            "raw fixture content is not accepted"
        )
    if matrix.get("consumer_runtime_invoked") is not False:
        raise V1ConsumerIntegrationCompatibilityError(
            "consumer runtime calls are not approved"
        )
    return {
        "matrix_ref": matrix_ref,
        "fixture_refs": list(fixture_refs),
        "compatibility_status": compatibility_status,
        "raw_fixture_content_included": False,
        "consumer_runtime_invoked": False,
    }


def _validate_version_compatibility(value: Any) -> dict[str, Any]:
    version = _mapping(value, "version_compatibility_metadata")
    compatibility_version_ref = _required_text(
        version.get("compatibility_version_ref"),
        "version_compatibility_metadata.compatibility_version_ref",
    )
    lima_candidate_version_ref = _required_text(
        version.get("lima_candidate_version_ref"),
        "version_compatibility_metadata.lima_candidate_version_ref",
    )
    consumer_version_ref = _required_text(
        version.get("consumer_version_ref"),
        "version_compatibility_metadata.consumer_version_ref",
    )
    compatibility_status = _compatibility_status(
        version.get("compatibility_status"),
        "version_compatibility_metadata.compatibility_status",
    )
    if version.get("final_api_freeze_claimed") is not False:
        raise V1ConsumerIntegrationCompatibilityError(
            "final public API freeze is not approved"
        )
    return {
        "compatibility_version_ref": compatibility_version_ref,
        "lima_candidate_version_ref": lima_candidate_version_ref,
        "consumer_version_ref": consumer_version_ref,
        "compatibility_status": compatibility_status,
        "final_api_freeze_claimed": False,
    }


def _validate_boundary_compatibility(value: Any, field_name: str) -> dict[str, Any]:
    boundary = _mapping(value, field_name)
    boundary_ref = _required_text(
        boundary.get("boundary_ref"),
        f"{field_name}.boundary_ref",
    )
    if boundary.get("compatible") is not True:
        raise V1ConsumerIntegrationCompatibilityError(
            f"{field_name} compatibility is required"
        )
    if boundary.get("proof_not_authority") is not True:
        raise V1ConsumerIntegrationCompatibilityError(
            f"{field_name} metadata cannot be authority"
        )
    if boundary.get("grants_execution_authority") is not False:
        raise V1ConsumerIntegrationCompatibilityError(
            f"{field_name} cannot grant execution"
        )
    if boundary.get("future_integration_requires_approval") is not True:
        raise V1ConsumerIntegrationCompatibilityError(
            "future integration approval requirement is required"
        )
    return {
        "boundary_ref": boundary_ref,
        "compatible": True,
        "proof_not_authority": True,
        "grants_execution_authority": False,
        "future_integration_requires_approval": True,
    }


def _validate_consumer_runtime_call_prohibition(value: Any) -> dict[str, Any]:
    prohibition = _mapping(value, "consumer_runtime_call_prohibition")
    prohibition_ref = _required_text(
        prohibition.get("prohibition_ref"),
        "consumer_runtime_call_prohibition.prohibition_ref",
    )
    if prohibition.get("non_execution_confirmed") is not True:
        raise V1ConsumerIntegrationCompatibilityError(
            "consumer runtime call prohibition must confirm non-execution"
        )
    if prohibition.get("consumer_runtime_calls_added") is not False:
        raise V1ConsumerIntegrationCompatibilityError(
            "consumer runtime calls are not approved"
        )
    if prohibition.get("live_import_performed") is not False:
        raise V1ConsumerIntegrationCompatibilityError(
            "live consumer imports are not approved"
        )
    if prohibition.get("live_call_performed") is not False:
        raise V1ConsumerIntegrationCompatibilityError(
            "consumer runtime calls are not approved"
        )
    return {
        "prohibition_ref": prohibition_ref,
        "non_execution_confirmed": True,
        "consumer_runtime_calls_added": False,
        "live_import_performed": False,
        "live_call_performed": False,
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
        raise V1ConsumerIntegrationCompatibilityError(
            "audit/evidence linkage is required"
        )
    if audit.get("proof_not_authority") is not True:
        raise V1ConsumerIntegrationCompatibilityError(
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
                raise V1ConsumerIntegrationCompatibilityError(
                    "raw sensitive content is not accepted"
                )
            _reject_raw_sensitive_content(nested)
    elif isinstance(value, (list, tuple, set, frozenset)):
        for nested in value:
            _reject_raw_sensitive_content(nested)
    elif isinstance(value, str):
        folded = value.strip().lower()
        if any(marker in folded for marker in RAW_SENSITIVE_VALUE_MARKERS):
            raise V1ConsumerIntegrationCompatibilityError(
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
                raise V1ConsumerIntegrationCompatibilityError(
                    "compatibility metadata cannot grant runtime authority"
                )
            _reject_runtime_authority_claims(nested)
    elif isinstance(value, (list, tuple, set, frozenset)):
        for nested in value:
            _reject_runtime_authority_claims(nested)


def _consumer_packet_family(value: Any) -> str:
    family = _normalize_token(_required_text(value, "consumer_packet_family"))
    if family not in ALLOWED_CONSUMER_PACKET_FAMILIES:
        raise V1ConsumerIntegrationCompatibilityError(
            "consumer packet family is not allowed"
        )
    return family


def _compatibility_status(value: Any, field_name: str) -> str:
    status = _normalize_token(_required_text(value, field_name))
    if status not in ALLOWED_COMPATIBILITY_STATUSES:
        raise V1ConsumerIntegrationCompatibilityError(
            "compatibility status is not allowed"
        )
    return status


def _commit_sha(value: Any, field_name: str) -> str:
    commit = _required_text(value, field_name).lower()
    if len(commit) < 7 or len(commit) > 64:
        raise V1ConsumerIntegrationCompatibilityError(
            f"{field_name} must be a commit SHA"
        )
    if any(character not in string.hexdigits.lower() for character in commit):
        raise V1ConsumerIntegrationCompatibilityError(
            f"{field_name} must be a commit SHA"
        )
    return commit


def _mapping(value: Any, field_name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping) or not value:
        raise V1ConsumerIntegrationCompatibilityError(f"{field_name} is required")
    return value


def _required_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise V1ConsumerIntegrationCompatibilityError(f"{field_name} is required")
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
        raise V1ConsumerIntegrationCompatibilityError(
            f"{field_name} must be a string sequence"
        )
    normalized = tuple(str(item).strip() for item in value if str(item).strip())
    if not normalized and not allow_empty:
        raise V1ConsumerIntegrationCompatibilityError(f"{field_name} is required")
    return normalized


def _require_true_confirmation(value: Any, field_name: str) -> None:
    if value is True:
        return
    if isinstance(value, Mapping) and value.get("confirmed") is True:
        return
    raise V1ConsumerIntegrationCompatibilityError(
        f"{field_name} confirmation is required"
    )


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
