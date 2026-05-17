"""Phase 40.4 Arc Bot consumer boundary archive tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_40_4_ARC_BOT_CONSUMER_BOUNDARY_ARCHIVE_CLOSEOUT.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_40_4_arc_bot_consumer_boundary_archive_closeout.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_40_4_archives_all_phase_40_phases() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "40.4"
    assert fixture["completed_phases"] == ["40.0", "40.1", "40.2", "40.3", "40.4"]
    assert fixture["sparkbot_reference_evidence_only"] is True
    assert fixture["primary_guarded_task_consumer"] == "arc_bot_lima_ai_office"
    assert fixture["lima_ai_os_runtime_safety_substrate_target"] is True


def test_phase_40_4_records_concept_classifications() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert "task_intake" in fixture["adopted"]
    assert "agent_identity_kill_switch" in fixture["adopted"]
    assert "operator_approval_boundary" in fixture["adapted_for_arc_bot_stricter_defaults"]
    assert "owner_local_execution_posture" in fixture["sparkbot_only"]
    assert "direct_sparkbot_integration" in fixture["deferred"]
    assert "runtime_authority_from_planning_labels" in fixture["rejected"]
    assert "inherited_sparkbot_owner_local_execution_in_lima_runtime" in fixture["rejected"]


def test_phase_40_4_recommends_phase_41_test_only_hardening() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase_41_recommended"] is True
    assert fixture["phase_41_lane"] == "docs_tests_fixtures_only_arc_bot_candidate_preview_hardening"
    assert fixture["runtime_implementation_recommended"] is False
    text = PHASE_DOC_PATH.read_text(encoding="utf-8")
    assert "Phase 41 should proceed as docs/tests/fixtures-only" in text
    assert "Phase 41 must not modify runtime code" in text


def test_phase_40_4_preserves_boundaries() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["runtime_behavior_changed"] is False
    assert fixture["phase_5_humaninput_bridge_remains_gated"] is True


def test_phase_40_4_stays_in_approved_scope() -> None:
    assert not list((REPO_ROOT / "lima").rglob("*phase_40_4*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_40_4*"))
