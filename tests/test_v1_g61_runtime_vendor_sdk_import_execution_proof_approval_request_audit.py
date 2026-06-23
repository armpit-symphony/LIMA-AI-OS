"""Static checks for the V1-G61 runtime vendor SDK import execution request audit."""

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
    / "v1_g61_runtime_vendor_sdk_import_execution_proof_approval_request_audit.json"
)
REQUEST_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g61_runtime_vendor_sdk_import_execution_proof_approval_request.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _load_audit_fixture() -> dict[str, Any]:
    return _load_json(AUDIT_FIXTURE_PATH)


def _load_request_fixture() -> dict[str, Any]:
    return _load_json(REQUEST_FIXTURE_PATH)


def test_v1_g61_request_audit_fixture_and_docs_exist() -> None:
    fixture = _load_audit_fixture()

    assert fixture["audit_id"] == (
        "v1_g61_runtime_vendor_sdk_import_execution_proof_approval_request_audit"
    )
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == (
        "docs-v1-post-g60-readiness-and-next-lane-matrix"
    )
    assert fixture["observed_workspace_branch"] == (
        "docs-v1-post-g60-readiness-and-next-lane-matrix"
    )
    assert fixture["audit_lane_label"] == (
        "audit-v1-g61-runtime-vendor-sdk-import-execution-proof-approval-request"
    )
    assert fixture["source_request_stage_lane_label"] == (
        "prepare-v1-g61-runtime-vendor-sdk-import-execution-proof-approval-request"
    )
    assert fixture["source_commit_before_audit"] == (
        "37626bf236bf96c8a57a3ca351668e90eeb0e651"
    )
    assert fixture["audit_verdict"] == "PASS"
    assert fixture["implementation_approved"] is True

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path
    for relative_path in fixture["request_files_reviewed"]:
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_g61_request_audit_matches_request_fixture() -> None:
    audit = _load_audit_fixture()
    request = _load_request_fixture()

    assert request["api_status"] == audit["api_status"]
    assert request["branch"] == audit["branch"]
    assert request["observed_workspace_branch"] == audit["observed_workspace_branch"]
    assert (
        request["request_stage_lane_label"]
        == audit["source_request_stage_lane_label"]
    )
    assert request["implementation_approved"] is False
    assert request["operator_approval_recorded"] is False
    assert request["decision_record"]["recorded_choice"] == "none"
    assert audit["audit_results"]["request_only"] is True
    assert audit["audit_results"]["request_file_scope_only"] is True


def test_v1_g61_request_audit_operator_decision_packet_is_waiting() -> None:
    audit = _load_audit_fixture()
    decision_text = (REPO_ROOT / audit["decision_packet_reviewed"]).read_text(
        encoding="utf-8"
    )

    assert "Decision packet status: `approved`" in decision_text
    assert "Current recorded choice: Approve-V1-G61" in decision_text
    assert "Recorded choice: Approve-V1-G61" in decision_text
    assert "Valid choice: Approve-V1-G61" in decision_text
    assert "Valid choice: Revise-V1-G61" in decision_text
    assert "Valid choice: Pause" in decision_text
    assert "Recorded choice: Revise-V1-G61" not in decision_text
    assert "Recorded choice: Pause" not in decision_text
    assert (
        "I explicitly approve V1-G61 implementation of the runtime vendor SDK "
        "import execution proof slice, limited to the file scope, behavior "
        "scope, tests, rollback plan, and stop conditions in "
        "docs/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_APPROVAL_REQUEST.md."
        in decision_text
    )


def test_v1_g61_request_audit_scope_and_boundaries_are_explicit() -> None:
    results = _load_audit_fixture()["audit_results"]

    assert results["request_verdict_ready_for_operator_decision_not_approved"] is True
    assert results["decision_packet_approved"] is True
    assert results["decision_packet_valid_choices_and_recorded_choice_are_distinct"] is True
    assert results["exact_approve_v1_g61_wording_present"] is True
    assert results["valid_operator_choices_exact"] is True
    assert results["implementation_approved"] is True
    assert results["operator_approval_recorded"] is True
    assert results["proposed_lima_runtime_files_empty"] is True
    assert results["proposed_dependency_manifest_scope_empty"] is True
    assert results["proposed_lockfile_scope_empty"] is True
    assert results["proposed_docs_tests_fixtures_scope_exact"] is True
    assert (
        results[
            "dependency_declaration_installation_lockfile_import_execution_client_construction_credential_endpoint_network_runtime_steps_separated"
        ]
        is True
    )


