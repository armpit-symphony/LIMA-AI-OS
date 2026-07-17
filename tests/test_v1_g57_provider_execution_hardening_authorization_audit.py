"""Static checks for the V1-G57 provider execution hardening authorization audit."""

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
    / "v1_g57_provider_execution_hardening_authorization_audit.json"
)
G57_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g57_provider_execution_hardening_authorization.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _load_audit_fixture() -> dict[str, Any]:
    return _load_json(AUDIT_FIXTURE_PATH)


def _load_g57_fixture() -> dict[str, Any]:
    return _load_json(G57_FIXTURE_PATH)


def test_v1_g57_audit_fixture_and_docs_exist() -> None:
    fixture = _load_audit_fixture()

    assert fixture["audit_id"] == "v1_g57_provider_execution_hardening_authorization_audit"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "audit-v1-g57-provider-execution-hardening-authorization"
    assert fixture["source_branch"] == "v1-g57-provider-execution-hardening-authorization"
    assert fixture["source_commit_before_audit"] == (
        "60397aef5b11c8ccc9757143ab55185a836bd66a"
    )
    assert fixture["audit_verdict"] == "PASS"
    assert fixture["operator_decision"] == "Approve-V1-G57"

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path
    for relative_path in fixture["lima_files_reviewed"]:
        assert (REPO_ROOT / relative_path).exists(), relative_path
    for relative_path in fixture["evidence_fixtures_reviewed"]:
        assert (REPO_ROOT / relative_path).exists(), relative_path
    for relative_path in fixture["tests_reviewed"]:
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_g57_audit_matches_implementation_fixture() -> None:
    audit = _load_audit_fixture()
    g57 = _load_g57_fixture()

    assert g57["operator_decision"] == audit["operator_decision"]
    assert g57["api_status"] == audit["api_status"]
    assert g57["branch"] == audit["source_branch"]
    assert g57["approved_scope"] == audit["approved_scope"]
    assert g57["provider_execution_hardening_authorization_added"] is True
    assert g57["approved_lima_docs_tests_fixtures_changed"] == audit[
        "lima_files_reviewed"
    ]
    assert g57["approved_lima_runtime_files_changed"] == audit[
        "lima_runtime_files_reviewed"
    ]
    assert g57["lima_runtime_files_changed"] is False
    assert g57["lima_public_api_changed"] is False
    assert g57["metadata_only"] is True


def test_v1_g57_audit_operator_decision_is_exact() -> None:
    audit = _load_audit_fixture()
    decision_text = (REPO_ROOT / audit["decision_packet_reviewed"]).read_text(
        encoding="utf-8"
    )

    assert "Decision packet status: `approved`" in decision_text
    assert "Recorded choice: Approve-V1-G57" in decision_text
    assert (
        "Recorded approval wording: I explicitly approve V1-G57 implementation "
        "of the LIMA-side provider execution hardening authorization metadata "
        "slice, limited to the file scope, behavior scope, tests, rollback plan, "
        "and stop conditions in "
        "docs/V1_G57_PROVIDER_EXECUTION_HARDENING_AUTHORIZATION_APPROVAL_REQUEST.md."
        in decision_text
    )
    assert (
        "Approved implementation branch: "
        "`v1-g57-provider-execution-hardening-authorization`"
        in decision_text
    )


def test_v1_g57_audit_authorization_requirements_match_implementation() -> None:
    audit_results = _load_audit_fixture()["audit_results"]
    requirements = _load_g57_fixture()["authorization_requirements"]

    assert audit_results["guardian_gate_required"] is True
    assert audit_results["operator_approval_linkage_required"] is True
    assert audit_results["deny_by_default_required"] is True
    assert audit_results["credential_reference_metadata_only"] is True
    assert audit_results["network_policy_reference_metadata_only"] is True
    assert audit_results["sanitized_evidence_only"] is True
    assert audit_results["audit_evidence_metadata_is_not_execution_authority"] is True
    assert audit_results["approval_metadata_is_not_broad_execution_authority"] is True
    assert audit_results["v1_g48_g53_g54_g55_g56_evidence_linked"] is True
    assert requirements["guardian_gate_required"] is True
    assert requirements["operator_approval_linkage_required"] is True
    assert requirements["deny_by_default_required"] is True
    assert requirements["links_v1_g48_v1_g53_v1_g54_v1_g55_v1_g56_evidence_required"]


