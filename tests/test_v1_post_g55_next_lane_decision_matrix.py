"""Static checks for the V1 post-G55 next-lane decision matrix."""

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
    / "v1_post_g55_next_lane_decision_matrix.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_post_g55_next_lane_matrix_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["matrix_id"] == "v1_post_g55_next_lane_decision_matrix"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "audit-v1-g55-real-provider-sdk-network-egress"

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_post_g55_next_lane_matrix_recommends_g56_request_only() -> None:
    fixture = _load_fixture()

    assert fixture["recommended_next_lane"] == (
        "V1-G56 consumer fake-executor provider SDK/network egress smoke approval request"
    )
    assert fixture["recommended_next_lane_slug"] == (
        "prepare-v1-g56-consumer-fake-executor-provider-sdk-network-egress-smoke-approval-request"
    )
    assert fixture["recommended_next_lane_status"] == "request_only_not_approved"
    assert "fake_injected_sdk_network_executors" in fixture["recommended_next_lane_reason"]


def test_post_g55_next_lane_matrix_order_is_safe() -> None:
    order = _load_fixture()["recommended_order"]

    assert order[0] == "consumer_fake_executor_provider_sdk_network_egress_smoke_approval_request"
    assert order[1] == "consumer_fake_executor_provider_sdk_network_egress_smoke_implementation_after_exact_approval"
    assert "credential_value_access_approval_request" in order[2]
    assert order[-1] == "product_readiness_lane"


def test_post_g55_next_lane_matrix_only_first_lane_should_come_next() -> None:
    lanes = {lane["lane"]: lane for lane in _load_fixture()["lanes"]}

    assert lanes["consumer_fake_executor_provider_sdk_network_egress_smoke_approval_request"]["should_come_next"] is True
    assert lanes["consumer_fake_executor_provider_sdk_network_egress_smoke_approval_request"]["request_only"] is True
    assert lanes["consumer_fake_executor_provider_sdk_network_egress_smoke_approval_request"]["implementation_approved"] is False

    for lane_name, lane in lanes.items():
        if lane_name != "consumer_fake_executor_provider_sdk_network_egress_smoke_approval_request":
            assert lane["should_come_next"] is False, lane_name
            assert lane["implementation_approved"] is False, lane_name


def test_post_g55_next_lane_matrix_blocked_authorities_remain_false() -> None:
    for key, value in _load_fixture()["blocked_authorities"].items():
        assert value is False, key


def test_post_g55_next_lane_matrix_doc_contains_stop_conditions() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["matrix"]).read_text(encoding="utf-8")

    assert "# V1 Post-G55 Next Lane Decision Matrix" in text
    assert "Recommended next lane: `V1-G56 consumer fake-executor provider SDK/network egress smoke approval request`." in text
    assert "with fake in-process provider SDK/network executors only" in text
    assert "Stop on consumer repo edits" in text
    assert "Credential value access approval request" in text
    assert "Product-readiness lane only after runtime, security, field operations, support, rollback, and incident evidence exist" in text
    assert "Do not start consumer fake-executor smoke implementation" in text
