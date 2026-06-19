"""Static checks for the V1 runtime authority chain audit through G55."""

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
    / "v1_runtime_authority_chain_through_g55_audit.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_runtime_authority_chain_g55_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["audit_id"] == "v1_runtime_authority_chain_through_g55_audit"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "audit-v1-g55-real-provider-sdk-network-egress"
    assert fixture["latest_gate"] == "V1-G55"
    assert fixture["audit_verdict"] == (
        "pass_candidate_only_authority_chain_preserved_after_g55"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_runtime_authority_chain_g55_has_complete_chain_position() -> None:
    accepted = _load_fixture()["accepted_chain"]

    assert accepted[0] == "V1-G43"
    assert accepted[-1] == "V1-G55"
    assert "V1-G54" in accepted
    assert len(accepted) == 13


def test_runtime_authority_chain_g55_wrapper_boundary() -> None:
    boundary = _load_fixture()["g55_authority_boundary"]

    assert boundary["real_provider_sdk_network_egress_wrapper_added"] is True
    assert boundary["caller_injected_provider_sdk_network_executor_only"] is True
    assert boundary["local_tests_use_fake_injected_executors_only"] is True
    assert boundary["requires_v1_g48_credential_network_hardening"] is True
    assert boundary["requires_v1_g50_invocation_envelope"] is True
    assert boundary["requires_v1_g51_caller_injected_executor_boundary"] is True
    assert boundary["requires_v1_g53_provider_sdk_network_credential_authority"] is True
    assert boundary["requires_v1_g54_fake_sdk_egress_harness_evidence"] is True
    assert boundary["sanitized_evidence_only"] is True


def test_runtime_authority_chain_g55_forbidden_boundaries_remain_false() -> None:
    boundary = _load_fixture()["g55_authority_boundary"]

    for key in (
        "built_in_provider_sdk_client_added",
        "sdk_dependency_added",
        "vendor_provider_sdk_import_added",
        "direct_provider_sdk_implementation_added",
        "lima_owned_endpoint_resolution_added",
        "lima_owned_dns_http_socket_network_call_added",
        "lima_owned_network_call_performed",
        "lima_owned_direct_provider_egress_performed",
        "secret_lookup_added",
        "credential_value_access_added",
        "provider_token_or_api_key_access_added",
        "provider_configuration_changes_added",
        "fallback_execution_added",
        "consumer_production_runtime_integration_added",
        "connector_browser_network_device_physical_world_behavior_added",
        "product_ready",
        "production_ready",
    ):
        assert boundary[key] is False, key


def test_runtime_authority_chain_g55_blocked_authorities_remain_false() -> None:
    for key, value in _load_fixture()["still_blocked_authorities"].items():
        assert value is False, key


def test_runtime_authority_chain_g55_doc_contains_required_boundaries() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["chain_audit"]).read_text(
        encoding="utf-8"
    )

    assert "# V1 Runtime Authority Chain Through G55 Audit" in text
    assert "API status: `CANDIDATE_ONLY`" in text
    assert "caller-injected provider SDK/network executor" in text
    assert "G55 expands `lima.harness` exports only by the two approved wrapper symbols" in text
    assert "LIMA-owned DNS/HTTP/socket/network clients" in text
    assert "Secret lookup and credential value access remain blocked." in text
    assert "Product readiness remains blocked." in text
    assert "The V1 runtime authority chain through G55 remains candidate-only" in text


def test_runtime_authority_chain_g55_validation_evidence_is_recorded() -> None:
    validation = _load_fixture()["validation_evidence"]

    assert validation["focused_v1_g55_validation"] == {
        "passed": True,
        "tests_passed": 84,
    }
    assert validation["focused_v1_g55_chain_validation"] == {
        "passed": True,
        "tests_passed": 371,
    }
    assert validation["focused_v1_g55_audit_validation"] == {
        "passed": True,
        "tests_passed": 93,
    }
    assert validation["full_lima_suite_before_refresh"] == {
        "passed": True,
        "tests_passed": 4881,
    }


def test_runtime_authority_chain_g55_next_steps_are_metadata_only() -> None:
    assert _load_fixture()["next_recommended_steps"] == [
        "v1_runtime_readiness_rollup_through_g55",
        "v1_post_g55_next_lane_decision_matrix",
        "prepare_v1_g56_consumer_fake_executor_provider_sdk_network_egress_smoke_approval_request",
    ]