def test_v1_g57_audit_forbidden_boundaries_remain_false() -> None:
    results = _load_audit_fixture()["audit_results"]

    for key in (
        "lima_runtime_files_changed",
        "lima_public_api_changed",
        "lima_runtime_behavior_added_by_v1_g57",
        "sparkbot_files_changed",
        "arc_bot_shell_files_changed",
        "consumer_production_runtime_source_files_changed",
        "consumer_runtime_calls_added",
        "consumer_integration_added",
        "provider_execution_expansion_added",
        "provider_execution_expansion_approved",
        "live_provider_model_call_execution_added",
        "built_in_provider_sdk_client_added",
        "sdk_dependency_added",
        "vendor_provider_sdk_import_added",
        "direct_provider_sdk_added",
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


def test_v1_g57_audit_blocked_future_authorities_remain_false() -> None:
    blocked = _load_audit_fixture()["still_blocked_authorities"]

    for key, value in blocked.items():
        assert value is False, key


def test_v1_g57_audit_validation_evidence_is_recorded() -> None:
    fixture = _load_audit_fixture()
    validation = fixture["validation_evidence"]
    audit_validation = fixture["audit_branch_validation_evidence"]

    assert validation["focused_v1_g57_validation"] == {
        "passed": True,
        "tests_passed": 10,
    }
    assert validation["focused_v1_g57_request_and_implementation_validation"] == {
        "passed": True,
        "tests_passed": 19,
    }
    assert validation[
        "focused_v1_g57_g56_g55_g54_g53_g48_authority_readiness_validation"
    ] == {
        "passed": True,
        "tests_passed": 263,
    }
    assert validation["compileall_lima"] == {"passed": True}
    assert validation["full_lima_suite"] == {"passed": True, "tests_passed": 5081}
    assert audit_validation["focused_v1_g57_audit_validation"] == {
        "passed": True,
        "tests_passed": 10,
    }
    assert audit_validation["focused_v1_g57_audit_chain_validation"] == {
        "passed": True,
        "tests_passed": 273,
    }
    assert audit_validation["compileall_lima"] == {"passed": True}
    assert audit_validation["full_lima_suite"] == {
        "passed": True,
        "tests_passed": 5091,
    }


def test_v1_g57_audit_docs_contain_required_boundary_language() -> None:
    audit = _load_audit_fixture()
    text = (REPO_ROOT / audit["documents"]["audit"]).read_text(encoding="utf-8")

    assert "Audit verdict: `PASS`" in text
    assert "metadata-only provider execution hardening authorization" in text
    assert "LIMA `lima/` runtime files changed by V1-G57: none, pass." in text
    assert "Provider execution expansion remains unapproved and unimplemented: pass." in text
    assert "Direct provider egress by LIMA remains absent: pass." in text
    assert "Final public API freeze remains unapproved: pass." in text
    assert "V1-G57 passes independent audit" in text


def test_v1_g57_audit_fixture_and_doc_do_not_include_sensitive_markers() -> None:
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


def test_v1_g57_audit_next_steps_remain_bounded() -> None:
    fixture = _load_audit_fixture()

    assert fixture["next_recommended_steps"] == [
        "post_g57_readiness_refresh",
        "post_g57_next_lane_decision_matrix",
        "prepare_next_explicit_operator_gate",
    ]
    assert fixture["audit_results"]["product_ready"] is False
    assert fixture["audit_results"]["production_ready"] is False
