"""Phase 41.3 Arc Bot hardening gap review tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_41_3_arc_bot_hardening_gap_and_next_lane_review.json"
)
PHASE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_41_3_ARC_BOT_HARDENING_GAP_AND_NEXT_LANE_REVIEW.md"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_41_3_reviews_phase_41_evidence() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "41.3"
    assert fixture["evidence_reviewed"] == [
        "phase_41_0_charter",
        "phase_41_1_fixture_corpus",
        "phase_41_2_regression_tests",
    ]
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["test_only_hardening"] is True


def test_phase_41_3_records_safe_hardening_findings() -> None:
    findings = _load_json(PHASE_FIXTURE_PATH)["findings"]
    assert findings["benign_draft_email_safe"] is True
    assert findings["risky_external_write_blocked"] is True
    assert findings["calendar_write_blocked"] is True
    assert findings["file_mutation_blocked"] is True
    assert findings["memory_persistence_blocked"] is True
    assert findings["scheduled_work_blocked"] is True
    assert findings["admin_breakglass_blocked"] is True
    assert findings["sparkbot_only_behavior_blocked"] is True
    assert findings["robotics_physical_world_blocked"] is True
    assert findings["strict_security_conservatively_blocked"] is True
    assert findings["conservative_blocking_accepted"] is True


def test_phase_41_3_finds_no_runtime_gap() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["remaining_gaps"] == []
    assert fixture["runtime_gap_found"] is False
    assert fixture["runtime_change_needed"] is False
    assert fixture["lima_change_needed"] is False
    assert fixture["tests_support_change_needed"] is False
    assert "No concrete runtime gap was found." in PHASE_DOC_PATH.read_text(encoding="utf-8")


def test_phase_41_3_recommends_archive_not_runtime() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase_41_4_recommended"] is True
    assert fixture["phase_41_4_lane"] == "docs_tests_fixtures_only_archive_closeout"
    assert fixture["next_runtime_implementation_recommended"] is False


def test_phase_41_3_stays_in_approved_scope() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["runtime_behavior_changed"] is False
    assert not list((REPO_ROOT / "lima").rglob("*phase_41_3*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_41_3*"))
