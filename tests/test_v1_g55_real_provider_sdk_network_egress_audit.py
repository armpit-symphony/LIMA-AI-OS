"""Static checks for the V1-G55 real provider SDK/network egress audit."""

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
    / "v1_g55_real_provider_sdk_network_egress_audit.json"
)
G55_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "v1_g55_real_provider_sdk_network_egress.json"
)
RUNTIME_MODULE_PATH = (
    REPO_ROOT / "lima" / "harness" / "v1_real_provider_sdk_network_egress.py"
)


def _load_json(path: Path) -> dict[str, Any]:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _load_fixture() -> dict[str, Any]:
    return _load_json(FIXTURE_PATH)


def _load_g55_fixture() -> dict[str, Any]:
    return _load_json(G55_FIXTURE_PATH)


def test_v1_g55_audit_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["audit_id"] == "v1_g55_real_provider_sdk_network_egress_audit"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "audit-v1-g55-real-provider-sdk-network-egress"
    assert fixture["audit_verdict"] == (
        "pass_bounded_real_provider_sdk_network_egress_authority_slice"
    )
    assert fixture["operator_decision"] == "Approve-V1-G55"
    assert fixture["scope_amendments"] == [
        "Approve-V1-G55-Scope-Amendment",
        "Approve-V1-G55-Scope-Amendment-2",
    ]

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()
    for relative_path in fixture["runtime_files_reviewed"]:
        assert (REPO_ROOT / relative_path).exists()
    for relative_path in fixture["evidence_fixtures_reviewed"]:
        assert (REPO_ROOT / relative_path).exists()
    for relative_path in fixture["tests_reviewed"]:
        assert (REPO_ROOT / relative_path).exists()


def test_v1_g55_audit_matches_implementation_fixture() -> None:
    audit = _load_fixture()
    g55 = _load_g55_fixture()

    assert g55["operator_decision"] == audit["operator_decision"]
    assert g55["api_status"] == audit["api_status"]
    assert g55["branch"] == audit["reviewed_implementation_branch"]
    assert g55["real_provider_sdk_network_egress_authority_wrapper_added"] is True
    assert g55["caller_injected_provider_sdk_network_executor_only"] is True
    assert g55["local_tests_use_fake_injected_executors_only"] is True
    assert g55["approved_lima_runtime_files_changed"] == audit[
        "runtime_files_reviewed"
    ]
    assert audit["audit_results"]["public_api_change_limited_to_approved_harness_exports"] is True
    assert g55["added_harness_exports"] == [
        "V1RealProviderSdkNetworkEgressError",
        "execute_v1_real_provider_sdk_network_egress",
    ]


def test_v1_g55_audit_authority_links_are_required() -> None:
    results = _load_fixture()["audit_results"]

    assert results["requires_v1_g48_credential_network_hardening"] is True
    assert results["requires_v1_g50_invocation_envelope"] is True
    assert results["requires_v1_g51_caller_injected_executor_boundary"] is True
    assert results["requires_v1_g53_provider_sdk_network_credential_authority"] is True
    assert results["requires_v1_g54_fake_sdk_egress_harness_evidence"] is True
    assert results["sanitized_evidence_only"] is True
    assert results["deterministic_record_hashes"] is True


def test_v1_g55_audit_forbidden_boundaries_remain_false() -> None:
    results = _load_fixture()["audit_results"]

    for key in (
        "sparkbot_files_changed",
        "arc_bot_shell_files_changed",
        "consumer_production_runtime_files_changed",
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
        "connector_browser_network_device_physical_world_behavior_added",
        "raw_sensitive_content_persisted",
        "product_ready",
        "production_ready",
    ):
        assert results[key] is False, key


def test_v1_g55_audit_blocked_future_authorities_remain_false() -> None:
    blocked = _load_fixture()["still_blocked_authorities"]

    for key, value in blocked.items():
        assert value is False, key


def test_v1_g55_audit_runtime_source_has_no_direct_provider_or_network_clients() -> None:
    source = RUNTIME_MODULE_PATH.read_text(encoding="utf-8")

    for forbidden in (
        "import requests",
        "import httpx",
        "import urllib",
        "import socket",
        "import subprocess",
        "import openai",
        "import anthropic",
        "import litellm",
        "os.environ",
    ):
        assert forbidden not in source


def test_v1_g55_audit_docs_contain_required_boundary_language() -> None:
    audit = _load_fixture()
    text = (REPO_ROOT / audit["documents"]["audit"]).read_text(encoding="utf-8")

    assert "caller-injected provider SDK/network executor" in text
    assert "LIMA-owned DNS/HTTP/socket/network clients" in text
    assert "Secret lookup remains absent: pass." in text
    assert "Credential value access remains absent: pass." in text
    assert "Fallback execution remains absent: pass." in text
    assert "Product-readiness and production-readiness claims remain absent: pass." in text
    assert "V1-G55 passes independent audit" in text


def test_v1_g55_audit_validation_evidence_is_recorded() -> None:
    validation = _load_fixture()["validation_evidence"]

    assert validation["focused_v1_g55_validation"] == {
        "passed": True,
        "tests_passed": 84,
    }
    assert validation["focused_v1_g55_chain_validation"] == {
        "passed": True,
        "tests_passed": 371,
    }
    assert validation["compileall_lima"] == {"passed": True}
    assert validation["full_lima_suite"] == {
        "passed": True,
        "tests_passed": 4881,
    }


def test_v1_g55_audit_fixture_and_doc_do_not_include_sensitive_markers() -> None:
    output = json.dumps(_load_fixture(), sort_keys=True)
    output += (
        REPO_ROOT / "docs" / "audits" / "V1_G55_REAL_PROVIDER_SDK_NETWORK_EGRESS_AUDIT.md"
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
