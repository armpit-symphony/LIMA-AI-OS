"""Phase 41.2 Arc Bot candidate preview regression tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from lima.kernel.candidate_preview import preview_candidate

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_41_1_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_41_1_arc_bot_candidate_preview_fixtures.json"
)

EXPECTED_HELPER_RESULTS = {
    "draft_email_no_send": ("proposed", ()),
    "external_email_send_request": ("blocked", ("dispatch_claim",)),
    "calendar_write_request": ("blocked", ("file_mutation_claim",)),
    "file_mutation_request": ("blocked", ("file_mutation_claim",)),
    "low_confidence_memory_fact": ("blocked", ("persistence_claim",)),
    "connector_missing_secret": ("blocked", ()),
    "agent_identity_kill_switch": ("blocked", ("authority_claim",)),
    "scheduled_task_requires_approval": (
        "blocked",
        ("authority_claim", "background_work_claim"),
    ),
    "admin_breakglass_request": ("blocked", ("authority_claim",)),
    "robotics_physical_world_request": ("blocked", ("robotics_physical_world_claim",)),
    "sparkbot_only_behavior_rejected": (
        "blocked",
        (
            "execution_claim",
            "live_adapter_claim",
            "shell_browser_network_claim",
            "sparkbot_claim",
        ),
    ),
    "strict_security_default_posture": ("blocked", ("authority_claim",)),
    "explain_plan_only_risky_request": (
        "blocked",
        ("execution_claim", "file_mutation_claim"),
    ),
}


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def _fixture_cases() -> list[dict[str, Any]]:
    cases = _load_json(PHASE_41_1_FIXTURE_PATH)["cases"]
    assert isinstance(cases, list)
    return cases


def test_phase_41_2_candidate_preview_outputs_match_safe_expected_results() -> None:
    for case in _fixture_cases():
        preview = preview_candidate(case["candidate_data"])
        expected_state, expected_claims = EXPECTED_HELPER_RESULTS[case["id"]]
        assert preview["preview_state"] == expected_state
        assert tuple(preview["blocked_claims"]) == expected_claims
        assert preview["normalized_status"] == expected_state


def test_phase_41_2_candidate_preview_is_deterministic_for_arc_bot_fixtures() -> None:
    for case in _fixture_cases():
        first_preview = preview_candidate(case["candidate_data"])
        second_preview = preview_candidate(case["candidate_data"])
        assert first_preview == second_preview


def test_phase_41_2_candidate_preview_preserves_all_inert_flags() -> None:
    for case in _fixture_cases():
        preview = preview_candidate(case["candidate_data"])
        assert preview["preview_type"] == "candidate_preview"
        assert preview["non_authoritative"] is True
        assert preview["read_only"] is True
        assert preview["local_only"] is True
        assert preview["deterministic"] is True
        assert preview["safe_by_default"] is True
        assert preview["execution_allowed"] is False
        assert preview["side_effects_allowed"] is False
        assert preview["approval_granted"] is False
        assert preview["dispatch_allowed"] is False
        assert preview["persistence_allowed"] is False
        assert preview["phase_5_humaninput_runtime_bridge_gated"] is True
        assert preview["humaninput_bridge_active"] is False
        assert preview["sparkbot_wiring_active"] is False
        assert preview["live_adapter_active"] is False
        assert preview["external_calls_allowed"] is False
        assert preview["robotics_allowed"] is False
        assert preview["physical_world_allowed"] is False


def test_phase_41_2_risky_arc_bot_cases_never_become_authoritative_or_ready() -> None:
    benign_ids = {"draft_email_no_send"}
    for case in _fixture_cases():
        preview = preview_candidate(case["candidate_data"])
        if case["id"] in benign_ids:
            assert preview["preview_state"] == "proposed"
            continue
        assert preview["preview_state"] == "blocked"
        assert preview["status_reason"] in {
            "caller_provided_claim_not_allowed_for_candidate_preview",
            "connector_missing_secret_setup_required",
        }


def test_phase_41_2_stays_in_approved_scope() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_41_2*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_41_2*"))
