"""Static V1-G2 typed bridge fail-closed acceptance proof."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = REPO_ROOT / "tests" / "fixtures" / "runtime_extraction"
FAIL_CLOSED_FIXTURE_NAMES = (
    "typed_bridge_acceptance_fail_closed_approval_bypass.json",
    "typed_bridge_acceptance_fail_closed_runtime_claim.json",
    "typed_bridge_acceptance_fail_closed_missing_guardian_request.json",
    "typed_bridge_acceptance_fail_closed_execution_claim.json",
    "typed_bridge_acceptance_fail_closed_provider_model_tool_driver_claim.json",
    "typed_bridge_acceptance_fail_closed_browser_file_network_device_robotics_claim.json",
)


def _load_json(path: Path) -> dict[str, Any]:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _fail_closed_fixtures() -> list[dict[str, Any]]:
    return [_load_json(FIXTURE_DIR / name) for name in FAIL_CLOSED_FIXTURE_NAMES]


def test_v1_g2_fail_closed_fixture_files_exist() -> None:
    for fixture_name in FAIL_CLOSED_FIXTURE_NAMES:
        assert (FIXTURE_DIR / fixture_name).exists()


def test_v1_g2_fail_closed_cases_cover_required_claim_families() -> None:
    cases = {fixture["case_id"]: fixture for fixture in _fail_closed_fixtures()}
    assert set(cases) == {
        "typed_bridge_acceptance_fail_closed_approval_bypass",
        "typed_bridge_acceptance_fail_closed_runtime_claim",
        "typed_bridge_acceptance_fail_closed_missing_guardian_request",
        "typed_bridge_acceptance_fail_closed_execution_claim",
        "typed_bridge_acceptance_fail_closed_provider_model_tool_driver_claim",
        "typed_bridge_acceptance_fail_closed_browser_file_network_device_robotics_claim",
    }
    expected_claims = {
        "approval_bypass_claim",
        "runtime_behavior_claim",
        "guardian_decision_authority_claim",
        "missing_guardian_request_metadata",
        "execution_claim",
        "dispatch_claim",
        "persistence_claim",
        "provider_model_routing_claim",
        "model_call_claim",
        "tool_call_claim",
        "driver_call_claim",
        "browser_claim",
        "file_mutation_claim",
        "network_claim",
        "device_claim",
        "robotics_claim",
        "haptic_device_claim",
        "physical_world_claim",
    }
    actual_claims: set[str] = set()
    for fixture in cases.values():
        actual_claims.update(fixture["expected_blocked_claims"])
    assert expected_claims.issubset(actual_claims)


def test_v1_g2_fail_closed_cases_have_source_and_candidate_metadata() -> None:
    for fixture in _fail_closed_fixtures():
        assert fixture["docs_tests_fixtures_only"] is True
        source = fixture["source_request_metadata"]
        assert source["source_kind"] in {"automation_request", "bot_request", "shell_request"}
        assert source["tenant_id"]
        assert source["actor_id"]
        assert source["lineage_ref"]
        candidate = fixture["typed_intentenvelope_candidate_metadata"]
        assert candidate["candidate_status"] in {"blocked", "needs_review"}
        assert candidate["risk_class"] in {"high", "critical"}
        assert candidate["requested_tool_packs"]


def test_v1_g2_fail_closed_guardian_request_boundary_is_enforced() -> None:
    fixtures = _fail_closed_fixtures()
    missing_guardian = [
        fixture
        for fixture in fixtures
        if fixture["case_id"] == "typed_bridge_acceptance_fail_closed_missing_guardian_request"
    ][0]
    assert missing_guardian["guardian_request_metadata"] is None
    assert "missing_guardian_request_metadata" in missing_guardian["expected_blocked_claims"]
    for fixture in fixtures:
        if fixture is missing_guardian:
            continue
        guardian_request = fixture["guardian_request_metadata"]
        assert guardian_request["request_state"] == "blocked"
        assert guardian_request["policy_review_needed"] is True
        assert guardian_request["approval_posture"] == "not_granted"


def test_v1_g2_fail_closed_cases_never_create_authority() -> None:
    for fixture in _fail_closed_fixtures():
        decision = fixture["future_guardian_decision_metadata"]
        assert decision["state"] in {"pending", "blocked"}
        assert decision["decision_id"] is None
        assert decision["approval_granted"] is False
        assert decision["execution_allowed"] is False
        flags = fixture["control_flags"]
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
            "browser_file_network_device_robotics_allowed",
            "haptic_device_behavior_allowed",
            "physical_world_allowed",
            "guardian_decision_created",
            "runtime_test_harness_active",
        ):
            assert flags[key] is False


def test_v1_g2_fail_closed_packet_states_are_bounded() -> None:
    packet_statuses = {fixture["packet_status"] for fixture in _fail_closed_fixtures()}
    assert packet_statuses == {"blocked", "deferred"}
    for fixture in _fail_closed_fixtures():
        if fixture["case_id"] == "typed_bridge_acceptance_fail_closed_missing_guardian_request":
            assert fixture["kernel_status"] == "needs_review"
            assert fixture["packet_status"] == "deferred"
        else:
            assert fixture["kernel_status"] == "blocked"
            assert fixture["packet_status"] == "blocked"


def test_v1_g2_fail_closed_suite_does_not_touch_runtime_or_support_paths() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*typed_bridge_acceptance*"))
    support = REPO_ROOT / "tests" / "support"
    if support.exists():
        assert not list(support.rglob("*typed_bridge_acceptance*"))
