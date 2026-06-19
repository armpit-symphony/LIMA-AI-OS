"""Static checks for the V1 runtime readiness rollup through G56."""

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
    / "v1_runtime_readiness_rollup_through_g56.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_runtime_readiness_rollup_g56_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["rollup_id"] == "v1_runtime_readiness_rollup_through_g56"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "audit-v1-runtime-authority-chain-through-g56"

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_runtime_readiness_rollup_g56_required_verdicts() -> None:
    verdicts = _load_fixture()["required_verdicts"]

    assert verdicts["v1_runtime_authority_chain"] == "CANDIDATE_ONLY"
    assert (
        verdicts["real_provider_sdk_network_egress_wrapper_with_caller_injected_executor_only"]
        == "CANDIDATE_ONLY"
    )
    assert verdicts["consumer_fake_executor_provider_sdk_network_egress_smoke_evidence"] == (
        "CANDIDATE_ONLY"
    )
    assert verdicts["built_in_provider_sdk_clients"] == "NOT_APPROVED"
    assert verdicts["lima_owned_provider_endpoint_resolution_execution"] == "NOT_APPROVED"
    assert verdicts["lima_owned_direct_provider_network_egress"] == "NOT_APPROVED"
    assert verdicts["secret_lookup_and_credential_value_access"] == "NOT_APPROVED"
    assert verdicts["fallback_execution"] == "NOT_APPROVED"
    assert verdicts["consumer_production_runtime_integration"] == "NOT_APPROVED"
    assert verdicts["physical_world_readiness"] == "BLOCKED"
    assert verdicts["product_readiness"] == "NOT_READY"


def test_runtime_readiness_rollup_g56_current_status_advances_with_g56_evidence() -> None:
    current = _load_fixture()["current_status"]

    assert current["latest_completed_gate"] == "V1-G56"
    assert current["latest_authority_chain_audit"] == "V1-G56"
    assert current["latest_readiness_rollup"] == "V1-G56"
    assert current["current_gate"] == "provider_sdk_network_egress_execution_request"
    assert current["next_lane_request_only"] is True
    assert current["v1_product_ready"] is False
    assert current["production_ready"] is False


def test_runtime_readiness_rollup_g56_g56_status() -> None:
    status = _load_fixture()["g56_status"]

    assert status["consumer_fake_executor_provider_sdk_network_egress_smoke_approved"] is True
    assert status["consumer_fake_executor_provider_sdk_network_egress_smoke_implemented"] is True
    assert status["lima_runtime_files_changed"] is False
    assert status["lima_public_api_expanded"] is False
    assert status["consumer_production_runtime_integration_added"] is False
    assert status["independent_audit_complete"] is True
    assert status["public_sparkbot_branch_push_blocked"] is True
    assert status["arc_bot_shell_pushed"] is True


def test_runtime_readiness_rollup_g56_blocked_authorities_remain_false() -> None:
    for key, value in _load_fixture()["blocked_authorities"].items():
        assert value is False, key


def test_runtime_readiness_rollup_g56_validation_evidence_is_recorded() -> None:
    validation = _load_fixture()["validation_evidence"]

    assert validation["focused_v1_g56_validation"] == {
        "passed": True,
        "tests_passed": 12,
    }
    assert validation["focused_v1_g56_rollup_validation"] == {
        "passed": True,
        "tests_passed": 404,
    }
    assert validation["full_lima_suite_before_refresh"] == {
        "passed": True,
        "tests_passed": 4931,
    }


def test_runtime_readiness_rollup_g56_doc_contains_next_lane_and_boundaries() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["rollup"]).read_text(encoding="utf-8")

    assert "# V1 Runtime Readiness Rollup Through G56" in text
    assert "Real provider SDK/network egress wrapper with caller-injected executor only: `CANDIDATE_ONLY`" in text
    assert "Built-in provider SDK clients: `NOT_APPROVED`" in text
    assert "Secret lookup and credential value access: `NOT_APPROVED`" in text
    assert "Product readiness: `NOT_READY`" in text
