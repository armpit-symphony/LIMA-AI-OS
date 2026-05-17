"""Phase 41.4 Arc Bot candidate preview hardening archive tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "PHASE_41_4_ARC_BOT_CANDIDATE_PREVIEW_HARDENING_ARCHIVE_CLOSEOUT.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_41_4_arc_bot_candidate_preview_hardening_archive_closeout.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_41_4_archives_all_phase_41_phases() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "41.4"
    assert fixture["test_only_hardening_archived"] is True
    assert fixture["completed_phases"] == ["41.0", "41.1", "41.2", "41.3", "41.4"]
    assert fixture["docs_tests_fixtures_only"] is True


def test_phase_41_4_records_arc_bot_fixture_coverage() -> None:
    coverage = set(_load_json(PHASE_FIXTURE_PATH)["coverage_added"])
    assert "draft_email_no_send" in coverage
    assert "external_email_send_request" in coverage
    assert "calendar_write_request" in coverage
    assert "file_mutation_request" in coverage
    assert "low_confidence_memory_fact" in coverage
    assert "connector_missing_secret" in coverage
    assert "agent_identity_kill_switch" in coverage
    assert "robotics_physical_world_request" in coverage
    assert "sparkbot_only_behavior_rejected" in coverage
    assert "explain_plan_only_risky_request" in coverage


def test_phase_41_4_archives_candidate_preview_boundary() -> None:
    boundary = _load_json(PHASE_FIXTURE_PATH)["candidate_preview_boundary"]
    assert boundary["deterministic"] is True
    assert boundary["read_only"] is True
    assert boundary["local_only"] is True
    assert boundary["non_authoritative"] is True
    assert boundary["safe_by_default"] is True
    for key in (
        "execution_allowed",
        "side_effects_allowed",
        "approval_granted",
        "dispatch_allowed",
        "persistence_allowed",
        "humaninput_bridge_active",
        "sparkbot_wiring_active",
        "live_adapter_active",
        "external_calls_allowed",
        "robotics_allowed",
        "physical_world_allowed",
    ):
        assert boundary[key] is False


def test_phase_41_4_finds_no_runtime_gap_and_recommends_no_code_design_review() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["remaining_gaps"] == []
    assert fixture["runtime_gap_found"] is False
    assert fixture["runtime_change_needed"] is False
    assert fixture["runtime_implementation_recommended"] is False
    assert (
        fixture["recommended_next_direction"]
        == "docs_tests_fixtures_only_no_code_arc_bot_lima_office_consumer_contract_design_review"
    )
    text = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "No runtime change is needed." in text
    assert "docs/tests/fixtures-only no-code design review" in text


def test_phase_41_4_stays_in_approved_scope() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["candidate_preview_changed"] is False
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["runtime_behavior_changed"] is False
    assert not list((REPO_ROOT / "lima").rglob("*phase_41_4*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_41_4*"))
