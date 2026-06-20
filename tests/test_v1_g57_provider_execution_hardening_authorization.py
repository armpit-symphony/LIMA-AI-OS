"""Tests for the approved V1-G57 provider execution hardening authorization slice."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g57_provider_execution_hardening_authorization.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_g57_fixture_records_approved_scope_and_status() -> None:
    fixture = _load_fixture()

    assert fixture["packet_set_id"] == "v1_g57_provider_execution_hardening_authorization"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "v1-g57-provider-execution-hardening-authorization"
    assert fixture["operator_decision"] == "Approve-V1-G57"
    assert fixture["approved_scope"] == (
        "provider_execution_hardening_authorization_metadata_slice"
    )
    assert fixture["required_approval_wording"] == (
        "I explicitly approve V1-G57 implementation of the LIMA-side provider "
        "execution hardening authorization metadata slice, limited to the file "
        "scope, behavior scope, tests, rollback plan, and stop conditions in "
        "docs/V1_G57_PROVIDER_EXECUTION_HARDENING_AUTHORIZATION_APPROVAL_REQUEST.md."
    )
    assert fixture["provider_execution_hardening_authorization_approved"] is True
    assert fixture["provider_execution_hardening_authorization_added"] is True
    assert fixture["provider_execution_hardening_authorization_result"] == (
        "provider_execution_hardening_authorization_metadata_recorded"
    )
    assert fixture["metadata_only"] is True
    assert fixture["docs_tests_fixtures_only"] is True


def test_v1_g57_lima_file_scope_is_exact_and_runtime_unchanged() -> None:
    fixture = _load_fixture()

    assert fixture["approved_lima_runtime_files_changed"] == []
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["lima_public_api_changed"] is False
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["arc_bot_shell_files_changed"] is False
    assert fixture["approved_lima_docs_tests_fixtures_changed"] == [
        "docs/V1_G57_PROVIDER_EXECUTION_HARDENING_AUTHORIZATION.md",
        "docs/V1_G57_PROVIDER_EXECUTION_HARDENING_AUTHORIZATION_CLOSEOUT.md",
        "tests/fixtures/runtime_extraction/v1_g57_provider_execution_hardening_authorization.json",
        "tests/test_v1_g57_provider_execution_hardening_authorization.py",
    ]
    assert fixture["decision_packet_updated"] == (
        "docs/V1_G57_PROVIDER_EXECUTION_HARDENING_AUTHORIZATION_OPERATOR_DECISION_PACKET.md"
    )

    for relative_path in fixture["approved_lima_docs_tests_fixtures_changed"]:
        assert (REPO_ROOT / relative_path).exists()
    assert (REPO_ROOT / fixture["decision_packet_updated"]).exists()


def test_v1_g57_authorization_requirements_are_locked() -> None:
    requirements = _load_fixture()["authorization_requirements"]

    assert requirements == {
        "guardian_gate_required": True,
        "operator_approval_linkage_required": True,
        "sanitized_evidence_only_required": True,
        "credential_reference_metadata_only_required": True,
        "network_policy_reference_metadata_only_required": True,
        "deny_by_default_required": True,
        "links_v1_g48_v1_g53_v1_g54_v1_g55_v1_g56_evidence_required": True,
        "audit_evidence_metadata_is_not_execution_authority": True,
        "approval_metadata_is_not_broad_execution_authority": True,
    }


def test_v1_g57_provider_execution_expansion_and_consumer_runtime_remain_blocked() -> None:
    fixture = _load_fixture()

    assert fixture["provider_execution_expansion_added"] is False
    assert fixture["provider_execution_expansion_approved"] is False
    assert fixture["consumer_repo_mutation_added"] is False
    assert fixture["consumer_runtime_calls_added"] is False
    assert fixture["consumer_production_runtime_integration_added"] is False
    assert fixture["consumer_production_runtime_source_files_changed"] is False
    assert fixture["live_provider_model_call_execution_added"] is False
    assert fixture["provider_sdk_network_egress_invocation_added"] is False

    assert fixture["blocked_future_authorities"] == {
        "built_in_provider_sdk_client_approved": False,
        "provider_secret_lookup_approved": False,
        "provider_credential_value_access_approved": False,
        "lima_owned_provider_endpoint_resolution_approved": False,
        "lima_owned_provider_network_egress_approved": False,
        "fallback_execution_approved": False,
        "connector_browser_network_authority_approved": False,
        "consumer_production_runtime_integration_approved": False,
        "physical_world_authority_approved": False,
        "product_readiness_approved": False,
        "final_public_api_freeze_approved": False,
    }


def test_v1_g57_forbidden_boundaries_remain_false() -> None:
    fixture = _load_fixture()

    for group_name in ("forbidden_boundaries", "sensitive_content_boundaries"):
        for key, value in fixture[group_name].items():
            assert value is False, f"{group_name}.{key}"


def test_v1_g57_future_gates_are_required_before_expansion() -> None:
    fixture = _load_fixture()

    assert fixture["future_required_gates"] == [
        "built_in_provider_sdk_client_approval_request",
        "provider_credential_value_access_approval_request",
        "lima_owned_provider_endpoint_resolution_approval_request",
        "lima_owned_provider_network_egress_approval_request",
        "fallback_execution_approval_request",
        "connector_browser_network_authority_approval_request",
        "consumer_production_runtime_integration_approval_request",
        "physical_world_authority_approval_request",
        "product_readiness_approval_request",
        "final_public_api_freeze_approval_request",
    ]
    assert all(fixture["required_confirmations"].values())


def test_v1_g57_accepted_evidence_refs_exist() -> None:
    for relative_path in _load_fixture()["accepted_evidence_refs"]:
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_v1_g57_decision_packet_records_exact_approval() -> None:
    decision_text = (
        REPO_ROOT
        / "docs"
        / "V1_G57_PROVIDER_EXECUTION_HARDENING_AUTHORIZATION_OPERATOR_DECISION_PACKET.md"
    ).read_text(encoding="utf-8")

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
    assert "Implementation approved: yes." in decision_text


def test_v1_g57_docs_contain_boundary_language() -> None:
    implementation_text = (
        REPO_ROOT
        / "docs"
        / "V1_G57_PROVIDER_EXECUTION_HARDENING_AUTHORIZATION.md"
    ).read_text(encoding="utf-8")
    closeout_text = (
        REPO_ROOT
        / "docs"
        / "V1_G57_PROVIDER_EXECUTION_HARDENING_AUTHORIZATION_CLOSEOUT.md"
    ).read_text(encoding="utf-8")

    assert "metadata-only provider execution hardening authorization" in implementation_text
    assert "No `lima/` runtime file" in implementation_text
    assert "Provider execution expansion added: no" in implementation_text
    assert "Direct provider egress performed by LIMA: no" in implementation_text
    assert "Credential-reference metadata only: yes" in implementation_text
    assert "Network-policy metadata only: yes" in implementation_text
    assert "V1-G57 is complete" in closeout_text
    assert "Product readiness claimed: no" in closeout_text
    assert "Final public API freeze claimed: no" in closeout_text


def test_v1_g57_fixture_and_docs_do_not_include_sensitive_markers() -> None:
    fixture = _load_fixture()
    output = json.dumps(fixture, sort_keys=True)
    output += (
        REPO_ROOT
        / "docs"
        / "V1_G57_PROVIDER_EXECUTION_HARDENING_AUTHORIZATION.md"
    ).read_text(encoding="utf-8")
    output += (
        REPO_ROOT
        / "docs"
        / "V1_G57_PROVIDER_EXECUTION_HARDENING_AUTHORIZATION_CLOSEOUT.md"
    ).read_text(encoding="utf-8")

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
