"""Static checks for the V1 runtime readiness rollup through G55."""

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
    / "v1_runtime_readiness_rollup_through_g55.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_runtime_readiness_rollup_g55_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["rollup_id"] == "v1_runtime_readiness_rollup_through_g55"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "audit-v1-g55-real-provider-sdk-network-egress"

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_runtime_readiness_rollup_g55_required_verdicts() -> None:
    verdicts = _load_fixture()["required_verdicts"]

    assert verdicts["v1_runtime_authority_chain"] == "CANDIDATE_ONLY"
    assert verdicts["real_provider_sdk_network_egress_wrapper_with_caller_injected_executor_only"] == "CANDIDATE_ONLY"
    assert verdicts["built_in_provider_sdk_clients"] == "NOT_APPROVED"
    assert verdicts["lima_owned_provider_endpoint_resolution_execution"] == "NOT_APPROVED"
    assert verdicts["lima_owned_direct_provider_network_egress"] == "NOT_APPROVED"
    assert verdicts["secret_lookup_and_credential_value_access"] == "NOT_APPROVED"
    assert verdicts["fallback_execution"] == "NOT_APPROVED"
    assert verdicts["consumer_production_runtime_integration"] == "NOT_APPROVED"
    assert verdicts["physical_world_readiness"] == "BLOCKED"
    assert verdicts["product_readiness"] == "NOT_READY"


def test_runtime_readiness_rollup_g55_current_status_advances_to_g56_request() -> None:
    current = _load_fixture()["current_status"]

    assert current["latest_completed_gate"] == "V1-G55"
    assert current["latest_authority_chain_audit"] == "V1-G55"
    assert current["latest_readiness_rollup"] == "V1-G55"
    assert current["current_gate"] == "V1-G56"
    assert current["next_recommended_lane"] == (
        "prepare_v1_g56_consumer_fake_executor_provider_sdk_network_egress_smoke_approval_request"
    )
    assert current["next_lane_request_only"] is True
    assert current["v1_product_ready"] is False
    assert current["production_ready"] is False


def test_runtime_readiness_rollup_g55_records_completed_g55_status() -> None:
    status = _load_fixture()["g55_status"]

    assert status["operator_approval_recorded"] is True
    assert status["runtime_implementation_approved"] is True
    assert status["runtime_wrapper_added"] is True
    assert status["public_api_exports_changed"] is True
    assert status["public_api_change_limited_to_approved_harness_exports"] is True
    assert status["independent_audit_complete"] is True
    assert status["caller_injected_provider_sdk_network_executor_only"] is True
    assert status["local_tests_use_fake_injected_executors_only"] is True


def test_runtime_readiness_rollup_g55_blocked_authorities_remain_false() -> None:
    for key, value in _load_fixture()["blocked_authorities"].items():
        assert value is False, key


def test_runtime_readiness_rollup_g55_doc_contains_next_lane_and_boundaries() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["rollup"]).read_text(encoding="utf-8")

    assert "# V1 Runtime Readiness Rollup Through G55" in text
    assert "Real provider SDK/network egress wrapper with caller-injected executor only: `CANDIDATE_ONLY`" in text
    assert "Built-in provider SDK clients: `NOT_APPROVED`" in text
    assert "Secret lookup and credential value access: `NOT_APPROVED`" in text
    assert "Product readiness: `NOT_READY`" in text
    assert "Next recommended lane: prepare a V1-G56 consumer fake-executor provider SDK/network egress smoke approval request." in text
    assert "request-only until approved" in text
