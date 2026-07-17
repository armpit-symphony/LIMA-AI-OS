"""Static checks for the V1 post-G56 next-lane decision matrix."""

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
    / "v1_post_g56_next_lane_decision_matrix.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_post_g56_next_lane_matrix_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["matrix_id"] == "v1_post_g56_next_lane_decision_matrix"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "audit-v1-runtime-authority-chain-through-g56"

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_post_g56_next_lane_matrix_recommends_execution_request_next() -> None:
    fixture = _load_fixture()

    assert fixture["recommended_next_lane"] == "provider execution/authority hardening request"
    assert fixture["recommended_next_lane_status"] == "request_only_not_approved"
    assert "provider execution" in fixture["recommended_next_lane_reason"]
    assert "explicit approvals" in fixture["recommended_next_lane_reason"]


def test_post_g56_next_lane_matrix_order_is_safe() -> None:
    order = _load_fixture()["recommended_order"]

    assert order[0] == "provider_sdk_network_egress_execution_request"
    assert order[1] == "provider_sdk_network_hardening_extension_request"
    assert order[-1] == "product_readiness_lane"


def test_post_g56_next_lane_matrix_only_first_lane_should_come_next() -> None:
    lanes = {lane["lane"]: lane for lane in _load_fixture()["lanes"]}

    assert lanes["provider_sdk_network_egress_execution_request"]["should_come_next"] is True
    assert lanes["provider_sdk_network_egress_execution_request"]["request_only"] is True
    assert lanes["provider_sdk_network_egress_execution_request"][
        "implementation_approved"
    ] is False

    for lane_name, lane in lanes.items():
        if lane_name != "provider_sdk_network_egress_execution_request":
            assert lane["should_come_next"] is False, lane_name
            assert lane["implementation_approved"] is False, lane_name


def test_post_g56_next_lane_matrix_blocked_authorities_remain_false() -> None:
    for key, value in _load_fixture()["blocked_authorities"].items():
        assert value is False, key


def test_post_g56_next_lane_matrix_doc_contains_boundaries() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["matrix"]).read_text(encoding="utf-8")

    assert "# V1 Post-G56 Next Lane Decision Matrix" in text
    assert "provider execution hardening" in text
    assert "Stop on credentials, built-in SDK clients" in text
    assert "No provider runtime behavior may be added" in text
