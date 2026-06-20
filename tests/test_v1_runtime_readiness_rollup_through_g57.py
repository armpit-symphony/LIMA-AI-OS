"""Static checks for the V1 runtime readiness rollup through G57."""

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
    / "v1_runtime_readiness_rollup_through_g57.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_runtime_readiness_rollup_g57_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["rollup_id"] == "v1_runtime_readiness_rollup_through_g57"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "docs-v1-post-g57-readiness-and-next-lane-matrix"

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_runtime_readiness_rollup_g57_required_verdicts() -> None:
    verdicts = _load_fixture()["required_verdicts"]

    assert verdicts["v1_runtime_authority_chain"] == "CANDIDATE_ONLY"
    assert (
        verdicts["real_provider_sdk_network_egress_wrapper_with_caller_injected_executor_only"]
        == "CANDIDATE_ONLY"
    )
    assert verdicts["consumer_fake_executor_provider_sdk_network_egress_smoke_evidence"] == (
        "CANDIDATE_ONLY"
    )
    assert verdicts["provider_execution_hardening_authorization_metadata"] == (
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
    assert verdicts["final_public_api_freeze"] == "NOT_APPROVED"


def test_runtime_readiness_rollup_g57_current_status_advances_with_g57_evidence() -> None:
    current = _load_fixture()["current_status"]

    assert current["latest_completed_gate"] == "V1-G57"
    assert current["latest_independent_audit"] == "V1-G57"
    assert current["latest_readiness_rollup"] == "V1-G57"
    assert current["current_gate"] == "built_in_provider_sdk_client_authority_contract_request"
    assert current["next_lane_request_only"] is True
    assert current["v1_product_ready"] is False
    assert current["production_ready"] is False


def test_runtime_readiness_rollup_g57_status() -> None:
    status = _load_fixture()["g57_status"]

    assert status["provider_execution_hardening_authorization_approved"] is True
    assert status["provider_execution_hardening_authorization_implemented"] is True
    assert status["provider_execution_hardening_authorization_audited"] is True
    assert status["metadata_only"] is True
    assert status["lima_runtime_files_changed"] is False
    assert status["lima_public_api_expanded"] is False
    assert status["sparkbot_files_changed"] is False
    assert status["arc_bot_shell_files_changed"] is False
    assert status["consumer_production_runtime_integration_added"] is False
    assert status["provider_execution_expansion_added"] is False
    assert status["product_readiness_claimed"] is False
    assert status["final_public_api_freeze_approved"] is False


def test_runtime_readiness_rollup_g57_blocked_authorities_remain_false() -> None:
    for key, value in _load_fixture()["blocked_authorities"].items():
        assert value is False, key


def test_runtime_readiness_rollup_g57_validation_evidence_is_recorded() -> None:
    validation = _load_fixture()["validation_evidence"]

    assert validation["focused_v1_g57_validation"] == {
        "passed": True,
        "tests_passed": 10,
    }
    assert validation["focused_v1_g57_audit_validation"] == {
        "passed": True,
        "tests_passed": 10,
    }
    assert validation["focused_v1_g57_rollup_validation"] == {
        "passed": True,
        "tests_passed": 273,
    }
    assert validation["full_lima_suite_before_refresh"] == {
        "passed": True,
        "tests_passed": 5091,
    }


def test_runtime_readiness_rollup_g57_doc_contains_next_lane_and_boundaries() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["rollup"]).read_text(encoding="utf-8")

    assert "# V1 Runtime Readiness Rollup Through G57" in text
    assert "Provider execution hardening authorization metadata: `CANDIDATE_ONLY`" in text
    assert "Built-in provider SDK clients: `NOT_APPROVED`" in text
    assert "Secret lookup and credential value access: `NOT_APPROVED`" in text
    assert "Final public API freeze: `NOT_APPROVED`" in text
    assert "Product readiness: `NOT_READY`" in text
    assert "built-in provider SDK client authority contract lane" in text
