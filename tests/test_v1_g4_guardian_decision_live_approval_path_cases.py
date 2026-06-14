"""Static case checks for the V1-G4 GuardianDecision/live approval gate."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = REPO_ROOT / "tests" / "fixtures" / "runtime_extraction"
CASE_NAMES = (
    "v1_g4_allow_readonly_decision_shape.json",
    "v1_g4_confirm_destructive_edit_requires_approval.json",
    "v1_g4_deny_unknown_tool_pack.json",
    "v1_g4_privileged_breakglass_requires_scope.json",
    "v1_g4_expired_decision_rejected.json",
    "v1_g4_revoked_approval_rejected.json",
    "v1_g4_block_missing_decision_id.json",
    "v1_g4_forged_decision_id_fail_closed.json",
)


def _load_json(path: Path) -> dict[str, Any]:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(fixture, dict)
    return fixture


def _cases() -> list[dict[str, Any]]:
    return [_load_json(FIXTURE_DIR / name) for name in CASE_NAMES]


def test_v1_g4_case_fixture_files_exist() -> None:
    for fixture_name in CASE_NAMES:
        assert (FIXTURE_DIR / fixture_name).exists()


def test_v1_g4_cases_cover_all_required_outcome_families() -> None:
    cases = _cases()
    assert {case["future_decision_outcome_family"] for case in cases} == {
        "allow",
        "confirm",
        "deny",
        "privileged",
        "expired",
        "revoked",
        "blocked",
    }
    blocked_cases = [
        case for case in cases if case["future_decision_outcome_family"] == "blocked"
    ]
    assert {case["case_family"] for case in blocked_cases} == {
        "blocked_missing_authority_static_only",
        "blocked_forged_authority_static_only",
    }


def test_v1_g4_cases_keep_decision_and_approval_authority_static_only() -> None:
    for case in _cases():
        assert case["docs_tests_fixtures_only"] is True
        decision_scope = case["decision_scope_design"]
        assert decision_scope["decision_id_required_in_future_runtime"] is True
        assert decision_scope["decision_id_issued_in_fixture"] is False
        approval = case["approval_path_design"]
        assert approval["approval_id_issued_in_fixture"] is False
        assert approval["approval_granted"] is False
        assert approval["approval_token_issued"] is False
        review = case["static_review_result"]
        assert review["accepted_as_static_evidence"] is True
        assert review["accepted_as_runtime_authority"] is False


def test_v1_g4_cases_map_outcomes_to_safe_packet_states() -> None:
    expected_packet_status = {
        "allow": "preview_only",
        "confirm": "explain_plan",
        "deny": "blocked",
        "privileged": "blocked",
        "expired": "blocked",
        "revoked": "blocked",
        "blocked": "blocked",
    }
    for case in _cases():
        outcome = case["future_decision_outcome_family"]
        assert case["packet_status"] == expected_packet_status[outcome]


def test_v1_g4_risky_cases_require_approval_or_blocking() -> None:
    risky_cases = [case for case in _cases() if case["action"]["consequential"] is True]
    for case in risky_cases:
        outcome = case["future_decision_outcome_family"]
        if outcome in {"confirm", "privileged", "revoked", "blocked"}:
            assert case["approval_path_design"]["approval_metadata_required"] is True
        assert case["packet_status"] in {"explain_plan", "blocked"}
        assert case["control_flags"]["execution_allowed"] is False


def test_v1_g4_forged_and_missing_authority_fail_closed() -> None:
    cases = {case["case_id"]: case for case in _cases()}
    missing = cases["v1_g4_block_missing_decision_id"]
    assert missing["future_decision_outcome_family"] == "blocked"
    assert "missing_decision_id" in missing["expected_blocked_claims"]
    assert "missing_guardian_authority" in missing["expected_blocked_claims"]
    forged = cases["v1_g4_forged_decision_id_fail_closed"]
    assert forged["claimed_authority"]["decision_id_forged"] is True
    assert forged["claimed_authority"]["approval_granted"] is True
    assert forged["static_review_result"]["forged_decision_id_rejected"] is True
    assert forged["approval_path_design"]["claimed_static_approval_rejected"] is True
    assert "forged_decision_id" in forged["expected_blocked_claims"]
    assert "approval_bypass_claim" in forged["expected_blocked_claims"]


def test_v1_g4_cases_never_create_runtime_authority_or_side_effects() -> None:
    for case in _cases():
        flags = case["control_flags"]
        assert flags["non_authoritative"] is True
        assert flags["safe_by_default"] is True
        assert flags["local_only"] is True
        assert flags["deterministic"] is True
        for key in (
            "decision_id_created",
            "approval_granted",
            "approval_token_issued",
            "execution_allowed",
            "dispatch_allowed",
            "persistence_allowed",
            "external_calls_allowed",
            "provider_model_routing_allowed",
            "model_calls_allowed",
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


def test_v1_g4_case_suite_does_not_touch_runtime_or_support_paths() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*v1_g4*"))
    support = REPO_ROOT / "tests" / "support"
    if support.exists():
        assert not list(support.rglob("*v1_g4*"))
