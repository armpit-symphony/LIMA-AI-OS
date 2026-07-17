"""Static checks for the V1 post-G60 next-lane decision matrix."""

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
    / "v1_post_g60_next_lane_decision_matrix.json"
)


def _load_fixture() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def test_post_g60_next_lane_matrix_fixture_and_docs_exist() -> None:
    fixture = _load_fixture()

    assert fixture["matrix_id"] == "v1_post_g60_next_lane_decision_matrix"
    assert fixture["api_status"] == "CANDIDATE_ONLY"
    assert fixture["branch"] == "docs-v1-post-g60-readiness-and-next-lane-matrix"
    assert fixture["source_commit_before_refresh"] == (
        "0550acdbd4cd2c9f1817a0ca163b3b6d3e9d09cc"
    )

    for relative_path in fixture["documents"].values():
        assert (REPO_ROOT / relative_path).exists()


def test_post_g60_next_lane_matrix_recommends_request_only_import_execution_proof() -> None:
    fixture = _load_fixture()

    assert fixture["recommended_next_lane"] == (
        "Runtime vendor SDK import execution proof approval request"
    )
    assert fixture["recommended_next_lane_status"] == "request_only_not_approved"
    assert (
        "G60 SDK dependency declaration and vendor provider SDK import-boundary evidence "
        "is complete"
        in fixture["recommended_next_lane_reason"]
    )
    assert "before any runtime import in lima" in fixture["recommended_next_lane_reason"]


def test_post_g60_next_lane_matrix_order_is_safe() -> None:
    order = _load_fixture()["recommended_order"]

    assert order[0] == "runtime_vendor_sdk_import_execution_proof_approval_request"
    assert order[1] == "runtime_vendor_sdk_import_execution_implementation_lane"
    assert order[2] == "lockfile_policy_update_lane"
    assert "built_in_provider_sdk_client_implementation_lane" in order
    assert "provider_credential_value_access_authority_request" in order
    assert "lima_owned_endpoint_resolution_and_network_egress_lane" in order
    assert order[-1] == "product_readiness_lane"


def test_post_g60_next_lane_matrix_only_first_lane_should_come_next() -> None:
    lanes = {lane["lane"]: lane for lane in _load_fixture()["lanes"]}

    first = lanes["runtime_vendor_sdk_import_execution_proof_approval_request"]
    assert first["should_come_next"] is True
    assert first["request_only"] is True
    assert first["implementation_approved"] is False

    for lane_name, lane in lanes.items():
        if lane_name != "runtime_vendor_sdk_import_execution_proof_approval_request":
            assert lane["should_come_next"] is False, lane_name
            assert lane["implementation_approved"] is False, lane_name


def test_post_g60_next_lane_matrix_blocked_authorities_remain_false() -> None:
    for key, value in _load_fixture()["blocked_authorities"].items():
        assert value is False, key


def test_post_g60_next_lane_matrix_doc_contains_boundaries() -> None:
    fixture = _load_fixture()
    text = (REPO_ROOT / fixture["documents"]["matrix"]).read_text(encoding="utf-8")

    assert "# V1 Post-G60 Next Lane Decision Matrix" in text
    assert "runtime vendor SDK import execution proof lane" in text
    assert "request-only and with no implementation in this branch" in text
    assert "Stop on lockfile edits" in text
    assert "No runtime vendor SDK import execution, lockfile edit" in text
