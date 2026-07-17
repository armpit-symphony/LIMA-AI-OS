"""Static checks for the V1-G60 SDK dependency/vendor import request audit."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
AUDIT_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g60_sdk_dependency_vendor_provider_sdk_import_approval_request_audit.json"
)
REQUEST_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g60_sdk_dependency_vendor_provider_sdk_import_approval_request.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _load_audit_fixture() -> dict[str, Any]:
    return _load_json(AUDIT_FIXTURE_PATH)


def _load_request_fixture() -> dict[str, Any]:
    return _load_json(REQUEST_FIXTURE_PATH)


def test_v1_g60_request_audit_fixture_and_docs_exist() -> None:
    fixture = _load_audit_fixture()

    assert fixture["audit_id"] == (
        "v1_g60_sdk_dependency_vendor_provider_sdk_import_approval_request_audit"
    )
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == (
        "audit-v1-g60-sdk-dependency-vendor-provider-sdk-import-approval-request"
    )
    assert fixture["source_branch"] == (
        "prepare-v1-g60-sdk-dependency-vendor-provider-sdk-import-approval-request"
    )
    assert fixture["source_commit_before_audit"] == (
        "67693574d9e66de67680144b13bd4f51b604cdf1"
    )
    assert fixture["audit_verdict"] == "PASS"
    assert fixture["implementation_approved"] is False

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path
    for relative_path in fixture["request_files_reviewed"]:
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_g60_request_audit_matches_request_fixture() -> None:
    audit = _load_audit_fixture()
    request = _load_request_fixture()

    assert request["api_status"] == audit["api_status"]
    assert request["branch"] == audit["source_branch"]
    assert request["implementation_approved"] is False
    assert request["operator_approval_recorded"] is False
    assert request["decision_record"]["recorded_choice"] == "none"
    assert audit["audit_results"]["request_only"] is True
    assert audit["audit_results"]["request_file_scope_only"] is True


def test_v1_g60_request_audit_operator_decision_packet_is_waiting() -> None:
    audit = _load_audit_fixture()
    decision_text = (REPO_ROOT / audit["decision_packet_reviewed"]).read_text(
        encoding="utf-8"
    )

    assert "Decision packet status: `awaiting_operator_decision`" in decision_text
    assert "Recorded choice: none" in decision_text
    assert "Recorded choice: Approve-V1-G60" in decision_text
    assert "Recorded choice: Revise-V1-G60" in decision_text
    assert "Recorded choice: Pause" in decision_text
    assert (
        "I explicitly approve V1-G60 implementation of the LIMA-side SDK "
        "dependency addition and vendor provider SDK import approval slice, "
        "limited to the file scope, behavior scope, tests, rollback plan, and "
        "stop conditions in "
        "docs/V1_G60_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_APPROVAL_REQUEST.md."
        in decision_text
    )


def test_v1_g60_request_audit_scope_and_boundaries_are_explicit() -> None:
    results = _load_audit_fixture()["audit_results"]

    assert results["request_verdict_ready_for_operator_decision_not_approved"] is True
    assert results["decision_packet_awaiting_operator_decision"] is True
    assert results["exact_approve_v1_g60_wording_present"] is True
    assert results["valid_operator_choices_exact"] is True
    assert results["implementation_approved"] is False
    assert results["operator_approval_recorded"] is False
    assert results["proposed_lima_runtime_files_empty"] is True
    assert results["proposed_dependency_manifest_scope_limited_to_pyproject_toml"] is True
    assert results["proposed_lockfile_scope_empty"] is True
    assert results["proposed_docs_tests_fixtures_scope_exact"] is True
    assert (
        results[
            "dependency_declaration_manifest_edit_vendor_import_client_construction_credential_endpoint_network_runtime_steps_separated"
        ]
        is True
    )


def test_v1_g60_request_audit_forbidden_boundaries_remain_false() -> None:
    results = _load_audit_fixture()["audit_results"]

    for key in (
        "lima_runtime_files_changed",
        "lima_public_api_changed",
        "sparkbot_files_changed",
        "arc_bot_shell_files_changed",
        "consumer_production_runtime_source_files_changed",
        "sdk_dependency_added",
        "dependency_manifest_edited",
        "lockfile_edited",
        "vendor_provider_sdk_import_added",
        "built_in_provider_sdk_client_implementation_added",
        "provider_client_construction_added",
        "provider_execution_expansion_added",
        "live_provider_model_call_execution_added",
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
        "credential_value_access_added",
        "provider_token_or_api_key_access_added",
        "provider_configuration_changes_added",
        "fallback_execution_added",
        "token_guardian_live_routing_added",
        "human_input_bridge_activated",
        "tool_execution_added",
        "connector_browser_network_file_device_robotics_physical_world_behavior_added",
        "scheduled_task_execution_added",
        "external_send_added",
        "raw_sensitive_content_persisted",
        "product_ready",
        "production_ready",
        "final_public_api_freeze_approved",
    ):
        assert results[key] is False, key


def test_v1_g60_request_audit_blocked_future_authorities_remain_false() -> None:
    blocked = _load_audit_fixture()["still_blocked_authorities"]

    for key, value in blocked.items():
        assert value is False, key


def test_v1_g60_request_audit_validation_evidence_is_recorded() -> None:
    fixture = _load_audit_fixture()
    validation = fixture["validation_evidence"]
    audit_validation = fixture["audit_branch_validation_evidence"]

    assert validation["focused_v1_g60_request_validation"] == {
        "passed": True,
        "tests_passed": 10,
    }
    assert validation["focused_v1_g60_g59_g58_request_readiness_validation"] == {
        "passed": True,
        "tests_passed": 93,
    }
    assert validation["compileall_lima"] == {"passed": True}
    assert validation["full_lima_suite"] == {"passed": True, "tests_passed": 5199}
    assert audit_validation["focused_v1_g60_request_audit_validation"] == {
        "passed": True,
        "tests_passed": 10,
    }
    assert audit_validation["focused_v1_g60_request_audit_chain_validation"] == {
        "passed": True,
        "tests_passed": 53,
    }
    assert audit_validation["compileall_lima"] == {"passed": True}
    assert audit_validation["full_lima_suite"] == {
        "passed": True,
        "tests_passed": 5209,
    }


def test_v1_g60_request_audit_doc_contains_required_boundary_language() -> None:
    audit = _load_audit_fixture()
    text = (REPO_ROOT / audit["documents"]["audit"]).read_text(encoding="utf-8")

    assert "Audit verdict: `PASS`" in text
    assert "request-only V1-G60 approval gate" in text
    assert "It does not approve implementation." in text
    assert "No SDK dependency was added by the request branch: pass." in text
    assert "`pyproject.toml` was not edited by the request branch: pass." in text
    assert "No vendor provider SDK import was added by the request branch: pass." in text
    assert "No endpoint resolution was added or performed by LIMA: pass." in text
    assert "V1-G60 passes independent request-gate audit" in text


def test_v1_g60_request_audit_fixture_and_doc_do_not_include_sensitive_markers() -> None:
    audit = _load_audit_fixture()
    output = json.dumps(audit, sort_keys=True)
    output += (REPO_ROOT / audit["documents"]["audit"]).read_text(encoding="utf-8")

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


def test_v1_g60_request_audit_next_step_requires_operator_decision() -> None:
    fixture = _load_audit_fixture()

    assert fixture["next_recommended_steps"] == [
        "operator_decision_on_approve_v1_g60_revise_v1_g60_or_pause",
        "do_not_start_v1_g60_implementation_without_exact_approval",
    ]
    assert fixture["audit_results"]["implementation_approved"] is False
    assert fixture["audit_results"]["product_ready"] is False
    assert fixture["audit_results"]["production_ready"] is False
