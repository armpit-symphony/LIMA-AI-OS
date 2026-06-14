"""Static case checks for V1-G3 destructive operator approval."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = REPO_ROOT / "tests" / "fixtures" / "runtime_extraction"
CASE_NAMES = (
    "v1_g3_delete_file_requires_operator_approval.json",
    "v1_g3_edit_file_requires_operator_approval.json",
    "v1_g3_overwrite_existing_content_requires_operator_approval.json",
    "v1_g3_delete_memory_record_requires_operator_approval.json",
    "v1_g3_connector_customer_record_mutation_requires_operator_approval.json",
    "v1_g3_safe_draft_preview_no_operator_approval_required.json",
    "v1_g3_approval_bypass_claim_fail_closed.json",
)


def _load_json(path: Path) -> dict[str, Any]:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _cases() -> list[dict[str, Any]]:
    return [_load_json(FIXTURE_DIR / name) for name in CASE_NAMES]


def test_v1_g3_case_fixture_files_exist() -> None:
    for fixture_name in CASE_NAMES:
        assert (FIXTURE_DIR / fixture_name).exists()


def test_v1_g3_destructive_cases_require_operator_approval() -> None:
    destructive_cases = [
        case
        for case in _cases()
        if case["case_family"]
        in {"destructive_requires_operator_approval", "approval_bypass_fail_closed"}
    ]
    assert {case["action"]["action_type"] for case in destructive_cases} == {
        "delete_file",
        "edit_file",
        "overwrite_existing_content",
        "delete_memory_record",
        "connector_customer_record_mutation",
    }
    for case in destructive_cases:
        assert case["docs_tests_fixtures_only"] is True
        assert case["action"]["destructive"] is True
        assert case["action"]["mutates_existing_state"] is True
        approval = case["operator_approval_metadata"]
        assert approval["operator_approval_required"] is True
        assert approval["operator_approval_state"] in {
            "missing",
            "required_not_granted",
            "expired",
            "revoked",
            "denied",
        }
        assert approval["approval_granted"] is False
        assert case["static_review_result"]["accepted_as_approval"] is False


def test_v1_g3_destructive_cases_map_to_blocked_or_explain_plan() -> None:
    for case in _cases():
        if case["action"]["destructive"] is False:
            continue
        assert case["packet_status"] in {"blocked", "explain_plan"}
        assert case["packet_status"] != "preview_only"
        if case["kernel_status"] == "needs_review":
            assert case["packet_status"] == "explain_plan"
        if case["kernel_status"] == "blocked":
            assert case["packet_status"] == "blocked"


def test_v1_g3_safe_draft_preview_needs_no_operator_approval_and_stays_inert() -> None:
    safe_case = [
        case
        for case in _cases()
        if case["case_id"] == "v1_g3_safe_draft_preview_no_operator_approval_required"
    ][0]
    assert safe_case["action"]["destructive"] is False
    assert safe_case["action"]["mutates_existing_state"] is False
    assert safe_case["operator_approval_metadata"]["operator_approval_required"] is False
    assert safe_case["operator_approval_metadata"]["approval_granted"] is False
    assert safe_case["kernel_status"] == "proposed"
    assert safe_case["packet_status"] == "preview_only"
    assert safe_case["expected_blocked_claims"] == []
    assert safe_case["static_review_result"]["result"] == "preview_only_no_operator_approval_required"


def test_v1_g3_static_approval_bypass_claim_fails_closed() -> None:
    bypass = [
        case for case in _cases() if case["case_id"] == "v1_g3_approval_bypass_claim_fail_closed"
    ][0]
    claimed = bypass["claimed_operator_approval_metadata"]
    assert claimed["operator_approval_state"] == "granted"
    assert claimed["approval_granted"] is True
    assert claimed["approval_id"] == "claimed-static-approval"
    actual = bypass["operator_approval_metadata"]
    assert actual["operator_approval_state"] == "required_not_granted"
    assert actual["approval_granted"] is False
    assert actual["approval_id"] is None
    review = bypass["static_review_result"]
    assert review["claimed_granted_state_rejected"] is True
    assert review["accepted_as_approval"] is False
    assert bypass["packet_status"] == "blocked"
    assert "approval_bypass_claim" in bypass["expected_blocked_claims"]
    assert "static_granted_state_claim" in bypass["expected_blocked_claims"]


def test_v1_g3_cases_never_create_runtime_authority_or_side_effects() -> None:
    for case in _cases():
        decision = case["future_guardian_decision_metadata"]
        assert decision["state"] in {"absent", "pending", "blocked"}
        assert decision["decision_id"] is None
        assert decision["approval_granted"] is False
        assert decision["execution_allowed"] is False
        flags = case["control_flags"]
        assert flags["non_authoritative"] is True
        assert flags["safe_by_default"] is True
        assert flags["local_only"] is True
        assert flags["deterministic"] is True
        for key in (
            "execution_allowed",
            "dispatch_allowed",
            "persistence_allowed",
            "approval_granted",
            "external_calls_allowed",
            "provider_model_routing_allowed",
            "model_calls_allowed",
            "tool_calls_allowed",
            "driver_calls_allowed",
            "adapter_calls_allowed",
            "file_mutation_allowed",
            "connector_mutation_allowed",
            "browser_file_network_device_robotics_allowed",
            "haptic_device_behavior_allowed",
            "physical_world_allowed",
            "guardian_decision_created",
            "runtime_test_harness_active",
        ):
            assert flags[key] is False


def test_v1_g3_case_suite_does_not_touch_runtime_or_support_paths() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*v1_g3*"))
    support = REPO_ROOT / "tests" / "support"
    if support.exists():
        assert not list(support.rglob("*v1_g3*"))
