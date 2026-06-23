"""Static checks for the V1-G61 runtime vendor SDK import execution proof request."""

from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
LIMA_ROOT = REPO_ROOT / "lima"
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g61_runtime_vendor_sdk_import_execution_proof_approval_request.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _lima_imported_modules() -> set[str]:
    modules: set[str] = set()
    for path in sorted(LIMA_ROOT.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                modules.add(node.module)
    return modules


def _lima_call_names() -> set[str]:
    names: set[str] = set()
    for path in sorted(LIMA_ROOT.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    names.add(node.func.id)
                elif isinstance(node.func, ast.Attribute):
                    names.add(node.func.attr)
    return names


def test_v1_g61_request_docs_and_fixture_exist() -> None:
    fixture = _load_fixture()

    assert fixture["gate_id"] == (
        "v1_g61_runtime_vendor_sdk_import_execution_proof_approval_request"
    )
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == (
        "docs-v1-post-g60-readiness-and-next-lane-matrix"
    )
    assert fixture["observed_workspace_branch"] == (
        "docs-v1-post-g60-readiness-and-next-lane-matrix"
    )
    assert fixture["request_stage_lane_label"] == (
        "prepare-v1-g61-runtime-vendor-sdk-import-execution-proof-approval-request"
    )
    assert fixture["source_commit_before_request"] == (
        "37626bf236bf96c8a57a3ca351668e90eeb0e651"
    )
    assert fixture["docs_tests_fixtures_only_request"] is True

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g61_has_no_implementation_approval_yet() -> None:
    fixture = _load_fixture()
    decision = fixture["decision_record"]

    assert fixture["implementation_approved"] is False
    assert fixture["operator_approval_recorded"] is False
    assert fixture["runtime_vendor_sdk_import_execution_proof_approved"] is False
    assert fixture["runtime_vendor_sdk_import_execution_proof_added"] is False
    assert fixture["dependency_manifest_edited"] is False
    assert fixture["lockfile_edited"] is False
    assert fixture["vendor_provider_sdk_import_added_to_lima"] is False
    assert fixture["built_in_provider_sdk_client_implementation_approved"] is False
    assert fixture["built_in_provider_sdk_client_implementation_added"] is False
    assert fixture["provider_client_construction_added"] is False
    assert decision["recorded_choice"] == "none"
    assert decision["approved_implementation_branch"] == "none"
    assert decision["implementation_approved"] is False


def test_v1_g61_exact_decision_options_are_locked() -> None:
    fixture = _load_fixture()

    assert fixture["valid_operator_choices"] == [
        "Approve-V1-G61",
        "Revise-V1-G61",
        "Pause",
    ]
    assert fixture["required_approval_wording"] == (
        "I explicitly approve V1-G61 implementation of the runtime vendor SDK "
        "import execution proof slice, limited to the file scope, behavior "
        "scope, tests, rollback plan, and stop conditions in "
        "docs/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_APPROVAL_REQUEST.md."
    )
    assert fixture["proposed_implementation_branch"] == (
        "v1-g61-runtime-vendor-sdk-import-execution-proof"
    )

    labels = fixture["decision_option_labels"]
    assert labels["valid_choices_use_valid_choice_label"] is True
    assert labels["only_actual_decision_record_uses_recorded_choice_label"] is True
    assert labels["recorded_approve_choice_present"] is False
    assert labels["recorded_revise_choice_present"] is False
    assert labels["recorded_pause_choice_present"] is False


def test_v1_g61_target_if_approved_is_bounded_import_proof_only() -> None:
    target = _load_fixture()[
        "runtime_vendor_sdk_import_execution_target_if_operator_says_yes"
    ]

    assert target["runtime_vendor_sdk_import_execution_proof_allowed"] is True
    assert target["approved_vendor_provider_sdk_module"] == "openai"
    assert target["approved_dependency_declaration"] == "openai>=1.0.0,<3.0.0"
    assert target["test_scoped_import_only_allowed"] is True
    assert target["lima_runtime_vendor_sdk_import_allowed"] is False
    assert target["dependency_manifest_edit_allowed"] is False
    assert target["lockfile_edit_allowed"] is False
    assert target["built_in_provider_sdk_client_implementation_allowed"] is False
    assert target["provider_client_construction_allowed"] is False
    assert target["provider_execution_expansion_allowed"] is False
    assert target["guardian_gate_required"] is True
    assert target["operator_approval_linkage_required"] is True
    assert target["sanitized_evidence_only_required"] is True
    assert target["deny_by_default_required"] is True
    assert target["links_v1_g57_v1_g58_v1_g59_v1_g60_evidence_required"] is True


def test_v1_g61_target_forbidden_authorities_are_false() -> None:
    target = _load_fixture()[
        "runtime_vendor_sdk_import_execution_target_if_operator_says_yes"
    ]

    for key in (
        "lima_runtime_file_change_allowed",
        "lima_public_api_change_allowed",
        "consumer_production_runtime_code_edit_allowed",
        "direct_provider_sdk_call_implementation_allowed",
        "provider_endpoint_resolution_by_lima_allowed",
        "dns_lookup_by_lima_allowed",
        "http_client_by_lima_allowed",
        "socket_client_by_lima_allowed",
        "network_calls_by_lima_allowed",
        "direct_provider_egress_by_lima_allowed",
        "credential_value_access_allowed",
        "secret_lookup_allowed",
        "provider_token_or_api_key_access_allowed",
        "provider_configuration_changes_allowed",
        "fallback_execution_allowed",
        "connector_browser_network_physical_world_allowed",
        "consumer_production_runtime_integration_allowed",
        "product_readiness_claim_allowed",
        "final_public_api_freeze_claim_allowed",
    ):
        assert target[key] is False, key


def test_v1_g61_approved_file_scope_if_approved_is_exact() -> None:
    fixture = _load_fixture()

    assert fixture["approved_lima_runtime_files_if_operator_says_yes"] == []
    assert fixture["approved_dependency_manifest_files_if_operator_says_yes"] == []
    assert fixture["approved_lockfiles_if_operator_says_yes"] == []
    assert fixture["approved_lima_docs_tests_fixtures_if_operator_says_yes"] == [
        "docs/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF.md",
        "docs/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g61_runtime_vendor_sdk_import_execution_proof.json",
        "tests/test_v1_g61_runtime_vendor_sdk_import_execution_proof.py",
    ]
    assert fixture["approved_sparkbot_files_if_operator_says_yes"] == []
    assert fixture["approved_arc_bot_shell_files_if_operator_says_yes"] == []


def test_v1_g61_preapproval_runtime_tree_has_no_vendor_import_or_client_construction() -> None:
    fixture = _load_fixture()
    scan = fixture["preapproval_runtime_tree_scan"]
    imported_modules = _lima_imported_modules()
    call_names = _lima_call_names()
    approved_future_paths = [
        REPO_ROOT / relative_path
        for relative_path in fixture["approved_lima_docs_tests_fixtures_if_operator_says_yes"]
    ]

    assert scan == {
        "lima_runtime_vendor_sdk_import_present": False,
        "provider_sdk_client_constructor_present_in_lima": False,
        "approved_future_implementation_files_present": True,
        "scan_scope": "lima_runtime_tree_and_future_g61_docs_tests_fixture_paths",
    }
    assert "openai" not in imported_modules
    assert not {
        "OpenAI",
        "AsyncOpenAI",
        "AzureOpenAI",
        "AsyncAzureOpenAI",
    }.intersection(call_names)
    assert all(path.exists() for path in approved_future_paths)


def test_v1_g61_prior_evidence_refs_exist() -> None:
    for relative_path in _load_fixture()["required_prior_evidence_refs"]:
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_g61_current_gate_evidence_refs_exist() -> None:
    for relative_path in _load_fixture()["required_current_gate_evidence_refs"]:
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_g61_forbidden_boundaries_remain_false_in_request() -> None:
    fixture = _load_fixture()

    for key in (
        "consumer_repo_mutation_added",
        "consumer_runtime_calls_added",
        "consumer_production_runtime_integration_added",
        "live_provider_model_call_execution_added",
        "provider_sdk_network_egress_invocation_added",
        "provider_execution_expansion_added",
        "direct_provider_sdk_call_implementation_added",
        "provider_endpoint_resolution_added",
        "provider_endpoint_resolution_performed",
        "direct_network_code_added",
        "dns_lookup_added",
        "http_client_added",
        "socket_client_added",
        "network_call_performed_by_lima",
        "direct_provider_egress_performed_by_lima",
        "provider_readiness_network_check_added",
        "secret_lookup_added",
        "secret_lookup_performed",
        "credential_value_access_added",
        "credential_value_accessed",
        "provider_token_or_api_key_access_added",
        "provider_token_or_api_key_accessed",
        "credential_storage_rotation_migration_or_provisioning_added",
        "provider_configuration_changes_added",
        "fallback_execution_added",
        "tool_execution_added",
        "connector_browser_network_file_device_robotics_physical_world_behavior_added",
        "raw_prompt_persisted",
        "raw_model_response_persisted",
        "raw_customer_data_persisted",
        "raw_secret_or_credential_persisted",
        "raw_provider_token_or_api_key_persisted",
        "raw_diff_or_patch_persisted",
        "raw_file_content_persisted",
        "product_ready",
        "final_public_api_freeze_approved",
    ):
        assert fixture[key] is False, key


def test_v1_g61_docs_contain_request_only_boundary_language() -> None:
    fixture = _load_fixture()
    approval_text = (REPO_ROOT / fixture["documents"]["approval_request"]).read_text(
        encoding="utf-8"
    )
    decision_text = (
        REPO_ROOT / fixture["documents"]["operator_decision_packet"]
    ).read_text(encoding="utf-8")
    preflight_text = (REPO_ROOT / fixture["documents"]["preflight_audit"]).read_text(
        encoding="utf-8"
    )
    work_order_text = (REPO_ROOT / fixture["documents"]["work_order"]).read_text(
        encoding="utf-8"
    )

    assert "Approval request packet only: yes" in approval_text
    assert (
        "Observed workspace branch: `docs-v1-post-g60-readiness-and-next-lane-matrix`"
        in approval_text
    )
    assert (
        "Request-stage lane label: `prepare-v1-g61-runtime-vendor-sdk-import-execution-proof-approval-request`"
        in approval_text
    )
    assert "Implementation approved by this request: no" in approval_text
    assert "Dependency manifest edited by this request: no" in approval_text
    assert "Lockfile edited by this request: no" in approval_text
    assert "Vendor provider SDK import added to `lima/`: no" in approval_text
    assert "Network call performed by LIMA: no" in approval_text
    assert "Direct provider egress performed by LIMA: no" in approval_text
    assert "Current recorded choice: Approve-V1-G61" in decision_text
    assert "Recorded choice: Approve-V1-G61" in decision_text
    assert "Valid choice: Approve-V1-G61" in decision_text
    assert "Valid choice: Revise-V1-G61" in decision_text
    assert "Valid choice: Pause" in decision_text
    assert "V1_CURRENT_GATE_CONSISTENCY_AUDIT.md" in decision_text
    assert "still records V1-G61 as the active gate" in decision_text
    assert "Recorded choice: Revise-V1-G61" not in decision_text
    assert "Recorded choice: Pause" not in decision_text
    assert (
        "Observed workspace branch: `docs-v1-post-g60-readiness-and-next-lane-matrix`"
        in decision_text
    )
    assert (
        "Request-stage lane label: `prepare-v1-g61-runtime-vendor-sdk-import-execution-proof-approval-request`"
        in decision_text
    )
    assert "Implementation must not start until `Approve-V1-G61`" in preflight_text
    assert (
        "Observed workspace branch: `docs-v1-post-g60-readiness-and-next-lane-matrix`"
        in preflight_text
    )
    assert (
        "Request-stage lane label: `prepare-v1-g61-runtime-vendor-sdk-import-execution-proof-approval-request`"
        in preflight_text
    )
    assert "No `lima/` runtime files may be changed." in work_order_text
    assert (
        "Observed workspace branch: `docs-v1-post-g60-readiness-and-next-lane-matrix`"
        in work_order_text
    )
    assert (
        "Request-stage lane label: `prepare-v1-g61-runtime-vendor-sdk-import-execution-proof-approval-request`"
        in work_order_text
    )


def test_v1_g61_docs_and_fixture_do_not_include_sensitive_markers() -> None:
    fixture = _load_fixture()
    output = json.dumps(fixture, sort_keys=True)
    for relative_path in fixture["documents"].values():
        output += (REPO_ROOT / relative_path).read_text(encoding="utf-8")

    for forbidden in (
        "diff --git",
        "@@",
        "BEGIN PATCH",
        "raw patch body",
        "raw prompt value",
        "raw model response value",
        "raw customer data value",
        "provider credential value",
        "provider token value",
        "api key value",
        "raw-secret-123",
    ):
        assert forbidden not in output