def test_v1_g61_request_audit_forbidden_boundaries_remain_false() -> None:
    results = _load_audit_fixture()["audit_results"]

    for key in (
        "lima_runtime_files_changed",
        "lima_public_api_changed",
        "sparkbot_files_changed",
        "arc_bot_shell_files_changed",
        "consumer_production_runtime_source_files_changed",
        "runtime_vendor_sdk_import_execution_proof_added",
        "dependency_manifest_edited",
        "lockfile_edited",
        "vendor_provider_sdk_import_added_to_lima",
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


def test_v1_g61_request_audit_blocked_future_authorities_remain_false() -> None:
    blocked = _load_audit_fixture()["still_blocked_authorities"]

    for key, value in blocked.items():
        assert value is False, key


def test_v1_g61_request_audit_prior_evidence_refs_exist() -> None:
    audit = _load_audit_fixture()

    for key in (
        "post_g60_readiness_rollup",
        "post_g60_next_lane_matrix",
        "prior_g60_audit",
        "prior_g60_implementation",
        "prior_g60_closeout",
        "prior_g59_audit",
        "prior_g58_audit",
        "prior_g57_audit",
    ):
        assert (REPO_ROOT / audit["documents"][key]).exists(), key


def test_v1_g61_request_audit_validation_evidence_is_recorded() -> None:
    fixture = _load_audit_fixture()
    validation = fixture["validation_evidence"]
    audit_validation = fixture["audit_branch_validation_evidence"]

    assert validation["focused_v1_g61_request_validation"] == {
        "passed": True,
        "tests_passed": 25,
    }
    assert validation["focused_v1_g61_g60_request_readiness_validation"] == {
        "passed": True,
        "tests_passed": 61,
    }
    assert validation["compileall_lima"] == {"passed": True}
    assert validation["full_lima_suite"] == {"passed": True, "tests_passed": 5262}
    assert audit_validation["focused_v1_g61_request_audit_validation"] == {
        "passed": True,
        "tests_passed": 11,
    }
    assert audit_validation["focused_v1_g61_request_audit_chain_validation"] == {
        "passed": True,
        "tests_passed": 42,
    }
    assert audit_validation["compileall_lima"] == {"passed": True}
    assert audit_validation["full_lima_suite"] == {
        "passed": True,
        "tests_passed": 5273,
    }


def test_v1_g61_request_audit_records_later_freshness_context() -> None:
    fixture = _load_audit_fixture()
    supplements = fixture["later_readiness_freshness_supplements_reviewed"]
    text = (REPO_ROOT / fixture["documents"]["audit"]).read_text(encoding="utf-8")

    assert supplements == {
        "latest_post_g61_request_refresh_focused_tests_passed": 8,
        "latest_post_g61_request_refresh_broader_tests_passed": 117,
        "latest_post_g61_request_refresh_full_lima_suite_tests_passed": 5362,
        "latest_quickstart_artifact_refresh_focused_tests_passed": 7,
        "latest_quickstart_artifact_refresh_adjacent_tests_passed": 64,
        "latest_quickstart_artifact_refresh_broader_tests_passed": 133,
        "latest_quickstart_artifact_refresh_full_lima_suite_tests_passed": 5364,
        "implementation_authority_created": True,
        "release_candidate_authority_created": False,
        "cutover_authority_created": False,
        "final_readiness_pass_created": False,
        "production_use_authority_created": False,
        "consumer_production_integration_authority_created": False,
        "final_public_api_freeze_authority_created": False,
    }
    assert "Later readiness freshness supplements reviewed after the original request audit:" in text
    assert "Post-G61 request readiness-refresh supplement: passed, 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, and 5362 full-suite tests." in text
    assert "Latest quickstart artifact refresh supplement: passed, 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5364 full-suite tests." in text
    assert "The later explicit operator decision packet approval is the authority for the bounded import execution proof only." in text


def test_v1_g61_request_audit_doc_contains_required_boundary_language() -> None:
    audit = _load_audit_fixture()
    text = (REPO_ROOT / audit["documents"]["audit"]).read_text(encoding="utf-8")

    assert "Audit verdict: `PASS`" in text
    assert (
        "Observed workspace branch: `docs-v1-post-g60-readiness-and-next-lane-matrix`"
        in text
    )
    assert (
        "Audit lane label: `audit-v1-g61-runtime-vendor-sdk-import-execution-proof-approval-request`"
        in text
    )
    assert (
        "Source request-stage lane label: `prepare-v1-g61-runtime-vendor-sdk-import-execution-proof-approval-request`"
        in text
    )
    assert "request-only V1-G61 approval gate" in text
    assert "The request packet did not approve implementation by itself" in text
    assert "No runtime import execution proof was added by the request branch itself: pass." in text
    assert "No dependency manifest was edited by the request branch: pass." in text
    assert "No lockfile was edited by the request branch: pass." in text
    assert "No vendor provider SDK import was added to `lima/` by the request branch: pass." in text
    assert "No endpoint resolution was added or performed by LIMA: pass." in text
    assert "V1-G61 passes independent request-gate audit" in text


def test_v1_g61_request_audit_fixture_and_doc_do_not_include_sensitive_markers() -> None:
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


def test_v1_g61_request_audit_next_step_requires_operator_decision() -> None:
    fixture = _load_audit_fixture()

    assert fixture["next_recommended_steps"] == [
        "refresh_post_g61_release_candidate_readiness",
        "do_not_expand_beyond_v1_g61_import_execution_proof_without_new_gate",
    ]
    assert fixture["audit_results"]["implementation_approved"] is True
    assert fixture["audit_results"]["product_ready"] is False
    assert fixture["audit_results"]["production_ready"] is False
