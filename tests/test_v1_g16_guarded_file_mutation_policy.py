"""Runtime tests for the approved V1-G16 file mutation policy slice."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from lima.guardian import (
    V1FileMutationPolicyError,
    validate_v1_guarded_file_mutation_policy,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g16_guarded_file_mutation_policy.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _policy_metadata(**overrides: Any) -> dict[str, Any]:
    record = {
        "request_classification": {
            "request_type": "file_delete",
            "mutation_kind": "destructive_delete",
            "destructive_mutation": True,
            "requires_operator_approval": True,
            "actual_execution_requested": False,
        },
        "mutation_intent_scope": {
            "scope_id": "scope:v1-g16:docs",
            "target_ref": "file:docs/example.md",
            "target_path": "docs/example.md",
            "normalized_target_path_ref": "docs/example.md",
            "approved_path_prefixes": ["docs"],
            "path_traversal_rejected": True,
            "target_path_normalization_required": True,
            "mutation_outside_scope_allowed": False,
        },
        "workspace_root_boundary": {
            "workspace_ref": "workspace:lima-ai-os",
            "root_ref": "repo-root",
            "root_boundary_required": True,
            "outside_workspace_allowed": False,
            "path_traversal_rejected": True,
        },
        "target_path_expectations": {
            "normalization_required": True,
            "path_traversal_rejected": True,
            "absolute_paths_rejected": True,
            "outside_workspace_rejected": True,
        },
        "shell_harness_file_authority": {
            "authority_ref": "authority:shell:file-scope:v1-g16",
            "provided_by_shell_or_harness": True,
            "authority_required": True,
            "authority_scope_refs": ["scope:v1-g16:docs"],
            "execution_authority_granted": False,
        },
        "operator_approval_evidence_requirements": {
            "approval_policy_ref": "policy:v1-g16:file-mutation",
            "approval_required": True,
            "approval_evidence_required": True,
            "approval_state_required": "granted",
            "approval_freshness_required": "fresh",
            "approval_replay_status_required": "not_replayed",
            "mutation_without_approval_allowed": False,
        },
        "dry_run_preview_requirement": {
            "required": True,
            "actual_mutation_allowed_in_preview": False,
        },
        "diff_patch_preview_expectation": {
            "required": True,
            "redacted_metadata_only": True,
            "raw_file_content_allowed": False,
        },
        "rollback_expectation": {
            "required": True,
            "rollback_plan_ref": "rollback:v1-g16:docs-example",
        },
        "destructive_delete_confirmation_expectation": {
            "required_for_delete": True,
            "confirmation_ref_required": True,
            "confirmation_policy_ref": "confirmation:v1-g16:delete",
        },
        "audit_evidence_linkage": {
            "required": True,
            "audit_record_ref": "audit:v1-g16:docs-example",
            "evidence_refs": ["fixture:v1-g16"],
            "proof_not_authority": True,
        },
        "tenant_scope": "tenant:alpha",
        "shell_scope": "shell:sparkbot-shell",
        "actor_scope": "actor:user-123",
        "session_scope": "session:local",
    }
    record.update(overrides)
    return record


def test_v1_g16_fixture_records_approved_scope_and_boundaries() -> None:
    fixture = _load_fixture()

    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g16-guarded-file-mutation-policy"
    assert fixture["operator_decision"] == "Approve-V1-G16"
    assert fixture["approved_scope"] == "guarded_file_mutation_policy_contract_slice"
    assert set(fixture["runtime_symbols"]) == {
        "V1FileMutationPolicyError",
        "validate_v1_guarded_file_mutation_policy",
    }
    assert fixture["actual_file_mutation_execution_approved"] is False
    assert all(value is False for value in fixture["forbidden_behavior"].values())


@pytest.mark.parametrize(
    "request_type,mutation_kind",
    [
        ("file_edit", "destructive_edit"),
        ("file_delete", "destructive_delete"),
        ("file_mutation", "destructive_file_mutation"),
    ],
)
def test_v1_g16_valid_policy_normalizes_file_mutation_contract(
    request_type: str,
    mutation_kind: str,
) -> None:
    metadata = _policy_metadata(
        request_classification={
            "request_type": request_type,
            "mutation_kind": mutation_kind,
            "destructive_mutation": True,
            "requires_operator_approval": True,
            "actual_execution_requested": False,
        }
    )
    record = validate_v1_guarded_file_mutation_policy(metadata)

    assert record["record_type"] == "v1_guarded_file_mutation_policy"
    assert record["schema_version"] == "v1-g16-candidate"
    assert record["request_type"] == request_type
    assert record["mutation_kind"] == mutation_kind
    assert record["normalized_target_path"] == "docs/example.md"
    assert record["capability_open"] is True
    assert record["authority_gated"] is True
    assert record["policy_authority_contract"] is True
    assert record["execution_allowed"] is False
    assert record["side_effects_allowed"] is False
    assert record["file_mutation_executed"] is False
    assert record["actual_file_mutation_execution_approved"] is False
    assert record["preview_dry_run_behavior_implemented"] is False


def test_v1_g16_records_are_deterministic_for_sanitized_metadata() -> None:
    first = validate_v1_guarded_file_mutation_policy(_policy_metadata())
    second = validate_v1_guarded_file_mutation_policy(_policy_metadata())

    assert first == second
    assert first["record_hash"] == second["record_hash"]


@pytest.mark.parametrize(
    "field",
    [
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
    ],
)
def test_v1_g16_required_policy_fields_fail_closed(field: str) -> None:
    metadata = _policy_metadata()
    del metadata[field]

    with pytest.raises(V1FileMutationPolicyError, match=field):
        validate_v1_guarded_file_mutation_policy(metadata)


@pytest.mark.parametrize(
    "override,match",
    [
        (
            {
                "request_classification": {
                    "request_type": "informational",
                    "mutation_kind": "destructive_delete",
                    "destructive_mutation": True,
                    "requires_operator_approval": True,
                    "actual_execution_requested": False,
                }
            },
            "classification",
        ),
        (
            {
                "request_classification": {
                    "request_type": "file_delete",
                    "mutation_kind": "destructive_edit",
                    "destructive_mutation": True,
                    "requires_operator_approval": True,
                    "actual_execution_requested": False,
                }
            },
            "delete",
        ),
        (
            {
                "request_classification": {
                    "request_type": "file_delete",
                    "mutation_kind": "destructive_delete",
                    "destructive_mutation": False,
                    "requires_operator_approval": True,
                    "actual_execution_requested": False,
                }
            },
            "destructive",
        ),
        (
            {
                "request_classification": {
                    "request_type": "file_delete",
                    "mutation_kind": "destructive_delete",
                    "destructive_mutation": True,
                    "requires_operator_approval": False,
                    "actual_execution_requested": False,
                }
            },
            "operator approval",
        ),
        (
            {
                "request_classification": {
                    "request_type": "file_delete",
                    "mutation_kind": "destructive_delete",
                    "destructive_mutation": True,
                    "requires_operator_approval": True,
                    "actual_execution_requested": True,
                }
            },
            "execution",
        ),
    ],
)
def test_v1_g16_classification_fail_closed_cases(
    override: dict[str, Any],
    match: str,
) -> None:
    with pytest.raises(V1FileMutationPolicyError, match=match):
        validate_v1_guarded_file_mutation_policy(_policy_metadata(**override))


@pytest.mark.parametrize(
    "target_path,match",
    [
        ("../secrets.env", "traversal"),
        ("docs/../secrets.env", "traversal"),
        ("C:/Users/limap/secret.txt", "drive"),
        ("/etc/passwd", "absolute"),
        ("~/secret.txt", "absolute|home"),
    ],
)
def test_v1_g16_path_traversal_and_absolute_paths_fail_closed(
    target_path: str,
    match: str,
) -> None:
    intent = dict(_policy_metadata()["mutation_intent_scope"])
    intent["target_path"] = target_path
    intent["normalized_target_path_ref"] = target_path

    with pytest.raises(V1FileMutationPolicyError, match=match):
        validate_v1_guarded_file_mutation_policy(
            _policy_metadata(mutation_intent_scope=intent)
        )


def test_v1_g16_target_outside_approved_scope_fails_closed() -> None:
    intent = dict(_policy_metadata()["mutation_intent_scope"])
    intent["target_path"] = "lima/guardian.py"
    intent["normalized_target_path_ref"] = "lima/guardian.py"
    intent["approved_path_prefixes"] = ["docs"]

    with pytest.raises(V1FileMutationPolicyError, match="outside approved scope"):
        validate_v1_guarded_file_mutation_policy(
            _policy_metadata(mutation_intent_scope=intent)
        )


def test_v1_g16_target_normalization_mismatch_fails_closed() -> None:
    intent = dict(_policy_metadata()["mutation_intent_scope"])
    intent["target_path"] = "./docs/example.md"
    intent["normalized_target_path_ref"] = "docs/other.md"

    with pytest.raises(V1FileMutationPolicyError, match="normalization"):
        validate_v1_guarded_file_mutation_policy(
            _policy_metadata(mutation_intent_scope=intent)
        )


@pytest.mark.parametrize(
    "field,value,match",
    [
        ("path_traversal_rejected", False, "path traversal"),
        ("target_path_normalization_required", False, "normalization"),
        ("mutation_outside_scope_allowed", True, "outside approved scope"),
    ],
)
def test_v1_g16_intent_scope_policy_flags_fail_closed(
    field: str,
    value: Any,
    match: str,
) -> None:
    intent = dict(_policy_metadata()["mutation_intent_scope"])
    intent[field] = value

    with pytest.raises(V1FileMutationPolicyError, match=match):
        validate_v1_guarded_file_mutation_policy(
            _policy_metadata(mutation_intent_scope=intent)
        )


@pytest.mark.parametrize(
    "field,value,match",
    [
        ("root_boundary_required", False, "workspace/root"),
        ("outside_workspace_allowed", True, "outside workspace/root"),
        ("path_traversal_rejected", False, "path traversal"),
    ],
)
def test_v1_g16_workspace_boundary_flags_fail_closed(
    field: str,
    value: Any,
    match: str,
) -> None:
    boundary = dict(_policy_metadata()["workspace_root_boundary"])
    boundary[field] = value

    with pytest.raises(V1FileMutationPolicyError, match=match):
        validate_v1_guarded_file_mutation_policy(
            _policy_metadata(workspace_root_boundary=boundary)
        )


@pytest.mark.parametrize(
    "field,value,match",
    [
        ("normalization_required", False, "normalization"),
        ("path_traversal_rejected", False, "path traversal"),
        ("absolute_paths_rejected", False, "absolute path"),
        ("outside_workspace_rejected", False, "outside workspace"),
    ],
)
def test_v1_g16_path_expectation_flags_fail_closed(
    field: str,
    value: Any,
    match: str,
) -> None:
    path_expectations = dict(_policy_metadata()["target_path_expectations"])
    path_expectations[field] = value

    with pytest.raises(V1FileMutationPolicyError, match=match):
        validate_v1_guarded_file_mutation_policy(
            _policy_metadata(target_path_expectations=path_expectations)
        )


@pytest.mark.parametrize(
    "field,value,match",
    [
        ("provided_by_shell_or_harness", False, "shell/harness"),
        ("authority_required", False, "shell/harness"),
        ("execution_authority_granted", True, "execution"),
        ("authority_scope_refs", [], "scope refs"),
    ],
)
def test_v1_g16_shell_harness_authority_fail_closed(
    field: str,
    value: Any,
    match: str,
) -> None:
    authority = dict(_policy_metadata()["shell_harness_file_authority"])
    authority[field] = value

    with pytest.raises(V1FileMutationPolicyError, match=match):
        validate_v1_guarded_file_mutation_policy(
            _policy_metadata(shell_harness_file_authority=authority)
        )


@pytest.mark.parametrize(
    "field,value,match",
    [
        ("approval_required", False, "approval"),
        ("approval_evidence_required", False, "approval evidence"),
        ("mutation_without_approval_allowed", True, "without approval"),
        ("approval_state_required", "none", "granted"),
        ("approval_freshness_required", "stale", "fresh"),
        ("approval_replay_status_required", "replayed", "not_replayed"),
    ],
)
def test_v1_g16_approval_policy_fail_closed(
    field: str,
    value: Any,
    match: str,
) -> None:
    approval = dict(_policy_metadata()["operator_approval_evidence_requirements"])
    approval[field] = value

    with pytest.raises(V1FileMutationPolicyError, match=match):
        validate_v1_guarded_file_mutation_policy(
            _policy_metadata(operator_approval_evidence_requirements=approval)
        )


@pytest.mark.parametrize(
    "field_name,field,value,match",
    [
        ("dry_run_preview_requirement", "required", False, "dry-run preview"),
        (
            "dry_run_preview_requirement",
            "actual_mutation_allowed_in_preview",
            True,
            "cannot allow mutation",
        ),
        ("diff_patch_preview_expectation", "required", False, "diff/patch preview"),
        (
            "diff_patch_preview_expectation",
            "redacted_metadata_only",
            False,
            "redacted metadata",
        ),
        (
            "diff_patch_preview_expectation",
            "raw_file_content_allowed",
            True,
            "raw file content",
        ),
    ],
)
def test_v1_g16_preview_policy_fail_closed(
    field_name: str,
    field: str,
    value: Any,
    match: str,
) -> None:
    nested = dict(_policy_metadata()[field_name])
    nested[field] = value

    with pytest.raises(V1FileMutationPolicyError, match=match):
        validate_v1_guarded_file_mutation_policy(_policy_metadata(**{field_name: nested}))


def test_v1_g16_rollback_expectation_is_required() -> None:
    rollback = dict(_policy_metadata()["rollback_expectation"])
    rollback["required"] = False

    with pytest.raises(V1FileMutationPolicyError, match="rollback"):
        validate_v1_guarded_file_mutation_policy(
            _policy_metadata(rollback_expectation=rollback)
        )


def test_v1_g16_destructive_delete_confirmation_is_required_for_delete() -> None:
    confirmation = dict(_policy_metadata()["destructive_delete_confirmation_expectation"])
    confirmation["confirmation_ref_required"] = False

    with pytest.raises(V1FileMutationPolicyError, match="confirmation"):
        validate_v1_guarded_file_mutation_policy(
            _policy_metadata(destructive_delete_confirmation_expectation=confirmation)
        )


@pytest.mark.parametrize(
    "field,value,match",
    [
        ("required", False, "audit/evidence"),
        ("proof_not_authority", False, "cannot be authority"),
        ("evidence_refs", [], "evidence refs"),
    ],
)
def test_v1_g16_audit_linkage_fail_closed(
    field: str,
    value: Any,
    match: str,
) -> None:
    audit = dict(_policy_metadata()["audit_evidence_linkage"])
    audit[field] = value

    with pytest.raises(V1FileMutationPolicyError, match=match):
        validate_v1_guarded_file_mutation_policy(
            _policy_metadata(audit_evidence_linkage=audit)
        )


@pytest.mark.parametrize(
    "field,value",
    [
        ("raw_secret", "raw-secret-123"),
        ("raw_prompt", "raw prompt text"),
        ("raw_file_contents", "raw file contents"),
        ("raw_diff", "raw diff body"),
        ("raw_patch", "raw patch body"),
        ("raw_approval_pin", "approval-pin-123456"),
        ("raw_approval_token", "approval token value"),
        ("raw_customer_data", "raw customer data"),
    ],
)
def test_v1_g16_raw_sensitive_content_fails_closed(field: str, value: str) -> None:
    with pytest.raises(V1FileMutationPolicyError, match="raw sensitive"):
        validate_v1_guarded_file_mutation_policy(_policy_metadata(**{field: value}))


@pytest.mark.parametrize(
    "field",
    [
        "actual_file_mutation_execution_added",
        "execution_allowed",
        "side_effects_allowed",
        "file_mutation_executed",
        "file_deleted",
        "file_overwritten",
        "patch_applied",
        "user_file_read",
        "approval_token_issued",
        "provider_model_routed",
        "connector_invoked",
        "browser_action_executed",
        "network_action_executed",
        "physical_world_invoked",
        "humaninput_bridge_activated",
        "consumer_integration_added",
        "final_api_freeze_approved",
        "product_ready",
    ],
)
def test_v1_g16_runtime_authority_claims_fail_closed(field: str) -> None:
    with pytest.raises(V1FileMutationPolicyError, match="runtime authority"):
        validate_v1_guarded_file_mutation_policy(_policy_metadata(**{field: True}))


def test_v1_g16_output_does_not_emit_sensitive_values() -> None:
    record = validate_v1_guarded_file_mutation_policy(_policy_metadata())
    output = json.dumps(record, sort_keys=True, default=str)

    for forbidden in (
        "raw-secret-123",
        "approval-pin",
        "approval token",
        "raw prompt",
        "raw file contents",
        "raw diff",
        "raw patch",
        "raw customer data",
    ):
        assert forbidden not in output
