"""V1 live provider/model call execution harness.

This module is the approved V1-G46 candidate runtime slice. It invokes only a
caller-injected provider executor after validating V1-G44 authority evidence,
redaction policy, approval linkage, and execution boundaries. It contains no
provider SDK clients, direct network client code, ambient secret lookup,
credential value access, fallback execution, tools, connectors, or consumer
repository integration.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
import hashlib
import json
from typing import Any, Final
from urllib.parse import urlsplit

from lima.contracts.guardian import GuardianDecision, GuardianDecisionStatus


SCHEMA_VERSION: Final[str] = "v1-g46-candidate"
AUTHORITY_SCHEMA_VERSION: Final[str] = "v1-g44-candidate"
ALLOWED_FINISH_STATUSES: Final[frozenset[str]] = frozenset(
    {"completed", "blocked", "failed", "cancelled"}
)
ARC_EXECUTOR_KIND_FAKE: Final[str] = "fake"
ARC_EXECUTOR_KIND_LOOPBACK_OLLAMA: Final[str] = "loopback_ollama"
ARC_EXECUTOR_KINDS: Final[frozenset[str]] = frozenset(
    {ARC_EXECUTOR_KIND_FAKE, ARC_EXECUTOR_KIND_LOOPBACK_OLLAMA}
)
LEGACY_FAKE_EXECUTOR_REFS: Final[frozenset[str]] = frozenset(
    {
        "in_process_fake_executor",
        "provider-executor:v1-g46:fake-openai",
    }
)
LOOPBACK_OLLAMA_HOSTS: Final[frozenset[str]] = frozenset(
    {"127.0.0.1", "localhost"}
)
LOOPBACK_OLLAMA_ERROR_CATEGORIES: Final[frozenset[str]] = frozenset(
    {
        "service_unavailable",
        "model_unavailable",
        "timeout",
        "malformed_response",
        "executor_error",
    }
)
REQUIRED_EXECUTION_FIELDS: Final[tuple[str, ...]] = (
    'guardian_decision',
    "execution_id",
    "authority_record",
    "provider_executor_ref",
    "provider_request_ref",
    "redacted_prompt_ref",
    "redacted_input_summary_ref",
    "execution_approval_linkage",
    "audit_evidence_linkage",
    "redaction_policy",
    "execution_boundary",
    "provider_executor_injected_confirmation",
    "no_direct_provider_sdk_confirmation",
    "no_direct_network_code_confirmation",
    "no_ambient_secret_lookup_confirmation",
    "no_credential_value_access_confirmation",
    "no_fallback_execution_confirmation",
    "no_raw_prompt_model_response_customer_data_persistence_confirmation",
)
RAW_SENSITIVE_KEYS: Final[frozenset[str]] = frozenset(
    {
        "api_key",
        "bearer_token",
        "credential",
        "credentials",
        "customer_data",
        "message_text",
        "model_response",
        "oauth_token",
        "output_text",
        "password",
        "prompt",
        "prompt_text",
        "provider_api_key",
        "provider_credentials",
        "provider_token",
        "raw_customer_context",
        "raw_customer_data",
        "raw_model_response",
        "raw_output",
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
    "api key",
    "bearer token",
    "model response text",
    "provider credential",
    "provider token",
    "raw customer context",
    "raw customer data",
    "raw model response",
    "raw prompt",
    "raw secret",
    "raw-secret-",
    "secret value",
)
FORBIDDEN_TRUE_CLAIM_KEYS: Final[frozenset[str]] = frozenset(
    {
        "ambient_environment_secret_lookup_added",
        "ambient_secret_lookup_performed",
        "browser_action_executed",
        "connector_invoked",
        "consumer_code_imported",
        "consumer_integration_added",
        "consumer_repo_mutation_added",
        "consumer_runtime_called",
        "consumer_runtime_calls_added",
        "credential_access_added",
        "credential_accessed",
        "credential_value_access_added",
        "credential_value_accessed",
        "device_command_invoked",
        "direct_network_client_added",
        "direct_network_code_added",
        "direct_network_code_used",
        "direct_provider_sdk_added",
        "direct_provider_sdk_used",
        "drone_control_invoked",
        "external_send_added",
        "fallback_executed",
        "fallback_execution_added",
        "fallback_execution_allowed",
        "file_mutation_executed",
        "humaninput_bridge_activated",
        "iot_control_invoked",
        "physical_world_invoked",
        "product_ready",
        "provider_readiness_check_performed",
        "provider_readiness_network_check_added",
        "provider_readiness_network_check_allowed",
        "raw_customer_data_persisted",
        "raw_diff_or_patch_persisted",
        "raw_file_content_persisted",
        "raw_model_response_persisted",
        "raw_prompt_persisted",
        "raw_sensitive_content_persisted",
        "robot_control_invoked",
        "robotics_invoked",
        "scheduled_task_executed",
        "secret_lookup_added",
        "secret_lookup_performed",
        "shell_runtime_wired",
        "token_guardian_live_routing_added",
        "tool_executed",
        "tool_execution_added",
    }
)
AUTHORITY_FALSE_FIELDS: Final[tuple[str, ...]] = (
    "live_provider_model_call_execution_added",
    "actual_model_request_dispatch_execution_added",
    "model_request_dispatched",
    "network_call_added",
    "network_call_performed",
    "provider_readiness_network_check_added",
    "token_guardian_live_routing_added",
    "secret_lookup_added",
    "credential_value_access_added",
    "credential_access_added",
    "fallback_execution_added",
    "fallback_executed",
    "tool_executed",
    "consumer_repo_mutation_added",
    "consumer_code_imported",
    "consumer_runtime_calls_added",
    "consumer_integration_added",
    "connector_invoked",
    "physical_world_invoked",
    "product_ready",
)


class V1LiveProviderModelCallExecutionError(ValueError):
    """Raised when V1-G46 live provider/model execution is not authorized."""


def execute_v1_live_provider_model_call(
    execution_request: Mapping[str, Any],
    provider_executor: Callable[[Mapping[str, Any]], Mapping[str, Any]],
) -> dict[str, Any]:
    """Execute one bounded provider/model call through an injected executor.

    The returned record is sanitized evidence. Raw prompts, raw model
    responses, customer data, secrets, credentials, provider tokens, and API
    keys are never included in the returned record.
    """

    if not isinstance(execution_request, Mapping):
        raise V1LiveProviderModelCallExecutionError(
            "execution_request must be a mapping"
        )
    if not callable(provider_executor):
        raise V1LiveProviderModelCallExecutionError(
            "provider_executor must be injected and callable"
        )

    _reject_raw_sensitive_content(execution_request)
    _reject_forbidden_claims(execution_request)

    if execution_request.get('runtime_consumer') == 'arc_bot_shell':
        return _execute_arc_consumer_baseline(execution_request, provider_executor)

    guardian_decision = _validate_guardian_decision(
        execution_request.get('guardian_decision')
    )

    for field_name in REQUIRED_EXECUTION_FIELDS:
        if field_name not in execution_request:
            raise V1LiveProviderModelCallExecutionError(f"{field_name} is required")

    execution_id = _required_text(execution_request.get("execution_id"), "execution_id")
    authority = _validate_authority_record(execution_request.get("authority_record"))
    if authority['guardian_decision_id'] != guardian_decision['decision_id']:
        raise V1LiveProviderModelCallExecutionError(
            'Guardian decision_id does not match authority lineage'
        )
    provider_executor_ref = _required_text(
        execution_request.get("provider_executor_ref"),
        "provider_executor_ref",
    )
    executor_kind = _resolve_executor_kind(
        execution_request,
        provider_executor_ref,
    )
    if executor_kind != ARC_EXECUTOR_KIND_FAKE:
        raise V1LiveProviderModelCallExecutionError(
            "unsupported executor_kind for the V1-G46 provider path"
        )
    provider_request_ref = _required_text(
        execution_request.get("provider_request_ref"),
        "provider_request_ref",
    )
    redacted_prompt_ref = _required_text(
        execution_request.get("redacted_prompt_ref"),
        "redacted_prompt_ref",
    )
    redacted_input_summary_ref = _required_text(
        execution_request.get("redacted_input_summary_ref"),
        "redacted_input_summary_ref",
    )
    approval_linkage = _validate_execution_approval_linkage(
        execution_request.get("execution_approval_linkage")
    )
    audit_linkage = _validate_audit_linkage(
        execution_request.get("audit_evidence_linkage")
    )
    redaction_policy = _validate_redaction_policy(
        execution_request.get("redaction_policy")
    )
    execution_boundary = _validate_execution_boundary(
        execution_request.get("execution_boundary")
    )

    _require_true_confirmation(
        execution_request.get("provider_executor_injected_confirmation"),
        "provider_executor_injected_confirmation",
    )
    _require_true_confirmation(
        execution_request.get("no_direct_provider_sdk_confirmation"),
        "no_direct_provider_sdk_confirmation",
    )
    _require_true_confirmation(
        execution_request.get("no_direct_network_code_confirmation"),
        "no_direct_network_code_confirmation",
    )
    _require_true_confirmation(
        execution_request.get("no_ambient_secret_lookup_confirmation"),
        "no_ambient_secret_lookup_confirmation",
    )
    _require_true_confirmation(
        execution_request.get("no_credential_value_access_confirmation"),
        "no_credential_value_access_confirmation",
    )
    _require_true_confirmation(
        execution_request.get("no_fallback_execution_confirmation"),
        "no_fallback_execution_confirmation",
    )
    _require_true_confirmation(
        execution_request.get(
            "no_raw_prompt_model_response_customer_data_persistence_confirmation"
        ),
        "no_raw_prompt_model_response_customer_data_persistence_confirmation",
    )

    executor_payload = {
        'guardian_decision': dict(guardian_decision),
        'guardian_decision_id': guardian_decision['decision_id'],
        "execution_id": execution_id,
        "authority_id": authority["authority_id"],
        "authority_record_hash": authority["record_hash"],
        "provider_id": authority["provider_id"],
        "model_id": authority["model_id"],
        "model_role": authority["model_role"],
        "provider_executor_ref": provider_executor_ref,
        "provider_request_ref": provider_request_ref,
        "redacted_prompt_ref": redacted_prompt_ref,
        "redacted_input_summary_ref": redacted_input_summary_ref,
        "redaction_policy_ref": redaction_policy["redaction_policy_ref"],
        "audit_record_ref": audit_linkage["audit_record_ref"],
        "data_sensitivity": authority["data_sensitivity"],
        "budget_class": authority["budget_class"],
        "estimated_cost_class": authority["estimated_cost_class"],
        "latency_tier": authority["latency_tier"],
    }

    try:
        provider_result = provider_executor(executor_payload)
    except Exception as exc:  # pragma: no cover - exact exception type is caller-owned.
        raise V1LiveProviderModelCallExecutionError(
            "provider executor failed"
        ) from exc

    result = _validate_provider_result(provider_result)

    record = {
        'guardian_decision': dict(guardian_decision),
        'guardian_decision_id': guardian_decision['decision_id'],
        "record_type": "v1_live_provider_model_call_execution",
        "schema_version": SCHEMA_VERSION,
        "execution_id": execution_id,
        "authority_id": authority["authority_id"],
        "authority_record_hash": authority["record_hash"],
        "provider_id": authority["provider_id"],
        "model_id": authority["model_id"],
        "model_role": authority["model_role"],
        "provider_executor_ref": provider_executor_ref,
        "provider_request_ref": provider_request_ref,
        "redacted_prompt_ref": redacted_prompt_ref,
        "redacted_input_summary_ref": redacted_input_summary_ref,
        "provider_call_id": result["provider_call_id"],
        "provider_output_ref": result["output_ref"],
        "redacted_output_summary_ref": result["redacted_output_summary_ref"],
        "finish_status": result["finish_status"],
        "usage_metadata": result["usage_metadata"],
        "execution_approval_linkage": approval_linkage,
        "audit_evidence_linkage": audit_linkage,
        "redaction_policy": redaction_policy,
        "execution_boundary": execution_boundary,
        "capability_open": True,
        "authority_gated": True,
        "live_provider_model_call_execution_added": True,
        "provider_executor_invocation_added": True,
        "provider_executor_invoked": True,
        "actual_model_request_dispatch_execution_added": True,
        "model_request_dispatched": True,
        "direct_provider_sdk_added": False,
        "direct_provider_sdk_used": False,
        "direct_network_code_added": False,
        "direct_network_code_used": False,
        "network_call_performed_by_lima_harness": False,
        "provider_readiness_network_check_added": False,
        "token_guardian_live_routing_added": False,
        "secret_lookup_added": False,
        "credential_value_access_added": False,
        "credential_access_added": False,
        "fallback_execution_added": False,
        "fallback_executed": False,
        "tool_execution_added": False,
        "tool_executed": False,
        "action_executed": False,
        "file_mutation_executed": False,
        "consumer_repo_mutation_added": False,
        "consumer_code_imported": False,
        "consumer_runtime_calls_added": False,
        "consumer_integration_added": False,
        "shell_runtime_wired": False,
        "connector_invoked": False,
        "browser_action_executed": False,
        "network_action_executed": False,
        "scheduled_task_executed": False,
        "external_send_added": False,
        "device_command_invoked": False,
        "robot_control_invoked": False,
        "drone_control_invoked": False,
        "iot_control_invoked": False,
        "physical_world_invoked": False,
        "raw_prompt_persisted": False,
        "raw_model_response_persisted": False,
        "raw_customer_data_persisted": False,
        "raw_sensitive_content_persisted": False,
        "product_ready": False,
        "metadata": {
            "v1_runtime_slice": "live_provider_model_call_execution",
            "candidate_only": True,
            "provider_executor_injected": True,
            "sanitized_evidence_only": True,
        },
    }
    _reject_raw_sensitive_content(record)
    record["record_hash"] = _record_hash(record)
    return record


def _execute_arc_consumer_baseline(
    runtime_request: Mapping[str, Any],
    executor: Callable[[Mapping[str, Any]], Mapping[str, Any]],
) -> dict[str, Any]:
    required_fields = (
        'request_id',
        'runtime_consumer',
        'requested_action',
        'guardian_decision',
        'executor_ref',
        'normalized_request',
    )
    for field_name in required_fields:
        if field_name not in runtime_request:
            raise V1LiveProviderModelCallExecutionError(f'{field_name} is required')

    request_id = _required_text(runtime_request.get('request_id'), 'request_id')
    if runtime_request.get('runtime_consumer') != 'arc_bot_shell':
        raise V1LiveProviderModelCallExecutionError('unsupported runtime consumer')
    if runtime_request.get('requested_action') != 'arc.local_model_preview':
        raise V1LiveProviderModelCallExecutionError('unsupported requested action')
    guardian_decision = _validate_guardian_decision(
        runtime_request.get('guardian_decision')
    )
    executor_ref = _required_text(runtime_request.get('executor_ref'), 'executor_ref')
    executor_kind = _resolve_executor_kind(runtime_request, executor_ref)
    normalized_request = _mapping(
        runtime_request.get('normalized_request'),
        'normalized_request',
    )
    loopback_contract: dict[str, Any] = {}
    if executor_kind == ARC_EXECUTOR_KIND_LOOPBACK_OLLAMA:
        loopback_contract = _validate_arc_loopback_ollama_request(runtime_request)

    executor_payload = {
        'request_id': request_id,
        'runtime_consumer': 'arc_bot_shell',
        'requested_action': 'arc.local_model_preview',
        'guardian_decision': dict(guardian_decision),
        'guardian_decision_id': guardian_decision['decision_id'],
        'executor_kind': executor_kind,
        'executor_ref': executor_ref,
        'normalized_request': dict(normalized_request),
        'evidence_refs': list(
            _string_sequence(
                runtime_request.get('evidence_refs', ()),
                'evidence_refs',
                allow_empty=True,
            )
        ),
    }
    executor_payload.update(loopback_contract)

    try:
        raw_result = executor(executor_payload)
    except Exception:  # pragma: no cover - exact exception type is caller-owned.
        raise V1LiveProviderModelCallExecutionError(
            'provider executor failed'
        ) from None

    if executor_kind == ARC_EXECUTOR_KIND_FAKE:
        return _normalize_arc_fake_result(
            raw_result,
            request_id=request_id,
            guardian_decision=guardian_decision,
            executor_ref=executor_ref,
        )
    return _normalize_arc_loopback_ollama_result(
        raw_result,
        request_id=request_id,
        guardian_decision=guardian_decision,
        executor_ref=executor_ref,
        expected_endpoint=loopback_contract['endpoint'],
        expected_model=loopback_contract['model'],
    )


def _resolve_executor_kind(
    runtime_request: Mapping[str, Any],
    executor_ref: str,
) -> str:
    raw_kind = runtime_request.get('executor_kind')
    if raw_kind is None:
        if executor_ref in LEGACY_FAKE_EXECUTOR_REFS:
            return ARC_EXECUTOR_KIND_FAKE
        raise V1LiveProviderModelCallExecutionError(
            'unsupported executor; executor_kind is required'
        )
    executor_kind = _required_text(raw_kind, 'executor_kind')
    if executor_kind not in ARC_EXECUTOR_KINDS:
        raise V1LiveProviderModelCallExecutionError('unsupported executor_kind')
    return executor_kind


def _validate_arc_loopback_ollama_request(
    runtime_request: Mapping[str, Any],
) -> dict[str, Any]:
    if runtime_request.get('network_scope') != 'loopback_only':
        raise V1LiveProviderModelCallExecutionError(
            'loopback_ollama requires network_scope=loopback_only'
        )
    if runtime_request.get('credentials_used') is not False:
        raise V1LiveProviderModelCallExecutionError(
            'loopback_ollama forbids credentials'
        )
    if runtime_request.get('external_side_effects') is not False:
        raise V1LiveProviderModelCallExecutionError(
            'loopback_ollama forbids external side effects'
        )
    endpoint = _normalize_loopback_ollama_endpoint(
        runtime_request.get('endpoint'),
        'endpoint',
    )
    model = _required_text(runtime_request.get('model'), 'model')
    return {
        'endpoint': endpoint,
        'model': model,
        'network_scope': 'loopback_only',
        'credentials_used': False,
        'external_side_effects': False,
    }


def _normalize_arc_fake_result(
    raw_result: Any,
    *,
    request_id: str,
    guardian_decision: Mapping[str, Any],
    executor_ref: str,
) -> dict[str, Any]:
    result = _mapping(raw_result, 'executor result')
    provider = _required_text(result.get('provider'), 'executor result.provider')
    model = _required_text(result.get('model'), 'executor result.model')
    output_text = _required_text(
        result.get('output_text'),
        'executor result.output_text',
    )
    _reject_raw_sensitive_content(output_text)
    if result.get('network_called') is not False:
        raise V1LiveProviderModelCallExecutionError(
            'fake executor must report network_called=false'
        )
    if result.get('credentials_used') is not False:
        raise V1LiveProviderModelCallExecutionError(
            'fake executor must report credentials_used=false'
        )
    if result.get('ollama_called', False) is not False:
        raise V1LiveProviderModelCallExecutionError(
            'fake executor must report ollama_called=false'
        )

    record = {
        'record_type': 'arc_consumer_runtime_baseline',
        'schema_version': 'arc-consumer-baseline-v1',
        'status': 'completed',
        'request_id': request_id,
        'runtime_consumer': 'arc_bot_shell',
        'requested_action': 'arc.local_model_preview',
        'guardian_decision': dict(guardian_decision),
        'guardian_decision_id': guardian_decision['decision_id'],
        'executor_ref': executor_ref,
        'executor_kind': ARC_EXECUTOR_KIND_FAKE,
        'executor_called': True,
        'provider': provider,
        'model': model,
        'output_text': output_text,
        'network_called': False,
        'credentials_used': False,
        'ollama_called': False,
        'evidence': {
            'guardian_decision_id': guardian_decision['decision_id'],
            'executor_ref': executor_ref,
            'executor_kind': ARC_EXECUTOR_KIND_FAKE,
            'executor_called': True,
            'network_called': False,
            'credentials_used': False,
            'ollama_called': False,
        },
    }
    record['record_hash'] = _record_hash(record)
    return record


def _normalize_arc_loopback_ollama_result(
    raw_result: Any,
    *,
    request_id: str,
    guardian_decision: Mapping[str, Any],
    executor_ref: str,
    expected_endpoint: str,
    expected_model: str,
) -> dict[str, Any]:
    result = _mapping(raw_result, 'executor result')
    provider = _required_text(result.get('provider'), 'executor result.provider')
    if provider != 'ollama':
        raise V1LiveProviderModelCallExecutionError(
            'loopback_ollama executor must report provider=ollama'
        )
    model = _required_text(result.get('model'), 'executor result.model')
    if model != expected_model:
        raise V1LiveProviderModelCallExecutionError(
            'loopback_ollama result model does not match request'
        )
    endpoint = _normalize_loopback_ollama_endpoint(
        result.get('endpoint'),
        'executor result.endpoint',
    )
    if endpoint != expected_endpoint:
        raise V1LiveProviderModelCallExecutionError(
            'loopback_ollama result endpoint does not match request'
        )
    if result.get('network_called') is not True:
        raise V1LiveProviderModelCallExecutionError(
            'loopback_ollama executor must report network_called=true'
        )
    if result.get('network_scope') != 'loopback_only':
        raise V1LiveProviderModelCallExecutionError(
            'loopback_ollama executor must report network_scope=loopback_only'
        )
    if result.get('ollama_called') is not True:
        raise V1LiveProviderModelCallExecutionError(
            'loopback_ollama executor must report ollama_called=true'
        )
    if result.get('credentials_used') is not False:
        raise V1LiveProviderModelCallExecutionError(
            'loopback_ollama executor must report credentials_used=false'
        )
    if result.get('external_side_effects') is not False:
        raise V1LiveProviderModelCallExecutionError(
            'loopback_ollama executor must report external_side_effects=false'
        )

    duration_value = result.get('duration_ms')
    duration_ms = (
        None
        if duration_value is None
        else _nonnegative_int(duration_value, 'executor result.duration_ms')
    )
    status = _normalize_token(
        _required_text(result.get('status'), 'executor result.status')
    )
    output_text = ''
    error_category: str | None = None
    error_message: str | None = None
    if status == 'completed':
        output_text = _required_text(
            result.get('output_text'),
            'executor result.output_text',
        )
        _reject_raw_sensitive_content(output_text)
        if result.get('error_category') not in {None, ''}:
            raise V1LiveProviderModelCallExecutionError(
                'completed loopback_ollama result cannot include error_category'
            )
        if result.get('error_message') not in {None, ''}:
            raise V1LiveProviderModelCallExecutionError(
                'completed loopback_ollama result cannot include error_message'
            )
    elif status == 'unavailable':
        if result.get('output_text') not in {None, ''}:
            raise V1LiveProviderModelCallExecutionError(
                'unavailable loopback_ollama result cannot include output_text'
            )
        error_category = _normalize_token(
            _required_text(
                result.get('error_category'),
                'executor result.error_category',
            )
        )
        if error_category not in LOOPBACK_OLLAMA_ERROR_CATEGORIES:
            raise V1LiveProviderModelCallExecutionError(
                'loopback_ollama error_category is not supported'
            )
        error_message = _sanitized_error_message(
            result.get('error_message'),
            'executor result.error_message',
        )
    else:
        raise V1LiveProviderModelCallExecutionError(
            'loopback_ollama status must be completed or unavailable'
        )

    record = {
        'record_type': 'arc_consumer_loopback_ollama_runtime',
        'schema_version': 'arc-consumer-loopback-ollama-v1.1',
        'status': status,
        'request_id': request_id,
        'runtime_consumer': 'arc_bot_shell',
        'requested_action': 'arc.local_model_preview',
        'guardian_decision': dict(guardian_decision),
        'guardian_decision_id': guardian_decision['decision_id'],
        'executor_ref': executor_ref,
        'executor_kind': ARC_EXECUTOR_KIND_LOOPBACK_OLLAMA,
        'executor_called': True,
        'provider': provider,
        'model': model,
        'output_text': output_text,
        'endpoint': endpoint,
        'network_called': True,
        'network_scope': 'loopback_only',
        'ollama_called': True,
        'credentials_used': False,
        'external_side_effects': False,
        'duration_ms': duration_ms,
        'error_category': error_category,
        'error_message': error_message,
        'evidence': {
            'guardian_decision_id': guardian_decision['decision_id'],
            'requested_action': 'arc.local_model_preview',
            'executor_ref': executor_ref,
            'executor_kind': ARC_EXECUTOR_KIND_LOOPBACK_OLLAMA,
            'executor_called': True,
            'provider': provider,
            'model': model,
            'endpoint': endpoint,
            'network_called': True,
            'network_scope': 'loopback_only',
            'ollama_called': True,
            'credentials_used': False,
            'external_side_effects': False,
            'duration_ms': duration_ms,
            'status': status,
            'error_category': error_category,
            'error_message': error_message,
        },
    }
    record['record_hash'] = _record_hash(record)
    return record


def _normalize_loopback_ollama_endpoint(value: Any, field_name: str) -> str:
    endpoint = _required_text(value, field_name)
    try:
        parsed = urlsplit(endpoint)
        port = parsed.port
        host = parsed.hostname
    except ValueError as exc:
        raise V1LiveProviderModelCallExecutionError(
            f'{field_name} is not a valid URL'
        ) from exc
    if parsed.scheme != 'http':
        raise V1LiveProviderModelCallExecutionError(
            f'{field_name} must use http'
        )
    if parsed.username is not None or parsed.password is not None:
        raise V1LiveProviderModelCallExecutionError(
            f'{field_name} cannot include URL credentials'
        )
    if host not in LOOPBACK_OLLAMA_HOSTS:
        raise V1LiveProviderModelCallExecutionError(
            f'{field_name} must use an approved loopback host'
        )
    if parsed.path not in {'', '/'} or parsed.query or parsed.fragment:
        raise V1LiveProviderModelCallExecutionError(
            f'{field_name} must be a loopback base URL'
        )
    if port is None or port < 1 or port > 65535:
        raise V1LiveProviderModelCallExecutionError(
            f'{field_name} must include a valid port'
        )
    return f'http://{host}:{port}'


def _sanitized_error_message(value: Any, field_name: str) -> str:
    message = _required_text(value, field_name)
    if len(message) > 512 or '\n' in message or '\r' in message:
        raise V1LiveProviderModelCallExecutionError(
            f'{field_name} must be a short single-line message'
        )
    _reject_raw_sensitive_content(message)
    return message


def _validate_authority_record(value: Any) -> dict[str, Any]:
    authority = _mapping(value, "authority_record")
    if authority.get("record_type") != "v1_live_provider_model_call_authority":
        raise V1LiveProviderModelCallExecutionError(
            "prevalidated V1-G44 authority record is required"
        )
    if authority.get("schema_version") != AUTHORITY_SCHEMA_VERSION:
        raise V1LiveProviderModelCallExecutionError(
            "V1-G44 authority schema_version is required"
        )
    if authority.get("record_hash") != _record_hash(authority):
        raise V1LiveProviderModelCallExecutionError(
            "V1-G44 authority record_hash is invalid"
        )
    if authority.get("proof_not_execution") is not True:
        raise V1LiveProviderModelCallExecutionError(
            "V1-G44 authority proof metadata is required"
        )
    if authority.get("non_executing") is not True:
        raise V1LiveProviderModelCallExecutionError(
            "V1-G44 authority must be non-executing preflight metadata"
        )
    if authority.get("authority_preflight_metadata_only") is not True:
        raise V1LiveProviderModelCallExecutionError(
            "V1-G44 authority preflight metadata is required"
        )
    for field_name in AUTHORITY_FALSE_FIELDS:
        if authority.get(field_name) is not False:
            raise V1LiveProviderModelCallExecutionError(
                "V1-G44 authority cannot already claim execution"
            )

    lineage = _mapping(
        authority.get('request_or_guardian_decision_linkage'),
        'authority_record.request_or_guardian_decision_linkage',
    )
    guardian_decision_id = _required_text(
        lineage.get('guardian_decision_id'),
        'authority_record.request_or_guardian_decision_linkage.guardian_decision_id',
    )
    if lineage.get('linkage_required') is not True:
        raise V1LiveProviderModelCallExecutionError(
            'Guardian decision lineage must be required'
        )

    return {
        'guardian_decision_id': guardian_decision_id,
        "authority_id": _required_text(authority.get("authority_id"), "authority_id"),
        "record_hash": _required_text(authority.get("record_hash"), "record_hash"),
        "provider_id": _required_text(authority.get("provider_id"), "provider_id"),
        "model_id": _required_text(authority.get("model_id"), "model_id"),
        "model_role": _required_text(authority.get("model_role"), "model_role"),
        "data_sensitivity": _required_text(
            authority.get("data_sensitivity"),
            "data_sensitivity",
        ),
        "budget_class": _required_text(authority.get("budget_class"), "budget_class"),
        "estimated_cost_class": _required_text(
            authority.get("estimated_cost_class"),
            "estimated_cost_class",
        ),
        "latency_tier": _required_text(authority.get("latency_tier"), "latency_tier"),
    }


def _validate_guardian_decision(value: Any) -> dict[str, Any]:
    if isinstance(value, GuardianDecision):
        decision_id = _required_text(value.decision_id, 'guardian_decision.decision_id')
        if value.status is not GuardianDecisionStatus.APPROVED:
            raise V1LiveProviderModelCallExecutionError(
                'Guardian decision must be approved and execution-eligible'
            )
        return {
            'decision_id': decision_id,
            'status': value.status.value,
            'allowed': True,
            'requires_approval': False,
        }

    decision = _mapping(value, 'guardian_decision')
    decision_id = _required_text(
        decision.get('decision_id'),
        'guardian_decision.decision_id',
    )
    raw_status = decision.get('status')
    if isinstance(raw_status, GuardianDecisionStatus):
        raw_status = raw_status.value
    status = _normalize_token(_required_text(raw_status, 'guardian_decision.status'))
    if status not in {'allow', 'allowed', 'approved'}:
        raise V1LiveProviderModelCallExecutionError(
            'Guardian decision must be approved and execution-eligible'
        )
    if decision.get('allowed') is not True:
        raise V1LiveProviderModelCallExecutionError(
            'Guardian decision must explicitly allow execution'
        )
    if decision.get('requires_approval') is not False:
        raise V1LiveProviderModelCallExecutionError(
            'Guardian approval-required decisions cannot execute'
        )
    return {
        'decision_id': decision_id,
        'status': status,
        'allowed': True,
        'requires_approval': False,
    }


def _validate_execution_approval_linkage(value: Any) -> dict[str, Any]:
    approval = _mapping(value, "execution_approval_linkage")
    approval_evidence_ref = _required_text(
        approval.get("approval_evidence_ref"),
        "execution_approval_linkage.approval_evidence_ref",
    )
    if approval.get("approval_evidence_current") is not True:
        raise V1LiveProviderModelCallExecutionError(
            "execution approval evidence must be current"
        )
    if approval.get("approval_scope") != "v1-g46-live-provider-model-call-execution":
        raise V1LiveProviderModelCallExecutionError(
            "V1-G46 execution approval scope is required"
        )
    if approval.get("grants_live_provider_execution_authority") is not True:
        raise V1LiveProviderModelCallExecutionError(
            "live provider/model execution authority is required"
        )
    if approval.get("proof_of_operator_approval") is not True:
        raise V1LiveProviderModelCallExecutionError(
            "operator approval proof is required"
        )
    return {
        "approval_evidence_ref": approval_evidence_ref,
        "approval_evidence_current": True,
        "approval_scope": "v1-g46-live-provider-model-call-execution",
        "grants_live_provider_execution_authority": True,
        "proof_of_operator_approval": True,
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
        raise V1LiveProviderModelCallExecutionError("audit linkage is required")
    if audit.get("sanitized_evidence_only") is not True:
        raise V1LiveProviderModelCallExecutionError(
            "audit linkage must be sanitized evidence only"
        )
    return {
        "audit_record_ref": audit_record_ref,
        "evidence_refs": list(evidence_refs),
        "required": True,
        "sanitized_evidence_only": True,
    }


def _validate_redaction_policy(value: Any) -> dict[str, Any]:
    policy = _mapping(value, "redaction_policy")
    redaction_policy_ref = _required_text(
        policy.get("redaction_policy_ref"),
        "redaction_policy.redaction_policy_ref",
    )
    if policy.get("redacted_input_required") is not True:
        raise V1LiveProviderModelCallExecutionError("redacted input is required")
    if policy.get("redacted_output_required") is not True:
        raise V1LiveProviderModelCallExecutionError("redacted output is required")
    for field_name in (
        "raw_prompt_persistence_allowed",
        "raw_model_response_persistence_allowed",
        "raw_customer_data_persistence_allowed",
        "raw_secret_credential_persistence_allowed",
    ):
        if policy.get(field_name) is not False:
            raise V1LiveProviderModelCallExecutionError(
                "raw prompt/model response/customer data persistence is not allowed"
            )
    return {
        "redaction_policy_ref": redaction_policy_ref,
        "redacted_input_required": True,
        "redacted_output_required": True,
        "raw_prompt_persistence_allowed": False,
        "raw_model_response_persistence_allowed": False,
        "raw_customer_data_persistence_allowed": False,
        "raw_secret_credential_persistence_allowed": False,
    }


def _validate_execution_boundary(value: Any) -> dict[str, Any]:
    boundary = _mapping(value, "execution_boundary")
    provider_executor_boundary_ref = _required_text(
        boundary.get("provider_executor_boundary_ref"),
        "execution_boundary.provider_executor_boundary_ref",
    )
    if boundary.get("provider_executor_injected") is not True:
        raise V1LiveProviderModelCallExecutionError(
            "provider executor must be injected"
        )
    for field_name in (
        "direct_provider_sdk_used",
        "direct_network_code_used",
        "ambient_secret_lookup_performed",
        "credential_value_accessed",
        "fallback_allowed",
        "tool_execution_allowed",
        "consumer_repo_mutation_allowed",
        "connector_browser_network_file_device_robotics_physical_world_behavior_allowed",
    ):
        if boundary.get(field_name) is not False:
            raise V1LiveProviderModelCallExecutionError(
                "execution boundary allows forbidden behavior"
            )
    return {
        "provider_executor_boundary_ref": provider_executor_boundary_ref,
        "provider_executor_injected": True,
        "direct_provider_sdk_used": False,
        "direct_network_code_used": False,
        "ambient_secret_lookup_performed": False,
        "credential_value_accessed": False,
        "fallback_allowed": False,
        "tool_execution_allowed": False,
        "consumer_repo_mutation_allowed": False,
        "connector_browser_network_file_device_robotics_physical_world_behavior_allowed": False,
    }


def _validate_provider_result(value: Any) -> dict[str, Any]:
    result = _mapping(value, "provider_result")
    _reject_raw_sensitive_content(result)
    _reject_forbidden_claims(result)

    finish_status = _normalize_token(
        _required_text(result.get("finish_status"), "finish_status")
    )
    if finish_status not in ALLOWED_FINISH_STATUSES:
        raise V1LiveProviderModelCallExecutionError("finish_status is not allowed")

    usage = _mapping(result.get("usage_metadata"), "usage_metadata")
    input_tokens = _nonnegative_int(usage.get("input_tokens"), "input_tokens")
    output_tokens = _nonnegative_int(usage.get("output_tokens"), "output_tokens")
    total_tokens = _nonnegative_int(usage.get("total_tokens"), "total_tokens")
    if total_tokens < input_tokens + output_tokens:
        raise V1LiveProviderModelCallExecutionError("total_tokens is inconsistent")

    return {
        "provider_call_id": _required_text(
            result.get("provider_call_id"),
            "provider_call_id",
        ),
        "output_ref": _required_text(result.get("output_ref"), "output_ref"),
        "redacted_output_summary_ref": _required_text(
            result.get("redacted_output_summary_ref"),
            "redacted_output_summary_ref",
        ),
        "finish_status": finish_status,
        "usage_metadata": {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
        },
    }


def _reject_raw_sensitive_content(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            if isinstance(key, str) and key.strip().lower() in RAW_SENSITIVE_KEYS:
                raise V1LiveProviderModelCallExecutionError(
                    "raw sensitive content is not accepted"
                )
            _reject_raw_sensitive_content(nested)
    elif isinstance(value, (list, tuple, set, frozenset)):
        for nested in value:
            _reject_raw_sensitive_content(nested)
    elif isinstance(value, str):
        folded = value.strip().lower()
        if any(marker in folded for marker in RAW_SENSITIVE_VALUE_MARKERS):
            raise V1LiveProviderModelCallExecutionError(
                "raw sensitive content is not accepted"
            )


def _reject_forbidden_claims(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            if (
                isinstance(key, str)
                and key.strip().lower() in FORBIDDEN_TRUE_CLAIM_KEYS
                and nested is not False
            ):
                raise V1LiveProviderModelCallExecutionError(
                    "execution request cannot claim forbidden behavior"
                )
            _reject_forbidden_claims(nested)
    elif isinstance(value, (list, tuple, set, frozenset)):
        for nested in value:
            _reject_forbidden_claims(nested)


def _mapping(value: Any, field_name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping) or not value:
        raise V1LiveProviderModelCallExecutionError(f"{field_name} is required")
    return value


def _required_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise V1LiveProviderModelCallExecutionError(f"{field_name} is required")
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
        raise V1LiveProviderModelCallExecutionError(
            f"{field_name} must be a string sequence"
        )
    normalized = tuple(str(item).strip() for item in value if str(item).strip())
    if not normalized and not allow_empty:
        raise V1LiveProviderModelCallExecutionError(f"{field_name} is required")
    return normalized


def _require_true_confirmation(value: Any, field_name: str) -> None:
    if value is True:
        return
    if isinstance(value, Mapping) and value.get("confirmed") is True:
        return
    raise V1LiveProviderModelCallExecutionError(
        f"{field_name} confirmation is required"
    )


def _nonnegative_int(value: Any, field_name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise V1LiveProviderModelCallExecutionError(
            f"{field_name} must be a non-negative integer"
        )
    return value


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
