"""V1 consumer proof packet audit-intake metadata validator.

This module is the approved V1-G18 candidate runtime slice. It validates
sanitized proof-packet metadata received from consumer teams without importing
consumer code, calling consumer runtimes, wiring shells, routing providers, or
performing external actions.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import hashlib
import json
import string
from typing import Any, Final


SCHEMA_VERSION: Final[str] = "v1-g18-candidate"
ALLOWED_CONSUMER_PACKET_FAMILIES: Final[frozenset[str]] = frozenset(
    {"sparkbot", "arc_bot", "lima_robo_os", "lima_office", "future_shell"}
)
NORMALIZED_PACKET_STATUSES: Final[dict[str, str]] = {
    "received": "received",
    "missing": "missing",
    "blocked": "blocked",
    "rejected": "rejected",
    "accepted_static_evidence": "accepted_static_evidence",
    "accepted-static-evidence": "accepted_static_evidence",
    "accepted static evidence": "accepted_static_evidence",
}
REQUIRED_TOP_LEVEL_FIELDS: Final[tuple[str, ...]] = (
    "consumer_packet_family",
    "consumer_name",
    "consumer_repository",
    "consumer_branch_ref",
    "consumer_commit_sha",
    "proof_packet_path",
    "audit_packet_path",
    "machine_readable_summary_path",
    "validation_commands",
    "proposed_import_call_shape_evidence",
    "normalized_metadata_examples",
    "capability_profile_expectations",
    "guardian_approval_boundary_expectations",
    "dry_run_non_execution_confirmation",
    "no_live_consumer_runtime_path_calls_lima",
    "no_bypass_claims",
    "independent_audit_required",
    "packet_status",
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
    "api key",
)
FORBIDDEN_TRUE_CLAIM_KEYS: Final[frozenset[str]] = frozenset(
    {
        "approval_token_issued",
        "browser_action_executed",
        "connector_invoked",
        "consumer_code_imported",
        "consumer_integration_added",
        "consumer_repo_mutation_added",
        "consumer_runtime_called",
        "consumer_runtime_calls_added",
        "consumer_runtime_invoked",
        "device_command_invoked",
        "drone_control_invoked",
        "execution_allowed",
        "external_send_added",
        "file_mutation_executed",
        "final_api_freeze_approved",
        "humaninput_bridge_activated",
        "iot_control_invoked",
        "live_call_performed",
        "live_import_performed",
        "model_routed",
        "network_action_executed",
        "physical_world_invoked",
        "product_ready",
        "provider_model_routed",
        "robot_control_invoked",
        "robotics_invoked",
        "scheduled_task_executed",
        "shell_runtime_wired",
        "shell_wired",
        "side_effects_allowed",
        "tool_executed",
    }
)


class V1ConsumerProofPacketIntakeError(ValueError):
    """Raised when proof-packet intake metadata fails the V1-G18 boundary."""


def validate_v1_consumer_proof_packet_intake(
    packet_metadata: Mapping[str, Any],
) -> dict[str, Any]:
    """Return a deterministic non-executing proof-packet audit-intake record."""

    if not isinstance(packet_metadata, Mapping):
        raise V1ConsumerProofPacketIntakeError("packet_metadata must be a mapping")

    _reject_raw_sensitive_content(packet_metadata)
    _reject_runtime_authority_claims(packet_metadata)

    for field_name in REQUIRED_TOP_LEVEL_FIELDS:
        if field_name not in packet_metadata:
            raise V1ConsumerProofPacketIntakeError(f"{field_name} is required")

    consumer_packet_family = _consumer_packet_family(
        packet_metadata.get("consumer_packet_family")
    )
    consumer_name = _required_text(packet_metadata.get("consumer_name"), "consumer_name")
    consumer_repository = _required_text(
        packet_metadata.get("consumer_repository"),
        "consumer_repository",
    )
    consumer_branch_ref = _required_text(
        packet_metadata.get("consumer_branch_ref"),
        "consumer_branch_ref",
    )
    consumer_commit_sha = _commit_sha(
        packet_metadata.get("consumer_commit_sha"),
        "consumer_commit_sha",
    )
    proof_packet_path = _metadata_path(
        packet_metadata.get("proof_packet_path"),
        "proof_packet_path",
    )
    audit_packet_path = _metadata_path(
        packet_metadata.get("audit_packet_path"),
        "audit_packet_path",
    )
    machine_readable_summary_path = _metadata_path(
        packet_metadata.get("machine_readable_summary_path"),
        "machine_readable_summary_path",
    )
    validation_commands = _validate_validation_commands(
        packet_metadata.get("validation_commands")
    )
    import_call_shape = _validate_import_call_shape(
        packet_metadata.get("proposed_import_call_shape_evidence")
    )
    normalized_examples = _validate_normalized_examples(
        packet_metadata.get("normalized_metadata_examples")
    )
    capability_profile = _validate_capability_profile(
        packet_metadata.get("capability_profile_expectations")
    )
    guardian_boundary = _validate_guardian_boundary(
        packet_metadata.get("guardian_approval_boundary_expectations")
    )
    non_execution = _validate_non_execution_confirmation(
        packet_metadata.get("dry_run_non_execution_confirmation")
    )
    _require_true_confirmation(
        packet_metadata.get("no_live_consumer_runtime_path_calls_lima"),
        "no_live_consumer_runtime_path_calls_lima",
    )
    _require_true_confirmation(packet_metadata.get("no_bypass_claims"), "no_bypass_claims")
    _require_true_confirmation(
        packet_metadata.get("independent_audit_required"),
        "independent_audit_required",
    )
    packet_status = _packet_status(packet_metadata.get("packet_status"))

    record = {
        "record_type": "v1_consumer_proof_packet_audit_intake",
        "schema_version": SCHEMA_VERSION,
        "consumer_packet_family": consumer_packet_family,
        "consumer_name": consumer_name,
        "consumer_repository": consumer_repository,
        "consumer_branch_ref": consumer_branch_ref,
        "consumer_commit_sha": consumer_commit_sha,
        "proof_packet_path": proof_packet_path,
        "audit_packet_path": audit_packet_path,
        "machine_readable_summary_path": machine_readable_summary_path,
        "packet_status": packet_status,
        "validation_commands": validation_commands,
        "proposed_import_call_shape_evidence": import_call_shape,
        "normalized_metadata_examples": normalized_examples,
        "capability_profile_expectations": capability_profile,
        "guardian_approval_boundary_expectations": guardian_boundary,
        "dry_run_non_execution_confirmation": non_execution,
        "status_ledger_record": {
            "ledger_record_type": "v1_consumer_proof_packet_status",
            "consumer_packet_family": consumer_packet_family,
            "consumer_name": consumer_name,
            "consumer_repository": consumer_repository,
            "consumer_branch_ref": consumer_branch_ref,
            "consumer_commit_sha": consumer_commit_sha,
            "packet_status": packet_status,
            "status_recorded": True,
            "proof_not_authority": True,
        },
        "capability_open": True,
        "authority_gated": True,
        "consumer_proof_packet_audit_intake_runtime_behavior": True,
        "proof_not_authority": True,
        "dry_run_only": True,
        "non_executing": True,
        "redacted_metadata_only": True,
        "execution_allowed": False,
        "side_effects_allowed": False,
        "consumer_repo_mutation_added": False,
        "consumer_integration_added": False,
        "consumer_runtime_calls_added": False,
        "consumer_code_imported": False,
        "consumer_runtime_called": False,
        "provider_model_routed": False,
        "tool_executed": False,
        "connector_invoked": False,
        "browser_action_executed": False,
        "network_action_executed": False,
        "file_mutation_executed": False,
        "scheduled_task_executed": False,
        "external_send_added": False,
        "device_command_invoked": False,
        "robot_control_invoked": False,
        "drone_control_invoked": False,
        "iot_control_invoked": False,
        "physical_world_invoked": False,
        "approval_token_issued": False,
        "raw_pin_verified": False,
        "raw_sensitive_content_persisted": False,
        "final_api_freeze_approved": False,
        "product_ready": False,
        "metadata": {
            "v1_runtime_slice": "consumer_proof_packet_audit_intake",
            "candidate_only": True,
            "non_executing": True,
            "proof_not_authority": True,
        },
    }
    record["record_hash"] = _record_hash(record)
    return record


def _validate_validation_commands(value: Any) -> list[dict[str, Any]]:
    commands = _mapping_sequence(value, "validation_commands")
    normalized: list[dict[str, Any]] = []
    for index, command in enumerate(commands):
        prefix = f"validation_commands[{index}]"
        command_ref = _required_text(command.get("command_ref"), f"{prefix}.command_ref")
        command_name = _required_text(command.get("command"), f"{prefix}.command")
        reported_result = _required_text(
            command.get("reported_result"),
            f"{prefix}.reported_result",
        ).lower()
        if reported_result not in {"pass", "pass_with_warnings", "fail", "not_run", "blocked"}:
            raise V1ConsumerProofPacketIntakeError(
                f"{prefix}.reported_result is not allowed"
            )
        normalized.append(
            {
                "command_ref": command_ref,
                "command": command_name,
                "reported_result": reported_result,
            }
        )
    return normalized


def _validate_import_call_shape(value: Any) -> dict[str, Any]:
    shape = _mapping(value, "proposed_import_call_shape_evidence")
    evidence_ref = _required_text(
        shape.get("evidence_ref"),
        "proposed_import_call_shape_evidence.evidence_ref",
    )
    proposed_import_shape = _required_text(
        shape.get("proposed_import_shape"),
        "proposed_import_call_shape_evidence.proposed_import_shape",
    )
    proposed_call_shape = _required_text(
        shape.get("proposed_call_shape"),
        "proposed_import_call_shape_evidence.proposed_call_shape",
    )
    if shape.get("evidence_only") is not True:
        raise V1ConsumerProofPacketIntakeError("import/call shape must be evidence only")
    if shape.get("live_import_performed") is not False:
        raise V1ConsumerProofPacketIntakeError("consumer imports are not approved")
    if shape.get("live_call_performed") is not False:
        raise V1ConsumerProofPacketIntakeError("consumer runtime calls are not approved")
    if shape.get("grants_runtime_authority") is not False:
        raise V1ConsumerProofPacketIntakeError("proof metadata cannot grant authority")
    return {
        "evidence_ref": evidence_ref,
        "proposed_import_shape": proposed_import_shape,
        "proposed_call_shape": proposed_call_shape,
        "evidence_only": True,
        "live_import_performed": False,
        "live_call_performed": False,
        "grants_runtime_authority": False,
    }


def _validate_normalized_examples(value: Any) -> dict[str, Any]:
    examples = _mapping(value, "normalized_metadata_examples")
    if examples.get("examples_present") is not True:
        raise V1ConsumerProofPacketIntakeError("normalized metadata examples are required")
    if examples.get("redacted") is not True:
        raise V1ConsumerProofPacketIntakeError("normalized metadata examples must be redacted")
    if examples.get("raw_content_included") is not False:
        raise V1ConsumerProofPacketIntakeError("raw content is not accepted")
    example_refs = _string_sequence(
        examples.get("example_refs"),
        "normalized_metadata_examples.example_refs",
    )
    if not example_refs:
        raise V1ConsumerProofPacketIntakeError("normalized metadata example refs are required")
    return {
        "examples_present": True,
        "redacted": True,
        "raw_content_included": False,
        "example_refs": list(example_refs),
    }


def _validate_capability_profile(value: Any) -> dict[str, Any]:
    profile = _mapping(value, "capability_profile_expectations")
    profile_ref = _required_text(
        profile.get("capability_profile_ref"),
        "capability_profile_expectations.capability_profile_ref",
    )
    if profile.get("expectations_declared") is not True:
        raise V1ConsumerProofPacketIntakeError("capability expectations are required")
    if profile.get("execution_authority_granted") is not False:
        raise V1ConsumerProofPacketIntakeError("capability profile cannot grant execution")
    if profile.get("future_integration_requires_approval") is not True:
        raise V1ConsumerProofPacketIntakeError(
            "future integration approval requirement is required"
        )
    tool_packs = _string_sequence(
        profile.get("expected_tool_packs"),
        "capability_profile_expectations.expected_tool_packs",
    )
    return {
        "capability_profile_ref": profile_ref,
        "expectations_declared": True,
        "expected_tool_packs": list(tool_packs),
        "execution_authority_granted": False,
        "future_integration_requires_approval": True,
    }


def _validate_guardian_boundary(value: Any) -> dict[str, Any]:
    boundary = _mapping(value, "guardian_approval_boundary_expectations")
    boundary_ref = _required_text(
        boundary.get("boundary_ref"),
        "guardian_approval_boundary_expectations.boundary_ref",
    )
    if boundary.get("guardian_required") is not True:
        raise V1ConsumerProofPacketIntakeError("Guardian boundary is required")
    if boundary.get("approval_boundary_declared") is not True:
        raise V1ConsumerProofPacketIntakeError("approval boundary is required")
    if boundary.get("proof_not_authority") is not True:
        raise V1ConsumerProofPacketIntakeError("proof metadata cannot be authority")
    if boundary.get("execution_authority_granted") is not False:
        raise V1ConsumerProofPacketIntakeError("Guardian boundary cannot grant execution")
    if boundary.get("future_integration_requires_approval") is not True:
        raise V1ConsumerProofPacketIntakeError(
            "future integration approval requirement is required"
        )
    return {
        "boundary_ref": boundary_ref,
        "guardian_required": True,
        "approval_boundary_declared": True,
        "proof_not_authority": True,
        "execution_authority_granted": False,
        "future_integration_requires_approval": True,
    }


def _validate_non_execution_confirmation(value: Any) -> dict[str, Any]:
    confirmation = _mapping(value, "dry_run_non_execution_confirmation")
    confirmation_ref = _required_text(
        confirmation.get("confirmation_ref"),
        "dry_run_non_execution_confirmation.confirmation_ref",
    )
    if confirmation.get("dry_run") is not True:
        raise V1ConsumerProofPacketIntakeError("dry-run confirmation is required")
    if confirmation.get("non_execution_confirmed") is not True:
        raise V1ConsumerProofPacketIntakeError("non-execution confirmation is required")
    if confirmation.get("no_side_effects_confirmed") is not True:
        raise V1ConsumerProofPacketIntakeError("no-side-effects confirmation is required")
    if confirmation.get("consumer_runtime_invoked") is not False:
        raise V1ConsumerProofPacketIntakeError("consumer runtime calls are not approved")
    return {
        "confirmation_ref": confirmation_ref,
        "dry_run": True,
        "non_execution_confirmed": True,
        "no_side_effects_confirmed": True,
        "consumer_runtime_invoked": False,
    }


def _reject_raw_sensitive_content(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            if isinstance(key, str) and key.strip().lower() in RAW_SENSITIVE_KEYS:
                raise V1ConsumerProofPacketIntakeError(
                    "raw sensitive content is not accepted"
                )
            _reject_raw_sensitive_content(nested)
    elif isinstance(value, (list, tuple, set, frozenset)):
        for nested in value:
            _reject_raw_sensitive_content(nested)
    elif isinstance(value, str):
        folded = value.strip().lower()
        if any(marker in folded for marker in RAW_SENSITIVE_VALUE_MARKERS):
            raise V1ConsumerProofPacketIntakeError(
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
                raise V1ConsumerProofPacketIntakeError(
                    "proof packet metadata cannot grant runtime authority"
                )
            _reject_runtime_authority_claims(nested)
    elif isinstance(value, (list, tuple, set, frozenset)):
        for nested in value:
            _reject_runtime_authority_claims(nested)


def _consumer_packet_family(value: Any) -> str:
    family = _required_text(value, "consumer_packet_family").lower().replace("-", "_")
    if family not in ALLOWED_CONSUMER_PACKET_FAMILIES:
        raise V1ConsumerProofPacketIntakeError("consumer packet family is not allowed")
    return family


def _packet_status(value: Any) -> str:
    status = _required_text(value, "packet_status").lower().replace("-", "_")
    if status not in NORMALIZED_PACKET_STATUSES:
        raise V1ConsumerProofPacketIntakeError("packet status is not allowed")
    return NORMALIZED_PACKET_STATUSES[status]


def _commit_sha(value: Any, field_name: str) -> str:
    commit = _required_text(value, field_name).lower()
    if len(commit) < 7 or len(commit) > 64:
        raise V1ConsumerProofPacketIntakeError(f"{field_name} must be a commit SHA")
    if any(character not in string.hexdigits.lower() for character in commit):
        raise V1ConsumerProofPacketIntakeError(f"{field_name} must be a commit SHA")
    return commit


def _metadata_path(value: Any, field_name: str) -> str:
    path = _required_text(value, field_name).replace("\\", "/").strip()
    while path.startswith("./"):
        path = path[2:]
    if not path:
        raise V1ConsumerProofPacketIntakeError(f"{field_name} is required")
    if path.startswith("/") or path.startswith("~") or path.startswith("//"):
        raise V1ConsumerProofPacketIntakeError("absolute or home paths are not allowed")
    if len(path) >= 2 and path[1] == ":":
        raise V1ConsumerProofPacketIntakeError("absolute or drive paths are not allowed")
    segments = [segment for segment in path.split("/") if segment]
    if any(segment == ".." for segment in segments):
        raise V1ConsumerProofPacketIntakeError("path traversal is not allowed")
    return "/".join(segments)


def _mapping(value: Any, field_name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping) or not value:
        raise V1ConsumerProofPacketIntakeError(f"{field_name} is required")
    return value


def _mapping_sequence(value: Any, field_name: str) -> tuple[Mapping[str, Any], ...]:
    if (
        not isinstance(value, Sequence)
        or isinstance(value, (str, bytes, bytearray))
        or not value
    ):
        raise V1ConsumerProofPacketIntakeError(f"{field_name} is required")
    if not all(isinstance(item, Mapping) and item for item in value):
        raise V1ConsumerProofPacketIntakeError(f"{field_name} must contain mappings")
    return tuple(value)


def _required_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise V1ConsumerProofPacketIntakeError(f"{field_name} is required")
    return value.strip()


def _string_sequence(value: Any, field_name: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        value = (value,)
    if not isinstance(value, Sequence) or isinstance(value, (bytes, bytearray)):
        raise V1ConsumerProofPacketIntakeError(f"{field_name} must be a string sequence")
    return tuple(str(item).strip() for item in value if str(item).strip())


def _require_true_confirmation(value: Any, field_name: str) -> None:
    if value is True:
        return
    if isinstance(value, Mapping) and value.get("confirmed") is True:
        return
    raise V1ConsumerProofPacketIntakeError(f"{field_name} confirmation is required")


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
