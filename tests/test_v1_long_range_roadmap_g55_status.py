"""Static checks for the V1 long-range roadmap post-G55 status."""

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
    / "v1_long_range_roadmap_g55_status.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_v1_long_range_roadmap_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["status_id"] == "v1_long_range_roadmap_g56_status"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == (
        "prepare-v1-g56-consumer-fake-executor-provider-sdk-network-egress-smoke-approval-request"
    )
    assert fixture["source_commit_before_refresh"] == (
        "146f8a7d934567b7c551af2c5db775215b47cf88"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_v1_long_range_roadmap_current_gate_is_g56_request_prep() -> None:
    fixture = _load_fixture()

    assert fixture["current_gate"] == "V1-G56"
    assert fixture["latest_completed_gate"] == "V1-G55"
    assert fixture["request_packet_prepared"] is True
    assert fixture["operator_approval_recorded"] is False
    assert fixture["runtime_implementation_approved"] is False
    assert fixture["valid_operator_choices"] == [
        "Approve-V1-G56",
        "Revise-V1-G56",
        "Pause",
    ]
    assert fixture["v1_product_ready"] is False
    assert fixture["production_ready"] is False
    assert fixture["next_smallest_safe_step"] == "record_v1_g56_operator_decision"


def test_v1_long_range_roadmap_refresh_adds_no_forbidden_behavior() -> None:
    forbidden = _load_fixture()["forbidden_by_refresh"]

    for key in (
        "runtime_behavior_added",
        "lima_runtime_files_changed",
        "public_api_exports_changed",
        "sparkbot_or_arc_bot_shell_changed",
        "g56_consumer_fake_executor_smoke_implementation_added",
        "built_in_provider_sdk_client_added",
        "sdk_dependency_added",
        "vendor_sdk_import_added",
        "provider_endpoint_resolution_by_lima_added",
        "network_call_performed_by_lima",
        "secret_lookup_added",
        "credential_value_access_added",
        "provider_token_or_api_key_access_added",
        "provider_configuration_changes_added",
        "fallback_execution_added",
        "consumer_production_runtime_integration_added",
        "connector_browser_network_file_device_robotics_physical_world_behavior_added",
    ):
        assert forbidden[key] is False, key


def test_v1_long_range_roadmap_text_points_to_g56_request_prep() -> None:
    fixture = _load_fixture()
    text = (
        REPO_ROOT / fixture["documents"]["long_range_roadmap"]
    ).read_text(encoding="utf-8")

    assert "## V1 Product Readiness Target" in text
    assert "public `Sparkbot`" in text
    assert "The active V1 gate is now operator decision for the prepared `V1-G56` request." in text
    assert "audited through `V1-G55`" in text
    assert "V1-G56 consumer fake-executor provider SDK/network egress smoke approval request is prepared" in text
    assert "Current V1-G55 authority documents:" in text
    assert "`docs/audits/V1_G55_REAL_PROVIDER_SDK_NETWORK_EGRESS_AUDIT.md`" in text
    assert "`docs/readiness/V1_POST_G55_NEXT_LANE_DECISION_MATRIX.md`" in text
    assert "Current V1-G56 authority request documents:" in text
    assert "`docs/V1_G56_CONSUMER_FAKE_EXECUTOR_PROVIDER_SDK_NETWORK_EGRESS_SMOKE_OPERATOR_DECISION_PACKET.md`" in text
    assert (
        "The next smallest safe V1 action is to record exactly one operator choice "
        "in the V1-G56 consumer fake-executor provider SDK/network egress smoke operator decision packet"
    ) in text
    assert "`Approve-V1-G56`, `Revise-V1-G56`, or `Pause`" in text
    assert "fake in-process caller-injected provider SDK/network executors" in text
    assert "built-in provider SDK clients" in text
    assert "LIMA-owned DNS/HTTP/socket/network calls" in text
    assert "secret lookup, credential value access" in text
    assert "product-readiness claims" in text
    assert "This roadmap update is product-direction evidence only." in text
