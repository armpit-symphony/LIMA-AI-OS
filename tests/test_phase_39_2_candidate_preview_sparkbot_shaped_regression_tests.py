"""Phase 39.2 Sparkbot-shaped candidate preview regression tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from lima.kernel.candidate_preview import preview_candidate

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_39_2_candidate_preview_sparkbot_shaped_regression_tests.json"
)
SPARKBOT_SHAPED_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_39_1_sparkbot_shaped_candidate_preview_fixtures.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def _assert_inert_preview(preview: dict[str, Any]) -> None:
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


def test_phase_39_2_records_regression_test_scope() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "39.2"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["runtime_files_changed"] is False
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["runtime_gap_found"] is False


def test_all_sparkbot_shaped_fixture_cases_are_tested() -> None:
    test_fixture = _load_json(PHASE_FIXTURE_PATH)
    data_fixture = _load_json(SPARKBOT_SHAPED_FIXTURE_PATH)
    assert set(test_fixture["cases_tested"]) == {case["case_id"] for case in data_fixture["cases"]}


def test_sparkbot_shaped_inputs_remain_blocked_and_inert() -> None:
    fixture = _load_json(SPARKBOT_SHAPED_FIXTURE_PATH)
    for case in fixture["cases"]:
        preview = preview_candidate(case["candidate"])
        assert preview["preview_state"] == case["expected_preview_state"]
        assert preview["normalized_status"] == "blocked"
        assert preview["status_reason"] == "caller_provided_claim_not_allowed_for_candidate_preview"
        assert "blocked_claims_present" in preview["warnings"]
        assert "preview_blocked" in preview["warnings"]
        assert set(case["expected_blocked_claims"]).issubset(set(preview["blocked_claims"]))
        _assert_inert_preview(preview)


def test_sparkbot_shaped_preview_output_is_deterministic() -> None:
    fixture = _load_json(SPARKBOT_SHAPED_FIXTURE_PATH)
    for case in fixture["cases"]:
        assert preview_candidate(case["candidate"]) == preview_candidate(dict(case["candidate"]))


def test_phase_39_2_assertions_match_inert_preview_contract() -> None:
    assertions = _load_json(PHASE_FIXTURE_PATH)["assertions"]
    assert assertions["deterministic_output"] is True
    assert assertions["all_cases_blocked"] is True
    assert assertions["expected_blocked_claims_present"] is True
    assert assertions["execution_allowed"] is False
    assert assertions["side_effects_allowed"] is False
    assert assertions["approval_granted"] is False
    assert assertions["dispatch_allowed"] is False
    assert assertions["persistence_allowed"] is False
    assert assertions["phase_5_humaninput_runtime_bridge_gated"] is True
    assert assertions["sparkbot_wiring_active"] is False
    assert assertions["robotics_allowed"] is False
    assert assertions["physical_world_allowed"] is False


def test_phase_39_2_files_are_not_under_runtime_or_support_paths() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_39_2*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_39_2*"))
