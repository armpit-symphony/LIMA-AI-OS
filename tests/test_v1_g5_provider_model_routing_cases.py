"""Static case checks for V1-G5 provider/model routing."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = REPO_ROOT / "tests" / "fixtures" / "runtime_extraction"
CASE_NAMES = (
    "v1_g5_safe_openai_route_shape.json",
    "v1_g5_private_data_requires_guardian_review.json",
    "v1_g5_expensive_model_requires_budget_review.json",
    "v1_g5_unknown_provider_denied.json",
    "v1_g5_missing_secret_ref_blocks_route.json",
    "v1_g5_tool_capable_model_without_tool_scope_blocked.json",
    "v1_g5_shell_disallowed_provider_denied.json",
    "v1_g5_forged_route_decision_fail_closed.json",
)


def _load_json(path: Path) -> dict[str, Any]:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _cases() -> list[dict[str, Any]]:
    return [_load_json(FIXTURE_DIR / name) for name in CASE_NAMES]


def test_v1_g5_case_fixture_files_exist() -> None:
    for fixture_name in CASE_NAMES:
        assert (FIXTURE_DIR / fixture_name).exists()


def test_v1_g5_cases_cover_required_gate_failures() -> None:
    cases = {case["case_id"]: case for case in _cases()}
    assert set(cases) == {
        "v1_g5_safe_openai_route_shape",
        "v1_g5_private_data_requires_guardian_review",
        "v1_g5_expensive_model_requires_budget_review",
        "v1_g5_unknown_provider_denied",
        "v1_g5_missing_secret_ref_blocks_route",
        "v1_g5_tool_capable_model_without_tool_scope_blocked",
        "v1_g5_shell_disallowed_provider_denied",
        "v1_g5_forged_route_decision_fail_closed",
    }
    blocked_claims: set[str] = set()
    for case in cases.values():
        blocked_claims.update(case["expected_blocked_claims"])
    assert "private_data_without_guardian_review" in blocked_claims
    assert "expensive_model_without_budget_review" in blocked_claims
    assert "unknown_provider_claim" in blocked_claims
    assert "missing_secret_ref" in blocked_claims
    assert "tool_pack_scope_bypass_claim" in blocked_claims
    assert "shell_disallowed_provider" in blocked_claims
    assert "forged_route_decision" in blocked_claims


def test_v1_g5_safe_route_shape_stays_preview_only_and_non_executing() -> None:
    safe_case = [
        case for case in _cases() if case["case_id"] == "v1_g5_safe_openai_route_shape"
    ][0]
    assert safe_case["case_family"] == "safe_route_shape_static_only"
    assert safe_case["routing_gates"]["shell_allows_model_pack"] is True
    assert safe_case["routing_gates"]["guardian_decision_allows_model_routing"] is True
    assert safe_case["routing_gates"]["provider_model_configured"] is True
    assert safe_case["routing_gates"]["secret_ref_exists_or_no_key_local"] is True
    assert safe_case["routing_gates"]["fallback_inherits_same_gates"] is True
    assert safe_case["static_review_result"]["accepted_as_runtime_route"] is False
    assert safe_case["kernel_status"] == "proposed"
    assert safe_case["packet_status"] == "preview_only"


def test_v1_g5_fail_closed_cases_map_to_blocked_or_explain_plan() -> None:
    for case in _cases():
        if case["case_family"] == "safe_route_shape_static_only":
            continue
        assert case["packet_status"] in {"blocked", "explain_plan"}
        assert case["packet_status"] != "preview_only"
        assert case["static_review_result"]["accepted_as_runtime_route"] is False
        assert case["expected_blocked_claims"]


def test_v1_g5_routing_gates_fail_for_expected_cases() -> None:
    cases = {case["case_id"]: case for case in _cases()}
    assert (
        cases["v1_g5_private_data_requires_guardian_review"]["routing_gates"][
            "data_sensitivity_allowed"
        ]
        is False
    )
    assert (
        cases["v1_g5_expensive_model_requires_budget_review"]["routing_gates"][
            "budget_cost_policy_allows"
        ]
        is False
    )
    assert cases["v1_g5_unknown_provider_denied"]["routing_gates"]["provider_model_configured"] is False
    assert (
        cases["v1_g5_missing_secret_ref_blocks_route"]["routing_gates"][
            "secret_ref_exists_or_no_key_local"
        ]
        is False
    )
    assert (
        cases["v1_g5_tool_capable_model_without_tool_scope_blocked"]["routing_gates"][
            "tool_pack_scope_allows"
        ]
        is False
    )
    assert (
        cases["v1_g5_shell_disallowed_provider_denied"]["routing_gates"][
            "shell_allows_model_pack"
        ]
        is False
    )
    assert (
        cases["v1_g5_forged_route_decision_fail_closed"]["routing_gates"][
            "fallback_inherits_same_gates"
        ]
        is False
    )


def test_v1_g5_forged_route_decision_and_live_route_claim_fail_closed() -> None:
    forged = [
        case for case in _cases() if case["case_id"] == "v1_g5_forged_route_decision_fail_closed"
    ][0]
    assert forged["claimed_authority"]["decision_id_forged"] is True
    assert forged["claimed_authority"]["token_guardian_live_route"] is True
    assert forged["claimed_authority"]["approval_granted"] is True
    assert forged["static_review_result"]["forged_route_decision_rejected"] is True
    assert "token_guardian_live_route_claim" in forged["expected_blocked_claims"]
    assert "fallback_policy_bypass_claim" in forged["expected_blocked_claims"]


def test_v1_g5_cases_never_call_models_or_read_secrets() -> None:
    for case in _cases():
        flags = case["control_flags"]
        assert flags["non_authoritative"] is True
        assert flags["safe_by_default"] is True
        assert flags["local_only"] is True
        assert flags["deterministic"] is True
        for key in (
            "provider_model_routing_active",
            "provider_model_call_allowed",
            "provider_readiness_check_allowed",
            "token_guardian_live_route_allowed",
            "fallback_execution_allowed",
            "secret_lookup_allowed",
            "raw_secret_allowed",
            "raw_private_context_in_audit_allowed",
            "guardian_decision_created",
            "approval_granted",
            "execution_allowed",
            "dispatch_allowed",
            "persistence_allowed",
            "external_calls_allowed",
            "tool_calls_allowed",
            "driver_calls_allowed",
            "adapter_calls_allowed",
            "file_mutation_allowed",
            "connector_mutation_allowed",
            "audit_persistence_allowed",
            "browser_file_network_device_robotics_allowed",
            "haptic_device_behavior_allowed",
            "physical_world_allowed",
            "runtime_test_harness_active",
        ):
            assert flags[key] is False


def test_v1_g5_case_suite_does_not_touch_runtime_or_support_paths() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*v1_g5*"))
    support = REPO_ROOT / "tests" / "support"
    if support.exists():
        assert not list(support.rglob("*v1_g5*"))
