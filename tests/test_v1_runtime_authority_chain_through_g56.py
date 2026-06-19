"""Static checks for the V1 runtime authority chain through G56."""

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
    / "v1_runtime_authority_chain_through_g56_audit.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_runtime_authority_chain_g56_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["audit_id"] == "v1_runtime_authority_chain_through_g56_audit"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "audit-v1-runtime-authority-chain-through-g56"
    assert fixture["latest_gate"] == "V1-G56"
    assert fixture["audit_verdict"] == (
        "pass_candidate_only_authority_chain_preserved_after_g56"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_runtime_authority_chain_g56_has_complete_chain_position() -> None:
    accepted = _load_fixture()["accepted_chain"]

    assert accepted[0] == "V1-G43"
    assert accepted[-1] == "V1-G56"
    assert "V1-G56" in accepted
    assert len(accepted) == 14


def test_runtime_authority_chain_g56_wrapper_boundary() -> None:
    boundary = _load_fixture()["g56_authority_boundary"]

    assert boundary["consumer_fake_executor_provider_sdk_network_egress_smoke_implemented"] is True
    assert boundary["fake_injected_provider_sdk_network_executor_only"] is True
    assert boundary["public_v1_g55_wrapper_invoked"] is True
    assert boundary["lima_runtime_files_changed"] is False
    assert boundary["lima_public_api_expanded"] is False
    assert boundary["consumer_production_runtime_integration_added"] is False
    assert boundary["built_in_provider_sdk_client_added"] is False
    assert boundary["sdk_dependency_added"] is False
    assert boundary["provider_endpoint_resolution_added"] is False
    assert boundary["lima_owned_network_call_performed"] is False
    assert boundary["direct_provider_egress_performed_by_lima"] is False
    assert boundary["ambient_environment_secret_lookup_added"] is False
    assert boundary["secret_lookup_added"] is False
    assert boundary["credential_value_access_added"] is False
    assert boundary["provider_token_or_api_key_access_added"] is False
    assert boundary["fallback_execution_added"] is False
    assert boundary["connector_browser_network_device_physical_world_behavior_added"] is False
    assert boundary["product_ready"] is False
    assert boundary["production_ready"] is False


def test_runtime_authority_chain_g56_blocked_authorities_remain_false() -> None:
    for key, value in _load_fixture()["still_blocked_authorities"].items():
        assert value is False, key


def test_runtime_authority_chain_g56_doc_contains_required_boundaries() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["chain_audit"]).read_text(
        encoding="utf-8"
    )

    assert "# V1 Runtime Authority Chain Through G56 Audit" in text
    assert "API status: `CANDIDATE_ONLY`" in text
    assert "V1-G56" in text
    assert "fake-executor" in text
    assert "fake in-process provider SDK/network executor only" in text
    assert "does not claim product readiness." in text


def test_runtime_authority_chain_g56_validation_evidence_is_recorded() -> None:
    validation = _load_fixture()["validation_evidence"]

    assert validation["focused_v1_g56_validation"] == {
        "passed": True,
        "tests_passed": 12,
    }
    assert validation["focused_v1_g56_chain_validation"] == {
        "passed": True,
        "tests_passed": 404,
    }
    assert validation["focused_v1_g56_audit_validation"] == {
        "passed": True,
        "tests_passed": 12,
    }
    assert validation["full_lima_suite_before_refresh"] == {
        "passed": True,
        "tests_passed": 4931,
    }


def test_runtime_authority_chain_g56_next_steps_are_metadata_refresh() -> None:
    assert _load_fixture()["next_recommended_steps"] == [
        "v1_runtime_readiness_rollup_through_g56",
        "v1_post_g56_next_lane_decision_matrix",
        "public_sparkbot_branch_push_after_write_credentials",
    ]
