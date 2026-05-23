"""Phase 43.2 universal contract profile regression tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from lima.kernel.candidate_preview import preview_candidate

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_43_1_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_43_1_universal_contract_profile_fixtures.json"
)
PHASE_43_2_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_43_2_universal_contract_profile_regression_tests.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def _fixture_cases() -> list[dict[str, Any]]:
    cases = _load_json(PHASE_43_1_FIXTURE_PATH)["cases"]
    assert isinstance(cases, list)
    return cases


def _candidate_data(case: dict[str, Any]) -> dict[str, Any]:
    return {
        "candidate_id": f"phase-43-2:{case['id']}",
        "candidate_status": case["expected_profile_state"],
        "summary": case["summary"],
        "provenance": {
            "source": "phase_43_1_fixture",
            "case_id": case["id"],
            "profile_kind": case["profile_kind"],
        },
        "profile_metadata": case["profile"],
        "control_flags": case["control_flags"],
        "execution_allowed": False,
        "side_effects_allowed": False,
        "approval_granted": False,
        "dispatch_allowed": False,
        "persistence_allowed": False,
    }


def test_phase_43_2_regression_metadata_matches_fixture_corpus() -> None:
    phase_43_1 = _load_json(PHASE_43_1_FIXTURE_PATH)
    phase_43_2 = _load_json(PHASE_43_2_FIXTURE_PATH)
    assert phase_43_2["phase"] == "43.2"
    assert phase_43_2["docs_tests_fixtures_only"] is True
    assert phase_43_2["regression_tests_only"] is True
    assert phase_43_2["uses_existing_helper_only"] is True
    assert phase_43_2["expected_case_count"] == len(phase_43_1["cases"])
    assert phase_43_2["lima_runtime_files_changed"] is False
    assert phase_43_2["sparkbot_files_changed"] is False
    assert phase_43_2["tests_support_changed"] is False
    assert phase_43_2["runtime_behavior_changed"] is False


def test_phase_43_2_candidate_preview_is_deterministic_for_universal_profiles() -> None:
    for case in _fixture_cases():
        candidate_data = _candidate_data(case)
        first_preview = preview_candidate(candidate_data)
        second_preview = preview_candidate(candidate_data)
        assert first_preview == second_preview


def test_phase_43_2_candidate_preview_preserves_all_inert_flags() -> None:
    required_flags = _load_json(PHASE_43_2_FIXTURE_PATH)["required_preview_flags"]
    for case in _fixture_cases():
        preview = preview_candidate(_candidate_data(case))
        for key, expected_value in required_flags.items():
            assert preview[key] is expected_value


def test_phase_43_2_risky_and_adversarial_profiles_stay_blocked() -> None:
    blocked_ids = set(_load_json(PHASE_43_2_FIXTURE_PATH)["must_remain_blocked_profile_ids"])
    cases = {case["id"]: case for case in _fixture_cases()}
    for case_id in blocked_ids:
        preview = preview_candidate(_candidate_data(cases[case_id]))
        assert preview["preview_state"] == "blocked"
        assert preview["normalized_status"] == "blocked"
        assert preview["status_reason"] in {
            "caller_provided_claim_not_allowed_for_candidate_preview",
            "candidate_preview_blocked",
        }


def test_phase_43_2_safe_planning_profiles_never_gain_authority() -> None:
    blocked_ids = set(_load_json(PHASE_43_2_FIXTURE_PATH)["must_remain_blocked_profile_ids"])
    for case in _fixture_cases():
        if case["id"] in blocked_ids:
            continue
        preview = preview_candidate(_candidate_data(case))
        assert preview["preview_state"] in {"proposed", "needs_review", "blocked"}
        assert preview["approval_granted"] is False
        assert preview["execution_allowed"] is False
        assert preview["dispatch_allowed"] is False
        assert preview["persistence_allowed"] is False
        assert preview["external_calls_allowed"] is False
        assert preview["robotics_allowed"] is False
        assert preview["physical_world_allowed"] is False


def test_phase_43_2_stays_out_of_runtime_and_tests_support() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_43_2*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_43_2*"))
