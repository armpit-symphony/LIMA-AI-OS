"""Runtime tests for the approved V1-G17 preview/diff slice."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from lima.guardian import (
    V1FileMutationPreviewError,
    validate_v1_file_mutation_preview_diff,
    validate_v1_guarded_file_mutation_policy,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g17_file_mutation_preview_diff.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _policy_metadata(**overrides: Any) -> dict[str, Any]:
    record = {
        "request_classification": {
            "request_type": "file_edit",
            "mutation_kind": "destructive_edit",
            "destructive_mutation": True,
            "requires_operator_approval": True,
            "actual_execution_requested": False,
        },
        "mutation_intent_scope": {
            "scope_id": "scope:v1-g17:docs",
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
            "authority_ref": "authority:shell:file-scope:v1-g17",
            "provided_by_shell_or_harness": True,
            "authority_required": True,
            "authority_scope_refs": ["scope:v1-g17:docs"],
            "execution_authority_granted": False,
        },
        "operator_approval_evidence_requirements": {
            "approval_policy_ref": "policy:v1-g17:file-mutation",
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
            "rollback_plan_ref": "rollback:v1-g17:docs-example",
        },
        "destructive_delete_confirmation_expectation": {
            "required_for_delete": True,
            "confirmation_ref_required": True,
            "confirmation_policy_ref": "confirmation:v1-g17:delete",
        },
        "audit_evidence_linkage": {
            "required": True,
            "audit_record_ref": "audit:v1-g17:docs-example",
            "evidence_refs": ["fixture:v1-g17"],
            "proof_not_authority": True,
        },
        "tenant_scope": "tenant:alpha",
        "shell_scope": "shell:sparkbot-shell",
        "actor_scope": "actor:user-123",
        "session_scope": "session:local",
    }
    record.update(overrides)
    return record


def _guarded_policy() -> dict[str, Any]:
    return validate_v1_guarded_file_mutation_policy(_policy_metadata())


def _preview_metadata(**overrides: Any) -> dict[str, Any]:
    policy = _guarded_policy()
    record = {
        "guarded_file_mutation_policy_ref": policy["record_hash"],
        "guarded_file_mutation_policy": policy,
        "path_scope_validation": {
            "validated": True,
            "normalized_target_path": "docs/example.md",
            "within_approved_scope": True,
            "mutation_outside_scope_allowed": False,
        },
        "workspace_root_validation": {
            "validated": True,
            "workspace_ref": "workspace:lima-ai-os",
            "root_ref": "repo-root",
            "inside_workspace_root": True,
            "outside_workspace_allowed": False,
        },
        "path_traversal_rejection": {
            "represented": True,
            "path_traversal_rejected": True,
            "absolute_paths_rejected": True,
            "checked_paths": ["docs/example.md"],
        },
        "dry_run_file_mutation_preview": {
            "preview_id": "preview:v1-g17:001",
            "dry_run": True,
            "preview_generated": True,
            "normalized_target_path": "docs/example.md",
            "actual_file_write": False,
            "actual_file_delete": False,
            "actual_file_mutation": False,
            "raw_file_content_persisted": False,
        },
        "redacted_diff_patch_preview": {
            "diff_preview_id": "diff-preview:v1-g17:001",
            "provided": True,
            "redacted_metadata_only": True,
            "raw_file_content_persisted": False,
            "raw_diff_persisted": False,
            "raw_patch_persisted": False,
            "patch_application_allowed": False,
            "redacted_hunk_count": 2,
            "redacted_addition_count": 5,
            "redacted_deletion_count": 1,
        },
        "rollback_plan_metadata": {
            "represented": True,
            "rollback_plan_ref": "rollback:v1-g17:docs-example",
            "required_before_execution": True,
        },
        "approval_evidence_linkage": {
            "required": True,
            "approval_evidence_ref": "approval-evidence:v1-g17:001",
            "approval_required_before_execution": True,
            "approval_metadata_grants_execution": False,
        },
        "user_operator_confirmation_linkage": {
            "required": True,
            "confirmation_ref": "confirmation:v1-g17:001",
            "confirmation_required_before_execution": True,
        },
        "shell_harness_policy_linkage": {
            "required": True,
            "shell_policy_ref": "shell-policy:v1-g17:001",
            "shell_runtime_wired": False,
            "execution_authority_granted": False,
        },
        "audit_evidence_linkage": {
            "required": True,
            "audit_record_ref": "audit:v1-g17:preview-diff",
            "evidence_refs": ["fixture:v1-g17", "approval-evidence:v1-g17:001"],
            "proof_not_authority": True,
        },
        "tenant_scope": "tenant:alpha",
        "shell_scope": "shell:sparkbot-shell",
        "actor_scope": "actor:user-123",
        "session_scope": "session:local",
    }
    record.update(overrides)
    return record


def test_v1_g17_fixture_records_approved_scope_and_boundaries() -> None:
    fixture = _load_fixture()

    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g17-file-mutation-preview-diff"
    assert fixture["operator_decision"] == "Approve-V1-G17"
    assert fixture["approved_scope"] == "file_mutation_preview_diff_runtime_slice"
    assert set(fixture["runtime_symbols"]) == {
        "V1FileMutationPreviewError",
        "validate_v1_file_mutation_preview_diff",
    }
    assert fixture["preview_diff_runtime_behavior_added"] is True
    assert fixture["actual_file_mutation_execution_approved"] is False
    assert all(value is False for value in fixture["forbidden_behavior"].values())


def test_v1_g17_valid_preview_diff_metadata_normalizes_record() -> None:
    record = validate_v1_file_mutation_preview_diff(_preview_metadata())

    assert record["record_type"] == "v1_file_mutation_preview_diff"
    assert record["schema_version"] == "v1-g17-candidate"
    assert record["policy_schema_version"] == "v1-g16-candidate"
    assert record["preview_id"] == "preview:v1-g17:001"
    assert record["diff_preview_id"] == "diff-preview:v1-g17:001"
    assert record["normalized_target_path"] == "docs/example.md"
    assert record["preview_diff_runtime_behavior"] is True
    assert record["dry_run_only"] is True
    assert record["redacted_metadata_only"] is True
    assert record["execution_allowed"] is False
    assert record["side_effects_allowed"] is False
    assert record["actual_file_mutation_execution_added"] is False
    assert record["file_read"] is False
    assert record["file_written"] is False
    assert record["file_deleted"] is False
    assert record["file_mutated"] is False
    assert record["patch_applied"] is False
    assert record["raw_file_content_persisted"] is False


def test_v1_g17_records_are_deterministic_for_sanitized_metadata() -> None:
    first = validate_v1_file_mutation_preview_diff(_preview_metadata())
    second = validate_v1_file_mutation_preview_diff(_preview_metadata())

    assert first == second
    assert first["record_hash"] == second["record_hash"]


@pytest.mark.parametrize(
    "field",
    [
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
    ],
)
def test_v1_g17_required_preview_fields_fail_closed(field: str) -> None:
    metadata = _preview_metadata()
    del metadata[field]

    with pytest.raises(V1FileMutationPreviewError, match=field):
        validate_v1_file_mutation_preview_diff(metadata)


def test_v1_g17_policy_linkage_is_required() -> None:
    metadata = _preview_metadata(guarded_file_mutation_policy_ref="wrong-ref")

    with pytest.raises(V1FileMutationPreviewError, match="policy ref"):
        validate_v1_file_mutation_preview_diff(metadata)


@pytest.mark.parametrize(
    "scope_field,value,match",
    [
        ("tenant_scope", "tenant:other", "tenant_scope"),
        ("shell_scope", "shell:other", "shell_scope"),
        ("actor_scope", "actor:other", "actor_scope"),
        ("session_scope", "session:other", "session_scope"),
    ],
)
def test_v1_g17_policy_scope_mismatch_fails_closed(
    scope_field: str,
    value: str,
    match: str,
) -> None:
    metadata = _preview_metadata(**{scope_field: value})

    with pytest.raises(V1FileMutationPreviewError, match=match):
        validate_v1_file_mutation_preview_diff(metadata)


@pytest.mark.parametrize(
    "field,value,match",
    [
        ("validated", False, "path scope"),
        ("within_approved_scope", False, "approved scope"),
        ("mutation_outside_scope_allowed", True, "outside approved scope"),
        ("normalized_target_path", "other/example.md", "match guarded policy"),
    ],
)
def test_v1_g17_path_scope_validation_fail_closed(
    field: str,
    value: Any,
    match: str,
) -> None:
    path_scope = dict(_preview_metadata()["path_scope_validation"])
    path_scope[field] = value

    with pytest.raises(V1FileMutationPreviewError, match=match):
        validate_v1_file_mutation_preview_diff(
            _preview_metadata(path_scope_validation=path_scope)
        )


@pytest.mark.parametrize(
    "field,value,match",
    [
        ("validated", False, "workspace/root"),
        ("inside_workspace_root", False, "inside workspace/root"),
        ("outside_workspace_allowed", True, "outside workspace"),
    ],
)
def test_v1_g17_workspace_root_validation_fail_closed(
    field: str,
    value: Any,
    match: str,
) -> None:
    workspace = dict(_preview_metadata()["workspace_root_validation"])
    workspace[field] = value

    with pytest.raises(V1FileMutationPreviewError, match=match):
        validate_v1_file_mutation_preview_diff(
            _preview_metadata(workspace_root_validation=workspace)
        )


@pytest.mark.parametrize(
    "field,value,match",
    [
        ("represented", False, "path traversal"),
        ("path_traversal_rejected", False, "path traversal"),
        ("absolute_paths_rejected", False, "absolute path"),
        ("checked_paths", ["../secret.env"], "traversal"),
        ("checked_paths", ["C:/secret.env"], "drive"),
    ],
)
def test_v1_g17_path_traversal_validation_fail_closed(
    field: str,
    value: Any,
    match: str,
) -> None:
    traversal = dict(_preview_metadata()["path_traversal_rejection"])
    traversal[field] = value

    with pytest.raises(V1FileMutationPreviewError, match=match):
        validate_v1_file_mutation_preview_diff(
            _preview_metadata(path_traversal_rejection=traversal)
        )


@pytest.mark.parametrize(
    "field,value,match",
    [
        ("dry_run", False, "dry-run"),
        ("preview_generated", False, "preview metadata"),
        ("actual_file_write", True, "write"),
        ("actual_file_delete", True, "delete"),
        ("actual_file_mutation", True, "mutate"),
        ("raw_file_content_persisted", True, "raw file content"),
        ("normalized_target_path", "docs/other.md", "match guarded policy"),
    ],
)
def test_v1_g17_dry_run_preview_fail_closed(
    field: str,
    value: Any,
    match: str,
) -> None:
    preview = dict(_preview_metadata()["dry_run_file_mutation_preview"])
    preview[field] = value

    with pytest.raises(V1FileMutationPreviewError, match=match):
        validate_v1_file_mutation_preview_diff(
            _preview_metadata(dry_run_file_mutation_preview=preview)
        )


@pytest.mark.parametrize(
    "field,value,match",
    [
        ("provided", False, "diff/patch"),
        ("redacted_metadata_only", False, "redacted metadata"),
        ("raw_file_content_persisted", True, "raw file content"),
        ("raw_diff_persisted", True, "raw diff"),
        ("raw_patch_persisted", True, "raw patch"),
        ("patch_application_allowed", True, "patch application"),
        ("redacted_hunk_count", -1, "non-negative"),
    ],
)
def test_v1_g17_redacted_diff_preview_fail_closed(
    field: str,
    value: Any,
    match: str,
) -> None:
    diff = dict(_preview_metadata()["redacted_diff_patch_preview"])
    diff[field] = value

    with pytest.raises(V1FileMutationPreviewError, match=match):
        validate_v1_file_mutation_preview_diff(
            _preview_metadata(redacted_diff_patch_preview=diff)
        )


@pytest.mark.parametrize(
    "field_name,field,value,match",
    [
        ("rollback_plan_metadata", "represented", False, "rollback"),
        ("rollback_plan_metadata", "required_before_execution", False, "rollback"),
        ("approval_evidence_linkage", "required", False, "approval evidence"),
        (
            "approval_evidence_linkage",
            "approval_required_before_execution",
            False,
            "approval evidence",
        ),
        (
            "approval_evidence_linkage",
            "approval_metadata_grants_execution",
            True,
            "grant execution",
        ),
        ("user_operator_confirmation_linkage", "required", False, "confirmation"),
        (
            "user_operator_confirmation_linkage",
            "confirmation_required_before_execution",
            False,
            "confirmation",
        ),
        ("shell_harness_policy_linkage", "required", False, "shell/harness"),
        ("shell_harness_policy_linkage", "shell_runtime_wired", True, "shell runtime"),
        (
            "shell_harness_policy_linkage",
            "execution_authority_granted",
            True,
            "grant execution",
        ),
        ("audit_evidence_linkage", "required", False, "audit/evidence"),
        ("audit_evidence_linkage", "proof_not_authority", False, "cannot be authority"),
        ("audit_evidence_linkage", "evidence_refs", [], "evidence refs"),
    ],
)
def test_v1_g17_required_linkage_metadata_fail_closed(
    field_name: str,
    field: str,
    value: Any,
    match: str,
) -> None:
    nested = dict(_preview_metadata()[field_name])
    nested[field] = value

    with pytest.raises(V1FileMutationPreviewError, match=match):
        validate_v1_file_mutation_preview_diff(_preview_metadata(**{field_name: nested}))


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
def test_v1_g17_raw_sensitive_content_fails_closed(field: str, value: str) -> None:
    with pytest.raises(V1FileMutationPreviewError, match="raw sensitive"):
        validate_v1_file_mutation_preview_diff(_preview_metadata(**{field: value}))


@pytest.mark.parametrize(
    "field",
    [
        "actual_file_mutation_execution_added",
        "actual_file_mutation_execution_approved",
        "execution_allowed",
        "side_effects_allowed",
        "file_read",
        "file_written",
        "file_deleted",
        "file_mutated",
        "file_overwritten",
        "patch_applied",
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
def test_v1_g17_runtime_authority_claims_fail_closed(field: str) -> None:
    with pytest.raises(V1FileMutationPreviewError, match="runtime authority"):
        validate_v1_file_mutation_preview_diff(_preview_metadata(**{field: True}))


def test_v1_g17_output_does_not_emit_sensitive_values() -> None:
    record = validate_v1_file_mutation_preview_diff(_preview_metadata())
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
