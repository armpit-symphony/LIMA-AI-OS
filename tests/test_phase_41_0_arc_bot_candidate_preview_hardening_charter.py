"""Phase 41.0 Arc Bot candidate preview hardening charter tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_DOC_PATH = (
    REPO_ROOT / "docs" / "PHASE_41_0_ARC_BOT_CANDIDATE_PREVIEW_HARDENING_CHARTER.md"
)
PHASE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "runtime_extraction"
    / "phase_41_0_arc_bot_candidate_preview_hardening_charter.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)
    assert isinstance(fixture, dict)
    return fixture


def test_phase_41_0_is_test_only_hardening() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["phase"] == "41.0"
    assert fixture["docs_tests_fixtures_only"] is True
    assert fixture["test_only_hardening"] is True
    assert fixture["runtime_implementation_approved"] is False
    assert fixture["lima_changes_allowed"] is False
    assert fixture["tests_support_changes_allowed"] is False
    assert "Phase 41 must not add runtime implementation" in PHASE_DOC_PATH.read_text(encoding="utf-8")


def test_phase_41_0_includes_arc_bot_fixture_targets() -> None:
    targets = set(_load_json(PHASE_FIXTURE_PATH)["hardening_targets"])
    assert "draft_email_no_send" in targets
    assert "external_email_send_request" in targets
    assert "calendar_write_request" in targets
    assert "file_mutation_request" in targets
    assert "low_confidence_memory_fact" in targets
    assert "connector_missing_secret" in targets
    assert "agent_identity_kill_switch" in targets
    assert "robotics_physical_world_request" in targets
    assert "sparkbot_only_behavior_rejected" in targets
    assert "explain_plan_only_risky_request" in targets


def test_phase_41_0_preserves_candidate_preview_invariants() -> None:
    invariants = _load_json(PHASE_FIXTURE_PATH)["hard_invariants"]
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
        assert invariants[key] is False
    assert invariants["non_authoritative"] is True
    assert invariants["safe_by_default"] is True
    assert invariants["preview_type"] == "candidate_preview"


def test_phase_41_0_stays_in_approved_scope() -> None:
    fixture = _load_json(PHASE_FIXTURE_PATH)
    assert fixture["lima_runtime_files_changed"] is False
    assert fixture["sparkbot_files_changed"] is False
    assert fixture["tests_support_changed"] is False
    assert fixture["runtime_behavior_changed"] is False
    assert not list((REPO_ROOT / "lima").rglob("*phase_41_0*"))
    assert not list((REPO_ROOT / "tests" / "support").rglob("*phase_41_0*"))
